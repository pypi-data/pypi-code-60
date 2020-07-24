#!/usr/bin/python
'''
# (c) 2020, NetApp, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
'''

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = '''
author: NetApp Ansible Team (@carchi8py) <ng-ansibleteam@netapp.com>
description:
  - Call a ZAPI on ONTAP.
  - Cluster ZAPIs are run using a cluster admin account.
  - Vserver ZAPIs can be run using a vsadmin account or using vserver tunneling (cluster admin with I(vserver option)).
  - In case of success, a json dictionary is returned as C(response).
  - In case of a ZAPI error, C(status), C(errno), C(reason) are set to help with diagnosing the issue,
  - and the call is reported as an error ('failed').
  - Other errors (eg connection issues) are reported as Ansible error.
extends_documentation_fragment:
  - netapp.ontap.netapp.na_ontap
module: na_ontap_zapit
short_description: NetApp ONTAP Run any ZAPI on ONTAP
version_added: "20.4.0"
options:
    zapi:
        description:
        - A dictionary for the zapi and arguments.
        - An XML tag I(<tag>value</tag>) is a dictionary with tag as the key.
        - Value can be another dictionary, a list of dictionaries, a string, or nothing.
        - eg I(<tag/>) is represented as I(tag:)
        - A single zapi can be called at a time.  Ansible warns if duplicate keys are found and only uses the last entry.
        required: true
        type: dict
    vserver:
        description:
        - if provided, forces vserver tunneling.  username identifies a cluster admin account.
        type: str
'''

EXAMPLES = """
-
  name: Ontap ZAPI
  hosts: localhost
  gather_facts: False
  collections:
    - netapp.ontap
  vars:
    login: &login
      hostname: "{{ admin_ip }}"
      username: "{{ admin_username }}"
      password: "{{ admin_password }}"
      https: true
      validate_certs: false
    svm_login: &svm_login
      hostname: "{{ svm_admin_ip }}"
      username: "{{ svm_admin_username }}"
      password: "{{ svm_admin_password }}"
      https: true
      validate_certs: false

  tasks:
    - name: run ontap ZAPI command as cluster admin
      na_ontap_zapit:
        <<: *login
        zapi:
          system-get-version:
      register: output
    - debug: var=output

    - name: run ontap ZAPI command as cluster admin
      na_ontap_zapit:
        <<: *login
        zapi:
          vserver-get-iter:
      register: output
    - debug: var=output

    - name: run ontap ZAPI command as cluster admin
      na_ontap_zapit:
        <<: *login
        zapi:
          vserver-get-iter:
            desired-attributes:
              vserver-info:
                - aggr-list:
                    - aggr-name
                - allowed-protocols:
                    - protocols
                - vserver-aggr-info-list:
                    - vserser-aggr-info
                - uuid
            query:
              vserver-info:
                vserver-name: trident_svm
      register: output
    - debug: var=output

    - name: run ontap ZAPI command as vsadmin
      na_ontap_zapit:
        <<: *svm_login
        zapi:
          vserver-get-iter:
            desired-attributes:
              vserver-info:
                - uuid
      register: output
    - debug: var=output

    - name: run ontap ZAPI command as vserver tunneling
      na_ontap_zapit:
        <<: *login
        vserver: trident_svm
        zapi:
          vserver-get-iter:
            desired-attributes:
              vserver-info:
                - uuid
      register: output
    - debug: var=output

    - name: run ontap active-directory ZAPI command
      na_ontap_zapit:
        <<: *login
        vserver: trident_svm
        zapi:
          active-directory-account-create:
            account-name: testaccount
            admin-username: testuser
            admin-password: testpass
            domain: testdomain
            organizational-unit: testou
      register: output
      ignore_errors: True
    - debug: var=output

"""

RETURN = """
response:
  description:
    - If successful, a json dictionary representing the data returned by the ZAPI.
    - If the ZAPI was executed but failed, an empty dictionary.
    - Not present if the ZAPI call cannot be performed.
  returned: On success
  type: dict
status:
  description:
    - If the ZAPI was executed but failed, the status set by the ZAPI.
    - Not present if successful, or if the ZAPI call cannot be performed.
  returned: On error
  type: str
errno:
  description:
    - If the ZAPI was executed but failed, the error code set by the ZAPI.
    - Not present if successful, or if the ZAPI call cannot be performed.
  returned: On error
  type: str
reason:
  description:
    - If the ZAPI was executed but failed, the error reason set by the ZAPI.
    - Not present if successful, or if the ZAPI call cannot be performed.
  returned: On error
  type: str
"""

import traceback
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
import ansible_collections.netapp.ontap.plugins.module_utils.netapp as netapp_utils

try:
    import xmltodict
    HAS_XMLTODICT = True
except ImportError:
    HAS_XMLTODICT = False

try:
    import json
    HAS_JSON = True
except ImportError:
    HAS_JSON = False

HAS_NETAPP_LIB = netapp_utils.has_netapp_lib()


class NetAppONTAPZapi(object):
    ''' calls a ZAPI command '''

    def __init__(self):
        self.argument_spec = netapp_utils.na_ontap_host_argument_spec()
        self.argument_spec.update(dict(
            zapi=dict(required=True, type='dict'),
            vserver=dict(required=False, type='str'),
        ))
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        parameters = self.module.params
        # set up state variables
        self.zapi = parameters['zapi']
        self.vserver = parameters['vserver']

        if not HAS_JSON:
            self.module.fail_json(msg="the python json module is required")
        if not HAS_XMLTODICT:
            self.module.fail_json(msg="the python xmltodict module is required")
        if not HAS_NETAPP_LIB:
            self.module.fail_json(msg="the python NetApp-Lib module is required")

        if self.vserver is not None:
            self.server = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)
        else:
            self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)

    def asup_log_for_cserver(self, event_name):
        """
        Fetch admin vserver for the given cluster
        Create and Autosupport log event with the given module name
        :param event_name: Name of the event log
        :return: None
        """
        results = netapp_utils.get_cserver(self.server)
        cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
        try:
            netapp_utils.ems_log_event(event_name, cserver)
        except netapp_utils.zapi.NaApiError as error:
            pass

    def jsonify_and_parse_output(self, xml_data):
        ''' convert from XML to JSON
            extract status and error fields is present
        '''
        try:
            as_dict = xmltodict.parse(xml_data.to_string(), xml_attribs=True)
        except Exception as exc:
            self.module.fail_json(msg='Error running zapi in xmltodict: %s: %s' %
                                  (xml_data.to_string(), str(exc)))
        try:
            as_json = json.loads(json.dumps(as_dict))
        except Exception as exc:
            self.module.fail_json(msg='Error running zapi in json load/dump: %s: %s' %
                                  (as_dict, str(exc)))

        if 'results' not in as_json:
            self.module.fail_json(msg='Error running zapi, no results field: %s: %s' %
                                  (xml_data.to_string(), str(exc)))

        # set status, and if applicable errno/reason, and remove attribute fields
        errno = None
        reason = None
        response = as_json.pop('results')
        status = response.get('@status', 'no_status_attr')
        if status != 'passed':
            # collect errno and reason
            errno = response.get('@errno', None)
            if errno is None:
                errno = response.get('errorno', None)
            if errno is None:
                errno = 'ESTATUSFAILED'
            reason = response.get('@reason', None)
            if reason is None:
                reason = response.get('reason', None)
            if reason is None:
                reason = 'Execution failure with unknown reason.'

        for key in ('@status', '@errno', '@reason', '@xmlns'):
            try:
                # remove irrelevant info
                del response[key]
            except KeyError:
                pass
        return response, status, errno, reason

    def run_zapi(self):
        ''' calls the ZAPI '''
        zapi_struct = self.zapi
        error = None
        if not isinstance(zapi_struct, dict):
            error = 'A directory entry is expected, eg: system-get-version: '
            zapi = zapi_struct
        else:
            zapi = list(zapi_struct.keys())
            if len(zapi) != 1:
                error = 'A single ZAPI can be called at a time'
            else:
                zapi = zapi[0]

        # log first, then error out as needed
        self.ems(zapi)
        if error:
            self.module.fail_json(msg='%s, received: %s' % (error, zapi))

        zapi_obj = netapp_utils.zapi.NaElement(zapi)
        attributes = zapi_struct[zapi]
        if attributes is not None and attributes != 'None':
            zapi_obj.translate_struct(attributes)

        try:
            output = self.server.invoke_elem(zapi_obj, True)
        except netapp_utils.zapi.NaApiError as error:
            self.module.fail_json(msg='Error running zapi %s: %s' %
                                  (zapi, to_native(error)),
                                  exception=traceback.format_exc())

        return self.jsonify_and_parse_output(output)

    def ems(self, zapi):
        """
        Error out if Cluster Admin username is used with Vserver, or Vserver admin used with out vserver being set
        :return:
        """
        if self.vserver:
            try:
                netapp_utils.ems_log_event("na_ontap_zapi" + str(zapi), self.server)
            except netapp_utils.zapi.NaApiError as error:
                pass
        else:
            self.asup_log_for_cserver("na_ontap_zapi: " + str(zapi))

    def apply(self):
        ''' calls the zapi and returns json output '''
        response, status, errno, reason = self.run_zapi()
        if status == 'passed':
            self.module.exit_json(changed=True, response=response)
        msg = 'ZAPI failure: check errno and reason.'
        self.module.fail_json(changed=False, response=response, status=status, errno=errno, reason=reason, msg=msg)


def main():
    """
    Execute action from playbook
    """
    zapi = NetAppONTAPZapi()
    zapi.apply()


if __name__ == '__main__':
    main()
