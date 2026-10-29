import io
import tempfile
import uuid
import wave
from pathlib import Path

from piper import PiperVoice
from piper.config import SynthesisConfig

from app.services.voice_modulation import apply_voice_modulation


VOICES_DIR = (
    Path(__file__).resolve().parents[2] / "voices"
)


class PiperService:

    def __init__(self):
        self.voices = {}

    # ---------------------------------
    # Load Piper Voice
    # ---------------------------------

    def _get_voice(self, voice_name: str):

        if voice_name not in self.voices:

            model_path = (
                VOICES_DIR / f"{voice_name}.onnx"
            )

            if not model_path.exists():
                raise FileNotFoundError(
                    f"Voice model not found: {voice_name}"
                )

            self.voices[voice_name] = (
                PiperVoice.load(
                    str(model_path)
                )
            )

        return self.voices[voice_name]

    # ---------------------------------
    # Basic Piper Synthesis
    # ---------------------------------

    def synthesize(
        self,
        text: str,
        voice_name: str,
        speed: float = 1.0,
    ) -> io.BytesIO:

        voice = self._get_voice(
            voice_name
        )

        audio = io.BytesIO()

        synthesis_config = SynthesisConfig(
            length_scale=1 / speed,
        )

        with wave.open(
            audio,
            "wb"
        ) as wav_file:

            voice.synthesize_wav(
                text,
                wav_file,
                syn_config=synthesis_config,
            )

        audio.seek(0)

        return audio

    # ---------------------------------
    # Emotional Sentence Synthesis
    # ---------------------------------

    def synthesize_emotional_sentence(
        self,
        text: str,
        voice_name: str,
        speed: float = 1.0,
        pitch: float = 0.0,
        energy: float = 1.0,
    ) -> io.BytesIO:

        original_audio = self.synthesize(
            text=text,
            voice_name=voice_name,
            speed=speed,
        )

        temp_dir = Path(
            tempfile.gettempdir()
        )

        unique_id = uuid.uuid4().hex

        input_file = (
            temp_dir /
            f"piper_input_{unique_id}.wav"
        )

        output_file = (
            temp_dir /
            f"piper_emotional_{unique_id}.wav"
        )

        try:

            # Save Piper audio
            with open(
                input_file,
                "wb"
            ) as file:

                file.write(
                    original_audio.getvalue()
                )

            # Apply pitch + energy
            apply_voice_modulation(
                input_file=str(input_file),
                output_file=str(output_file),
                speed=1.0,
                pitch=pitch,
                energy=energy,
            )

            # Read processed audio
            with open(
                output_file,
                "rb"
            ) as file:

                result = io.BytesIO(
                    file.read()
                )

            result.seek(0)

            return result

        finally:

            if input_file.exists():
                input_file.unlink()

            if output_file.exists():
                output_file.unlink()

    # ---------------------------------
    # Synthesize Emotional Segments
    # ---------------------------------

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

                text = str(
                    segment["text"]
                )

                segment_speed = (
                    float(segment["speed"])
                    * speed
                )

                pitch = float(
                    segment.get(
                        "pitch",
                        0.0
                    )
                )

                energy = float(
                    segment.get(
                        "energy",
                        1.0
                    )
                )

                pause = float(
                    segment.get(
                        "pause",
                        0.3
                    )
                )

                # ---------------------------------
                # Generate emotional sentence
                # ---------------------------------

                audio = (
                    self.synthesize_emotional_sentence(
                        text=text,
                        voice_name=voice_name,
                        speed=segment_speed,
                        pitch=pitch,
                        energy=energy,
                    )
                )

                with wave.open(
                    audio,
                    "rb"
                ) as input_wave:

                    # ---------------------------------
                    # Create output WAV
                    # ---------------------------------

                    if output_wave is None:

                        output_wave = wave.open(
                            combined,
                            "wb"
                        )

                        output_wave.setparams(
                            input_wave.getparams()
                        )

                    # ---------------------------------
                    # Add sentence audio
                    # ---------------------------------

                    frames = input_wave.readframes(
                        input_wave.getnframes()
                    )

                    output_wave.writeframes(
                        frames
                    )

                    # ---------------------------------
                    # Add silence/pause
                    # ---------------------------------

                    if pause > 0:

                        silence_frames = int(
                            input_wave.getframerate()
                            * pause
                        )

                        silence = (
                            b"\x00"
                            * input_wave.getsampwidth()
                            * silence_frames
                            * input_wave.getnchannels()
                        )

                        output_wave.writeframes(
                            silence
                        )

        finally:

            if output_wave is not None:
                output_wave.close()

        combined.seek(0)

        return combined


piper_service = PiperService()