from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.models.spells import SpellInput, CasterInput, CastInput, PrimaryFactorMode

router = APIRouter()


@router.post("/")
def validate_cast(cast: CastInput) -> CastInput:
    return cast


def validate_caster(caster: CasterInput) -> CasterInput:
    return caster


def validate_spell(spell: SpellInput) -> SpellInput:
    return spell


@router.post("/mana")
def total_mana(cast: CastInput) -> int:
    return cast.total_mana()


@router.post("/paradox")
def paradox_pool(cast: CastInput) -> int | None:
    return cast.total_paradox()


@router.post("/pool")
def spellcasting_pool(cast: CastInput) -> int:
    return cast.spellcasting_pool()
