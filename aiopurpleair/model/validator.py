"""Define validators to use across models."""
from datetime import datetime


def validate_timestamp(value: int) -> datetime:
    """Validate a longitude.

    Args:
        value: An integer (epoch datetime) to evaluate.

    Returns:
        A parsed datetime.datetime object.
    """
    return datetime.utcfromtimestamp(value)
