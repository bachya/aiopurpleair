"""Run an example script to quickly test."""

import asyncio
import logging

from aiohttp import ClientSession

from aiopurpleair import API
from aiopurpleair.errors import PurpleAirError

_LOGGER = logging.getLogger()

API_KEY = "<API KEY>"  # noqa: S105


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            api = API(API_KEY, session=session)

            sensors_response = await api.sensors.async_get_sensors(["name"])
            _LOGGER.info(sensors_response)

            nearby_sensor_indices = await api.sensors.async_get_nearby_sensors(
                ["name"], 51.5285582, -0.2416796, 10
            )
            _LOGGER.info(nearby_sensor_indices)
        except PurpleAirError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
