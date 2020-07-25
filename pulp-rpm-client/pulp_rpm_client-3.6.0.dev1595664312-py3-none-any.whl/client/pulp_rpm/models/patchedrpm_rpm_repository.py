# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_rpm.configuration import Configuration


class PatchedrpmRpmRepository(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'description': 'str',
        'metadata_signing_service': 'str',
        'retain_package_versions': 'int'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'metadata_signing_service': 'metadata_signing_service',
        'retain_package_versions': 'retain_package_versions'
    }

    def __init__(self, name=None, description=None, metadata_signing_service=None, retain_package_versions=None, local_vars_configuration=None):  # noqa: E501
        """PatchedrpmRpmRepository - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._metadata_signing_service = None
        self._retain_package_versions = None
        self.discriminator = None

        if name is not None:
            self.name = name
        self.description = description
        self.metadata_signing_service = metadata_signing_service
        if retain_package_versions is not None:
            self.retain_package_versions = retain_package_versions

    @property
    def name(self):
        """Gets the name of this PatchedrpmRpmRepository.  # noqa: E501

        A unique name for this repository.  # noqa: E501

        :return: The name of this PatchedrpmRpmRepository.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatchedrpmRpmRepository.

        A unique name for this repository.  # noqa: E501

        :param name: The name of this PatchedrpmRpmRepository.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this PatchedrpmRpmRepository.  # noqa: E501

        An optional description.  # noqa: E501

        :return: The description of this PatchedrpmRpmRepository.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PatchedrpmRpmRepository.

        An optional description.  # noqa: E501

        :param description: The description of this PatchedrpmRpmRepository.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def metadata_signing_service(self):
        """Gets the metadata_signing_service of this PatchedrpmRpmRepository.  # noqa: E501

        A reference to an associated signing service.  # noqa: E501

        :return: The metadata_signing_service of this PatchedrpmRpmRepository.  # noqa: E501
        :rtype: str
        """
        return self._metadata_signing_service

    @metadata_signing_service.setter
    def metadata_signing_service(self, metadata_signing_service):
        """Sets the metadata_signing_service of this PatchedrpmRpmRepository.

        A reference to an associated signing service.  # noqa: E501

        :param metadata_signing_service: The metadata_signing_service of this PatchedrpmRpmRepository.  # noqa: E501
        :type: str
        """

        self._metadata_signing_service = metadata_signing_service

    @property
    def retain_package_versions(self):
        """Gets the retain_package_versions of this PatchedrpmRpmRepository.  # noqa: E501

        The number of versions of each package to keep in the repository; older versions will be purged. The default is '0', which will disable this feature and keep all versions of each package.  # noqa: E501

        :return: The retain_package_versions of this PatchedrpmRpmRepository.  # noqa: E501
        :rtype: int
        """
        return self._retain_package_versions

    @retain_package_versions.setter
    def retain_package_versions(self, retain_package_versions):
        """Sets the retain_package_versions of this PatchedrpmRpmRepository.

        The number of versions of each package to keep in the repository; older versions will be purged. The default is '0', which will disable this feature and keep all versions of each package.  # noqa: E501

        :param retain_package_versions: The retain_package_versions of this PatchedrpmRpmRepository.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                retain_package_versions is not None and retain_package_versions < 0):  # noqa: E501
            raise ValueError("Invalid value for `retain_package_versions`, must be a value greater than or equal to `0`")  # noqa: E501

        self._retain_package_versions = retain_package_versions

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PatchedrpmRpmRepository):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedrpmRpmRepository):
            return True

        return self.to_dict() != other.to_dict()
