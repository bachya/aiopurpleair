"""Define geographical util tests."""

import pytest

from aiopurpleair.util.geo import GeoLocation


@pytest.mark.parametrize(
    "latitude,longitude,distance_km,nw_latitude,nw_longitude,se_latitude,se_longitude",
    [
        (
            51.5285582,
            -0.2416796,
            5,
            51.57347,
            -0.31388,
            51.48364,
            -0.16948,
        ),
        (
            0.2,
            179.99999999999,
            500,
            4.6916,
            175.50837,
            -4.2916,
            -175.50837,
        ),
        (
            0.2,
            -179.99999999999,
            500,
            4.6916,
            175.50837,
            -4.2916,
            -175.50837,
        ),
        (
            89.9,
            0.2,
            500,
            90.0,
            -180.0,
            85.4084,
            180.0,
        ),
    ],
)
def test_geo_location_bounding_box(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    distance_km: float,
    latitude: float,
    longitude: float,
    nw_latitude: float,
    nw_longitude: float,
    se_latitude: float,
    se_longitude: float,
) -> None:
    """Test getting a 5km bounding box around London.

    Args:
        distance_km: The bounding box distance (in kilometers).
        latitude: The central latitude.
        longitude: The central longitude.
        nw_latitude: The latitude of the NW point.
        nw_longitude: The longitude of the NW point.
        se_latitude: The latitude of the SE point.
        se_longitude: The longitude of the SE point.
    """
    location = GeoLocation.from_degrees(latitude, longitude)
    nw_coordinate, se_coordinate = location.bounding_box(distance_km)
    # We round to prevent floating point errors in CI:
    assert round(nw_coordinate.latitude_degrees, 5) == nw_latitude
    assert round(nw_coordinate.longitude_degrees, 5) == nw_longitude
    assert round(se_coordinate.latitude_degrees, 5) == se_latitude
    assert round(se_coordinate.longitude_degrees, 5) == se_longitude


def test_geo_location_bounding_box_invalid_distance() -> None:
    """Test an error with an invalid bounding box distance."""
    location = GeoLocation.from_degrees(51.5285582, -0.2416796)
    with pytest.raises(ValueError) as err:
        _, _ = location.bounding_box(-1)
    assert "Cannot calculate a bounding box with negative distance" in str(err.value)


def test_geo_location_distance_to() -> None:
    """Test getting the distance between two GeoLocation objects."""
    london = GeoLocation.from_degrees(51.5285582, -0.2416796)
    liverpool = GeoLocation.from_degrees(53.4121569, -2.9860979)
    distance = london.distance_to(liverpool)
    assert distance == 280.31725082207095


def test_geo_location_from_degrees() -> None:
    """Test creating a GeoLocation object from a degrees-based latitude/longitude."""
    location = GeoLocation.from_degrees(51.5285582, -0.2416796)
    assert location.latitude_degrees == 51.5285582
    assert location.longitude_degrees == -0.2416796
    assert location.latitude_radians == 0.8993429993955228
    assert location.longitude_radians == -0.004218104754902888


def test_geo_location_from_radians() -> None:
    """Test creating a GeoLocation object from a radians-based latitude/longitude."""
    location = GeoLocation.from_radians(0.8993429993955228, -0.004218104754902888)
    assert location.latitude_degrees == 51.5285582
    assert location.longitude_degrees == -0.24167960000000002
    assert location.latitude_radians == 0.8993429993955228
    assert location.longitude_radians == -0.004218104754902888


def test_geo_location_invalid_coordinates() -> None:
    """Test an error with invalid coordinates."""
    with pytest.raises(ValueError) as err:
        _ = GeoLocation.from_degrees(97.0, -0.2416796)
    assert "Invalid latitude: 1.6929693744344996 radians" in str(err.value)
