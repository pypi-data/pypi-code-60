# (c) 2019, NetApp, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

""" unit tests for Ansible module: na_ontap_security_certificates """

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import json
import pytest

from ansible_collections.netapp.ontap.tests.unit.compat import unittest
from ansible_collections.netapp.ontap.tests.unit.compat.mock import patch, Mock
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
import ansible_collections.netapp.ontap.plugins.module_utils.netapp as netapp_utils

from ansible_collections.netapp.ontap.plugins.modules.na_ontap_security_certificates \
    import NetAppOntapSecurityCertificates as my_module  # module under test


# REST API canned responses when mocking send_request
SRR = {
    # common responses
    'is_rest': (200, {}, None),
    'is_zapi': (400, {}, "Unreachable"),
    'empty_good': ({}, None),
    'end_of_sequence': (None, "Unexpected call to send_request"),
    'generic_error': (None, "Expected error"),
    # module specific responses
    'empty_records': ({'records': []}, None),
    'get_uuid': ({'records': [{'uuid': 'ansible'}]}, None),
}


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)  # pylint: disable=protected-access


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):  # pylint: disable=unused-argument
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):  # pylint: disable=unused-argument
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def set_default_args():
    return dict({
        'hostname': 'hostname',
        'username': 'username',
        'password': 'password',
        'name': 'name_for_certificate'
    })


@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
def test_module_fail_when_required_args_missing(mock_fail):
    ''' required arguments are reported as errors '''
    mock_fail.side_effect = fail_json
    set_module_args({})
    with pytest.raises(AnsibleFailJson) as exc:
        my_module()
    print('Info: %s' % exc.value.args[0]['msg'])


@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_ensure_get_certificate_called(mock_request, mock_fail):
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['get_uuid'],
        SRR['end_of_sequence']
    ]
    set_module_args(set_default_args())
    my_obj = my_module()
    assert my_obj.get_certificate() is not None


@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_error(mock_request, mock_fail):
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['generic_error'],
        SRR['end_of_sequence']
    ]
    set_module_args(set_default_args())
    my_obj = my_module()
    with pytest.raises(AnsibleFailJson) as exc:
        my_obj.apply()
    assert exc.value.args[0]['msg'] == SRR['generic_error'][1]


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_create_failed(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['empty_records'],   # get certificate -> not found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'type': 'client_ca',
        'vserver': 'abc',
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleFailJson) as exc:
        my_obj.apply()
    msg = 'Error creating or installing certificate %s: one or more of the following options are missing' % data['name']
    assert exc.value.args[0]['msg'].startswith(msg)


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_successful_create(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['empty_records'],   # get certificate -> not found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'type': 'client_ca',
        'vserver': 'abc',
        'common_name': 'cname'
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleExitJson) as exc:
        my_obj.apply()
    assert exc.value.args[0]['changed']


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_idempotent_create(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['get_uuid'],    # get certificate -> found
        SRR['end_of_sequence']
    ]
    data = {
        'type': 'client_ca',
        'vserver': 'abc',
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleExitJson) as exc:
        my_obj.apply()
    assert not exc.value.args[0]['changed']


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_successful_delete(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['get_uuid'],    # get certificate -> found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'state': 'absent',
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleExitJson) as exc:
        my_obj.apply()
    assert exc.value.args[0]['changed']


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_idempotent_delete(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['empty_records'],   # get certificate -> not found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'state': 'absent',
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleExitJson) as exc:
        my_obj.apply()
    assert not exc.value.args[0]['changed']


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_successful_sign(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['get_uuid'],    # get certificate -> found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'vserver': 'abc',
        'signing_request': 'CSR'
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleExitJson) as exc:
        my_obj.apply()
    assert exc.value.args[0]['changed']


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_failed_sign_missing_ca(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['empty_records'],   # get certificate -> not found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'vserver': 'abc',
        'signing_request': 'CSR'
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleFailJson) as exc:
        my_obj.apply()
    msg = "signing certificate with name '%s' not found on svm: %s" % (data['name'], data['vserver'])
    assert exc.value.args[0]['msg'] == msg


@patch('ansible.module_utils.basic.AnsibleModule.exit_json')
@patch('ansible.module_utils.basic.AnsibleModule.fail_json')
@patch('ansible_collections.netapp.ontap.plugins.module_utils.netapp.OntapRestAPI.send_request')
def test_rest_failed_sign_absent(mock_request, mock_fail, mock_exit):
    mock_exit.side_effect = exit_json
    mock_fail.side_effect = fail_json
    mock_request.side_effect = [
        SRR['is_rest'],
        SRR['get_uuid'],    # get certificate -> found
        SRR['empty_good'],
        SRR['end_of_sequence']
    ]
    data = {
        'vserver': 'abc',
        'signing_request': 'CSR',
        'state': 'absent'
    }
    data.update(set_default_args())
    set_module_args(data)
    my_obj = my_module()
    with pytest.raises(AnsibleFailJson) as exc:
        my_obj.apply()
    msg = "'signing_request' is not supported with 'state' set to 'absent'"
    assert exc.value.args[0]['msg'] == msg
