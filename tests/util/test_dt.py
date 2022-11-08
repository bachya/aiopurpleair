"""Define datetime util tests."""
from datetime import datetime

from aiopurpleair.util.dt import utc_to_timestamp


def test_utc_to_timestamp() -> None:
    """Test the utc_to_timestamp util."""
    test_datetime = datetime(2022, 11, 8, 6, 34, 39)
    assert utc_to_timestamp(test_datetime) == 1667889279
