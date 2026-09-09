EMOTION_SETTINGS = {
    "neutral": {
        "speed": 1.0,
        "pause": 0.20,
    },

    "happy": {
        "speed": 1.10,
        "pause": 0.15,
    },

    "sad": {
        "speed": 0.80,
        "pause": 0.45,
    },

    "angry": {
        "speed": 1.15,
        "pause": 0.15,
    },

    "excited": {
        "speed": 1.20,
        "pause": 0.10,
    },

    "fearful": {
        "speed": 1.05,
        "pause": 0.30,
    },

    "calm": {
        "speed": 0.85,
        "pause": 0.50,
    },

    "hopeful": {
        "speed": 0.95,
        "pause": 0.30,
    },
}


def get_emotion_settings(emotion: str):

    return EMOTION_SETTINGS.get(
        emotion,
        EMOTION_SETTINGS["neutral"]
    )