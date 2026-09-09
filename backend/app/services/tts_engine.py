import io
from pathlib import Path

from app.services.emotion import analyze_text
from app.services.piper_service import piper_service


def generate_sentence(
    sentence: str,
    voice_model: str,
    speed: float = 1.0,
) -> io.BytesIO:
    """Generate one sentence with the selected local Piper voice."""
    return piper_service.synthesize(sentence, voice_model, speed=speed)


def generate_emotional_speech(
    text: str,
    voice_model: str,
    output_file: str | None = None,
) -> io.BytesIO:
    """Analyze, synthesize, pause, and combine every sentence in order."""
    segments = analyze_text(text)
    if not segments:
        raise ValueError("No sentences found")

    audio = piper_service.synthesize_segments(segments, voice_model)
    if output_file:
        Path(output_file).write_bytes(audio.getvalue())
    return audio
