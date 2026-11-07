import pytest
from app.engines.news.classifier import NewsEventClassifier
from app.engines.news.sentiment import NewsSentimentAnalyzer
from app.engines.news.entity_matcher import NewsEntityMatcher
from app.models.company import Company


def test_event_classification():
    assert NewsEventClassifier.classify("Reliance Q3 Net Profit surges 16%", "Earnings report") == "Earnings"
    assert NewsEventClassifier.classify("TCS bags $850M deal with European lender", "Contract win") == "Contracts"
    assert NewsEventClassifier.classify("Company acquires 51% stake in German robotics firm", "Takeover") == "Acquisitions"
    assert NewsEventClassifier.classify("Board recommends Final Dividend of Rs 20", "Payout") == "Dividends"
    assert NewsEventClassifier.classify("SEBI issues regulatory notice over disclosure", "Investigation") == "Regulatory action"


def test_sentiment_analysis():
    # Positive
    pos = NewsSentimentAnalyzer.analyze("Record profit growth and surge in quarterly order wins", "")
    assert pos["label"] == "Positive"
    assert pos["score"] > 0

    # Negative
    neg = NewsSentimentAnalyzer.analyze("Profit slumps as margin declines amid regulatory probe", "")
    assert neg["label"] == "Negative"
    assert neg["score"] < 0

    # Neutral
    neu = NewsSentimentAnalyzer.analyze("Company holds annual general meeting in Mumbai", "")
    assert neu["label"] == "Neutral"


def test_entity_matching_collision_safety():
    comp1 = Company(symbol="RELIANCE", name="Reliance Industries Limited")
    comp2 = Company(symbol="IT", name="IT Solutions Ltd")

    # Should match RELIANCE
    res = NewsEntityMatcher.match_company("News regarding RELIANCE investment", "New expansion", [comp1])
    assert res is not None
    assert res.symbol == "RELIANCE"

    # Should NOT match blacklisted collision word "it" when used as pronoun
    res_it = NewsEntityMatcher.match_company("It is expected that markets will rebound", "Daily Wrap", [comp2])
    assert res_it is None

