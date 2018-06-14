from .client import Client


class CinderClient(Client):
    def __init__(self, session=None, api_url=None):
        super().__init__('cinder', ['volumes'], session, api_url)

    async def init_api(self, timeout=60):
        await super().init_api(timeout)
        self.api.volumes.actions["force_delete"] = {"method": "DELETE", "url": "volumes/{}"}
        self.api.volumes.actions["get"] = {"method": "GET", "url": "volumes/{}"}
        self.api.volumes.actions["list"] = {"method": "GET", "url": "volumes/detail"}
        self.api.volumes.add_action("force_delete")
        self.api.volumes.add_action("get")
