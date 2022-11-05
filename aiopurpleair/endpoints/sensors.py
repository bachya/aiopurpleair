"""Define an API endpoint for requests related to sensors."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any, cast

from pydantic import ValidationError

from aiopurpleair.errors import InvalidRequestError
from aiopurpleair.helpers.typing import ResponseModelT
from aiopurpleair.models.sensors import (
    GetSensorsRequest,
    GetSensorsResponse,
    LocationType,
)


class SensorsEndpoints:  # pylint: disable=too-few-public-methods
    """Define the API manager object."""

    def __init__(self, async_request: Callable[..., Awaitable[ResponseModelT]]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the API object.
        """
        self._async_request = async_request

    async def async_get_sensors(
        self,
        fields: list[str],
        *,
        location_type: LocationType | None = None,
        max_age: int | None = None,
        modified_since: datetime | None = None,
        read_keys: list[str] | None = None,
        sensor_indices: list[int] | None = None,
    ) -> GetSensorsResponse:
        """Get all sensors.

        Args:
            fields: The sensor data fields to include.
            location_type: An optional LocationType to filter by.
            max_age: Filter results modified within these seconds.
            modified_since: Filter results modified since a datetime.
            read_keys: Optional read keys for private sensors.
            sensor_indices: Filter results by sensor index.

        Returns:
            An API response payload in the form of a Pydantic model.

        Raises:
            InvalidRequestError: Raised on invalid parameters.
        """
        payload: dict[str, Any] = {"fields": fields}

        for api_query_param, func_param in (
            ("location_type", location_type),
            ("max_age", max_age),
            ("modified_since", modified_since),
            ("read_keys", read_keys),
            ("show_only", sensor_indices),
        ):
            if not func_param:
                continue
            payload[api_query_param] = func_param

        try:
            request = GetSensorsRequest.parse_obj(payload)
        except ValidationError as err:
            raise InvalidRequestError(err) from err

        response = await self._async_request(
            "get",
            "/sensors",
            GetSensorsResponse,
            params=request.dict(exclude_none=True),
        )
        return cast(GetSensorsResponse, response)
