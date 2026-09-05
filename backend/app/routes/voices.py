from pathlib import Path

from fastapi import APIRouter


router = APIRouter(
    prefix="/api/voices",
    tags=["Voices"]
)


VOICES_DIR = (
    Path(__file__).resolve().parents[2] / "voices"
)


@router.get("")
def get_voices():
    voices = []

    for model_file in VOICES_DIR.glob("*.onnx"):
        voices.append({
            "id": model_file.stem,
            "name": model_file.stem,
        })

    return {
        "voices": voices
    }