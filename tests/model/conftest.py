"""Define dynamic fixtures."""
import json

import pytest

from tests.common import load_fixture


@pytest.fixture(name="get_keys_response", scope="session")
def get_keys_response_fixture():
    """Define a fixture for successful GET /keys response data."""
    return json.loads(load_fixture("get_keys_response.json"))
