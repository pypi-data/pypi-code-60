# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class NetworkInterfaceBackendAddressPoolAssociation(pulumi.CustomResource):
    backend_address_pool_id: pulumi.Output[str]
    """
    The ID of the Load Balancer Backend Address Pool which this Network Interface which should be connected to. Changing this forces a new resource to be created.
    """
    ip_configuration_name: pulumi.Output[str]
    """
    The Name of the IP Configuration within the Network Interface which should be connected to the Backend Address Pool. Changing this forces a new resource to be created.
    """
    network_interface_id: pulumi.Output[str]
    """
    The ID of the Network Interface. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, backend_address_pool_id=None, ip_configuration_name=None, network_interface_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages the association between a Network Interface and a Load Balancer's Backend Address Pool.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefix="10.0.2.0/24")
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("exampleLoadBalancer",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            frontend_ip_configurations=[{
                "name": "primary",
                "public_ip_address_id": example_public_ip.id,
            }])
        example_backend_address_pool = azure.lb.BackendAddressPool("exampleBackendAddressPool",
            resource_group_name=example_resource_group.name,
            loadbalancer_id=example_load_balancer.id)
        example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            ip_configurations=[{
                "name": "testconfiguration1",
                "subnet_id": example_subnet.id,
                "privateIpAddressAllocation": "Dynamic",
            }])
        example_network_interface_backend_address_pool_association = azure.network.NetworkInterfaceBackendAddressPoolAssociation("exampleNetworkInterfaceBackendAddressPoolAssociation",
            network_interface_id=example_network_interface.id,
            ip_configuration_name="testconfiguration1",
            backend_address_pool_id=example_backend_address_pool.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_address_pool_id: The ID of the Load Balancer Backend Address Pool which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] ip_configuration_name: The Name of the IP Configuration within the Network Interface which should be connected to the Backend Address Pool. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
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

            if backend_address_pool_id is None:
                raise TypeError("Missing required property 'backend_address_pool_id'")
            __props__['backend_address_pool_id'] = backend_address_pool_id
            if ip_configuration_name is None:
                raise TypeError("Missing required property 'ip_configuration_name'")
            __props__['ip_configuration_name'] = ip_configuration_name
            if network_interface_id is None:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__['network_interface_id'] = network_interface_id
        super(NetworkInterfaceBackendAddressPoolAssociation, __self__).__init__(
            'azure:network/networkInterfaceBackendAddressPoolAssociation:NetworkInterfaceBackendAddressPoolAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, backend_address_pool_id=None, ip_configuration_name=None, network_interface_id=None):
        """
        Get an existing NetworkInterfaceBackendAddressPoolAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend_address_pool_id: The ID of the Load Balancer Backend Address Pool which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] ip_configuration_name: The Name of the IP Configuration within the Network Interface which should be connected to the Backend Address Pool. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["backend_address_pool_id"] = backend_address_pool_id
        __props__["ip_configuration_name"] = ip_configuration_name
        __props__["network_interface_id"] = network_interface_id
        return NetworkInterfaceBackendAddressPoolAssociation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
