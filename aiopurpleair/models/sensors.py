"""Define request and response models for sensors."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, root_validator, validator

from aiopurpleair.const import SENSOR_FIELDS, ChannelFlag, ChannelState, LocationType
from aiopurpleair.helpers.validators import validate_timestamp
from aiopurpleair.helpers.validators.sensors import (
    validate_channel_flag,
    validate_fields_request,
    validate_latitude,
    validate_longitude,
)
from aiopurpleair.util.dt import utc_to_timestamp


class SensorModelStats(BaseModel):
    """Define a model for sensor statistics."""

    pm2_5: float
    pm2_5_10minute: float
    pm2_5_1week: float
    pm2_5_24hour: float
    pm2_5_30minute: float
    pm2_5_60minute: float
    pm2_5_6hour: float
    timestamp_utc: datetime

    class Config:
        """Define configuration for this model."""

        fields = {
            "pm2_5": {"alias": "pm2.5"},
            "pm2_5_10minute": {"alias": "pm2.5_10minute"},
            "pm2_5_1week": {"alias": "pm2.5_1week"},
            "pm2_5_24hour": {"alias": "pm2.5_24hour"},
            "pm2_5_30minute": {"alias": "pm2.5_30minute"},
            "pm2_5_60minute": {"alias": "pm2.5_60minute"},
            "pm2_5_6hour": {"alias": "pm2.5_6hour"},
            "timestamp_utc": {"alias": "time_stamp"},
        }
        frozen = True

    validate_timestamp_utc = validator(
        "timestamp_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)


class SensorModel(BaseModel):
    """Define a model for a sensor."""

    sensor_index: int

    altitude: Optional[float] = None
    analog_input: Optional[float] = None
    channel_flags: Optional[ChannelFlag] = None
    channel_flags_auto: Optional[ChannelFlag] = None
    channel_flags_manual: Optional[ChannelFlag] = None
    channel_state: Optional[ChannelState] = None
    confidence: Optional[float] = None
    confidence_auto: Optional[float] = None
    confidence_manual: Optional[float] = None
    date_created_utc: Optional[datetime] = None
    deciviews: Optional[float] = None
    deciviews_a: Optional[float] = None
    deciviews_b: Optional[float] = None
    firmware_upgrade: Optional[str] = None
    firmware_version: Optional[str] = None
    hardware: Optional[str] = None
    humidity: Optional[float] = None
    humidity_a: Optional[float] = None
    humidity_b: Optional[float] = None
    icon: Optional[int] = None
    is_owner: Optional[bool] = None
    last_modified_utc: Optional[datetime] = None
    last_seen_utc: Optional[datetime] = None
    latitude: Optional[float] = None
    led_brightness: Optional[float] = None
    location_type: Optional[LocationType] = None
    longitude: Optional[float] = None
    memory: Optional[float] = None
    model: Optional[str] = None
    name: Optional[str] = None
    ozone1: Optional[float] = None
    pa_latency: Optional[int] = None
    pm0_3_um_count: Optional[float] = None
    pm0_3_um_count_a: Optional[float] = None
    pm0_3_um_count_b: Optional[float] = None
    pm0_5_um_count: Optional[float] = None
    pm0_5_um_count_a: Optional[float] = None
    pm0_5_um_count_b: Optional[float] = None
    pm10_0: Optional[float] = None
    pm10_0_a: Optional[float] = None
    pm10_0_atm: Optional[float] = None
    pm10_0_atm_a: Optional[float] = None
    pm10_0_atm_b: Optional[float] = None
    pm10_0_b: Optional[float] = None
    pm10_0_cf_1: Optional[float] = None
    pm10_0_cf_1_a: Optional[float] = None
    pm10_0_cf_1_b: Optional[float] = None
    pm10_0_um_count: Optional[float] = None
    pm10_0_um_count_a: Optional[float] = None
    pm10_0_um_count_b: Optional[float] = None
    pm1_0: Optional[float] = None
    pm1_0_a: Optional[float] = None
    pm1_0_atm: Optional[float] = None
    pm1_0_atm_a: Optional[float] = None
    pm1_0_atm_b: Optional[float] = None
    pm1_0_b: Optional[float] = None
    pm1_0_cf_1: Optional[float] = None
    pm1_0_cf_1_a: Optional[float] = None
    pm1_0_cf_1_b: Optional[float] = None
    pm1_0_um_count: Optional[float] = None
    pm1_0_um_count_a: Optional[float] = None
    pm1_0_um_count_b: Optional[float] = None
    pm2_5: Optional[float] = None
    pm2_5_10minute: Optional[float] = None
    pm2_5_10minute_a: Optional[float] = None
    pm2_5_10minute_b: Optional[float] = None
    pm2_5_1week: Optional[float] = None
    pm2_5_1week_a: Optional[float] = None
    pm2_5_1week_b: Optional[float] = None
    pm2_5_24hour: Optional[float] = None
    pm2_5_24hour_a: Optional[float] = None
    pm2_5_24hour_b: Optional[float] = None
    pm2_5_30minute: Optional[float] = None
    pm2_5_30minute_a: Optional[float] = None
    pm2_5_30minute_b: Optional[float] = None
    pm2_5_60minute: Optional[float] = None
    pm2_5_60minute_a: Optional[float] = None
    pm2_5_60minute_b: Optional[float] = None
    pm2_5_6hour: Optional[float] = None
    pm2_5_6hour_a: Optional[float] = None
    pm2_5_6hour_b: Optional[float] = None
    pm2_5_a: Optional[float] = None
    pm2_5_alt: Optional[float] = None
    pm2_5_alt_a: Optional[float] = None
    pm2_5_alt_b: Optional[float] = None
    pm2_5_atm: Optional[float] = None
    pm2_5_atm_a: Optional[float] = None
    pm2_5_atm_b: Optional[float] = None
    pm2_5_b: Optional[float] = None
    pm2_5_cf_1: Optional[float] = None
    pm2_5_cf_1_a: Optional[float] = None
    pm2_5_cf_1_b: Optional[float] = None
    pm2_5_um_count: Optional[float] = None
    pm2_5_um_count_a: Optional[float] = None
    pm2_5_um_count_b: Optional[float] = None
    pm5_0_um_count: Optional[float] = None
    pm5_0_um_count_a: Optional[float] = None
    pm5_0_um_count_b: Optional[float] = None
    position_rating: Optional[int] = None
    pressure: Optional[float] = None
    pressure_a: Optional[float] = None
    pressure_b: Optional[float] = None
    primary_id_a: Optional[int] = None
    primary_id_b: Optional[int] = None
    primary_key_a: Optional[str] = None
    primary_key_b: Optional[str] = None
    private: Optional[bool] = None
    rssi: Optional[int] = None
    scattering_coefficient: Optional[float] = None
    scattering_coefficient_a: Optional[float] = None
    scattering_coefficient_b: Optional[float] = None
    secondary_id_a: Optional[int] = None
    secondary_id_b: Optional[int] = None
    secondary_key_a: Optional[str] = None
    secondary_key_b: Optional[str] = None
    stats: Optional[SensorModelStats] = None
    stats_a: Optional[SensorModelStats] = None
    stats_b: Optional[SensorModelStats] = None
    temperature: Optional[float] = None
    temperature_a: Optional[float] = None
    temperature_b: Optional[float] = None
    uptime: Optional[int] = None
    visual_range: Optional[float] = None
    visual_range_a: Optional[float] = None
    visual_range_b: Optional[float] = None
    voc: Optional[float] = None
    voc_a: Optional[float] = None
    voc_b: Optional[float] = None

    class Config:
        """Define configuration for this model."""

        fields = {
            "date_created_utc": {"alias": "date_created"},
            "last_modified_utc": {"alias": "last_modified"},
            "last_seen_utc": {"alias": "last_seen"},
            "pm0_3_um_count": {"alias": "0.3_um_count"},
            "pm0_3_um_count_a": {"alias": "0.3_um_count_a"},
            "pm0_3_um_count_b": {"alias": "0.3_um_count_b"},
            "pm0_5_um_count": {"alias": "0.5_um_count"},
            "pm0_5_um_count_a": {"alias": "0.5_um_count_a"},
            "pm0_5_um_count_b": {"alias": "0.5_um_count_b"},
            "pm10_0": {"alias": "pm10.0"},
            "pm10_0_a": {"alias": "pm10.0_a"},
            "pm10_0_atm": {"alias": "pm10.0_atm"},
            "pm10_0_atm_a": {"alias": "pm10.0_atm_a"},
            "pm10_0_atm_b": {"alias": "pm10.0_atm_b"},
            "pm10_0_b": {"alias": "pm10.0_b"},
            "pm10_0_cf_1": {"alias": "pm10.0_cf_1"},
            "pm10_0_cf_1_a": {"alias": "pm10.0_cf_1_a"},
            "pm10_0_cf_1_b": {"alias": "pm10.0_cf_1_b"},
            "pm10_0_um_count": {"alias": "10.0_um_count"},
            "pm10_0_um_count_a": {"alias": "10.0_um_count_a"},
            "pm10_0_um_count_b": {"alias": "10.0_um_count_b"},
            "pm1_0": {"alias": "pm1.0"},
            "pm1_0_a": {"alias": "pm1.0_a"},
            "pm1_0_atm": {"alias": "pm1.0_atm"},
            "pm1_0_atm_a": {"alias": "pm1.0_atm_a"},
            "pm1_0_atm_b": {"alias": "pm1.0_atm_b"},
            "pm1_0_b": {"alias": "pm1.0_b"},
            "pm1_0_cf_1": {"alias": "pm1.0_cf_1"},
            "pm1_0_cf_1_a": {"alias": "pm1.0_cf_1_a"},
            "pm1_0_cf_1_b": {"alias": "pm1.0_cf_1_b"},
            "pm1_0_um_count": {"alias": "1.0_um_count"},
            "pm1_0_um_count_a": {"alias": "1.0_um_count_a"},
            "pm1_0_um_count_b": {"alias": "1.0_um_count_b"},
            "pm2_5": {"alias": "pm2.5"},
            "pm2_5_10minute": {"alias": "pm2.5_10minute"},
            "pm2_5_10minute_a": {"alias": "pm2.5_10minute_a"},
            "pm2_5_10minute_b": {"alias": "pm2.5_10minute_b"},
            "pm2_5_1week": {"alias": "pm2.5_1week"},
            "pm2_5_1week_a": {"alias": "pm2.5_1week_a"},
            "pm2_5_1week_b": {"alias": "pm2.5_1week_b"},
            "pm2_5_24hour": {"alias": "pm2.5_24hour"},
            "pm2_5_24hour_a": {"alias": "pm2.5_24hour_a"},
            "pm2_5_24hour_b": {"alias": "pm2.5_24hour_b"},
            "pm2_5_30minute": {"alias": "pm2.5_30minute"},
            "pm2_5_30minute_a": {"alias": "pm2.5_30minute_a"},
            "pm2_5_30minute_b": {"alias": "pm2.5_30minute_b"},
            "pm2_5_60minute": {"alias": "pm2.5_60minute"},
            "pm2_5_60minute_a": {"alias": "pm2.5_60minute_a"},
            "pm2_5_60minute_b": {"alias": "pm2.5_60minute_b"},
            "pm2_5_6hour": {"alias": "pm2.5_6hour"},
            "pm2_5_6hour_a": {"alias": "pm2.5_6hour_a"},
            "pm2_5_6hour_b": {"alias": "pm2.5_6hour_b"},
            "pm2_5_a": {"alias": "pm2.5_a"},
            "pm2_5_alt": {"alias": "pm2.5_alt"},
            "pm2_5_alt_a": {"alias": "pm2.5_alt_a"},
            "pm2_5_alt_b": {"alias": "pm2.5_alt_b"},
            "pm2_5_atm": {"alias": "pm2.5_atm"},
            "pm2_5_atm_a": {"alias": "pm2.5_atm_a"},
            "pm2_5_atm_b": {"alias": "pm2.5_atm_b"},
            "pm2_5_b": {"alias": "pm2.5_b"},
            "pm2_5_cf_1": {"alias": "pm2.5_cf_1"},
            "pm2_5_cf_1_a": {"alias": "pm2.5_cf_1_a"},
            "pm2_5_cf_1_b": {"alias": "pm2.5_cf_1_b"},
            "pm2_5_um_count": {"alias": "2.5_um_count"},
            "pm2_5_um_count_a": {"alias": "2.5_um_count_a"},
            "pm2_5_um_count_b": {"alias": "2.5_um_count_b"},
            "pm5_0_um_count": {"alias": "5.0_um_count"},
            "pm5_0_um_count_a": {"alias": "5.0_um_count_a"},
            "pm5_0_um_count_b": {"alias": "5.0_um_count_b"},
        }
        frozen = True

    validate_channel_flags = validator(
        "channel_flags",
        allow_reuse=True,
        pre=True,
    )(validate_channel_flag)

    validate_channel_flags_auto = validator(
        "channel_flags_auto",
        allow_reuse=True,
        pre=True,
    )(validate_channel_flag)

    validate_channel_flags_manual = validator(
        "channel_flags_manual",
        allow_reuse=True,
        pre=True,
    )(validate_channel_flag)

    @validator("channel_state", pre=True)
    @classmethod
    def validate_channel_state(cls, value: int) -> ChannelState:
        """Validate the channel state.

        Args:
            value: The integer-based interpretation of a channel state.

        Returns:
            A ChannelState value.

        Raises:
            ValueError: Raised upon an unknown location type.
        """
        try:
            return ChannelState(value)
        except ValueError as err:
            raise ValueError(f"{value} is an unknown channel state") from err

    validate_date_created_utc = validator(
        "date_created_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)

    validate_last_modified_utc = validator(
        "last_modified_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)

    validate_last_seen_utc = validator(
        "last_seen_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)

    validate_latitude = validator(
        "latitude",
        allow_reuse=True,
    )(validate_latitude)

    @validator("location_type", pre=True)
    @classmethod
    def validate_location_type_response(cls, value: int) -> LocationType:
        """Validate a location type for a request payload.

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

    validate_longitude = validator(
        "longitude",
        allow_reuse=True,
    )(validate_longitude)


class GetSensorRequest(BaseModel):
    """Define a request to GET /v1/sensors/:sensor_index."""

    fields: Optional[list[str]] = None
    read_key: Optional[str] = None

    class Config:
        """Define configuration for this model."""

        frozen = True

    validate_fields = validator(
        "fields",
        allow_reuse=True,
    )(validate_fields_request)


class GetSensorResponse(BaseModel):
    """Define a response to GET /v1/sensors/:sensor_index."""

    api_version: str
    sensor: SensorModel
    data_timestamp_utc: datetime
    timestamp_utc: datetime

    class Config:
        """Define configuration for this model."""

        fields = {
            "data_timestamp_utc": {"alias": "data_time_stamp"},
            "timestamp_utc": {"alias": "time_stamp"},
        }
        frozen = True

    validate_data_timestamp_utc = validator(
        "data_timestamp_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)

    validate_timestamp_utc = validator(
        "timestamp_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)


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

        fields = {
            "modified_since": {"alias": "modified_since_utc"},
        }
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

    validate_fields = validator(
        "fields",
        allow_reuse=True,
    )(validate_fields_request)

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

    validate_nwlat = validator(
        "nwlat",
        allow_reuse=True,
    )(validate_latitude)

    validate_nwlng = validator(
        "nwlng",
        allow_reuse=True,
    )(validate_longitude)

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

    validate_selat = validator(
        "selat",
        allow_reuse=True,
    )(validate_latitude)

    validate_selng = validator(
        "selng",
        allow_reuse=True,
    )(validate_longitude)

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


class GetSensorsResponse(BaseModel):
    """Define a response to GET /v1/sensors."""

    fields: list[str]
    data: dict[int, SensorModel]

    api_version: str
    firmware_default_version: str
    max_age: int
    data_timestamp_utc: datetime
    timestamp_utc: datetime

    class Config:
        """Define configuration for this model."""

        fields = {
            "data_timestamp_utc": {"alias": "data_time_stamp"},
            "timestamp_utc": {"alias": "time_stamp"},
        }
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
            sensor_values[0]: SensorModel.parse_obj(
                dict(zip(values["fields"], sensor_values))
            )
            for sensor_values in value
        }

    validate_data_timestamp_utc = validator(
        "data_timestamp_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)

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

    validate_timestamp_utc = validator(
        "timestamp_utc",
        allow_reuse=True,
        pre=True,
    )(validate_timestamp)
