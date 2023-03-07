"""Define tests for sensor endpoints."""
from __future__ import annotations

import json
from datetime import datetime

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiopurpleair import API
from aiopurpleair.const import ChannelFlag, ChannelState, LocationType
from aiopurpleair.endpoints.sensors import NearbySensorResult
from aiopurpleair.errors import InvalidRequestError
from aiopurpleair.models.sensors import SensorModel
from tests.common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "limit_results,output",
    [
        (
            None,
            [
                NearbySensorResult(
                    sensor=SensorModel(
                        sensor_index=131077,
                        name="BEE Patio",
                        latitude=37.93273,
                        longitude=-122.03972,
                    ),
                    distance=2.2331696896024913,
                ),
                NearbySensorResult(
                    sensor=SensorModel(
                        sensor_index=131079,
                        name="BRSKBV-outside",
                        latitude=37.75315,
                        longitude=-122.44364,
                    ),
                    distance=41.766579532099314,
                ),
                NearbySensorResult(
                    sensor=SensorModel(
                        sensor_index=131083,
                        name="Test Sensor",
                        latitude=38.287594,
                        longitude=-122.46281,
                    ),
                    distance=56.35082086588817,
                ),
                NearbySensorResult(
                    sensor=SensorModel(
                        sensor_index=131075,
                        name="Mariners Bluff",
                        latitude=33.51511,
                        longitude=-117.67972,
                    ),
                    distance=627.8171580436522,
                ),
            ],
        ),
        (
            1,
            [
                NearbySensorResult(
                    sensor=SensorModel(
                        sensor_index=131077,
                        name="BEE Patio",
                        latitude=37.93273,
                        longitude=-122.03972,
                    ),
                    distance=2.2331696896024913,
                ),
            ],
        ),
    ],
)
async def test_get_nearby_sensors(
    aresponses: ResponsesMockServer,
    limit_results: int | None,
    output: list[NearbySensorResult],
) -> None:
    """Test getting sensor indices within a bounding box around a latitude/longitude.

    Args:
        aresponses: An aresponses server.
        limit_results: An optional limit.
        output: The expected output.
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
        sensors = await api.sensors.async_get_nearby_sensors(
            ["name", "latitude", "longitude"],
            37.92122,
            -122.01889,
            10,
            limit_results=limit_results,
        )
        assert sensors == output

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_sensor(  # pylint: disable=too-many-statements
    aresponses: ResponsesMockServer,
) -> None:
    """Test the GET /sensors/:sensor_index endpoint.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/sensors/12345",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("get_sensor_response.json")), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        response = await api.sensors.async_get_sensor(12345)
        assert response.api_version == "V1.0.11-0.0.41"
        assert response.timestamp_utc == datetime(2022, 11, 5, 16, 37, 3)
        assert response.data_timestamp_utc == datetime(2022, 11, 5, 16, 36, 21)
        assert response.sensor.sensor_index == 131075
        assert response.sensor.altitude == 569
        assert response.sensor.analog_input == 0.03
        assert response.sensor.channel_flags == ChannelFlag.NORMAL
        assert response.sensor.channel_flags_auto == ChannelFlag.NORMAL
        assert response.sensor.channel_flags_manual == ChannelFlag.NORMAL
        assert response.sensor.channel_state == ChannelState.PM_A_PM_B
        assert response.sensor.confidence == 100
        assert response.sensor.confidence_auto == 100
        assert response.sensor.confidence_manual == 100
        assert response.sensor.date_created_utc == datetime(2021, 9, 29, 22, 46, 14)
        assert response.sensor.firmware_version == "7.02"
        assert response.sensor.hardware == "2.0+BME280+PMSX003-B+PMSX003-A"
        assert response.sensor.humidity == 33
        assert response.sensor.humidity_a == 33
        assert response.sensor.icon == 0
        assert response.sensor.is_owner is False
        assert response.sensor.last_modified_utc == datetime(2021, 10, 30, 22, 27, 9)
        assert response.sensor.last_seen_utc == datetime(2022, 11, 5, 16, 36, 2)
        assert response.sensor.latitude == 33.51511
        assert response.sensor.led_brightness == 35
        assert response.sensor.location_type == LocationType.OUTSIDE
        assert response.sensor.longitude == -117.67972
        assert response.sensor.memory == 16008
        assert response.sensor.model == "PA-II"
        assert response.sensor.name == "Mariners Bluff"
        assert response.sensor.pa_latency == 992
        assert response.sensor.pm0_3_um_count == 75
        assert response.sensor.pm0_3_um_count_a == 65
        assert response.sensor.pm0_3_um_count_b == 86
        assert response.sensor.pm0_5_um_count == 65
        assert response.sensor.pm0_5_um_count_a == 58
        assert response.sensor.pm0_5_um_count_b == 73
        assert response.sensor.pm10_0_cf_1_a == 0.0
        assert response.sensor.pm10_0_cf_1_b == 0.0
        assert response.sensor.pm10_0 == 0.0
        assert response.sensor.pm10_0_a == 0.0
        assert response.sensor.pm10_0_atm == 0.0
        assert response.sensor.pm10_0_atm_a == 0.0
        assert response.sensor.pm10_0_atm_b == 0.0
        assert response.sensor.pm10_0_b == 0.0
        assert response.sensor.pm10_0_cf_1 == 0.0
        assert response.sensor.pm10_0_um_count == 0
        assert response.sensor.pm10_0_um_count_a == 0
        assert response.sensor.pm10_0_um_count_b == 0
        assert response.sensor.pm1_0 == 0.0
        assert response.sensor.pm1_0_a == 0.0
        assert response.sensor.pm1_0_atm == 0.0
        assert response.sensor.pm1_0_atm_a == 0.0
        assert response.sensor.pm1_0_atm_b == 0.0
        assert response.sensor.pm1_0_b == 0.0
        assert response.sensor.pm1_0_cf_1 == 0.0
        assert response.sensor.pm1_0_cf_1_a == 0.0
        assert response.sensor.pm1_0_cf_1_b == 0.0
        assert response.sensor.pm1_0_um_count == 0
        assert response.sensor.pm1_0_um_count_a == 0
        assert response.sensor.pm1_0_um_count_b == 0
        assert response.sensor.pm2_5 == 0.0
        assert response.sensor.pm2_5_a == 0.0
        assert response.sensor.pm2_5_alt == 0.4
        assert response.sensor.pm2_5_alt_a == 0.3
        assert response.sensor.pm2_5_alt_b == 0.4
        assert response.sensor.pm2_5_atm == 0.0
        assert response.sensor.pm2_5_atm_a == 0.0
        assert response.sensor.pm2_5_atm_b == 0.0
        assert response.sensor.pm2_5_b == 0.0
        assert response.sensor.pm2_5_cf_1 == 0.0
        assert response.sensor.pm2_5_cf_1_a == 0.0
        assert response.sensor.pm2_5_cf_1_b == 0.0
        assert response.sensor.pm2_5_um_count == 0
        assert response.sensor.pm2_5_um_count_a == 0
        assert response.sensor.pm2_5_um_count_b == 0
        assert response.sensor.pm5_0_um_count == 0
        assert response.sensor.pm5_0_um_count_a == 0
        assert response.sensor.pm5_0_um_count_b == 0
        assert response.sensor.position_rating == 5
        assert response.sensor.pressure == 1001.66
        assert response.sensor.pressure_a == 1001.66
        assert response.sensor.primary_id_a == 1522282
        assert response.sensor.primary_id_b == 1522284
        assert response.sensor.primary_key_a == "FVXH9TQTQGG2CHEY"
        assert response.sensor.primary_key_b == "31ZHIMYRBK62KPY1"
        assert response.sensor.private is False
        assert response.sensor.rssi == -67
        assert response.sensor.secondary_id_a == 1522283
        assert response.sensor.secondary_id_b == 1522285
        assert response.sensor.secondary_key_a == "UVKQCKBKJATTQGCX"
        assert response.sensor.secondary_key_b == "DT8UOXHFJS1JDONG"
        assert response.sensor.temperature == 69
        assert response.sensor.temperature_a == 69
        assert response.sensor.uptime == 15682

        assert response.sensor.stats
        assert response.sensor.stats.pm2_5 == 0.0
        assert response.sensor.stats.pm2_5_10minute == 0.2
        assert response.sensor.stats.pm2_5_30minute == 1.0
        assert response.sensor.stats.pm2_5_60minute == 1.2
        assert response.sensor.stats.pm2_5_6hour == 1.2
        assert response.sensor.stats.pm2_5_24hour == 1.8
        assert response.sensor.stats.pm2_5_1week == 5.8
        assert response.sensor.stats.timestamp_utc == datetime(2022, 11, 5, 16, 36, 2)

        assert response.sensor.stats_a
        assert response.sensor.stats_a.pm2_5 == 0.0
        assert response.sensor.stats_a.pm2_5_10minute == 0.1
        assert response.sensor.stats_a.pm2_5_30minute == 0.9
        assert response.sensor.stats_a.pm2_5_60minute == 1.0
        assert response.sensor.stats_a.pm2_5_6hour == 1.0
        assert response.sensor.stats_a.pm2_5_24hour == 1.4
        assert response.sensor.stats_a.pm2_5_1week == 4.8
        assert response.sensor.stats_a.timestamp_utc == datetime(2022, 11, 5, 16, 36, 2)

        assert response.sensor.stats_b
        assert response.sensor.stats_b.pm2_5 == 0.0
        assert response.sensor.stats_b.pm2_5_10minute == 0.2
        assert response.sensor.stats_b.pm2_5_30minute == 1.2
        assert response.sensor.stats_b.pm2_5_60minute == 1.3
        assert response.sensor.stats_b.pm2_5_6hour == 1.5
        assert response.sensor.stats_b.pm2_5_24hour == 2.2
        assert response.sensor.stats_b.pm2_5_1week == 6.7
        assert response.sensor.stats_b.timestamp_utc == datetime(2022, 11, 5, 16, 36, 2)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_get_sensor_validation_error(aresponses: ResponsesMockServer) -> None:
    """Test the GET /sensors/:sensor_index endpoint, returning a validation error.

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
        assert response.timestamp_utc == datetime(2022, 11, 3, 19, 26, 29)
        assert response.data_timestamp_utc == datetime(2022, 11, 3, 19, 25, 31)
        assert response.firmware_default_version == "7.02"
        assert response.max_age == 604800
        assert response.fields == ["sensor_index", "name", "latitude", "longitude"]
        assert response.data == {
            131075: SensorModel(
                sensor_index=131075,
                name="Mariners Bluff",
                latitude=33.51511,
                longitude=-117.67972,
            ),
            131079: SensorModel(
                sensor_index=131079,
                name="BRSKBV-outside",
                latitude=37.75315,
                longitude=-122.44364,
            ),
            131077: SensorModel(
                sensor_index=131077,
                name="BEE Patio",
                latitude=37.93273,
                longitude=-122.03972,
            ),
            131083: SensorModel(
                sensor_index=131083,
                name="Test Sensor",
                latitude=38.287594,
                longitude=-122.46281,
            ),
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
