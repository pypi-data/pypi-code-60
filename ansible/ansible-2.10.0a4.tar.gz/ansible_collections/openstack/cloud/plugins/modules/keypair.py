#!/usr/bin/python

# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
# Copyright (c) 2013, Benno Joy <benno@ansible.com>
# Copyright (c) 2013, John Dewey <john@dewey.ws>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: keypair
short_description: Add/Delete a keypair from OpenStack
author: "Benno Joy (@bennojoy)"
description:
  - Add or Remove key pair from OpenStack
options:
  name:
    description:
      - Name that has to be given to the key pair
    required: true
    type: str
  public_key:
    description:
      - The public key that would be uploaded to nova and injected into VMs
        upon creation.
    type: str
  public_key_file:
    description:
      - Path to local file containing ssh public key. Mutually exclusive
        with public_key.
    type: str
  state:
    description:
      - Should the resource be present or absent. If state is replace and
        the key exists but has different content, delete it and recreate it
        with the new content.
    choices: [present, absent, replace]
    default: present
    type: str
requirements:
    - "python >= 3.6"
    - "openstacksdk"

extends_documentation_fragment:
- openstack.cloud.openstack
'''

EXAMPLES = '''
# Creates a key pair with the running users public key
- openstack.cloud.keypair:
      cloud: mordred
      state: present
      name: ansible_key
      public_key_file: /home/me/.ssh/id_rsa.pub

# Creates a new key pair and the private key returned after the run.
- openstack.cloud.keypair:
      cloud: rax-dfw
      state: present
      name: ansible_key
'''

RETURN = '''
id:
    description: Unique UUID.
    returned: success
    type: str
name:
    description: Name given to the keypair.
    returned: success
    type: str
public_key:
    description: The public key value for the keypair.
    returned: success
    type: str
private_key:
    description: The private key value for the keypair.
    returned: Only when a keypair is generated for the user (e.g., when creating one
              and a public key is not specified).
    type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.openstack.cloud.plugins.module_utils.openstack import (openstack_full_argument_spec,
                                                                                openstack_module_kwargs,
                                                                                openstack_cloud_from_module)


def _system_state_change(module, keypair):
    state = module.params['state']
    if state == 'present' and not keypair:
        return True
    if state == 'absent' and keypair:
        return True
    return False


def main():
    argument_spec = openstack_full_argument_spec(
        name=dict(required=True),
        public_key=dict(default=None),
        public_key_file=dict(default=None),
        state=dict(default='present',
                   choices=['absent', 'present', 'replace']),
    )

    module_kwargs = openstack_module_kwargs(
        mutually_exclusive=[['public_key', 'public_key_file']])

    module = AnsibleModule(argument_spec,
                           supports_check_mode=True,
                           **module_kwargs)

    state = module.params['state']
    name = module.params['name']
    public_key = module.params['public_key']

    if module.params['public_key_file']:
        with open(module.params['public_key_file']) as public_key_fh:
            public_key = public_key_fh.read().rstrip()

    sdk, cloud = openstack_cloud_from_module(module)
    try:
        keypair = cloud.get_keypair(name)

        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, keypair))

        if state in ('present', 'replace'):
            if keypair and keypair['name'] == name:
                if public_key and (public_key != keypair['public_key']):
                    if state == 'present':
                        module.fail_json(
                            msg="Key name %s present but key hash not the same"
                                " as offered. Delete key first." % name
                        )
                    else:
                        cloud.delete_keypair(name)
                        keypair = cloud.create_keypair(name, public_key)
                        changed = True
                else:
                    changed = False
            else:
                keypair = cloud.create_keypair(name, public_key)
                changed = True

            module.exit_json(changed=changed,
                             key=keypair,
                             id=keypair['id'])

        elif state == 'absent':
            if keypair:
                cloud.delete_keypair(name)
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
