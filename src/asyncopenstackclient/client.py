import aiohttp
from simple_rest_client.api import API
from simple_rest_client.resource import AsyncResource
from urllib.parse import urlparse


class Client:

    def __init__(self, api_name, resources, session=None, api_url=None):
        self.api_name = api_name
        self.resources = resources
        self.session = session
        self._custom_api_url = api_url
        self._catalog_api_url = None
        self._current_api_url = None
        if self.session is None:
            raise AttributeError("provided session object is None, probably auth error?")

    async def init_api(self):
        await self.get_credentials()
        self.api = API(
            api_root_url=self.api_url,
            headers={'X-Auth-Token': self.session.token},
            json_encode_body=True
        )
        for resource in self.resources:
            self.api.add_resource(resource_name=resource, resource_class=AsyncResource)

    @property
    def api_url(self):
        api_url = self._custom_api_url or self._current_api_url or self._catalog_api_url
        if api_url and not api_url.endswith('/'):
            api_url += '/'
        return api_url

    async def get_current_version_api_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                versions = await response.json()
                return [version["links"][0]["href"] for version in versions["versions"] if version["status"] == "CURRENT"][0]

    async def get_credentials(self):
        await self.session.authenticate()

        # api_url is provided, don't bother to determine
        if self.api_url:
            return

        # take url from catalog
        url = self.session.get_endpoint_url(self.api_name)
        parts = urlparse(url)
        if parts.path:
            # preasumly full url with api or/and project id
            self._catalog_api_url = url
        else:
            # base url so we need to determine full url with version
            self._current_api_url = await self.get_current_version_api_url(url)
