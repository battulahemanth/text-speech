import io
import wave
from pathlib import Path

from piper import PiperVoice


VOICES_DIR = (
    Path(__file__).resolve().parents[2] / "voices"
)


class PiperService:
    def __init__(self):
        self.voices = {}

    def _get_voice(self, voice_name: str):
        if voice_name not in self.voices:
            model_path = VOICES_DIR / f"{voice_name}.onnx"

            if not model_path.exists():
                raise FileNotFoundError(
                    f"Voice model not found: {voice_name}"
                )

            self.voices[voice_name] = PiperVoice.load(
                str(model_path)
            )

        return self.voices[voice_name]

    def synthesize(
        self,
        text: str,
        voice_name: str
    ) -> io.BytesIO:

        voice = self._get_voice(voice_name)

        audio = io.BytesIO()

        with wave.open(audio, "wb") as wav_file:
            voice.synthesize_wav(
                text,
                wav_file
            )

        audio.seek(0)

        return audio


piper_service = PiperService()