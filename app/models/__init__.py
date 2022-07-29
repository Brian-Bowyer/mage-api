from typing import List
from enum import Enum

from pydantic import BaseModel, Field

POSITIVE_INT = Field(default=1, gt=0)
SHORT_COD_ATTRIBUTE = Field(default=1, gt=0, lt=6)
LONG_COD_ATTRIBUTE = Field(default=1, gt=0, lt=11)


class NamedProperty(BaseModel):
    name: str
    value: int = POSITIVE_INT


class Skill(NamedProperty):
    value: int = SHORT_COD_ATTRIBUTE
