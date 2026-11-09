"""
ALPHANEXUS – News Event Classifier
==================================
Categorizes headlines into Earnings, M&A, Management Changes, Regulatory, and Contracts.
"""

from app.engines.news.classifier import NewsEventClassifier

EventClassifier = NewsEventClassifier
event_classifier = NewsEventClassifier()

__all__ = ["NewsEventClassifier", "EventClassifier", "event_classifier"]
