"""Define tests key models."""
from datetime import datetime

from pydantic import ValidationError
import pytest

from aiopurpleair.model.keys import ApiKeyType, GetKeysResponse


def test_get_keys_response(get_keys_response):
    """Test the GetKeysResponse model."""
    response = GetKeysResponse.parse_obj(get_keys_response)
    assert response.api_version == "V1.0.11-0.0.41"
    assert response.time_stamp == datetime(2022, 10, 27, 12, 25, 41)
    assert response.api_key_type == ApiKeyType.READ


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
def test_get_keys_response_errors(get_keys_response):
    """Test errors for the GetKeysResponse model."""
    with pytest.raises(ValidationError):
        _ = GetKeysResponse.parse_obj(get_keys_response)
