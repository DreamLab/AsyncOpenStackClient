import os
from aioresponses import aioresponses
from aiounittest import AsyncTestCase, futurized
from asyncopenstackclient import AuthPassword
from unittest.mock import patch


class TestAuth(AsyncTestCase):

    def setUp(self):
        self.auth_args = ('http://url', 'm_user', 'm_pass', 'm_project',
                          'm_user_domain', 'm_project_domain')
        self.auth = AuthPassword(*self.auth_args)

    def tearDown(self):
        patch.stopall()
        for name in list(os.environ.keys()):
            if name.startswith('OS_'):
                del os.environ[name]

    async def test_create_object(self):
        expected_payload = {'auth': {
            'identity': {'methods': ['password'], 'password': {'user': {
                'domain': {'name': 'm_user_domain'},
                'name': 'm_user', 'password': 'm_pass'
            }}},
            'scope': {'project': {'domain': {'name': 'm_project_domain'}, 'name': 'm_project'}}
        }}
        self.assertEqual(self.auth._auth_payload, expected_payload)
        self.assertEqual(self.auth._auth_endpoint, 'http://url/auth/tokens')
        self.assertTrue('Content-Type' in self.auth.headers)

    async def test_create_object_use_environ(self):
        expected_payload = {'auth': {
            'identity': {'methods': ['password'], 'password': {'user': {'domain': {'name': 'udm'}, 'name': 'uuu', 'password': 'ppp'}}},
            'scope': {'project': {'domain': {'name': 'udm'}, 'name': 'prj'}}
        }}
        env = {
            'OS_AUTH_URL': 'https://keystone/v3',
            'OS_PASSWORD': 'ppp', 'OS_USERNAME': 'uuu',
            'OS_USER_DOMAIN_NAME': 'udm', 'OS_PROJECT_NAME': 'prj'
        }

        with patch.dict('os.environ', env, clear=True):
            auth = AuthPassword()
        self.assertEqual(auth._auth_payload, expected_payload)
        self.assertEqual(auth._auth_endpoint, 'https://keystone/v3/auth/tokens')
        self.assertTrue('Content-Type' in auth.headers)

    async def test_get_token(self):
        body = {
            "token": {
                "catalog": {
                    "endpoints": [
                        {"name": "mock_endpoint", "endpoints": [{"url": "mock_url", "interface": "public"}]}
                    ]
                },
                "expires_at": "1970-01-01T01:00:00.000000Z"
            }
        }
        headers = {
            "Vary": "X-Auth-Token",
            "x-openstack-request-id": "1234",
            "Content-Type": "application/json",
            "X-Subject-Token": "gAAAAABao"
        }
        with aioresponses() as req:
            req.post('http://url/auth/tokens', payload=body, headers=headers)

            res = await self.auth.get_token()

            self.assertEqual(res, (headers["X-Subject-Token"], 3600, body["token"]["catalog"]))

    def test_get_endpoint_url_existing_endpoint(self):
        self.auth.endpoints = [
            {"name": "mock_endpoint", "endpoints": [{"url": "mock_url", "interface": "public"}]}
        ]

        endpoint_url = self.auth.get_endpoint_url("mock_endpoint")

        self.assertEqual(endpoint_url, "mock_url")

    def test_get_endpoint_url_bad_endpoint_name(self):
        self.auth.endpoints = [
            {"name": "mock_endpoint", "endpoints": [{"url": "mock_url", "interface": "public"}]}
        ]
        with self.assertRaises(ValueError):
            self.auth.get_endpoint_url("none_existing_endpoint")

    def test_get_endpoint_url_bad_interface(self):
        self.auth.endpoints = [
            {"name": "mock_endpoint", "endpoints": [{"url": "mock_url", "interface": "public"}]}
        ]
        with self.assertRaises(ValueError):
            self.auth.get_endpoint_url("mock_endpoint", prefered_interface="not_existing_interface")

    async def test_authenticate_first_time(self):

        mock_get_token_results = [
            futurized(('mock-token1', 1000, 'whatever')),
            futurized(('mock-token2', 1000, 'whatever')),
        ]

        # time is gonna be called 2 times becouse of Pythons lazy evaluation
        mock_time_results = [
            900,
            1100
        ]

        patch('asyncopenstackclient.auth.AuthPassword.get_token', side_effect=mock_get_token_results).start()
        patch('asyncopenstackclient.auth.time', side_effect=mock_time_results).start()

        # first time token should be None and get_token shall be called
        await self.auth.authenticate()
        self.assertEqual(self.auth.token, 'mock-token1')

        # second time, token is not None and current time is before token expiration, no change
        await self.auth.authenticate()
        self.assertEqual(self.auth.token, 'mock-token1')

        # third time, token expires and should be renewed
        await self.auth.authenticate()
        self.assertEqual(self.auth.token, 'mock-token2')
