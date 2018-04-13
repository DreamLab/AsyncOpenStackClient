from .client import Client


class GlanceClient(Client):
    def __init__(self, session=None, api_url=None):
        super().__init__('glance', ['images'], session, api_url)
