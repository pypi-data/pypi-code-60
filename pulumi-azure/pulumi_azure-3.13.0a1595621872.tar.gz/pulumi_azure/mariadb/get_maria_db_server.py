# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetMariaDbServerResult:
    """
    A collection of values returned by getMariaDbServer.
    """
    def __init__(__self__, administrator_login=None, fqdn=None, id=None, location=None, name=None, resource_group_name=None, sku_name=None, ssl_enforcement=None, storage_profiles=None, tags=None, version=None):
        if administrator_login and not isinstance(administrator_login, str):
            raise TypeError("Expected argument 'administrator_login' to be a str")
        __self__.administrator_login = administrator_login
        """
        The Administrator Login for the MariaDB Server.
        """
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        __self__.fqdn = fqdn
        """
        The FQDN of the MariaDB Server.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The Azure location where the resource exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        __self__.sku_name = sku_name
        """
        The SKU Name for this MariaDB Server.
        """
        if ssl_enforcement and not isinstance(ssl_enforcement, str):
            raise TypeError("Expected argument 'ssl_enforcement' to be a str")
        __self__.ssl_enforcement = ssl_enforcement
        """
        The SSL being enforced on connections.
        """
        if storage_profiles and not isinstance(storage_profiles, list):
            raise TypeError("Expected argument 'storage_profiles' to be a list")
        __self__.storage_profiles = storage_profiles
        """
        A `storage_profile` block as defined below.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        ---
        """
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        __self__.version = version
        """
        The version of MariaDB being used.
        """
class AwaitableGetMariaDbServerResult(GetMariaDbServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMariaDbServerResult(
            administrator_login=self.administrator_login,
            fqdn=self.fqdn,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            sku_name=self.sku_name,
            ssl_enforcement=self.ssl_enforcement,
            storage_profiles=self.storage_profiles,
            tags=self.tags,
            version=self.version)

def get_maria_db_server(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing MariaDB Server.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    db_server = azure.mariadb.get_maria_db_server(name="mariadb-server",
        resource_group_name=azurerm_mariadb_server["example"]["resource_group_name"])
    pulumi.export("mariadbServerId", data["azurerm_mariadb_server"]["example"]["id"])
    ```


    :param str name: The name of the MariaDB Server to retrieve information about.
    :param str resource_group_name: The name of the resource group where the MariaDB Server exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:mariadb/getMariaDbServer:getMariaDbServer', __args__, opts=opts).value

    return AwaitableGetMariaDbServerResult(
        administrator_login=__ret__.get('administratorLogin'),
        fqdn=__ret__.get('fqdn'),
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku_name=__ret__.get('skuName'),
        ssl_enforcement=__ret__.get('sslEnforcement'),
        storage_profiles=__ret__.get('storageProfiles'),
        tags=__ret__.get('tags'),
        version=__ret__.get('version'))
