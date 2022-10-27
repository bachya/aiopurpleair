"""Define dynamic fixtures."""
import json
from typing import Any, cast

import pytest

from tests.common import load_fixture


@pytest.fixture(name="error_invalid_api_key_response", scope="session")
def error_invalid_api_key_response_fixture() -> dict[str, Any]:
    """Define a fixture for error response data from GET /keys."""
    return cast(
        dict[str, Any], json.loads(load_fixture("error_invalid_api_key_response.json"))
    )


@pytest.fixture(name="get_keys_response", scope="session")
def get_keys_response_fixture() -> dict[str, Any]:
    """Define a fixture for successful response data from GET /keys."""
    return cast(dict[str, Any], json.loads(load_fixture("get_keys_response.json")))
