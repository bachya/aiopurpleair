"""Define package constants."""
import logging
from enum import Enum

LOGGER = logging.getLogger(__package__)


class ChannelFlag(Enum):
    """Define a channel flag."""

    NORMAL = 0
    A_DOWNGRADED = 1
    B_DOWNGRADED = 2
    A_B_DOWNGRADED = 3


class ChannelState(Enum):
    """Define a channel state."""

    NO_PM = 0
    PM_A = 1
    PM_B = 2
    PM_A_PM_B = 3


class LocationType(Enum):
    """Define a location type."""

    OUTSIDE = 0
    INSIDE = 1


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
    "10.0_um_count",
    "10.0_um_count_a",
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
    "sensor_index",
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
