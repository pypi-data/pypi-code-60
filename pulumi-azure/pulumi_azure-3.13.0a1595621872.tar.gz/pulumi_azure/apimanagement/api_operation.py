# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class ApiOperation(pulumi.CustomResource):
    api_management_name: pulumi.Output[str]
    """
    The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
    """
    api_name: pulumi.Output[str]
    """
    The name of the API within the API Management Service where this API Operation should be created. Changing this forces a new resource to be created.
    """
    description: pulumi.Output[str]
    """
    A description for this API Operation, which may include HTML formatting tags.
    """
    display_name: pulumi.Output[str]
    """
    The Display Name for this API Management Operation.
    """
    method: pulumi.Output[str]
    """
    The HTTP Method used for this API Management Operation, like `GET`, `DELETE`, `PUT` or `POST` - but not limited to these values.
    """
    operation_id: pulumi.Output[str]
    """
    A unique identifier for this API Operation. Changing this forces a new resource to be created.
    """
    request: pulumi.Output[dict]
    """
    A `request` block as defined below.

      * `description` (`str`) - A description of the HTTP Request, which may include HTML tags.
      * `headers` (`list`) - One or more `header` blocks as defined above.
        * `defaultValue` (`str`) - The default value for this Header.
        * `description` (`str`) - A description of this Header.
        * `name` (`str`) - The Name of this Header.
        * `required` (`bool`) - Is this Header Required?
        * `type` (`str`) - The Type of this Header, such as a `string`.
        * `values` (`list`) - One or more acceptable values for this Header.

      * `queryParameters` (`list`) - One or more `query_parameter` blocks as defined above.
        * `defaultValue` (`str`) - The default value for this Query Parameter.
        * `description` (`str`) - A description of this Query Parameter.
        * `name` (`str`) - The Name of this Query Parameter.
        * `required` (`bool`) - Is this Query Parameter Required?
        * `type` (`str`) - The Type of this Query Parameter, such as a `string`.
        * `values` (`list`) - One or more acceptable values for this Query Parameter.

      * `representations` (`list`) - One or more `representation` blocks as defined below.
        * `content_type` (`str`) - The Content Type of this representation, such as `application/json`.
        * `formParameters` (`list`) - One or more `form_parameter` block as defined above.
          * `defaultValue` (`str`) - The default value for this Form Parameter.
          * `description` (`str`) - A description of this Form Parameter.
          * `name` (`str`) - The Name of this Form Parameter.
          * `required` (`bool`) - Is this Form Parameter Required?
          * `type` (`str`) - The Type of this Form Parameter, such as a `string`.
          * `values` (`list`) - One or more acceptable values for this Form Parameter.

        * `sample` (`str`) - An example of this representation.
        * `schema_id` (`str`) - The ID of an API Management Schema which represents this Response.
        * `typeName` (`str`) - The Type Name defined by the Schema.
    """
    resource_group_name: pulumi.Output[str]
    """
    The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
    """
    responses: pulumi.Output[list]
    """
    One or more `response` blocks as defined below.

      * `description` (`str`) - A description of the HTTP Response, which may include HTML tags.
      * `headers` (`list`) - One or more `header` blocks as defined above.
        * `defaultValue` (`str`) - The default value for this Header.
        * `description` (`str`) - A description of this Header.
        * `name` (`str`) - The Name of this Header.
        * `required` (`bool`) - Is this Header Required?
        * `type` (`str`) - The Type of this Header, such as a `string`.
        * `values` (`list`) - One or more acceptable values for this Header.

      * `representations` (`list`) - One or more `representation` blocks as defined below.
        * `content_type` (`str`) - The Content Type of this representation, such as `application/json`.
        * `formParameters` (`list`) - One or more `form_parameter` block as defined above.
          * `defaultValue` (`str`) - The default value for this Form Parameter.
          * `description` (`str`) - A description of this Form Parameter.
          * `name` (`str`) - The Name of this Form Parameter.
          * `required` (`bool`) - Is this Form Parameter Required?
          * `type` (`str`) - The Type of this Form Parameter, such as a `string`.
          * `values` (`list`) - One or more acceptable values for this Form Parameter.

        * `sample` (`str`) - An example of this representation.
        * `schema_id` (`str`) - The ID of an API Management Schema which represents this Response.
        * `typeName` (`str`) - The Type Name defined by the Schema.

      * `statusCode` (`float`) - The HTTP Status Code.
    """
    template_parameters: pulumi.Output[list]
    """
    One or more `template_parameter` blocks as defined below.

      * `defaultValue` (`str`) - The default value for this Template Parameter.
      * `description` (`str`) - A description of this Template Parameter.
      * `name` (`str`) - The Name of this Template Parameter.
      * `required` (`bool`) - Is this Template Parameter Required?
      * `type` (`str`) - The Type of this Template Parameter, such as a `string`.
      * `values` (`list`) - One or more acceptable values for this Template Parameter.
    """
    url_template: pulumi.Output[str]
    """
    The relative URL Template identifying the target resource for this operation, which may include parameters.
    """
    def __init__(__self__, resource_name, opts=None, api_management_name=None, api_name=None, description=None, display_name=None, method=None, operation_id=None, request=None, resource_group_name=None, responses=None, template_parameters=None, url_template=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an API Operation within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_api = azure.apimanagement.get_api(name="search-api",
            api_management_name="search-api-management",
            resource_group_name="search-service",
            revision="2")
        example_api_operation = azure.apimanagement.ApiOperation("exampleApiOperation",
            operation_id="user-delete",
            api_name=example_api.name,
            api_management_name=example_api.api_management_name,
            resource_group_name=example_api.resource_group_name,
            display_name="Delete User Operation",
            method="DELETE",
            url_template="/users/{id}/delete",
            description="This can only be done by the logged in user.",
            responses=[{
                "statusCode": 200,
            }])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] api_name: The name of the API within the API Management Service where this API Operation should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: A description for this API Operation, which may include HTML formatting tags.
        :param pulumi.Input[str] display_name: The Display Name for this API Management Operation.
        :param pulumi.Input[str] method: The HTTP Method used for this API Management Operation, like `GET`, `DELETE`, `PUT` or `POST` - but not limited to these values.
        :param pulumi.Input[str] operation_id: A unique identifier for this API Operation. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] request: A `request` block as defined below.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[list] responses: One or more `response` blocks as defined below.
        :param pulumi.Input[list] template_parameters: One or more `template_parameter` blocks as defined below.
        :param pulumi.Input[str] url_template: The relative URL Template identifying the target resource for this operation, which may include parameters.

        The **request** object supports the following:

          * `description` (`pulumi.Input[str]`) - A description of the HTTP Request, which may include HTML tags.
          * `headers` (`pulumi.Input[list]`) - One or more `header` blocks as defined above.
            * `defaultValue` (`pulumi.Input[str]`) - The default value for this Header.
            * `description` (`pulumi.Input[str]`) - A description of this Header.
            * `name` (`pulumi.Input[str]`) - The Name of this Header.
            * `required` (`pulumi.Input[bool]`) - Is this Header Required?
            * `type` (`pulumi.Input[str]`) - The Type of this Header, such as a `string`.
            * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Header.

          * `queryParameters` (`pulumi.Input[list]`) - One or more `query_parameter` blocks as defined above.
            * `defaultValue` (`pulumi.Input[str]`) - The default value for this Query Parameter.
            * `description` (`pulumi.Input[str]`) - A description of this Query Parameter.
            * `name` (`pulumi.Input[str]`) - The Name of this Query Parameter.
            * `required` (`pulumi.Input[bool]`) - Is this Query Parameter Required?
            * `type` (`pulumi.Input[str]`) - The Type of this Query Parameter, such as a `string`.
            * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Query Parameter.

          * `representations` (`pulumi.Input[list]`) - One or more `representation` blocks as defined below.
            * `content_type` (`pulumi.Input[str]`) - The Content Type of this representation, such as `application/json`.
            * `formParameters` (`pulumi.Input[list]`) - One or more `form_parameter` block as defined above.
              * `defaultValue` (`pulumi.Input[str]`) - The default value for this Form Parameter.
              * `description` (`pulumi.Input[str]`) - A description of this Form Parameter.
              * `name` (`pulumi.Input[str]`) - The Name of this Form Parameter.
              * `required` (`pulumi.Input[bool]`) - Is this Form Parameter Required?
              * `type` (`pulumi.Input[str]`) - The Type of this Form Parameter, such as a `string`.
              * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Form Parameter.

            * `sample` (`pulumi.Input[str]`) - An example of this representation.
            * `schema_id` (`pulumi.Input[str]`) - The ID of an API Management Schema which represents this Response.
            * `typeName` (`pulumi.Input[str]`) - The Type Name defined by the Schema.

        The **responses** object supports the following:

          * `description` (`pulumi.Input[str]`) - A description of the HTTP Response, which may include HTML tags.
          * `headers` (`pulumi.Input[list]`) - One or more `header` blocks as defined above.
            * `defaultValue` (`pulumi.Input[str]`) - The default value for this Header.
            * `description` (`pulumi.Input[str]`) - A description of this Header.
            * `name` (`pulumi.Input[str]`) - The Name of this Header.
            * `required` (`pulumi.Input[bool]`) - Is this Header Required?
            * `type` (`pulumi.Input[str]`) - The Type of this Header, such as a `string`.
            * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Header.

          * `representations` (`pulumi.Input[list]`) - One or more `representation` blocks as defined below.
            * `content_type` (`pulumi.Input[str]`) - The Content Type of this representation, such as `application/json`.
            * `formParameters` (`pulumi.Input[list]`) - One or more `form_parameter` block as defined above.
              * `defaultValue` (`pulumi.Input[str]`) - The default value for this Form Parameter.
              * `description` (`pulumi.Input[str]`) - A description of this Form Parameter.
              * `name` (`pulumi.Input[str]`) - The Name of this Form Parameter.
              * `required` (`pulumi.Input[bool]`) - Is this Form Parameter Required?
              * `type` (`pulumi.Input[str]`) - The Type of this Form Parameter, such as a `string`.
              * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Form Parameter.

            * `sample` (`pulumi.Input[str]`) - An example of this representation.
            * `schema_id` (`pulumi.Input[str]`) - The ID of an API Management Schema which represents this Response.
            * `typeName` (`pulumi.Input[str]`) - The Type Name defined by the Schema.

          * `statusCode` (`pulumi.Input[float]`) - The HTTP Status Code.

        The **template_parameters** object supports the following:

          * `defaultValue` (`pulumi.Input[str]`) - The default value for this Template Parameter.
          * `description` (`pulumi.Input[str]`) - A description of this Template Parameter.
          * `name` (`pulumi.Input[str]`) - The Name of this Template Parameter.
          * `required` (`pulumi.Input[bool]`) - Is this Template Parameter Required?
          * `type` (`pulumi.Input[str]`) - The Type of this Template Parameter, such as a `string`.
          * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Template Parameter.
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
            if api_name is None:
                raise TypeError("Missing required property 'api_name'")
            __props__['api_name'] = api_name
            __props__['description'] = description
            if display_name is None:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            if method is None:
                raise TypeError("Missing required property 'method'")
            __props__['method'] = method
            if operation_id is None:
                raise TypeError("Missing required property 'operation_id'")
            __props__['operation_id'] = operation_id
            __props__['request'] = request
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['responses'] = responses
            __props__['template_parameters'] = template_parameters
            if url_template is None:
                raise TypeError("Missing required property 'url_template'")
            __props__['url_template'] = url_template
        super(ApiOperation, __self__).__init__(
            'azure:apimanagement/apiOperation:ApiOperation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, api_management_name=None, api_name=None, description=None, display_name=None, method=None, operation_id=None, request=None, resource_group_name=None, responses=None, template_parameters=None, url_template=None):
        """
        Get an existing ApiOperation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where the API exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] api_name: The name of the API within the API Management Service where this API Operation should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: A description for this API Operation, which may include HTML formatting tags.
        :param pulumi.Input[str] display_name: The Display Name for this API Management Operation.
        :param pulumi.Input[str] method: The HTTP Method used for this API Management Operation, like `GET`, `DELETE`, `PUT` or `POST` - but not limited to these values.
        :param pulumi.Input[str] operation_id: A unique identifier for this API Operation. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] request: A `request` block as defined below.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group in which the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[list] responses: One or more `response` blocks as defined below.
        :param pulumi.Input[list] template_parameters: One or more `template_parameter` blocks as defined below.
        :param pulumi.Input[str] url_template: The relative URL Template identifying the target resource for this operation, which may include parameters.

        The **request** object supports the following:

          * `description` (`pulumi.Input[str]`) - A description of the HTTP Request, which may include HTML tags.
          * `headers` (`pulumi.Input[list]`) - One or more `header` blocks as defined above.
            * `defaultValue` (`pulumi.Input[str]`) - The default value for this Header.
            * `description` (`pulumi.Input[str]`) - A description of this Header.
            * `name` (`pulumi.Input[str]`) - The Name of this Header.
            * `required` (`pulumi.Input[bool]`) - Is this Header Required?
            * `type` (`pulumi.Input[str]`) - The Type of this Header, such as a `string`.
            * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Header.

          * `queryParameters` (`pulumi.Input[list]`) - One or more `query_parameter` blocks as defined above.
            * `defaultValue` (`pulumi.Input[str]`) - The default value for this Query Parameter.
            * `description` (`pulumi.Input[str]`) - A description of this Query Parameter.
            * `name` (`pulumi.Input[str]`) - The Name of this Query Parameter.
            * `required` (`pulumi.Input[bool]`) - Is this Query Parameter Required?
            * `type` (`pulumi.Input[str]`) - The Type of this Query Parameter, such as a `string`.
            * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Query Parameter.

          * `representations` (`pulumi.Input[list]`) - One or more `representation` blocks as defined below.
            * `content_type` (`pulumi.Input[str]`) - The Content Type of this representation, such as `application/json`.
            * `formParameters` (`pulumi.Input[list]`) - One or more `form_parameter` block as defined above.
              * `defaultValue` (`pulumi.Input[str]`) - The default value for this Form Parameter.
              * `description` (`pulumi.Input[str]`) - A description of this Form Parameter.
              * `name` (`pulumi.Input[str]`) - The Name of this Form Parameter.
              * `required` (`pulumi.Input[bool]`) - Is this Form Parameter Required?
              * `type` (`pulumi.Input[str]`) - The Type of this Form Parameter, such as a `string`.
              * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Form Parameter.

            * `sample` (`pulumi.Input[str]`) - An example of this representation.
            * `schema_id` (`pulumi.Input[str]`) - The ID of an API Management Schema which represents this Response.
            * `typeName` (`pulumi.Input[str]`) - The Type Name defined by the Schema.

        The **responses** object supports the following:

          * `description` (`pulumi.Input[str]`) - A description of the HTTP Response, which may include HTML tags.
          * `headers` (`pulumi.Input[list]`) - One or more `header` blocks as defined above.
            * `defaultValue` (`pulumi.Input[str]`) - The default value for this Header.
            * `description` (`pulumi.Input[str]`) - A description of this Header.
            * `name` (`pulumi.Input[str]`) - The Name of this Header.
            * `required` (`pulumi.Input[bool]`) - Is this Header Required?
            * `type` (`pulumi.Input[str]`) - The Type of this Header, such as a `string`.
            * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Header.

          * `representations` (`pulumi.Input[list]`) - One or more `representation` blocks as defined below.
            * `content_type` (`pulumi.Input[str]`) - The Content Type of this representation, such as `application/json`.
            * `formParameters` (`pulumi.Input[list]`) - One or more `form_parameter` block as defined above.
              * `defaultValue` (`pulumi.Input[str]`) - The default value for this Form Parameter.
              * `description` (`pulumi.Input[str]`) - A description of this Form Parameter.
              * `name` (`pulumi.Input[str]`) - The Name of this Form Parameter.
              * `required` (`pulumi.Input[bool]`) - Is this Form Parameter Required?
              * `type` (`pulumi.Input[str]`) - The Type of this Form Parameter, such as a `string`.
              * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Form Parameter.

            * `sample` (`pulumi.Input[str]`) - An example of this representation.
            * `schema_id` (`pulumi.Input[str]`) - The ID of an API Management Schema which represents this Response.
            * `typeName` (`pulumi.Input[str]`) - The Type Name defined by the Schema.

          * `statusCode` (`pulumi.Input[float]`) - The HTTP Status Code.

        The **template_parameters** object supports the following:

          * `defaultValue` (`pulumi.Input[str]`) - The default value for this Template Parameter.
          * `description` (`pulumi.Input[str]`) - A description of this Template Parameter.
          * `name` (`pulumi.Input[str]`) - The Name of this Template Parameter.
          * `required` (`pulumi.Input[bool]`) - Is this Template Parameter Required?
          * `type` (`pulumi.Input[str]`) - The Type of this Template Parameter, such as a `string`.
          * `values` (`pulumi.Input[list]`) - One or more acceptable values for this Template Parameter.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_management_name"] = api_management_name
        __props__["api_name"] = api_name
        __props__["description"] = description
        __props__["display_name"] = display_name
        __props__["method"] = method
        __props__["operation_id"] = operation_id
        __props__["request"] = request
        __props__["resource_group_name"] = resource_group_name
        __props__["responses"] = responses
        __props__["template_parameters"] = template_parameters
        __props__["url_template"] = url_template
        return ApiOperation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
