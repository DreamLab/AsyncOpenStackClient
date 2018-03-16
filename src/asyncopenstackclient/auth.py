from time import time, strptime, mktime
import aiohttp


class AuthModel:

    async def authenticate(self):
        raise NotImplementedError()

    def verify(self):
        return self.token_expires_at - time() < 3600


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

    async def get_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.auth_url, json=self.auth_dict, headers=self.headers) as response:
                result = await response.json()
                return (
                    response.headers['X-Subject-Token'],
                    mktime(strptime(result['token']['expires_at'], "%Y-%m-%dT%H:%M:%S.000000Z")),
                    result['token']['catalog']
                )

    def get_endpoint_url(self, endpoint_name, prefered_interface="public"):
        try:
            for endpoint in self.endpoints:
                if endpoint['name'] == endpoint_name:
                    return [url['url'] for url in endpoint['endpoints'] if url['interface'] == prefered_interface][0]
        except IndexError:
            raise ValueError("could not find desired interface")
        raise ValueError("endpoint %s not found" % endpoint_name)

    async def authenticate(self):
        if self.token is None or self.token_expires_at - time() < 0:
            self.token, self.token_expires_at, self.endpoints = await self.get_token()
