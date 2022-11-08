"""Define various geographical utilities."""
from __future__ import annotations

import math
from dataclasses import dataclass

EARTH_RAIDUS_KM = 6378.1

MINIMUM_LATITUDE = math.radians(-90)
MAXIMUM_LATITUDE = math.radians(90)
MINIMUM_LONGITUDE = math.radians(-180)
MAXIMUM_LONGITUDE = math.radians(180)


@dataclass
class GeoLocation:
    """Define a representation of a single latitude/longitude coordinate.

    Inspiration from https://github.com/jfein/PyGeoTools/blob/master/geolocation.py.
    """

    latitude_radians: float
    longitude_radians: float
    latitude_degrees: float
    longitude_degrees: float

    def __post_init__(self) -> None:
        """Perform some post-init processing.

        Raises:
            ValueError: Raised upon invalid latitude/longitude.
        """
        for kind, value, minimum, maximum in (
            ("latitude", self.latitude_radians, MINIMUM_LATITUDE, MAXIMUM_LATITUDE),
            ("longitude", self.longitude_radians, MINIMUM_LONGITUDE, MAXIMUM_LONGITUDE),
        ):
            if value < minimum or value > maximum:
                raise ValueError(f"Invalid {kind}: {value} radians")

    @classmethod
    def from_degrees(
        cls, latitude_degrees: float, longitude_degrees: float
    ) -> GeoLocation:
        """Create a GeoLocation object from a latitude/longitude in degrees.

        Args:
            latitude_degrees: A latitude in degrees.
            longitude_degrees: A longitude in degrees.

        Returns:
            A GeoLocation object.
        """
        latitude_radians = math.radians(latitude_degrees)
        longitude_radians = math.radians(longitude_degrees)
        return cls(
            latitude_radians, longitude_radians, latitude_degrees, longitude_degrees
        )

    @classmethod
    def from_radians(
        cls, latitude_radians: float, longitude_radians: float
    ) -> GeoLocation:
        """Create a GeoLocation object from a latitude/longitude in radians.

        Args:
            latitude_radians: A latitude in radians.
            longitude_radians: A longitude in radians.

        Returns:
            A GeoLocation object.
        """
        latitude_degrees = math.degrees(latitude_radians)
        longitude_degrees = math.degrees(longitude_radians)
        return cls(
            latitude_radians, longitude_radians, latitude_degrees, longitude_degrees
        )

    def bounding_box(self, distance_km: float) -> tuple[GeoLocation, GeoLocation]:
        """Calculate a bounding box a certain distance from this GeoLocation.

        Args:
            distance_km: A distance (in kilometers).

        Returns:
            Two GeoLocation objects (representing the NW and SE corners of the box).

        Raises:
            ValueError: Raised on a negative distance_km parameter.
        """
        if distance_km < 0:
            raise ValueError("Cannot calculate a bounding box with negative distance")

        distance_radians = distance_km / EARTH_RAIDUS_KM
        box_minimum_latitude = self.latitude_radians - distance_radians
        box_maximum_latitude = self.latitude_radians + distance_radians

        if MINIMUM_LATITUDE < box_maximum_latitude < MAXIMUM_LATITUDE:
            delta_longitude = math.asin(
                math.sin(distance_radians) / math.cos(self.latitude_radians)
            )

            box_minimum_longitude = self.longitude_radians - delta_longitude
            if box_minimum_longitude < MINIMUM_LONGITUDE:
                box_minimum_longitude += 2 * math.pi

            box_maximum_longitude = self.longitude_radians + delta_longitude
            if box_maximum_longitude > MAXIMUM_LONGITUDE:
                box_maximum_longitude -= 2 * math.pi
        else:
            # One of the poles is within the bounding box:
            box_minimum_latitude = max(box_minimum_latitude, MINIMUM_LATITUDE)
            box_maximum_latitude = min(box_maximum_latitude, MAXIMUM_LATITUDE)
            box_minimum_longitude = MINIMUM_LONGITUDE
            box_maximum_longitude = MAXIMUM_LONGITUDE

        return (
            GeoLocation.from_radians(box_maximum_latitude, box_minimum_longitude),
            GeoLocation.from_radians(box_minimum_latitude, box_maximum_longitude),
        )

    def distance_to(self, endpoint: GeoLocation) -> float:
        """Calculate the great circle distance between this GeoLocation and another.

        Args:
            endpoint: The GeoLocation to which the distance should be measured.

        Returns:
            The distance between this GeoLocation and the endpoint GeoLocation.
        """
        return EARTH_RAIDUS_KM * math.acos(
            math.sin(self.latitude_radians) * math.sin(endpoint.latitude_radians)
            + math.cos(self.latitude_radians)
            * math.cos(endpoint.latitude_radians)
            * math.cos(self.longitude_radians - endpoint.longitude_radians)
        )
