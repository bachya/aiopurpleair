"""Define an API client."""
from typing import Any

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from aiopurpleair.const import LOGGER
from aiopurpleair.endpoint.keys import KeysEndpoints
from aiopurpleair.errors import raise_error

API_URL_BASE = "https://api.purpleair.com/v1"

DEFAULT_TIMEOUT = 10


class API:  # pylint: disable=too-few-public-methods
    """Define the API object."""

    def __init__(self, api_key: str, *, session: ClientSession | None = None) -> None:
        """Initialize.

        Args:
            api_key: A PurpleAir API key.
            session: An optional aiohttp ClientSession.
        """
        self._api_key = api_key
        self._session = session

        self.keys = KeysEndpoints(self.async_request)

    async def async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.
        """
        url: str = f"{API_URL_BASE}{endpoint}"

        kwargs.setdefault("headers", {})
        if self._api_key:
            kwargs["headers"]["X-API-Key"] = self._api_key

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        data: dict[str, Any] = {}

        try:
            async with session.request(method, url, **kwargs) as resp:
                data = await resp.json()
                raising_err = None

                try:
                    resp.raise_for_status()
                except ClientError as err:
                    raising_err = err

                raise_error(resp, data, raising_err)
        finally:
            if not use_running_session:
                await session.close()

        LOGGER.debug("Data received for %s: %s", endpoint, data)

        return data
