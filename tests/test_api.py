"""Define tests for the API object."""
from __future__ import annotations

import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiopurpleair import API
from aiopurpleair.errors import InvalidApiKeyError, RequestError
from tests.common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error_fixture_filename,err_type,status_code",
    [
        ("error_invalid_api_key_response.json", InvalidApiKeyError, 403),
        ("error_missing_api_key_response.json", InvalidApiKeyError, 403),
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
            await api.async_request("get", "/bad_endpoint")

    aresponses.assert_plan_strictly_followed()
