# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetVirtualNetworkGatewayResult:
    """
    A collection of values returned by getVirtualNetworkGateway.
    """
    def __init__(__self__, active_active=None, bgp_settings=None, default_local_network_gateway_id=None, enable_bgp=None, generation=None, id=None, ip_configurations=None, location=None, name=None, resource_group_name=None, sku=None, tags=None, type=None, vpn_client_configurations=None, vpn_type=None):
        if active_active and not isinstance(active_active, bool):
            raise TypeError("Expected argument 'active_active' to be a bool")
        __self__.active_active = active_active
        """
        Is this an Active-Active Gateway?
        """
        if bgp_settings and not isinstance(bgp_settings, list):
            raise TypeError("Expected argument 'bgp_settings' to be a list")
        __self__.bgp_settings = bgp_settings
        if default_local_network_gateway_id and not isinstance(default_local_network_gateway_id, str):
            raise TypeError("Expected argument 'default_local_network_gateway_id' to be a str")
        __self__.default_local_network_gateway_id = default_local_network_gateway_id
        """
        The ID of the local network gateway
        through which outbound Internet traffic from the virtual network in which the
        gateway is created will be routed (*forced tunneling*). Refer to the
        [Azure documentation on forced tunneling](https://docs.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-forced-tunneling-rm).
        """
        if enable_bgp and not isinstance(enable_bgp, bool):
            raise TypeError("Expected argument 'enable_bgp' to be a bool")
        __self__.enable_bgp = enable_bgp
        """
        Will BGP (Border Gateway Protocol) will be enabled
        for this Virtual Network Gateway.
        """
        if generation and not isinstance(generation, str):
            raise TypeError("Expected argument 'generation' to be a str")
        __self__.generation = generation
        """
        The Generation of the Virtual Network Gateway.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if ip_configurations and not isinstance(ip_configurations, list):
            raise TypeError("Expected argument 'ip_configurations' to be a list")
        __self__.ip_configurations = ip_configurations
        """
        One or two `ip_configuration` blocks documented below.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The location/region where the Virtual Network Gateway is located.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The user-defined name of the revoked certificate.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        """
        Configuration of the size and capacity of the Virtual Network Gateway.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        __self__.type = type
        """
        The type of the Virtual Network Gateway.
        """
        if vpn_client_configurations and not isinstance(vpn_client_configurations, list):
            raise TypeError("Expected argument 'vpn_client_configurations' to be a list")
        __self__.vpn_client_configurations = vpn_client_configurations
        """
        A `vpn_client_configuration` block which is documented below.
        """
        if vpn_type and not isinstance(vpn_type, str):
            raise TypeError("Expected argument 'vpn_type' to be a str")
        __self__.vpn_type = vpn_type
        """
        The routing type of the Virtual Network Gateway.
        """
class AwaitableGetVirtualNetworkGatewayResult(GetVirtualNetworkGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkGatewayResult(
            active_active=self.active_active,
            bgp_settings=self.bgp_settings,
            default_local_network_gateway_id=self.default_local_network_gateway_id,
            enable_bgp=self.enable_bgp,
            generation=self.generation,
            id=self.id,
            ip_configurations=self.ip_configurations,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            vpn_client_configurations=self.vpn_client_configurations,
            vpn_type=self.vpn_type)

def get_virtual_network_gateway(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Virtual Network Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_virtual_network_gateway(name="production",
        resource_group_name="networking")
    pulumi.export("virtualNetworkGatewayId", example.id)
    ```


    :param str name: Specifies the name of the Virtual Network Gateway.
    :param str resource_group_name: Specifies the name of the resource group the Virtual Network Gateway is located in.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:network/getVirtualNetworkGateway:getVirtualNetworkGateway', __args__, opts=opts).value

    return AwaitableGetVirtualNetworkGatewayResult(
        active_active=__ret__.get('activeActive'),
        bgp_settings=__ret__.get('bgpSettings'),
        default_local_network_gateway_id=__ret__.get('defaultLocalNetworkGatewayId'),
        enable_bgp=__ret__.get('enableBgp'),
        generation=__ret__.get('generation'),
        id=__ret__.get('id'),
        ip_configurations=__ret__.get('ipConfigurations'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        sku=__ret__.get('sku'),
        tags=__ret__.get('tags'),
        type=__ret__.get('type'),
        vpn_client_configurations=__ret__.get('vpnClientConfigurations'),
        vpn_type=__ret__.get('vpnType'))
