#
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
The arg spec for the nxos_vlans module
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class VlansArgs(object):
    """The arg spec for the nxos_vlans module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "running_config": {"type": "str"},
        "config": {
            "elements": "dict",
            "options": {
                "enabled": {"type": "bool"},
                "mapped_vni": {"type": "int"},
                "mode": {"choices": ["ce", "fabricpath"], "type": "str"},
                "name": {"type": "str"},
                "vlan_id": {"required": True, "type": "int"},
                "state": {"choices": ["active", "suspend"], "type": "str"},
            },
            "type": "list",
        },
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }
