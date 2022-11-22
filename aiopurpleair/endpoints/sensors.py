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
from aiopurpleair.util.geo import GeoLocation


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
        response: GetSensorsResponse = await self._async_endpoint_request_with_models(
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

    async def async_get_nearby_sensor_indices(
        self,
        latitude: float,
        longitude: float,
        distance_km: float,
        *,
        limit_results: int | None = None,
    ) -> list[int]:
        """Get sensor indices near a coordinate pair within a distance (in kilometers).

        The resulting list of indices is ordered from nearest to furthest within the
        bounding box defined by the distance.

        Args:
            latitude: The latitude of the "search center."
            longitude: The longitude of the "search center."
            distance_km: The radius of the "search center."
            limit_results: The number of results to limit.

        Returns:
            A sorted list of sensor indices.
        """
        center = GeoLocation.from_degrees(latitude, longitude)
        nw_coordinate_pair, se_coordinate_pair = center.bounding_box(distance_km)

        data = await self._async_request(
            "get",
            "/sensors",
            params={
                "fields": "latitude,longitude",
                "nwlat": nw_coordinate_pair.latitude_degrees,
                "nwlng": nw_coordinate_pair.longitude_degrees,
                "selat": se_coordinate_pair.latitude_degrees,
                "selng": se_coordinate_pair.longitude_degrees,
            },
        )

        results = [
            i[0]
            for i in sorted(
                (i for i in data["data"]),
                key=lambda i: center.distance_to(GeoLocation.from_degrees(i[1], i[2])),
            )
        ]

        if limit_results:
            return results[:limit_results]
        return results
