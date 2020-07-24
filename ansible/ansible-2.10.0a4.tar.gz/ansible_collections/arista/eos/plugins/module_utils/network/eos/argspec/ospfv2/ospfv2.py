#
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

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
The arg spec for the eos_ospfv2 module
"""


class Ospfv2Args(object):  # pylint: disable=R0903
    """The arg spec for the eos_ospfv2 module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        "config": {
            "options": {
                "processes": {
                    "elements": "dict",
                    "options": {
                        "process_id": {"type": "int"},
                        "vrf": {"type": "str"},
                        "traffic_engineering": {"type": "bool"},
                        "adjacency": {
                            "options": {
                                "exchange_start": {
                                    "options": {"threshold": {"type": "int"}},
                                    "type": "dict",
                                }
                            },
                            "type": "dict",
                        },
                        "areas": {
                            "elements": "dict",
                            "options": {
                                "default_cost": {"type": "int"},
                                "filter": {
                                    "options": {
                                        "address": {"type": "str"},
                                        "prefix_list": {"type": "str"},
                                        "subnet_address": {"type": "str"},
                                        "subnet_mask": {"type": "str"},
                                    },
                                    "type": "dict",
                                },
                                "not_so_stubby": {
                                    "options": {
                                        "default_information_originate": {
                                            "options": {
                                                "metric": {"type": "int"},
                                                "metric_type": {"type": "int"},
                                                "nssa_only": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                        "no_summary": {"type": "bool"},
                                        "nssa_only": {"type": "bool"},
                                        "lsa": {"type": "bool"},
                                        "set": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "nssa": {
                                    "options": {
                                        "default_information_originate": {
                                            "options": {
                                                "metric": {"type": "int"},
                                                "metric_type": {"type": "int"},
                                                "nssa_only": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                        "no_summary": {"type": "bool"},
                                        "nssa_only": {"type": "bool"},
                                        "set": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                                "area_id": {"type": "str"},
                                "range": {
                                    "options": {
                                        "address": {"type": "str"},
                                        "advertise": {"type": "bool"},
                                        "cost": {"type": "int"},
                                        "subnet_address": {"type": "str"},
                                        "subnet_mask": {"type": "str"},
                                    },
                                    "type": "dict",
                                },
                                "stub": {
                                    "options": {
                                        "no_summary": {"type": "bool"},
                                        "set": {"type": "bool"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "list",
                        },
                        "auto_cost": {
                            "options": {
                                "reference_bandwidth": {"type": "int"}
                            },
                            "type": "dict",
                        },
                        "bfd": {
                            "options": {"all_interfaces": {"type": "bool"}},
                            "type": "dict",
                        },
                        "default_information": {
                            "options": {
                                "always": {"type": "bool"},
                                "metric": {"type": "int"},
                                "metric_type": {"type": "int"},
                                "originate": {"type": "bool"},
                                "route_map": {"type": "str"},
                            },
                            "type": "dict",
                        },
                        "default_metric": {"type": "int"},
                        "distance": {
                            "options": {
                                "external": {"type": "int"},
                                "inter_area": {"type": "int"},
                                "intra_area": {"type": "int"},
                            },
                            "type": "dict",
                        },
                        "distribute_list": {
                            "options": {
                                "prefix_list": {"type": "str"},
                                "route_map": {"type": "str"},
                            },
                            "type": "dict",
                        },
                        "dn_bit_ignore": {"type": "bool"},
                        "fips_restrictions": {"type": "str"},
                        "graceful_restart": {
                            "options": {
                                "grace_period": {"type": "int"},
                                "set": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "graceful_restart_helper": {"type": "bool"},
                        "log_adjacency_changes": {
                            "options": {"detail": {"type": "bool"}},
                            "type": "dict",
                        },
                        "max_lsa": {
                            "options": {
                                "count": {"type": "int"},
                                "ignore_count": {"type": "int"},
                                "ignore_time": {"type": "int"},
                                "reset_time": {"type": "int"},
                                "threshold": {"type": "int"},
                                "warning": {"type": "bool"},
                            },
                            "type": "dict",
                        },
                        "max_metric": {
                            "options": {
                                "router_lsa": {
                                    "options": {
                                        "set": {"type": "bool"},
                                        "include_stub": {"type": "bool"},
                                        "on_startup": {
                                            "options": {
                                                "wait_period": {"type": "int"}
                                            },
                                            "type": "dict",
                                        },
                                        "summary_lsa": {
                                            "options": {
                                                "max_metric_value": {
                                                    "type": "int"
                                                },
                                                "set": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                        "external_lsa": {
                                            "options": {
                                                "max_metric_value": {
                                                    "type": "int"
                                                },
                                                "set": {"type": "bool"},
                                            },
                                            "type": "dict",
                                        },
                                    },
                                    "type": "dict",
                                }
                            },
                            "type": "dict",
                        },
                        "maximum_paths": {"type": "int"},
                        "mpls_ldp": {"type": "bool"},
                        "networks": {
                            "elements": "dict",
                            "options": {
                                "area": {"type": "str"},
                                "mask": {"type": "str"},
                                "network_address": {"type": "str"},
                                "prefix": {"type": "str"},
                            },
                            "type": "list",
                        },
                        "passive_interface": {
                            "type": "dict",
                            "options": {
                                "interface_list": {"type": "str"},
                                "default": {"type": "bool"},
                            },
                        },
                        "point_to_point": {"type": "bool"},
                        "redistribute": {
                            "elements": "dict",
                            "options": {
                                "isis_level": {"type": "str"},
                                "route_map": {"type": "str"},
                                "routes": {"type": "str"},
                            },
                            "type": "list",
                        },
                        "retransmission_threshold": {"type": "int"},
                        "rfc1583compatibility": {"type": "bool"},
                        "router_id": {"type": "str"},
                        "shutdown": {"type": "bool"},
                        "summary_address": {
                            "options": {
                                "address": {"type": "str"},
                                "attribute_map": {"type": "str"},
                                "mask": {"type": "str"},
                                "not_advertise": {"type": "bool"},
                                "prefix": {"type": "str"},
                                "tag": {"type": "int"},
                            },
                            "type": "dict",
                        },
                        "timers": {
                            "elements": "dict",
                            "options": {
                                "lsa": {
                                    "options": {
                                        "rx": {
                                            "options": {
                                                "min_interval": {"type": "int"}
                                            },
                                            "type": "dict",
                                        },
                                        "tx": {
                                            "options": {
                                                "delay": {
                                                    "options": {
                                                        "initial": {
                                                            "type": "int"
                                                        },
                                                        "max": {"type": "int"},
                                                        "min": {"type": "int"},
                                                    },
                                                    "type": "dict",
                                                }
                                            },
                                            "type": "dict",
                                        },
                                    },
                                    "type": "dict",
                                },
                                "out_delay": {"type": "int"},
                                "pacing": {"type": "int"},
                                "spf": {
                                    "options": {
                                        "initial": {"type": "int"},
                                        "max": {"type": "int"},
                                        "min": {"type": "int"},
                                        "seconds": {"type": "int"},
                                    },
                                    "type": "dict",
                                },
                            },
                            "type": "list",
                        },
                    },
                    "type": "list",
                }
            },
            "type": "dict",
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "deleted",
                "merged",
                "overridden",
                "replaced",
                "gathered",
                "rendered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
