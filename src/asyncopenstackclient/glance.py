import aiohttp
from .client import Client


class GlanceClient(Client):
    def __init__(self, api_version=None, session=None):
        super().__init__('glance', ['images'], api_version, session)

    async def get_api_url_with_version(self, glance_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(glance_url) as response:
                versions = await response.json()
                return [version["links"][0]["href"] for version in versions["versions"] if version["status"] == "CURRENT"][0]

    async def get_credentials(self):
        await super().get_credentials()
        self.api_url = await self.get_api_url_with_version(self.api_url)
