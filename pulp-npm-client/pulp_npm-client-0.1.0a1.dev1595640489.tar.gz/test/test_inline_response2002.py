# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_npm
from pulpcore.client.pulp_npm.models.inline_response2002 import InlineResponse2002  # noqa: E501
from pulpcore.client.pulp_npm.rest import ApiException

class TestInlineResponse2002(unittest.TestCase):
    """InlineResponse2002 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2002
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_npm.models.inline_response2002.InlineResponse2002()  # noqa: E501
        if include_optional :
            return InlineResponse2002(
                count = 56, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_npm.models.npm/npm_remote.npm.NpmRemote(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        name = '0', 
                        url = '0', 
                        ca_cert = '0', 
                        client_cert = '0', 
                        client_key = '0', 
                        tls_validation = True, 
                        proxy_url = '0', 
                        username = '0', 
                        password = '0', 
                        pulp_last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        download_concurrency = 1, 
                        policy = 'immediate', )
                    ]
            )
        else :
            return InlineResponse2002(
                count = 56,
                results = [
                    pulpcore.client.pulp_npm.models.npm/npm_remote.npm.NpmRemote(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        name = '0', 
                        url = '0', 
                        ca_cert = '0', 
                        client_cert = '0', 
                        client_key = '0', 
                        tls_validation = True, 
                        proxy_url = '0', 
                        username = '0', 
                        password = '0', 
                        pulp_last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        download_concurrency = 1, 
                        policy = 'immediate', )
                    ],
        )

    def testInlineResponse2002(self):
        """Test InlineResponse2002"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
