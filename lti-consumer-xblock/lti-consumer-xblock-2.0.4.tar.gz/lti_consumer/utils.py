# -*- coding: utf-8 -*-
"""
Utility functions for LTI Consumer block
"""
from django.conf import settings


def _(text):
    """
    Make '_' a no-op so we can scrape strings
    """
    return text


def lti_1p3_enabled():
    """
    Returns `true` if LTI 1.3 integration is enabled for instance.
    """
    return settings.FEATURES.get('LTI_1P3_ENABLED', False) is True


def get_lms_base():
    """
    Returns LMS base url to be used as issuer on OAuth2 flows

    TODO: This needs to be improved and account for Open edX sites and
    organizations.
    One possible improvement is to use `contentstore.get_lms_link_for_item`
    and strip the base domain name.
    """
    return settings.LMS_ROOT_URL


def get_lms_lti_keyset_link(location):
    """
    Returns an LMS link to LTI public keyset endpoint

    :param location: the location of the block
    """
    return u"{lms_base}/api/lti_consumer/v1/public_keysets/{location}".format(
        lms_base=get_lms_base(),
        location=str(location),
    )


def get_lms_lti_launch_link():
    """
    Returns an LMS link to LTI Launch endpoint

    :param location: the location of the block
    """
    return u"{lms_base}/api/lti_consumer/v1/launch/".format(
        lms_base=get_lms_base(),
    )


def get_lms_lti_access_token_link(location):
    """
    Returns an LMS link to LTI Launch endpoint

    :param location: the location of the block
    """
    return u"{lms_base}/api/lti_consumer/v1/token/{location}".format(
        lms_base=get_lms_base(),
        location=str(location),
    )
