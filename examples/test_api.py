"""Run an example script to quickly test."""

import asyncio
import logging

from aiohttp import ClientSession

from aiopurpleair import API
from aiopurpleair.errors import PurpleAirError

_LOGGER = logging.getLogger()

API_KEY: str = "API_READ_KEY"
READ_KEYS: list[str] | None = None  # ["SENSOR_READ_KEY", "SENSOR_READ_KEY"]
INDEXES: list[int] | None = None  # [SENSOR_INDEX, SENSOR_INDEX]
LATITUDE: float = 51.5285582
LONGITUDE: float = -0.2416796
DISTANCE: float = 10
FIELDS: list[str] = ["name", "model", "location_type",
                     "private", "latitude", "longitude"]


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            api = API(API_KEY, session=session)

            sensors_response = await api.sensors.async_get_sensors(
                fields=FIELDS,
                read_keys=READ_KEYS,
                sensor_indices=INDEXES)
            _LOGGER.info(sensors_response)

            nearby_sensor_indices = await api.sensors.async_get_nearby_sensors(
                fields=FIELDS,
                latitude=LATITUDE,
                longitude=LONGITUDE,
                distance_km=DISTANCE,
                read_keys=READ_KEYS
            )
            _LOGGER.info(nearby_sensor_indices)
        except PurpleAirError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
