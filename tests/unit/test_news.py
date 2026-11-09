"""
Unit tests for ALPHANEXUS News Intelligence and Event Classification
"""
import pytest
from app.engines.news.classifier import NewsEventClassifier
from app.engines.news.sentiment import NewsSentimentAnalyzer


def test_sentiment_scoring():
    analyzer = NewsSentimentAnalyzer()
    res = analyzer.analyze(
        title="Company reports record high quarterly profits",
        description="The management announced a generous dividend hike after record net profit.",
    )
    assert res["label"] in ["Positive", "Negative", "Neutral"]
    assert "score" in res


def test_event_classification():
    classifier = NewsEventClassifier()
    category = classifier.classify(
        title="Board approves acquisition of European tech unit",
        description="Transaction valued at 500 million cash buyout.",
    )
    assert isinstance(category, str)
    assert len(category) > 0
