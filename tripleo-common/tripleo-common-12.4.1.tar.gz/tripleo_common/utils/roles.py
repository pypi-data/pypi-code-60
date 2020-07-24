#   Copyright 2017 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging
import os
import shutil
import yaml

import six
from six.moves import cStringIO as StringIO

from tripleo_common import constants
from tripleo_common.exception import NotFound
from tripleo_common.exception import RoleMetadataError
from tripleo_common.utils import stack_parameters as stack_param_utils

LOG = logging.getLogger(__name__)


def get_roles_list_from_directory(directory):
    """Return array of roles in roles path"""
    if not os.path.exists(directory):
        raise ValueError("Invalid roles path specified: {}".format(
            directory))
    roles = []
    for f in os.listdir(directory):
        if f.endswith(".yaml"):
            roles.append(f[:-5])
    roles.sort()
    return roles


def check_role_exists(available_roles, requested_roles):
    """Performs a check on the requested roles to ensure they exist

    :param available_roles list of available role names
    :param requested_roles list of requested role names
    :exception NotFound if a role in the requested list is not available
    """
    unique_roles = list(set([r.split(':')[0] for r in requested_roles]))
    role_check = set(unique_roles) - set(available_roles)
    if len(role_check) > 0:
        msg = "Invalid roles requested: {}\nValid Roles:\n{}".format(
            ','.join(role_check), '\n'.join(available_roles)
        )
        raise NotFound(msg)


def generate_role_with_colon_format(content, defined_role, generated_role):
    """Generate role data with input as Compute:ComputeA

    In Compute:ComputeA, the defined role 'Compute' can be added to
    roles_data.yaml by changing the name to 'ComputeA'. This allows duplicating
    the defined roles so that hardware specific nodes can be targeted with
    specific roles.

    :param content defined role file's content
    :param defined_role defined role's name
    :param generated_role role's name to generate from defined role
    :exception ValueError if generated role name is of invalid format
    """

    # "Compute:Compute" is invalid format
    if generated_role == defined_role:
        msg = ("Generated role name cannot be same as existing role name ({}) "
               "with colon format".format(defined_role))
        raise ValueError(msg)

    # "Compute:A" is invalid format
    if not generated_role.startswith(defined_role):
        msg = ("Generated role name ({}) name should start with existing role "
               "name ({})".format(generated_role, defined_role))
        raise ValueError(msg)

    name_line = "name:%s" % defined_role
    name_line_match = False
    processed = []
    for line in content.split('\n'):
        stripped_line = line.replace(' ', '')
        # Only 'name' need to be replaced in the existing role
        if name_line in stripped_line:
            line = line.replace(defined_role, generated_role)
            name_line_match = True
        processed.append(line)

    if not name_line_match:
        raise ValueError(" error")

    return '\n'.join(processed)


def generate_roles_data_from_directory(directory, roles, validate=True):
    """Generate a roles data file using roles from a local path

    :param directory local filesystem path to the roles
    :param roles ordered list of roles
    :param validate validate the metadata format in the role yaml files
    :returns string contents of the roles_data.yaml
    """
    available_roles = get_roles_list_from_directory(directory)
    check_role_exists(available_roles, roles)
    output = StringIO()

    header = ["#" * 79,
              "# File generated by TripleO",
              "#" * 79,
              ""]
    output.write("\n".join(header))

    for role in roles:
        defined_role = role.split(':')[0]
        file_path = os.path.join(directory, "{}.yaml".format(defined_role))
        if validate:
            validate_role_yaml(role_path=file_path)
        with open(file_path, "r") as f:
            if ':' in role:
                generated_role = role.split(':')[1]
                content = generate_role_with_colon_format(f.read(),
                                                          defined_role,
                                                          generated_role)
                output.write(content)
            else:
                shutil.copyfileobj(f, output)

    return output.getvalue()


def validate_role_yaml(role_data=None, role_path=None):
    """Basic role yaml validation

    :param role_data the role yaml in string form
    :param role_path the path to the yaml file to validate.
    :exception RoleMetadataError
    :returns parsed role yaml object
    """
    if role_data and role_path or (not role_data and not role_path):
        raise ValueError('Either role_data OR role_path must be specified')

    if role_path:
        with open(role_path, 'r') as f:
            role_data = f.read()

    try:
        role = yaml.safe_load(role_data)[0]
    except yaml.YAMLError:
        raise RoleMetadataError('Unable to parse role yaml')

    schema = {
        'name': {'type': six.string_types},
        'CountDefault': {'type': int},
        'HostnameFormatDefault': {'type': six.string_types},
        'disable_constraints': {'type': bool},  # TODO(sbaker) remove in U
        'upgrade_batch_size': {'type': int},
        'ServicesDefault': {'type': list},
        'tags': {'type': list},
        'description': {'type': six.string_types},
        'networks': {'type': [list, dict]},
        'networks_skip_config': {'type': list},
    }

    if 'name' not in role:
        raise RoleMetadataError('Role name is missing from the role')

    # validate numeric metadata is numeric
    for k in schema:
        if k in role:
            if k == 'networks':
                if not (isinstance(role[k], schema[k]['type'][0]) or
                        isinstance(role[k], schema[k]['type'][1])):
                    msg = "Role '{}': {} is not of expected type {}".format(
                        role['name'], k, schema[k]['type'])
                    raise RoleMetadataError(msg)
            else:
                if not isinstance(role[k], schema[k]['type']):
                    msg = "Role '{}': {} is not of expected type {}".format(
                        role['name'], k, schema[k]['type'])
                    raise RoleMetadataError(msg)
    return role


def get_roles_from_plan(swift, heat=None,
                        container=constants.DEFAULT_CONTAINER_NAME,
                        role_file_name=constants.OVERCLOUD_J2_ROLES_NAME,
                        detail=False, valid=False):

    """Returns a deployment plan's roles list

    Parses roles_data.yaml and returns the names of all available/valid roles.

    :param swift: legacy object client
    :param heat: legacy orchestration client
    :param container: name of the Swift container / plan name
    :param roles_file_name: name of the foles file
    :param detail: if false(default), displays role names only.  if true,
                   returns all roles data
    :param valid: check if the role has count > 0 in heat environment
    :return: list of roles in the container's deployment plan
    """

    try:
        roles_data = yaml.safe_load(swift.get_object(
            container, role_file_name)[1])
    except Exception as err:
        err_msg = ("Error retrieving roles data from deployment plan: %s"
                   % err)
        LOG.exception(err_msg)
        raise RuntimeError(err_msg)

    if detail:
        return roles_data

    role_names = [role['name'] for role in roles_data]

    if not valid:
        return role_names

    assert heat is not None

    try:
        heat_resource_tree = stack_param_utils.get_flattened_parameters(
            swift, heat, container)['heat_resource_tree']
    except Exception as err:
        err_msg = ("Error retrieving getting heat resource tree: %s"
                   % err)
        LOG.exception(err_msg)
        raise RuntimeError(err_msg)

    valid_roles = []
    for name in role_names:
        role_count = heat_resource_tree['parameters'].get(
            name + 'Count', {}).get('default', 0)
        if role_count > 0:
            valid_roles.append(name)

    return valid_roles
