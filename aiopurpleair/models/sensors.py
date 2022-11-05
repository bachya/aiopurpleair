"""Define request and response models for sensors."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, root_validator, validator

from aiopurpleair.const import SENSOR_FIELDS
from aiopurpleair.helpers.validators import validate_timestamp
from aiopurpleair.helpers.validators.sensors import (
    validate_fields_request,
    validate_latitude,
    validate_longitude,
)
from aiopurpleair.util.dt import utc_to_timestamp


class LocationType(Enum):
    """Define a location type."""

    OUTSIDE = 0
    INSIDE = 1


class GetSensorRequest(BaseModel):
    """Define a request to GET /v1/sensor/:sensor_index."""

    fields: Optional[list[str]] = None
    read_key: Optional[str] = None

    class Config:
        """Define configuration for this model."""

        frozen = True

    validate_fields = validator("fields", allow_reuse=True)(validate_fields_request)


class GetSensorResponse(BaseModel):
    """Define a response to GET /v1/sensor/:sensor_index."""

    api_version: str
    time_stamp: datetime
    data_time_stamp: datetime
    sensor: dict[str, Any]

    class Config:
        """Define configuration for this model."""

        frozen = True

    validate_data_time_stamp = validator("data_time_stamp", allow_reuse=True, pre=True)(
        validate_timestamp
    )

    validate_time_stamp = validator("time_stamp", allow_reuse=True, pre=True)(
        validate_timestamp
    )


class GetSensorsRequest(BaseModel):
    """Define a request to GET /v1/sensors."""

    fields: list[str]

    location_type: Optional[LocationType] = None
    max_age: Optional[int] = None
    modified_since: Optional[datetime] = None
    nwlat: Optional[float] = None
    nwlng: Optional[float] = None
    read_keys: Optional[list[str]] = None
    selat: Optional[float] = None
    selng: Optional[float] = None
    show_only: Optional[list[int]] = None

    class Config:
        """Define configuration for this model."""

        frozen = True

    @root_validator(pre=True)
    @classmethod
    def validate_bounding_box_missing_or_complete(
        cls, values: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate the fields.

        Args:
            values: The fields passed into the model.

        Returns:
            The fields.

        Raises:
            ValueError: Only some of the bounding box coordinates have been provided.
        """
        num_of_keys = len(
            [
                key
                for key in ("nwlng", "nwlat", "selng", "selat")
                if values.get(key) is not None
            ]
        )

        if num_of_keys not in (0, 4):
            raise ValueError("must pass none or all of the bounding box coordinates")

        return values

    validate_fields = validator("fields", allow_reuse=True)(validate_fields_request)

    @validator("location_type")
    @classmethod
    def validate_location_type(cls, value: LocationType) -> int:
        """Validate the location type.

        Args:
            value: A LocationType value.

        Returns:
            The integer-based interpretation of a location type.
        """
        return value.value

    @validator("modified_since")
    @classmethod
    def validate_modified_since(cls, value: datetime) -> int:
        """Validate the "modified since" datetime.

        Args:
            value: A "modified since" datetime object (in UTC).

        Returns:
            The timestamp of the datetime object.
        """
        return round(utc_to_timestamp(value))

    validate_nwlat = validator("nwlat", allow_reuse=True)(validate_latitude)
    validate_nwlng = validator("nwlng", allow_reuse=True)(validate_longitude)

    @validator("read_keys")
    @classmethod
    def validate_read_keys(cls, value: list[str]) -> str:
        """Validate the read keys.

        Args:
            value: A list of read key strings.

        Returns:
            A comma-separate string of read keys.
        """
        return ",".join(value)

    validate_selat = validator("selat", allow_reuse=True)(validate_latitude)
    validate_selng = validator("selng", allow_reuse=True)(validate_longitude)

    @validator("show_only")
    @classmethod
    def validate_show_only(cls, value: list[int]) -> str:
        """Validate the sensor ID list by which to filter the results.

        Args:
            value: A list of sensor IDs.

        Returns:
            A comma-separate string of sensor IDs.
        """
        return ",".join([str(i) for i in value])


def convert_sensor_response(
    fields: list[str], field_values: list[Any]
) -> dict[str, Any]:
    """Convert sensor fields into an easier-to-parse dictionary.

    Args:
        fields: A list of sensor types.
        field_values: A raw list of sensor fields.

    Returns:
        A dictionary of sensor data.
    """
    return dict(zip(fields, field_values))


class GetSensorsResponse(BaseModel):
    """Define a response to GET /v1/sensors."""

    fields: list[str]
    data: dict[int, dict[str, Any]]

    api_version: str
    time_stamp: datetime
    data_time_stamp: datetime
    max_age: int
    firmware_default_version: str

    channel_flags: Optional[
        Literal["Normal", "A-Downgraded", "B-Downgraded", "A+B-Downgraded"]
    ] = None
    channel_states: Optional[Literal["No PM", "PM-A", "PM-B", "PM-A+PM-B"]] = None
    location_type: Optional[LocationType] = None
    location_types: Optional[Literal["inside", "outside"]] = None

    class Config:
        """Define configuration for this model."""

        frozen = True

    @validator("data", pre=True)
    @classmethod
    def validate_data(
        cls, value: list[list[Any]], values: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate the data.

        Args:
            value: The pre-validated data payload.
            values: The fields passed into the model.

        Returns:
            A better format for the data.
        """
        return {
            sensor_values[0]: convert_sensor_response(values["fields"], sensor_values)
            for sensor_values in value
        }

    validate_data_time_stamp = validator("data_time_stamp", allow_reuse=True, pre=True)(
        validate_timestamp
    )

    @root_validator(pre=True)
    @classmethod
    def validate_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate the fields string.

        Args:
            values: The fields passed into the model.

        Returns:
            The fields passed into the model.

        Raises:
            ValueError: An invalid API key type was received.
        """
        for field in values["fields"]:
            if field not in SENSOR_FIELDS:
                raise ValueError(f"{field} is an unknown field")
        return values

    @validator("location_type", pre=True)
    @classmethod
    def validate_location_type(cls, value: int) -> LocationType:
        """Validate the location type.

        Args:
            value: The integer-based interpretation of a location type.

        Returns:
            A LocationType value.

        Raises:
            ValueError: Raised upon an unknown location type.
        """
        try:
            return LocationType(value)
        except ValueError as err:
            raise ValueError(f"{value} is an unknown location type") from err

    validate_time_stamp = validator("time_stamp", allow_reuse=True, pre=True)(
        validate_timestamp
    )
