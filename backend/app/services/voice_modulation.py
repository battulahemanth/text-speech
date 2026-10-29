import librosa
import soundfile as sf
import numpy as np


def change_pitch(
    input_file: str,
    output_file: str,
    semitones: float
):
    """
    Change pitch without changing duration.
    """

    audio, sample_rate = librosa.load(
        input_file,
        sr=None,
        mono=True
    )

    if semitones != 0:
        audio = librosa.effects.pitch_shift(
            audio,
            sr=sample_rate,
            n_steps=semitones
        )

    sf.write(
        output_file,
        audio,
        sample_rate
    )

    return output_file


def change_speed(
    input_file: str,
    output_file: str,
    speed: float
):
    """
    Change speaking speed while preserving pitch.
    """

    audio, sample_rate = librosa.load(
        input_file,
        sr=None,
        mono=True
    )

    if speed != 1.0:
        audio = librosa.effects.time_stretch(
            audio,
            rate=speed
        )

    sf.write(
        output_file,
        audio,
        sample_rate
    )

    return output_file


def change_energy(
    input_file: str,
    output_file: str,
    energy: float
):
    """
    Increase or decrease voice volume.
    """

    audio, sample_rate = librosa.load(
        input_file,
        sr=None,
        mono=True
    )

    audio = audio * energy

    audio = np.clip(
        audio,
        -0.99,
        0.99
    )

    sf.write(
        output_file,
        audio,
        sample_rate
    )

    return output_file


def apply_voice_modulation(
    input_file: str,
    output_file: str,
    speed: float = 1.0,
    pitch: float = 0.0,
    energy: float = 1.0
):
    """
    Apply automatic voice modulation.

    speed:
        1.0 = normal
        < 1.0 = slower
        > 1.0 = faster

    pitch:
        0.0 = normal
        positive = higher pitch
        negative = lower pitch

    energy:
        1.0 = normal
        < 1.0 = softer
        > 1.0 = louder
    """

    # -------------------------
    # Safety limits
    # -------------------------

    speed = max(0.5, min(speed, 1.5))
    pitch = max(-6.0, min(pitch, 6.0))
    energy = max(0.5, min(energy, 1.5))

    # -------------------------
    # Load audio
    # -------------------------

    audio, sample_rate = librosa.load(
        input_file,
        sr=None,
        mono=True
    )

    # -------------------------
    # Pitch
    # -------------------------

    if pitch != 0:
        audio = librosa.effects.pitch_shift(
            audio,
            sr=sample_rate,
            n_steps=pitch
        )

    # -------------------------
    # Speed
    # -------------------------

    if speed != 1.0:
        audio = librosa.effects.time_stretch(
            audio,
            rate=speed
        )

    # -------------------------
    # Energy
    # -------------------------

    audio = audio * energy

    # -------------------------
    # Prevent clipping
    # -------------------------

    max_value = np.max(
        np.abs(audio)
    )

    if max_value > 0.99:
        audio = (
            audio / max_value
        ) * 0.99

    # -------------------------
    # Save WAV
    # -------------------------

    sf.write(
        output_file,
        audio,
        sample_rate
    )

    return output_file