"""Define validators to use across models."""
from datetime import datetime


def validate_timestamp(value: int) -> datetime:
    """Validate a longitude."""
    return datetime.fromtimestamp(value)
