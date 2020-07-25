# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.inline_response2005 import InlineResponse2005  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestInlineResponse2005(unittest.TestCase):
    """InlineResponse2005 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2005
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.inline_response2005.InlineResponse2005()  # noqa: E501
        if include_optional :
            return InlineResponse2005(
                count = 123, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_rpm.models.rpm/package_environment_response.rpm.PackageEnvironmentResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        id = '0', 
                        name = '0', 
                        description = '0', 
                        display_order = 56, 
                        group_ids = pulpcore.client.pulp_rpm.models.group_ids.group_ids(), 
                        option_ids = pulpcore.client.pulp_rpm.models.option_ids.option_ids(), 
                        desc_by_lang = pulpcore.client.pulp_rpm.models.desc_by_lang.desc_by_lang(), 
                        name_by_lang = pulpcore.client.pulp_rpm.models.name_by_lang.name_by_lang(), 
                        digest = '0', )
                    ]
            )
        else :
            return InlineResponse2005(
        )

    def testInlineResponse2005(self):
        """Test InlineResponse2005"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
