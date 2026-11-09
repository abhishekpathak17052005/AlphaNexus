"""
ALPHANEXUS – News & Event Intelligence Pipeline
===============================================
Entity-matched news feed aggregator, event tagger, and sentiment classifier.
"""

from app.engines.news.service import NewsService, news_service
from app.engines.news.classifier import NewsEventClassifier
from app.engines.news.sentiment import NewsSentimentAnalyzer
from app.engines.news.entity_matcher import NewsEntityMatcher

EventClassifier = NewsEventClassifier
event_classifier = NewsEventClassifier()

SentimentAnalyzer = NewsSentimentAnalyzer
sentiment_analyzer = NewsSentimentAnalyzer()

EntityMatcher = NewsEntityMatcher
entity_matcher = NewsEntityMatcher()

__all__ = [
    "NewsService",
    "news_service",
    "NewsEventClassifier",
    "EventClassifier",
    "event_classifier",
    "NewsSentimentAnalyzer",
    "SentimentAnalyzer",
    "sentiment_analyzer",
    "NewsEntityMatcher",
    "EntityMatcher",
    "entity_matcher",
]
