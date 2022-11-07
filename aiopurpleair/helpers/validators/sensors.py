"""Define reusable Pydantic validors for sensors."""
from aiopurpleair.const import SENSOR_FIELDS, ChannelFlag


def validate_channel_flag(value: int) -> ChannelFlag:
    """Validate the channel flag.

    Args:
        value: The integer-based interpretation of a channel flag.

    Returns:
        A ChannelFlag value.

    Raises:
        ValueError: Raised upon an unknown location type.
    """
    try:
        return ChannelFlag(value)
    except ValueError as err:
        raise ValueError(f"{value} is an unknown channel flag") from err


def validate_fields_request(value: list[str]) -> str:
    """Validate sensor fields for a request payload.

    Args:
        value: A list of field strings.

    Returns:
        A comma-separate string of fields.

    Raises:
        ValueError: An invalid field was provided.
    """
    for field in value:
        if field not in SENSOR_FIELDS:
            raise ValueError(f"{field} is an unknown field")

    return ",".join(value)


def validate_latitude(value: float) -> float:
    """Validate a latitude.

    Args:
        value: An float to evaluate.

    Returns:
        The float, if valid.

    Raises:
        ValueError: Raised on an invalid latitude.
    """
    if value < -90 or value > 90:
        raise ValueError(f"{value} is an invalid latitude")
    return value


def validate_longitude(value: float) -> float:
    """Validate a longitude.

    Args:
        value: An float to evaluate.

    Returns:
        The float, if valid.

    Raises:
        ValueError: Raised on an invalid longitude.
    """
    if value < -180 or value > 180:
        raise ValueError(f"{value} is an invalid longitude")
    return value
