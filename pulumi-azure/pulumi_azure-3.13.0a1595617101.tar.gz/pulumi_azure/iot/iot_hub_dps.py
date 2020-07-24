# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class IotHubDps(pulumi.CustomResource):
    allocation_policy: pulumi.Output[str]
    """
    The allocation policy of the IoT Device Provisioning Service.
    """
    device_provisioning_host_name: pulumi.Output[str]
    """
    The device endpoint of the IoT Device Provisioning Service.
    """
    id_scope: pulumi.Output[str]
    """
    The unique identifier of the IoT Device Provisioning Service.
    """
    linked_hubs: pulumi.Output[list]
    """
    A `linked_hub` block as defined below.

      * `allocationWeight` (`float`) - The weight applied to the IoT Hub. Defaults to 0.
      * `applyAllocationPolicy` (`bool`) - Determines whether to apply allocation policies to the IoT Hub. Defaults to false.
      * `connection_string` (`str`) - The connection string to connect to the IoT Hub. Changing this forces a new resource.
      * `hostname` (`str`) - The IoT Hub hostname.
      * `location` (`str`) - The location of the IoT hub. Changing this forces a new resource.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource has to be createc. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Iot Device Provisioning Service resource. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group under which the Iot Device Provisioning Service resource has to be created. Changing this forces a new resource to be created.
    """
    service_operations_host_name: pulumi.Output[str]
    """
    The service endpoint of the IoT Device Provisioning Service.
    """
    sku: pulumi.Output[dict]
    """
    A `sku` block as defined below.

      * `capacity` (`float`) - The number of provisioned IoT Device Provisioning Service units.
      * `name` (`str`) - The name of the sku. Possible values are `B1`, `B2`, `B3`, `F1`, `S1`, `S2`, and `S3`.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, linked_hubs=None, location=None, name=None, resource_group_name=None, sku=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an IotHub Device Provisioning Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_iot_hub_dps = azure.iot.IotHubDps("exampleIotHubDps",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            sku={
                "name": "S1",
                "capacity": "1",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] linked_hubs: A `linked_hub` block as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource has to be createc. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Iot Device Provisioning Service resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the Iot Device Provisioning Service resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] sku: A `sku` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **linked_hubs** object supports the following:

          * `allocationWeight` (`pulumi.Input[float]`) - The weight applied to the IoT Hub. Defaults to 0.
          * `applyAllocationPolicy` (`pulumi.Input[bool]`) - Determines whether to apply allocation policies to the IoT Hub. Defaults to false.
          * `connection_string` (`pulumi.Input[str]`) - The connection string to connect to the IoT Hub. Changing this forces a new resource.
          * `hostname` (`pulumi.Input[str]`) - The IoT Hub hostname.
          * `location` (`pulumi.Input[str]`) - The location of the IoT hub. Changing this forces a new resource.

        The **sku** object supports the following:

          * `capacity` (`pulumi.Input[float]`) - The number of provisioned IoT Device Provisioning Service units.
          * `name` (`pulumi.Input[str]`) - The name of the sku. Possible values are `B1`, `B2`, `B3`, `F1`, `S1`, `S2`, and `S3`.
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

            __props__['linked_hubs'] = linked_hubs
            __props__['location'] = location
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['allocation_policy'] = None
            __props__['device_provisioning_host_name'] = None
            __props__['id_scope'] = None
            __props__['service_operations_host_name'] = None
        super(IotHubDps, __self__).__init__(
            'azure:iot/iotHubDps:IotHubDps',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, allocation_policy=None, device_provisioning_host_name=None, id_scope=None, linked_hubs=None, location=None, name=None, resource_group_name=None, service_operations_host_name=None, sku=None, tags=None):
        """
        Get an existing IotHubDps resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_policy: The allocation policy of the IoT Device Provisioning Service.
        :param pulumi.Input[str] device_provisioning_host_name: The device endpoint of the IoT Device Provisioning Service.
        :param pulumi.Input[str] id_scope: The unique identifier of the IoT Device Provisioning Service.
        :param pulumi.Input[list] linked_hubs: A `linked_hub` block as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource has to be createc. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Iot Device Provisioning Service resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the Iot Device Provisioning Service resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] service_operations_host_name: The service endpoint of the IoT Device Provisioning Service.
        :param pulumi.Input[dict] sku: A `sku` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **linked_hubs** object supports the following:

          * `allocationWeight` (`pulumi.Input[float]`) - The weight applied to the IoT Hub. Defaults to 0.
          * `applyAllocationPolicy` (`pulumi.Input[bool]`) - Determines whether to apply allocation policies to the IoT Hub. Defaults to false.
          * `connection_string` (`pulumi.Input[str]`) - The connection string to connect to the IoT Hub. Changing this forces a new resource.
          * `hostname` (`pulumi.Input[str]`) - The IoT Hub hostname.
          * `location` (`pulumi.Input[str]`) - The location of the IoT hub. Changing this forces a new resource.

        The **sku** object supports the following:

          * `capacity` (`pulumi.Input[float]`) - The number of provisioned IoT Device Provisioning Service units.
          * `name` (`pulumi.Input[str]`) - The name of the sku. Possible values are `B1`, `B2`, `B3`, `F1`, `S1`, `S2`, and `S3`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allocation_policy"] = allocation_policy
        __props__["device_provisioning_host_name"] = device_provisioning_host_name
        __props__["id_scope"] = id_scope
        __props__["linked_hubs"] = linked_hubs
        __props__["location"] = location
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["service_operations_host_name"] = service_operations_host_name
        __props__["sku"] = sku
        __props__["tags"] = tags
        return IotHubDps(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
