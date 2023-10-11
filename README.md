# 🟣 aiopurpleair: A Python3, asyncio-based library to interact with the PurpleAir API

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`aiopurpleair` is a Python3, asyncio-based library to interact with the
[PurpleAir](https://www2.purpleair.com/) API.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
  - [Checking an API Key](#checking-an-api-key)
  - [Getting Sensors](#getting-sensors)
  - [Getting a Single Sensor](#getting-a-single-sensor)
  - [Getting Nearby Sensors](#getting-nearby-sensors)
  - [Getting a Map URL](#getting-a-map-url)
  - [Connection Pooling](#connection-pooling)
- [Contributing](#contributing)

# Installation

```bash
pip install aiopurpleair
```

# Python Versions

`aiopurpleair` is currently supported on:

- Python 3.10
- Python 3.11
- Python 3.12

# Usage

In-depth documentation on the API can be found [here][purpleair-api]. Unless otherwise
noted, `aiopurpleair` endeavors to follow the API as closely as possible.

## Checking an API Key

To check whether an API key is valid and what properties it has:

```python
import asyncio

from aiopurpleair import API


async def main() -> None:
    """Run."""
    api = API("<API KEY>")
    response = await api.async_check_api_key()
    # >>> response.api_key_type == ApiKeyType.READ
    # >>> response.api_version == "V1.0.11-0.0.41"
    # >>> response.timestamp_utc == datetime(2022, 10, 27, 18, 25, 41)


asyncio.run(main())
```

## Getting Sensors

```python
import asyncio

from aiopurpleair import API


async def main() -> None:
    """Run."""
    api = API("<API_KEY>")
    response = await api.sensors.async_get_sensors(["name"])
    # >>> response.api_version == "V1.0.11-0.0.41"
    # >>> response.data == {
    # >>>     131075: SensorModel(sensor_index=131075, name=Mariners Bluff),
    # >>>     131079: SensorModel(sensor_index=131079, name=BRSKBV-outside),
    # >>> }
    # >>> response.data_timestamp_utc == datetime(2022, 11, 3, 19, 25, 31)
    # >>> response.fields == ["sensor_index", "name"]
    # >>> response.firmware_default_version == "7.02"
    # >>> response.max_age == 604800
    # >>> response.timestamp_utc == datetime(2022, 11, 3, 19, 26, 29)


asyncio.run(main())
```

### Method Parameters

- `fields` (required): The sensor data fields to include
- `location_type` (optional): An LocationType to filter by
- `max_age` (optional): Filter results modified within these seconds
- `modified_since` (optional): Filter results modified since a UTC datetime
- `read_keys` (optional): Read keys for private sensors
- `sensor_indices` (optional): Filter results by sensor index

## Getting a Single Sensor

```python
import asyncio

from aiopurpleair import API


async def main() -> None:
    """Run."""
    api = API("<API_KEY>")
    response = await api.sensors.async_get_sensor(131075)
    # >>> response.api_version == "V1.0.11-0.0.41"
    # >>> response.data_timestamp_utc == datetime(2022, 11, 5, 16, 36, 21)
    # >>> response.sensor == SensorModel(sensor_index=131075, ...),
    # >>> response.timestamp_utc == datetime(2022, 11, 5, 16, 37, 3)


asyncio.run(main())
```

### Method Parameters

- `sensor_index` (required): The sensor index of the sensor to retrieve.
- `fields` (optional): The sensor data fields to include.
- `read_key` (optional): A read key for a private sensor.

## Getting Nearby Sensors

This method returns a list of `NearbySensorResult` objects that are within a bounding box
around a given latitude/longitude pair. The list is sorted from nearest to furthest
(i.e., the first index in the list is the closest to the latitude/longitude).

`NearbySensorResult` objects have two properties:

- `sensor`: the corresponding `SensorModel` object
- `distance`: the calculated distance (in kilometers) between this sensor and the provided
  latitude/longitude

```python
import asyncio

from aiopurpleair import API


async def main() -> None:
    """Run."""
    api = API("<API_KEY>")
    sensors = await api.sensors.async_get_nearby_sensors(
        ["name"], 51.5285582, -0.2416796, 10
    )
    # >>> [NearbySensorResult(...), NearbySensorResult(...)]


asyncio.run(main())
```

### Method Parameters

- `fields` (required): The sensor data fields to include
- `latitude` (required): The latitude of the point to measure distance from
- `longitude` (required): The longitude of the point to measure distance from
- `distance` (required): The distance from the measured point to search (in kilometers)
- `limit` (optional): Limit the results

## Getting a Map URL

If you need to get the URL to a particular sensor index on the PurpleAir map website,
simply pass the appropriate sensor index to the `get_map_url` method:

```python
import asyncio

from aiopurpleair import API


async def main() -> None:
    """Run."""
    api = API("<API_KEY>")
    map_url = api.get_map_url(12345)
    # >>> https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=12345


asyncio.run(main())
```

## Connection Pooling

By default, the library creates a new connection to the PurpleAir API with each
coroutine. If you are calling a large number of coroutines (or merely want to squeeze
out every second of runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can
be used for connection pooling:

```python
import asyncio

from aiohttp import ClientSession

from aiopurpleair import API


async def main() -> None:
    """Run."""
    async with ClientSession() as session:
        api = await API("<API KEY>")

        # Get to work...


asyncio.run(main())
```

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov aiopurpleair tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[ci-badge]: https://github.com/bachya/aiopurpleair/workflows/CI/badge.svg
[ci]: https://github.com/bachya/aiopurpleair/actions
[codecov-badge]: https://codecov.io/gh/bachya/aiopurpleair/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/aiopurpleair
[contributors]: https://github.com/bachya/aiopurpleair/graphs/contributors
[fork]: https://github.com/bachya/aiopurpleair/fork
[issues]: https://github.com/bachya/aiopurpleair/issues
[license-badge]: https://img.shields.io/pypi/l/aiopurpleair.svg
[license]: https://github.com/bachya/aiopurpleair/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/40e0f45570a0eb9aab24/maintainability
[maintainability]: https://codeclimate.com/github/bachya/aiopurpleair/maintainability
[new-issue]: https://github.com/bachya/aiopurpleair/issues/new
[new-issue]: https://github.com/bachya/aiopurpleair/issues/new
[notion]: https://getnotion.com
[purpleair-api]: https://api.purpleair.com/#api-welcome
[purpleair]: https://www2.purpleair.com/
[pypi-badge]: https://img.shields.io/pypi/v/aiopurpleair.svg
[pypi]: https://pypi.python.org/pypi/aiopurpleair
[version-badge]: https://img.shields.io/pypi/pyversions/aiopurpleair.svg
[version]: https://pypi.python.org/pypi/aiopurpleair
