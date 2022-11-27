from enum import Enum
from typing import List

from pydantic import BaseModel, Field

POSITIVE_INT = Field(default=1, gt=0)
SHORT_COD_ATTRIBUTE = Field(default=1, gt=0, lt=6)
LONG_COD_ATTRIBUTE = Field(default=1, gt=0, lt=11)


class NamedProperty(BaseModel):
    name: str
    value: int = POSITIVE_INT

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __lt__(self, other) -> bool:
        return self.value < other.value


class Skill(NamedProperty):
    value: int = SHORT_COD_ATTRIBUTE
