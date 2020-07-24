# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class AccessPolicy(pulumi.CustomResource):
    application_id: pulumi.Output[str]
    """
    The object ID of an Application in Azure Active Directory.
    """
    certificate_permissions: pulumi.Output[list]
    """
    List of certificate permissions, must be one or more from
    the following: `backup`, `create`, `delete`, `deleteissuers`, `get`, `getissuers`, `import`, `list`, `listissuers`,
    `managecontacts`, `manageissuers`, `purge`, `recover`, `restore`, `setissuers` and `update`.
    """
    key_permissions: pulumi.Output[list]
    """
    List of key permissions, must be one or more from
    the following: `backup`, `create`, `decrypt`, `delete`, `encrypt`, `get`, `import`, `list`, `purge`,
    `recover`, `restore`, `sign`, `unwrapKey`, `update`, `verify` and `wrapKey`.
    """
    key_vault_id: pulumi.Output[str]
    """
    Specifies the id of the Key Vault resource. Changing this
    forces a new resource to be created.
    """
    object_id: pulumi.Output[str]
    """
    The object ID of a user, service principal or security
    group in the Azure Active Directory tenant for the vault. The object ID must
    be unique for the list of access policies. Changing this forces a new resource
    to be created.
    """
    secret_permissions: pulumi.Output[list]
    """
    List of secret permissions, must be one or more
    from the following: `backup`, `delete`, `get`, `list`, `purge`, `recover`, `restore` and `set`.
    """
    storage_permissions: pulumi.Output[list]
    """
    List of storage permissions, must be one or more from the following: `backup`, `delete`, `deletesas`, `get`, `getsas`, `list`, `listsas`, `purge`, `recover`, `regeneratekey`, `restore`, `set`, `setsas` and `update`.
    """
    tenant_id: pulumi.Output[str]
    """
    The Azure Active Directory tenant ID that should be used
    for authenticating requests to the key vault. Changing this forces a new resource
    to be created.
    """
    def __init__(__self__, resource_name, opts=None, application_id=None, certificate_permissions=None, key_permissions=None, key_vault_id=None, object_id=None, secret_permissions=None, storage_permissions=None, tenant_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Key Vault Access Policy.

        > **NOTE:** It's possible to define Key Vault Access Policies both within the `keyvault.KeyVault` resource via the `access_policy` block and by using the `keyvault.AccessPolicy` resource. However it's not possible to use both methods to manage Access Policies within a KeyVault, since there'll be conflicts.

        > **NOTE:** Azure permits a maximum of 1024 Access Policies per Key Vault - [more information can be found in this document](https://docs.microsoft.com/en-us/azure/key-vault/key-vault-secure-your-key-vault#data-plane-access-control).

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The object ID of an Application in Azure Active Directory.
        :param pulumi.Input[list] certificate_permissions: List of certificate permissions, must be one or more from
               the following: `backup`, `create`, `delete`, `deleteissuers`, `get`, `getissuers`, `import`, `list`, `listissuers`,
               `managecontacts`, `manageissuers`, `purge`, `recover`, `restore`, `setissuers` and `update`.
        :param pulumi.Input[list] key_permissions: List of key permissions, must be one or more from
               the following: `backup`, `create`, `decrypt`, `delete`, `encrypt`, `get`, `import`, `list`, `purge`,
               `recover`, `restore`, `sign`, `unwrapKey`, `update`, `verify` and `wrapKey`.
        :param pulumi.Input[str] key_vault_id: Specifies the id of the Key Vault resource. Changing this
               forces a new resource to be created.
        :param pulumi.Input[str] object_id: The object ID of a user, service principal or security
               group in the Azure Active Directory tenant for the vault. The object ID must
               be unique for the list of access policies. Changing this forces a new resource
               to be created.
        :param pulumi.Input[list] secret_permissions: List of secret permissions, must be one or more
               from the following: `backup`, `delete`, `get`, `list`, `purge`, `recover`, `restore` and `set`.
        :param pulumi.Input[list] storage_permissions: List of storage permissions, must be one or more from the following: `backup`, `delete`, `deletesas`, `get`, `getsas`, `list`, `listsas`, `purge`, `recover`, `regeneratekey`, `restore`, `set`, `setsas` and `update`.
        :param pulumi.Input[str] tenant_id: The Azure Active Directory tenant ID that should be used
               for authenticating requests to the key vault. Changing this forces a new resource
               to be created.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['application_id'] = application_id
            __props__['certificate_permissions'] = certificate_permissions
            __props__['key_permissions'] = key_permissions
            if key_vault_id is None:
                raise TypeError("Missing required property 'key_vault_id'")
            __props__['key_vault_id'] = key_vault_id
            if object_id is None:
                raise TypeError("Missing required property 'object_id'")
            __props__['object_id'] = object_id
            __props__['secret_permissions'] = secret_permissions
            __props__['storage_permissions'] = storage_permissions
            if tenant_id is None:
                raise TypeError("Missing required property 'tenant_id'")
            __props__['tenant_id'] = tenant_id
        super(AccessPolicy, __self__).__init__(
            'azure:keyvault/accessPolicy:AccessPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, application_id=None, certificate_permissions=None, key_permissions=None, key_vault_id=None, object_id=None, secret_permissions=None, storage_permissions=None, tenant_id=None):
        """
        Get an existing AccessPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The object ID of an Application in Azure Active Directory.
        :param pulumi.Input[list] certificate_permissions: List of certificate permissions, must be one or more from
               the following: `backup`, `create`, `delete`, `deleteissuers`, `get`, `getissuers`, `import`, `list`, `listissuers`,
               `managecontacts`, `manageissuers`, `purge`, `recover`, `restore`, `setissuers` and `update`.
        :param pulumi.Input[list] key_permissions: List of key permissions, must be one or more from
               the following: `backup`, `create`, `decrypt`, `delete`, `encrypt`, `get`, `import`, `list`, `purge`,
               `recover`, `restore`, `sign`, `unwrapKey`, `update`, `verify` and `wrapKey`.
        :param pulumi.Input[str] key_vault_id: Specifies the id of the Key Vault resource. Changing this
               forces a new resource to be created.
        :param pulumi.Input[str] object_id: The object ID of a user, service principal or security
               group in the Azure Active Directory tenant for the vault. The object ID must
               be unique for the list of access policies. Changing this forces a new resource
               to be created.
        :param pulumi.Input[list] secret_permissions: List of secret permissions, must be one or more
               from the following: `backup`, `delete`, `get`, `list`, `purge`, `recover`, `restore` and `set`.
        :param pulumi.Input[list] storage_permissions: List of storage permissions, must be one or more from the following: `backup`, `delete`, `deletesas`, `get`, `getsas`, `list`, `listsas`, `purge`, `recover`, `regeneratekey`, `restore`, `set`, `setsas` and `update`.
        :param pulumi.Input[str] tenant_id: The Azure Active Directory tenant ID that should be used
               for authenticating requests to the key vault. Changing this forces a new resource
               to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["application_id"] = application_id
        __props__["certificate_permissions"] = certificate_permissions
        __props__["key_permissions"] = key_permissions
        __props__["key_vault_id"] = key_vault_id
        __props__["object_id"] = object_id
        __props__["secret_permissions"] = secret_permissions
        __props__["storage_permissions"] = storage_permissions
        __props__["tenant_id"] = tenant_id
        return AccessPolicy(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
