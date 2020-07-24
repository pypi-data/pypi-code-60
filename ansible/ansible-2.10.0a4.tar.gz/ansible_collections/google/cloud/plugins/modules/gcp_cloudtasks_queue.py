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
module: gcp_cloudtasks_queue
description:
- A named resource to which messages are sent by publishers.
short_description: Creates a GCP Queue
version_added: '2.9'
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
    - The queue name.
    required: false
    type: str
  app_engine_routing_override:
    description:
    - Overrides for task-level appEngineRouting. These settings apply only to App
      Engine tasks in this queue .
    required: false
    type: dict
    suboptions:
      service:
        description:
        - App service.
        - By default, the task is sent to the service which is the default service
          when the task is attempted.
        required: false
        type: str
      version:
        description:
        - App version.
        - By default, the task is sent to the version which is the default version
          when the task is attempted.
        required: false
        type: str
      instance:
        description:
        - App instance.
        - By default, the task is sent to an instance which is available when the
          task is attempted.
        required: false
        type: str
  rate_limits:
    description:
    - Rate limits for task dispatches.
    - 'The queue''s actual dispatch rate is the result of: * Number of tasks in the
      queue * User-specified throttling: rateLimits, retryConfig, and the queue''s
      state.'
    - "* System throttling due to 429 (Too Many Requests) or 503 (Service Unavailable)
      responses from the worker, high error rates, or to smooth sudden large traffic
      spikes."
    required: false
    type: dict
    suboptions:
      max_dispatches_per_second:
        description:
        - The maximum rate at which tasks are dispatched from this queue.
        - If unspecified when the queue is created, Cloud Tasks will pick the default.
        required: false
        type: str
      max_concurrent_dispatches:
        description:
        - The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched
          for this queue. After this threshold has been reached, Cloud Tasks stops
          dispatching tasks until the number of concurrent requests decreases.
        required: false
        type: int
  retry_config:
    description:
    - Settings that determine the retry behavior.
    required: false
    type: dict
    suboptions:
      max_attempts:
        description:
        - Number of attempts per task.
        - Cloud Tasks will attempt the task maxAttempts times (that is, if the first
          attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1.
        - If unspecified when the queue is created, Cloud Tasks will pick the default.
        - "-1 indicates unlimited attempts."
        required: false
        type: int
      max_retry_duration:
        description:
        - If positive, maxRetryDuration specifies the time limit for retrying a failed
          task, measured from when the task was first attempted. Once maxRetryDuration
          time has passed and the task has been attempted maxAttempts times, no further
          attempts will be made and the task will be deleted.
        - If zero, then the task age is unlimited.
        required: false
        type: str
      min_backoff:
        description:
        - A task will be scheduled for retry between minBackoff and maxBackoff duration
          after it fails, if the queue's RetryConfig specifies that the task should
          be retried.
        required: false
        type: str
      max_backoff:
        description:
        - A task will be scheduled for retry between minBackoff and maxBackoff duration
          after it fails, if the queue's RetryConfig specifies that the task should
          be retried.
        required: false
        type: str
      max_doublings:
        description:
        - The time between retries will double maxDoublings times.
        - A task's retry interval starts at minBackoff, then doubles maxDoublings
          times, then increases linearly, and finally retries retries at intervals
          of maxBackoff up to maxAttempts times.
        required: false
        type: int
  status:
    description:
    - The current state of the queue.
    - 'Some valid choices include: "RUNNING", "PAUSED", "DISABLED"'
    required: false
    type: str
  location:
    description:
    - The location of the queue.
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
'''

EXAMPLES = '''
- name: create a queue
  google.cloud.gcp_cloudtasks_queue:
    name: test_object
    location: us-central1
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - The queue name.
  returned: success
  type: str
appEngineRoutingOverride:
  description:
  - Overrides for task-level appEngineRouting. These settings apply only to App Engine
    tasks in this queue .
  returned: success
  type: complex
  contains:
    service:
      description:
      - App service.
      - By default, the task is sent to the service which is the default service when
        the task is attempted.
      returned: success
      type: str
    version:
      description:
      - App version.
      - By default, the task is sent to the version which is the default version when
        the task is attempted.
      returned: success
      type: str
    instance:
      description:
      - App instance.
      - By default, the task is sent to an instance which is available when the task
        is attempted.
      returned: success
      type: str
    host:
      description:
      - The host that the task is sent to.
      returned: success
      type: str
rateLimits:
  description:
  - Rate limits for task dispatches.
  - 'The queue''s actual dispatch rate is the result of: * Number of tasks in the
    queue * User-specified throttling: rateLimits, retryConfig, and the queue''s state.'
  - "* System throttling due to 429 (Too Many Requests) or 503 (Service Unavailable)
    responses from the worker, high error rates, or to smooth sudden large traffic
    spikes."
  returned: success
  type: complex
  contains:
    maxDispatchesPerSecond:
      description:
      - The maximum rate at which tasks are dispatched from this queue.
      - If unspecified when the queue is created, Cloud Tasks will pick the default.
      returned: success
      type: str
    maxConcurrentDispatches:
      description:
      - The maximum number of concurrent tasks that Cloud Tasks allows to be dispatched
        for this queue. After this threshold has been reached, Cloud Tasks stops dispatching
        tasks until the number of concurrent requests decreases.
      returned: success
      type: int
    maxBurstSize:
      description:
      - The max burst size.
      - Max burst size limits how fast tasks in queue are processed when many tasks
        are in the queue and the rate is high. This field allows the queue to have
        a high rate so processing starts shortly after a task is enqueued, but still
        limits resource usage when many tasks are enqueued in a short period of time.
      returned: success
      type: int
retryConfig:
  description:
  - Settings that determine the retry behavior.
  returned: success
  type: complex
  contains:
    maxAttempts:
      description:
      - Number of attempts per task.
      - Cloud Tasks will attempt the task maxAttempts times (that is, if the first
        attempt fails, then there will be maxAttempts - 1 retries). Must be >= -1.
      - If unspecified when the queue is created, Cloud Tasks will pick the default.
      - "-1 indicates unlimited attempts."
      returned: success
      type: int
    maxRetryDuration:
      description:
      - If positive, maxRetryDuration specifies the time limit for retrying a failed
        task, measured from when the task was first attempted. Once maxRetryDuration
        time has passed and the task has been attempted maxAttempts times, no further
        attempts will be made and the task will be deleted.
      - If zero, then the task age is unlimited.
      returned: success
      type: str
    minBackoff:
      description:
      - A task will be scheduled for retry between minBackoff and maxBackoff duration
        after it fails, if the queue's RetryConfig specifies that the task should
        be retried.
      returned: success
      type: str
    maxBackoff:
      description:
      - A task will be scheduled for retry between minBackoff and maxBackoff duration
        after it fails, if the queue's RetryConfig specifies that the task should
        be retried.
      returned: success
      type: str
    maxDoublings:
      description:
      - The time between retries will double maxDoublings times.
      - A task's retry interval starts at minBackoff, then doubles maxDoublings times,
        then increases linearly, and finally retries retries at intervals of maxBackoff
        up to maxAttempts times.
      returned: success
      type: int
    purgeTime:
      description:
      - The last time this queue was purged.
      returned: success
      type: str
status:
  description:
  - The current state of the queue.
  returned: success
  type: str
location:
  description:
  - The location of the queue.
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

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(type='str'),
            app_engine_routing_override=dict(type='dict', options=dict(service=dict(type='str'), version=dict(type='str'), instance=dict(type='str'))),
            rate_limits=dict(type='dict', options=dict(max_dispatches_per_second=dict(type='str'), max_concurrent_dispatches=dict(type='int'))),
            retry_config=dict(
                type='dict',
                options=dict(
                    max_attempts=dict(type='int'),
                    max_retry_duration=dict(type='str'),
                    min_backoff=dict(type='str'),
                    max_backoff=dict(type='str'),
                    max_doublings=dict(type='int'),
                ),
            ),
            status=dict(type='str'),
            location=dict(required=True, type='str'),
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
                update(module, self_link(module), fetch)
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

    if fetch:
        instance = QueueStatus(module, fetch.get('state'))
        instance.run()
        if module.params.get('status'):
            fetch.update({'status': module.params['status']})
    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link):
    auth = GcpSession(module, 'cloudtasks')
    return return_if_object(module, auth.post(link, resource_to_request(module)))


def update(module, link, fetch):
    auth = GcpSession(module, 'cloudtasks')
    params = {'updateMask': updateMask(resource_to_request(module), response_to_hash(module, fetch))}
    request = resource_to_request(module)
    del request['name']
    return return_if_object(module, auth.patch(link, request, params=params))


def updateMask(request, response):
    update_mask = []
    if request.get('appEngineRoutingOverride') != response.get('appEngineRoutingOverride'):
        update_mask.append('appEngineRoutingOverride')
    if request.get('rateLimits') != response.get('rateLimits'):
        update_mask.append('rateLimits')
    if request.get('retryConfig') != response.get('retryConfig'):
        update_mask.append('retryConfig')
    if request.get('status') != response.get('status'):
        update_mask.append('status')
    return ','.join(update_mask)


def delete(module, link):
    auth = GcpSession(module, 'cloudtasks')
    return return_if_object(module, auth.delete(link))


def resource_to_request(module):
    request = {
        u'location': module.params.get('location'),
        u'name': name_pattern(module.params.get('name'), module),
        u'appEngineRoutingOverride': QueueAppengineroutingoverride(module.params.get('app_engine_routing_override', {}), module).to_request(),
        u'rateLimits': QueueRatelimits(module.params.get('rate_limits', {}), module).to_request(),
        u'retryConfig': QueueRetryconfig(module.params.get('retry_config', {}), module).to_request(),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, allow_not_found=True):
    auth = GcpSession(module, 'cloudtasks')
    return return_if_object(module, auth.get(link), allow_not_found)


def self_link(module):
    return "https://cloudtasks.googleapis.com/v2/projects/{project}/locations/{location}/queues/{name}".format(**module.params)


def collection(module):
    return "https://cloudtasks.googleapis.com/v2/projects/{project}/locations/{location}/queues".format(**module.params)


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
        u'name': name_pattern(module.params.get('name'), module),
        u'appEngineRoutingOverride': QueueAppengineroutingoverride(response.get(u'appEngineRoutingOverride', {}), module).from_response(),
        u'rateLimits': QueueRatelimits(response.get(u'rateLimits', {}), module).from_response(),
        u'retryConfig': QueueRetryconfig(response.get(u'retryConfig', {}), module).from_response(),
    }


def name_pattern(name, module):
    if name is None:
        return

    regex = r"projects/.*/locations/.*/queues/.*"

    if not re.match(regex, name):
        name = "projects/{project}/locations/{location}/queues/{name}".format(**module.params)

    return name


class QueueStatus(object):
    def __init__(self, module, current_status):
        self.module = module
        self.current_status = current_status
        self.desired_status = self.module.params.get('status')

    def run(self):
        # GcpRequest handles unicode text handling
        if GcpRequest({'status': self.current_status}) == GcpRequest({'status': self.desired_status}):
            return
        elif self.desired_status == 'PAUSED':
            self.stop()
        elif self.desired_status == 'RUNNING':
            self.start()

    def start(self):
        auth = GcpSession(self.module, 'cloudtasks')
        return_if_object(self.module, auth.post(self._start_url()))

    def stop(self):
        auth = GcpSession(self.module, 'cloudtasks')
        return_if_object(self.module, auth.post(self._stop_url()))

    def _start_url(self):
        return "https://cloudtasks.googleapis.com/v2/projects/{project}/locations/{location}/queues/{name}:resume".format(**self.module.params)

    def _stop_url(self):
        return "https://cloudtasks.googleapis.com/v2/projects/{project}/locations/{location}/queues/{name}:pause".format(**self.module.params)


class QueueAppengineroutingoverride(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {u'service': self.request.get('service'), u'version': self.request.get('version'), u'instance': self.request.get('instance')}
        )

    def from_response(self):
        return remove_nones_from_dict(
            {u'service': self.request.get(u'service'), u'version': self.request.get(u'version'), u'instance': self.request.get(u'instance')}
        )


class QueueRatelimits(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {
                u'maxDispatchesPerSecond': self.request.get('max_dispatches_per_second'),
                u'maxConcurrentDispatches': self.request.get('max_concurrent_dispatches'),
            }
        )

    def from_response(self):
        return remove_nones_from_dict(
            {u'maxDispatchesPerSecond': self.request.get(u'maxDispatchesPerSecond'), u'maxConcurrentDispatches': self.request.get(u'maxConcurrentDispatches')}
        )


class QueueRetryconfig(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {
                u'maxAttempts': self.request.get('max_attempts'),
                u'maxRetryDuration': self.request.get('max_retry_duration'),
                u'minBackoff': self.request.get('min_backoff'),
                u'maxBackoff': self.request.get('max_backoff'),
                u'maxDoublings': self.request.get('max_doublings'),
            }
        )

    def from_response(self):
        return remove_nones_from_dict(
            {
                u'maxAttempts': self.request.get(u'maxAttempts'),
                u'maxRetryDuration': self.request.get(u'maxRetryDuration'),
                u'minBackoff': self.request.get(u'minBackoff'),
                u'maxBackoff': self.request.get(u'maxBackoff'),
                u'maxDoublings': self.request.get(u'maxDoublings'),
            }
        )


if __name__ == '__main__':
    main()
