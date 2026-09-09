VOICES = {
    "en_US-lessac-medium": {
        "name": "English - Lessac",
        "language": "en-US",
        "type": "piper"
    },

    "hemanth": {
        "name": "Hemanth Voice",
        "language": "en-US",
        "type": "custom",
        "model": None
    }
}


def get_voices():
    return list(VOICES.values())


def get_voice(voice_id: str):
    return VOICES.get(voice_id)