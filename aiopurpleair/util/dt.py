"""Define datetime utilities."""
from datetime import datetime

EPOCHORDINAL = datetime(1970, 1, 1).toordinal()


def utc_to_timestamp(utc_dt: datetime) -> float:
    """Define a fast conversion of a datetime in UTC to a timestamp.

    Args:
        utc_dt: A datetime object with a UTC timezone.

    Returns:
        A UTC timestamp.
    """
    return (
        (utc_dt.toordinal() - EPOCHORDINAL) * 86400
        + utc_dt.hour * 3600
        + utc_dt.minute * 60
        + utc_dt.second
        + (utc_dt.microsecond / 1000000)
    )
