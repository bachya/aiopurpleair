"""Define dynamic fixtures."""
import json
from typing import Any, cast

import pytest

from tests.common import load_fixture


@pytest.fixture(name="get_keys_response", scope="session")
def get_keys_response_fixture() -> dict[str, Any]:
    """Define a fixture for successful GET /keys response data."""
    return cast(dict[str, Any], json.loads(load_fixture("get_keys_response.json")))
