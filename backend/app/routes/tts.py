from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.piper_service import piper_service


router = APIRouter(
    prefix="/api/tts",
    tags=["TTS"]
)


class SynthesisRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000
    )

    voice: str = "en_US-lessac-medium"


@router.post("")
def synthesize(request: SynthesisRequest):

    try:
        audio = piper_service.synthesize(
            request.text,
            request.voice
        )

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
            "Content-Disposition": (
                "attachment; filename=speech.wav"
            )
        }
    )