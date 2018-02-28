from time import time, strptime, mktime
import aiohttp


class AuthModel:

    async def authenticate(self):
        raise NotImplementedError()


class AuthPassword:

    def __init__(self, auth_url, username, password, project_name, user_domain_name, project_domain_name):
        self.auth_url = auth_url + '/auth/tokens'
        self.token = None
        self.token_expires_at = 0
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.auth_dict = {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'domain': {
                                'name': user_domain_name
                            },
                            'name': username,
                            'password': password
                        }
                    }
                },
                'scope': {
                    "project": {
                        "domain": {
                            "name": project_domain_name
                        },
                        "name": project_name
                    }
                }
            }
        }

    def verify(self):
        return self.token_expires_at - time() < 3600

    async def get_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.auth_url, json=self.auth_dict, headers=self.headers) as response:
                result = await response.json()
                return (
                    response.headers['X-Subject-Token'], mktime(strptime(result['token']['expires_at'],
                    "%Y-%m-%dT%H:%M:%S.000000Z")), result['token']['catalog']
                )

    async def get_ednpoint_url(self, endpoint_name):
        for endpoint in self.endpoints:
            if endpoint['name'] == endpoint_name:
                return endpoint['endpoints'][0]['url']

    async def authenticate(self):
        if self.token is None or self.token_expires_at - time() > 0:
            self.token, self.token_expires_at, self.endpoints = await self.get_token()
