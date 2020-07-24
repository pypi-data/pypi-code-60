# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Share(pulumi.CustomResource):
    acls: pulumi.Output[list]
    """
    One or more `acl` blocks as defined below.

      * `access_policies` (`list`) - An `access_policy` block as defined below.
        * `expiry` (`str`) - The time at which this Access Policy should be valid until, in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format.
        * `permissions` (`str`) - The permissions which should be associated with this Shared Identifier. Possible value is combination of `d` (delete), `l` (list), `r` (read) and `w` (write).
        * `start` (`str`) - The time at which this Access Policy should be valid from, in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format.

      * `id` (`str`) - The ID which should be used for this Shared Identifier.
    """
    metadata: pulumi.Output[dict]
    """
    A mapping of MetaData for this File Share.
    """
    name: pulumi.Output[str]
    """
    The name of the share. Must be unique within the storage account where the share is located.
    """
    quota: pulumi.Output[float]
    """
    The maximum size of the share, in gigabytes. For Standard storage accounts, this must be greater than 0 and less than 5120 GB (5 TB). For Premium FileStorage storage accounts, this must be greater than 100 GB and less than 102400 GB (100 TB). Default is 5120.
    """
    resource_manager_id: pulumi.Output[str]
    """
    The Resource Manager ID of this File Share.
    """
    storage_account_name: pulumi.Output[str]
    """
    Specifies the storage account in which to create the share.
    Changing this forces a new resource to be created.
    """
    url: pulumi.Output[str]
    """
    The URL of the File Share
    """
    def __init__(__self__, resource_name, opts=None, acls=None, metadata=None, name=None, quota=None, storage_account_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a File Share within Azure Storage.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_share = azure.storage.Share("exampleShare",
            storage_account_name=example_account.name,
            quota=50,
            acls=[{
                "id": "MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTI",
                "access_policies": [{
                    "permissions": "rwdl",
                    "start": "2019-07-02T09:38:21.0000000Z",
                    "expiry": "2019-07-02T10:38:21.0000000Z",
                }],
            }])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] acls: One or more `acl` blocks as defined below.
        :param pulumi.Input[dict] metadata: A mapping of MetaData for this File Share.
        :param pulumi.Input[str] name: The name of the share. Must be unique within the storage account where the share is located.
        :param pulumi.Input[float] quota: The maximum size of the share, in gigabytes. For Standard storage accounts, this must be greater than 0 and less than 5120 GB (5 TB). For Premium FileStorage storage accounts, this must be greater than 100 GB and less than 102400 GB (100 TB). Default is 5120.
        :param pulumi.Input[str] storage_account_name: Specifies the storage account in which to create the share.
               Changing this forces a new resource to be created.

        The **acls** object supports the following:

          * `access_policies` (`pulumi.Input[list]`) - An `access_policy` block as defined below.
            * `expiry` (`pulumi.Input[str]`) - The time at which this Access Policy should be valid until, in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format.
            * `permissions` (`pulumi.Input[str]`) - The permissions which should be associated with this Shared Identifier. Possible value is combination of `d` (delete), `l` (list), `r` (read) and `w` (write).
            * `start` (`pulumi.Input[str]`) - The time at which this Access Policy should be valid from, in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format.

          * `id` (`pulumi.Input[str]`) - The ID which should be used for this Shared Identifier.
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

            __props__['acls'] = acls
            __props__['metadata'] = metadata
            __props__['name'] = name
            __props__['quota'] = quota
            if storage_account_name is None:
                raise TypeError("Missing required property 'storage_account_name'")
            __props__['storage_account_name'] = storage_account_name
            __props__['resource_manager_id'] = None
            __props__['url'] = None
        super(Share, __self__).__init__(
            'azure:storage/share:Share',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, acls=None, metadata=None, name=None, quota=None, resource_manager_id=None, storage_account_name=None, url=None):
        """
        Get an existing Share resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] acls: One or more `acl` blocks as defined below.
        :param pulumi.Input[dict] metadata: A mapping of MetaData for this File Share.
        :param pulumi.Input[str] name: The name of the share. Must be unique within the storage account where the share is located.
        :param pulumi.Input[float] quota: The maximum size of the share, in gigabytes. For Standard storage accounts, this must be greater than 0 and less than 5120 GB (5 TB). For Premium FileStorage storage accounts, this must be greater than 100 GB and less than 102400 GB (100 TB). Default is 5120.
        :param pulumi.Input[str] resource_manager_id: The Resource Manager ID of this File Share.
        :param pulumi.Input[str] storage_account_name: Specifies the storage account in which to create the share.
               Changing this forces a new resource to be created.
        :param pulumi.Input[str] url: The URL of the File Share

        The **acls** object supports the following:

          * `access_policies` (`pulumi.Input[list]`) - An `access_policy` block as defined below.
            * `expiry` (`pulumi.Input[str]`) - The time at which this Access Policy should be valid until, in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format.
            * `permissions` (`pulumi.Input[str]`) - The permissions which should be associated with this Shared Identifier. Possible value is combination of `d` (delete), `l` (list), `r` (read) and `w` (write).
            * `start` (`pulumi.Input[str]`) - The time at which this Access Policy should be valid from, in [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) format.

          * `id` (`pulumi.Input[str]`) - The ID which should be used for this Shared Identifier.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["acls"] = acls
        __props__["metadata"] = metadata
        __props__["name"] = name
        __props__["quota"] = quota
        __props__["resource_manager_id"] = resource_manager_id
        __props__["storage_account_name"] = storage_account_name
        __props__["url"] = url
        return Share(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
