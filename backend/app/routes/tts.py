from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.tts_engine import generate_emotional_speech
from app.voice_catalog import get_available_voice_ids


router = APIRouter(
    prefix="/api/tts",
    tags=["TTS"]
)

analysis_router = APIRouter(
    prefix="/api",
    tags=["Analysis"],
)


class SynthesisRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000
    )

    voice: str = "en_US-lessac-medium"


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


@router.post("")
def synthesize(request: SynthesisRequest):

    if request.voice not in get_available_voice_ids():
        raise HTTPException(
            status_code=400,
            detail=f"Voice is not available locally: {request.voice}",
        )

    try:
        audio = generate_emotional_speech(request.text, request.voice)

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"TTS generation failed: {exc}"
        )

    return StreamingResponse(
        audio,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'inline; filename="speech.wav"',
        }
    )


@analysis_router.post("/analyze")
def analyze_emotions(request: AnalyzeRequest):
    from app.services.emotion import analyze_text

    return {"sentences": analyze_text(request.text)}
