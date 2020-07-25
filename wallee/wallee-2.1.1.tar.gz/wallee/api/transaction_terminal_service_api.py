# coding: utf-8

from __future__ import absolute_import

import six

from wallee.api_client import ApiClient

class TransactionTerminalServiceApi:

    def __init__(self, configuration):
        self.api_client = ApiClient(configuration=configuration)

    def receipt(self, space_id, transaction_id, type_id, width, **kwargs):
        """getTerminalReceipt

        Returns the PDF document for the requested terminal receipt with the given page width.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.receipt(space_id, transaction_id, type_id, width, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param int transaction_id: The ID of the transaction to get the receipt for. (required)
        :param int type_id:  (required)
        :param int width:  (required)
        :return: RenderedTerminalReceipt
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.receipt_with_http_info(space_id, transaction_id, type_id, width, **kwargs)
        else:
            (data) = self.receipt_with_http_info(space_id, transaction_id, type_id, width, **kwargs)
            return data

    def receipt_with_http_info(self, space_id, transaction_id, type_id, width, **kwargs):
        """getTerminalReceipt

        Returns the PDF document for the requested terminal receipt with the given page width.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.receipt_with_http_info(space_id, transaction_id, type_id, width, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param int transaction_id: The ID of the transaction to get the receipt for. (required)
        :param int type_id:  (required)
        :param int width:  (required)
        :return: RenderedTerminalReceipt
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_id', 'transaction_id', 'type_id', 'width']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method receipt" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_id' is set
        if ('space_id' not in params or
                params['space_id'] is None):
            raise ValueError("Missing the required parameter `space_id` when calling `receipt`")
        # verify the required parameter 'transaction_id' is set
        if ('transaction_id' not in params or
                params['transaction_id'] is None):
            raise ValueError("Missing the required parameter `transaction_id` when calling `receipt`")
        # verify the required parameter 'type_id' is set
        if ('type_id' not in params or
                params['type_id'] is None):
            raise ValueError("Missing the required parameter `type_id` when calling `receipt`")
        # verify the required parameter 'width' is set
        if ('width' not in params or
                params['width'] is None):
            raise ValueError("Missing the required parameter `width` when calling `receipt`")

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'space_id' in params:
            query_params.append(('spaceId', params['space_id']))
        if 'transaction_id' in params:
            query_params.append(('transactionId', params['transaction_id']))
        if 'type_id' in params:
            query_params.append(('typeId', params['type_id']))
        if 'width' in params:
            query_params.append(('width', params['width']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json;charset=utf-8'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(
            ['*/*'])

        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(
            '/transaction-terminal/receipt', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RenderedTerminalReceipt',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def till_connection_credentials(self, space_id, transaction_id, terminal_id, **kwargs):
        """Create Till Connection Credentials

        This operation creates a set of credentials to use within the WebSocket.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.till_connection_credentials(space_id, transaction_id, terminal_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param int transaction_id: The ID of the transaction which is used to process with the terminal. (required)
        :param int terminal_id: The ID of the terminal which should be used to process the transaction. (required)
        :param str language: The language in which the messages should be rendered in.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.till_connection_credentials_with_http_info(space_id, transaction_id, terminal_id, **kwargs)
        else:
            (data) = self.till_connection_credentials_with_http_info(space_id, transaction_id, terminal_id, **kwargs)
            return data

    def till_connection_credentials_with_http_info(self, space_id, transaction_id, terminal_id, **kwargs):
        """Create Till Connection Credentials

        This operation creates a set of credentials to use within the WebSocket.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.till_connection_credentials_with_http_info(space_id, transaction_id, terminal_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int space_id:  (required)
        :param int transaction_id: The ID of the transaction which is used to process with the terminal. (required)
        :param int terminal_id: The ID of the terminal which should be used to process the transaction. (required)
        :param str language: The language in which the messages should be rendered in.
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['space_id', 'transaction_id', 'terminal_id', 'language']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method till_connection_credentials" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'space_id' is set
        if ('space_id' not in params or
                params['space_id'] is None):
            raise ValueError("Missing the required parameter `space_id` when calling `till_connection_credentials`")
        # verify the required parameter 'transaction_id' is set
        if ('transaction_id' not in params or
                params['transaction_id'] is None):
            raise ValueError("Missing the required parameter `transaction_id` when calling `till_connection_credentials`")
        # verify the required parameter 'terminal_id' is set
        if ('terminal_id' not in params or
                params['terminal_id'] is None):
            raise ValueError("Missing the required parameter `terminal_id` when calling `till_connection_credentials`")

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'space_id' in params:
            query_params.append(('spaceId', params['space_id']))
        if 'transaction_id' in params:
            query_params.append(('transactionId', params['transaction_id']))
        if 'terminal_id' in params:
            query_params.append(('terminalId', params['terminal_id']))
        if 'language' in params:
            query_params.append(('language', params['language']))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []

        return self.api_client.call_api(
            '/transaction-terminal/till-connection-credentials', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
