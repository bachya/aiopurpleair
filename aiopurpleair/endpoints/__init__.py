"""Define API endpoints."""
from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable
from typing import Any

from pydantic import ValidationError

from aiopurpleair.errors import InvalidRequestError
from aiopurpleair.helpers.model import PurpleAirBaseModel, PurpleAirBaseModelT


class APIEndpointsBase:  # pylint: disable=too-few-public-methods
    """Define a base API endpoints manager."""

    def __init__(
        self, async_request: Callable[..., Awaitable[PurpleAirBaseModelT]]
    ) -> None:
        """Initialize.

        Args:
            async_request: The request method from the API object.
        """
        self._async_request = async_request

    async def _async_endpoint_request_with_models(
        self,
        endpoint: str,
        query_param_map: Iterable[tuple[str, Any]],
        request_model: type[PurpleAirBaseModel],
        response_model: type[PurpleAirBaseModel],
    ) -> PurpleAirBaseModelT:
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
        try:
            request = request_model.model_validate(
                {
                    api_query_param: func_param
                    for api_query_param, func_param in query_param_map
                    if func_param is not None
                }
            )
        except ValidationError as err:
            raise InvalidRequestError(err) from err

        return await self._async_request(
            "get",
            endpoint,
            response_model,
            params=request.model_dump(exclude_none=True),
        )
