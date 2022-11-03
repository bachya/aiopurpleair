"""Define request and response models for sensors."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, root_validator, validator

from aiopurpleair.model.validator import validate_latitude, validate_longitude
from aiopurpleair.util.dt import utc_to_timestamp

SENSOR_FIELDS = {
    "0.3_um_count",
    "0.3_um_count_a",
    "0.3_um_count_b",
    "0.5_um_count",
    "0.5_um_count_a",
    "0.5_um_count_b",
    "1.0_um_count",
    "1.0_um_count_a",
    "1.0_um_count_b",
    "10.0_um_count 10.0_um_count_a",
    "10.0_um_count_b",
    "2.5_um_count",
    "2.5_um_count_a",
    "2.5_um_count_b",
    "5.0_um_count",
    "5.0_um_count_a",
    "5.0_um_count_b",
    "altitude",
    "analog_input",
    "channel_flags",
    "channel_flags_auto",
    "channel_flags_manual",
    "channel_state",
    "confidence",
    "confidence_auto",
    "confidence_manual",
    "date_created",
    "deciviews",
    "deciviews_a",
    "deciviews_b",
    "firmware_upgrade",
    "firmware_version",
    "hardware",
    "humidity",
    "humidity_a",
    "humidity_b",
    "icon",
    "last_modified",
    "last_seen",
    "latitude",
    "led_brightness",
    "location_type",
    "longitude",
    "memory",
    "model",
    "name",
    "ozone1",
    "pa_latency",
    "pm1.0",
    "pm1.0_a",
    "pm1.0_atm",
    "pm1.0_atm_a",
    "pm1.0_atm_b",
    "pm1.0_b",
    "pm1.0_cf_1",
    "pm1.0_cf_1_a",
    "pm1.0_cf_1_b",
    "pm10.0",
    "pm10.0_a",
    "pm10.0_atm",
    "pm10.0_atm_a",
    "pm10.0_atm_b",
    "pm10.0_b",
    "pm10.0_cf_1",
    "pm10.0_cf_1_a",
    "pm10.0_cf_1_b",
    "pm2.5",
    "pm2.5_10minute",
    "pm2.5_10minute_a",
    "pm2.5_10minute_b",
    "pm2.5_1week",
    "pm2.5_1week_a",
    "pm2.5_1week_b",
    "pm2.5_24hour",
    "pm2.5_24hour_a",
    "pm2.5_24hour_b",
    "pm2.5_30minute",
    "pm2.5_30minute_a",
    "pm2.5_30minute_b",
    "pm2.5_60minute",
    "pm2.5_60minute_a",
    "pm2.5_60minute_b",
    "pm2.5_6hour",
    "pm2.5_6hour_a",
    "pm2.5_6hour_b",
    "pm2.5_a",
    "pm2.5_alt",
    "pm2.5_alt_a",
    "pm2.5_alt_b",
    "pm2.5_atm",
    "pm2.5_atm_a",
    "pm2.5_atm_b",
    "pm2.5_b",
    "pm2.5_cf_1",
    "pm2.5_cf_1_a",
    "pm2.5_cf_1_b",
    "position_rating",
    "pressure",
    "pressure_a",
    "pressure_b",
    "primary_id_a",
    "primary_id_b",
    "primary_key_a",
    "primary_key_b",
    "private",
    "rssi",
    "scattering_coefficient",
    "scattering_coefficient_a",
    "scattering_coefficient_b",
    "secondary_id_a",
    "secondary_id_b",
    "secondary_key_a",
    "secondary_key_b",
    "temperature",
    "temperature_a",
    "temperature_b",
    "uptime",
    "visual_range",
    "visual_range_a",
    "visual_range_b",
    "voc",
    "voc_a",
    "voc_b",
}


class LocationType(Enum):
    """Define a location type."""

    OUTSIDE = 0
    INSIDE = 1


class GetSensorsRequest(BaseModel):
    """Define a request to GET /v1/sensors."""

    fields: list[str]
    location_type: LocationType | None = None
    read_keys: list[str] | None = None
    show_only: list[int] | None = None
    modified_since: datetime | None = None
    max_age: int = 0
    nwlng: float | None = None
    nwlat: float | None = None
    selng: float | None = None
    selat: float | None = None

    @root_validator
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

    @validator("fields")
    @classmethod
    def validate_fields(cls, value: list[str]) -> str:
        """Validate the fields.

        Args:
            value: A list of field strings.

        Returns:
            A comma-separate string of fields.

        Raises:
            ValueError: An invalid API key type was received.
        """
        for field in value:
            if field not in SENSOR_FIELDS:
                raise ValueError(f"{field} is an unknown field")

        return ",".join(value)

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
