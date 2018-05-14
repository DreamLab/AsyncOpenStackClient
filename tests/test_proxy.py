from aiounittest import AsyncTestCase, futurized
from asyncopenstackclient.proxy import ResourceProxy, MethodProxy
from unittest.mock import Mock, patch


class MockClass:

    def __init__(self, api='mock-api'):
        self.api = api

    def __getattr__(self, name):
        return ResourceProxy(self.api, name)


class TestClient(AsyncTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        patch.stopall()

    def test_pass_arguments_resource_proxy(self):
        res = ResourceProxy('mock-api', 'mock-resource')

        self.assertEqual(res.api, 'mock-api')
        self.assertEqual(res.resource_name, 'mock-resource')
        self.assertIsInstance(res.not_existing_property, MethodProxy)

    def test_resouce_proxy_return_method_proxy(self):
        mock_method_proxy = patch('asyncopenstackclient.proxy.MethodProxy').start()
        res = ResourceProxy('mock-api', 'mock-resource')
        res.mock_method()

        mock_method_proxy.assert_called_once_with('mock-api', 'mock-resource', 'mock_method')

    def test_resource_proxy_from_mock_class(self):
        mock_method_proxy = patch('asyncopenstackclient.proxy.MethodProxy').start()
        obj = MockClass()

        res = obj.servers.list()

        mock_method_proxy.assert_called_once_with('mock-api', 'servers', 'list')
        self.assertEqual(res, mock_method_proxy()())

    def test_pass_arguments_method_proxy(self):
        res = MethodProxy('mock-api', 'mock-resource', 'mock-method')

        self.assertEqual(res.api, 'mock-api')
        self.assertEqual(res.resource, 'mock-resource')
        self.assertEqual(res.method, 'mock-method')

    async def test_get_result_method_proxy(self):
        res_mock = Mock()
        res_mock.body = 'awesome_body'
        awaitable = futurized(res_mock)
        proxy = MethodProxy('api', 'resource', 'method')

        result = await proxy.get_result(awaitable)

        self.assertEqual(result, 'awesome_body')

    async def test_call_method_proxy_with_query_params(self):
        mock_args = ('a', 'b',)
        mock_kwargs = {'k1': 'v1'}
        mock_api = Mock()
        mock_api.servers = Mock()
        mock_api.servers.list = Mock()
        mock_res = Mock()
        mock_res.body = 'return_value'
        mock_api.servers.list.return_value = futurized(mock_res)
        mock_api.servers.actions = {'list': {'method': 'GET'}}

        obj = MockClass(api=mock_api)
        res = await obj.servers.list(*mock_args, **mock_kwargs)

        self.assertEqual(res, 'return_value')
        mock_api.servers.list.assert_called_once_with(*mock_args, params=mock_kwargs)

    async def test_call_method_proxy_with_body(self):
        mock_args = ('a', 'b',)
        mock_kwargs = {'k1': 'v1'}
        mock_api = Mock()
        mock_api.servers = Mock()
        mock_api.servers.create = Mock()
        mock_res = Mock()
        mock_res.body = 'return_value'
        mock_api.servers.create.return_value = futurized(mock_res)
        mock_api.servers.actions = {'create': {'method': 'POST'}}

        obj = MockClass(api=mock_api)
        res = await obj.servers.create(*mock_args, **mock_kwargs)

        self.assertEqual(res, 'return_value')
        mock_api.servers.create.assert_called_once_with(*mock_args, body=mock_kwargs)
