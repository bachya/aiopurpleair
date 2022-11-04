"""Define tests for sensor models."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from aiopurpleair.model.sensors import GetSensorsRequest, LocationType


@pytest.mark.parametrize(
    "input_payload,output_payload",
    [
        (
            {
                "fields": ["name", "icon"],
            },
            {
                "fields": "name,icon",
                "max_age": 0,
            },
        ),
        (
            {
                "fields": ["name", "icon"],
                "location_type": LocationType.OUTSIDE,
            },
            {
                "fields": "name,icon",
                "location_type": 0,
                "max_age": 0,
            },
        ),
        (
            {
                "fields": ["name", "icon"],
                "location_type": LocationType.INSIDE,
            },
            {
                "fields": "name,icon",
                "location_type": 1,
                "max_age": 0,
            },
        ),
        (
            {
                "fields": ["name", "icon"],
                "location_type": LocationType.INSIDE,
                "read_keys": ["abc", "def"],
                "show_only": [123, 456],
                "modified_since": datetime(2022, 11, 3, 15, 46, 21),
                "max_age": 1200,
                "nwlng": -0.2416796,
                "nwlat": 51.5285582,
                "selng": -0.8876124,
                "selat": 54.7818162,
            },
            {
                "fields": "name,icon",
                "location_type": 1,
                "read_keys": "abc,def",
                "show_only": "123,456",
                "modified_since": 1667490381,
                "max_age": 1200,
                "nwlng": -0.2416796,
                "nwlat": 51.5285582,
                "selng": -0.8876124,
                "selat": 54.7818162,
            },
        ),
    ],
)
def test_get_sensors_request(
    input_payload: dict[str, Any], output_payload: dict[str, Any]
) -> None:
    """Test the GetSensorsRequest model.

    Args:
        input_payload: input_payload parameters for the model:
        output_payload: A parsed model dictionary output_payload.
    """
    request = GetSensorsRequest.parse_obj(input_payload)
    assert request.dict(exclude_none=True) == output_payload


@pytest.mark.parametrize(
    "payload,error_string",
    [
        (
            {
                "fields": ["name", "foobar"],
            },
            "foobar is an unknown field",
        ),
        (
            {
                "fields": ["name"],
                "nwlng": -0.2416796,
                "nwlat": -100.2416796,
                "selng": -0.8876124,
                "selat": 54.7818162,
            },
            "-100.2416796 is an invalid latitude",
        ),
        (
            {
                "fields": ["name"],
                "nwlng": -200.2416796,
                "nwlat": 51.5285582,
                "selng": -0.8876124,
                "selat": 54.7818162,
            },
            "-200.2416796 is an invalid longitude",
        ),
        (
            {
                "fields": ["name"],
                "nwlng": -0.2416796,
            },
            "must pass none or all of the bounding box coordinates",
        ),
    ],
)
def test_get_sensors_request_invalid_payload(
    error_string: str, payload: dict[str, Any]
) -> None:
    """Test inputting an invalid payload into the GetSensorsRequest model.

    Args:
        error_string: The error string that gets raised.
        payload: The payload to test.
    """
    with pytest.raises(ValidationError) as err:
        _ = GetSensorsRequest.parse_obj(payload)
    assert error_string in str(err.value)
