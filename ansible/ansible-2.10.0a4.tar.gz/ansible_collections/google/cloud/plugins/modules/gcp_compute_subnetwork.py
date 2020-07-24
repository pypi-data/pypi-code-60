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
module: gcp_compute_subnetwork
description:
- A VPC network is a virtual version of the traditional physical networks that exist
  within and between physical data centers. A VPC network provides connectivity for
  your Compute Engine virtual machine (VM) instances, Container Engine containers,
  App Engine Flex services, and other network-related resources.
- Each GCP project contains one or more VPC networks. Each VPC network is a global
  entity spanning all GCP regions. This global VPC network allows VM instances and
  other resources to communicate with each other via internal, private IP addresses.
- Each VPC network is subdivided into subnets, and each subnet is contained within
  a single region. You can have more than one subnet in a region for a given VPC network.
  Each subnet has a contiguous private RFC1918 IP space. You create instances, containers,
  and the like in these subnets.
- When you create an instance, you must create it in a subnet, and the instance draws
  its internal IP address from that subnet.
- Virtual machine (VM) instances in a VPC network can communicate with instances in
  all other subnets of the same VPC network, regardless of region, using their RFC1918
  private IP addresses. You can isolate portions of the network, even entire subnets,
  using firewall rules.
short_description: Creates a GCP Subnetwork
version_added: '2.6'
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
  description:
    description:
    - An optional description of this resource. Provide this property when you create
      the resource. This field can be set only at resource creation time.
    required: false
    type: str
  ip_cidr_range:
    description:
    - The range of internal addresses that are owned by this subnetwork.
    - Provide this property when you create the subnetwork. For example, 10.0.0.0/8
      or 192.168.0.0/16. Ranges must be unique and non-overlapping within a network.
      Only IPv4 is supported.
    required: true
    type: str
  name:
    description:
    - The name of the resource, provided by the client when initially creating the
      resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically,
      the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`
      which means the first character must be a lowercase letter, and all following
      characters must be a dash, lowercase letter, or digit, except the last character,
      which cannot be a dash.
    required: true
    type: str
  network:
    description:
    - The network this subnet belongs to.
    - Only networks that are in the distributed mode can have subnetworks.
    - 'This field represents a link to a Network resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''selfLink'' and value
      of your resource''s selfLink Alternatively, you can add `register: name-of-resource`
      to a gcp_compute_network task and then set this network field to "{{ name-of-resource
      }}"'
    required: true
    type: dict
  secondary_ip_ranges:
    description:
    - An array of configurations for secondary IP ranges for VM instances contained
      in this subnetwork. The primary IP of such VM must belong to the primary ipCidrRange
      of the subnetwork. The alias IPs may belong to either primary or secondary ranges.
    elements: dict
    required: false
    type: list
    version_added: '2.8'
    suboptions:
      range_name:
        description:
        - The name associated with this subnetwork secondary range, used when adding
          an alias IP range to a VM instance. The name must be 1-63 characters long,
          and comply with RFC1035. The name must be unique within the subnetwork.
        required: true
        type: str
      ip_cidr_range:
        description:
        - The range of IP addresses belonging to this subnetwork secondary range.
          Provide this property when you create the subnetwork.
        - Ranges must be unique and non-overlapping with all primary and secondary
          IP ranges within a network. Only IPv4 is supported.
        required: true
        type: str
  private_ip_google_access:
    description:
    - When enabled, VMs in this subnetwork without external IP addresses can access
      Google APIs and services by using Private Google Access.
    required: false
    type: bool
  region:
    description:
    - The GCP region for this subnetwork.
    required: true
    type: str
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
- 'API Reference: U(https://cloud.google.com/compute/docs/reference/rest/beta/subnetworks)'
- 'Private Google Access: U(https://cloud.google.com/vpc/docs/configure-private-google-access)'
- 'Cloud Networking: U(https://cloud.google.com/vpc/docs/using-vpc)'
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
- name: create a network
  google.cloud.gcp_compute_network:
    name: network-subnetwork
    auto_create_subnetworks: 'true'
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: network

- name: create a subnetwork
  google.cloud.gcp_compute_subnetwork:
    name: ansiblenet
    region: us-west1
    network: "{{ network }}"
    ip_cidr_range: 172.16.0.0/16
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
creationTimestamp:
  description:
  - Creation timestamp in RFC3339 text format.
  returned: success
  type: str
description:
  description:
  - An optional description of this resource. Provide this property when you create
    the resource. This field can be set only at resource creation time.
  returned: success
  type: str
gatewayAddress:
  description:
  - The gateway address for default routes to reach destination addresses outside
    this subnetwork.
  returned: success
  type: str
id:
  description:
  - The unique identifier for the resource.
  returned: success
  type: int
ipCidrRange:
  description:
  - The range of internal addresses that are owned by this subnetwork.
  - Provide this property when you create the subnetwork. For example, 10.0.0.0/8
    or 192.168.0.0/16. Ranges must be unique and non-overlapping within a network.
    Only IPv4 is supported.
  returned: success
  type: str
name:
  description:
  - The name of the resource, provided by the client when initially creating the resource.
    The name must be 1-63 characters long, and comply with RFC1035. Specifically,
    the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`
    which means the first character must be a lowercase letter, and all following
    characters must be a dash, lowercase letter, or digit, except the last character,
    which cannot be a dash.
  returned: success
  type: str
network:
  description:
  - The network this subnet belongs to.
  - Only networks that are in the distributed mode can have subnetworks.
  returned: success
  type: dict
secondaryIpRanges:
  description:
  - An array of configurations for secondary IP ranges for VM instances contained
    in this subnetwork. The primary IP of such VM must belong to the primary ipCidrRange
    of the subnetwork. The alias IPs may belong to either primary or secondary ranges.
  returned: success
  type: complex
  contains:
    rangeName:
      description:
      - The name associated with this subnetwork secondary range, used when adding
        an alias IP range to a VM instance. The name must be 1-63 characters long,
        and comply with RFC1035. The name must be unique within the subnetwork.
      returned: success
      type: str
    ipCidrRange:
      description:
      - The range of IP addresses belonging to this subnetwork secondary range. Provide
        this property when you create the subnetwork.
      - Ranges must be unique and non-overlapping with all primary and secondary IP
        ranges within a network. Only IPv4 is supported.
      returned: success
      type: str
privateIpGoogleAccess:
  description:
  - When enabled, VMs in this subnetwork without external IP addresses can access
    Google APIs and services by using Private Google Access.
  returned: success
  type: bool
region:
  description:
  - The GCP region for this subnetwork.
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
import time

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            description=dict(type='str'),
            ip_cidr_range=dict(required=True, type='str'),
            name=dict(required=True, type='str'),
            network=dict(required=True, type='dict'),
            secondary_ip_ranges=dict(
                type='list', elements='dict', options=dict(range_name=dict(required=True, type='str'), ip_cidr_range=dict(required=True, type='str'))
            ),
            private_ip_google_access=dict(type='bool'),
            region=dict(required=True, type='str'),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/compute']

    state = module.params['state']
    kind = 'compute#subnetwork'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), kind, fetch)
                fetch = fetch_resource(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link, kind, fetch):
    update_fields(module, resource_to_request(module), response_to_hash(module, fetch))
    return fetch_resource(module, self_link(module), kind)


def update_fields(module, request, response):
    if response.get('ipCidrRange') != request.get('ipCidrRange'):
        ip_cidr_range_update(module, request, response)
    if response.get('secondaryIpRanges') != request.get('secondaryIpRanges'):
        secondary_ip_ranges_update(module, request, response)
    if response.get('privateIpGoogleAccess') != request.get('privateIpGoogleAccess'):
        private_ip_google_access_update(module, request, response)


def ip_cidr_range_update(module, request, response):
    auth = GcpSession(module, 'compute')
    auth.post(
        ''.join(["https://www.googleapis.com/compute/v1/", "projects/{project}/regions/{region}/subnetworks/{name}/expandIpCidrRange"]).format(**module.params),
        {u'ipCidrRange': module.params.get('ip_cidr_range')},
    )


def secondary_ip_ranges_update(module, request, response):
    auth = GcpSession(module, 'compute')
    auth.patch(
        ''.join(["https://www.googleapis.com/compute/v1/", "projects/{project}/regions/{region}/subnetworks/{name}"]).format(**module.params),
        {u'secondaryIpRanges': SubnetworkSecondaryiprangesArray(module.params.get('secondary_ip_ranges', []), module).to_request()},
    )


def private_ip_google_access_update(module, request, response):
    auth = GcpSession(module, 'compute')
    auth.post(
        ''.join(["https://www.googleapis.com/compute/v1/", "projects/{project}/regions/{region}/subnetworks/{name}/setPrivateIpGoogleAccess"]).format(
            **module.params
        ),
        {u'privateIpGoogleAccess': module.params.get('private_ip_google_access')},
    )


def delete(module, link, kind):
    auth = GcpSession(module, 'compute')
    return wait_for_operation(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'kind': 'compute#subnetwork',
        u'description': module.params.get('description'),
        u'ipCidrRange': module.params.get('ip_cidr_range'),
        u'name': module.params.get('name'),
        u'network': replace_resource_dict(module.params.get(u'network', {}), 'selfLink'),
        u'secondaryIpRanges': SubnetworkSecondaryiprangesArray(module.params.get('secondary_ip_ranges', []), module).to_request(),
        u'privateIpGoogleAccess': module.params.get('private_ip_google_access'),
        u'region': module.params.get('region'),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind, allow_not_found=True):
    auth = GcpSession(module, 'compute')
    return return_if_object(module, auth.get(link), kind, allow_not_found)


def self_link(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/subnetworks/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/subnetworks".format(**module.params)


def return_if_object(module, response, kind, allow_not_found=False):
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
        u'creationTimestamp': response.get(u'creationTimestamp'),
        u'description': response.get(u'description'),
        u'gatewayAddress': response.get(u'gatewayAddress'),
        u'id': response.get(u'id'),
        u'ipCidrRange': response.get(u'ipCidrRange'),
        u'name': response.get(u'name'),
        u'network': replace_resource_dict(module.params.get(u'network', {}), 'selfLink'),
        u'secondaryIpRanges': SubnetworkSecondaryiprangesArray(response.get(u'secondaryIpRanges', []), module).from_response(),
        u'privateIpGoogleAccess': response.get(u'privateIpGoogleAccess'),
        u'region': module.params.get('region'),
    }


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/operations/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response, 'compute#operation')
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['status'])
    wait_done = wait_for_completion(status, op_result, module)
    return fetch_resource(module, navigate_hash(wait_done, ['targetLink']), 'compute#subnetwork')


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while status != 'DONE':
        raise_if_errors(op_result, ['error', 'errors'], module)
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, 'compute#operation', False)
        status = navigate_hash(op_result, ['status'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


class SubnetworkSecondaryiprangesArray(object):
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
        return remove_nones_from_dict({u'rangeName': item.get('range_name'), u'ipCidrRange': item.get('ip_cidr_range')})

    def _response_from_item(self, item):
        return remove_nones_from_dict({u'rangeName': item.get(u'rangeName'), u'ipCidrRange': item.get(u'ipCidrRange')})


if __name__ == '__main__':
    main()
