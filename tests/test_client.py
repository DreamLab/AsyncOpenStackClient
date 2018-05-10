from aiounittest import AsyncTestCase, futurized
from asyncopenstackclient import Client
from unittest import mock


class TestClient(AsyncTestCase):

    def setUp(self):
        super().setUp()
        self.mock_sess = mock.Mock()
        self.mock_sess.authenticate.return_value = futurized(None)
        self.mock_sess.token = 'mock_token'
        self.mock_sess.get_endpoint_url.return_value = 'mock_url'

    def tearDown(self):
        mock.patch.stopall()

    def test_create_object(self):
        api_name = 'mock_api'
        resources = 'mock_resource'
        session = 'mock_session'
        client = Client(api_name, resources, session=session)

        self.assertEqual(client.api_name, api_name)
        self.assertEqual(client.resources, resources)
        self.assertEqual(client.session, session)

    def test_create_object_bad_session(self):
        with self.assertRaises(AttributeError):
            Client('mock_name', 'resource', session=None)

    async def test_get_credentials(self):
        self.mock_sess.get_endpoint_url.return_value = 'http://glance.a2.iaas:9292/v2'

        client = Client('glance', ['some_res'], session=self.mock_sess)

        # this is not a good practice but the simplest one
        client.get_current_version_api_url = mock.Mock(return_value=futurized('http://blah'))

        await client.get_credentials()

        client.get_current_version_api_url.assert_not_called()
        self.mock_sess.get_endpoint_url.assert_called_once_with('glance')
        self.assertEqual(client.api_url, 'http://glance.a2.iaas:9292/v2/')

    async def test_get_credentials_base_api_url_only_from_catalog(self):
        self.mock_sess.get_endpoint_url.return_value = 'http://glance.a2.iaas:9292'

        client = Client('glance', ['some_res'], session=self.mock_sess)

        # this is not a good practice but the simplest one
        client.get_current_version_api_url = mock.Mock(return_value=futurized('http://blah'))

        await client.get_credentials()

        self.mock_sess.get_endpoint_url.assert_called_once_with('glance')
        client.get_current_version_api_url.assert_called_once_with('http://glance.a2.iaas:9292')
        self.assertEqual(client.api_url, 'http://blah/')

    async def test_custom_api_url(self):
        client = Client('mock_name', 'some_res', session=self.mock_sess, api_url="http://my-api-url/")
        await client.get_credentials()

        self.mock_sess.get_endpoint_url.assert_not_called()
        self.assertEqual(client.api_url, 'http://my-api-url/')

    async def test_init_api(self):
        mock_api = mock.Mock()
        mock.patch('asyncopenstackclient.client.API', new_callable=mock_api).start()

        client = Client('mock_name', ['mock', 'resource', 'list'], session=self.mock_sess)
        await client.init_api()

        mock_api().assert_called_once_with(
            api_root_url='mock_url/',
            headers={'X-Auth-Token': 'mock_token'},
            json_encode_body=True
        )

        mock_api()().add_resource.assert_has_calls([
            mock.call(resource_name='mock', resource_class=mock.ANY),
            mock.call(resource_name='resource', resource_class=mock.ANY),
            mock.call(resource_name='list', resource_class=mock.ANY),
        ])
