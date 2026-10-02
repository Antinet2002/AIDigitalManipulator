import re
from collections import Counter

# This is a linguistic pattern detector, NOT a true lie detector.
PATTERNS = {
    "Guilt-tripping": [
        r"\bif you really cared\b", r"\byou don't care\b",
        r"\byou clearly don't care\b", r"\bafter everything i('?ve| have) done\b",
        r"\bso you('re| are) going to\b"
    ],
    "Emotional pressure": [
        r"\bif you leave me\b", r"\byou'll regret\b",
        r"\bdon't do this to me\b", r"\bhow could you\b",
        r"\byou owe me\b"
    ],
    "Urgency / pressure": [
        r"\bright now\b", r"\bimmediately\b", r"\banswer me\b",
        r"\byou have to\b", r"\bno excuses\b", r"\blast chance\b",
        r"\bbefore it's too late\b"
    ],
    "Blame shifting": [
        r"\bthis is your fault\b", r"\byou made me\b",
        r"\bit's because of you\b", r"\byou caused this\b",
        r"\byou're the reason\b"
    ],
    "Threatening language": [
        r"\bi will leave\b", r"\bi('ll| will) expose\b",
        r"\byou'll be sorry\b", r"\bi('ll| will) tell everyone\b",
        r"\byou'll regret this\b"
    ],
    "Gaslighting-style wording": [
        r"\byou're imagining things\b", r"\bthat never happened\b",
        r"\byou're too sensitive\b", r"\byou're crazy\b",
        r"\byou remember it wrong\b", r"\bit's all in your head\b"
    ],
    "Excessive dependency": [
        r"\byou('re| are) all i have\b", r"\bi can't live without you\b",
        r"\bwithout you i have nothing\b", r"\bif you loved me\b"
    ],
}

WEIGHTS = {
    "Guilt-tripping": 16,
    "Emotional pressure": 15,
    "Urgency / pressure": 12,
    "Blame shifting": 14,
    "Threatening language": 20,
    "Gaslighting-style wording": 18,
    "Excessive dependency": 15,
}

POSITIVE = {"happy", "good", "great", "love", "thank", "thanks", "excited", "proud"}
NEGATIVE = {"hate", "angry", "sad", "hurt", "sorry", "afraid", "scared", "blame", "fault", "regret"}

def split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]

def sentiment(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    pos = sum(w in POSITIVE for w in words)
    neg = sum(w in NEGATIVE for w in words)
    if neg > pos:
        label = "Negative / emotionally charged"
    elif pos > neg:
        label = "Positive / neutral"
    else:
        label = "Neutral / mixed"
    return {"label": label, "positive_words": pos, "negative_words": neg}

def analyze_text(text):
    lower = text.lower()
    sentences = split_sentences(text)
    detected = []
    highlighted = []

    for category, patterns in PATTERNS.items():
        matches = []
        for pattern in patterns:
            for m in re.finditer(pattern, lower):
                matches.append(m.group(0))
        if matches:
            unique = list(dict.fromkeys(matches))
            detected.append({
                "category": category,
                "count": len(unique),
                "examples": unique[:3],
                "weight": WEIGHTS[category]
            })

    # Score is deliberately capped and described as risk, not truthfulness.
    raw_score = sum(item["weight"] for item in detected)
    score = min(100, raw_score)

    if score >= 60:
        level = "High"
        description = "Several strong linguistic pressure patterns were detected."
    elif score >= 30:
        level = "Moderate"
        description = "Some potentially manipulative or pressuring language was detected."
    else:
        level = "Low"
        description = "Few or no predefined manipulation patterns were detected."

    # Sentence-level highlighting.
    for sentence in sentences:
        sl = sentence.lower()
        cats = []
        for category, patterns in PATTERNS.items():
            if any(re.search(p, sl) for p in patterns):
                cats.append(category)
        highlighted.append({
            "sentence": sentence,
            "flagged": bool(cats),
            "categories": cats
        })

    recommendations = []
    if any(d["category"] == "Threatening language" for d in detected):
        recommendations.append("Look for threats or consequences being used to force a response.")
    if any(d["category"] == "Guilt-tripping" for d in detected):
        recommendations.append("Separate the actual request from statements designed to create guilt.")
    if any(d["category"] == "Gaslighting-style wording" for d in detected):
        recommendations.append("Check the disputed facts independently rather than relying only on the message.")
    if any(d["category"] == "Urgency / pressure" for d in detected):
        recommendations.append("Pause before responding to artificial urgency.")
    if not recommendations:
        recommendations.append("No strong predefined manipulation pattern was detected. Context still matters.")

    return {
        "risk_score": score,
        "risk_level": level,
        "description": description,
        "patterns": detected,
        "sentences": highlighted,
        "sentiment": sentiment(text),
        "recommendations": recommendations,
        "disclaimer": "This tool analyzes linguistic patterns. It cannot reliably determine whether a person is lying, and results require context."
    }
