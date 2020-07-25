from __future__ import absolute_import, print_function, unicode_literals
from future import standard_library
standard_library.install_aliases
from typing import Dict, Optional
import urllib.parse
from retry import retry
import requests
import yaml
from collections import OrderedDict
from functools import lru_cache

from .pushd import Dir
from .distgit import ImageDistGitRepo, RPMDistGitRepo
from . import exectools
from . import logutil

from .model import Model, Missing

#
# These are used as labels to index selection of a subclass.
#
DISTGIT_TYPES = {
    'image': ImageDistGitRepo,
    'rpm': RPMDistGitRepo
}

CONFIG_MODES = [
    'enabled',  # business as usual
    'disabled',  # manually disabled from automatically building
    'wip',  # Work in Progress, do not build
]

CONFIG_MODE_DEFAULT = CONFIG_MODES[0]


class Metadata(object):

    def __init__(self, meta_type, runtime, data_obj: Dict, commitish: Optional[str] = None):
        """
        :param: meta_type - a string. Index to the sub-class <'rpm'|'image'>.
        :param: runtime - a Runtime object.
        :param: name - a filename to load as metadata
        :param: commitish: If not None, build from the specified upstream commit-ish instead of the branch tip.
        """
        self.meta_type = meta_type
        self.runtime = runtime
        self.data_obj = data_obj
        self.config_filename = data_obj.filename
        self.full_config_path = data_obj.path
        self.commitish = commitish

        # URL and branch of public upstream source are set later by Runtime.resolve_source()
        self.public_upstream_url = None
        self.public_upstream_branch = None

        # Some config filenames have suffixes to avoid name collisions; strip off the suffix to find the real
        # distgit repo name (which must be combined with the distgit namespace).
        # e.g. openshift-enterprise-mediawiki.apb.yml
        #      distgit_key=openshift-enterprise-mediawiki.apb
        #      name (repo name)=openshift-enterprise-mediawiki

        self.distgit_key = data_obj.key
        self.name = self.distgit_key.split('.')[0]   # Split off any '.apb' style differentiator (if present)

        self.runtime.logger.debug("Loading metadata from {}".format(self.full_config_path))

        self.config = Model(data_obj.data)

        self.mode = self.config.get('mode', CONFIG_MODE_DEFAULT).lower()
        if self.mode not in CONFIG_MODES:
            raise ValueError('Invalid mode for {}'.format(self.config_filename))

        self.enabled = (self.mode == CONFIG_MODE_DEFAULT)

        # Basic config validation. All images currently required to have a name in the metadata.
        # This is required because from.member uses these data to populate FROM in images.
        # It would be possible to query this data from the distgit Dockerflie label, but
        # not implementing this until we actually need it.
        assert (self.config.name is not Missing)

        # Choose default namespace for config data
        if meta_type == "image":
            self.namespace = "containers"
        else:
            self.namespace = "rpms"

        # Allow config data to override
        if self.config.distgit.namespace is not Missing:
            self.namespace = self.config.distgit.namespace

        self.qualified_name = "%s/%s" % (self.namespace, self.name)
        self.qualified_key = "%s/%s" % (self.namespace, self.distgit_key)

        # Includes information to identify the metadata being used with each log message
        self.logger = logutil.EntityLoggingAdapter(logger=self.runtime.logger, extra={'entity': self.qualified_key})

        self._distgit_repo = None

    def save(self):
        self.data_obj.data = self.config.primitive()
        self.data_obj.save()

    def distgit_remote_url(self):
        pkgs_host = self.runtime.group_config.urls.get('pkgs_host', 'pkgs.devel.redhat.com')
        # rhpkg uses a remote named like this to pull content from distgit
        if self.runtime.user:
            return f'ssh://{self.runtime.user}@{pkgs_host}/{self.qualified_name}'
        return f'ssh://{pkgs_host}/{self.qualified_name}'

    def distgit_repo(self, autoclone=True):
        if self._distgit_repo is None:
            self._distgit_repo = DISTGIT_TYPES[self.meta_type](self, autoclone=autoclone)
        return self._distgit_repo

    def branch(self):
        if self.config.distgit.branch is not Missing:
            return self.config.distgit.branch
        return self.runtime.branch

    def candidate_brew_tag(self):
        return '{}-candidate'.format(self.branch())

    def get_arches(self):
        """
        :return: Returns the list of architecture this image/rpm should build for. This is an intersection
        of config specific arches & globally enabled arches in group.yml
        """
        if self.config.arches:
            ca = self.config.arches
            intersection = list(set(self.runtime.get_global_arches()) & set(ca))
            if len(intersection) != len(ca):
                self.logger.info(f'Arches are being pruned by group.yml. Using computed {intersection} vs config list {ca}')
            if not intersection:
                raise ValueError(f'No arches remained enabled in {self.qualified_key}')
            return intersection
        else:
            return list(self.runtime.get_global_arches())

    def cgit_url(self, filename):
        rev = self.branch()
        ret = "/".join((self.runtime.group_config.urls.cgit, self.qualified_name, "plain", filename))
        if rev is not None:
            ret = "{}?h={}".format(ret, rev)
        return ret

    def fetch_cgit_file(self, filename):
        url = self.cgit_url(filename)
        req = exectools.retry(
            3, lambda: urllib.request.urlopen(url),
            check_f=lambda req: req.code == 200)
        return req.read()

    def get_latest_build(self, default=-1):
        """
        :param default: A value to return if no latest is found (if not specified, an exception will be thrown)
        :return: Returns the most recent build object from koji.
                 Example https://gist.github.com/jupierce/e6bfd98a3777ae5d56e0f7e92e5db0c9
        """
        component_name = self.get_component_name()
        with self.runtime.pooled_koji_client_session() as koji_api:
            builds = koji_api.getLatestBuilds(self.candidate_brew_tag(), package=component_name)
            if not builds:
                if default != -1:
                    self.logger.warning("No builds detected for using tag: %s" % (self.candidate_brew_tag()))
                    return default
                raise IOError("No builds detected for %s using tag: %s" % (self.qualified_name, self.candidate_brew_tag()))
            return builds[0]

    def get_latest_build_info(self, default=-1):
        """
        Queries brew to determine the most recently built release of the component
        associated with this image. This method does not rely on the "release"
        label needing to be present in the Dockerfile.
        :param default: A value to return if no latest is found (if not specified, an exception will be thrown)
        :return: A tuple: (component name, version, release); e.g. ("registry-console-docker", "v3.6.173.0.75", "1")
        """
        build = self.get_latest_build(default=default)
        if default != -1 and build == default:
            return default
        return build['name'], build['version'], build['release']

    def get_component_name(self, default=-1):
        """
        :param default: If the component name cannot be determine,
        :return: Returns the component name of the image. This is the name in the nvr
        that brew assigns to this image's build.
        """
        raise IOError('Subclass must implement')

    def needs_rebuild(self):
        """
        Check whether the commit that we recorded in the distgit content (according to cgit)
        matches the commit of the source (according to git ls-remote) and has been built
        (according to brew). Nothing is cloned and no existing clones are consulted.
        Returns: (<bool>, message). If True, message describing the details is returned. If False,
                None is returned.
        """
        component_name = self.get_component_name(default='')
        if not component_name:
            # This can happen for RPMs if they have never been rebased into
            # distgit.
            return True, 'Could not find component name; assuming never built'

        latest_build = self.get_latest_build(default='')
        if not latest_build:
            # Truly never built.
            return True, f'Component {component_name} has never been built'

        latest_build_creation_event_id = latest_build['creation_event_id']
        with self.runtime.pooled_koji_client_session() as koji_api:
            # getEvent returns something like {'id': 31825801, 'ts': 1591039601.2667}
            latest_build_creation_ts = int(koji_api.getEvent(latest_build_creation_event_id)['ts'])

        dgr = self.distgit_repo()
        with Dir(dgr.distgit_dir):
            ts, _ = exectools.cmd_assert('git show -s --format=%ct HEAD')
            distgit_head_commit_millis = int(ts)

        one_hour = (1 * 60 * 60 * 1000)  # in milliseconds

        if not dgr.has_source():
            if distgit_head_commit_millis > latest_build_creation_ts:
                # Two options:
                # 1. A user has made a commit to this dist-git only branch and there has been no build attempt
                # 2. We've already tried a build and the build failed.
                # To balance these two options, if the diff > 1 hour, request a build.
                if (distgit_head_commit_millis - latest_build_creation_ts) > one_hour:
                    return True, 'Distgit only repo commit is at least one hour older than most recent build'
            return False, 'Distgit only repo commit is older than most recent build'

        # We have source.
        with Dir(dgr.source_path()):
            ts, _ = exectools.cmd_assert('git show -s --format=%ct HEAD')
            upstream_source_head_commit_millis = int(ts)

        if upstream_source_head_commit_millis > distgit_head_commit_millis:
            # Someone has committed something new upstream. Easy call to build.
            return True, 'Upstream source commit change newer than distgit commit'
        else:
            if distgit_head_commit_millis > latest_build_creation_ts:
                # Distgit is ahead of the latest build.
                # We've likely made an attempt to rebase and the subsequent build failed.
                # Try again if we are at least 6 hours out from the build to avoid
                # pestering image owners will repeated build failures.
                if distgit_head_commit_millis - latest_build_creation_ts > (6 * one_hour):
                    return True, 'It has been 6 hours since last failed build attempt'
                return False, f'Distgit commit ts {distgit_head_commit_millis} ahead of last successful build ts {latest_build_creation_ts}, but holding off for at least 6 hours before rebuild'
            else:
                # The latest build is newer than the latest distgit commit. No change required.
                return False, 'Latest build is newer than latest distgit commit -- no build required'

    def get_maintainer_info(self):
        """
        :return: Returns a dict of identifying maintainer information. Dict might be empty if no maintainer information is available.
            fields are generally [ component: '...', subcomponent: '...', and product: '...' ] if available. These
            are coordinates for product security to figure out where to file bugs when an image or RPM has an issue.
        """

        # We are trying to discover some team information that indicates which BZ or Jira board bugs for this
        # component should be filed against. This information can be stored in the doozer metadata OR
        # in upstream source. Metadata overrides, as usual.

        source_dir = self.runtime.resolve_source(self)

        # Maintainer info can be defined in metadata, so try there first.
        maintainer = self.config.maintainer or dict()

        # This tuple will also define key ordering in the returned OrderedDict
        known_fields = ('product', 'component', 'subcomponent')

        # Fill in any missing attributes from upstream source
        if source_dir:
            with Dir(source_dir):
                # Not every repo has a master branch, they may have a different default; detect it.
                remote_info, _ = exectools.cmd_assert('git remote show origin')
                head_branch_lines = [i for i in remote_info.splitlines() if i.strip().startswith('HEAD branch:')]  # e.g. [ "  HEAD branch: master" ]
                if not head_branch_lines:
                    raise IOError('Error trying to detect remote default branch')
                default_branch = head_branch_lines[0].strip().split()[-1]  # [ "  HEAD branch: master" ] => "master"

                _, owners_yaml, _ = exectools.cmd_gather(f'git --no-pager show origin/{default_branch}:OWNERS')
                if owners_yaml.strip():
                    owners = yaml.safe_load(owners_yaml)
                    for field in known_fields:
                        if field not in maintainer and field in owners:
                            maintainer[field] = owners[field]

        if 'product' not in maintainer:
            maintainer['product'] = 'OpenShift Container Platform'  # Safe bet - we are ART.

        # Just so we return things in a defined order (avoiding unnecessary changes in git commits)
        sorted_maintainer = OrderedDict()
        for k in known_fields:
            if k in maintainer:
                sorted_maintainer[k] = maintainer[k]

        # Add anything remaining in alpha order
        for k in sorted(maintainer.keys()):
            if k not in sorted_maintainer:
                sorted_maintainer[k] = maintainer[k]

        return sorted_maintainer
