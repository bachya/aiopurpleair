"""Define validators to use across models."""
from datetime import datetime


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


def validate_timestamp(value: int) -> datetime:
    """Validate a timestamp.

    Args:
        value: An integer (epoch datetime) to evaluate.

    Returns:
        A parsed datetime.datetime object.
    """
    return datetime.utcfromtimestamp(value)
