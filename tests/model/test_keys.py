"""Define tests key models."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest
from pydantic import ValidationError

from aiopurpleair.model.keys import ApiKeyType, GetKeysResponse


def test_get_keys_response(get_keys_response: dict[str, Any]) -> None:
    """Test the GetKeysResponse model.

    Args:
        get_keys_response: A dict of response data from GET /keys.
    """
    response = GetKeysResponse.parse_obj(get_keys_response)
    assert response.dict() == {
        "api_version": "V1.0.11-0.0.41",
        "time_stamp": datetime(2022, 10, 27, 12, 25, 41),
        "api_key_type": ApiKeyType.READ,
    }


@pytest.mark.parametrize(
    "get_keys_response",
    [
        {
            "Foo": "Bar",
        },
        {
            "api_version": "V1.0.11-0.0.41",
            "time_stamp": 1666895141,
            "api_key_type": "FAKE_TYPE",
        },
    ],
)
def test_get_keys_response_errors(get_keys_response: dict[str, Any]) -> None:
    """Test errors for the GetKeysResponse model.

    Args:
        get_keys_response: A dict of response data from GET /keys.
    """
    with pytest.raises(ValidationError):
        _ = GetKeysResponse.parse_obj(get_keys_response)
