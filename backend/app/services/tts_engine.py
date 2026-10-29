import io
from pathlib import Path

from app.services.emotion import analyze_text
from app.services.language_detector import detect_language
from app.services.piper_service import piper_service
from app.voice_catalog import get_voice_catalog


# =========================================================
# DEFAULT VOICES
# =========================================================

DEFAULT_VOICES = {
    "english": "en_US-lessac-medium",
    "hindi": "hi_IN-rohan-medium",
    "telugu": "te_IN-maya-medium",
}


# =========================================================
# GET DEFAULT VOICE FOR LANGUAGE
# =========================================================

def get_voice_for_language(
    language: str,
) -> str:
    """
    Return the default local voice
    for the detected language.
    """

    voice_id = DEFAULT_VOICES.get(
        language
    )

    if not voice_id:

        raise ValueError(
            "No default voice configured "
            f"for language: {language}"
        )

    catalog = get_voice_catalog()

    for voices in catalog.values():

        for voice in voices:

            if voice["id"] == voice_id:

                if not voice["available"]:

                    raise FileNotFoundError(
                        "Voice model is not installed: "
                        f"{voice_id}"
                    )

                return voice_id

    raise FileNotFoundError(
        "Voice is not available locally: "
        f"{voice_id}"
    )


# =========================================================
# GENERATE NORMAL SENTENCE
# =========================================================

def generate_sentence(
    sentence: str,
    voice_model: str,
    speed: float = 1.0,
) -> io.BytesIO:
    """
    Generate one normal sentence
    using Piper.
    """

    return piper_service.synthesize(
        sentence,
        voice_model,
        speed=speed,
    )


# =========================================================
# GENERATE EMOTIONAL SPEECH
# =========================================================

def generate_emotional_speech(
    text: str,
    voice_model: str | None = None,
    output_file: str | None = None,
    speed: float = 1.0,
) -> io.BytesIO:
    """
    Generate speech with automatic
    sentence-level emotion modulation.

    Pipeline:

    Text
      ↓
    Emotion Detection
      ↓
    Speed
    Pitch
    Energy
    Pause
      ↓
    Piper TTS
      ↓
    Voice Modulation
      ↓
    Final WAV
    """

    # -----------------------------------------------------
    # Analyze text
    # -----------------------------------------------------

    segments = analyze_text(
        text
    )

    if not segments:

        raise ValueError(
            "No sentences found"
        )

    # -----------------------------------------------------
    # Detect language and correct a requested voice from another language.
    # -----------------------------------------------------

    language = detect_language(
        text
    )

    if language in DEFAULT_VOICES:
        catalog = get_voice_catalog()
        requested_voice_language = next(
            (
                catalog_language
                for catalog_language, voices in catalog.items()
                if any(
                    voice["id"] == voice_model
                    for voice in voices
                )
            ),
            None,
        )

        if requested_voice_language != language:
            voice_model = get_voice_for_language(
                language
            )

    elif not voice_model:
        raise ValueError(
            "Could not determine a supported language and no voice was selected."
        )

    # -----------------------------------------------------
    # Generate emotional speech
    # -----------------------------------------------------

    audio = (
        piper_service.synthesize_segments(
            segments=segments,
            voice_name=voice_model,
            speed=speed,
        )
    )

    # -----------------------------------------------------
    # Save output file if requested
    # -----------------------------------------------------

    if output_file:

        Path(
            output_file
        ).write_bytes(
            audio.getvalue()
        )

    audio.seek(0)

    return audio