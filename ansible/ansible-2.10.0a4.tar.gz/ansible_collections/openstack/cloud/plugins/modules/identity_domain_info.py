#!/usr/bin/python
# Copyright (c) 2016 Hewlett-Packard Enterprise Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: identity_domain_info
short_description: Retrieve information about one or more OpenStack domains
author: "Ricardo Carrillo Cruz (@rcarrillocruz)"
description:
    - Retrieve information about a one or more OpenStack domains
    - This module was called C(openstack.cloud.identity_domain_facts) before Ansible 2.9, returning C(ansible_facts).
      Note that the M(openstack.cloud.identity_domain_info) module no longer returns C(ansible_facts)!
options:
   name:
     description:
        - Name or ID of the domain
     type: str
   filters:
     description:
        - A dictionary of meta data to use for further filtering.  Elements of
          this dictionary may be additional dictionaries.
     type: dict
requirements:
    - "python >= 3.6"
    - "openstacksdk"

extends_documentation_fragment:
- openstack.cloud.openstack
'''

EXAMPLES = '''
# Gather information about previously created domain
- openstack.cloud.identity_domain_info:
    cloud: awesomecloud
  register: result
- debug:
    msg: "{{ result.openstack_domains }}"

# Gather information about a previously created domain by name
- openstack.cloud.identity_domain_info:
    cloud: awesomecloud
    name: demodomain
  register: result
- debug:
    msg: "{{ result.openstack_domains }}"

# Gather information about a previously created domain with filter
- openstack.cloud.identity_domain_info:
    cloud: awesomecloud
    name: demodomain
    filters:
      enabled: false
  register: result
- debug:
    msg: "{{ result.openstack_domains }}"
'''


RETURN = '''
openstack_domains:
    description: has all the OpenStack information about domains
    returned: always, but can be null
    type: complex
    contains:
        id:
            description: Unique UUID.
            returned: success
            type: str
        name:
            description: Name given to the domain.
            returned: success
            type: str
        description:
            description: Description of the domain.
            returned: success
            type: str
        enabled:
            description: Flag to indicate if the domain is enabled.
            returned: success
            type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.openstack.cloud.plugins.module_utils.openstack import (openstack_full_argument_spec,
                                                                                openstack_module_kwargs,
                                                                                openstack_cloud_from_module)


def main():

    argument_spec = openstack_full_argument_spec(
        name=dict(required=False, default=None),
        filters=dict(required=False, type='dict', default=None),
    )
    module_kwargs = openstack_module_kwargs(
        mutually_exclusive=[
            ['name', 'filters'],
        ]
    )
    module = AnsibleModule(argument_spec, **module_kwargs)
    is_old_facts = module._name == 'openstack.cloud.identity_domain_facts'
    if is_old_facts:
        module.deprecate("The 'openstack.cloud.identity_domain_facts' module has been renamed to 'openstack.cloud.identity_domain_info', "
                         "and the renamed one no longer returns ansible_facts", version='2.13')

    sdk, opcloud = openstack_cloud_from_module(module)
    try:
        name = module.params['name']
        filters = module.params['filters']

        if name:
            # Let's suppose user is passing domain ID
            try:
                domains = opcloud.get_domain(name)
            except Exception:
                domains = opcloud.search_domains(filters={'name': name})

        else:
            domains = opcloud.search_domains(filters)

        if is_old_facts:
            module.exit_json(changed=False, ansible_facts=dict(
                openstack_domains=domains))
        else:
            module.exit_json(changed=False, openstack_domains=domains)

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
