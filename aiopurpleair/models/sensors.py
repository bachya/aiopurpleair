"""Define request and response models for sensors."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import Field, field_validator, model_validator

from aiopurpleair.const import SENSOR_FIELDS, ChannelFlag, ChannelState, LocationType
from aiopurpleair.helpers.model import PurpleAirBaseModel
from aiopurpleair.helpers.validator import validate_timestamp
from aiopurpleair.helpers.validator.sensors import (
    validate_channel_flag,
    validate_fields_request,
    validate_latitude,
    validate_longitude,
)
from aiopurpleair.util.dt import utc_to_timestamp


class SensorModelStats(PurpleAirBaseModel):
    """Define a model for sensor statistics."""

    pm2_5: float = Field(alias="pm2.5")
    pm2_5_10minute: float = Field(alias="pm2.5_10minute")
    pm2_5_1week: float = Field(alias="pm2.5_1week")
    pm2_5_24hour: float = Field(alias="pm2.5_24hour")
    pm2_5_30minute: float = Field(alias="pm2.5_30minute")
    pm2_5_60minute: float = Field(alias="pm2.5_60minute")
    pm2_5_6hour: float = Field(alias="pm2.5_6hour")
    timestamp_utc: datetime = Field(alias="time_stamp")

    validate_timestamp_utc = field_validator("timestamp_utc", mode="before")(
        validate_timestamp
    )


class SensorModel(PurpleAirBaseModel):
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
    date_created_utc: Optional[datetime] = Field(alias="date_created", default=None)
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
    last_modified_utc: Optional[datetime] = Field(alias="last_modified", default=None)
    last_seen_utc: Optional[datetime] = Field(alias="last_seen", default=None)
    latitude: Optional[float] = None
    led_brightness: Optional[float] = None
    location_type: Optional[LocationType] = None
    longitude: Optional[float] = None
    memory: Optional[float] = None
    model: Optional[str] = None
    name: Optional[str] = None
    ozone1: Optional[float] = None
    pa_latency: Optional[int] = None
    pm0_3_um_count: Optional[float] = Field(alias="0.3_um_count", default=None)
    pm0_3_um_count_a: Optional[float] = Field(alias="0.3_um_count_a", default=None)
    pm0_3_um_count_b: Optional[float] = Field(alias="0.3_um_count_b", default=None)
    pm0_5_um_count: Optional[float] = Field(alias="0.5_um_count", default=None)
    pm0_5_um_count_a: Optional[float] = Field(alias="0.5_um_count_a", default=None)
    pm0_5_um_count_b: Optional[float] = Field(alias="0.5_um_count_b", default=None)
    pm10_0: Optional[float] = Field(alias="pm10.0", default=None)
    pm10_0_a: Optional[float] = Field(alias="pm10.0_a", default=None)
    pm10_0_atm: Optional[float] = Field(alias="pm10.0_atm", default=None)
    pm10_0_atm_a: Optional[float] = Field(alias="pm10.0_atm_a", default=None)
    pm10_0_atm_b: Optional[float] = Field(alias="pm10.0_atm_b", default=None)
    pm10_0_b: Optional[float] = Field(alias="pm10.0_b", default=None)
    pm10_0_cf_1: Optional[float] = Field(alias="pm10.0_cf_1", default=None)
    pm10_0_cf_1_a: Optional[float] = Field(alias="pm10.0_cf_1_a", default=None)
    pm10_0_cf_1_b: Optional[float] = Field(alias="pm10.0_cf_1_b", default=None)
    pm10_0_um_count: Optional[float] = Field(alias="10.0_um_count", default=None)
    pm10_0_um_count_a: Optional[float] = Field(alias="10.0_um_count_a", default=None)
    pm10_0_um_count_b: Optional[float] = Field(alias="10.0_um_count_b", default=None)
    pm1_0: Optional[float] = Field(alias="pm1.0", default=None)
    pm1_0_a: Optional[float] = Field(alias="pm1.0_a", default=None)
    pm1_0_atm: Optional[float] = Field(alias="pm1.0_atm", default=None)
    pm1_0_atm_a: Optional[float] = Field(alias="pm1.0_atm_a", default=None)
    pm1_0_atm_b: Optional[float] = Field(alias="pm1.0_atm_b", default=None)
    pm1_0_b: Optional[float] = Field(alias="pm1.0_b", default=None)
    pm1_0_cf_1: Optional[float] = Field(alias="pm1.0_cf_1", default=None)
    pm1_0_cf_1_a: Optional[float] = Field(alias="pm1.0_cf_1_a", default=None)
    pm1_0_cf_1_b: Optional[float] = Field(alias="pm1.0_cf_1_b", default=None)
    pm1_0_um_count: Optional[float] = Field(alias="1.0_um_count", default=None)
    pm1_0_um_count_a: Optional[float] = Field(alias="1.0_um_count_a", default=None)
    pm1_0_um_count_b: Optional[float] = Field(alias="1.0_um_count_b", default=None)
    pm2_5: Optional[float] = Field(alias="pm2.5", default=None)
    pm2_5_10minute: Optional[float] = Field(alias="pm2.5_10minute", default=None)
    pm2_5_10minute_a: Optional[float] = Field(alias="pm2.5_10minute_a", default=None)
    pm2_5_10minute_b: Optional[float] = Field(alias="pm2.5_10minute_b", default=None)
    pm2_5_1week: Optional[float] = Field(alias="pm2.5_1week", default=None)
    pm2_5_1week_a: Optional[float] = Field(alias="pm2.5_1week_a", default=None)
    pm2_5_1week_b: Optional[float] = Field(alias="pm2.5_1week_b", default=None)
    pm2_5_24hour: Optional[float] = Field(alias="pm2.5_24hour", default=None)
    pm2_5_24hour_a: Optional[float] = Field(alias="pm2.5_24hour_a", default=None)
    pm2_5_24hour_b: Optional[float] = Field(alias="pm2.5_24hour_b", default=None)
    pm2_5_30minute: Optional[float] = Field(alias="pm2.5_30minute", default=None)
    pm2_5_30minute_a: Optional[float] = Field(alias="pm2.5_30minute_a", default=None)
    pm2_5_30minute_b: Optional[float] = Field(alias="pm2.5_30minute_b", default=None)
    pm2_5_60minute: Optional[float] = Field(alias="pm2.5_60minute", default=None)
    pm2_5_60minute_a: Optional[float] = Field(alias="pm2.5_60minute_a", default=None)
    pm2_5_60minute_b: Optional[float] = Field(alias="pm2.5_60minute_b", default=None)
    pm2_5_6hour: Optional[float] = Field(alias="pm2.5_6hour", default=None)
    pm2_5_6hour_a: Optional[float] = Field(alias="pm2.5_6hour_a", default=None)
    pm2_5_6hour_b: Optional[float] = Field(alias="pm2.5_6hour_b", default=None)
    pm2_5_a: Optional[float] = Field(alias="pm2.5_a", default=None)
    pm2_5_alt: Optional[float] = Field(alias="pm2.5_alt", default=None)
    pm2_5_alt_a: Optional[float] = Field(alias="pm2.5_alt_a", default=None)
    pm2_5_alt_b: Optional[float] = Field(alias="pm2.5_alt_b", default=None)
    pm2_5_atm: Optional[float] = Field(alias="pm2.5_atm", default=None)
    pm2_5_atm_a: Optional[float] = Field(alias="pm2.5_atm_a", default=None)
    pm2_5_atm_b: Optional[float] = Field(alias="pm2.5_atm_b", default=None)
    pm2_5_b: Optional[float] = Field(alias="pm2.5_b", default=None)
    pm2_5_cf_1: Optional[float] = Field(alias="pm2.5_cf_1", default=None)
    pm2_5_cf_1_a: Optional[float] = Field(alias="pm2.5_cf_1_a", default=None)
    pm2_5_cf_1_b: Optional[float] = Field(alias="pm2.5_cf_1_b", default=None)
    pm2_5_um_count: Optional[float] = Field(alias="2.5_um_count", default=None)
    pm2_5_um_count_a: Optional[float] = Field(alias="2.5_um_count_a", default=None)
    pm2_5_um_count_b: Optional[float] = Field(alias="2.5_um_count_b", default=None)
    pm5_0_um_count: Optional[float] = Field(alias="5.0_um_count", default=None)
    pm5_0_um_count_a: Optional[float] = Field(alias="5.0_um_count_a", default=None)
    pm5_0_um_count_b: Optional[float] = Field(alias="5.0_um_count_b", default=None)
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

    validate_channel_flags = field_validator("channel_flags", mode="before")(
        validate_channel_flag
    )

    validate_channel_flags_auto = field_validator("channel_flags_auto", mode="before")(
        validate_channel_flag
    )

    validate_channel_flags_manual = field_validator(
        "channel_flags_manual", mode="before"
    )(validate_channel_flag)

    @field_validator("channel_state", mode="before")
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

    validate_date_created_utc = field_validator("date_created_utc", mode="before")(
        validate_timestamp
    )

    validate_last_modified_utc = field_validator("last_modified_utc", mode="before")(
        validate_timestamp
    )

    validate_last_seen_utc = field_validator("last_seen_utc", mode="before")(
        validate_timestamp
    )

    validate_latitude = field_validator("latitude")(validate_latitude)

    @field_validator("location_type", mode="before")
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

    validate_longitude = field_validator("longitude")(validate_longitude)


class GetSensorRequest(PurpleAirBaseModel):
    """Define a request to GET /v1/sensors/:sensor_index."""

    fields: Optional[str] = None
    read_key: Optional[str] = None

    validate_fields = field_validator("fields", mode="before")(validate_fields_request)


class GetSensorResponse(PurpleAirBaseModel):
    """Define a response to GET /v1/sensors/:sensor_index."""

    api_version: str
    sensor: SensorModel
    data_timestamp_utc: datetime = Field(alias="data_time_stamp")
    timestamp_utc: datetime = Field(alias="time_stamp")

    validate_data_timestamp_utc = field_validator("data_timestamp_utc", mode="before")(
        validate_timestamp
    )

    validate_timestamp_utc = field_validator("timestamp_utc", mode="before")(
        validate_timestamp
    )


class GetSensorsRequest(PurpleAirBaseModel):
    """Define a request to GET /v1/sensors."""

    fields: str

    location_type: Optional[LocationType] = None
    max_age: Optional[int] = None
    modified_since: Optional[datetime] = Field(alias="modified_since_utc", default=None)
    nwlat: Optional[float] = None
    nwlng: Optional[float] = None
    read_keys: Optional[list[str]] = None
    selat: Optional[float] = None
    selng: Optional[float] = None
    show_only: Optional[list[int]] = None

    @model_validator(mode="before")
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

    validate_fields = field_validator("fields", mode="before")(validate_fields_request)

    @field_validator("location_type")
    @classmethod
    def validate_location_type(cls, value: LocationType) -> int:
        """Validate the location type.

        Args:
            value: A LocationType value.

        Returns:
            The integer-based interpretation of a location type.
        """
        return value.value

    @field_validator("modified_since")
    @classmethod
    def validate_modified_since(cls, value: datetime) -> int:
        """Validate the "modified since" datetime.

        Args:
            value: A "modified since" datetime object (in UTC).

        Returns:
            The timestamp of the datetime object.
        """
        return round(utc_to_timestamp(value))

    validate_nwlat = field_validator("nwlat")(validate_latitude)

    validate_nwlng = field_validator("nwlng")(validate_longitude)

    @field_validator("read_keys")
    @classmethod
    def validate_read_keys(cls, value: list[str]) -> str:
        """Validate the read keys.

        Args:
            value: A list of read key strings.

        Returns:
            A comma-separate string of read keys.
        """
        return ",".join(value)

    validate_selat = field_validator("selat")(validate_latitude)
    validate_selng = field_validator("selng")(validate_longitude)

    @field_validator("show_only")
    @classmethod
    def validate_show_only(cls, value: list[int]) -> str:
        """Validate the sensor ID list by which to filter the results.

        Args:
            value: A list of sensor IDs.

        Returns:
            A comma-separate string of sensor IDs.
        """
        return ",".join([str(i) for i in value])


class GetSensorsResponse(PurpleAirBaseModel):
    """Define a response to GET /v1/sensors."""

    fields: list[str]
    data: dict[int, SensorModel]

    api_version: str
    firmware_default_version: str
    max_age: int
    data_timestamp_utc: datetime = Field(alias="data_time_stamp")
    timestamp_utc: datetime = Field(alias="time_stamp")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate the fields string.

        Args:
            values: The response payload.

        Returns:
            The response paylioad with validated fields.

        Raises:
            ValueError: An invalid API key type was received.
        """
        for field in values["fields"]:
            if field not in SENSOR_FIELDS:
                raise ValueError(f"{field} is an unknown field")

        values["data"] = {
            sensor_values[0]: SensorModel.model_validate(
                dict(zip(values["fields"], sensor_values))  # noqa: B905
            )
            for sensor_values in values["data"]
        }

        return values

    validate_data_timestamp_utc = field_validator("data_timestamp_utc", mode="before")(
        validate_timestamp
    )

    validate_timestamp_utc = field_validator("timestamp_utc", mode="before")(
        validate_timestamp
    )
