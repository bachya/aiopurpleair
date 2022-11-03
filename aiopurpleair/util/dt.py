"""Define datetime utilities."""
from datetime import datetime

# EPOCHORDINAL is not exposed as a constant
# https://github.com/python/cpython/blob/3.10/Lib/zoneinfo/_zoneinfo.py#L12
EPOCHORDINAL = datetime(1970, 1, 1).toordinal()


def utc_to_timestamp(utc_dt: datetime) -> float:
    """Define a fast conversion of a datetime in UTC to a timestamp.

    Args:
        utc_dt: A datetime object with a UTC timezone.

    Returns:
        A UTC timestamp.
    """
    # Taken from
    # https://github.com/python/cpython/blob/3.10/Lib/zoneinfo/_zoneinfo.py#L185
    return (
        (utc_dt.toordinal() - EPOCHORDINAL) * 86400
        + utc_dt.hour * 3600
        + utc_dt.minute * 60
        + utc_dt.second
        + (utc_dt.microsecond / 1000000)
    )
