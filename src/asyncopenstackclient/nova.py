from .client import Client


class NovaClient(Client):
    def __init__(self, session=None, api_url=None):
        super().__init__('nova', ['flavors', 'servers', 'metadata'], session, api_url)

    async def init_api(self, timeout=60):
        await super().init_api(timeout)
        self.api.servers.actions["force_delete"] = {"method": "DELETE", "url": "servers/{}"}
        self.api.servers.actions["get"] = {"method": "GET", "url": "servers/{}"}
        self.api.servers.actions["list"] = {"method": "GET", "url": "servers/detail"}
        self.api.servers.actions["run_action"] = {"method": "POST", "url": "servers/{}/action"}
        self.api.servers.add_action("force_delete")
        self.api.servers.add_action("get")
        self.api.servers.add_action("run_action")
        self.api.flavors.actions["list"] = {"method": "GET", "url": "flavors/detail"}
        self.api.metadata.actions['get'] = {"method": "GET", "url": "servers/{}/metadata"}
        self.api.metadata.actions['set'] = {"method": "POST", "url": "servers/{}/metadata"}
        self.api.metadata.actions['get_item'] = {"method": "GET", "url": "servers/{}/metadata/{}"}
        self.api.metadata.actions['set_item'] = {"method": "PUT", "url": "servers/{}/metadata/{}"}
        self.api.metadata.add_action("set_item")
        self.api.metadata.add_action("get_item")
        self.api.metadata.add_action("get")
        self.api.metadata.add_action("set")
