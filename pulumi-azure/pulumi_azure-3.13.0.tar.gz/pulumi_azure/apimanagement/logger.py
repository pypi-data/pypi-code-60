# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Logger(pulumi.CustomResource):
    api_management_name: pulumi.Output[str]
    """
    The name of the API Management Service. Changing this forces a new resource to be created.
    """
    application_insights: pulumi.Output[dict]
    """
    An `application_insights` block as documented below.

      * `instrumentation_key` (`str`) - The instrumentation key used to push data to Application Insights.
    """
    buffered: pulumi.Output[bool]
    """
    Specifies whether records should be buffered in the Logger prior to publishing. Defaults to `true`.
    """
    description: pulumi.Output[str]
    """
    A description of this Logger.
    """
    eventhub: pulumi.Output[dict]
    """
    An `eventhub` block as documented below.

      * `connection_string` (`str`) - The connection string of an EventHub Namespace.
      * `name` (`str`) - The name of an EventHub.
    """
    name: pulumi.Output[str]
    """
    The name of this Logger, which must be unique within the API Management Service. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, api_management_name=None, application_insights=None, buffered=None, description=None, eventhub=None, name=None, resource_group_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Logger within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_insights = azure.appinsights.Insights("exampleInsights",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            application_type="other")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="My Company",
            publisher_email="company@exmaple.com",
            sku_name="Developer_1")
        example_logger = azure.apimanagement.Logger("exampleLogger",
            api_management_name=example_service.name,
            resource_group_name=example_resource_group.name,
            application_insights={
                "instrumentation_key": example_insights.instrumentation_key,
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] application_insights: An `application_insights` block as documented below.
        :param pulumi.Input[bool] buffered: Specifies whether records should be buffered in the Logger prior to publishing. Defaults to `true`.
        :param pulumi.Input[str] description: A description of this Logger.
        :param pulumi.Input[dict] eventhub: An `eventhub` block as documented below.
        :param pulumi.Input[str] name: The name of this Logger, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.

        The **application_insights** object supports the following:

          * `instrumentation_key` (`pulumi.Input[str]`) - The instrumentation key used to push data to Application Insights.

        The **eventhub** object supports the following:

          * `connection_string` (`pulumi.Input[str]`) - The connection string of an EventHub Namespace.
          * `name` (`pulumi.Input[str]`) - The name of an EventHub.
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

            if api_management_name is None:
                raise TypeError("Missing required property 'api_management_name'")
            __props__['api_management_name'] = api_management_name
            __props__['application_insights'] = application_insights
            __props__['buffered'] = buffered
            __props__['description'] = description
            __props__['eventhub'] = eventhub
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
        super(Logger, __self__).__init__(
            'azure:apimanagement/logger:Logger',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_management_name=None, application_insights=None, buffered=None, description=None, eventhub=None, name=None, resource_group_name=None):
        """
        Get an existing Logger resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] application_insights: An `application_insights` block as documented below.
        :param pulumi.Input[bool] buffered: Specifies whether records should be buffered in the Logger prior to publishing. Defaults to `true`.
        :param pulumi.Input[str] description: A description of this Logger.
        :param pulumi.Input[dict] eventhub: An `eventhub` block as documented below.
        :param pulumi.Input[str] name: The name of this Logger, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.

        The **application_insights** object supports the following:

          * `instrumentation_key` (`pulumi.Input[str]`) - The instrumentation key used to push data to Application Insights.

        The **eventhub** object supports the following:

          * `connection_string` (`pulumi.Input[str]`) - The connection string of an EventHub Namespace.
          * `name` (`pulumi.Input[str]`) - The name of an EventHub.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_management_name"] = api_management_name
        __props__["application_insights"] = application_insights
        __props__["buffered"] = buffered
        __props__["description"] = description
        __props__["eventhub"] = eventhub
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        return Logger(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
