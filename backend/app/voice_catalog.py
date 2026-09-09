from pathlib import Path
from typing import TypedDict


VOICES_DIR = Path(__file__).resolve().parents[1] / "voices"


class Voice(TypedDict):
    id: str
    name: str
    language: str
    model: str
    available: bool


VOICE_CATALOG: dict[str, list[Voice]] = {
    "english": [
        {
            "id": "en_US-lessac-medium",
            "name": "English - Lessac",
            "language": "English",
            "model": "en_US-lessac-medium.onnx",
            "available": False,
        },
        {
            "id": "en_US-amy-medium",
            "name": "English - Amy",
            "language": "English",
            "model": "en_US-amy-medium.onnx",
            "available": False,
        },
    ],
    "hindi": [
        {
            "id": "hi_IN-rohan-medium",
            "name": "Hindi - Rohan",
            "language": "Hindi",
            "model": "hi_IN-rohan-medium.onnx",
            "available": False,
        },
    ],
    "telugu": [
        {
            "id": "te_IN-maya-medium",
            "name": "Telugu - Maya",
            "language": "Telugu",
            "model": "te_IN-maya-medium.onnx",
            "available": False,
        },
        {
            "id": "te_IN-padmavathi-medium",
            "name": "Telugu - Padmavathi",
            "language": "Telugu",
            "model": "te_IN-padmavathi-medium.onnx",
            "available": False,
        },
        {
            "id": "te_IN-venkatesh-medium",
            "name": "Telugu - Venkatesh",
            "language": "Telugu",
            "model": "te_IN-venkatesh-medium.onnx",
            "available": False,
        },
        {
            "id": "hemanth",
            "name": "Hemanth Voice",
            "language": "Telugu",
            "model": "hemanth.onnx",
            "available": False,
        },
    ],
}

def get_voice_catalog() -> dict[str, list[Voice]]:
    catalog = {}

    for language, voices in VOICE_CATALOG.items():
        catalog[language] = []
        for voice in voices:
            catalog[language].append(
                {
                    **voice,
                    "available": (VOICES_DIR / voice["model"]).exists(),
                }
            )

    return catalog


def get_available_voice_ids() -> set[str]:
    return {
        voice["id"]
        for voices in get_voice_catalog().values()
        for voice in voices
        if voice["available"]
    }


