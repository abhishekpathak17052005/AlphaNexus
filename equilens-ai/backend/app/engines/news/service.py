import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.news import NewsArticle
from app.models.company import Company
from app.engines.providers.marketaux import MarketauxProvider
from app.engines.providers.gemini import GeminiProvider
from app.engines.news.entity_matcher import NewsEntityMatcher
from app.engines.news.classifier import NewsEventClassifier
from app.engines.news.sentiment import NewsSentimentAnalyzer
from app.core.config import settings
from app.core.logging import logger


class NewsService:
    """
    Independent News Intelligence Engine for EquiLens AI.
    Handles multi-source news ingestion, deduplication, entity extraction,
    category classification, sentiment analysis, AI executive summaries, and persistence.
    """

    def __init__(self):
        self.provider = MarketauxProvider()
        self.gemini_provider = GeminiProvider()

    def process_and_store_article(
        self,
        db: Session,
        article_data: Dict[str, Any],
        active_companies: Optional[List[Company]] = None,
    ) -> Optional[NewsArticle]:
        """Validates, classifies, analyzes, deduplicates, and stores an article."""
        title = article_data.get("title", "").strip()
        url = article_data.get("url", "").strip()
        if not title or not url:
            return None

        # Check for duplicates by URL or external_id
        external_id = article_data.get("uuid") or hashlib.sha256(url.encode()).hexdigest()
        existing = db.query(NewsArticle).filter(
            (NewsArticle.external_id == external_id) | (NewsArticle.url == url)
        ).first()
        if existing:
            return existing

        description = article_data.get("description", "")
        content = article_data.get("content", "")

        # Entity Matching
        if active_companies is None:
            active_companies = db.query(Company).filter(Company.is_active == True).all()

        matched_company = NewsEntityMatcher.match_company(
            text=f"{description} {content}",
            title=title,
            companies=active_companies,
        )

        # Classification & Sentiment
        category = NewsEventClassifier.classify(title, description)
        sentiment_res = NewsSentimentAnalyzer.analyze(title, description)

        # Published date parsing
        pub_raw = article_data.get("published_at")
        try:
            if isinstance(pub_raw, str):
                published_at = datetime.fromisoformat(pub_raw.replace("Z", "+00:00"))
            elif isinstance(pub_raw, datetime):
                published_at = pub_raw
            else:
                published_at = datetime.utcnow()
        except Exception:
            published_at = datetime.utcnow()

        # AI Summary (Generative or structured heuristic synthesis)
        ai_summary = article_data.get("ai_summary")
        financial_impact = article_data.get("financial_impact")

        if not ai_summary:
            company_mention = matched_company.name if matched_company else "Industry participant"
            ai_summary = f"{company_mention} featured in {category} announcement: {title}. {description[:200]}"
            financial_impact = f"Potential impact on {category.lower()} metrics for {matched_company.symbol if matched_company else 'sector'}."

        article = NewsArticle(
            company_id=matched_company.id if matched_company else None,
            external_id=external_id,
            title=title,
            description=description,
            content=content,
            url=url,
            source=article_data.get("source", "Marketaux"),
            publisher=article_data.get("publisher", "Financial Press"),
            published_at=published_at,
            category=category,
            sentiment_label=sentiment_res["label"],
            sentiment_score=sentiment_res["score"],
            ai_summary=ai_summary,
            financial_impact=financial_impact,
            is_duplicate=False,
        )

        db.add(article)
        db.commit()
        db.refresh(article)
        return article

    def sync_news(self, db: Session, limit: int = 15) -> Dict[str, Any]:
        """
        Syncs news from Marketaux API or applies curated fixtures when credentials are absent.
        """
        active_companies = db.query(Company).filter(Company.is_active == True).all()
        symbols = [c.symbol for c in active_companies if c.symbol]

        raw_articles = []
        is_live = False

        if self.provider.is_configured:
            raw_articles = self.provider.fetch_news(symbols=symbols[:10], limit=limit)
            is_live = True

        if not raw_articles and settings.DATA_MODE == "demo":
            # Seed curated high-fidelity demonstration fixtures
            raw_articles = self._get_demo_articles()

        stored_count = 0
        for art in raw_articles:
            res = self.process_and_store_article(db, art, active_companies)
            if res:
                stored_count += 1

        return {
            "synced_count": stored_count,
            "is_live_provider": is_live,
            "provider_status": self.provider.check_availability(),
        }

    @staticmethod
    def _get_demo_articles() -> List[Dict[str, Any]]:
        return [
            {
                "uuid": "mkt-rel-001",
                "title": "Reliance Industries bags ₹14,200 Cr green energy storage contract from SECI",
                "description": "Reliance New Energy secures landmark commercial contract for battery energy storage systems over 25 years.",
                "url": "https://economictimes.indiatimes.com/industry/energy/reliance-green-energy-contract",
                "source": "Economic Times",
                "publisher": "ET Bureau",
                "published_at": datetime.utcnow().isoformat(),
                "ai_summary": "Reliance New Energy awarded ₹14,200 Cr contract from SECI. Solidifies green energy capex conversion into contracted revenue.",
                "financial_impact": "Expected to contribute approximately 1.5% to annual EBITDA upon phased commissioning from FY26.",
            },
            {
                "uuid": "mkt-tcs-002",
                "title": "TCS expands cloud transformation partnership with European banking giant in $850M deal",
                "description": "Tata Consultancy Services signs multi-year digital core transformation agreement with tier-1 European lender.",
                "url": "https://www.livemint.com/companies/news/tcs-signs-850-million-european-deal",
                "source": "LiveMint",
                "publisher": "Tech Wire",
                "published_at": datetime.utcnow().isoformat(),
                "ai_summary": "TCS wins $850M deal over 7 years with European financial institution, strengthening BFSI order book.",
                "financial_impact": "Supports FY26 revenue visibility in European BFSI segment with estimated 25% operating margins.",
            },
            {
                "uuid": "mkt-hdfc-003",
                "title": "HDFC Bank posts 16.8% YoY net profit growth for Q3; Gross NPA improves to 1.24%",
                "description": "HDFC Bank delivered robust quarterly results with net interest income rising to ₹28,450 Cr and stable net interest margins.",
                "url": "https://www.business-standard.com/finance/news/hdfc-bank-q3-results",
                "source": "Business Standard",
                "publisher": "Banking Desk",
                "published_at": datetime.utcnow().isoformat(),
                "ai_summary": "HDFC Bank reported 16.8% YoY profit increase in Q3 with Gross NPA dropping to 1.24% and NIM holding at 3.4%.",
                "financial_impact": "Affirms post-merger balance sheet consolidation and steady credit cost trajectory.",
            },
            {
                "uuid": "mkt-infy-004",
                "title": "Infosys raises full-year constant currency revenue guidance to 4.5% - 5.0%",
                "description": "Infosys announces upward revision in constant currency guidance driven by strong generative AI contract ramp-ups.",
                "url": "https://www.moneycontrol.com/news/business/earnings/infosys-guidance-upgrade",
                "source": "Moneycontrol",
                "publisher": "MC Research",
                "published_at": datetime.utcnow().isoformat(),
                "ai_summary": "Infosys increased annual CC revenue forecast following 5 mega deal signings in North America.",
                "financial_impact": "Positive surprise for consensus estimates; projected operating margin band maintained at 20-22%.",
            },
        ]


news_service = NewsService()

