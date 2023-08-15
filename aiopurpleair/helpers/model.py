"""Define model helpers."""
from typing import TypeVar

from pydantic import BaseModel, ConfigDict


class PurpleAirBaseModel(BaseModel):
    """Define a PurpleAir-specific base model."""

    model_config = ConfigDict(frozen=True)


PurpleAirBaseModelT = TypeVar("PurpleAirBaseModelT", bound=PurpleAirBaseModel)
