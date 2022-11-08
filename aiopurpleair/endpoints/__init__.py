"""Define API endpoints."""
from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from typing import Any

from pydantic import BaseModel, ValidationError

from aiopurpleair.errors import InvalidRequestError
from aiopurpleair.helpers.typing import ModelT


class APIEndpointsBase:  # pylint: disable=too-few-public-methods
    """Define a base API endpoints manager."""

    def __init__(
        self,
        async_request: Callable[..., Awaitable[dict[str, Any]]],
        async_request_with_response_model: Callable[..., Awaitable[ModelT]],
    ) -> None:
        """Initialize.

        Args:
            async_request: The request method that returns raw JSON.
            async_request_with_response_model: The request method that returns a
                Pydantic model.
        """
        self._async_request = async_request
        self._async_request_with_response_model = async_request_with_response_model

    async def _async_endpoint_request_with_models(
        self,
        endpoint: str,
        query_param_map: Iterable[tuple[str, Any]],
        request_model: type[BaseModel],
        response_model: type[BaseModel],
    ) -> ModelT:
        """Perform an API endpoint request.

        Args:
            endpoint: The API endpoint to query.
            query_param_map: A tuple of API query parameters to include (if they exist).
            request_model: The Pydantic model for the request.
            response_model: The Pydantic model for the response.

        Returns:
            An API response payload in the form of a Pydantic model.

        Raises:
            InvalidRequestError: Raised on invalid parameters.
        """
        payload: dict[str, Any] = {}

        for api_query_param, func_param in query_param_map:
            if not func_param:
                continue
            payload[api_query_param] = func_param

        try:
            request = request_model.parse_obj(payload)
        except ValidationError as err:
            raise InvalidRequestError(err) from err

        return await self._async_request_with_response_model(
            "get", endpoint, response_model, params=request.dict(exclude_none=True)
        )
