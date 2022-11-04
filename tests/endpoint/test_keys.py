"""Define tests for keys-related API endpoints."""
from __future__ import annotations

import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiopurpleair import API
from tests.common import TEST_API_KEY, load_fixture


@pytest.mark.asyncio
async def test_check_api_key(aresponses: ResponsesMockServer) -> None:
    """Test the GET /keys endpoint.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/keys",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("get_keys_response.json")), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, session=session)
        data = await api.keys.async_check_api_key()
        assert data == {
            "api_version": "V1.0.11-0.0.41",
            "time_stamp": 1666895141,
            "api_key_type": "READ",
        }

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_check_api_key_no_session(aresponses: ResponsesMockServer) -> None:
    """Test the GET /keys endpoint without an explicit aiohttp ClientSession.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.purpleair.com",
        "/v1/keys",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("get_keys_response.json")), status=200
        ),
    )

    api = API(TEST_API_KEY)
    data = await api.keys.async_check_api_key()
    assert data == {
        "api_version": "V1.0.11-0.0.41",
        "time_stamp": 1666895141,
        "api_key_type": "READ",
    }

    aresponses.assert_plan_strictly_followed()
