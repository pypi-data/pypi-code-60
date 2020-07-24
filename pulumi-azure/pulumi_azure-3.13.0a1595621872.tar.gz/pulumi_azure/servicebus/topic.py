# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Topic(pulumi.CustomResource):
    auto_delete_on_idle: pulumi.Output[str]
    """
    The ISO 8601 timespan duration of the idle interval after which the
    Topic is automatically deleted, minimum of 5 minutes.
    """
    default_message_ttl: pulumi.Output[str]
    """
    The ISO 8601 timespan duration of TTL of messages sent to this topic if no
    TTL value is set on the message itself.
    """
    duplicate_detection_history_time_window: pulumi.Output[str]
    """
    The ISO 8601 timespan duration during which
    duplicates can be detected. Defaults to 10 minutes. (`PT10M`)
    """
    enable_batched_operations: pulumi.Output[bool]
    """
    Boolean flag which controls if server-side
    batched operations are enabled. Defaults to false.
    """
    enable_express: pulumi.Output[bool]
    """
    Boolean flag which controls whether Express Entities
    are enabled. An express topic holds a message in memory temporarily before writing
    it to persistent storage. Defaults to false.
    """
    enable_partitioning: pulumi.Output[bool]
    """
    Boolean flag which controls whether to enable
    the topic to be partitioned across multiple message brokers. Defaults to false.
    Changing this forces a new resource to be created.
    """
    max_size_in_megabytes: pulumi.Output[float]
    """
    Integer value which controls the size of
    memory allocated for the topic. For supported values see the "Queue/topic size"
    section of [this document](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the ServiceBus Topic resource. Changing this forces a
    new resource to be created.
    """
    namespace_name: pulumi.Output[str]
    """
    The name of the ServiceBus Namespace to create
    this topic in. Changing this forces a new resource to be created.
    """
    requires_duplicate_detection: pulumi.Output[bool]
    """
    Boolean flag which controls whether
    the Topic requires duplicate detection. Defaults to false. Changing this forces
    a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to
    create the namespace. Changing this forces a new resource to be created.
    """
    status: pulumi.Output[str]
    """
    The Status of the Service Bus Topic. Acceptable values are `Active` or `Disabled`. Defaults to `Active`.
    """
    support_ordering: pulumi.Output[bool]
    """
    Boolean flag which controls whether the Topic
    supports ordering. Defaults to false.
    """
    def __init__(__self__, resource_name, opts=None, auto_delete_on_idle=None, default_message_ttl=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_express=None, enable_partitioning=None, max_size_in_megabytes=None, name=None, namespace_name=None, requires_duplicate_detection=None, resource_group_name=None, status=None, support_ordering=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a ServiceBus Topic.

        **Note** Topics can only be created in Namespaces with an SKU of `standard` or higher.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_namespace = azure.servicebus.Namespace("exampleNamespace",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard",
            tags={
                "source": "example",
            })
        example_topic = azure.servicebus.Topic("exampleTopic",
            resource_group_name=example_resource_group.name,
            namespace_name=example_namespace.name,
            enable_partitioning=True)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_delete_on_idle: The ISO 8601 timespan duration of the idle interval after which the
               Topic is automatically deleted, minimum of 5 minutes.
        :param pulumi.Input[str] default_message_ttl: The ISO 8601 timespan duration of TTL of messages sent to this topic if no
               TTL value is set on the message itself.
        :param pulumi.Input[str] duplicate_detection_history_time_window: The ISO 8601 timespan duration during which
               duplicates can be detected. Defaults to 10 minutes. (`PT10M`)
        :param pulumi.Input[bool] enable_batched_operations: Boolean flag which controls if server-side
               batched operations are enabled. Defaults to false.
        :param pulumi.Input[bool] enable_express: Boolean flag which controls whether Express Entities
               are enabled. An express topic holds a message in memory temporarily before writing
               it to persistent storage. Defaults to false.
        :param pulumi.Input[bool] enable_partitioning: Boolean flag which controls whether to enable
               the topic to be partitioned across multiple message brokers. Defaults to false.
               Changing this forces a new resource to be created.
        :param pulumi.Input[float] max_size_in_megabytes: Integer value which controls the size of
               memory allocated for the topic. For supported values see the "Queue/topic size"
               section of [this document](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Topic resource. Changing this forces a
               new resource to be created.
        :param pulumi.Input[str] namespace_name: The name of the ServiceBus Namespace to create
               this topic in. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] requires_duplicate_detection: Boolean flag which controls whether
               the Topic requires duplicate detection. Defaults to false. Changing this forces
               a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to
               create the namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] status: The Status of the Service Bus Topic. Acceptable values are `Active` or `Disabled`. Defaults to `Active`.
        :param pulumi.Input[bool] support_ordering: Boolean flag which controls whether the Topic
               supports ordering. Defaults to false.
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

            __props__['auto_delete_on_idle'] = auto_delete_on_idle
            __props__['default_message_ttl'] = default_message_ttl
            __props__['duplicate_detection_history_time_window'] = duplicate_detection_history_time_window
            __props__['enable_batched_operations'] = enable_batched_operations
            __props__['enable_express'] = enable_express
            __props__['enable_partitioning'] = enable_partitioning
            __props__['max_size_in_megabytes'] = max_size_in_megabytes
            __props__['name'] = name
            if namespace_name is None:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            __props__['requires_duplicate_detection'] = requires_duplicate_detection
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['status'] = status
            __props__['support_ordering'] = support_ordering
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure:eventhub/topic:Topic")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Topic, __self__).__init__(
            'azure:servicebus/topic:Topic',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, auto_delete_on_idle=None, default_message_ttl=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_express=None, enable_partitioning=None, max_size_in_megabytes=None, name=None, namespace_name=None, requires_duplicate_detection=None, resource_group_name=None, status=None, support_ordering=None):
        """
        Get an existing Topic resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_delete_on_idle: The ISO 8601 timespan duration of the idle interval after which the
               Topic is automatically deleted, minimum of 5 minutes.
        :param pulumi.Input[str] default_message_ttl: The ISO 8601 timespan duration of TTL of messages sent to this topic if no
               TTL value is set on the message itself.
        :param pulumi.Input[str] duplicate_detection_history_time_window: The ISO 8601 timespan duration during which
               duplicates can be detected. Defaults to 10 minutes. (`PT10M`)
        :param pulumi.Input[bool] enable_batched_operations: Boolean flag which controls if server-side
               batched operations are enabled. Defaults to false.
        :param pulumi.Input[bool] enable_express: Boolean flag which controls whether Express Entities
               are enabled. An express topic holds a message in memory temporarily before writing
               it to persistent storage. Defaults to false.
        :param pulumi.Input[bool] enable_partitioning: Boolean flag which controls whether to enable
               the topic to be partitioned across multiple message brokers. Defaults to false.
               Changing this forces a new resource to be created.
        :param pulumi.Input[float] max_size_in_megabytes: Integer value which controls the size of
               memory allocated for the topic. For supported values see the "Queue/topic size"
               section of [this document](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Topic resource. Changing this forces a
               new resource to be created.
        :param pulumi.Input[str] namespace_name: The name of the ServiceBus Namespace to create
               this topic in. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] requires_duplicate_detection: Boolean flag which controls whether
               the Topic requires duplicate detection. Defaults to false. Changing this forces
               a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to
               create the namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] status: The Status of the Service Bus Topic. Acceptable values are `Active` or `Disabled`. Defaults to `Active`.
        :param pulumi.Input[bool] support_ordering: Boolean flag which controls whether the Topic
               supports ordering. Defaults to false.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["auto_delete_on_idle"] = auto_delete_on_idle
        __props__["default_message_ttl"] = default_message_ttl
        __props__["duplicate_detection_history_time_window"] = duplicate_detection_history_time_window
        __props__["enable_batched_operations"] = enable_batched_operations
        __props__["enable_express"] = enable_express
        __props__["enable_partitioning"] = enable_partitioning
        __props__["max_size_in_megabytes"] = max_size_in_megabytes
        __props__["name"] = name
        __props__["namespace_name"] = namespace_name
        __props__["requires_duplicate_detection"] = requires_duplicate_detection
        __props__["resource_group_name"] = resource_group_name
        __props__["status"] = status
        __props__["support_ordering"] = support_ordering
        return Topic(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
