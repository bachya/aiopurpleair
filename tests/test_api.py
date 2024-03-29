"""Define tests for the API object."""

from __future__ import annotations

import json
from datetime import datetime

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiopurpleair import API
from aiopurpleair.errors import InvalidApiKeyError, NotFoundError, RequestError
from aiopurpleair.models.keys import ApiKeyType, GetKeysResponse
from tests.common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error_fixture_filename,err_type,status_code",
    [
        ("error_invalid_api_key_response.json", InvalidApiKeyError, 403),
        ("error_missing_api_key_response.json", InvalidApiKeyError, 403),
        ("error_not_found_response.json", NotFoundError, 404),
        ("error_unknown_response.json", RequestError, 500),
    ],
)
async def test_api_error(
    aresponses: ResponsesMockServer,
    err_type: type[RequestError],
    error_fixture_filename: str,
    status_code: int,
) -> None:
    """Test an invalid API call.

    Args:
        aresponses: An aresponses server.
        err_type: A subclass of PurpleAirError.
        error_fixture_filename: A fixture that contains an error API response.
        status_code: An HTTP status code.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/bad_endpoint",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture(error_fixture_filename)), status=status_code
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        with pytest.raises(err_type):
            await api.async_request("get", "/bad_endpoint", GetKeysResponse)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize("use_session", [True, False])
async def test_check_api_key(
    aresponses: ResponsesMockServer, use_session: bool
) -> None:
    """Test the GET /keys endpoint.

    Args:
        aresponses: An aresponses server.
        use_session: Whether an existing aiohttp ClientSession should be used.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/keys",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("get_keys_response.json")), status=200
        ),
    )

    if use_session:
        async with aiohttp.ClientSession() as session:
            api = API(TEST_API_KEY, session=session)
    else:
        api = API(TEST_API_KEY)

    response = await api.async_check_api_key()
    assert isinstance(response, GetKeysResponse)
    assert response.api_key_type == ApiKeyType.READ
    assert response.api_version == "V1.0.11-0.0.41"
    assert response.timestamp_utc == datetime(2022, 10, 27, 18, 25, 41)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_check_api_key_validation_error(aresponses: ResponsesMockServer) -> None:
    """Test the GET /keys endpoint, returning a validation error.

    Args:
        aresponses: An aresponses server.
    """
    raw_response = json.loads(load_fixture("get_keys_response.json"))
    raw_response["api_key_type"] = "FAKE"

    aresponses.add(
        "api.purpleair.com",
        "/v1/keys",
        "get",
        response=aiohttp.web_response.json_response(raw_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(RequestError) as err:
            api = API(TEST_API_KEY, session=session)
            _ = await api.async_check_api_key()
        assert "FAKE is an unknown API key type" in str(err.value)

    aresponses.assert_plan_strictly_followed()


def test_get_map_url() -> None:
    """Test getting the map URL for a sensor index."""
    api = API(TEST_API_KEY)
    map_url = api.get_map_url(12345)
    assert map_url == "https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=12345"
