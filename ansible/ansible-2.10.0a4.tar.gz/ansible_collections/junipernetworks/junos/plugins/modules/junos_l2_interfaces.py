#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the resource
#   module builder playbook.
#
# Do not edit this file manually.
#
# Changes to this file will be over written
#   by the resource module builder.
#
# Changes should be made in the model used to
#   generate this file or in the resource module
#   builder template.
#
#############################################

"""
The module file for junos_l2_interfaces
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: junos_l2_interfaces
short_description: L2 interfaces resource module
description: This module provides declarative management of a Layer-2 interface on
  Juniper JUNOS devices.
version_added: 1.0.0
author: Ganesh Nalawade (@ganeshrn)
options:
  config:
    description: A dictionary of Layer-2 interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Full name of interface, e.g. ge-0/0/1.
        type: str
        required: true
      unit:
        description:
        - Logical interface number. Value of C(unit) should be of type integer.
        type: int
      access:
        description:
        - Configure the interface as a Layer 2 access mode.
        type: dict
        suboptions:
          vlan:
            description:
            - Configure the access VLAN ID.
            type: str
      trunk:
        description:
        - Configure the interface as a Layer 2 trunk mode.
        type: dict
        suboptions:
          allowed_vlans:
            description:
            - List of VLANs to be configured in trunk port. It's used as the VLAN
              range to ADD or REMOVE from the trunk.
            type: list
          native_vlan:
            description:
            - Native VLAN to be configured in trunk port. It is used as the trunk
              native VLAN ID.
            type: str
      enhanced_layer:
        description:
        - True if your device has Enhanced Layer 2 Software (ELS). If the l2 configuration
          is under C(interface-mode) the value is True else if the l2 configuration
          is under C(port-mode) value is False
        type: bool
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    default: merged
    description:
    - The state of the configuration after module completion
    type: str
requirements:
- ncclient (>=v0.6.4)
notes:
- This module requires the netconf system service be enabled on the remote device
  being managed.
- Tested against vSRX JUNOS version 18.4R1.
- This module works with connection C(netconf). See L(the Junos OS Platform Options,../network/user_guide/platform_junos.html).
"""
EXAMPLES = """
# Using deleted

# Before state:
# -------------
#
# ansible@junos01# show interfaces
# ge-0/0/1 {
#    description "L2 interface";
#    speed 1g;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode access;
#            vlan {
#                members vlan30;
#            }
#        }
#    }
#}
#ge-0/0/2 {
#    description "non L2 interface";
#    unit 0 {
#        family inet {
#            address 192.168.56.14/24;
#        }
#    }

- name: "Delete L2 attributes of given interfaces (Note: This won't delete the
    interface itself)."
  junipernetworks.junos.junos_l2_interfaces:
    config:
    - name: ge-0/0/1
    - name: ge-0/0/2
    state: deleted

# After state:
# ------------
#
# ansible@junos01# show interfaces
# ge-0/0/1 {
#    description "L2 interface";
#    speed 1g;
# }
#ge-0/0/2 {
#    description "non L2 interface";
#    unit 0 {
#        family inet {
#            address 192.168.56.14/24;
#        }
#    }


# Using merged

# Before state:
# -------------
# ansible@junos01# show interfaces
# ge-0/0/3 {
#    description "test interface";
#    speed 1g;
#}
# ge-0/0/4 {
#    description interface-trunk;
#    native-vlan-id 100;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode trunk;
#            vlan {
#                members [ vlan40 ];
#            }
#        }
#    }
# }

- name: Merge provided configuration with device configuration (default operation
    is merge)
  junipernetworks.junos.junos_l2_interfaces:
    config:
    - name: ge-0/0/3
      access:
        vlan: v101
    - name: ge-0/0/4
      trunk:
        allowed_vlans:
        - vlan30
        native_vlan: 50
    state: merged

# After state:
# ------------
# user@junos01# show interfaces
# ge-0/0/3 {
#    description "test interface";
#    speed 1g;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode access;
#            vlan {
#                members v101;
#            }
#        }
#    }
# }
# ge-0/0/4 {
#    description interface-trunk;
#    native-vlan-id 50;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode trunk;
#            vlan {
#                members [ vlan40 vlan30 ];
#            }
#        }
#    }
# }


# Using overridden

# Before state:
# -------------
# ansible@junos01# show interfaces
# ge-0/0/3 {
#    description "test interface";
#    speed 1g;
#}
# ge-0/0/4 {
#    description interface-trunk;
#    native-vlan-id 100;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode trunk;
#            vlan {
#                members [ vlan40 ];
#            }
#        }
#    }
# }
# ge-0/0/5 {
#    description "Configured by Ansible-11";
#    unit 0 {
#        family ethernet-switching {
#            interface-mode access;
#            vlan {
#                members v101;
#            }
#        }
#    }
# }

- name: Override provided configuration with device configuration
  junipernetworks.junos.junos_l2_interfaces:
    config:
    - name: ge-0/0/3
      access:
        vlan: v101
    - name: ge-0/0/4
      trunk:
        allowed_vlans:
        - vlan30
        native_vlan: 50
    state: overridden

# After state:
# ------------
# user@junos01# show interfaces
# ge-0/0/3 {
#    unit 0 {
#        family ethernet-switching {
#            interface-mode access;
#            vlan {
#                members v101;
#            }
#        }
#    }
# }
# ge-0/0/4 {
#    description interface-trunk;
#    native-vlan-id 50;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode trunk;
#            vlan {
#                members [ vlan30 ];
#            }
#        }
#    }
# }


# Using replaced

# Before state:
# -------------
# ansible@junos01# show interfaces
# ge-0/0/3 {
#    description "test interface";
#    speed 1g;
#}
# ge-0/0/4 {
#    description interface-trunk;
#    native-vlan-id 100;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode trunk;
#            vlan {
#                members [ vlan40 ];
#            }
#        }
#    }
# }

- name: Replace provided configuration with device configuration
  junipernetworks.junos.junos_l2_interfaces:
    config:
    - name: ge-0/0/3
      access:
        vlan: v101
    - name: ge-0/0/4
      trunk:
        allowed_vlans:
        - vlan30
        native_vlan: 50
    state: replaced

# After state:
# ------------
# user@junos01# show interfaces
# ge-0/0/3 {
#    unit 0 {
#        family ethernet-switching {
#            interface-mode access;
#            vlan {
#                members v101;
#            }
#        }
#    }
# }
# ge-0/0/4 {
#    description interface-trunk;
#    native-vlan-id 50;
#    unit 0 {
#        family ethernet-switching {
#            interface-mode trunk;
#            vlan {
#                members [ vlan30 ];
#            }
#        }
#    }
# }


"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['command 1', 'command 2', 'command 3']
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.argspec.l2_interfaces.l2_interfaces import (
    L2_interfacesArgs,
)
from ansible_collections.junipernetworks.junos.plugins.module_utils.network.junos.config.l2_interfaces.l2_interfaces import (
    L2_interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
    ]

    module = AnsibleModule(
        argument_spec=L2_interfacesArgs.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    result = L2_interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
