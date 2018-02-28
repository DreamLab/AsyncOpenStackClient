import logging
from simple_rest_client.api import API
from simple_rest_client.resource import AsyncResource


class Client:

    def __init__(self, api_name, resources, api_version=None, session=None):
        self.api_version = api_version or '2.26'
        self.api_name = api_name
        self.resources = resources
        self.session = session
        if self.session is None:
            logging.error("provided session object is None, probably auth error?")
            raise AttributeError()

    async def init_api(self):
        await self.get_credentials()
        self.api = API(
            api_root_url=self.api_url,
            headers={'X-Auth-Token': self.session.token},
            json_encode_body=True
        )
        for resource in self.resources:
            self.api.add_resource(resource_name=resource, resource_class=AsyncResource)

    async def get_credentials(self):
        await self.session.authenticate()
        self.api_url = await self.session.get_ednpoint_url(self.api_name)
