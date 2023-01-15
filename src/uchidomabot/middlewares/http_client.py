from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from cheapshapi.client import CheapShark


class ClientMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, client):
        super().__init__()
        self.client = client

    async def pre_process(self, obj, data, *args):
        data["client"] = self.client

    async def post_process(self, obj, data, *args):
        del data["client"]
