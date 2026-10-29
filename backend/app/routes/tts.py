import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.tts_engine import generate_emotional_speech
from app.voice_catalog import get_available_voice_ids


# =========================================================
# TTS ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/tts",
    tags=["TTS"],
)


# =========================================================
# ANALYSIS ROUTER
# =========================================================

analysis_router = APIRouter(
    prefix="/api",
    tags=["Analysis"],
)


# =========================================================
# TRANSCRIPTION ROUTER
# =========================================================

transcription_router = APIRouter(
    prefix="/api",
    tags=["Transcription"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class SynthesisRequest(BaseModel):

    text: str = Field(
        min_length=1,
        max_length=5000,
    )

    voice: str | None = None
    speed: float = Field(default=1.0, ge=0.5, le=1.5)


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


# =========================================================
# TEXT TO SPEECH
# =========================================================

@router.post("")
def synthesize(request: SynthesisRequest):

    # -----------------------------------------------------
    # Keep automatic language-based voice selection in the TTS engine.
    # -----------------------------------------------------

    voice = request.voice

    # -----------------------------------------------------
    # Validate voice
    # -----------------------------------------------------

    if voice and voice not in get_available_voice_ids():

        raise HTTPException(
            status_code=400,
            detail=(
                f"Voice is not available locally: {voice}"
            ),
        )

    # -----------------------------------------------------
    # Generate emotional speech
    # -----------------------------------------------------

    try:

        audio = generate_emotional_speech(
            request.text,voice,
            speed=request.speed,
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        print(
            f"TTS generation failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"TTS generation failed: {exc}"
            ),
        )

    # -----------------------------------------------------
    # Return WAV
    # -----------------------------------------------------

    return StreamingResponse(
        audio,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'inline; filename="speech.wav"',
        }
    )


# =========================================================
# EMOTION ANALYSIS
# =========================================================

@analysis_router.post("/analyze")
def analyze_emotions(request: AnalyzeRequest):
    from app.services.emotion import analyze_text

    try:

        sentences = analyze_text(
            request.text
        )

        return {
            "sentences": sentences
        }

    except Exception as exc:

        print(
            f"Emotion analysis failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Emotion analysis failed: {exc}"
            ),
        )


# =========================================================
# SPEECH TO TEXT
# =========================================================

@transcription_router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
):

    # -----------------------------------------------------
    # Validate filename
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    # -----------------------------------------------------
    # Validate file type
    # -----------------------------------------------------

    allowed_types = (
        "audio/",
        "video/",
    )

    if (
        not file.content_type
        or not file.content_type.startswith(
            allowed_types
        )
    ):

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        allowed_extensions = {
            ".wav",
            ".mp3",
            ".m4a",
            ".webm",
            ".ogg",
            ".flac",
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
        }

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Please upload an audio or video file."
                ),
            )

    # -----------------------------------------------------
    # Load Whisper
    # -----------------------------------------------------

    try:

        import whisper

    except ImportError as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Transcription dependency is not installed. "
                "Please install openai-whisper."
            ),
        ) from exc

    temp_path = None

    try:

        # -------------------------------------------------
        # Create temporary file
        # -------------------------------------------------

        extension = (
            Path(file.filename)
            .suffix
            or ".wav"
        )

        fd, temp_path = tempfile.mkstemp(
            suffix=extension
        )

        os.close(fd)

        # -------------------------------------------------
        # Save uploaded file
        # -------------------------------------------------

        audio_bytes = await file.read()

        with open(
            temp_path,
            "wb",
        ) as temp_file:

            temp_file.write(
                audio_bytes
            )

        # -------------------------------------------------
        # Load Whisper model
        # -------------------------------------------------

        model = whisper.load_model(
            "tiny"
        )

        # -------------------------------------------------
        # Transcribe
        # -------------------------------------------------

        result = model.transcribe(
            temp_path,
            fp16=False,
        )

        transcript = (
            result.get("text") or ""
        ).strip()

        # -------------------------------------------------
        # Check result
        # -------------------------------------------------

        if not transcript:

            raise HTTPException(
                status_code=422,
                detail=(
                    "No speech detected "
                    "in the audio file."
                ),
            )

        return {
            "text": transcript
        }

    except HTTPException:

        raise

    except Exception as exc:

        print(
            f"Audio transcription failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Audio transcription failed: {exc}"
            ),
        ) from exc

    finally:

        # -------------------------------------------------
        # Delete temporary file
        # -------------------------------------------------

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            try:
                os.remove(temp_path)
            except Exception:
                pass