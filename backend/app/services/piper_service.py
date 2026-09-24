import io
import wave
from pathlib import Path

from piper import PiperVoice
from piper.config import SynthesisConfig


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
        voice_name: str,
        speed: float = 1.0,
    ) -> io.BytesIO:

        voice = self._get_voice(voice_name)

        audio = io.BytesIO()
        synthesis_config = SynthesisConfig(
            length_scale=1 / speed,
        )

        with wave.open(audio, "wb") as wav_file:
            voice.synthesize_wav(
                text,
                wav_file,
                syn_config=synthesis_config,
            )

        audio.seek(0)

        return audio

    def synthesize_segments(
        self,
        segments: list[dict[str, object]],
        voice_name: str,
        speed: float = 1.0,
    ) -> io.BytesIO:
        combined = io.BytesIO()
        output_wave = None

        try:
            for segment in segments:
                segment_speed = float(segment["speed"]) * speed
                audio = self.synthesize(
                    str(segment["text"]),
                    voice_name,
                    speed=segment_speed,
                )
                with wave.open(audio, "rb") as input_wave:
                    if output_wave is None:
                        output_wave = wave.open(combined, "wb")
                        output_wave.setparams(input_wave.getparams())
                    output_wave.writeframes(input_wave.readframes(input_wave.getnframes()))

                    pause = float(segment["pause"])
                    if pause > 0:
                        silence_frames = int(input_wave.getframerate() * pause)
                        output_wave.writeframes(
                            b"\x00" * input_wave.getsampwidth()
                            * silence_frames
                            * input_wave.getnchannels()
                        )
        finally:
            if output_wave is not None:
                output_wave.close()

        combined.seek(0)
        return combined


piper_service = PiperService()