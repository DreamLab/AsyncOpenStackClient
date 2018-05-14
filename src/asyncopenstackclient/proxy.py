class ResourceProxy:

    def __init__(self, api, resource_name):
        self.resource_name = resource_name
        self.api = api

    def __getattr__(self, name):
        return MethodProxy(self.api, self.resource_name, name)


class MethodProxy:

    def __init__(self, api, resource, method):
        self.api = api
        self.resource = resource
        self.method = method

    def __call__(self, *args, **kwargs):
        resource = getattr(self.api, self.resource)
        method = getattr(resource, self.method)
        if resource.actions[self.method]['method'] in ('GET',):
            return self.get_result(method(*args, params=kwargs))
        else:
            return self.get_result(method(*args, body=kwargs))

    async def get_result(self, method_awaitable):
        result = await method_awaitable
        return result.body
