import re
from typing import Tuple, Dict, Any


class NewsSentimentAnalyzer:
    """
    Deterministic & lexicon-weighted sentiment analyzer for financial news.
    Supports Positive, Negative, Neutral, Unclear with numerical score (-1.0 to +1.0).
    Important: Sentiment reflects news tone, NOT guaranteed stock performance.
    """

    POSITIVE_WORDS = {
        "surge", "surges", "jump", "jumps", "beat", "beats", "growth", "record",
        "profit", "strong", "outperform", "bullish", "expansion", "order win",
        "dividend", "higher", "gain", "gains", "upgrade", "upgrades", "soars",
        "milestone", "robust", "optimistic", "contract", "exceeds"
    }

    NEGATIVE_WORDS = {
        "fall", "falls", "slump", "slumps", "drop", "drops", "loss", "losses",
        "miss", "misses", "penalty", "probe", "investigation", "decline", "declines",
        "bearish", "downgrade", "downgrades", "warning", "deficit", "default",
        "breach", "layoffs", "delay", "curb", "scrutiny", "resigns", "scandal"
    }

    @classmethod
    def analyze(cls, title: str, description: str) -> Dict[str, Any]:
        text = f"{title} {description}".lower()
        words = re.findall(r"\b[a-z]{3,}\b", text)

        if not words:
            return {"label": "Neutral", "score": 0.0, "confidence": 0.5}

        pos_count = sum(1 for w in words if w in cls.POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in cls.NEGATIVE_WORDS)

        total_signals = pos_count + neg_count
        if total_signals == 0:
            return {"label": "Neutral", "score": 0.0, "confidence": 0.6}

        score = (pos_count - neg_count) / max(total_signals, 1)

        if score > 0.15:
            label = "Positive"
        elif score < -0.15:
            label = "Negative"
        else:
            label = "Neutral"

        confidence = round(min(0.5 + (total_signals * 0.1), 0.98), 2)

        return {
            "label": label,
            "score": round(score, 4),
            "confidence": confidence,
            "signals_detected": total_signals,
            "disclaimer": "Sentiment represents textual tone of published news; not a market price return forecast.",
        }

