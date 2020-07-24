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
module: gcp_bigquery_dataset
description:
- Datasets allow you to organize and control access to your tables.
short_description: Creates a GCP Dataset
version_added: '2.8'
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
    - Dataset name.
    required: false
    type: str
  access:
    description:
    - An array of objects that define dataset access for one or more entities.
    elements: dict
    required: false
    type: list
    suboptions:
      domain:
        description:
        - A domain to grant access to. Any users signed in with the domain specified
          will be granted the specified access .
        required: false
        type: str
      group_by_email:
        description:
        - An email address of a Google Group to grant access to.
        required: false
        type: str
      role:
        description:
        - Describes the rights granted to the user specified by the other member of
          the access object. Primitive, Predefined and custom roles are supported.
          Predefined roles that have equivalent primitive roles are swapped by the
          API to their Primitive counterparts. See [official docs](U(https://cloud.google.com/bigquery/docs/access-control)).
        required: false
        type: str
      special_group:
        description:
        - 'A special group to grant access to. Possible values include: * `projectOwners`:
          Owners of the enclosing project.'
        - "* `projectReaders`: Readers of the enclosing project."
        - "* `projectWriters`: Writers of the enclosing project."
        - "* `allAuthenticatedUsers`: All authenticated BigQuery users. ."
        required: false
        type: str
      user_by_email:
        description:
        - 'An email address of a user to grant access to. For example: fred@example.com
          .'
        required: false
        type: str
      view:
        description:
        - A view from a different dataset to grant access to. Queries executed against
          that view will have read access to tables in this dataset. The role field
          is not required when this field is set. If that view is updated by any user,
          access to the view needs to be granted again via an update operation.
        required: false
        type: dict
        suboptions:
          dataset_id:
            description:
            - The ID of the dataset containing this table.
            required: true
            type: str
          project_id:
            description:
            - The ID of the project containing this table.
            required: true
            type: str
          table_id:
            description:
            - The ID of the table. The ID must contain only letters (a-z, A-Z), numbers
              (0-9), or underscores. The maximum length is 1,024 characters.
            required: true
            type: str
  dataset_reference:
    description:
    - A reference that identifies the dataset.
    required: true
    type: dict
    suboptions:
      dataset_id:
        description:
        - A unique ID for this dataset, without the project name. The ID must contain
          only letters (a-z, A-Z), numbers (0-9), or underscores. The maximum length
          is 1,024 characters.
        required: true
        type: str
      project_id:
        description:
        - The ID of the project containing this dataset.
        required: false
        type: str
  default_table_expiration_ms:
    description:
    - The default lifetime of all tables in the dataset, in milliseconds.
    - The minimum value is 3600000 milliseconds (one hour).
    - Once this property is set, all newly-created tables in the dataset will have
      an `expirationTime` property set to the creation time plus the value in this
      property, and changing the value will only affect new tables, not existing ones.
      When the `expirationTime` for a given table is reached, that table will be deleted
      automatically.
    - If a table's `expirationTime` is modified or removed before the table expires,
      or if you provide an explicit `expirationTime` when creating a table, that value
      takes precedence over the default expiration time indicated by this property.
    required: false
    type: int
  default_partition_expiration_ms:
    description:
    - The default partition expiration for all partitioned tables in the dataset,
      in milliseconds.
    - Once this property is set, all newly-created partitioned tables in the dataset
      will have an `expirationMs` property in the `timePartitioning` settings set
      to this value, and changing the value will only affect new tables, not existing
      ones. The storage in a partition will have an expiration time of its partition
      time plus this value.
    - 'Setting this property overrides the use of `defaultTableExpirationMs` for partitioned
      tables: only one of `defaultTableExpirationMs` and `defaultPartitionExpirationMs`
      will be used for any new partitioned table. If you provide an explicit `timePartitioning.expirationMs`
      when creating or updating a partitioned table, that value takes precedence over
      the default partition expiration time indicated by this property.'
    required: false
    type: int
    version_added: '2.9'
  description:
    description:
    - A user-friendly description of the dataset.
    required: false
    type: str
  friendly_name:
    description:
    - A descriptive name for the dataset.
    required: false
    type: str
  labels:
    description:
    - The labels associated with this dataset. You can use these to organize and group
      your datasets .
    required: false
    type: dict
  location:
    description:
    - The geographic location where the dataset should reside.
    - See [official docs](U(https://cloud.google.com/bigquery/docs/dataset-locations)).
    - There are two types of locations, regional or multi-regional. A regional location
      is a specific geographic place, such as Tokyo, and a multi-regional location
      is a large geographic area, such as the United States, that contains at least
      two geographic places.
    - 'Possible regional values include: `asia-east1`, `asia-northeast1`, `asia-southeast1`,
      `australia-southeast1`, `europe-north1`, `europe-west2` and `us-east4`.'
    - 'Possible multi-regional values: `EU` and `US`.'
    - The default value is multi-regional location `US`.
    - Changing this forces a new resource to be created.
    required: false
    default: US
    type: str
  default_encryption_configuration:
    description:
    - The default encryption key for all tables in the dataset. Once this property
      is set, all newly-created partitioned tables in the dataset will have encryption
      key set to this value, unless table creation request (or query) overrides the
      key.
    required: false
    type: dict
    version_added: '2.10'
    suboptions:
      kms_key_name:
        description:
        - Describes the Cloud KMS encryption key that will be used to protect destination
          BigQuery table. The BigQuery Service Account associated with your project
          requires access to this encryption key.
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
- 'API Reference: U(https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets)'
- 'Datasets Intro: U(https://cloud.google.com/bigquery/docs/datasets-intro)'
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
- name: create a dataset
  google.cloud.gcp_bigquery_dataset:
    name: my_example_dataset
    dataset_reference:
      dataset_id: my_example_dataset
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - Dataset name.
  returned: success
  type: str
access:
  description:
  - An array of objects that define dataset access for one or more entities.
  returned: success
  type: complex
  contains:
    domain:
      description:
      - A domain to grant access to. Any users signed in with the domain specified
        will be granted the specified access .
      returned: success
      type: str
    groupByEmail:
      description:
      - An email address of a Google Group to grant access to.
      returned: success
      type: str
    role:
      description:
      - Describes the rights granted to the user specified by the other member of
        the access object. Primitive, Predefined and custom roles are supported. Predefined
        roles that have equivalent primitive roles are swapped by the API to their
        Primitive counterparts. See [official docs](U(https://cloud.google.com/bigquery/docs/access-control)).
      returned: success
      type: str
    specialGroup:
      description:
      - 'A special group to grant access to. Possible values include: * `projectOwners`:
        Owners of the enclosing project.'
      - "* `projectReaders`: Readers of the enclosing project."
      - "* `projectWriters`: Writers of the enclosing project."
      - "* `allAuthenticatedUsers`: All authenticated BigQuery users. ."
      returned: success
      type: str
    userByEmail:
      description:
      - 'An email address of a user to grant access to. For example: fred@example.com
        .'
      returned: success
      type: str
    view:
      description:
      - A view from a different dataset to grant access to. Queries executed against
        that view will have read access to tables in this dataset. The role field
        is not required when this field is set. If that view is updated by any user,
        access to the view needs to be granted again via an update operation.
      returned: success
      type: complex
      contains:
        datasetId:
          description:
          - The ID of the dataset containing this table.
          returned: success
          type: str
        projectId:
          description:
          - The ID of the project containing this table.
          returned: success
          type: str
        tableId:
          description:
          - The ID of the table. The ID must contain only letters (a-z, A-Z), numbers
            (0-9), or underscores. The maximum length is 1,024 characters.
          returned: success
          type: str
creationTime:
  description:
  - The time when this dataset was created, in milliseconds since the epoch.
  returned: success
  type: int
datasetReference:
  description:
  - A reference that identifies the dataset.
  returned: success
  type: complex
  contains:
    datasetId:
      description:
      - A unique ID for this dataset, without the project name. The ID must contain
        only letters (a-z, A-Z), numbers (0-9), or underscores. The maximum length
        is 1,024 characters.
      returned: success
      type: str
    projectId:
      description:
      - The ID of the project containing this dataset.
      returned: success
      type: str
defaultTableExpirationMs:
  description:
  - The default lifetime of all tables in the dataset, in milliseconds.
  - The minimum value is 3600000 milliseconds (one hour).
  - Once this property is set, all newly-created tables in the dataset will have an
    `expirationTime` property set to the creation time plus the value in this property,
    and changing the value will only affect new tables, not existing ones. When the
    `expirationTime` for a given table is reached, that table will be deleted automatically.
  - If a table's `expirationTime` is modified or removed before the table expires,
    or if you provide an explicit `expirationTime` when creating a table, that value
    takes precedence over the default expiration time indicated by this property.
  returned: success
  type: int
defaultPartitionExpirationMs:
  description:
  - The default partition expiration for all partitioned tables in the dataset, in
    milliseconds.
  - Once this property is set, all newly-created partitioned tables in the dataset
    will have an `expirationMs` property in the `timePartitioning` settings set to
    this value, and changing the value will only affect new tables, not existing ones.
    The storage in a partition will have an expiration time of its partition time
    plus this value.
  - 'Setting this property overrides the use of `defaultTableExpirationMs` for partitioned
    tables: only one of `defaultTableExpirationMs` and `defaultPartitionExpirationMs`
    will be used for any new partitioned table. If you provide an explicit `timePartitioning.expirationMs`
    when creating or updating a partitioned table, that value takes precedence over
    the default partition expiration time indicated by this property.'
  returned: success
  type: int
description:
  description:
  - A user-friendly description of the dataset.
  returned: success
  type: str
etag:
  description:
  - A hash of the resource.
  returned: success
  type: str
friendlyName:
  description:
  - A descriptive name for the dataset.
  returned: success
  type: str
id:
  description:
  - The fully-qualified unique name of the dataset in the format projectId:datasetId.
    The dataset name without the project name is given in the datasetId field .
  returned: success
  type: str
labels:
  description:
  - The labels associated with this dataset. You can use these to organize and group
    your datasets .
  returned: success
  type: dict
lastModifiedTime:
  description:
  - The date when this dataset or any of its tables was last modified, in milliseconds
    since the epoch.
  returned: success
  type: int
location:
  description:
  - The geographic location where the dataset should reside.
  - See [official docs](U(https://cloud.google.com/bigquery/docs/dataset-locations)).
  - There are two types of locations, regional or multi-regional. A regional location
    is a specific geographic place, such as Tokyo, and a multi-regional location is
    a large geographic area, such as the United States, that contains at least two
    geographic places.
  - 'Possible regional values include: `asia-east1`, `asia-northeast1`, `asia-southeast1`,
    `australia-southeast1`, `europe-north1`, `europe-west2` and `us-east4`.'
  - 'Possible multi-regional values: `EU` and `US`.'
  - The default value is multi-regional location `US`.
  - Changing this forces a new resource to be created.
  returned: success
  type: str
defaultEncryptionConfiguration:
  description:
  - The default encryption key for all tables in the dataset. Once this property is
    set, all newly-created partitioned tables in the dataset will have encryption
    key set to this value, unless table creation request (or query) overrides the
    key.
  returned: success
  type: complex
  contains:
    kmsKeyName:
      description:
      - Describes the Cloud KMS encryption key that will be used to protect destination
        BigQuery table. The BigQuery Service Account associated with your project
        requires access to this encryption key.
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

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(type='str'),
            access=dict(
                type='list',
                elements='dict',
                options=dict(
                    domain=dict(type='str'),
                    group_by_email=dict(type='str'),
                    role=dict(type='str'),
                    special_group=dict(type='str'),
                    user_by_email=dict(type='str'),
                    view=dict(
                        type='dict',
                        options=dict(
                            dataset_id=dict(required=True, type='str'), project_id=dict(required=True, type='str'), table_id=dict(required=True, type='str')
                        ),
                    ),
                ),
            ),
            dataset_reference=dict(required=True, type='dict', options=dict(dataset_id=dict(required=True, type='str'), project_id=dict(type='str'))),
            default_table_expiration_ms=dict(type='int'),
            default_partition_expiration_ms=dict(type='int'),
            description=dict(type='str'),
            friendly_name=dict(type='str'),
            labels=dict(type='dict'),
            location=dict(default='US', type='str'),
            default_encryption_configuration=dict(type='dict', options=dict(kms_key_name=dict(required=True, type='str'))),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/bigquery']

    state = module.params['state']
    kind = 'bigquery#dataset'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), kind)
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
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.post(link, resource_to_request(module)), kind)


def update(module, link, kind):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.put(link, resource_to_request(module)), kind)


def delete(module, link, kind):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.delete(link), kind)


def resource_to_request(module):
    request = {
        u'kind': 'bigquery#dataset',
        u'name': module.params.get('name'),
        u'access': DatasetAccessArray(module.params.get('access', []), module).to_request(),
        u'datasetReference': DatasetDatasetreference(module.params.get('dataset_reference', {}), module).to_request(),
        u'defaultTableExpirationMs': module.params.get('default_table_expiration_ms'),
        u'defaultPartitionExpirationMs': module.params.get('default_partition_expiration_ms'),
        u'description': module.params.get('description'),
        u'friendlyName': module.params.get('friendly_name'),
        u'labels': module.params.get('labels'),
        u'location': module.params.get('location'),
        u'defaultEncryptionConfiguration': DatasetDefaultencryptionconfiguration(
            module.params.get('default_encryption_configuration', {}), module
        ).to_request(),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind, allow_not_found=True):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.get(link), kind, allow_not_found)


def self_link(module):
    return "https://www.googleapis.com/bigquery/v2/projects/{project}/datasets/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/bigquery/v2/projects/{project}/datasets".format(**module.params)


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
        u'name': response.get(u'name'),
        u'access': DatasetAccessArray(response.get(u'access', []), module).from_response(),
        u'creationTime': response.get(u'creationTime'),
        u'datasetReference': DatasetDatasetreference(response.get(u'datasetReference', {}), module).from_response(),
        u'defaultTableExpirationMs': response.get(u'defaultTableExpirationMs'),
        u'defaultPartitionExpirationMs': response.get(u'defaultPartitionExpirationMs'),
        u'description': response.get(u'description'),
        u'etag': response.get(u'etag'),
        u'friendlyName': response.get(u'friendlyName'),
        u'id': response.get(u'id'),
        u'labels': response.get(u'labels'),
        u'lastModifiedTime': response.get(u'lastModifiedTime'),
        u'location': response.get(u'location'),
        u'defaultEncryptionConfiguration': DatasetDefaultencryptionconfiguration(response.get(u'defaultEncryptionConfiguration', {}), module).from_response(),
    }


class DatasetAccessArray(object):
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
        return remove_nones_from_dict(
            {
                u'domain': item.get('domain'),
                u'groupByEmail': item.get('group_by_email'),
                u'role': item.get('role'),
                u'specialGroup': item.get('special_group'),
                u'userByEmail': item.get('user_by_email'),
                u'view': DatasetView(item.get('view', {}), self.module).to_request(),
            }
        )

    def _response_from_item(self, item):
        return remove_nones_from_dict(
            {
                u'domain': item.get(u'domain'),
                u'groupByEmail': item.get(u'groupByEmail'),
                u'role': item.get(u'role'),
                u'specialGroup': item.get(u'specialGroup'),
                u'userByEmail': item.get(u'userByEmail'),
                u'view': DatasetView(item.get(u'view', {}), self.module).from_response(),
            }
        )


class DatasetView(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {u'datasetId': self.request.get('dataset_id'), u'projectId': self.request.get('project_id'), u'tableId': self.request.get('table_id')}
        )

    def from_response(self):
        return remove_nones_from_dict(
            {u'datasetId': self.request.get(u'datasetId'), u'projectId': self.request.get(u'projectId'), u'tableId': self.request.get(u'tableId')}
        )


class DatasetDatasetreference(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({u'datasetId': self.request.get('dataset_id'), u'projectId': self.request.get('project_id')})

    def from_response(self):
        return remove_nones_from_dict({u'datasetId': self.request.get(u'datasetId'), u'projectId': self.request.get(u'projectId')})


class DatasetDefaultencryptionconfiguration(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({u'kmsKeyName': self.request.get('kms_key_name')})

    def from_response(self):
        return remove_nones_from_dict({u'kmsKeyName': self.request.get(u'kmsKeyName')})


if __name__ == '__main__':
    main()
