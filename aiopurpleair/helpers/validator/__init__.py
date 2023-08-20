"""Define Pydantic validator helpers."""
from datetime import datetime, timezone


def validate_timestamp(value: int) -> datetime:
    """Validate a timestamp.

    Args:
        value: An integer (epoch datetime) to evaluate.

    Returns:
        A parsed datetime.datetime object (UTC).
    """
    return datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)
