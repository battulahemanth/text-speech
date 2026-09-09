from fastapi import APIRouter

from app.voice_catalog import get_voice_catalog


router = APIRouter(
    prefix="/api/voices",
    tags=["Voices"]
)


@router.get("")
def get_voices():
    return get_voice_catalog()