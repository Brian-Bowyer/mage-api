from math import ceil
from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.models.spells import SpellInput, CasterInput, CastInput, PrimaryFactor

router = APIRouter()


def max_yantras(gnosis: int):
    return 1 + ceil(gnosis / 2)


def highest_arcana_max(gnosis: int):
    return min(2 + ceil(gnosis / 2), 5)


def other_arcana_max(gnosis: int):
    return min(2 + gnosis // 2, 5)


def paradox_per_reach(gnosis: int):
    return (gnosis + 1) // 2


def total_reach(spell: SpellInput):
    return (
        spell.potency.advanced
        + spell.duration.advanced
        + spell.casting_time.advanced
        + spell.scale.advanced
        + spell.range.advanced
        + spell.extra_reach
    )


@router.post("/")
def validate_cast(cast: CastInput, raise_on_failure=True):
    match cast:
        case CastInput(yantras=n) if len(n) > (m := max_yantras(cast.caster.gnosis)):
            HTTPException(status_code=422, detail=f"Too many yantras: {n} out of {m}")
        case CastInput(
            spell=SpellInput(arcanum=spell_arcanum),
            caster=CasterInput(arcanum=caster_arcanum),
        ) if spell_arcanum > caster_arcanum:
            HTTPException("Missing required arcanum")
        case CastInput(
            spell=SpellInput(is_rote=True), caster=CasterInput(rote_skill=None)
        ):
            HTTPException("Cannot have a rote without a rote skill")

    return dict(status=True, reason="")


def validate_caster(caster: CasterInput):
    pass


def validate_spell(spell: SpellInput):
    pass


@router.post("/mana")
def total_mana(cast: CastInput):
    raise NotImplementedError()


@router.post("/paradox")
def paradox_pool(cast: CastInput):
    yantra_names = [yantra.name for yantra in cast.yantras]
    using_DMT = "Dedicated Magical Tool" in yantra_names
    return (
        paradox_per_reach(cast.caster.gnosis) * total_reach(cast)
        + cast.paradox.sleepers
        + cast.paradox.paradox_accumulation
        + cast.paradox.is_inured
        - 2 * using_DMT
        - cast.paradox.paradox_mana_spent
    )


def account_for_primary_factor(
    primary_factor: PrimaryFactor, potency: int, duration: int, current_arcana: int
):
    if primary_factor == "Potency":
        final_potency = potency - 1 - current_arcana
        final_duration = duration - 1
    elif primary_factor == "Duration":
        final_potency = potency - 1
        final_duration = duration - 1 - current_arcana
    else:
        raise HTTPException(
            status_code=422, detail=f"Invalid primary factor '{primary_factor}'"
        )

    return final_potency, final_duration


@router.post("/pool")
def spellcasting_pool(cast: CastInput):
    final_potency, final_duration = account_for_primary_factor(
        primary_factor=cast.spell.primary_factor,
        potency=cast.factors.potency.magnitude,
        duration=cast.factors.duration.magnitude,
        current_arcana=cast.caster.arcanum,
    )
    if len(cast.yantras) > max_yantras(cast.caster.gnosis):
        raise HTTPException(
            status_code=422,
            detail=f"Too many yantras: {len(cast.yantras)} out of {max_yantras(cast.caster.gnosis)}",
        )
    total_yantra_bonus = sum([yantra.magnitude for yantra in cast.yantras])
    total_yantra_bonus = (
        total_yantra_bonus
        - 2 * final_potency
        - 2 * final_duration
        - 2 * cast.factors.scale.magnitude
    )
    total_yantra_bonus = min(total_yantra_bonus, 5)

    return (
        cast.caster.gnosis
        + cast.spell.arcanum.value
        + total_yantra_bonus
        + 3 * cast.spent_willpower
        + cast.misc_bonus
    )
