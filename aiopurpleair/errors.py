"""Define package exceptions."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientResponse
from aiohttp.client_exceptions import ClientError


class PurpleAirError(Exception):
    """Define a base exception."""

    pass


class NotFoundError(PurpleAirError):
    """Define an unknown resource."""

    pass


class InvalidRequestError(PurpleAirError):
    """Define an invalid request."""

    pass


class RequestError(PurpleAirError):
    """Define a general HTTP request error."""

    pass


class InvalidApiKeyError(RequestError):
    """Define a base exception."""

    pass


ERROR_CODE_MAP = {
    "ApiKeyMissingError": InvalidApiKeyError,
    "ApiKeyInvalidError": InvalidApiKeyError,
    "NotFoundError": NotFoundError,
}


def raise_error(
    resp: ClientResponse, payload: dict[str, Any], raising_err: ClientError | None
) -> None:
    """Raise the appropriate error based on the response data.

    Args:
        resp: An aiohttp ClientResponse.
        payload: An API response payload.
        raising_err: The aiohttp ClientError that caused the overall issue.

    Raises:
        exc: Raised upon an HTTP error.
    """
    if (error_code := payload.get("error")) is None:
        return

    exc = ERROR_CODE_MAP.get(error_code, RequestError)
    exc.__cause__ = raising_err
    raise exc(f"Error while querying {resp.url}: {payload['description']}")
