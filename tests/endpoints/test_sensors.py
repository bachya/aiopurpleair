"""Define tests for sensor endpoints."""
from __future__ import annotations

import json
from datetime import datetime

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiopurpleair import API
from aiopurpleair.errors import InvalidRequestError
from aiopurpleair.models.sensors import LocationType
from tests.common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
async def test_get_sensors(aresponses: ResponsesMockServer) -> None:
    """Test the GET /sensors endpoint.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/sensors",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("get_sensors_response.json")), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        response = await api.sensors.async_get_sensors(
            fields=["name"], location_type=LocationType.OUTSIDE
        )
        assert response.api_version == "V1.0.11-0.0.41"
        assert response.time_stamp == datetime(2022, 11, 3, 19, 26, 29)
        assert response.data_time_stamp == datetime(2022, 11, 3, 19, 25, 31)
        assert response.firmware_default_version == "7.02"
        assert response.max_age == 604800
        assert response.channel_flags is None
        assert response.channel_states is None
        assert response.location_type is LocationType.OUTSIDE
        assert response.location_types is None
        assert response.fields == ["sensor_index", "name"]
        assert response.data == {
            131075: {
                "sensor_index": 131075,
                "name": "Mariners Bluff",
            },
            131079: {
                "sensor_index": 131079,
                "name": "BRSKBV-outside",
            },
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_sensors_validation_error(aresponses: ResponsesMockServer) -> None:
    """Test the GET /sensors endpoint, returning a validation error.

    Args:
        aresponses: An aresponses server.
    """
    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        with pytest.raises(InvalidRequestError) as err:
            _ = await api.sensors.async_get_sensors(["foobar"])
        assert "foobar is an unknown field" in str(err.value)

    aresponses.assert_plan_strictly_followed()
