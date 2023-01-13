from typing import Any, Optional

from aiohttp import ClientError, ClientSession

from cheapshapi.exceptions import SharkException

URL = "https://apidocs.cheapshark.com/"


class SharkBase:
    def __init__(self, session: Optional[ClientSession] = None):
        self.base_url = URL
        self.session = session or ClientSession()

    async def _request(
        self,
        path: str,
        *,
        method: str,
        params: Optional[dict[str, Any]] = None,
        json=None,
        data=None,
    ):
        if not path.startswith("https://"):
            path = self.base_url + path
        try:
            async with self.session as session:
                async with session.request(method, url=path) as response:
                    text = await response.text()
                    print(text)
        except ClientError as exc:
            raise SharkException from exc
