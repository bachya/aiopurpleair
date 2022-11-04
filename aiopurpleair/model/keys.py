"""Define request and response models for keys."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, validator

from .validator import validate_timestamp


class ApiKeyType(str, Enum):
    """Define an API key type."""

    READ = "READ"
    READ_DISABLED = "READ_DISABLED"
    UNKNOWN = "UNKNOWN"
    WRITE = "WRITE"
    WRITE_DISABLED = "WRITE_DISABLED"


class GetKeysResponse(BaseModel):
    """Define a response to GET /v1/keys."""

    api_version: str
    time_stamp: int
    api_key_type: str

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

    validate_time_stamp = validator("time_stamp", allow_reuse=True)(validate_timestamp)


class InvalidApiKeyResponse(BaseModel):
    """Define an invalid API key error response for GET /v1/keys."""

    api_version: str
    time_stamp: int
    error: str
    description: str

    validate_time_stamp = validator("time_stamp", allow_reuse=True)(validate_timestamp)
