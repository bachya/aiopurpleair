"""Define geographical util tests."""
from aiopurpleair.util.geo import GeoLocation


def test_geo_location_bounding_box() -> None:
    """Test getting a 5km bounding box around Londo."""
    london = GeoLocation.from_degrees(51.5285582, -0.2416796)
    nw_coordinate, se_coordinate = london.bounding_box(5)
    assert nw_coordinate.latitude_degrees == 51.57347422476684
    assert nw_coordinate.longitude_degrees == -0.3138774212931301
    assert se_coordinate.latitude_degrees == 51.48364217523316
    assert se_coordinate.longitude_degrees == -0.1694817787068699


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


def test_geo_location_distance_to() -> None:
    """Test getting the distance between two GeoLocation objects."""
    london = GeoLocation.from_degrees(51.5285582, -0.2416796)
    liverpool = GeoLocation.from_degrees(53.4121569, -2.9860979)
    distance = london.distance_to(liverpool)
    assert distance == 280.31725082207095
