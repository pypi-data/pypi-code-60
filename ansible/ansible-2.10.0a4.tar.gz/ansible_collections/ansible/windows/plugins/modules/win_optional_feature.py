#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Carson Anderson <rcanderson23@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: win_optional_feature
short_description: Manage optional Windows features
description:
    - Install or uninstall optional Windows features on non-Server Windows.
    - This module uses the C(Enable-WindowsOptionalFeature) and C(Disable-WindowsOptionalFeature) cmdlets.
options:
  name:
    description:
      - The name(s) of the feature to install.
      - This relates to C(FeatureName) in the Powershell cmdlet.
      - To list all available features use the PowerShell command C(Get-WindowsOptionalFeature).
    type: list
    elements: str
    required: yes
  state:
    description:
      - Whether to ensure the feature is absent or present on the system.
    type: str
    choices: [ absent, present ]
    default: present
  include_parent:
    description:
      - Whether to enable the parent feature and the parent's dependencies.
    type: bool
    default: no
  source:
    description:
      - Specify a source to install the feature from.
      - Can either be C({driveletter}:\sources\sxs) or C(\\{IP}\share\sources\sxs).
    type: str
seealso:
- module: chocolatey.chocolatey.win_chocolatey
- module: ansible.windows.win_feature
- module: ansible.windows.win_package
author:
    - Carson Anderson (@rcanderson23)
'''

EXAMPLES = r'''
- name: Install .Net 3.5
  ansible.windows.win_optional_feature:
    name: NetFx3
    state: present

- name: Install .Net 3.5 from source
  ansible.windows.win_optional_feature:
    name: NetFx3
    source: \\share01\win10\sources\sxs
    state: present

- name: Install Microsoft Subsystem for Linux
  ansible.windows.win_optional_feature:
    name: Microsoft-Windows-Subsystem-Linux
    state: present
  register: wsl_status

- name: Reboot if installing Linux Subsytem as feature requires it
  ansible.windows.win_reboot:
  when: wsl_status.reboot_required

- name: Install multiple features in one task
  ansible.windows.win_optional_feature:
    name:
    - NetFx3
    - Microsoft-Windows-Subsystem-Linux
    state: present
'''

RETURN = r'''
reboot_required:
    description: True when the target server requires a reboot to complete updates
    returned: success
    type: bool
    sample: true
'''
