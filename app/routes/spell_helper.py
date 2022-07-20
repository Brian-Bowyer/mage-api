from math import ceil
from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.models import SpellIn

router = APIRouter()


def max_yantras(gnosis):
    return 1 + ceil(gnosis / 2)


def highest_arcana_max(gnosis):
    return min(2 + ceil(gnosis / 2), 5)


def other_arcana_max(gnosis):
    return min(2 + gnosis // 2, 5)


@router.post("/")
def validate_spell(spell: SpellIn):
    if len(spell.yantras) > max_yantras(spell.gnosis):
        raise HTTPException(
            status_code=422,
            detail=f"Too many yantras: {len(spell.yantras)} out of {max_yantras(spell.gnosis)}",
        )


@router.post("/mana")
def total_mana(spell: SpellIn):
    raise NotImplementedError()


@router.post("/paradox")
def paradox_pool(spell: SpellIn):
    raise NotImplementedError()


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

    return (
        spell.gnosis
        + spell.current_arcana.value
        + spell.misc_bonus
        + 3 * spell.spent_willpower
        - 2 * virtual_potency
        - 2 * virtual_duration
        - 2 * spell.scale.magnitude
        + total_yantra_bonus
    )
