"""Define request and response models for keys."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator

from aiopurpleair.backports.enum import StrEnum
from aiopurpleair.helpers.model import PurpleAirBaseModel
from aiopurpleair.helpers.validator import validate_timestamp


class ApiKeyType(StrEnum):
    """Define an API key type."""

    READ = "READ"
    READ_DISABLED = "READ_DISABLED"
    UNKNOWN = "UNKNOWN"
    WRITE = "WRITE"
    WRITE_DISABLED = "WRITE_DISABLED"


class GetKeysResponse(PurpleAirBaseModel):
    """Define a response to GET /v1/keys."""

    api_key_type: str
    api_version: str
    timestamp_utc: datetime = Field(alias="time_stamp")

    @field_validator("api_key_type")
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

    validate_utc_timestamp = field_validator("timestamp_utc", mode="before")(
        validate_timestamp
    )
