from typing import Any, Optional, TypeVar

from aiohttp import ClientError, ClientSession, ClientResponse
from yarl import URL

from cheapshapi.exceptions import SharkException

BASE_URL = "https://www.cheapshark.com/api/1.0/"

from pprint import pprint


class SharkBase:
    def __init__(self, session: Optional[ClientSession] = None):
        self.base_url = BASE_URL
        self.session = session or ClientSession()

    async def _request(
        self,
        path: str,
        *,
        fabric: Any,
        method: str,
        params: Optional[dict[str, Any]] = None,
        json=None,
        data=None,
        headers=None
    ) -> Any:
        if not path.startswith("https://"):
            path = self.base_url + path
        try:
            # async with self.session as session:
            async with self.session.request(
                method=method,
                url=URL(path, encoded=True),
                json=json,
                data=data,
                params=params,
                headers=headers,
            ) as response:
                if fabric != Any:
                    resp_json = await response.json()
                    if isinstance(resp_json, list):
                        return fabric(resp_json)
                    return fabric.parse_obj(resp_json)
                return response.status
        except ClientError as exc:
            raise SharkException from exc
