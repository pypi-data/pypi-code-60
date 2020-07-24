#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_serviceusage_service
description:
- A service that is available for use .
short_description: Creates a GCP Service
version_added: '2.10'
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
    type: str
  name:
    description:
    - The resource name of the service .
    required: true
    type: str
  disable_dependent_services:
    description:
    - Indicates if dependent services should also be disabled. Can only be turned
      on if service is disabled.
    required: false
    type: bool
  project:
    description:
    - The Google Cloud Platform project to use.
    type: str
  auth_kind:
    description:
    - The type of credential used.
    type: str
    required: true
    choices:
    - application
    - machineaccount
    - serviceaccount
  service_account_contents:
    description:
    - The contents of a Service Account JSON file, either in a dictionary or as a
      JSON string that represents it.
    type: jsonarg
  service_account_file:
    description:
    - The path of a Service Account JSON file if serviceaccount is selected as type.
    type: path
  service_account_email:
    description:
    - An optional service account email address if machineaccount is selected and
      the user does not wish to use the default email.
    type: str
  scopes:
    description:
    - Array of scopes to be used
    type: list
  env_type:
    description:
    - Specifies which Ansible environment you're running this module within.
    - This should not be set unless you know what you're doing.
    - This only alters the User Agent string for any API requests.
    type: str
notes:
- 'Getting Started: U(https://cloud.google.com/service-usage/docs/getting-started)'
- for authentication, you can set service_account_file using the C(gcp_service_account_file)
  env variable.
- for authentication, you can set service_account_contents using the C(GCP_SERVICE_ACCOUNT_CONTENTS)
  env variable.
- For authentication, you can set service_account_email using the C(GCP_SERVICE_ACCOUNT_EMAIL)
  env variable.
- For authentication, you can set auth_kind using the C(GCP_AUTH_KIND) env variable.
- For authentication, you can set scopes using the C(GCP_SCOPES) env variable.
- Environment variables values will only be used if the playbook values are not set.
- The I(service_account_email) and I(service_account_file) options are mutually exclusive.
'''

EXAMPLES = '''
- name: create a service
  google.cloud.gcp_serviceusage_service:
    name: spanner.googleapis.com
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - The resource name of the service .
  returned: success
  type: str
parent:
  description:
  - The name of the parent of this service. For example 'projects/123' .
  returned: success
  type: str
state:
  description:
  - Whether or not the service has been enabled for use by the consumer.
  returned: success
  type: str
disableDependentServices:
  description:
  - Indicates if dependent services should also be disabled. Can only be turned on
    if service is disabled.
  returned: success
  type: bool
config:
  description:
  - The service configuration of the available service.
  returned: success
  type: complex
  contains:
    name:
      description:
      - The DNS address at which this service is available.
      returned: success
      type: str
    title:
      description:
      - The product title for this service.
      returned: success
      type: str
    apis:
      description:
      - The list of API interfaces exported by this service.
      returned: success
      type: complex
      contains:
        name:
          description:
          - Name of the API.
          returned: success
          type: str
        version:
          description:
          - The version of the API.
          returned: success
          type: str
'''

################################################################################
# Imports
################################################################################

from ansible_collections.google.cloud.plugins.module_utils.gcp_utils import (
    navigate_hash,
    GcpSession,
    GcpModule,
    GcpRequest,
    remove_nones_from_dict,
    replace_resource_dict,
)
import json
import re
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(required=True, type='str'),
            disable_dependent_services=dict(type='bool'),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/cloud-platform']

    state = module.params['state']

    fetch = fetch_resource(module, self_link(module))
    changed = False

    if module.params['state'] == 'present' and module.params['disable_dependent_services']:
        module.fail_json(msg="You cannot enable a service and use the disable_dependent_service option")

    if fetch and fetch.get('state') == 'DISABLED':
        fetch = {}

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module))
                fetch = fetch_resource(module, self_link(module))
                changed = True
        else:
            delete(module, delete_link(module))
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, create_link(module))
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link):
    auth = GcpSession(module, 'serviceusage')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link):
    auth = GcpSession(module, 'serviceusage')
    return wait_for_operation(module, auth.put(link, resource_to_request(module)))


def delete(module, link):
    auth = GcpSession(module, 'serviceusage')
    return wait_for_operation(module, auth.post(link))


def resource_to_request(module):
    request = {u'disableDependentServices': module.params.get('disable_dependent_services')}
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, allow_not_found=True):
    auth = GcpSession(module, 'serviceusage')
    return return_if_object(module, auth.get(link), allow_not_found)


def self_link(module):
    return "https://serviceusage.googleapis.com/v1/projects/{project}/services/{name}".format(**module.params)


def collection(module):
    return "https://serviceusage.googleapis.com/v1/projects/{project}/services".format(**module.params)


def create_link(module):
    return "https://serviceusage.googleapis.com/v1/projects/{project}/services/{name}:enable".format(**module.params)


def delete_link(module):
    return "https://serviceusage.googleapis.com/v1/projects/{project}/services/{name}:disable".format(**module.params)


def return_if_object(module, response, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError):
        module.fail_json(msg="Invalid JSON response with error: %s" % response.text)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'name': response.get(u'name'),
        u'parent': response.get(u'parent'),
        u'state': response.get(u'state'),
        u'disableDependentServices': response.get(u'disableDependentServices'),
        u'config': ServiceConfig(response.get(u'config', {}), module).from_response(),
    }


def name_pattern(name, module):
    if name is None:
        return

    regex = r"projects/.*/services/.*"

    if not re.match(regex, name):
        name = "projects/{project}/services/{name}".format(**module.params)

    return name


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://serviceusage.googleapis.com/v1/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response)
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['done'])
    wait_done = wait_for_completion(status, op_result, module)
    raise_if_errors(wait_done, ['error'], module)
    return navigate_hash(wait_done, ['response'])


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while not status:
        raise_if_errors(op_result, ['error'], module)
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, False)
        status = navigate_hash(op_result, ['done'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


class ServiceConfig(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {
                u'name': self.request.get('name'),
                u'title': self.request.get('title'),
                u'apis': ServiceApisArray(self.request.get('apis', []), self.module).to_request(),
            }
        )

    def from_response(self):
        return remove_nones_from_dict(
            {
                u'name': self.request.get(u'name'),
                u'title': self.request.get(u'title'),
                u'apis': ServiceApisArray(self.request.get(u'apis', []), self.module).from_response(),
            }
        )


class ServiceApisArray(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = []

    def to_request(self):
        items = []
        for item in self.request:
            items.append(self._request_for_item(item))
        return items

    def from_response(self):
        items = []
        for item in self.request:
            items.append(self._response_from_item(item))
        return items

    def _request_for_item(self, item):
        return remove_nones_from_dict({u'name': item.get('name'), u'version': item.get('version')})

    def _response_from_item(self, item):
        return remove_nones_from_dict({u'name': item.get(u'name'), u'version': item.get(u'version')})


if __name__ == '__main__':
    main()
