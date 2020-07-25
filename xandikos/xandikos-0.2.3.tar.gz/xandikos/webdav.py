# Xandikos
# Copyright (C) 2016-2017 Jelmer Vernooĳ <jelmer@jelmer.uk>, et al.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 3
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Abstract WebDAV server implementation..

This module contains an abstract WebDAV server. All caldav/carddav specific
functionality should live in xandikos.caldav/xandikos.carddav respectively.
"""

# TODO(jelmer): Add authorization support

import asyncio
import collections
import fnmatch
import functools
import logging
import os
import posixpath
from typing import (
    Callable,
    Dict,
    Iterable,
    AsyncIterable,
    List,
    Optional,
    Union,
    Tuple,
    Sequence,
)
import urllib.parse
from wsgiref.util import request_uri

from defusedxml.ElementTree import fromstring as xmlparse
# Hmm, defusedxml doesn't have XML generation functions? :(
from xml.etree import ElementTree as ET

DEFAULT_ENCODING = 'utf-8'
COLLECTION_RESOURCE_TYPE = '{DAV:}collection'
PRINCIPAL_RESOURCE_TYPE = '{DAV:}principal'


PropStatus = collections.namedtuple(
    'PropStatus', ['statuscode', 'responsedescription', 'prop'])


class BadRequestError(Exception):
    """Base class for bad request errors."""

    def __init__(self, message):
        super(BadRequestError, self).__init__(message)
        self.message = message


class NotAcceptableError(Exception):
    """Base class for not acceptable errors."""

    def __init__(self, available_content_types, acceptable_content_types):
        super(NotAcceptableError, self).__init__(
            "Unable to convert from content types %r to one of %r" % (
                available_content_types, acceptable_content_types))
        self.available_content_types = available_content_types
        self.acceptable_content_types = acceptable_content_types


class UnsupportedMediaType(Exception):
    """Base class for unsupported media type errors."""

    def __init__(self, content_type):
        super(UnsupportedMediaType, self).__init__(
            "Unsupported media type: %r" % (content_type, ))
        self.content_type = content_type


class UnauthorizedError(Exception):
    """Base class for unauthorized errors."""

    def __init__(self):
        super(UnauthorizedError, self).__init__(
            "Request unauthorized")


class Response(object):
    """Generic wrapper for HTTP-style responses.
    """

    def __init__(self, status=200, reason='OK', body=None, headers=None):
        if isinstance(status, str):
            self.status = int(status.split(' ', 1)[0])
            self.reason = status.split(' ', 1)[1]
        else:
            self.status = status
            self.reason = reason
        self.body = body or []
        if isinstance(headers, dict):
            self.headers = list(headers.items())
        elif isinstance(headers, list):
            self.headers = list(headers)
        elif not headers:
            self.headers = []
        else:
            raise TypeError(headers)

    def for_wsgi(self, start_response):
        start_response(
            '%d %s' % (self.status, self.reason),
            self.headers)
        return self.body

    def for_aiohttp(self):
        from aiohttp import web
        if isinstance(self.body, list):
            body = b''.join(self.body)
        else:
            body = self.body
        return web.Response(
            status=self.status, reason=self.reason,
            headers=self.headers, body=body)


def pick_content_types(accepted_content_types, available_content_types):
    """Pick best content types for a client.

    :param accepted_content_types: Accept variable (as name, params tuples)
    :raise NotAcceptableError: If there are no overlapping content types
    """
    available_content_types = set(available_content_types)
    acceptable_by_q = {}
    for ct, params in accepted_content_types:
        acceptable_by_q.setdefault(float(params.get('q', '1')), []).append(ct)
    if 0 in acceptable_by_q:
        # Items with q=0 are not acceptable
        for pat in acceptable_by_q[0]:
            available_content_types -= set(fnmatch.filter(
                available_content_types, pat))
        del acceptable_by_q[0]
    for q, pats in sorted(acceptable_by_q.items(), reverse=True):
        ret = []
        for pat in pats:
            ret.extend(fnmatch.filter(available_content_types, pat))
        if ret:
            return ret
    raise NotAcceptableError(
        available_content_types, accepted_content_types)


def parse_type(content_type):
    """Parse a content-type style header.

    :param content_type: type to parse
    :return: Tuple with base name and dict with params
    """
    params = {}
    try:
        (ct, rest) = content_type.split(';', 1)
    except ValueError:
        ct = content_type
    else:
        for param in rest.split(';'):
            (key, val) = param.split('=')
            params[key.strip()] = val.strip()
    return (ct, params)


def parse_accept_header(accept):
    """Parse a HTTP Accept or Accept-Language header.

    :param accept: Accept header contents
    :return: List of (content_type, params) tuples
    """
    ret = []
    for part in accept.split(','):
        part = part.strip()
        if not part:
            continue
        ret.append(parse_type(part))
    return ret


class PreconditionFailure(Exception):
    """A precondition failed."""

    def __init__(self, precondition, description):
        self.precondition = precondition
        self.description = description


class InsufficientStorage(Exception):
    """Insufficient storage."""


class ResourceLocked(Exception):
    """Resource locked."""


def etag_matches(condition, actual_etag):
    """Check if an etag matches an If-Matches condition.

    :param condition: Condition (e.g. '*', '"foo"' or '"foo", "bar"'
    :param actual_etag: ETag to compare to. None nonexistant
    :return: bool indicating whether condition matches
    """
    if actual_etag is None and condition:
        return False
    for etag in condition.split(','):
        if etag.strip(' ') == '*':
            return True
        if etag.strip(' ') == actual_etag:
            return True
    return False


class NeedsMultiStatus(Exception):
    """Raised when a response needs multi-status (e.g. for propstat)."""


def propstat_by_status(propstat):
    """Sort a list of propstatus objects by HTTP status.

    :param propstat: List of PropStatus objects:
    :return: dictionary mapping HTTP status code to list of PropStatus objects
    """
    bystatus = {}
    for propstat in propstat:
        (bystatus
         .setdefault((propstat.statuscode, propstat.responsedescription), [])
         .append(propstat.prop))
    return bystatus


def propstat_as_xml(propstat):
    """Format a list of propstats as XML elements.

    :param propstat: List of PropStatus objects
    :return: Iterator over {DAV:}propstat elements
    """
    bystatus = propstat_by_status(propstat)
    for (status, rd), props in sorted(bystatus.items()):
        propstat = ET.Element('{DAV:}propstat')
        ET.SubElement(propstat, '{DAV:}status').text = 'HTTP/1.1 ' + status
        if rd:
            ET.SubElement(propstat, '{DAV:}responsedescription').text = rd
        propresp = ET.SubElement(propstat, '{DAV:}prop')
        for prop in props:
            propresp.append(prop)
        yield propstat


def path_from_environ(environ, name):
    """Return a path from an environ dict.

    Will re-decode using a different encoding as necessary.
    """
    # Re-decode using DEFAULT_ENCODING. PEP-3333 says that
    # everything will be decoded using iso-8859-1.
    # See also https://bugs.python.org/issue16679
    path = environ[name].encode('iso-8859-1').decode(DEFAULT_ENCODING)
    return posixpath.normpath(path)


class Status(object):
    """A DAV response that can be used in multi-status."""

    def __init__(self, href, status=None, error=None, responsedescription=None,
                 propstat=None):
        self.href = str(href)
        self.status = status
        self.error = error
        self.propstat = propstat
        self.responsedescription = responsedescription

    def __repr__(self):
        return "<%s(%r, %r, %r)>" % (
            type(self).__name__,
            self.href, self.status, self.responsedescription
        )

    def get_single_body(self, encoding):
        if self.propstat and len(propstat_by_status(self.propstat)) > 1:
            raise NeedsMultiStatus()
        if self.error is not None:
            raise NeedsMultiStatus()
        if self.propstat:
            [ret] = list(propstat_as_xml(self.propstat))
            body = ET.tostringlist(ret, encoding)
            return body, ('text/xml; encoding="%s"' % encoding)
        else:
            body = (
                [self.responsedescription.encode(encoding)]
                if self.responsedescription
                else [])
            return body, ('text/plain; encoding="%s"' % encoding)

    def aselement(self):
        ret = ET.Element('{DAV:}response')
        ret.append(create_href(self.href))
        if self.propstat:
            for ps in propstat_as_xml(self.propstat):
                ret.append(ps)
        elif self.status:
            ET.SubElement(ret, '{DAV:}status').text = 'HTTP/1.1 ' + self.status
        # Note the check for "is not None" here. Elements without children
        # evaluate to False.
        if self.error is not None:
            ET.SubElement(ret, '{DAV:}error').append(self.error)
        if self.responsedescription:
            ET.SubElement(ret, '{DAV:}responsedescription').text = (
                self.responsedescription)
        return ret


def multistatus(req_fn):

    async def wrapper(self, environ, *args, **kwargs):
        responses = []
        async for resp in req_fn(self, environ, *args, **kwargs):
            responses.append(resp)
        return _send_dav_responses(responses, DEFAULT_ENCODING)

    return wrapper


class Resource(object):
    """A WebDAV resource."""

    # A list of resource type names (e.g. '{DAV:}collection')
    resource_types: List[str] = []

    # TODO(jelmer): Be consistent in using get/set functions vs properties.
    def set_resource_types(self, resource_types):
        """Set the resource types."""
        raise NotImplementedError(self.set_resource_types)

    def get_displayname(self):
        """Get the resource display name."""
        raise KeyError

    def set_displayname(self, displayname):
        """Set the resource display name."""
        raise NotImplementedError(self.set_displayname)

    def get_creationdate(self):
        """Get the resource creation date.

        :return: A datetime object
        """
        raise NotImplementedError(self.get_creationdate)

    def get_supported_locks(self):
        """Get the list of supported locks.

        This should return a list of (lockscope, locktype) tuples.
        Known lockscopes are LOCK_SCOPE_EXCLUSIVE, LOCK_SCOPE_SHARED
        Known locktypes are LOCK_TYPE_WRITE
        """
        raise NotImplementedError(self.get_supported_locks)

    def get_active_locks(self):
        """Return the list of active locks.

        :return: A list of ActiveLock tuples
        """
        raise NotImplementedError(self.get_active_locks)

    def get_content_type(self):
        """Get the content type for the resource.

        This is a mime type like text/plain
        """
        raise NotImplementedError(self.get_content_type)

    def get_owner(self):
        """Get an href identifying the owner of the resource.

        Can be None if owner information is not known.
        """
        raise NotImplementedError(self.get_owner)

    async def get_etag(self):
        """Get the etag for this resource.

        Contains the ETag header value (from Section 14.19 of [RFC2616]) as it
        would be returned by a GET without accept headers.
        """
        raise NotImplementedError(self.get_etag)

    async def get_body(self):
        """Get resource contents.

        :return: Iterable over bytestrings."""
        raise NotImplementedError(self.get_body)

    async def render(self, self_url, accepted_content_types,
                     accepted_languages):
        """'Render' this resource in the specified content type.

        The default implementation just checks that the
        resource' content type is acceptable and if so returns
        (get_body(), get_content_type(), get_content_language()).

        :param accepted_content_types: List of accepted content types
        :param accepted_languages: List of accepted languages
        :raise NotAcceptableError: if there is no acceptable content type
        :return: Tuple with (content_body, content_length, etag, content_type,
                 content_language)
        """
        # TODO(jelmer): Check content_language
        content_types = pick_content_types(
            accepted_content_types, [self.get_content_type()])
        assert content_types == [self.get_content_type()]
        body = await self.get_body()
        try:
            content_language = self.get_content_language()
        except KeyError:
            content_language = None
        return (body, sum(map(len, body)), await self.get_etag(),
                self.get_content_type(), content_language)

    async def get_content_length(self):
        """Get content length.

        :return: Length of this objects content.
        """
        return sum(map(len, await self.get_body()))

    def get_content_language(self):
        """Get content language.

        :return: Language, as used in HTTP Accept-Language
        """
        raise NotImplementedError(self.get_content_language)

    def set_body(self, body, replace_etag=None):
        """Set resource contents.

        :param body: Iterable over bytestrings
        :return: New ETag
        """
        raise NotImplementedError(self.set_body)

    def set_comment(self, comment):
        """Set resource comment.

        :param comment: New comment
        """
        raise NotImplementedError(self.set_comment)

    def get_comment(self):
        """Get resource comment.

        :return: comment
        """
        raise NotImplementedError(self.get_comment)

    def get_last_modified(self):
        """Get last modified time.

        :return: Last modified time
        """
        raise NotImplementedError(self.get_last_modified)

    def get_is_executable(self):
        """Get executable bit.

        :return: Boolean indicating executability
        """
        raise NotImplementedError(self.get_is_executable)

    def set_is_executable(self, executable):
        """Set executable bit.

        :param executable: Boolean indicating executability
        """
        raise NotImplementedError(self.set_is_executable)

    def get_quota_used_bytes(self):
        """Return bytes consumed by this resource.

        If unknown, this can raise KeyError.

        :return: an integer
        """
        raise NotImplementedError(self.get_quota_used_bytes)

    def get_quota_available_bytes(self):
        """Return quota available as bytes.

        This can raise KeyError if there is infinite quota available.
        """
        raise NotImplementedError(self.get_quota_available_bytes)


class Property(object):
    """Handler for listing, retrieving and updating DAV Properties."""

    # Property name (e.g. '{DAV:}resourcetype')
    name: str

    # Whether to include this property in 'allprop' PROPFIND requests.
    # https://tools.ietf.org/html/rfc4918, section 14.2
    in_allprops: bool = True

    # Resource type this property belongs to. If None, get_value()
    # will always be called.
    resource_type: Optional[Sequence[str]] = None

    # Whether this property is live (i.e set by the server)
    live: bool

    def supported_on(self, resource: Resource) -> bool:
        if self.resource_type is None:
            return True
        if isinstance(self.resource_type, tuple):
            return any(rs in resource.resource_types
                       for rs in self.resource_type)
        if self.resource_type in resource.resource_types:
            return True
        return False

    async def is_set(self,
                     href: str,
                     resource: Resource,
                     environ: Dict[str, str]) -> bool:
        """Check if this property is set on a resource."""
        if not self.supported_on(resource):
            return False
        try:
            await self.get_value('/', resource, ET.Element(self.name), environ)
        except KeyError:
            return False
        else:
            return True

    async def get_value(self, href: str, resource: Resource, el: ET.Element,
                        environ: Dict[str, str]) -> None:
        """Get property with specified name.

        :param href: Resource href
        :param resource: Resource for which to retrieve the property
        :param el: Element to populate
        :param environ: WSGI environment dict
        :raise KeyError: if this property is not present
        """
        raise KeyError(self.name)

    def set_value(self, href: str, resource: Resource, el: ET.Element) -> None:
        """Set property.

        :param href: Resource href
        :param resource: Resource to modify
        :param el: Element to get new value from (None to remove property)
        :raise NotImplementedError: to indicate this property can not be set
            (i.e. is protected)
        """
        raise NotImplementedError(self.set_value)


class ResourceTypeProperty(Property):
    """Provides {DAV:}resourcetype."""

    name = '{DAV:}resourcetype'

    resource_type = None

    live = True

    async def get_value(self, href, resource, el, environ):
        for rt in resource.resource_types:
            ET.SubElement(el, rt)

    def set_value(self, href, resource, el):
        resource.set_resource_types([e.tag for e in el])


class DisplayNameProperty(Property):
    """Provides {DAV:}displayname.

    https://tools.ietf.org/html/rfc4918, section 5.2
    """

    name = '{DAV:}displayname'
    resource_type = None

    async def get_value(self, href, resource, el, environ):
        el.text = resource.get_displayname()

    def set_value(self, href, resource, el):
        resource.set_displayname(el.text)


class GetETagProperty(Property):
    """Provides {DAV:}getetag.

    https://tools.ietf.org/html/rfc4918, section 15.6
    """

    name = '{DAV:}getetag'
    resource_type = None
    live = True

    async def get_value(self, href, resource, el, environ):
        el.text = await resource.get_etag()


ADD_MEMBER_FEATURE = 'add-member'


class AddMemberProperty(Property):
    """Provides {DAV:}add-member.

    https://tools.ietf.org/html/rfc5995, section 3.2.1
    """

    name = '{DAV:}add-member'
    resource_type = COLLECTION_RESOURCE_TYPE
    live = True

    async def get_value(self, href, resource, el, environ):
        # Support POST against collection URL
        el.append(create_href('.', href))


class GetLastModifiedProperty(Property):
    """Provides {DAV:}getlastmodified.

    https://tools.ietf.org/html/rfc4918, section 15.7
    """

    name = '{DAV:}getlastmodified'
    resource_type = None
    live = True
    in_allprops = True

    async def get_value(self, href, resource, el, environ):
        # Use rfc1123 date (section 3.3.1 of RFC2616)
        el.text = resource.get_last_modified().strftime(
            '%a, %d %b %Y %H:%M:%S GMT')


def format_datetime(dt):
    s = "%04d%02d%02dT%02d%02d%02dZ" % (
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second
    )
    return s.encode('utf-8')


class CreationDateProperty(Property):
    """Provides {DAV:}creationdate.

    https://tools.ietf.org/html/rfc4918, section 23.2
    """

    name = '{DAV:}creationdate'
    resource_type = None
    live = True

    async def get_value(self, href, resource, el, environ):
        el.text = format_datetime(resource.get_creationdate())


class GetContentLanguageProperty(Property):
    """Provides {DAV:}getcontentlanguage.

    https://tools.ietf.org/html/rfc4918, section 15.3
    """

    name = '{DAV:}getcontentlanguage'
    resource_type = None

    async def get_value(self, href, resource, el, environ):
        el.text = ', '.join(resource.get_content_language())


class GetContentLengthProperty(Property):
    """Provides {DAV:}getcontentlength.

    https://tools.ietf.org/html/rfc4918, section 15.4
    """

    name = '{DAV:}getcontentlength'
    resource_type = None

    async def get_value(self, href, resource, el, environ):
        el.text = str(await resource.get_content_length())


class GetContentTypeProperty(Property):
    """Provides {DAV:}getcontenttype.

    https://tools.ietf.org/html/rfc4918, section 13.5
    """

    name = '{DAV:}getcontenttype'
    resource_type = None

    async def get_value(self, href, resource, el, environ):
        el.text = resource.get_content_type()


class CurrentUserPrincipalProperty(Property):
    """Provides {DAV:}current-user-principal.

    See https://tools.ietf.org/html/rfc5397
    """

    name = '{DAV:}current-user-principal'
    resource_type = None
    in_allprops = False
    live = True

    def __init__(self, get_current_user_principal):
        super(CurrentUserPrincipalProperty, self).__init__()
        self.get_current_user_principal = get_current_user_principal

    async def get_value(self, href, resource, el, environ):
        """Get property with specified name.

        :param name: A property name.
        """
        current_user_principal = self.get_current_user_principal(environ)
        if current_user_principal is None:
            ET.SubElement(el, '{DAV:}unauthenticated')
        else:
            current_user_principal = ensure_trailing_slash(
                current_user_principal.lstrip('/'))
            el.append(create_href(
                current_user_principal, environ['SCRIPT_NAME']))


class PrincipalURLProperty(Property):

    name = '{DAV:}principal-URL'
    resource_type = '{DAV:}principal'
    in_allprops = True
    live = True

    async def get_value(self, href, resource, el, environ):
        """Get property with specified name.

        :param name: A property name.
        """
        el.append(create_href(
            ensure_trailing_slash(resource.get_principal_url()), href))


class SupportedReportSetProperty(Property):

    name = '{DAV:}supported-report-set'
    resource_type = '{DAV:}collection'
    in_allprops = False
    live = True

    def __init__(self, reporters):
        self._reporters = reporters

    async def get_value(self, href, resource, el, environ):
        for name, reporter in self._reporters.items():
            if reporter.supported_on(resource):
                bel = ET.SubElement(el, '{DAV:}supported-report')
                ET.SubElement(bel, name)


class GetCTagProperty(Property):
    """getctag property

    """

    name: str
    resource_type = COLLECTION_RESOURCE_TYPE
    in_allprops = False
    live = True

    async def get_value(self, href, resource, el, environ):
        el.text = resource.get_ctag()


class DAVGetCTagProperty(GetCTagProperty):
    """getctag property

    """

    name = '{DAV:}getctag'


class AppleGetCTagProperty(GetCTagProperty):
    """getctag property

    """

    name = '{http://calendarserver.org/ns/}getctag'


class RefreshRateProperty(Property):
    """refreshrate property.

    (no public documentation, but contains an ical-style frequency indicator)
    """

    name = '{http://calendarserver.org/ns/}refreshrate'
    resource_type = COLLECTION_RESOURCE_TYPE
    in_allprops = False

    async def get_value(self, href, resource, el, environ):
        el.text = resource.get_refreshrate()

    def set_value(self, href, resource, el):
        resource.set_refreshrate(el.text)


LOCK_SCOPE_EXCLUSIVE = '{DAV:}exclusive'
LOCK_SCOPE_SHARED = '{DAV:}shared'
LOCK_TYPE_WRITE = '{DAV:}write'


ActiveLock = collections.namedtuple(
    'ActiveLock',
    ['lockscope', 'locktype', 'depth', 'owner', 'timeout', 'locktoken',
        'lockroot'])


class Collection(Resource):
    """Resource for a WebDAV Collection."""

    resource_types = Resource.resource_types + [COLLECTION_RESOURCE_TYPE]

    def members(self):
        """List all members.

        :return: List of (name, Resource) tuples
        """
        raise NotImplementedError(self.members)

    def get_member(self, name):
        """Retrieve a member by name.

        :param name: Name of member to retrieve
        :return: A Resource
        """
        raise NotImplementedError(self.get_member)

    def delete_member(self, name, etag=None):
        """Delete a member with a specific name.

        :param name: Member name
        :param etag: Optional required etag
        :raise KeyError: when the item doesn't exist
        """
        raise NotImplementedError(self.delete_member)

    def create_member(self, name, contents, content_type):
        """Create a new member with specified name and contents.

        :param name: Member name (can be None)
        :param contents: Chunked contents
        :param etag: Optional required etag
        :return: (name, etag) for the new member
        """
        raise NotImplementedError(self.create_member)

    def get_sync_token(self):
        """Get sync-token for the current state of this collection.
        """
        raise NotImplementedError(self.get_sync_token)

    def iter_differences_since(self, old_token, new_token):
        """Iterate over differences in this collection.

        Should return an iterator over (name, old resource, new resource)
        tuples. If one of the two didn't exist previously or now, they should
        be None.

        If old_token is None, this should return full contents of the
        collection.

        May raise NotImplementedError if iterating differences is not
        supported.
        """
        raise NotImplementedError(self.iter_differences_since)

    def get_ctag(self):
        raise NotImplementedError(self.getctag)

    def get_headervalue(self):
        raise NotImplementedError(self.get_headervalue)

    def destroy(self):
        """Destroy this collection itself.
        """
        raise NotImplementedError(self.destroy)

    def set_refreshrate(self, value):
        """Set the recommended refresh rate for this collection.

        :param value: Refresh rate (None to remove)
        """
        raise NotImplementedError(self.set_refreshrate)

    def get_refreshrate(self):
        """Get the recommended refresh rate.

        :return: Recommended refresh rate
        :raise KeyError: if there is no refresh rate set
        """
        raise NotImplementedError(self.get_refreshrate)


class Principal(Resource):
    """Resource for a DAV Principal."""

    resource_Types = Resource.resource_types + [PRINCIPAL_RESOURCE_TYPE]

    def get_principal_url(self):
        """Return the principal URL for this principal.

        :return: A URL identifying this principal.
        """
        raise NotImplementedError(self.get_principal_url)

    def get_infit_settings(self):
        """Return inf-it settings string.
        """
        raise NotImplementedError(self.get_infit_settings)

    def set_infit_settings(self, settings):
        """Set inf-it settings string."""
        raise NotImplementedError(self.get_infit_settings)

    def get_group_membership(self):
        """Get group membership URLs."""
        raise NotImplementedError(self.get_group_membership)

    def get_calendar_proxy_read_for(self):
        """List principals for which this one is a read proxy.

        :return: List of principal hrefs
        """
        raise NotImplementedError(self.get_calendar_proxy_read_for)

    def get_calendar_proxy_write_for(self):
        """List principals for which this one is a write proxy.

        :return: List of principal hrefs
        """
        raise NotImplementedError(self.get_calendar_proxy_write_for)

    def get_schedule_inbox_url(self):
        raise NotImplementedError(self.get_schedule_inbox_url)

    def get_schedule_outbox_url(self):
        raise NotImplementedError(self.get_schedule_outbox_url)


async def get_property_from_name(
        href: str, resource: Resource,
        properties, name: str, environ):
    """Get a single property on a resource.

    :param href: Resource href
    :param resource: Resource object
    :param properties: Dictionary of properties
    :param environ: WSGI environ dict
    :param name: name of property to resolve
    :return: PropStatus items
    """
    return await get_property_from_element(
        href, resource, properties, environ, ET.Element(name))


async def get_property_from_element(
        href: str, resource: Resource,
        properties: Dict[str, Property],
        environ, requested: ET.Element) -> PropStatus:
    """Get a single property on a resource.

    :param href: Resource href
    :param resource: Resource object
    :param properties: Dictionary of properties
    :param environ: WSGI environ dict
    :param requested: Requested element
    :return: PropStatus items
    """
    responsedescription = None
    ret = ET.Element(requested.tag)
    try:
        prop = properties[requested.tag]
    except KeyError:
        statuscode = '404 Not Found'
        logging.warning(
            'Client requested unknown property %s on %s (%r)',
            requested.tag, href, resource.resource_types)
    else:
        try:
            if not prop.supported_on(resource):
                raise KeyError
            try:
                get_value_ext = prop.get_value_ext  # type: ignore
            except AttributeError:
                await prop.get_value(href, resource, ret, environ)
            else:
                await get_value_ext(href, resource, ret, environ, requested)
        except KeyError:
            statuscode = '404 Not Found'
        except NotImplementedError:
            logging.exception(
                'Not implemented while getting %s for %r',
                requested.tag, resource)
            statuscode = '501 Not Implemented'
        else:
            statuscode = '200 OK'
    return PropStatus(statuscode, responsedescription, ret)


async def get_properties(
        href: str, resource: Resource,
        properties: Dict[str, Property], environ,
        requested: ET.Element) -> AsyncIterable[PropStatus]:
    """Get a set of properties.

    :param href: Resource Href
    :param resource: Resource object
    :param properties: Dictionary of properties
    :param requested: XML {DAV:}prop element with properties to look up
    :param environ: WSGI environ dict
    :return: Iterator over PropStatus items
    """
    for propreq in list(requested):
        yield await get_property_from_element(
            href, resource, properties, environ, propreq)


async def get_property_names(
        href: str, resource: Resource,
        properties: Dict[str, Property], environ,
        requested: ET.Element) -> AsyncIterable[PropStatus]:
    """Get a set of property names.

    :param href: Resource Href
    :param resource: Resource object
    :param properties: Dictionary of properties
    :param environ: WSGI environ dict
    :param requested: XML {DAV:}prop element with properties to look up
    :return: Iterator over PropStatus items
    """
    for name, prop in properties.items():
        if await prop.is_set(href, resource, environ):
            yield PropStatus('200 OK', None, ET.Element(name))


async def get_all_properties(
        href: str, resource: Resource,
        properties: Dict[str, Property], environ) -> AsyncIterable[PropStatus]:
    """Get all properties.

    :param href: Resource Href
    :param resource: Resource object
    :param properties: Dictionary of properties
    :param requested: XML {DAV:}prop element with properties to look up
    :param environ: WSGI environ dict
    :return: Iterator over PropStatus items
    """
    for name in properties:
        ps = await get_property_from_name(
            href, resource, properties, name, environ)
        if ps.statuscode == '200 OK':
            yield ps


def ensure_trailing_slash(href: str) -> str:
    """Ensure that a href has a trailing slash.

    Useful for collection hrefs, e.g. when used with urljoin.

    :param href: href to possibly add slash to
    :return: href with trailing slash
    """
    if href.endswith('/'):
        return href
    return href + '/'


async def traverse_resource(
        base_resource: Resource, base_href: str, depth: str,
        members: Optional[
            Callable[[Collection], Iterable[Tuple[str, Resource]]]] = None
        ) -> AsyncIterable[Tuple[str, Resource]]:
    """Traverse a resource.

    :param base_resource: Resource to traverse from
    :param base_href: href for base resource
    :param depth: Depth ("0", "1", "infinity")
    :param members: Function to use to get members of each
        collection.
    :return: Iterator over (URL, Resource) tuples
    """
    if members is None:
        def members_fn(c):
            return c.members()
    else:
        members_fn = members
    todo = collections.deque([(base_href, base_resource, depth)])
    while todo:
        (href, resource, depth) = todo.popleft()
        if COLLECTION_RESOURCE_TYPE in resource.resource_types:
            # caldavzap/carddavmate require this
            # https://tools.ietf.org/html/rfc4918#section-5.2
            # mentions that a trailing slash *SHOULD* be added for
            # collections.
            href = ensure_trailing_slash(href)
        yield (href, resource)
        if depth == "0":
            continue
        elif depth == "1":
            nextdepth = "0"
        elif depth == "infinity":
            nextdepth = "infinity"
        else:
            raise AssertionError("invalid depth %r" % depth)
        if COLLECTION_RESOURCE_TYPE in resource.resource_types:
            for (child_name, child_resource) in members_fn(resource):
                child_href = urllib.parse.urljoin(href, child_name)
                todo.append((child_href, child_resource, nextdepth))


class Reporter(object):
    """Implementation for DAV REPORT requests."""

    name: str

    resource_type: Optional[Union[str, Tuple]] = None

    def supported_on(self, resource: Resource) -> bool:
        """Check if this reporter is available for the specified resource.

        :param resource: Resource to check for
        :return: boolean indicating whether this reporter is available
        """
        if self.resource_type is None:
            return True
        if isinstance(self.resource_type, tuple):
            return any(rs in resource.resource_types
                       for rs in self.resource_type)
        return self.resource_type in resource.resource_types

    async def report(
            self, environ: Dict[str, str],
            request_body: ET.Element,
            resources_by_hrefs: Callable[
                [Iterable[str]], Iterable[Tuple[str, Resource]]],
            properties: Dict[str, Property],
            href: str,
            resource: Resource,
            depth: str) -> Status:
        """Send a report.

        :param environ: wsgi environ
        :param request_body: XML Element for request body
        :param resources_by_hrefs: Function for retrieving resource by HREF
        :param properties: Dictionary mapping names to DAVProperty instances
        :param href: Base resource href
        :param resource: Resource to start from
        :param depth: Depth ("0", "1", ...)
        :return: a response
        """
        raise NotImplementedError(self.report)


def create_href(href: str, base_href: Optional[str] = None) -> ET.Element:
    parsed_url = urllib.parse.urlparse(href)
    if '//' in parsed_url.path:
        logging.warning('invalidly formatted href: %s', href)
    et = ET.Element('{DAV:}href')
    if base_href is not None:
        href = urllib.parse.urljoin(ensure_trailing_slash(base_href), href)
    et.text = urllib.parse.quote(href)
    return et


def read_href_element(et: ET.Element) -> Optional[str]:
    if et.text is None:
        return None
    el = urllib.parse.unquote(et.text)
    parsed_url = urllib.parse.urlsplit(el)
    # TODO(jelmer): Check that the hostname matches the local hostname?
    return parsed_url.path


class ExpandPropertyReporter(Reporter):
    """A expand-property reporter.

    See https://tools.ietf.org/html/rfc3253, section 3.8
    """

    name = '{DAV:}expand-property'

    async def _populate(
            self, prop_list: ET.Element,
            resources_by_hrefs: Callable[
                [Iterable[str]], List[Tuple[str, Resource]]],
            properties: Dict[str, Property], href: str,
            resource: Resource, environ) -> AsyncIterable[Status]:
        """Expand properties for a resource.

        :param prop_list: DAV:property elements to retrieve and expand
        :param resources_by_hrefs: Resolve resource by HREF
        :param properties: Available properties
        :param href: href for current resource
        :param resource: current resource
        :param environ: WSGI environ dict
        :return: Status object
        """
        ret = []
        for prop in prop_list:
            prop_name = prop.get('name')
            if prop_name is None:
                logging.warning('Tag %s without name attribute', prop.tag)
                continue
            # FIXME: Resolve prop_name on resource
            propstat = await get_property_from_name(
                href, resource, properties, prop_name, environ)
            new_prop = ET.Element(propstat.prop.tag)
            child_hrefs = filter(None, [
                read_href_element(prop_child)
                for prop_child in propstat.prop
                if prop_child.tag == '{DAV:}href'])
            child_resources = resources_by_hrefs(child_hrefs)
            for prop_child in propstat.prop:
                if prop_child.tag != '{DAV:}href':
                    new_prop.append(prop_child)
                else:
                    child_href = read_href_element(prop_child)
                    if child_href is None:
                        logging.warning(
                            'Tag %s without valid href', prop_child.tag)
                        continue
                    child_resource = dict(child_resources).get(child_href)
                    if child_resource is None:
                        # FIXME: What to do if the referenced href is invalid?
                        # For now, let's just keep the unresolved href around
                        new_prop.append(prop_child)
                    else:
                        async for response in self._populate(
                                prop, resources_by_hrefs, properties,
                                child_href, child_resource, environ):
                            new_prop.append(response.aselement())
            propstat = PropStatus(propstat.statuscode,
                                  propstat.responsedescription, prop=new_prop)
            ret.append(propstat)
        yield Status(href, '200 OK', propstat=ret)

    @multistatus
    async def report(self, environ, request_body, resources_by_hrefs,
                     properties, href, resource, depth):
        async for resp in self._populate(
                request_body, resources_by_hrefs, properties, href, resource,
                environ):
            yield resp


class SupportedLockProperty(Property):
    """supportedlock property.

    See rfc4918, section 15.10.
    """

    name = '{DAV:}supportedlock'
    resource_type = None
    live = True

    async def get_value(self, href, resource, el, environ):
        for (lockscope, locktype) in resource.get_supported_locks():
            entry = ET.SubElement(el, '{DAV:}lockentry')
            scope_el = ET.SubElement(entry, '{DAV:}lockscope')
            ET.SubElement(scope_el, lockscope)
            type_el = ET.SubElement(entry, '{DAV:}locktype')
            ET.SubElement(type_el, locktype)


class LockDiscoveryProperty(Property):
    """lockdiscovery property.

    See rfc4918, section 15.8
    """

    name = '{DAV:}lockdiscovery'
    resource_type = None
    live = True

    async def get_value(self, href, resource, el, environ):
        for activelock in resource.get_active_locks():
            entry = ET.SubElement(el, '{DAV:}activelock')
            type_el = ET.SubElement(entry, '{DAV:}locktype')
            ET.SubElement(type_el, activelock.locktype)
            scope_el = ET.SubElement(entry, '{DAV:}lockscope')
            ET.SubElement(scope_el, activelock.lockscope)
            ET.SubElement(entry, '{DAV:}depth').text = str(activelock.depth)
            if activelock.owner:
                ET.SubElement(entry, '{DAV:}owner').text = activelock.owner
            if activelock.timeout:
                ET.SubElement(entry, '{DAV:}timeout').text = activelock.timeout
            if activelock.locktoken:
                locktoken_el = ET.SubElement(entry, '{DAV:}locktoken')
                locktoken_el.append(create_href(activelock.locktoken))
            if activelock.lockroot:
                lockroot_el = ET.SubElement(entry, '{DAV:}lockroot')
                lockroot_el.append(create_href(activelock.lockroot))


class CommentProperty(Property):
    """comment property.

    See RFC3253, section 3.1.1
    """
    name = '{DAV:}comment'
    live = False
    in_allprops = False

    async def get_value(self, href, resource, el, environ):
        el.text = resource.get_comment()

    def set_value(self, href, resource, el):
        resource.set_comment(el.text)


class Backend(object):
    """WebDAV backend."""

    def create_collection(self, relpath):
        """Create a collection with the specified relpath.

        :param relpath: Collection path
        """
        raise NotImplementedError(self.create_collection)

    def get_resource(self, relpath):
        raise NotImplementedError(self.get_resource)


def _get_resources_by_hrefs(backend, environ, hrefs):
    """Retrieve multiple resources by href.

    :param backend: backend from which to retrieve resources
    :param environ: Environment dictionary
    :param hrefs: List of hrefs to resolve
    :return: iterator over (href, resource) tuples
    """
    script_name = environ['SCRIPT_NAME']
    # TODO(jelmer): Bulk query hrefs in a more efficient manner
    for href in hrefs:
        if not href.startswith(script_name):
            resource = None
        else:
            path = href[len(script_name):]
            if not path.startswith('/'):
                path = '/' + path
            resource = backend.get_resource(path)
        yield (href, resource)


def _send_xml_response(status, et, out_encoding):
    body_type = 'text/xml; charset="%s"' % out_encoding
    if os.environ.get('XANDIKOS_DUMP_DAV_XML'):
        print("OUT: " + ET.tostring(et).decode('utf-8'))
    body = ET.tostringlist(et, encoding=out_encoding)
    return Response(
        status=status,
        body=body,
        headers={
            'Content-Type': body_type,
            'Content-Length': str(sum(map(len, body)))})


def _send_dav_responses(responses, out_encoding):
    if isinstance(responses, Status):
        try:
            (body, body_type) = responses.get_single_body(
                out_encoding)
        except NeedsMultiStatus:
            responses = [responses]
        else:
            return Response(status=responses.status, headers={
                'Content-Type': body_type,
                'Content-Length': str(sum(map(len, body)))},
                body=body)
    ret = ET.Element('{DAV:}multistatus')
    for response in responses:
        ret.append(response.aselement())
    return _send_xml_response('207 Multi-Status', ret, out_encoding)


def _send_simple_dav_error(request, statuscode, error,
                           description):
    status = Status(request.url, statuscode, error=error,
                    responsedescription=description)
    return _send_dav_responses(status, DEFAULT_ENCODING)


def _send_not_found(request):
    body = [b'Path ' + request.path.encode(DEFAULT_ENCODING) + b' not found.']
    return Response(body=body, status=404, reason='Not Found')


def _send_method_not_allowed(allowed_methods):
    return Response(
        status=405, reason='Method Not Allowed',
        headers={'Allow': ', '.join(allowed_methods)})


def apply_modify_prop(el, href, resource, properties):
    """Apply property set/remove operations.

    :param el: set element to apply.
    :param href: Resource href
    :param resource: Resource to apply property modifications on
    :param properties: Known properties
    :yield: PropStatus objects
    """
    if el.tag not in ('{DAV:}set', '{DAV:}remove'):
        # callers should check tag
        raise AssertionError
    try:
        [requested] = el
    except IndexError:
        raise BadRequestError(
            'Received more than one element in {DAV:}set element.')
    if requested.tag != '{DAV:}prop':
        raise BadRequestError('Expected prop tag, got ' + requested.tag)
    for propel in requested:
        try:
            handler = properties[propel.tag]
        except KeyError:
            logging.warning(
                'client attempted to modify unknown property %r on %r',
                propel.tag, href)
            yield PropStatus('404 Not Found', None, ET.Element(propel.tag))
        else:
            if el.tag == '{DAV:}remove':
                newval = None
            elif el.tag == '{DAV:}set':
                newval = propel
            else:
                raise AssertionError
            if not handler.supported_on(resource):
                statuscode = '404 Not Found'
            else:
                try:
                    handler.set_value(href, resource, newval)
                except NotImplementedError:
                    # TODO(jelmer): Signal
                    # {DAV:}cannot-modify-protected-property error
                    statuscode = '409 Conflict'
                else:
                    statuscode = '200 OK'
            yield PropStatus(statuscode, None, ET.Element(propel.tag))


async def _readBody(request):
    request_body_size = request.content_length
    if request_body_size is None:
        return [await request.content.read()]
    else:
        return [await request.content.read(request_body_size)]


async def _readXmlBody(
        request, expected_tag: Optional[str] = None, strict: bool = True):
    content_type = request.content_type
    base_content_type, params = parse_type(content_type)
    if strict and base_content_type not in ('text/xml', 'application/xml'):
        raise UnsupportedMediaType(content_type)
    body = b''.join(await _readBody(request))
    if os.environ.get('XANDIKOS_DUMP_DAV_XML'):
        print("IN: " + body.decode('utf-8'))
    try:
        et = xmlparse(body)
    except ET.ParseError:
        raise BadRequestError('Unable to parse body.')
    if expected_tag is not None and et.tag != expected_tag:
        raise BadRequestError('Expected %s tag, got %s' %
                              (expected_tag, et.tag))
    return et


class Method(object):

    @property
    def name(self):
        return type(self).__name__.upper()[:-6]

    async def handle(self, request, environ, app):
        raise NotImplementedError(self.handle)

    def allow(self, request):
        """Is this method allowed considering the specified request?"""
        return True


class DeleteMethod(Method):

    async def handle(self, request, environ, app):
        unused_href, path, r = app._get_resource_from_environ(request, environ)
        if r is None:
            return _send_not_found(request)
        container_path, item_name = posixpath.split(path.rstrip('/'))
        pr = app.backend.get_resource(container_path)
        if pr is None:
            return _send_not_found(request)
        current_etag = await r.get_etag()
        if_match = request.headers.get('If-Match', None)
        if if_match is not None and not etag_matches(if_match, current_etag):
            return Response(status=412, reason='Precondition Failed')
        pr.delete_member(item_name, current_etag)
        return Response(status=204, reason='No Content')


class PostMethod(Method):

    async def handle(self, request, environ, app):
        # see RFC5995
        new_contents = await _readBody(request)
        unused_href, path, r = app._get_resource_from_environ(request, environ)
        if r is None:
            return _send_not_found(request)
        if COLLECTION_RESOURCE_TYPE not in r.resource_types:
            return _send_method_not_allowed(
                app._get_allowed_methods(request))
        content_type, params = parse_type(request.content_type)
        try:
            (name, etag) = r.create_member(None, new_contents, content_type)
        except PreconditionFailure as e:
            return _send_simple_dav_error(
                request, '412 Precondition Failed',
                error=ET.Element(e.precondition),
                description=e.description)
        except InsufficientStorage:
            return Response(status=507, reason='Insufficient Storage')
        except ResourceLocked:
            return Response(status=423, reason='Resource Locked')
        href = (
            environ['SCRIPT_NAME'] +
            urllib.parse.urljoin(ensure_trailing_slash(path), name)
        )
        return Response(headers={'Location': href})


class PutMethod(Method):

    async def handle(self, request, environ, app):
        new_contents = await _readBody(request)
        unused_href, path, r = app._get_resource_from_environ(request, environ)
        if r is not None:
            current_etag = await r.get_etag()
        else:
            current_etag = None
        if_match = request.headers.get('If-Match', None)
        if if_match is not None and not etag_matches(if_match, current_etag):
            return Response(status='412 Precondition Failed')
        if_none_match = request.headers.get('If-None-Match', None)
        if if_none_match and etag_matches(if_none_match, current_etag):
            return Response(status='412 Precondition Failed')
        if r is not None:
            # Item already exists; update it
            try:
                new_etag = r.set_body(new_contents, current_etag)
            except PreconditionFailure as e:
                return _send_simple_dav_error(
                    request, '412 Precondition Failed',
                    error=ET.Element(e.precondition),
                    description=e.description)
            except NotImplementedError:
                return _send_method_not_allowed(
                    app._get_allowed_methods(request))
            else:
                return Response(status='204 No Content', headers=[
                    ('ETag', new_etag)])
        content_type = request.content_type
        container_path, name = posixpath.split(path)
        r = app.backend.get_resource(container_path)
        if r is None:
            return _send_not_found(request)
        if COLLECTION_RESOURCE_TYPE not in r.resource_types:
            return _send_method_not_allowed(
                app._get_allowed_methods(request))
        try:
            (new_name, new_etag) = r.create_member(
                name, new_contents, content_type)
        except PreconditionFailure as e:
            return _send_simple_dav_error(
                request, '412 Precondition Failed',
                error=ET.Element(e.precondition),
                description=e.description)
        except InsufficientStorage:
            return Response(status=507, reason='Insufficient Storage')
        except ResourceLocked:
            return Response(status=423, reason='Resource Locked')
        return Response(
            status=201, reason='Created', headers=[
                ('ETag', new_etag)])


class ReportMethod(Method):

    async def handle(self, request, environ, app):
        # See https://tools.ietf.org/html/rfc3253, section 3.6
        base_href, unused_path, r = app._get_resource_from_environ(
            request, environ)
        if r is None:
            return _send_not_found(request)
        depth = request.headers.get("Depth", "0")
        et = await _readXmlBody(request, None, strict=app.strict)
        try:
            reporter = app.reporters[et.tag]
        except KeyError:
            logging.warning('Client requested unknown REPORT %s', et.tag)
            return _send_simple_dav_error(
                request,
                '403 Forbidden', error=ET.Element('{DAV:}supported-report'),
                description=('Unknown report %s.' % et.tag)
            )
        if not reporter.supported_on(r):
            return _send_simple_dav_error(
                request,
                '403 Forbidden', error=ET.Element('{DAV:}supported-report'),
                description=('Report %s not supported on resource.' % et.tag)
            )
        return await reporter.report(
            environ, et, functools.partial(
                _get_resources_by_hrefs, app.backend, environ),
            app.properties, base_href, r, depth)


class PropfindMethod(Method):

    @multistatus
    async def handle(self, request, environ, app):
        base_href, unused_path, base_resource = (
            app._get_resource_from_environ(request, environ))
        if base_resource is None:
            yield Status(request.url, '404 Not Found')
            return
        # Default depth is infinity, per RFC2518
        depth = request.headers.get("Depth", "infinity")
        if not request.can_read_body:
            requested = None
        else:
            et = await _readXmlBody(
                request, '{DAV:}propfind', strict=app.strict)
            try:
                [requested] = et
            except ValueError:
                raise BadRequestError(
                    'Received more than one element in propfind.')
        async for href, resource in traverse_resource(
                base_resource, base_href, depth):
            propstat = []
            if requested is None or requested.tag == '{DAV:}allprop':
                propstat = get_all_properties(
                    href, resource, app.properties, environ)
            elif requested.tag == '{DAV:}prop':
                propstat = get_properties(
                    href, resource, app.properties, environ, requested)
            elif requested.tag == '{DAV:}propname':
                propstat = get_property_names(
                    href, resource, app.properties, environ, requested)
            else:
                raise BadRequestError(
                    'Expected prop/allprop/propname tag, got ' + requested.tag)
            yield Status(href, '200 OK', propstat=[s async for s in propstat])
        # By my reading of the WebDAV RFC, it should be legal to return
        # '200 OK' here if Depth=0, but the RFC is not super clear and
        # some clients don't seem to like it and prefer a 207 instead.


class ProppatchMethod(Method):

    @multistatus
    async def handle(self, request, environ, app):
        href, unused_path, resource = app._get_resource_from_environ(
            request, environ)
        if resource is None:
            yield Status(request.url, '404 Not Found')
            return
        et = await _readXmlBody(
            request, '{DAV:}propertyupdate', strict=app.strict)
        propstat = []
        for el in et:
            if el.tag not in ('{DAV:}set', '{DAV:}remove'):
                raise BadRequestError('Unknown tag %s in propertyupdate'
                                      % el.tag)
            propstat.extend(apply_modify_prop(el, href, resource,
                                              app.properties))
        yield Status(request.url, propstat=propstat)


class MkcolMethod(Method):

    async def handle(self, request, environ, app):
        content_type = request.content_type
        base_content_type, params = parse_type(content_type)
        if base_content_type not in (
            'text/plain', 'text/xml', 'application/xml', None,
            'application/octet-stream',
        ):
            raise UnsupportedMediaType(base_content_type)
        href, path, resource = app._get_resource_from_environ(request, environ)
        if resource is not None:
            return _send_method_not_allowed(
                app._get_allowed_methods(request))
        try:
            resource = app.backend.create_collection(path)
        except FileNotFoundError:
            return Response(status=409, reason='Conflict')
        if base_content_type in ('text/xml', 'application/xml'):
            # Extended MKCOL (RFC5689)
            et = await _readXmlBody(request, '{DAV:}mkcol', strict=app.strict)
            propstat = []
            for el in et:
                if el.tag != '{DAV:}set':
                    raise BadRequestError('Unknown tag %s in mkcol' % el.tag)
                propstat.extend(apply_modify_prop(el, href, resource,
                                                  app.properties))
            ret = ET.Element('{DAV:}mkcol-response')
            for propstat_el in propstat_as_xml(propstat):
                ret.append(propstat_el)
            return _send_xml_response(
                '201 Created', ret, DEFAULT_ENCODING)
        else:
            return Response(status=201, reason='Created')


class OptionsMethod(Method):

    async def handle(self, request, environ, app):
        headers = []
        if request.raw_path != '*':
            unused_href, unused_path, r = (
                app._get_resource_from_environ(request, environ))
            if r is None:
                return _send_not_found(request)
            dav_features = app._get_dav_features(r)
            headers.append(('DAV', ', '.join(dav_features)))
            allowed_methods = app._get_allowed_methods(request)
            headers.append(('Allow', ', '.join(allowed_methods)))

        # RFC7231 requires that if there is no response body,
        # Content-Length: 0 must be sent. This implies that there is
        # content (albeit empty), and thus a 204 is not a valid reply.
        # Thunderbird also fails if a 204 is sent rather than a 200.
        return Response(status=200, reason='OK', headers=headers + [
            ('Content-Length', '0')])


class HeadMethod(Method):

    async def handle(self, request, environ, app):
        return await _do_get(request, environ, app, send_body=False)


class GetMethod(Method):

    async def handle(self, request, environ, app):
        return await _do_get(request, environ, app, send_body=True)


async def _do_get(request, environ, app, send_body):
    unused_href, unused_path, r = app._get_resource_from_environ(
        request, environ)
    if r is None:
        return _send_not_found(request)
    accept_content_types = parse_accept_header(
        request.headers.get('Accept', '*/*'))
    accept_content_languages = parse_accept_header(
        request.headers.get('Accept-Languages', '*'))

    (
        body,
        content_length,
        current_etag,
        content_type,
        content_languages
    ) = await r.render(
        request.path, accept_content_types, accept_content_languages)

    if_none_match = request.headers.get('If-None-Match', None)
    if (
        if_none_match and current_etag is not None and
        etag_matches(if_none_match, current_etag)
    ):
        return Response(status='304 Not Modified')
    headers = [
        ('Content-Length', str(content_length)),
    ]
    if current_etag is not None:
        headers.append(('ETag', current_etag))
    if content_type is not None:
        headers.append(('Content-Type', content_type))
    try:
        last_modified = r.get_last_modified()
    except KeyError:
        pass
    else:
        headers.append(('Last-Modified', last_modified))
    if content_languages is not None:
        headers.append(('Content-Language', ', '.join(content_languages)))
    if send_body:
        return Response(body=body, status=200, reason='OK', headers=headers)
    else:
        return Response(status=200, reason='OK', headers=headers)


class WSGIRequest(object):
    """Request object for wsgi requests (with environ)."""

    def __init__(self, environ):
        self._environ = environ
        self.method = environ['REQUEST_METHOD']
        self.raw_path = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        self.path = environ['SCRIPT_NAME'] + path_from_environ(
            environ, 'PATH_INFO')
        self.content_type = environ.get(
            'CONTENT_TYPE', 'application/octet-stream')
        try:
            self.content_length = int(environ['CONTENT_LENGTH'])
        except (KeyError, ValueError):
            self.content_length = None
        from multidict import CIMultiDict
        self.headers = CIMultiDict([
            (k[5:], v) for k, v in environ.items()
            if k.startswith('HTTP_')])
        self.url = request_uri(environ)

        class StreamWrapper(object):

            def __init__(self, stream):
                self._stream = stream

            async def read(self, size=None):
                return self._stream.read(size)

        self.content = StreamWrapper(self._environ['wsgi.input'])
        self.match_info = {'path_info': environ['PATH_INFO']}

    @property
    def can_read_body(self):
        return ('CONTENT_TYPE' in self._environ or
                self._environ.get('CONTENT_LENGTH') != '0')

    async def read(self):
        return self._environ['wsgi.input'].read()


class WebDAVApp(object):
    """A wsgi App that provides a WebDAV server.

    A concrete implementation should provide an implementation of the
    lookup_resource function that can map a path to a Resource object
    (returning None for nonexistant objects).
    """

    def __init__(self, backend, strict=True):
        self.backend = backend
        self.properties = {}
        self.reporters = {}
        self.methods = {}
        self.strict = strict
        self.register_methods([
            DeleteMethod(),
            PostMethod(),
            PutMethod(),
            ReportMethod(),
            PropfindMethod(),
            ProppatchMethod(),
            MkcolMethod(),
            OptionsMethod(),
            GetMethod(),
            HeadMethod(),
        ])

    def _get_resource_from_environ(self, request, environ):
        path_info = request.match_info['path_info']
        if not path_info.startswith('/'):
            path_info = '/' + path_info
        r = self.backend.get_resource(path_info)
        return (request.path, path_info, r)

    def register_properties(self, properties):
        for p in properties:
            self.properties[p.name] = p

    def register_reporters(self, reporters):
        for r in reporters:
            self.reporters[r.name] = r

    def register_methods(self, methods):
        for m in methods:
            self.methods[m.name] = m

    def _get_dav_features(self, resource):
        # TODO(jelmer): Support access-control
        return ['1', '2', '3', 'calendar-access', 'calendar-auto-scheduling',
                'addressbook', 'extended-mkcol', 'add-member',
                'sync-collection', 'quota']

    def _get_allowed_methods(self, request):
        """List of supported methods on this endpoint."""
        ret = []
        for name in sorted(self.methods.keys()):
            if self.methods[name].allow(request):
                ret.append(name)
        return ret

    async def _handle_request(self, request, environ):
        if request.headers.get('Expect', '') != '':
            return Response(status='417 Expectation Failed')
        try:
            do = self.methods[request.method]
        except KeyError:
            return _send_method_not_allowed(self._get_allowed_methods(request))
        try:
            return await do.handle(request, environ, self)
        except BadRequestError as e:
            return Response(
                status='400 Bad Request',
                body=[e.message.encode(DEFAULT_ENCODING)])
        except NotAcceptableError as e:
            return Response(
                status='406 Not Acceptable',
                body=[str(e).encode(DEFAULT_ENCODING)])
        except UnsupportedMediaType as e:
            return Response(
                status='415 Unsupported Media Type',
                body=[('Unsupported media type %r' % e.content_type)
                      .encode(DEFAULT_ENCODING)])
        except UnauthorizedError:
            return Response(
                status='401 Unauthorized',
                body=[('Please login.'.encode(DEFAULT_ENCODING))])

    def handle_wsgi_request(self, environ, start_response):
        if 'SCRIPT_NAME' not in environ:
            logging.debug('SCRIPT_NAME not set; assuming "".')
            environ['SCRIPT_NAME'] = ''
        request = WSGIRequest(environ)
        environ = {'SCRIPT_NAME': environ['SCRIPT_NAME']}
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self._handle_request(
            request, environ))
        return response.for_wsgi(start_response)

    async def aiohttp_handler(self, request, route_prefix='/'):
        environ = {'SCRIPT_NAME': route_prefix}
        response = await self._handle_request(request, environ)
        return response.for_aiohttp()

    # Backwards compatibility
    __call__ = handle_wsgi_request
