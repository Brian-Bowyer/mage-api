from typing import List
from enum import Enum

from pydantic import BaseModel, Field
from models import (
    NamedProperty,
    Skill,
    POSITIVE_INT,
    SHORT_COD_ATTRIBUTE,
    LONG_COD_ATTRIBUTE,
)


class Yantra(NamedProperty):
    # just a named property, nothing else to see here
    pass


class PrimaryFactor(str, Enum):
    potency = "Potency"
    duration = "Duration"


class SpellFactor(BaseModel):
    magnitude: int = POSITIVE_INT
    advanced: bool = False


class SpellFactors(BaseModel):
    potency: SpellFactor = SpellFactor()  # the default spellfactor
    duration: SpellFactor = SpellFactor()
    casting_time: SpellFactor = SpellFactor()
    scale: SpellFactor = SpellFactor()
    range: SpellFactor = SpellFactor()


class Arcanum(NamedProperty):
    value: int = SHORT_COD_ATTRIBUTE


class CasterArcanum(Arcanum):
    is_ruling: bool


class SpellArcanum(Arcanum):
    is_primary: bool


class Paradox(BaseModel):
    ## paradox
    sleepers: bool = False
    paradox_accumulation: int = 0
    is_inured: bool = False
    paradox_mana_spent: int = 0


class SpellInput(BaseModel):
    # spell properties
    name: str = None
    arcanum: SpellArcanum
    primary_factor: PrimaryFactor = "Potency"
    is_rote: bool = False
    is_praxis: bool = False


class CasterInput(BaseModel):
    # caster properties
    arcanum: CasterArcanum
    gnosis: int = LONG_COD_ATTRIBUTE
    rote_skill: Skill | None = None


class CastInput(BaseModel):
    spell: SpellInput
    caster: CasterInput
    # casting properties
    extra_reach: List[str] = []
    yantras: List[Yantra] = []
    spent_willpower: bool = False
    misc_bonus: int = Field(default=1, gt=-1)

    factors: SpellFactors = SpellFactors()  # default for all factors is non-advanced
    paradox: Paradox = Paradox()  # default is no paradox
