from enum import Enum
from typing import List

from pydantic import BaseModel, Field, root_validator

from app.models import (
    LONG_COD_ATTRIBUTE,
    POSITIVE_INT,
    SHORT_COD_ATTRIBUTE,
    NamedProperty,
    Skill,
)
from app.utils.constants import MAX_YANTRA_BONUS
from app.utils.spells import max_yantras, paradox_per_reach


class PrimaryFactorMode(str, Enum):
    POTENCY = "Potency"
    DURATION = "Duration"


def account_for_primary_factor(
    primary_factor: PrimaryFactorMode, potency: int, duration: int, current_arcana: int
) -> tuple[int, int]:
    if primary_factor == "Potency":
        final_potency = potency - 1 - current_arcana
        final_duration = duration - 1
    elif primary_factor == "Duration":
        final_potency = potency - 1
        final_duration = duration - 1 - current_arcana
    else:
        raise ValueError(f"Invalid primary factor '{primary_factor}'")

    return final_potency, final_duration


class Yantra(NamedProperty):
    # just a named property, nothing else to see here
    pass


class Yantras(BaseModel):
    __root__: list[Yantra]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item) -> Yantra:
        return self.__root__[item]  # type: ignore

    def __len__(self) -> int:
        return len(self.__root__)

    def names(self) -> list:
        return [yantra.name for yantra in self]

    def magnitudes(self) -> list:
        return [yantra.magnitude for yantra in self]

    def has_yantra(self, name: str) -> bool:
        return name in self.names()

    def raw_yantra_bonus(self) -> int:
        return sum(self.magnitudes())

    def total_yantra_bonus(self, total_penalty) -> int:
        total_yantra_bonus = self.raw_yantra_bonus() - 2 * total_penalty
        return min(total_yantra_bonus, MAX_YANTRA_BONUS)


class SpellFactor(BaseModel):
    is_advanced: bool = False

    def reach(self) -> int:
        return int(self.is_advanced)

    def paradox(self, overreach_factor: int) -> int:
        return self.reach() * overreach_factor

    def mana(self) -> int:
        return 0

    def dice_modifier(self) -> int:
        return 0


class MagnitudeFactor(SpellFactor):
    magnitude: int = POSITIVE_INT

    def dice_modifier(self) -> int:
        return (-2 * (self.magnitude - 1)) + super().dice_modifier()


class PotencyFactor(MagnitudeFactor):
    pass


class DurationFactor(MagnitudeFactor):
    def is_indefinite(self) -> bool:
        return self.is_advanced and self.magnitude == 5

    @root_validator
    def cap_magnitude_if_advanced(cls, values: dict) -> dict:
        if values["is_advanced"]:
            assert values["magnitude"] <= 5
        return values

    def reach(self) -> int:
        return super().reach() + self.is_indefinite()

    def mana(self) -> int:
        return self.is_indefinite() + super().mana()


class ScaleFactor(MagnitudeFactor):
    pass


class CastingTimeFactor(SpellFactor):
    ritual_bonus: int = 0

    @root_validator
    def ritual(cls, values: dict) -> dict:
        if values["ritual_bonus"] > 0:
            assert not values["is_advanced"]
        return values

    def dice_modifier(self) -> int:
        return self.ritual_bonus


class RangeFactor(SpellFactor):
    remote_viewing = False

    def reach(self) -> int:
        return super().reach() + self.remote_viewing


class SpellFactors(BaseModel):
    primary_factor: PrimaryFactorMode = PrimaryFactorMode.POTENCY

    potency: PotencyFactor = PotencyFactor()
    duration: DurationFactor = DurationFactor()
    scale: ScaleFactor = ScaleFactor()
    casting_time: CastingTimeFactor = CastingTimeFactor()
    range: RangeFactor = RangeFactor()

    def reach(self) -> int:
        return (
            self.potency.reach()
            + self.duration.reach()
            + self.scale.reach()
            + self.casting_time.reach()
            + self.range.reach()
        )

    def paradox(self, overreach_factor) -> int:
        return (
            self.potency.paradox(overreach_factor)
            + self.duration.paradox(overreach_factor)
            + self.scale.paradox(overreach_factor)
            + self.casting_time.paradox(overreach_factor)
            + self.range.paradox(overreach_factor)
        )

    def mana(self) -> int:
        return (
            self.potency.mana()
            + self.duration.mana()
            + self.scale.mana()
            + self.casting_time.mana()
            + self.range.mana()
        )

    def penalty(self) -> int:
        return (
            self.potency.dice_modifier()
            + self.duration.dice_modifier()
            + self.scale.dice_modifier()
        )

    def dice_modifier(self) -> int:
        # casting time's modifier, unlike the others', is positive
        return self.penalty() + self.casting_time.dice_modifier()


class Arcanum(NamedProperty):
    value: int = SHORT_COD_ATTRIBUTE


class CasterArcanum(Arcanum):
    is_ruling: bool = False
    is_highest: bool = False


class SpellArcanum(Arcanum):
    pass


class Paradox(BaseModel):
    ## paradox
    are_sleepers_present: bool = False
    paradox_accumulation: int = 0
    is_inured: bool = False
    paradox_mana_spent: int = 0

    def has_paradox(self, paradox_from_reach) -> bool:
        return (
            bool(paradox_from_reach)
            and self.are_sleepers_present
            and bool(self.paradox_accumulation)
            and self.is_inured
        )

    def total_paradox(
        self, paradox_from_reach: int, using_DMT: bool = False
    ) -> int | None:
        total_paradox = (
            paradox_from_reach
            + self.are_sleepers_present
            + self.paradox_accumulation
            + self.is_inured
            - 2 * using_DMT
            - self.paradox_mana_spent
        )

        if self.has_paradox(paradox_from_reach) or total_paradox > 0:
            return total_paradox
        else:
            return None


class SpellInput(BaseModel):
    # spell properties
    name: str | None = None
    arcanum: SpellArcanum
    is_rote: bool = False
    rote_skill: Skill | None = None
    is_praxis: bool = False

    @root_validator
    def valid_rote(cls, values: dict) -> dict:
        if values["is_rote"]:
            assert (
                values["rote_skill"] is not None
            ), "Cannot have a rote without a rote skill"
        return values


class CasterInput(BaseModel):
    # caster properties
    arcanum: CasterArcanum
    gnosis: int = LONG_COD_ATTRIBUTE

    # TODO: check for highest arcanum


class CastInput(BaseModel):
    # composition
    spell: SpellInput
    caster: CasterInput
    paradox: Paradox = Paradox()  # default is no paradox
    factors: SpellFactors = SpellFactors()  # default for all factors is non-advanced

    # casting properties
    yantras: Yantras = []  # type: ignore
    extra_reach: List[str] = []  # TODO: reach should be a type, not a str
    spent_willpower: bool = False
    misc_bonus: int = Field(default=1, gt=-1)

    # validators
    @root_validator
    def has_required_arcana_rating(cls, values: dict) -> dict:
        try:
            caster_arcanum, spell_arcanum = (
                values["caster"].arcanum,
                values["spell"].arcanum,
            )
        except KeyError:
            raise KeyError(values)
        assert (
            caster_arcanum.name == spell_arcanum.name
        ), f"Arcana names don't match: {caster_arcanum.name=} vs {spell_arcanum.name=}"
        assert (
            caster_arcanum.value >= spell_arcanum.value
        ), f"Caster must have {spell_arcanum} Arcanum rating to cast this spell, but only has {caster_arcanum}"

        return values

    @root_validator
    def has_under_permitted_number_of_yantras(cls, values: dict) -> dict:
        try:
            gnosis = values["caster"].gnosis
        except KeyError:
            raise KeyError(values)
        permitted_num_yantras = max_yantras(gnosis)
        current_num_yantras = len(values["yantras"])

        assert (
            current_num_yantras <= permitted_num_yantras
        ), f"Caster of gnosis {gnosis} can only use {permitted_num_yantras}, but you have {current_num_yantras}"

        return values

    # other functionality
    def total_reach(self) -> int:
        return self.factors.reach() + len(self.extra_reach)

    def total_paradox(self) -> int | None:
        return self.paradox.total_paradox(
            self.factors.paradox(
                overreach_factor=paradox_per_reach(self.caster.gnosis)
            ),
            self.yantras.has_yantra("Dedicated Magical Tool"),
        )

    def spellcasting_pool(self) -> int:
        return (
            self.caster.gnosis
            + self.spell.arcanum.value
            + self.yantras.total_yantra_bonus(self.factors.penalty())
            + 3 * self.spent_willpower
            + self.misc_bonus
        )

    def total_mana(self) -> int:
        return self.factors.mana() + self.paradox.paradox_mana_spent
