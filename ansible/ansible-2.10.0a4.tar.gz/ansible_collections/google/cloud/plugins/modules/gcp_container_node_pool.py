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
module: gcp_container_node_pool
description:
- NodePool contains the name and configuration for a cluster's node pool.
- Node pools are a set of nodes (i.e. VM's), with a common configuration and specification,
  under the control of the cluster master. They may have a set of Kubernetes labels
  applied to them, which may be used to reference them during pod scheduling. They
  may also be resized up or down, to accommodate the workload.
short_description: Creates a GCP NodePool
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
  name:
    description:
    - The name of the node pool.
    required: false
    type: str
  config:
    description:
    - The node configuration of the pool.
    required: false
    type: dict
    suboptions:
      machine_type:
        description:
        - The name of a Google Compute Engine machine type (e.g.
        - n1-standard-1). If unspecified, the default machine type is n1-standard-1.
        required: false
        type: str
      disk_size_gb:
        description:
        - Size of the disk attached to each node, specified in GB. The smallest allowed
          disk size is 10GB. If unspecified, the default disk size is 100GB.
        required: false
        type: int
      oauth_scopes:
        description:
        - The set of Google API scopes to be made available on all of the node VMs
          under the "default" service account.
        - 'The following scopes are recommended, but not required, and by default
          are not included: U(https://www.googleapis.com/auth/compute) is required
          for mounting persistent storage on your nodes.'
        - U(https://www.googleapis.com/auth/devstorage.read_only) is required for
          communicating with gcr.io (the Google Container Registry).
        - If unspecified, no scopes are added, unless Cloud Logging or Cloud Monitoring
          are enabled, in which case their required scopes will be added.
        elements: str
        required: false
        type: list
      service_account:
        description:
        - The Google Cloud Platform Service Account to be used by the node VMs. If
          no Service Account is specified, the "default" service account is used.
        required: false
        type: str
      metadata:
        description:
        - The metadata key/value pairs assigned to instances in the cluster.
        - 'Keys must conform to the regexp [a-zA-Z0-9-_]+ and be less than 128 bytes
          in length. These are reflected as part of a URL in the metadata server.
          Additionally, to avoid ambiguity, keys must not conflict with any other
          metadata keys for the project or be one of the four reserved keys: "instance-template",
          "kube-env", "startup-script", and "user-data" Values are free-form strings,
          and only have meaning as interpreted by the image running in the instance.
          The only restriction placed on them is that each value''s size must be less
          than or equal to 32 KB.'
        - The total size of all keys and values must be less than 512 KB.
        - 'An object containing a list of "key": value pairs.'
        - 'Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'
        required: false
        type: dict
      image_type:
        description:
        - The image type to use for this node. Note that for a given image type, the
          latest version of it will be used.
        required: false
        type: str
      labels:
        description:
        - 'The map of Kubernetes labels (key/value pairs) to be applied to each node.
          These will added in addition to any default label(s) that Kubernetes may
          apply to the node. In case of conflict in label keys, the applied set may
          differ depending on the Kubernetes version -- it''s best to assume the behavior
          is undefined and conflicts should be avoided. For more information, including
          usage and the valid values, see: U(http://kubernetes.io/v1.1/docs/user-guide/labels.html)
          An object containing a list of "key": value pairs.'
        - 'Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'
        required: false
        type: dict
      local_ssd_count:
        description:
        - The number of local SSD disks to be attached to the node.
        - 'The limit for this value is dependant upon the maximum number of disks
          available on a machine per zone. See: U(https://cloud.google.com/compute/docs/disks/local-ssd#local_ssd_limits)
          for more information.'
        required: false
        type: int
      tags:
        description:
        - The list of instance tags applied to all nodes. Tags are used to identify
          valid sources or targets for network firewalls and are specified by the
          client during cluster or node pool creation. Each tag within the list must
          comply with RFC1035.
        elements: str
        required: false
        type: list
      preemptible:
        description:
        - 'Whether the nodes are created as preemptible VM instances. See: U(https://cloud.google.com/compute/docs/instances/preemptible)
          for more information about preemptible VM instances.'
        required: false
        type: bool
      accelerators:
        description:
        - A list of hardware accelerators to be attached to each node.
        elements: dict
        required: false
        type: list
        version_added: '2.9'
        suboptions:
          accelerator_count:
            description:
            - The number of the accelerator cards exposed to an instance.
            required: false
            type: int
          accelerator_type:
            description:
            - The accelerator type resource name.
            required: false
            type: str
      disk_type:
        description:
        - Type of the disk attached to each node (e.g. 'pd-standard' or 'pd-ssd')
          If unspecified, the default disk type is 'pd-standard' .
        required: false
        type: str
        version_added: '2.9'
      min_cpu_platform:
        description:
        - Minimum CPU platform to be used by this instance. The instance may be scheduled
          on the specified or newer CPU platform .
        required: false
        type: str
        version_added: '2.9'
      taints:
        description:
        - List of kubernetes taints to be applied to each node.
        elements: dict
        required: false
        type: list
        version_added: '2.9'
        suboptions:
          key:
            description:
            - Key for taint.
            required: false
            type: str
          value:
            description:
            - Value for taint.
            required: false
            type: str
          effect:
            description:
            - Effect for taint.
            required: false
            type: str
  initial_node_count:
    description:
    - The initial node count for the pool. You must ensure that your Compute Engine
      resource quota is sufficient for this number of instances. You must also have
      available firewall and routes quota.
    required: true
    type: int
  version:
    description:
    - The version of the Kubernetes of this node.
    required: false
    type: str
    version_added: '2.8'
  autoscaling:
    description:
    - Autoscaler configuration for this NodePool. Autoscaler is enabled only if a
      valid configuration is present.
    required: false
    type: dict
    suboptions:
      enabled:
        description:
        - Is autoscaling enabled for this node pool.
        required: false
        type: bool
      min_node_count:
        description:
        - Minimum number of nodes in the NodePool. Must be >= 1 and <= maxNodeCount.
        required: false
        type: int
      max_node_count:
        description:
        - Maximum number of nodes in the NodePool. Must be >= minNodeCount.
        - There has to enough quota to scale up the cluster.
        required: false
        type: int
  management:
    description:
    - Management configuration for this NodePool.
    required: false
    type: dict
    suboptions:
      auto_upgrade:
        description:
        - A flag that specifies whether node auto-upgrade is enabled for the node
          pool. If enabled, node auto-upgrade helps keep the nodes in your node pool
          up to date with the latest release version of Kubernetes.
        required: false
        type: bool
      auto_repair:
        description:
        - A flag that specifies whether the node auto-repair is enabled for the node
          pool. If enabled, the nodes in this node pool will be monitored and, if
          they fail health checks too many times, an automatic repair action will
          be triggered.
        required: false
        type: bool
      upgrade_options:
        description:
        - Specifies the Auto Upgrade knobs for the node pool.
        required: false
        type: dict
        suboptions: {}
  max_pods_constraint:
    description:
    - The constraint on the maximum number of pods that can be run simultaneously
      on a node in the node pool.
    required: false
    type: dict
    version_added: '2.9'
    suboptions:
      max_pods_per_node:
        description:
        - Constraint enforced on the max num of pods per node.
        required: false
        type: int
  conditions:
    description:
    - Which conditions caused the current node pool state.
    elements: dict
    required: false
    type: list
    version_added: '2.9'
    suboptions:
      code:
        description:
        - Machine-friendly representation of the condition.
        - 'Some valid choices include: "UNKNOWN", "GCE_STOCKOUT", "GKE_SERVICE_ACCOUNT_DELETED",
          "GCE_QUOTA_EXCEEDED", "SET_BY_OPERATOR"'
        required: false
        type: str
  cluster:
    description:
    - The cluster this node pool belongs to.
    - 'This field represents a link to a Cluster resource in GCP. It can be specified
      in two ways. First, you can place a dictionary with key ''name'' and value of
      your resource''s name Alternatively, you can add `register: name-of-resource`
      to a gcp_container_cluster task and then set this cluster field to "{{ name-of-resource
      }}"'
    required: true
    type: dict
  location:
    description:
    - The location where the node pool is deployed.
    required: true
    type: str
    aliases:
    - region
    - zone
    version_added: '2.8'
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
'''

EXAMPLES = '''
- name: create a cluster
  google.cloud.gcp_container_cluster:
    name: cluster-nodepool
    initial_node_count: 4
    location: us-central1-a
    project: "{{ gcp_project }}"
    auth_kind: "{{ gcp_cred_kind }}"
    service_account_file: "{{ gcp_cred_file }}"
    state: present
  register: cluster

- name: create a node pool
  google.cloud.gcp_container_node_pool:
    name: my-pool
    initial_node_count: 4
    cluster: "{{ cluster }}"
    location: us-central1-a
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - The name of the node pool.
  returned: success
  type: str
config:
  description:
  - The node configuration of the pool.
  returned: success
  type: complex
  contains:
    machineType:
      description:
      - The name of a Google Compute Engine machine type (e.g.
      - n1-standard-1). If unspecified, the default machine type is n1-standard-1.
      returned: success
      type: str
    diskSizeGb:
      description:
      - Size of the disk attached to each node, specified in GB. The smallest allowed
        disk size is 10GB. If unspecified, the default disk size is 100GB.
      returned: success
      type: int
    oauthScopes:
      description:
      - The set of Google API scopes to be made available on all of the node VMs under
        the "default" service account.
      - 'The following scopes are recommended, but not required, and by default are
        not included: U(https://www.googleapis.com/auth/compute) is required for mounting
        persistent storage on your nodes.'
      - U(https://www.googleapis.com/auth/devstorage.read_only) is required for communicating
        with gcr.io (the Google Container Registry).
      - If unspecified, no scopes are added, unless Cloud Logging or Cloud Monitoring
        are enabled, in which case their required scopes will be added.
      returned: success
      type: list
    serviceAccount:
      description:
      - The Google Cloud Platform Service Account to be used by the node VMs. If no
        Service Account is specified, the "default" service account is used.
      returned: success
      type: str
    metadata:
      description:
      - The metadata key/value pairs assigned to instances in the cluster.
      - 'Keys must conform to the regexp [a-zA-Z0-9-_]+ and be less than 128 bytes
        in length. These are reflected as part of a URL in the metadata server. Additionally,
        to avoid ambiguity, keys must not conflict with any other metadata keys for
        the project or be one of the four reserved keys: "instance-template", "kube-env",
        "startup-script", and "user-data" Values are free-form strings, and only have
        meaning as interpreted by the image running in the instance. The only restriction
        placed on them is that each value''s size must be less than or equal to 32
        KB.'
      - The total size of all keys and values must be less than 512 KB.
      - 'An object containing a list of "key": value pairs.'
      - 'Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'
      returned: success
      type: dict
    imageType:
      description:
      - The image type to use for this node. Note that for a given image type, the
        latest version of it will be used.
      returned: success
      type: str
    labels:
      description:
      - 'The map of Kubernetes labels (key/value pairs) to be applied to each node.
        These will added in addition to any default label(s) that Kubernetes may apply
        to the node. In case of conflict in label keys, the applied set may differ
        depending on the Kubernetes version -- it''s best to assume the behavior is
        undefined and conflicts should be avoided. For more information, including
        usage and the valid values, see: U(http://kubernetes.io/v1.1/docs/user-guide/labels.html)
        An object containing a list of "key": value pairs.'
      - 'Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.'
      returned: success
      type: dict
    localSsdCount:
      description:
      - The number of local SSD disks to be attached to the node.
      - 'The limit for this value is dependant upon the maximum number of disks available
        on a machine per zone. See: U(https://cloud.google.com/compute/docs/disks/local-ssd#local_ssd_limits)
        for more information.'
      returned: success
      type: int
    tags:
      description:
      - The list of instance tags applied to all nodes. Tags are used to identify
        valid sources or targets for network firewalls and are specified by the client
        during cluster or node pool creation. Each tag within the list must comply
        with RFC1035.
      returned: success
      type: list
    preemptible:
      description:
      - 'Whether the nodes are created as preemptible VM instances. See: U(https://cloud.google.com/compute/docs/instances/preemptible)
        for more information about preemptible VM instances.'
      returned: success
      type: bool
    accelerators:
      description:
      - A list of hardware accelerators to be attached to each node.
      returned: success
      type: complex
      contains:
        acceleratorCount:
          description:
          - The number of the accelerator cards exposed to an instance.
          returned: success
          type: int
        acceleratorType:
          description:
          - The accelerator type resource name.
          returned: success
          type: str
    diskType:
      description:
      - Type of the disk attached to each node (e.g. 'pd-standard' or 'pd-ssd') If
        unspecified, the default disk type is 'pd-standard' .
      returned: success
      type: str
    minCpuPlatform:
      description:
      - Minimum CPU platform to be used by this instance. The instance may be scheduled
        on the specified or newer CPU platform .
      returned: success
      type: str
    taints:
      description:
      - List of kubernetes taints to be applied to each node.
      returned: success
      type: complex
      contains:
        key:
          description:
          - Key for taint.
          returned: success
          type: str
        value:
          description:
          - Value for taint.
          returned: success
          type: str
        effect:
          description:
          - Effect for taint.
          returned: success
          type: str
initialNodeCount:
  description:
  - The initial node count for the pool. You must ensure that your Compute Engine
    resource quota is sufficient for this number of instances. You must also have
    available firewall and routes quota.
  returned: success
  type: int
status:
  description:
  - Status of nodes in this pool instance.
  returned: success
  type: str
statusMessage:
  description:
  - Additional information about the current status of this node pool instance.
  returned: success
  type: str
version:
  description:
  - The version of the Kubernetes of this node.
  returned: success
  type: str
autoscaling:
  description:
  - Autoscaler configuration for this NodePool. Autoscaler is enabled only if a valid
    configuration is present.
  returned: success
  type: complex
  contains:
    enabled:
      description:
      - Is autoscaling enabled for this node pool.
      returned: success
      type: bool
    minNodeCount:
      description:
      - Minimum number of nodes in the NodePool. Must be >= 1 and <= maxNodeCount.
      returned: success
      type: int
    maxNodeCount:
      description:
      - Maximum number of nodes in the NodePool. Must be >= minNodeCount.
      - There has to enough quota to scale up the cluster.
      returned: success
      type: int
management:
  description:
  - Management configuration for this NodePool.
  returned: success
  type: complex
  contains:
    autoUpgrade:
      description:
      - A flag that specifies whether node auto-upgrade is enabled for the node pool.
        If enabled, node auto-upgrade helps keep the nodes in your node pool up to
        date with the latest release version of Kubernetes.
      returned: success
      type: bool
    autoRepair:
      description:
      - A flag that specifies whether the node auto-repair is enabled for the node
        pool. If enabled, the nodes in this node pool will be monitored and, if they
        fail health checks too many times, an automatic repair action will be triggered.
      returned: success
      type: bool
    upgradeOptions:
      description:
      - Specifies the Auto Upgrade knobs for the node pool.
      returned: success
      type: complex
      contains:
        autoUpgradeStartTime:
          description:
          - This field is set when upgrades are about to commence with the approximate
            start time for the upgrades, in RFC3339 text format.
          returned: success
          type: str
        description:
          description:
          - This field is set when upgrades are about to commence with the description
            of the upgrade.
          returned: success
          type: str
maxPodsConstraint:
  description:
  - The constraint on the maximum number of pods that can be run simultaneously on
    a node in the node pool.
  returned: success
  type: complex
  contains:
    maxPodsPerNode:
      description:
      - Constraint enforced on the max num of pods per node.
      returned: success
      type: int
conditions:
  description:
  - Which conditions caused the current node pool state.
  returned: success
  type: complex
  contains:
    code:
      description:
      - Machine-friendly representation of the condition.
      returned: success
      type: str
podIpv4CidrSize:
  description:
  - The pod CIDR block size per node in this node pool.
  returned: success
  type: int
cluster:
  description:
  - The cluster this node pool belongs to.
  returned: success
  type: dict
location:
  description:
  - The location where the node pool is deployed.
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
            name=dict(type='str'),
            config=dict(
                type='dict',
                options=dict(
                    machine_type=dict(type='str'),
                    disk_size_gb=dict(type='int'),
                    oauth_scopes=dict(type='list', elements='str'),
                    service_account=dict(type='str'),
                    metadata=dict(type='dict'),
                    image_type=dict(type='str'),
                    labels=dict(type='dict'),
                    local_ssd_count=dict(type='int'),
                    tags=dict(type='list', elements='str'),
                    preemptible=dict(type='bool'),
                    accelerators=dict(type='list', elements='dict', options=dict(accelerator_count=dict(type='int'), accelerator_type=dict(type='str'))),
                    disk_type=dict(type='str'),
                    min_cpu_platform=dict(type='str'),
                    taints=dict(type='list', elements='dict', options=dict(key=dict(type='str'), value=dict(type='str'), effect=dict(type='str'))),
                ),
            ),
            initial_node_count=dict(required=True, type='int'),
            version=dict(type='str'),
            autoscaling=dict(type='dict', options=dict(enabled=dict(type='bool'), min_node_count=dict(type='int'), max_node_count=dict(type='int'))),
            management=dict(
                type='dict', options=dict(auto_upgrade=dict(type='bool'), auto_repair=dict(type='bool'), upgrade_options=dict(type='dict', options=dict()))
            ),
            max_pods_constraint=dict(type='dict', options=dict(max_pods_per_node=dict(type='int'))),
            conditions=dict(type='list', elements='dict', options=dict(code=dict(type='str'))),
            cluster=dict(required=True, type='dict'),
            location=dict(required=True, type='str', aliases=['region', 'zone']),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/cloud-platform']

    state = module.params['state']

    fetch = fetch_resource(module, self_link(module))
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module))
                fetch = fetch_resource(module, self_link(module))
                changed = True
        else:
            delete(module, self_link(module))
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module))
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link):
    auth = GcpSession(module, 'container')
    return wait_for_operation(module, auth.post(link, resource_to_request(module)))


def update(module, link):
    auth = GcpSession(module, 'container')
    return wait_for_operation(module, auth.put(link, resource_to_request(module)))


def delete(module, link):
    auth = GcpSession(module, 'container')
    return wait_for_operation(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'name': module.params.get('name'),
        u'config': NodePoolConfig(module.params.get('config', {}), module).to_request(),
        u'initialNodeCount': module.params.get('initial_node_count'),
        u'version': module.params.get('version'),
        u'autoscaling': NodePoolAutoscaling(module.params.get('autoscaling', {}), module).to_request(),
        u'management': NodePoolManagement(module.params.get('management', {}), module).to_request(),
        u'maxPodsConstraint': NodePoolMaxpodsconstraint(module.params.get('max_pods_constraint', {}), module).to_request(),
        u'conditions': NodePoolConditionsArray(module.params.get('conditions', []), module).to_request(),
    }
    request = encode_request(request, module)
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, allow_not_found=True):
    auth = GcpSession(module, 'container')
    return return_if_object(module, auth.get(link), allow_not_found)


def self_link(module):
    res = {
        'project': module.params['project'],
        'location': module.params['location'],
        'cluster': replace_resource_dict(module.params['cluster'], 'name'),
        'name': module.params['name'],
    }
    return "https://container.googleapis.com/v1/projects/{project}/locations/{location}/clusters/{cluster}/nodePools/{name}".format(**res)


def collection(module):
    res = {'project': module.params['project'], 'location': module.params['location'], 'cluster': replace_resource_dict(module.params['cluster'], 'name')}
    return "https://container.googleapis.com/v1/projects/{project}/locations/{location}/clusters/{cluster}/nodePools".format(**res)


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
        u'config': NodePoolConfig(response.get(u'config', {}), module).from_response(),
        u'initialNodeCount': module.params.get('initial_node_count'),
        u'status': response.get(u'status'),
        u'statusMessage': response.get(u'statusMessage'),
        u'version': module.params.get('version'),
        u'autoscaling': NodePoolAutoscaling(response.get(u'autoscaling', {}), module).from_response(),
        u'management': NodePoolManagement(response.get(u'management', {}), module).from_response(),
        u'maxPodsConstraint': NodePoolMaxpodsconstraint(response.get(u'maxPodsConstraint', {}), module).from_response(),
        u'conditions': NodePoolConditionsArray(response.get(u'conditions', []), module).from_response(),
        u'podIpv4CidrSize': response.get(u'podIpv4CidrSize'),
    }


def async_op_url(module, extra_data=None):
    if extra_data is None:
        extra_data = {}
    url = "https://container.googleapis.com/v1/projects/{project}/locations/{location}/operations/{op_id}"
    combined = extra_data.copy()
    combined.update(module.params)
    return url.format(**combined)


def wait_for_operation(module, response):
    op_result = return_if_object(module, response)
    if op_result is None:
        return {}
    status = navigate_hash(op_result, ['status'])
    wait_done = wait_for_completion(status, op_result, module)
    return fetch_resource(module, navigate_hash(wait_done, ['targetLink']))


def wait_for_completion(status, op_result, module):
    op_id = navigate_hash(op_result, ['name'])
    op_uri = async_op_url(module, {'op_id': op_id})
    while status != 'DONE':
        raise_if_errors(op_result, ['error', 'errors'], module)
        time.sleep(1.0)
        op_result = fetch_resource(module, op_uri, False)
        status = navigate_hash(op_result, ['status'])
    return op_result


def raise_if_errors(response, err_path, module):
    errors = navigate_hash(response, err_path)
    if errors is not None:
        module.fail_json(msg=errors)


# Google Container Engine API has its own layout for the create method,
# defined like this:
#
# {
#   'nodePool': {
#     ... node pool data
#   }
# }
#
# Format the request to match the expected input by the API
def encode_request(resource_request, module):
    return {'nodePool': resource_request}


class NodePoolConfig(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {
                u'machineType': self.request.get('machine_type'),
                u'diskSizeGb': self.request.get('disk_size_gb'),
                u'oauthScopes': self.request.get('oauth_scopes'),
                u'serviceAccount': self.request.get('service_account'),
                u'metadata': self.request.get('metadata'),
                u'imageType': self.request.get('image_type'),
                u'labels': self.request.get('labels'),
                u'localSsdCount': self.request.get('local_ssd_count'),
                u'tags': self.request.get('tags'),
                u'preemptible': self.request.get('preemptible'),
                u'accelerators': NodePoolAcceleratorsArray(self.request.get('accelerators', []), self.module).to_request(),
                u'diskType': self.request.get('disk_type'),
                u'minCpuPlatform': self.request.get('min_cpu_platform'),
                u'taints': NodePoolTaintsArray(self.request.get('taints', []), self.module).to_request(),
            }
        )

    def from_response(self):
        return remove_nones_from_dict(
            {
                u'machineType': self.request.get(u'machineType'),
                u'diskSizeGb': self.request.get(u'diskSizeGb'),
                u'oauthScopes': self.request.get(u'oauthScopes'),
                u'serviceAccount': self.request.get(u'serviceAccount'),
                u'metadata': self.request.get(u'metadata'),
                u'imageType': self.request.get(u'imageType'),
                u'labels': self.request.get(u'labels'),
                u'localSsdCount': self.request.get(u'localSsdCount'),
                u'tags': self.request.get(u'tags'),
                u'preemptible': self.request.get(u'preemptible'),
                u'accelerators': NodePoolAcceleratorsArray(self.request.get(u'accelerators', []), self.module).from_response(),
                u'diskType': self.request.get(u'diskType'),
                u'minCpuPlatform': self.request.get(u'minCpuPlatform'),
                u'taints': NodePoolTaintsArray(self.request.get(u'taints', []), self.module).from_response(),
            }
        )


class NodePoolAcceleratorsArray(object):
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
        return remove_nones_from_dict({u'acceleratorCount': item.get('accelerator_count'), u'acceleratorType': item.get('accelerator_type')})

    def _response_from_item(self, item):
        return remove_nones_from_dict({u'acceleratorCount': item.get(u'acceleratorCount'), u'acceleratorType': item.get(u'acceleratorType')})


class NodePoolTaintsArray(object):
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
        return remove_nones_from_dict({u'key': item.get('key'), u'value': item.get('value'), u'effect': item.get('effect')})

    def _response_from_item(self, item):
        return remove_nones_from_dict({u'key': item.get(u'key'), u'value': item.get(u'value'), u'effect': item.get(u'effect')})


class NodePoolAutoscaling(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {u'enabled': self.request.get('enabled'), u'minNodeCount': self.request.get('min_node_count'), u'maxNodeCount': self.request.get('max_node_count')}
        )

    def from_response(self):
        return remove_nones_from_dict(
            {u'enabled': self.request.get(u'enabled'), u'minNodeCount': self.request.get(u'minNodeCount'), u'maxNodeCount': self.request.get(u'maxNodeCount')}
        )


class NodePoolManagement(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {
                u'autoUpgrade': self.request.get('auto_upgrade'),
                u'autoRepair': self.request.get('auto_repair'),
                u'upgradeOptions': NodePoolUpgradeoptions(self.request.get('upgrade_options', {}), self.module).to_request(),
            }
        )

    def from_response(self):
        return remove_nones_from_dict(
            {
                u'autoUpgrade': self.request.get(u'autoUpgrade'),
                u'autoRepair': self.request.get(u'autoRepair'),
                u'upgradeOptions': NodePoolUpgradeoptions(self.request.get(u'upgradeOptions', {}), self.module).from_response(),
            }
        )


class NodePoolUpgradeoptions(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({})

    def from_response(self):
        return remove_nones_from_dict({})


class NodePoolMaxpodsconstraint(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({u'maxPodsPerNode': self.request.get('max_pods_per_node')})

    def from_response(self):
        return remove_nones_from_dict({u'maxPodsPerNode': self.request.get(u'maxPodsPerNode')})


class NodePoolConditionsArray(object):
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
        return remove_nones_from_dict({u'code': item.get('code')})

    def _response_from_item(self, item):
        return remove_nones_from_dict({u'code': item.get(u'code')})


if __name__ == '__main__':
    main()
