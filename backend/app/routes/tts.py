import os
import tempfile
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, File, HTTPException, UploadFile
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

transcription_router = APIRouter(
    prefix="/api",
    tags=["Transcription"],
)


class SynthesisRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000
    )

    voice: str | None = None
    speed: Literal[0.5, 1.0, 1.5] = 1.0


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
        audio = generate_emotional_speech(request.text, request.voice, speed=request.speed)

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


@transcription_router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    allowed_types = ("audio/", "video/")
    if not file.content_type or not file.content_type.startswith(allowed_types):
        extension = Path(file.filename).suffix.lower()
        if extension not in {".wav", ".mp3", ".m4a", ".webm", ".ogg", ".flac"}:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload an audio file.",
            )

    try:
        import whisper
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="Transcription dependency is not installed. Please install openai-whisper.",
        ) from exc

    temp_path = None
    try:
        fd, temp_path = tempfile.mkstemp(suffix=Path(file.filename).suffix or ".wav")
        os.close(fd)

        audio_bytes = await file.read()
        with open(temp_path, "wb") as temp_file:
            temp_file.write(audio_bytes)

        model = whisper.load_model("tiny")
        result = model.transcribe(temp_path, fp16=False)
        transcript = (result.get("text") or "").strip()

        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="No speech detected in the audio file.",
            )

        return {"text": transcript}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Audio transcription failed: {exc}",
        ) from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
