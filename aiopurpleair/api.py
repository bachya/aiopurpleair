"""Define an API client."""
from __future__ import annotations

from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel, ValidationError

from aiopurpleair.const import LOGGER
from aiopurpleair.endpoints.sensors import SensorsEndpoints
from aiopurpleair.errors import RequestError, raise_error
from aiopurpleair.helpers.typing import ModelT
from aiopurpleair.models.keys import GetKeysResponse

API_URL_BASE = "https://api.purpleair.com/v1"

DEFAULT_TIMEOUT = 10

MAP_URL_BASE = "https://map.purpleair.com/1/mAQI/a10/p604800/cC0"


class API:
    """Define the API object."""

    def __init__(
        self,
        api_key: str,
        *,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize.

        Args:
            api_key: A PurpleAir API key.
            session: An optional aiohttp ClientSession.
        """
        self._api_key = api_key
        self._session = session

        self.sensors = SensorsEndpoints(self.async_request)

    async def async_check_api_key(self) -> GetKeysResponse:
        """Check the validity of the API key.

        Returns:
            An API response payload.
        """
        return await self.async_request("get", "/keys", GetKeysResponse)

    async def async_request(
        self,
        method: str,
        endpoint: str,
        response_model: type[BaseModel],
        **kwargs: dict[str, Any],
    ) -> ModelT:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            response_model: A Pydantic model to parse the response data with.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload in the form of a Pydantic model.

        Raises:
            RequestError: Raised when response data can't be validated.
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

        try:
            return cast(ModelT, response_model.parse_obj(data))
        except ValidationError as err:
            raise RequestError(
                f"Error while parsing response from {endpoint}: {err}"
            ) from err

    def get_map_url(self, sensor_index: int) -> str:
        """Get the map URL for a sensor index.

        Args:
            sensor_index: The sensor index to get the map URL for.

        Returns:
            A MAP URL.
        """
        return f"{MAP_URL_BASE}?select={sensor_index}"
