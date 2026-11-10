# ALPHANEXUS – News & Event Intelligence Engine

## 1. Overview

The News Intelligence Engine pulls corporate news feeds, categorizes material events, and computes confidence-weighted sentiment scores.

---

## 2. Key Modules

- **Provider Integration:** Connects to Marketaux API for Indian and global equities.
- **Event Classifier:** Identifies critical corporate catalysts:
  - M&A / Mergers & Acquisitions
  - Board Resolutions & Dividends
  - Earnings Announcements
  - Credit Rating Upgrades/Downgrades
  - Regulatory / Legal Inquiries
- **Lexicon Sentiment Scoring:** Analyzes headline and summary sentiment using a domain-specific financial dictionary, avoiding false positives common in general-purpose NLP libraries.

