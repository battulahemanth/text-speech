import re


def detect_language(text: str) -> str:
    """
    Detect the primary language from Unicode script.
    Returns: english, hindi, telugu, tamil, odia, or unknown
    """

    counts = {
        "hindi": 0,
        "telugu": 0,
        "tamil": 0,
        "odia": 0,
        "english": 0,
    }

    for char in text:
        code = ord(char)

        # Devanagari: Hindi
        if 0x0900 <= code <= 0x097F:
            counts["hindi"] += 1

        # Telugu
        elif 0x0C00 <= code <= 0x0C7F:
            counts["telugu"] += 1

        # Tamil
        elif 0x0B80 <= code <= 0x0BFF:
            counts["tamil"] += 1

        # Odia
        elif 0x0B00 <= code <= 0x0B7F:
            counts["odia"] += 1

        # English / Latin
        elif ("A" <= char <= "Z") or ("a" <= char <= "z"):
            counts["english"] += 1

    detected = max(counts, key=counts.get)

    if counts[detected] == 0:
        return "unknown"

    return detected