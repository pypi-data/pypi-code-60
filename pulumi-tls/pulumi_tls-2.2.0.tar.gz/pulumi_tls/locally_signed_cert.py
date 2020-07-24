# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables


class LocallySignedCert(pulumi.CustomResource):
    allowed_uses: pulumi.Output[list]
    """
    List of keywords each describing a use that is permitted
    for the issued certificate. The valid keywords are listed below.
    """
    ca_cert_pem: pulumi.Output[str]
    """
    PEM-encoded certificate data for the CA.
    """
    ca_key_algorithm: pulumi.Output[str]
    """
    The name of the algorithm for the key provided
    in `ca_private_key_pem`.
    """
    ca_private_key_pem: pulumi.Output[str]
    """
    PEM-encoded private key data for the CA.
    This can be read from a separate file using the ``file`` interpolation
    function.
    """
    cert_pem: pulumi.Output[str]
    """
    The certificate data in PEM format.
    """
    cert_request_pem: pulumi.Output[str]
    """
    PEM-encoded request certificate data.
    """
    early_renewal_hours: pulumi.Output[float]
    """
    Number of hours before the certificates expiry when a new certificate will be generated
    """
    is_ca_certificate: pulumi.Output[bool]
    """
    Boolean controlling whether the CA flag will be set in the
    generated certificate. Defaults to `false`, meaning that the certificate does not represent
    a certificate authority.
    """
    ready_for_renewal: pulumi.Output[bool]
    set_subject_key_id: pulumi.Output[bool]
    """
    If `true`, the certificate will include
    the subject key identifier. Defaults to `false`, in which case the subject
    key identifier is not set at all.
    """
    validity_end_time: pulumi.Output[str]
    """
    The time until which the certificate is invalid, as an
    [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp.
    """
    validity_period_hours: pulumi.Output[float]
    """
    The number of hours after initial issuing that the
    certificate will become invalid.
    """
    validity_start_time: pulumi.Output[str]
    """
    The time after which the certificate is valid, as an
    [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp.
    """
    def __init__(__self__, resource_name, opts=None, allowed_uses=None, ca_cert_pem=None, ca_key_algorithm=None, ca_private_key_pem=None, cert_request_pem=None, early_renewal_hours=None, is_ca_certificate=None, set_subject_key_id=None, validity_period_hours=None, __props__=None, __name__=None, __opts__=None):
        """
        Create a LocallySignedCert resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] allowed_uses: List of keywords each describing a use that is permitted
               for the issued certificate. The valid keywords are listed below.
        :param pulumi.Input[str] ca_cert_pem: PEM-encoded certificate data for the CA.
        :param pulumi.Input[str] ca_key_algorithm: The name of the algorithm for the key provided
               in `ca_private_key_pem`.
        :param pulumi.Input[str] ca_private_key_pem: PEM-encoded private key data for the CA.
               This can be read from a separate file using the ``file`` interpolation
               function.
        :param pulumi.Input[str] cert_request_pem: PEM-encoded request certificate data.
        :param pulumi.Input[float] early_renewal_hours: Number of hours before the certificates expiry when a new certificate will be generated
        :param pulumi.Input[bool] is_ca_certificate: Boolean controlling whether the CA flag will be set in the
               generated certificate. Defaults to `false`, meaning that the certificate does not represent
               a certificate authority.
        :param pulumi.Input[bool] set_subject_key_id: If `true`, the certificate will include
               the subject key identifier. Defaults to `false`, in which case the subject
               key identifier is not set at all.
        :param pulumi.Input[float] validity_period_hours: The number of hours after initial issuing that the
               certificate will become invalid.
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

            if allowed_uses is None:
                raise TypeError("Missing required property 'allowed_uses'")
            __props__['allowed_uses'] = allowed_uses
            if ca_cert_pem is None:
                raise TypeError("Missing required property 'ca_cert_pem'")
            __props__['ca_cert_pem'] = ca_cert_pem
            if ca_key_algorithm is None:
                raise TypeError("Missing required property 'ca_key_algorithm'")
            __props__['ca_key_algorithm'] = ca_key_algorithm
            if ca_private_key_pem is None:
                raise TypeError("Missing required property 'ca_private_key_pem'")
            __props__['ca_private_key_pem'] = ca_private_key_pem
            if cert_request_pem is None:
                raise TypeError("Missing required property 'cert_request_pem'")
            __props__['cert_request_pem'] = cert_request_pem
            __props__['early_renewal_hours'] = early_renewal_hours
            __props__['is_ca_certificate'] = is_ca_certificate
            __props__['set_subject_key_id'] = set_subject_key_id
            if validity_period_hours is None:
                raise TypeError("Missing required property 'validity_period_hours'")
            __props__['validity_period_hours'] = validity_period_hours
            __props__['cert_pem'] = None
            __props__['ready_for_renewal'] = None
            __props__['validity_end_time'] = None
            __props__['validity_start_time'] = None
        super(LocallySignedCert, __self__).__init__(
            'tls:index/locallySignedCert:LocallySignedCert',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, allowed_uses=None, ca_cert_pem=None, ca_key_algorithm=None, ca_private_key_pem=None, cert_pem=None, cert_request_pem=None, early_renewal_hours=None, is_ca_certificate=None, ready_for_renewal=None, set_subject_key_id=None, validity_end_time=None, validity_period_hours=None, validity_start_time=None):
        """
        Get an existing LocallySignedCert resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] allowed_uses: List of keywords each describing a use that is permitted
               for the issued certificate. The valid keywords are listed below.
        :param pulumi.Input[str] ca_cert_pem: PEM-encoded certificate data for the CA.
        :param pulumi.Input[str] ca_key_algorithm: The name of the algorithm for the key provided
               in `ca_private_key_pem`.
        :param pulumi.Input[str] ca_private_key_pem: PEM-encoded private key data for the CA.
               This can be read from a separate file using the ``file`` interpolation
               function.
        :param pulumi.Input[str] cert_pem: The certificate data in PEM format.
        :param pulumi.Input[str] cert_request_pem: PEM-encoded request certificate data.
        :param pulumi.Input[float] early_renewal_hours: Number of hours before the certificates expiry when a new certificate will be generated
        :param pulumi.Input[bool] is_ca_certificate: Boolean controlling whether the CA flag will be set in the
               generated certificate. Defaults to `false`, meaning that the certificate does not represent
               a certificate authority.
        :param pulumi.Input[bool] set_subject_key_id: If `true`, the certificate will include
               the subject key identifier. Defaults to `false`, in which case the subject
               key identifier is not set at all.
        :param pulumi.Input[str] validity_end_time: The time until which the certificate is invalid, as an
               [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp.
        :param pulumi.Input[float] validity_period_hours: The number of hours after initial issuing that the
               certificate will become invalid.
        :param pulumi.Input[str] validity_start_time: The time after which the certificate is valid, as an
               [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allowed_uses"] = allowed_uses
        __props__["ca_cert_pem"] = ca_cert_pem
        __props__["ca_key_algorithm"] = ca_key_algorithm
        __props__["ca_private_key_pem"] = ca_private_key_pem
        __props__["cert_pem"] = cert_pem
        __props__["cert_request_pem"] = cert_request_pem
        __props__["early_renewal_hours"] = early_renewal_hours
        __props__["is_ca_certificate"] = is_ca_certificate
        __props__["ready_for_renewal"] = ready_for_renewal
        __props__["set_subject_key_id"] = set_subject_key_id
        __props__["validity_end_time"] = validity_end_time
        __props__["validity_period_hours"] = validity_period_hours
        __props__["validity_start_time"] = validity_start_time
        return LocallySignedCert(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
