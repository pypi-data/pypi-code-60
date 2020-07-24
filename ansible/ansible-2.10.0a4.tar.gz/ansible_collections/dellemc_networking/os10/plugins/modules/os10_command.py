#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Peter Sprygada <psprygada@ansible.com>
# Copyright: (c) 2020, Dell Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
---
module: os10_command
version_added: "2.2"
author: "Senthil Kumar Ganesan (@skg-net)"
short_description: Run commands on remote devices running Dell OS10
description:
  - Sends arbitrary commands to a Dell EMC OS10 node and returns the results
    read from the device. This module includes an
    argument that will cause the module to wait for a specific condition
    before returning or timing out if the condition is not met.
  - This module does not support running commands in configuration mode.
    Please use M(os10_config) to configure Dell EMC OS10 devices.
extends_documentation_fragment: dellemc_networking.os10.os10
options:
  commands:
    description:
      - List of commands to send to the remote OS10 device over the
        configured provider. The resulting output from the command
        is returned. If the I(wait_for) argument is provided, the
        module is not returned until the condition is satisfied or
        the number of retries has expired.
    type: list
    required: true
  wait_for:
    description:
      - List of conditions to evaluate against the output of the
        command. The task will wait for each condition to be true
        before moving forward. If the conditional is not true
        within the configured number of I(retries), the task fails.
        See examples.
    type: list
    version_added: "2.2"
  match:
    description:
      - The I(match) argument is used in conjunction with the
        I(wait_for) argument to specify the match policy.  Valid
        values are C(all) or C(any).  If the value is set to C(all)
        then all conditionals in the wait_for must be satisfied.  If
        the value is set to C(any) then only one of the values must be
        satisfied.
    type: str
    default: all
    choices: [ all, any ]
    version_added: "2.5"
  retries:
    description:
      - Specifies the number of retries a command should be tried
        before it is considered failed. The command is run on the
        target device every retry and evaluated against the
        I(wait_for) conditions.
    type: int
    default: 10
  interval:
    description:
      - Configures the interval in seconds to wait between retries
        of the command. If the command does not pass the specified
        conditions, the interval indicates how long to wait before
        trying the command again.
    type: int
    default: 1
"""

EXAMPLES = """
tasks:
  - name: run show version on remote devices
    os10_command:
      commands: show version

  - name: run show version and check to see if output contains OS10
    os10_command:
      commands: show version
      wait_for: result[0] contains OS10

  - name: run multiple commands on remote nodes
    os10_command:
      commands:
        - show version
        - show interface

  - name: run multiple commands and evaluate the output
    os10_command:
      commands:
        - show version
        - show interface
      wait_for:
        - result[0] contains OS10
        - result[1] contains Ethernet
"""

RETURN = """
stdout:
  description: The set of responses from the commands
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: ['...', '...']
stdout_lines:
  description: The value of stdout split into a list
  returned: always apart from low level errors (such as action plugin)
  type: list
  sample: [['...', '...'], ['...'], ['...']]
failed_conditions:
  description: The list of conditionals that have failed
  returned: failed
  type: list
  sample: ['...', '...']
warnings:
  description: The list of warnings (if any) generated by module based on arguments
  returned: always
  type: list
  sample: ['...', '...']
"""
import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc_networking.os10.plugins.module_utils.network.os10 import run_commands
from ansible_collections.dellemc_networking.os10.plugins.module_utils.network.os10 import os10_argument_spec, check_args
from ansible.module_utils.network.common.utils import ComplexList
from ansible.module_utils.network.common.parsing import Conditional
from ansible.module_utils.six import string_types

def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).split('\n')
        yield item


def parse_commands(module, warnings):
    command = ComplexList(dict(
        command=dict(key=True),
        prompt=dict(),
        answer=dict()
    ), module)
    commands = command(module.params['commands'])
    for index, item in enumerate(commands):
        if module.check_mode and not item['command'].startswith('show'):
            warnings.append(
                'only show commands are supported when using check mode, not '
                'executing `%s`' % item['command']
            )
        elif item['command'].startswith('conf'):
            module.fail_json(
                msg='os10_command does not support running config mode '
                    'commands.  Please use os10_config instead'
            )
    return commands


def main():
    """main entry point for module execution
    """
    argument_spec = dict(
        # { command: <str>, prompt: <str>, response: <str> }
        commands=dict(type='list', required=True),

        wait_for=dict(type='list'),
        match=dict(default='all', choices=['all', 'any']),

        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int')
    )

    argument_spec.update(os10_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = {'changed': False}

    warnings = list()
    check_args(module, warnings)
    commands = parse_commands(module, warnings)
    result['warnings'] = warnings

    wait_for = module.params['wait_for'] or list()
    conditionals = [Conditional(c) for c in wait_for]

    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']

    while retries > 0:
        responses = run_commands(module, commands)

        for item in list(conditionals):
            if item(responses):
                if match == 'any':
                    conditionals = list()
                    break
                conditionals.remove(item)

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not been satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result.update({
        'changed': False,
        'stdout': responses,
        'stdout_lines': list(to_lines(responses))
    })

    module.exit_json(**result)


if __name__ == '__main__':
    main()
