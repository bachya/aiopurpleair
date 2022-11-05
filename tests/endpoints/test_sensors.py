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
async def test_get_sensor(aresponses: ResponsesMockServer) -> None:
    """Test the GET /sensor/:sensor_index endpoint.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/sensor/12345",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("get_sensor_response.json")), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        response = await api.sensors.async_get_sensor(12345)
        assert response.api_version == "V1.0.11-0.0.41"
        assert response.time_stamp == datetime(2022, 11, 5, 16, 37, 3)
        assert response.data_time_stamp == datetime(2022, 11, 5, 16, 36, 21)
        assert response.sensor == {
            "sensor_index": 131075,
            "last_modified": 1635632829,
            "date_created": 1632955574,
            "last_seen": 1667666162,
            "private": 0,
            "is_owner": 0,
            "name": "Mariners Bluff",
            "icon": 0,
            "location_type": 0,
            "model": "PA-II",
            "hardware": "2.0+BME280+PMSX003-B+PMSX003-A",
            "led_brightness": 35,
            "firmware_version": "7.02",
            "rssi": -67,
            "uptime": 15682,
            "pa_latency": 992,
            "memory": 16008,
            "position_rating": 5,
            "latitude": 33.51511,
            "longitude": -117.67972,
            "altitude": 569,
            "channel_state": 3,
            "channel_flags": 0,
            "channel_flags_manual": 0,
            "channel_flags_auto": 0,
            "confidence": 100,
            "confidence_auto": 100,
            "confidence_manual": 100,
            "humidity": 33,
            "humidity_a": 33,
            "temperature": 69,
            "temperature_a": 69,
            "pressure": 1001.66,
            "pressure_a": 1001.66,
            "analog_input": 0.03,
            "pm1.0": 0.0,
            "pm1.0_a": 0.0,
            "pm1.0_b": 0.0,
            "pm2.5": 0.0,
            "pm2.5_a": 0.0,
            "pm2.5_b": 0.0,
            "pm2.5_alt": 0.4,
            "pm2.5_alt_a": 0.3,
            "pm2.5_alt_b": 0.4,
            "pm10.0": 0.0,
            "pm10.0_a": 0.0,
            "pm10.0_b": 0.0,
            "0.3_um_count": 75,
            "0.3_um_count_a": 65,
            "0.3_um_count_b": 86,
            "0.5_um_count": 65,
            "0.5_um_count_a": 58,
            "0.5_um_count_b": 73,
            "1.0_um_count": 0,
            "1.0_um_count_a": 0,
            "1.0_um_count_b": 0,
            "2.5_um_count": 0,
            "2.5_um_count_a": 0,
            "2.5_um_count_b": 0,
            "5.0_um_count": 0,
            "5.0_um_count_a": 0,
            "5.0_um_count_b": 0,
            "10.0_um_count": 0,
            "10.0_um_count_a": 0,
            "10.0_um_count_b": 0,
            "pm1.0_cf_1": 0.0,
            "pm1.0_cf_1_a": 0.0,
            "pm1.0_cf_1_b": 0.0,
            "pm1.0_atm": 0.0,
            "pm1.0_atm_a": 0.0,
            "pm1.0_atm_b": 0.0,
            "pm2.5_atm": 0.0,
            "pm2.5_atm_a": 0.0,
            "pm2.5_atm_b": 0.0,
            "pm2.5_cf_1": 0.0,
            "pm2.5_cf_1_a": 0.0,
            "pm2.5_cf_1_b": 0.0,
            "pm10.0_atm": 0.0,
            "pm10.0_atm_a": 0.0,
            "pm10.0_atm_b": 0.0,
            "pm10.0_cf_1": 0.0,
            "pm10.0_cf_1_a": 0.0,
            "pm10.0_cf_1_b": 0.0,
            "primary_id_a": 1522282,
            "primary_key_a": "FVXH9TQTQGG2CHEY",
            "primary_id_b": 1522284,
            "primary_key_b": "31ZHIMYRBK62KPY1",
            "secondary_id_a": 1522283,
            "secondary_key_a": "UVKQCKBKJATTQGCX",
            "secondary_id_b": 1522285,
            "secondary_key_b": "DT8UOXHFJS1JDONG",
            "stats": {
                "pm2.5": 0.0,
                "pm2.5_10minute": 0.2,
                "pm2.5_30minute": 1.0,
                "pm2.5_60minute": 1.2,
                "pm2.5_6hour": 1.2,
                "pm2.5_24hour": 1.8,
                "pm2.5_1week": 5.8,
                "time_stamp": 1667666162,
            },
            "stats_a": {
                "pm2.5": 0.0,
                "pm2.5_10minute": 0.1,
                "pm2.5_30minute": 0.9,
                "pm2.5_60minute": 1.0,
                "pm2.5_6hour": 1.0,
                "pm2.5_24hour": 1.4,
                "pm2.5_1week": 4.8,
                "time_stamp": 1667666162,
            },
            "stats_b": {
                "pm2.5": 0.0,
                "pm2.5_10minute": 0.2,
                "pm2.5_30minute": 1.2,
                "pm2.5_60minute": 1.3,
                "pm2.5_6hour": 1.5,
                "pm2.5_24hour": 2.2,
                "pm2.5_1week": 6.7,
                "time_stamp": 1667666162,
            },
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_sensor_validation_error(aresponses: ResponsesMockServer) -> None:
    """Test the GET /sensor/:sensor_index endpoint, returning a validation error.

    Args:
        aresponses: An aresponses server.
    """
    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        with pytest.raises(InvalidRequestError) as err:
            _ = await api.sensors.async_get_sensor(12345, fields=["foobar"])
        assert "foobar is an unknown field" in str(err.value)

    aresponses.assert_plan_strictly_followed()


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
