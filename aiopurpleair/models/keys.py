"""Define request and response models for keys."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, validator

from aiopurpleair.backports.enum import StrEnum
from aiopurpleair.helpers.validators import validate_timestamp


class ApiKeyType(StrEnum):
    """Define an API key type."""

    READ = "READ"
    READ_DISABLED = "READ_DISABLED"
    UNKNOWN = "UNKNOWN"
    WRITE = "WRITE"
    WRITE_DISABLED = "WRITE_DISABLED"


class GetKeysResponse(BaseModel):
    """Define a response to GET /v1/keys."""

    api_key_type: str
    api_version: str
    timestamp_utc: datetime

    class Config:  # pylint: disable=too-few-public-methods
        """Define configuration for this model."""

        fields = {
            "timestamp_utc": {"alias": "time_stamp"},
        }
        frozen = True

    @validator("api_key_type")
    @classmethod
    def validate_api_key_type(cls, value: str) -> ApiKeyType:
        """Validate the API key type.

        Args:
            value: An API key to validate.

        Returns:
            A parsed ApiKeyType.

        Raises:
            ValueError: An invalid API key type was received.
        """
        try:
            return ApiKeyType(value)
        except ValueError as err:
            raise ValueError(f"{value} is an unknown API key type") from err

    validate_utc_timestamp = validator("timestamp_utc", allow_reuse=True, pre=True)(
        validate_timestamp
    )
