import io
import unittest
from unittest.mock import patch

from app.services.tts_engine import generate_emotional_speech


class SpeechSpeedTests(unittest.TestCase):
    @patch("app.services.tts_engine.analyze_text")
    @patch("app.services.tts_engine.piper_service.synthesize_segments")
    def test_generate_emotional_speech_uses_selected_speed(self, synthesize_segments, analyze_text):
        analyze_text.return_value = [{"text": "Hello world", "speed": 1.0, "pause": 0.2}]
        synthesize_segments.return_value = io.BytesIO(b"audio")

        generate_emotional_speech("Hello world", "en_US-lessac-medium", speed=1.5)

        synthesize_segments.assert_called_once_with(
            [{"text": "Hello world", "speed": 1.0, "pause": 0.2}],
            "en_US-lessac-medium",
            speed=1.5,
        )


if __name__ == "__main__":
    unittest.main()
