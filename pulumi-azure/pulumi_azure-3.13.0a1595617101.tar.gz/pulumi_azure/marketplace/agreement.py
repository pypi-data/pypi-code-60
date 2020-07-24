# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Agreement(pulumi.CustomResource):
    license_text_link: pulumi.Output[str]
    offer: pulumi.Output[str]
    """
    The Offer of the Marketplace Image. Changing this forces a new resource to be created.
    """
    plan: pulumi.Output[str]
    """
    The Plan of the Marketplace Image. Changing this forces a new resource to be created.
    """
    privacy_policy_link: pulumi.Output[str]
    publisher: pulumi.Output[str]
    """
    The Publisher of the Marketplace Image. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, offer=None, plan=None, publisher=None, __props__=None, __name__=None, __opts__=None):
        """
        Allows accepting the Legal Terms for a Marketplace Image.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        barracuda = azure.marketplace.Agreement("barracuda",
            offer="waf",
            plan="hourly",
            publisher="barracudanetworks")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] offer: The Offer of the Marketplace Image. Changing this forces a new resource to be created.
        :param pulumi.Input[str] plan: The Plan of the Marketplace Image. Changing this forces a new resource to be created.
        :param pulumi.Input[str] publisher: The Publisher of the Marketplace Image. Changing this forces a new resource to be created.
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

            if offer is None:
                raise TypeError("Missing required property 'offer'")
            __props__['offer'] = offer
            if plan is None:
                raise TypeError("Missing required property 'plan'")
            __props__['plan'] = plan
            if publisher is None:
                raise TypeError("Missing required property 'publisher'")
            __props__['publisher'] = publisher
            __props__['license_text_link'] = None
            __props__['privacy_policy_link'] = None
        super(Agreement, __self__).__init__(
            'azure:marketplace/agreement:Agreement',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, license_text_link=None, offer=None, plan=None, privacy_policy_link=None, publisher=None):
        """
        Get an existing Agreement resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] offer: The Offer of the Marketplace Image. Changing this forces a new resource to be created.
        :param pulumi.Input[str] plan: The Plan of the Marketplace Image. Changing this forces a new resource to be created.
        :param pulumi.Input[str] publisher: The Publisher of the Marketplace Image. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["license_text_link"] = license_text_link
        __props__["offer"] = offer
        __props__["plan"] = plan
        __props__["privacy_policy_link"] = privacy_policy_link
        __props__["publisher"] = publisher
        return Agreement(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
