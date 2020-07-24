# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetSharedAccessPolicyResult:
    """
    A collection of values returned by getSharedAccessPolicy.
    """
    def __init__(__self__, id=None, iothub_name=None, name=None, primary_connection_string=None, primary_key=None, resource_group_name=None, secondary_connection_string=None, secondary_key=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if iothub_name and not isinstance(iothub_name, str):
            raise TypeError("Expected argument 'iothub_name' to be a str")
        __self__.iothub_name = iothub_name
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if primary_connection_string and not isinstance(primary_connection_string, str):
            raise TypeError("Expected argument 'primary_connection_string' to be a str")
        __self__.primary_connection_string = primary_connection_string
        """
        The primary connection string of the Shared Access Policy.
        """
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        __self__.primary_key = primary_key
        """
        The primary key used to create the authentication token.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if secondary_connection_string and not isinstance(secondary_connection_string, str):
            raise TypeError("Expected argument 'secondary_connection_string' to be a str")
        __self__.secondary_connection_string = secondary_connection_string
        """
        The secondary connection string of the Shared Access Policy.
        """
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        __self__.secondary_key = secondary_key
        """
        The secondary key used to create the authentication token.
        """
class AwaitableGetSharedAccessPolicyResult(GetSharedAccessPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharedAccessPolicyResult(
            id=self.id,
            iothub_name=self.iothub_name,
            name=self.name,
            primary_connection_string=self.primary_connection_string,
            primary_key=self.primary_key,
            resource_group_name=self.resource_group_name,
            secondary_connection_string=self.secondary_connection_string,
            secondary_key=self.secondary_key)

def get_shared_access_policy(iothub_name=None,name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing IotHub Shared Access Policy

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.iot.get_shared_access_policy(name="example",
        resource_group_name=azurerm_resource_group["example"]["name"],
        iothub_name=azurerm_iothub["example"]["name"])
    ```


    :param str iothub_name: The name of the IoTHub to which this Shared Access Policy belongs.
    :param str name: Specifies the name of the IotHub Shared Access Policy resource.
    :param str resource_group_name: The name of the resource group under which the IotHub Shared Access Policy resource has to be created.
    """
    __args__ = dict()


    __args__['iothubName'] = iothub_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:iot/getSharedAccessPolicy:getSharedAccessPolicy', __args__, opts=opts).value

    return AwaitableGetSharedAccessPolicyResult(
        id=__ret__.get('id'),
        iothub_name=__ret__.get('iothubName'),
        name=__ret__.get('name'),
        primary_connection_string=__ret__.get('primaryConnectionString'),
        primary_key=__ret__.get('primaryKey'),
        resource_group_name=__ret__.get('resourceGroupName'),
        secondary_connection_string=__ret__.get('secondaryConnectionString'),
        secondary_key=__ret__.get('secondaryKey'))
