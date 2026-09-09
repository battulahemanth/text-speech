VOICES = {
    "english": [
        {
            "id": "en_US-lessac-medium",
            "name": "English - Lessac",
            "language": "English",
            "model": "en_US-lessac-medium.onnx"
        },
        {
            "id": "en_US-amy-medium",
            "name": "English - Amy",
            "language": "English",
            "model": "en_US-amy-medium.onnx"
        }
    ],

    "hindi": [
        {
            "id": "hi_IN-rohan-medium",
            "name": "Hindi - Rohan",
            "language": "Hindi",
            "model": "hi_IN-rohan-medium.onnx"
        }
    ],

    "telugu": [
        {
            "id": "te_IN-meera-medium",
            "name": "Telugu - Meera",
            "language": "Telugu",
            "model": "te_IN-meera-medium.onnx"
        }
    ]
}
"""Backward-compatible access to the voice catalog."""

from app.voice_catalog import VOICE_CATALOG as VOICES

__all__ = ["VOICES"]