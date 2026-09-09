import re

from app.services.emotion_settings import get_emotion_settings


EMOTION_KEYWORDS = {
    "happy": (
        "happy", "happiest", "happiness", "joy", "joyful", "cheerful", "wonderful",
        "great", "success", "love", "smile", "సంతోషం", "సంతోషంగా", "ఆనందం",
        "ఆనందంగా", "సంతోషకరమైన", "విజయం", "గెలిచాను", "అద్భుతం", "బాగుంది", "నవ్వు", "నవ్వుతూ",
    ),
    "sad": (
        "sad", "sadness", "cry", "crying", "tears", "pain", "lost", "alone",
        "miss", "death", "sick", "emotional", "బాధ", "బాధగా", "దుఃఖం", "దుఃఖంగా",
        "కన్నీళ్లు", "ఏడుపు", "ఏడ్చాడు", "ఏడ్చింది", "కోల్పోయాను", "ఒంటరి", "మిస్",
        "చనిపోయాడు", "అనారోగ్యం", "అనారోగ్యంగా", "చెడ్డ వార్త", "గుర్తుకు వచ్చింది",
    ),
    "angry": (
        "angry", "anger", "mad", "furious", "hate", "shout", "shouted", "damn",
        "కోపం", "కోపంగా", "కోపంతో", "అరిచాను", "అరిచాడు", "అరిచింది", "ఆగ్రహం",
        "ద్వేషం", "ఎందుకు చెప్పలేదు",
    ),
    "excited": (
        "excited", "excitement", "energetic", "wow", "amazing", "fantastic",
        "incredible", "finally", "yes", "ఉత్సాహం", "ఉత్సాహంగా", "వావ్", "చివరకు",
        "అద్భుతం", "విజయం",
    ),
    "fearful": (
        "fear", "afraid", "scared", "terrified", "danger", "frightened", "భయం",
        "భయంగా", "భయపడ్డాను", "భయపడ్డాడు", "భయపడింది", "భయంకరమైన", "వణికాను", "ప్రమాదం",
    ),
    "calm": (
        "calm", "peaceful", "relaxed", "quietly", "slowly", "peace", "ప్రశాంతం",
        "ప్రశాంతంగా", "శాంతంగా", "నెమ్మదిగా", "ప్రశాంతంగా ఉండి",
    ),
    "hopeful": (
        "hope", "hopeful", "everything will be alright", "everything will be okay",
        "ఆశ", "ఆశగా", "అంతా మంచిగానే జరుగుతుంది", "అంతా బాగానే ఉంటుంది",
        "విజయం సాధిస్తాము", "విజయం సాధిస్తాం",
    ),
}


def split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?।])\s+", text.strip())
    merged = []
    for sentence in (sentence.strip() for sentence in sentences if sentence.strip()):
        dialogue_continuation = re.match(
            r"^(?:I|he|she|they)\b", sentence, re.IGNORECASE
        ) or sentence.startswith("అని")
        if merged and merged[-1].endswith("?") and dialogue_continuation:
            merged[-1] = f"{merged[-1]} {sentence}"
        else:
            merged.append(sentence)
    return merged


def _contains_keyword(text: str, keyword: str) -> bool:
    keyword = keyword.casefold()
    if re.fullmatch(r"[a-z0-9 ]+", keyword):
        return re.search(rf"\b{re.escape(keyword)}\b", text) is not None
    return keyword in text


def detect_emotion(sentence: str) -> str:
    text = sentence.casefold()
    scores = {
        emotion: sum(_contains_keyword(text, keyword) for keyword in keywords)
        for emotion, keywords in EMOTION_KEYWORDS.items()
    }

    highest_emotion = max(scores, key=scores.get)
    if scores[highest_emotion] == 0:
        return "excited" if "!" in sentence else "neutral"
    return highest_emotion


def analyze_text(text: str) -> list[dict[str, object]]:
    result = []
    for sentence in split_sentences(text):
        emotion = detect_emotion(sentence)
        settings = get_emotion_settings(emotion)
        result.append(
            {
                "sentence": sentence,
                "text": sentence,
                "emotion": emotion,
                "speed": settings["speed"],
                "pause": settings["pause"],
            }
        )
    return result


analyze_paragraph = analyze_text
