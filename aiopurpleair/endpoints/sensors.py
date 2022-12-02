"""Define an API endpoint for requests related to sensors."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import cast

from aiopurpleair.endpoints import APIEndpointsBase
from aiopurpleair.models.sensors import (
    GetSensorRequest,
    GetSensorResponse,
    GetSensorsRequest,
    GetSensorsResponse,
    LocationType,
    SensorModel,
)
from aiopurpleair.util.geo import GeoLocation


@dataclass
class NearbySensorResult:
    """Define a nearby sensor result."""

    sensor: SensorModel
    distance: float


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
        response: GetSensorResponse = await self._async_endpoint_request_with_models(
            f"/sensors/{sensor_index}",
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
        nw_latitude: float | None = None,
        nw_longitude: float | None = None,
        read_keys: list[str] | None = None,
        se_latitude: float | None = None,
        se_longitude: float | None = None,
        sensor_indices: list[int] | None = None,
    ) -> GetSensorsResponse:
        """Get all sensors.

        Args:
            fields: The sensor data fields to include.
            location_type: An optional LocationType to filter by.
            max_age: Filter results modified within these seconds.
            modified_since_utc: Filter results modified since a datetime.
            nw_latitude: The latitude of the NE corner of an optional bounding box.
            nw_longitude: The longitude of the NE corner of an optional bounding box.
            read_keys: Optional read keys for private sensors.
            se_latitude: The latitude of the SE corner of an optional bounding box.
            se_longitude: The longitude of the SE corner of an optional bounding box.
            sensor_indices: Filter results by sensor index.

        Returns:
            An API response payload in the form of a Pydantic model.
        """
        response: GetSensorsResponse = await self._async_endpoint_request_with_models(
            "/sensors",
            (
                ("fields", fields),
                ("location_type", location_type),
                ("max_age", max_age),
                ("modified_since", modified_since_utc),
                ("nwlat", nw_latitude),
                ("nwlng", nw_longitude),
                ("read_keys", read_keys),
                ("selat", se_latitude),
                ("selng", se_longitude),
                ("show_only", sensor_indices),
            ),
            GetSensorsRequest,
            GetSensorsResponse,
        )
        return response

    async def async_get_nearby_sensors(
        self,
        fields: list[str],
        latitude: float,
        longitude: float,
        distance_km: float,
        *,
        limit_results: int | None = None,
    ) -> list[NearbySensorResult]:
        """Get sensors near a coordinate pair within a distance (in kilometers).

        The resulting list of sensors is ordered from nearest to furthest within the
        bounding box defined by the distance.

        Args:
            fields: The sensor data fields to include.
            latitude: The latitude of the "search center."
            longitude: The longitude of the "search center."
            distance_km: The radius of the "search center."
            limit_results: The number of results to limit.

        Returns:
            A sorted list of NearbySensorResult objects (containing both the sensor and
                the distance).
        """
        center = GeoLocation.from_degrees(latitude, longitude)
        nw_coordinate_pair, se_coordinate_pair = center.bounding_box(distance_km)

        # Ensure that latitude and longitude are included in the fields no matter what:
        fields.extend(
            field for field in ("latitude", "longitude") if field not in fields
        )

        sensors_response = await self.async_get_sensors(
            fields,
            nw_latitude=nw_coordinate_pair.latitude_degrees,
            nw_longitude=nw_coordinate_pair.longitude_degrees,
            se_latitude=se_coordinate_pair.latitude_degrees,
            se_longitude=se_coordinate_pair.longitude_degrees,
        )

        nearby_results = [
            NearbySensorResult(
                sensor=sensor,
                distance=center.distance_to(
                    GeoLocation.from_degrees(
                        cast(float, sensor.latitude), cast(float, sensor.longitude)
                    )
                ),
            )
            for sensor in list(sensors_response.data.values())
        ]

        sorted_results = sorted(nearby_results, key=lambda result: result.distance)

        if limit_results:
            return sorted_results[:limit_results]
        return sorted_results
