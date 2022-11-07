"""Define an API endpoint for requests related to sensors."""
from __future__ import annotations

from datetime import datetime

from aiopurpleair.endpoints import APIEndpointsBase
from aiopurpleair.models.sensors import (
    GetSensorRequest,
    GetSensorResponse,
    GetSensorsRequest,
    GetSensorsResponse,
    LocationType,
)


class SensorsEndpoints(APIEndpointsBase):
    """Define the API manager object."""

    async def async_get_sensor(
        self,
        sensor_index: int,
        *,
        fields: list[str] | None = None,
        read_key: str | None = None,
    ) -> GetSensorResponse:
        """Get all sensors.

        Args:
            sensor_index: The sensor index to get data for.
            fields: The optional sensor data fields to include.
            read_key: An optional read key for private sensors.

        Returns:
            An API response payload in the form of a Pydantic model.
        """
        response: GetSensorResponse = await self._async_endpoint_request(
            f"/sensor/{sensor_index}",
            (
                ("fields", fields),
                ("read_key", read_key),
            ),
            GetSensorRequest,
            GetSensorResponse,
        )
        return response

    async def async_get_sensors(
        self,
        fields: list[str],
        *,
        location_type: LocationType | None = None,
        max_age: int | None = None,
        modified_since_utc: datetime | None = None,
        read_keys: list[str] | None = None,
        sensor_indices: list[int] | None = None,
    ) -> GetSensorsResponse:
        """Get all sensors.

        Args:
            fields: The sensor data fields to include.
            location_type: An optional LocationType to filter by.
            max_age: Filter results modified within these seconds.
            modified_since_utc: Filter results modified since a datetime.
            read_keys: Optional read keys for private sensors.
            sensor_indices: Filter results by sensor index.

        Returns:
            An API response payload in the form of a Pydantic model.
        """
        response: GetSensorsResponse = await self._async_endpoint_request(
            "/sensors",
            (
                ("fields", fields),
                ("location_type", location_type),
                ("max_age", max_age),
                ("modified_since", modified_since_utc),
                ("read_keys", read_keys),
                ("show_only", sensor_indices),
            ),
            GetSensorsRequest,
            GetSensorsResponse,
        )
        return response
