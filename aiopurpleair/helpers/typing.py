"""Define typing helpers."""
from typing import TypeVar

from pydantic.v1 import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)
