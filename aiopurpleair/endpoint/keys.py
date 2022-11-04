"""Define API endpoint management for keys-related endpoints."""
from collections.abc import Awaitable, Callable
from typing import Any


class KeysEndpoints:  # pylint: disable=too-few-public-methods
    """Define an API manager for keys-related endpoints."""

    def __init__(self, async_request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def async_check_api_key(self) -> dict[str, Any]:
        """Check the validity of the API key.

        Returns:
            An API response payload.
        """
        return await self._async_request("get", "/keys")
