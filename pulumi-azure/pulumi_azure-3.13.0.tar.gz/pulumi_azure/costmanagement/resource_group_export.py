# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class ResourceGroupExport(pulumi.CustomResource):
    active: pulumi.Output[bool]
    """
    Is the cost management export active? Default is `true`.
    """
    delivery_info: pulumi.Output[dict]
    """
    A `delivery_info` block as defined below.

      * `container_name` (`str`) - The name of the container where exports will be uploaded.
      * `rootFolderPath` (`str`) - The path of the directory where exports will be uploaded.
      * `storage_account_id` (`str`) - The storage account id where exports will be delivered.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Cost Management Export. Changing this forces a new resource to be created.
    """
    query: pulumi.Output[dict]
    """
    A `query` block as defined below.

      * `timeFrame` (`str`) - The time frame for pulling data for the query. If custom, then a specific time period must be provided. Possible values include: `WeekToDate`, `MonthToDate`, `YearToDate`, `TheLastWeek`, `TheLastMonth`, `TheLastYear`, `Custom`.
      * `type` (`str`) - The type of the query.
    """
    recurrence_period_end: pulumi.Output[str]
    """
    The date the export will stop capturing information.
    """
    recurrence_period_start: pulumi.Output[str]
    """
    The date the export will start capturing information.
    """
    recurrence_type: pulumi.Output[str]
    """
    How often the requested information will be exported. Valid values include `Annually`, `Daily`, `Monthly`, `Weekly`.
    """
    resource_group_id: pulumi.Output[str]
    """
    The id of the resource group in which to export information.
    """
    def __init__(__self__, resource_name, opts=None, active=None, delivery_info=None, name=None, query=None, recurrence_period_end=None, recurrence_period_start=None, recurrence_type=None, resource_group_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Azure Cost Management Export for a Resource Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="northeurope")
        example_account = azure.storage.Account("exampleAccount",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            account_tier="Standard",
            account_replication_type="LRS")
        example_resource_group_export = azure.costmanagement.ResourceGroupExport("exampleResourceGroupExport",
            resource_group_id=example_resource_group.id,
            recurrence_type="Monthly",
            recurrence_period_start="2020-08-18T00:00:00Z",
            recurrence_period_end="2020-09-18T00:00:00Z",
            delivery_info={
                "storage_account_id": example_account.id,
                "container_name": "examplecontainer",
                "rootFolderPath": "/root/updated",
            },
            query={
                "type": "Usage",
                "timeFrame": "WeekToDate",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] active: Is the cost management export active? Default is `true`.
        :param pulumi.Input[dict] delivery_info: A `delivery_info` block as defined below.
        :param pulumi.Input[str] name: Specifies the name of the Cost Management Export. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] query: A `query` block as defined below.
        :param pulumi.Input[str] recurrence_period_end: The date the export will stop capturing information.
        :param pulumi.Input[str] recurrence_period_start: The date the export will start capturing information.
        :param pulumi.Input[str] recurrence_type: How often the requested information will be exported. Valid values include `Annually`, `Daily`, `Monthly`, `Weekly`.
        :param pulumi.Input[str] resource_group_id: The id of the resource group in which to export information.

        The **delivery_info** object supports the following:

          * `container_name` (`pulumi.Input[str]`) - The name of the container where exports will be uploaded.
          * `rootFolderPath` (`pulumi.Input[str]`) - The path of the directory where exports will be uploaded.
          * `storage_account_id` (`pulumi.Input[str]`) - The storage account id where exports will be delivered.

        The **query** object supports the following:

          * `timeFrame` (`pulumi.Input[str]`) - The time frame for pulling data for the query. If custom, then a specific time period must be provided. Possible values include: `WeekToDate`, `MonthToDate`, `YearToDate`, `TheLastWeek`, `TheLastMonth`, `TheLastYear`, `Custom`.
          * `type` (`pulumi.Input[str]`) - The type of the query.
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

            __props__['active'] = active
            if delivery_info is None:
                raise TypeError("Missing required property 'delivery_info'")
            __props__['delivery_info'] = delivery_info
            __props__['name'] = name
            if query is None:
                raise TypeError("Missing required property 'query'")
            __props__['query'] = query
            if recurrence_period_end is None:
                raise TypeError("Missing required property 'recurrence_period_end'")
            __props__['recurrence_period_end'] = recurrence_period_end
            if recurrence_period_start is None:
                raise TypeError("Missing required property 'recurrence_period_start'")
            __props__['recurrence_period_start'] = recurrence_period_start
            if recurrence_type is None:
                raise TypeError("Missing required property 'recurrence_type'")
            __props__['recurrence_type'] = recurrence_type
            if resource_group_id is None:
                raise TypeError("Missing required property 'resource_group_id'")
            __props__['resource_group_id'] = resource_group_id
        super(ResourceGroupExport, __self__).__init__(
            'azure:costmanagement/resourceGroupExport:ResourceGroupExport',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, active=None, delivery_info=None, name=None, query=None, recurrence_period_end=None, recurrence_period_start=None, recurrence_type=None, resource_group_id=None):
        """
        Get an existing ResourceGroupExport resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] active: Is the cost management export active? Default is `true`.
        :param pulumi.Input[dict] delivery_info: A `delivery_info` block as defined below.
        :param pulumi.Input[str] name: Specifies the name of the Cost Management Export. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] query: A `query` block as defined below.
        :param pulumi.Input[str] recurrence_period_end: The date the export will stop capturing information.
        :param pulumi.Input[str] recurrence_period_start: The date the export will start capturing information.
        :param pulumi.Input[str] recurrence_type: How often the requested information will be exported. Valid values include `Annually`, `Daily`, `Monthly`, `Weekly`.
        :param pulumi.Input[str] resource_group_id: The id of the resource group in which to export information.

        The **delivery_info** object supports the following:

          * `container_name` (`pulumi.Input[str]`) - The name of the container where exports will be uploaded.
          * `rootFolderPath` (`pulumi.Input[str]`) - The path of the directory where exports will be uploaded.
          * `storage_account_id` (`pulumi.Input[str]`) - The storage account id where exports will be delivered.

        The **query** object supports the following:

          * `timeFrame` (`pulumi.Input[str]`) - The time frame for pulling data for the query. If custom, then a specific time period must be provided. Possible values include: `WeekToDate`, `MonthToDate`, `YearToDate`, `TheLastWeek`, `TheLastMonth`, `TheLastYear`, `Custom`.
          * `type` (`pulumi.Input[str]`) - The type of the query.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["active"] = active
        __props__["delivery_info"] = delivery_info
        __props__["name"] = name
        __props__["query"] = query
        __props__["recurrence_period_end"] = recurrence_period_end
        __props__["recurrence_period_start"] = recurrence_period_start
        __props__["recurrence_type"] = recurrence_type
        __props__["resource_group_id"] = resource_group_id
        return ResourceGroupExport(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
