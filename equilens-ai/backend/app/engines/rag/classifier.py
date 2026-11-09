"""
EquiLens AI – Financial Document Classifier
============================================
Classifies uploaded documents into one of 11 categories using
keyword heuristics on filename + first-page text.

Classes:
  - Annual Report
  - Quarterly Result
  - Financial Statement
  - Investor Presentation
  - Earnings Call Transcript
  - Corporate Announcement
  - Acquisition Agreement
  - Business Contract
  - Research Report
  - Regulatory Disclosure
  - Other

Always returns a classification result with a confidence score.
If confidence is low (<0.5), the document is flagged for manual review.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from app.core.logging import logger


@dataclass
class ClassificationResult:
    document_type: str
    confidence: float              # 0.0 – 1.0
    needs_review: bool
    signals: List[str]             # human-readable evidence for the classification
    fallback: bool = False


# ---------------------------------------------------------------------------
# Keyword signal sets (ordered by specificity)
# ---------------------------------------------------------------------------

_TYPE_SIGNALS = {
    "Annual Report": {
        "filename": ["annual report", "annual_report", "ar20", "ar-20", "annualreport"],
        "text": [
            "annual report", "integrated annual report", "directors' report",
            "auditor's report", "chairman's message", "corporate governance report",
            "statement of profit and loss", "notes to accounts",
            "management discussion and analysis",
        ],
        "weight": 1.0,
    },
    "Quarterly Result": {
        "filename": ["q1", "q2", "q3", "q4", "quarterly", "qr", "results"],
        "text": [
            "quarterly financial results", "unaudited financial results",
            "q1 fy", "q2 fy", "q3 fy", "q4 fy", "quarter ended",
            "standalone unaudited", "standalone financial results",
        ],
        "weight": 1.0,
    },
    "Financial Statement": {
        "filename": ["financial_statement", "financials", "accounts", "balance_sheet"],
        "text": [
            "balance sheet", "statement of financial position",
            "cash flow statement", "statement of cash flows",
            "profit and loss account", "income statement",
            "total assets", "total liabilities", "shareholders equity",
        ],
        "weight": 0.85,
    },
    "Investor Presentation": {
        "filename": ["investor_pres", "investor-pres", "presentation", "roadshow", "ppt"],
        "text": [
            "investor presentation", "key highlights", "earnings highlights",
            "strategic priorities", "slide", "value creation",
            "market opportunity", "competitive landscape",
        ],
        "weight": 0.9,
    },
    "Earnings Call Transcript": {
        "filename": ["earnings_call", "concall", "conf_call", "transcript"],
        "text": [
            "earnings call", "conference call", "analyst call",
            "q&a session", "moderator:", "analyst:", "operator:",
            "good morning", "good evening", "thank you for joining",
        ],
        "weight": 1.0,
    },
    "Corporate Announcement": {
        "filename": ["announcement", "bse_filing", "nse_filing", "disclosure", "exchange_filing"],
        "text": [
            "board of directors", "outcome of board meeting",
            "trading window", "dividend declared", "record date",
            "book closure", "pursuant to sebi", "regulation 33",
            "regulation 30", "nse/bse",
        ],
        "weight": 0.9,
    },
    "Acquisition Agreement": {
        "filename": ["acquisition", "merger", "takeover", "scheme_of_arrangement"],
        "text": [
            "acquisition agreement", "scheme of arrangement",
            "definitive agreement", "purchase price", "completion of acquisition",
            "target company", "acquiree", "merger agreement",
        ],
        "weight": 1.0,
    },
    "Business Contract": {
        "filename": ["contract", "agreement", "mou", "loi"],
        "text": [
            "memorandum of understanding", "letter of intent",
            "contract for", "parties agree", "effective date of this agreement",
            "terms and conditions", "service agreement", "supply agreement",
        ],
        "weight": 0.85,
    },
    "Research Report": {
        "filename": ["research_report", "analyst_report", "initiating_coverage"],
        "text": [
            "initiating coverage", "buy", "sell", "hold",
            "target price", "price target", "our thesis",
            "recommendation", "analyst", "12-month target",
        ],
        "weight": 0.9,
    },
    "Regulatory Disclosure": {
        "filename": ["sebi", "rbi", "irdai", "drhp", "rhp", "prospectus"],
        "text": [
            "securities and exchange board", "reserve bank of india",
            "draft red herring prospectus", "red herring prospectus",
            "offer document", "ipo", "fpo", "regulatory",
        ],
        "weight": 0.95,
    },
}


class DocumentClassifier:
    """
    Rule-based document classifier for financial filings.
    Uses a weighted signal-matching approach on filename and first-page text.
    """

    def classify(
        self,
        filename: str,
        first_page_text: str = "",
        manual_hint: Optional[str] = None,
    ) -> ClassificationResult:
        """
        Classify a document by matching signals in filename and text.

        Args:
            filename: Original filename (lower-cased internally)
            first_page_text: Extracted text from first 1-2 pages
            manual_hint: If the user explicitly specified a document type, trust it

        Returns:
            ClassificationResult with type, confidence, and evidence signals
        """
        if manual_hint and manual_hint.strip():
            known_types = list(_TYPE_SIGNALS.keys()) + ["Other"]
            # Try exact match first (case-insensitive)
            for kt in known_types:
                if kt.lower() == manual_hint.lower():
                    return ClassificationResult(
                        document_type=kt,
                        confidence=1.0,
                        needs_review=False,
                        signals=[f"Manual override: {manual_hint}"],
                    )
            # Partial match
            for kt in known_types:
                if manual_hint.lower() in kt.lower() or kt.lower() in manual_hint.lower():
                    return ClassificationResult(
                        document_type=kt,
                        confidence=0.95,
                        needs_review=False,
                        signals=[f"Manual hint matched to: {kt}"],
                    )

        fn_lower = (filename or "").lower().replace("-", "_").replace(" ", "_")
        text_lower = (first_page_text or "").lower()[:3000]

        best_type = "Other"
        best_score = 0.0
        best_signals: List[str] = []

        for doc_type, cfg in _TYPE_SIGNALS.items():
            signals_found = []
            raw_score = 0.0

            # Filename signals (2x weight)
            for kw in cfg["filename"]:
                if kw in fn_lower:
                    raw_score += 2.0
                    signals_found.append(f"filename:'{kw}'")

            # Text signals (1x weight)
            for kw in cfg["text"]:
                if kw in text_lower:
                    raw_score += 1.0
                    signals_found.append(f"text:'{kw}'")

            # Apply type-level weight
            weighted = raw_score * cfg.get("weight", 1.0)

            if weighted > best_score:
                best_score = weighted
                best_type = doc_type
                best_signals = signals_found

        # Normalise to 0-1 confidence (heuristic cap)
        confidence = min(1.0, best_score / 8.0)
        needs_review = confidence < 0.4

        if best_type == "Other" or best_score == 0:
            needs_review = True

        logger.debug(
            f"[Classifier] '{filename}' → {best_type} "
            f"(score={best_score:.1f}, conf={confidence:.2f})"
        )

        return ClassificationResult(
            document_type=best_type,
            confidence=confidence,
            needs_review=needs_review,
            signals=best_signals[:6],  # top 6 for explainability
            fallback=(best_type == "Other"),
        )


document_classifier = DocumentClassifier()
