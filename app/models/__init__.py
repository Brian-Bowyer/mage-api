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


class Yantra(NamedProperty):
    # just a named property, nothing else to see here
    pass


class Factor(str, Enum):
    potency = "Potency"
    duration = "Duration"


class SpellFactor(BaseModel):
    magnitude: int = POSITIVE_INT
    advanced: bool = False


class Arcanum(NamedProperty):
    value: int = SHORT_COD_ATTRIBUTE


class CasterArcanum(Arcanum):
    is_ruling: bool


class SpellArcanum(Arcanum):
    is_primary: bool


class SpellIn(BaseModel):
    # spell properties
    name: str = None
    required_arcana: SpellArcanum
    primary_factor: Factor = "Potency"
    is_rote: bool = False
    is_praxis: bool = False

    # caster properties
    current_arcana: CasterArcanum
    gnosis: int = LONG_COD_ATTRIBUTE
    rote_skill: Skill | None = None
    misc_bonus: int = Field(default=1, gt=-1)
    spent_willpower: bool = False

    # casting properties
    extra_reach: List[str] = []
    yantras: List[Yantra] = []

    ## factors
    potency: SpellFactor = SpellFactor()  # the default spellfactor
    duration: SpellFactor = SpellFactor()
    casting_time: SpellFactor = SpellFactor()
    scale: SpellFactor = SpellFactor()
    range: SpellFactor = SpellFactor()

    ## paradox
    sleepers: bool = False
    paradox_accumulation: int = 0
    is_inured: bool = False
    paradox_mana_spent: int = 0
