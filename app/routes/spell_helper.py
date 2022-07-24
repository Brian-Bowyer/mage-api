from math import ceil
from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.models import SpellIn

router = APIRouter()


def max_yantras(gnosis: int):
    return 1 + ceil(gnosis / 2)


def highest_arcana_max(gnosis: int):
    return min(2 + ceil(gnosis / 2), 5)


def other_arcana_max(gnosis: int):
    return min(2 + gnosis // 2, 5)


def paradox_per_reach(gnosis: int):
    return (gnosis + 1) // 2


def total_reach(spell: SpellIn):
    return (
        spell.potency.advanced
        + spell.duration.advanced
        + spell.casting_time.advanced
        + spell.scale.advanced
        + spell.range.advanced
        + spell.extra_reach
    )


@router.post("/")
def validate_spell(spell: SpellIn, raise_on_failure=True):
    def failure(reason):
        if raise_on_failure:
            raise HTTPException(
                status_code=422,
                detail=reason,
            )
        else:
            return dict(status=False, reason=reason)

    match spell:
        case SpellIn(yantras=n) if len(n) > (m := max_yantras(spell.gnosis)):
            failure(f"Too many yantras: {n} out of {m}")
        case SpellIn(required_arcana=a, current_arcana=b) if a > b:
            failure("Missing required arcanum")
        case SpellIn(is_rote=True, rote_skill=None):
            failure("Cannot have a rote without a rote skill")

    return dict(status=True, reason="")


@router.post("/mana")
def total_mana(spell: SpellIn):
    raise NotImplementedError()


@router.post("/paradox")
def paradox_pool(spell: SpellIn):
    yantra_names = [yantra.name for yantra in spell.yantras]
    using_DMT = "Dedicated Magical Tool" in yantra_names
    return (
        paradox_per_reach(spell.gnosis) * total_reach(spell)
        + spell.sleepers
        + spell.paradox_accumulation
        + spell.is_inured
        - 2 * using_DMT
        - spell.paradox_mana_spent
    )


@router.post("/pool")
def spellcasting_pool(spell: SpellIn):
    if spell.primary_factor == "Potency":
        virtual_potency = spell.potency.magnitude - 1 - spell.current_arcana
        virtual_duration = spell.duration.magnitude - 1
    elif spell.primary_factor == "Duration":
        virtual_potency = spell.potency.magnitude - 1
        virtual_duration = spell.duration.magnitude - 1 - spell.current_arcana
    else:
        raise HTTPException(
            status_code=422, detail=f"Invalid primary factor '{spell.primary_factor}'"
        )

    if len(spell.yantras) > max_yantras(spell.gnosis):
        raise HTTPException(
            status_code=422,
            detail=f"Too many yantras: {len(spell.yantras)} out of {max_yantras(spell.gnosis)}",
        )
    total_yantra_bonus = sum([yantra.magnitude for yantra in spell.yantras])
    yantras_minus_penalties = min(
        5,
        (
            total_yantra_bonus
            - 2 * virtual_potency
            - 2 * virtual_duration
            - 2 * spell.scale.magnitude
        ),
    )

    return (
        spell.gnosis
        + spell.current_arcana.value
        + yantras_minus_penalties
        + 3 * spell.spent_willpower
        + spell.misc_bonus
    )
