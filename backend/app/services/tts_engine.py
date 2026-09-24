import io
from pathlib import Path

from app.services.emotion import analyze_text
from app.services.language_detector import detect_language
from app.services.piper_service import piper_service
from app.voice_catalog import get_voice_catalog


DEFAULT_VOICES = {
    "english": "en_US-lessac-medium",
    "hindi": "hi_IN-rohan-medium",
    "telugu": "te_IN-maya-medium",
}


def get_voice_for_language(language: str) -> str:
    """Return the default local voice for a detected language."""

    voice_id = DEFAULT_VOICES.get(language)

    if not voice_id:
        raise ValueError(
            f"No default voice configured for language: {language}"
        )

    catalog = get_voice_catalog()

    for voices in catalog.values():
        for voice in voices:
            if voice["id"] == voice_id:
                if not voice["available"]:
                    raise FileNotFoundError(
                        f"Voice model is not installed: {voice_id}"
                    )

                return voice_id

    raise FileNotFoundError(
        f"Voice is not available locally: {voice_id}"
    )


def generate_sentence(
    sentence: str,
    voice_model: str,
    speed: float = 1.0,
) -> io.BytesIO:
    """Generate one sentence with the selected Piper voice."""

    return piper_service.synthesize(
        sentence,
        voice_model,
        speed=speed,
    )


def generate_emotional_speech(
    text: str,
    voice_model: str | None = None,
    output_file: str | None = None,
    speed: float = 1.0,
) -> io.BytesIO:

    segments = analyze_text(text)

    if not segments:
        raise ValueError("No sentences found")

    # Automatically detect language when voice is not selected
    if not voice_model:
        language = detect_language(text)
        voice_model = get_voice_for_language(language)

    audio = piper_service.synthesize_segments(
        segments,
        voice_model,
        speed=speed,
    )

    if output_file:
        Path(output_file).write_bytes(audio.getvalue())

    return audio