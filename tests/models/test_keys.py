"""Define tests for key models."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from aiopurpleair.models.keys import ApiKeyType, GetKeysResponse


def test_get_keys_response(get_keys_response: dict[str, Any]) -> None:
    """Test the GetKeysResponse model.

    Args:
        get_keys_response: A dict of response data from GET /v1/keys.
    """
    response = GetKeysResponse.parse_obj(get_keys_response)
    assert response.dict() == {
        "api_key_type": ApiKeyType.READ,
        "api_version": "V1.0.11-0.0.41",
        "timestamp_utc": datetime(2022, 10, 27, 18, 25, 41),
    }


@pytest.mark.parametrize(
    "get_keys_response",
    [
        {
            "Foo": "Bar",
        },
        {
            "api_key_type": "FAKE_TYPE",
            "api_version": "V1.0.11-0.0.41",
            "timestamp_utc": 1666895141,
        },
    ],
)
def test_get_keys_response_errors(get_keys_response: dict[str, Any]) -> None:
    """Test errors for the GetKeysResponse model.

    Args:
        get_keys_response: A dict of response data from GET /v1/keys.
    """
    with pytest.raises(ValidationError):
        _ = GetKeysResponse.parse_obj(get_keys_response)
