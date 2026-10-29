# app/services/emotion.py

import re

from app.services.emotion_settings import get_emotion_settings


EMOTION_KEYWORDS = {
    "happy": (
        "happy", "happily", "happiest", "happiness",
        "joy", "joyful", "cheerful", "wonderful",
        "great", "success", "love", "smile", "smiled",
        "laugh", "laughed", "glad", "amazing", "beautiful",
        "సంతోషం", "సంతోషంగా", "సంతోషకరమైన",
        "ఆనందం", "ఆనందంగా", "విజయం",
        "గెలిచాను", "గెలిచాడు", "గెలిచింది",
        "అద్భుతం", "బాగుంది", "నవ్వు", "నవ్వుతూ",
        "నవ్వాడు", "నవ్వింది",
    ),

    "sad": (
        "sad", "sadly", "sadness", "cry", "crying",
        "cried", "tears", "pain", "lost", "alone",
        "lonely", "miss", "missed", "death", "dead",
        "sick", "sorrow", "heartbroken", "wept",
        "బాధ", "బాధగా", "దుఃఖం", "దుఃఖంగా",
        "కన్నీళ్లు", "ఏడుపు", "ఏడుస్తూ",
        "ఏడ్చాడు", "ఏడ్చింది", "ఏడ్చారు",
        "కోల్పోయాను", "కోల్పోయాడు", "కోల్పోయింది",
        "ఒంటరి", "మిస్", "చనిపోయాడు", "చనిపోయింది",
        "అనారోగ్యం", "అనారోగ్యంగా",
        "చెడ్డ వార్త", "గుర్తుకు వచ్చింది",
    ),

    "angry": (
        "angry", "anger", "mad", "furious", "rage",
        "hate", "shout", "shouted", "shouting",
        "scream", "screamed", "damn", "destroy",
        "fight", "fighting", "attacked",
        "కోపం", "కోపంగా", "కోపంతో",
        "అరిచాను", "అరిచాడు", "అరిచింది",
        "అరిచారు", "ఆగ్రహం", "ద్వేషం",
        "కొట్టాడు", "కొట్టింది", "పోరాటం",
        "ఎందుకు చెప్పలేదు",
    ),

    "excited": (
        "excited", "excitement", "exciting",
        "energetic", "wow", "amazing", "fantastic",
        "incredible", "finally", "yes", "victory",
        "won", "win", "adventure",
        "ఉత్సాహం", "ఉత్సాహంగా", "వావ్",
        "చివరకు", "అద్భుతం", "విజయం",
        "గెలిచాం", "గెలిచాము", "గెలిచాడు",
        "సాహసం",
    ),

    "fearful": (
        "fear", "afraid", "scared", "terrified",
        "danger", "dangerous", "frightened",
        "horror", "monster", "escape", "panic",
        "trembling",
        "భయం", "భయంగా", "భయపడ్డాను",
        "భయపడ్డాడు", "భయపడింది", "భయపడ్డారు",
        "భయంకరమైన", "వణికాను", "వణికాడు",
        "వణికింది", "ప్రమాదం",
        "ప్రమాదకరమైన", "రాక్షసుడు", "పారిపో",
    ),

    "surprise": (
        "surprise", "surprised", "shocked", "shock",
        "suddenly", "unexpected", "unbelievable",
        "astonished", "really", "what",
        "ఆశ్చర్యం", "ఆశ్చర్యంగా",
        "ఆశ్చర్యపోయాడు", "ఆశ్చర్యపోయింది",
        "అకస్మాత్తుగా", "ఊహించని",
        "నమ్మలేకపోయాడు", "నమ్మలేకపోయింది",
        "ఏమిటి", "ఏంటి",
    ),

    "calm": (
        "calm", "peaceful", "relaxed",
        "quietly", "slowly", "peace", "gently",
        "ప్రశాంతం", "ప్రశాంతంగా", "శాంతంగా",
        "నెమ్మదిగా", "ప్రశాంతంగా ఉండి",
        "మెల్లగా",
    ),

    "hopeful": (
        "hope", "hopeful",
        "everything will be alright",
        "everything will be okay",
        "we can do it",
        "we will win",
        "ఆశ", "ఆశగా",
        "అంతా మంచిగానే జరుగుతుంది",
        "అంతా బాగానే ఉంటుంది",
        "విజయం సాధిస్తాము",
        "విజయం సాధిస్తాం",
        "మనము గెలుస్తాము",
        "మనం గెలుస్తాం",
    ),
}


def split_sentences(text: str) -> list[str]:
    sentences = re.split(
        r"(?<=[.!?।॥])\s+",
        text.strip()
    )

    merged = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        dialogue_continuation = (
            re.match(
                r"^(?:I|he|she|they)\b",
                sentence,
                re.IGNORECASE
            )
            or sentence.startswith("అని")
        )

        if (
            merged
            and merged[-1].endswith("?")
            and dialogue_continuation
        ):
            merged[-1] = (
                f"{merged[-1]} {sentence}"
            )
        else:
            merged.append(sentence)

    return merged


def _contains_keyword(
    text: str,
    keyword: str
) -> bool:

    keyword = keyword.casefold()

    if re.fullmatch(
        r"[a-z0-9 ]+",
        keyword
    ):
        return (
            re.search(
                rf"\b{re.escape(keyword)}\b",
                text
            )
            is not None
        )

    return keyword in text


def detect_emotion(sentence: str) -> str:

    text = sentence.casefold()

    scores = {
        emotion: sum(
            _contains_keyword(
                text,
                keyword
            )
            for keyword in keywords
        )
        for emotion, keywords in EMOTION_KEYWORDS.items()
    }

    highest_emotion = max(
        scores,
        key=scores.get
    )

    highest_score = scores[highest_emotion]

    if highest_score == 0:

        if "!" in sentence:
            return "excited"

        return "neutral"

    return highest_emotion


def analyze_text(
    text: str
) -> list[dict[str, object]]:

    result = []

    for sentence in split_sentences(text):

        emotion = detect_emotion(sentence)

        settings = get_emotion_settings(
            emotion
        )

        result.append(
            {
                "sentence": sentence,
                "text": sentence,
                "emotion": emotion,

                "speed": settings.get(
                    "speed",
                    1.0
                ),

                "pitch": settings.get(
                    "pitch",
                    0.0
                ),

                "energy": settings.get(
                    "energy",
                    1.0
                ),

                "pause": settings.get(
                    "pause",
                    0.3
                ),
            }
        )

    return result


analyze_paragraph = analyze_text