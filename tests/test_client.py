from aiounittest import AsyncTestCase, futurized
from asyncopenstackclient import Client
from unittest import mock


class TestClient(AsyncTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        mock.patch.stopall()

    def test_create_object(self):
        api_name = 'mock_api'
        resources = 'mock_resource'
        api_version = 'mock_api_version'
        session = 'mock_session'
        client = Client(api_name, resources, api_version=api_version, session=session)

        self.assertEqual(client.api_name, api_name)
        self.assertEqual(client.api_version, api_version)
        self.assertEqual(client.resources, resources)
        self.assertEqual(client.session, session)

    def test_create_object_bad_session(self):
        with self.assertRaises(AttributeError):
            Client('mock_name', 'mock_version', session=None)

    async def test_get_credentials(self):
        session = mock.Mock()
        session.authenticate.return_value = futurized(None)
        session.get_endpoint_url.return_value = "mock_url"

        client = Client("mock_name", "mock_version", session=session)
        await client.get_credentials()

        self.assertEqual(client.api_url, "mock_url")

    async def test_init_api(self):
        session = mock.Mock()
        session.authenticate.return_value = futurized(None)
        session.get_endpoint_url.return_value = "mock_url"
        session.token = 'mock_token'
        mock_api = mock.Mock()

        mock.patch('asyncopenstackclient.client.API', new_callable=mock_api).start()

        client = Client("mock_name", ['mock', 'resource', 'list'], session=session)
        await client.init_api()

        mock_api().assert_called_once_with(
            api_root_url="mock_url",
            headers={"X-Auth-Token": 'mock_token'},
            json_encode_body=True
        )

        mock_api()().add_resource.assert_has_calls([
            mock.call(resource_name='mock', resource_class=mock.ANY),
            mock.call(resource_name='resource', resource_class=mock.ANY),
            mock.call(resource_name='list', resource_class=mock.ANY),
        ])
