# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class ProtectedVM(pulumi.CustomResource):
    backup_policy_id: pulumi.Output[str]
    """
    Specifies the id of the backup policy to use.
    """
    recovery_vault_name: pulumi.Output[str]
    """
    Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Recovery Services Vault. Changing this forces a new resource to be created.
    """
    source_vm_id: pulumi.Output[str]
    """
    Specifies the ID of the VM to backup. Changing this forces a new resource to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, backup_policy_id=None, recovery_vault_name=None, resource_group_name=None, source_vm_id=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages Azure Backup for an Azure VM

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_vault = azure.recoveryservices.Vault("exampleVault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard")
        example_policy_vm = azure.backup.PolicyVM("examplePolicyVM",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=example_vault.name,
            backup={
                "frequency": "Daily",
                "time": "23:00",
            })
        vm1 = azure.backup.ProtectedVM("vm1",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=example_vault.name,
            source_vm_id=azurerm_virtual_machine["example"]["id"],
            backup_policy_id=example_policy_vm.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: Specifies the id of the backup policy to use.
        :param pulumi.Input[str] recovery_vault_name: Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Recovery Services Vault. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_vm_id: Specifies the ID of the VM to backup. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
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

            if backup_policy_id is None:
                raise TypeError("Missing required property 'backup_policy_id'")
            __props__['backup_policy_id'] = backup_policy_id
            if recovery_vault_name is None:
                raise TypeError("Missing required property 'recovery_vault_name'")
            __props__['recovery_vault_name'] = recovery_vault_name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if source_vm_id is None:
                raise TypeError("Missing required property 'source_vm_id'")
            __props__['source_vm_id'] = source_vm_id
            __props__['tags'] = tags
        super(ProtectedVM, __self__).__init__(
            'azure:backup/protectedVM:ProtectedVM',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, backup_policy_id=None, recovery_vault_name=None, resource_group_name=None, source_vm_id=None, tags=None):
        """
        Get an existing ProtectedVM resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: Specifies the id of the backup policy to use.
        :param pulumi.Input[str] recovery_vault_name: Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Recovery Services Vault. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_vm_id: Specifies the ID of the VM to backup. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["backup_policy_id"] = backup_policy_id
        __props__["recovery_vault_name"] = recovery_vault_name
        __props__["resource_group_name"] = resource_group_name
        __props__["source_vm_id"] = source_vm_id
        __props__["tags"] = tags
        return ProtectedVM(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
