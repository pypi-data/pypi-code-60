# coding: utf-8

"""
    REST API

    Rockset's REST API allows for creating and managing all resources in Rockset. Each supported endpoint is documented below.  All requests must be authorized with a Rockset API key, which can be created in the [Rockset console](https://console.rockset.com). The API key must be provided as `ApiKey <api_key>` in the `Authorization` request header. For example: ``` Authorization: ApiKey aB35kDjg93J5nsf4GjwMeErAVd832F7ad4vhsW1S02kfZiab42sTsfW5Sxt25asT ```  All endpoints are only accessible via https.  Build something awesome!  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from rockset.swagger_client.models.query_lambda_version import QueryLambdaVersion  # noqa: F401,E501


class QueryLambda(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'workspace': 'str',
        'last_updated_by': 'str',
        'last_updated': 'str',
        'name': 'str',
        'version_count': 'int',
        'collections': 'list[str]',
        'latest_version': 'QueryLambdaVersion'
    }

    attribute_map = {
        'workspace': 'workspace',
        'last_updated_by': 'last_updated_by',
        'last_updated': 'last_updated',
        'name': 'name',
        'version_count': 'version_count',
        'collections': 'collections',
        'latest_version': 'latest_version'
    }

    def __init__(self, **kwargs):  # noqa: E501
        """QueryLambda - a model defined in Swagger"""  # noqa: E501

        self._workspace = None
        self._last_updated_by = None
        self._last_updated = None
        self._name = None
        self._version_count = None
        self._collections = None
        self._latest_version = None
        self.discriminator = None

        self.workspace = kwargs.pop('workspace', None)
        self.last_updated_by = kwargs.pop('last_updated_by', None)
        self.last_updated = kwargs.pop('last_updated', None)
        self.name = kwargs.pop('name', None)
        self.version_count = kwargs.pop('version_count', None)
        self.collections = kwargs.pop('collections', None)
        self.latest_version = kwargs.pop('latest_version', None)

    @property
    def workspace(self):
        """Gets the workspace of this QueryLambda.  # noqa: E501

        workspace of this Query Lambda  # noqa: E501

        :return: The workspace of this QueryLambda.  # noqa: E501
        :rtype: str
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """Sets the workspace of this QueryLambda.

        workspace of this Query Lambda  # noqa: E501

        :param workspace: The workspace of this QueryLambda.  # noqa: E501
        :type: str
        """

        self._workspace = workspace

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this QueryLambda.  # noqa: E501

        user that created this Query Lambda  # noqa: E501

        :return: The last_updated_by of this QueryLambda.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this QueryLambda.

        user that created this Query Lambda  # noqa: E501

        :param last_updated_by: The last_updated_by of this QueryLambda.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def last_updated(self):
        """Gets the last_updated of this QueryLambda.  # noqa: E501

        ISO-8601 date of when Query Lambda was last updated  # noqa: E501

        :return: The last_updated of this QueryLambda.  # noqa: E501
        :rtype: str
        """
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated):
        """Sets the last_updated of this QueryLambda.

        ISO-8601 date of when Query Lambda was last updated  # noqa: E501

        :param last_updated: The last_updated of this QueryLambda.  # noqa: E501
        :type: str
        """

        self._last_updated = last_updated

    @property
    def name(self):
        """Gets the name of this QueryLambda.  # noqa: E501

        Query Lambda name  # noqa: E501

        :return: The name of this QueryLambda.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this QueryLambda.

        Query Lambda name  # noqa: E501

        :param name: The name of this QueryLambda.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def version_count(self):
        """Gets the version_count of this QueryLambda.  # noqa: E501

        number of Query Lambda versions  # noqa: E501

        :return: The version_count of this QueryLambda.  # noqa: E501
        :rtype: int
        """
        return self._version_count

    @version_count.setter
    def version_count(self, version_count):
        """Sets the version_count of this QueryLambda.

        number of Query Lambda versions  # noqa: E501

        :param version_count: The version_count of this QueryLambda.  # noqa: E501
        :type: int
        """

        self._version_count = version_count

    @property
    def collections(self):
        """Gets the collections of this QueryLambda.  # noqa: E501

        collections queried by underlying SQL query  # noqa: E501

        :return: The collections of this QueryLambda.  # noqa: E501
        :rtype: list[str]
        """
        return self._collections

    @collections.setter
    def collections(self, collections):
        """Sets the collections of this QueryLambda.

        collections queried by underlying SQL query  # noqa: E501

        :param collections: The collections of this QueryLambda.  # noqa: E501
        :type: list[str]
        """

        self._collections = collections

    @property
    def latest_version(self):
        """Gets the latest_version of this QueryLambda.  # noqa: E501

        Query Lambda version details for most recently created version  # noqa: E501

        :return: The latest_version of this QueryLambda.  # noqa: E501
        :rtype: QueryLambdaVersion
        """
        return self._latest_version

    @latest_version.setter
    def latest_version(self, latest_version):
        """Sets the latest_version of this QueryLambda.

        Query Lambda version details for most recently created version  # noqa: E501

        :param latest_version: The latest_version of this QueryLambda.  # noqa: E501
        :type: QueryLambdaVersion
        """

        self._latest_version = latest_version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(QueryLambda, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QueryLambda):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, item):
        return getattr(self, item)

    def items(self):
        return self.to_dict().items()

    def __setitem__(self, item, value):
        return seattr(self, item, value)
