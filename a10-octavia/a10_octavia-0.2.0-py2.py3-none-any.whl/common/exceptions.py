# Copyright 2019 A10 Networks
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

from octavia.common import exceptions
from octavia.i18n import _
from octavia.network import base


class NoDatabaseURL(exceptions.OctaviaException):
    message = _("Must set db connection url in configuration file.")


class PortCreationFailedException(base.NetworkException):
    pass


class DeallocateTrunkException(base.NetworkException):
    pass


class AllocateTrunkException(base.NetworkException):
    pass


class VRIDIPNotInSubentRangeError(base.NetworkException):
    pass


class MissingVlanIDConfigError(cfg.ConfigFileValueError):

    def __init__(self, interface_num):
        msg = ('Missing `vlan_id` attribute for `interface_num` {0} ' +
               ' in `interface_vlan_map` under ' +
               '[hardware_thunder] section.').format(interface_num)
        super(MissingVlanIDConfigError, self).__init__(msg=msg)


class DuplicateVlanTagsConfigError(cfg.ConfigFileValueError):

    def __init__(self, interface_num, vlan_id):
        msg = ('Duplicate `vlan_tags` entry of `vlan_id` {0} ' +
               'found for `interface_num` {1} in `interface_vlan_map` under ' +
               '[hardware_thunder] section.').format(vlan_id, interface_num)
        super(DuplicateVlanTagsConfigError, self).__init__(msg=msg)


class MissingInterfaceNumConfigError(cfg.ConfigFileValueError):

    def __init__(self):
        msg = (
            'Missing `interface_num` in `interface_vlan_map` under [hardware_thunder] section.')
        super(MissingInterfaceNumConfigError, self).__init__(msg=msg)


class VirtEthCollisionConfigError(cfg.ConfigFileValueError):

    def __init__(self, interface_num, vlan_id):
        msg = ('Check settings for `vlan_id` {0} of `interface_num` {1}. ' +
               'Please set `use_dhcp` to False ' +
               'before setting the `ve_ip`').format(vlan_id, interface_num)
        super(VirtEthCollisionConfigError, self).__init__(msg=msg)


class VirtEthMissingConfigError(cfg.ConfigFileValueError):

    def __init__(self, interface_num, vlan_id):
        msg = ('Check settings for `vlan_id` {0} of `interface_num` {1}. ' +
               'Missing `use_dhcp` and `ve_ip` in config. ' +
               'Please provide either.').format(vlan_id, interface_num)
        super(VirtEthMissingConfigError, self).__init__(msg=msg)


class InvalidInterfaceNumberConfigError(cfg.ConfigFileValueError):

    def __init__(self, interface_num):
        msg = ('Invalid value given for setting `interface_num` as \"{0}\". ' +
               'Please provide Integer values only.').format(interface_num)
        super(InvalidInterfaceNumberConfigError, self).__init__(msg=msg)


class InvalidVlanIdConfigError(cfg.ConfigFileValueError):

    def __init__(self, vlan_id):
        msg = ('Invalid value given for setting `vlan_id` as \"{0}\". ' +
               'Please provide Integer values only.').format(vlan_id)
        super(InvalidVlanIdConfigError, self).__init__(msg=msg)


class InvalidUseDhcpConfigError(cfg.ConfigFileValueError):

    def __init__(self, use_dhcp):
        msg = ('Invalid value given for setting `use_dhcp` as {0}. ' +
               'Please provide either "True" or "False" only.').format(use_dhcp)
        super(InvalidUseDhcpConfigError, self).__init__(msg=msg)


class VcsDevicesNumberExceedsConfigError(cfg.ConfigFileValueError):

    def __init__(self, num_devices):
        msg = ('Number of vcs devices {0} exceeds the maximum allowed value 2. ' +
               'Please reduce the devices in cluster.').format(num_devices)
        super(VcsDevicesNumberExceedsConfigError, self).__init__(msg=msg)


class InvalidVcsDeviceIdConfigError(cfg.ConfigFileValueError):

    def __init__(self, vcs_device_id):
        msg = ('Invalid `vcs_device_id` {0}, it should be in the range 1-2. ' +
               'Please provide the proper `vcs_device_id`.').format(vcs_device_id)
        super(InvalidVcsDeviceIdConfigError, self).__init__(msg=msg)


class MissingMgmtIpConfigError(cfg.ConfigFileValueError):

    def __init__(self, vcs_device_id):
        msg = ('Missing `mgmt_ip_address` for vcs device with id {0}. ' +
               'Please provide management IP address').format(vcs_device_id)
        super(MissingMgmtIpConfigError, self).__init__(msg=msg)


class InvalidVCSDeviceCount(cfg.ConfigFileValueError):

    def __init__(self, device_count):
        msg = ('Number of devices in config is should be 1 when VCS is not enabled, ' +
               'provided {0}').format(device_count)
        super(InvalidVCSDeviceCount, self).__init__(msg=msg)


class MissingVCSDeviceConfig(base.NetworkException):
    def __init__(self, device_ids):
        msg = ('Device ids {0} provided in config are not present in VCS' +
               'cluster.').format(device_ids)
        super(MissingVCSDeviceConfig, self).__init__(msg=msg)
