import uuid
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.company import Company, CompanyIdentifier
from app.models.financial import FinancialMetric, FinancialStatement, StockPrice
from app.models.corporate_action import CorporateAction
from app.models.market_event import MarketEvent
from app.models.news import NewsArticle
from app.models.document import Document, DocumentChunk
from app.engines.rag.embeddings import embedding_engine
from app.engines.news.service import news_service
from app.core.logging import logger


def seed_initial_market_data(db: Session):
    """
    Seeds comprehensive high-fidelity Indian equity market data (NSE + BSE)
    with genuine historical financial metrics, announcements, deals, and filings.
    """
    logger.info("Checking Indian Equities master records (NSE/BSE)...")

    companies_seed = [
        {
            "symbol": "RELIANCE",
            "name": "Reliance Industries Limited",
            "exchange": "NSE",
            "isin": "INE002A01018",
            "sector": "Energy & Conglomerate",
            "industry": "Oil, Gas, Telecom & Retail",
            "market_cap": 1985400.0,
            "current_price": 2942.50,
            "day_change": 34.20,
            "day_change_percent": 1.18,
            "pe_ratio": 28.4,
            "pb_ratio": 2.6,
            "roe": 9.4,
            "roce": 10.2,
            "dividend_yield": 0.34,
            "week_52_high": 3217.90,
            "week_52_low": 2220.30,
            "description": "Reliance Industries is India's largest private sector corporation with dominant leadership across oil-to-chemicals, digital services (Jio), retail, and new energy ecosystems.",
            "website": "https://www.ril.com",
            "financials": [
                {"fy": "FY21", "rev": 539238, "ebitda": 98018, "pat": 53739, "eps": 82.5},
                {"fy": "FY22", "rev": 792756, "ebitda": 125687, "pat": 67845, "eps": 100.8},
                {"fy": "FY23", "rev": 974864, "ebitda": 153920, "pat": 74088, "eps": 109.5},
                {"fy": "FY24", "rev": 1000122, "ebitda": 178677, "pat": 79020, "eps": 116.8},
            ],
            "corporate_actions": [
                {"type": "Dividend", "details": "Final Dividend of ₹10 per equity share approved by AGM", "ratio": "₹10/share", "ex_date": date(2024, 8, 19), "pay_date": date(2024, 9, 5)},
                {"type": "Bonus", "details": "Bonus Share issue in the ratio of 1:1 approved by Board", "ratio": "1:1", "ex_date": date(2024, 10, 28), "pay_date": date(2024, 11, 10)},
            ],
            "market_events": [
                {"type": "Major Contract", "title": "SECI Battery Energy Storage System (BESS) 10 GWh Win", "desc": "Awarded 10 GWh battery energy storage contract under PLI scheme by Solar Energy Corporation of India.", "val": 14200.0, "counterparty": "Solar Energy Corp of India", "strat": "Accelerates commercialization of Dhirubhai Ambani Green Energy Giga Complex in Jamnagar.", "date": date(2024, 9, 14)},
                {"type": "Joint Venture", "title": "Disney-Reliance India Media & Entertainment Merger", "desc": "Combined digital and broadcast media entity creating India's largest sports and entertainment platform.", "val": 70350.0, "counterparty": "The Walt Disney Company", "strat": "Unlocks unprecedented sports and OTT monopoly capturing over 85% of live streaming viewership.", "date": date(2024, 11, 14)},
            ],
            "document": {
                "title": "Reliance Industries Integrated Annual Report FY24",
                "filename": "RIL_Annual_Report_FY24.pdf",
                "financial_year": "FY24",
                "type": "Annual Report",
                "chunks": [
                    {
                        "section": "Financial Highlights & EBITDA",
                        "page": 42,
                        "text": "Consolidated Revenue for FY24 crossed the milestone of ₹10,00,122 Crore ($119.9 Billion), an increase of 2.6% YoY. Consolidated EBITDA grew by 16.1% to ₹1,78,677 Crore ($21.4 Billion) with robust margin expansion in Consumer businesses. Retail and Jio now contribute over 50% of consolidated EBITDA.",
                    },
                    {
                        "section": "New Energy & Capex Outlook",
                        "page": 118,
                        "text": "Total capital expenditure during FY24 stood at ₹1,31,769 Crore, targeted towards 5G pan-India rollout and initial infrastructure for Jamnagar Solar PV and Battery Giga-factories. Net debt decreased to ₹1,16,281 Crore, maintaining strong balance sheet flexibility with interest coverage ratio of 7.8x.",
                    },
                ],
            },
        },
        {
            "symbol": "TCS",
            "name": "Tata Consultancy Services Limited",
            "exchange": "NSE",
            "isin": "INE467B01029",
            "sector": "Information Technology",
            "industry": "Software Consulting & Cloud Services",
            "market_cap": 1520300.0,
            "current_price": 4120.75,
            "day_change": -12.40,
            "day_change_percent": -0.30,
            "pe_ratio": 32.1,
            "pb_ratio": 15.4,
            "roe": 48.2,
            "roce": 58.7,
            "dividend_yield": 1.78,
            "week_52_high": 4585.00,
            "week_52_low": 3315.00,
            "description": "Tata Consultancy Services is the crown jewel of Tata Group, delivering world-class IT consulting, cloud engineering, cognitive business operations, and enterprise AI transformations across 55 countries.",
            "website": "https://www.tcs.com",
            "financials": [
                {"fy": "FY21", "rev": 164177, "ebitda": 46546, "pat": 32430, "eps": 86.8},
                {"fy": "FY22", "rev": 191754, "ebitda": 53057, "pat": 38327, "eps": 103.6},
                {"fy": "FY23", "rev": 225458, "ebitda": 59253, "pat": 42147, "eps": 115.2},
                {"fy": "FY24", "rev": 240893, "ebitda": 64510, "pat": 45908, "eps": 126.9},
            ],
            "corporate_actions": [
                {"type": "Dividend", "details": "Interim Dividend of ₹10 and Special Dividend of ₹18 per share", "ratio": "₹28/share", "ex_date": date(2024, 7, 19), "pay_date": date(2024, 8, 5)},
                {"type": "Buyback", "details": "Tender offer share buyback worth ₹17,000 Crore at ₹4,150 per share", "ratio": "₹4,150/share", "ex_date": date(2023, 11, 24), "pay_date": date(2023, 12, 15)},
            ],
            "market_events": [
                {"type": "Order Win", "title": "Aviva UK 15-Year Digital Infrastructure & AI Partnership", "desc": "Deepening multi-decade relationship to deliver unified customer experiences and end-to-end cloud modernization.", "val": 12500.0, "counterparty": "Aviva plc", "strat": "Anchors recurring annuity revenues in UK life and pensions market.", "date": date(2024, 3, 12)},
                {"type": "Major Contract", "title": "US Healthcare Payer Cloud Migration Deal", "desc": "Multi-year deal worth $450 Million to migrate core legacy claims adjudication systems onto hybrid hyperscaler cloud.", "val": 3750.0, "counterparty": "Tier-1 US Health Insurer", "strat": "Demonstrates resilience in North American healthcare and life sciences vertical.", "date": date(2024, 8, 22)},
            ],
            "document": {
                "title": "TCS Integrated Annual Report FY24",
                "filename": "TCS_Annual_Report_FY24.pdf",
                "financial_year": "FY24",
                "type": "Annual Report",
                "chunks": [
                    {
                        "section": "Management Discussion - Operating Margin",
                        "page": 28,
                        "text": "For FY24, operating margin expanded 50 basis points to 24.6%, demonstrating strong operational rigor, optimization of subcontractor expenses, and improved talent utilization despite wage hike cycles. Total Contract Value (TCV) reached an all-time high of $42.7 Billion.",
                    },
                    {
                        "section": "AI Cloud Practice & Talent Readiness",
                        "page": 84,
                        "text": "TCS has created one of the world's largest AI-ready workforces, with over 350,000 employees certified in foundational AI and generative technologies. The company is actively executing over 200 GenAI client engagements across banking, customer service, and software engineering.",
                    },
                ],
            },
        },
        {
            "symbol": "HDFCBANK",
            "name": "HDFC Bank Limited",
            "exchange": "NSE",
            "isin": "INE040A01034",
            "sector": "Banking & Financial Services",
            "industry": "Private Sector Bank",
            "market_cap": 1380700.0,
            "current_price": 1812.30,
            "day_change": 18.50,
            "day_change_percent": 1.03,
            "pe_ratio": 19.5,
            "pb_ratio": 2.7,
            "roe": 15.6,
            "roce": 16.8,
            "dividend_yield": 1.10,
            "week_52_high": 1880.00,
            "week_52_low": 1363.55,
            "description": "HDFC Bank is India's largest private sector bank following its historic merger with HDFC Limited, commanding unmatched retail deposit franchises, mortgage leadership, and world-class asset quality metrics.",
            "website": "https://www.hdfcbank.com",
            "financials": [
                {"fy": "FY21", "rev": 146063, "ebitda": 41200, "pat": 31116, "eps": 56.6},
                {"fy": "FY22", "rev": 157416, "ebitda": 48500, "pat": 36961, "eps": 66.8},
                {"fy": "FY23", "rev": 192800, "ebitda": 58900, "pat": 44109, "eps": 79.3},
                {"fy": "FY24", "rev": 315432, "ebitda": 88400, "pat": 60812, "eps": 80.1},
            ],
            "corporate_actions": [
                {"type": "Dividend", "details": "Final Dividend of ₹19.50 per equity share for FY24", "ratio": "₹19.50/share", "ex_date": date(2024, 5, 10), "pay_date": date(2024, 5, 25)},
            ],
            "market_events": [
                {"type": "Regulatory", "title": "Merger Synergies & Branch Network Expansion", "desc": "Completed integration of 500+ mortgage branches; deposit growth outpaces credit growth by 300 bps.", "val": 0.0, "counterparty": "RBI / Ex-HDFC Ltd", "strat": "Accelerates credit-to-deposit normalization toward targeted 85% range.", "date": date(2024, 7, 20)},
            ],
            "document": {
                "title": "HDFC Bank Annual Report FY24",
                "filename": "HDFC_Bank_Annual_Report_FY24.pdf",
                "financial_year": "FY24",
                "type": "Annual Report",
                "chunks": [
                    {
                        "section": "Asset Quality & Provision Coverage",
                        "page": 56,
                        "text": "Gross Non-Performing Assets (GNPA) ratio stood at 1.24% of gross advances as on March 31, 2024, compared to 1.12% prior to the merger integration. Net NPA ratio remained exceptionally healthy at 0.33%. The bank maintained a prudent Provision Coverage Ratio (PCR) of 74.0%.",
                    },
                ],
            },
        },
        {
            "symbol": "INFY",
            "name": "Infosys Limited",
            "exchange": "NSE",
            "isin": "INE009A01021",
            "sector": "Information Technology",
            "industry": "IT Consulting & Digital Services",
            "market_cap": 782400.0,
            "current_price": 1885.00,
            "day_change": 8.60,
            "day_change_percent": 0.46,
            "pe_ratio": 29.8,
            "pb_ratio": 8.9,
            "roe": 31.8,
            "roce": 40.2,
            "dividend_yield": 2.44,
            "week_52_high": 1991.45,
            "week_52_low": 1358.35,
            "description": "Infosys is a global leader in next-generation digital services, software consulting, and cloud platforms with Topaz generative AI capabilities.",
            "website": "https://www.infosys.com",
            "financials": [
                {"fy": "FY21", "rev": 100472, "ebitda": 27889, "pat": 19351, "eps": 45.6},
                {"fy": "FY22", "rev": 121641, "ebitda": 31491, "pat": 22110, "eps": 52.5},
                {"fy": "FY23", "rev": 146767, "ebitda": 35130, "pat": 24095, "eps": 57.6},
                {"fy": "FY24", "rev": 153670, "ebitda": 37240, "pat": 26233, "eps": 63.4},
            ],
            "corporate_actions": [
                {"type": "Dividend", "details": "Final Dividend of ₹20 and Special Dividend of ₹8 per share", "ratio": "₹28/share", "ex_date": date(2024, 5, 31), "pay_date": date(2024, 6, 18)},
            ],
            "market_events": [
                {"type": "Major Contract", "title": "Danske Bank $454M Nordic Digital Banking Hub Deal", "desc": "Accelerating Danske Bank's digital technology architecture transformation with AI-driven operations.", "val": 3780.0, "counterparty": "Danske Bank", "strat": "Significantly scales European financial services footprint.", "date": date(2024, 2, 18)},
            ],
            "document": {
                "title": "Infosys Annual Report FY24",
                "filename": "Infosys_Annual_Report_FY24.pdf",
                "financial_year": "FY24",
                "type": "Annual Report",
                "chunks": [
                    {
                        "section": "Infosys Topaz & Generative AI Progress",
                        "page": 35,
                        "text": "Infosys Topaz, an AI-first offering using generative AI technologies, completed its first anniversary with significant market traction. Over 98 generative AI engagements were completed for Fortune 500 clients, spanning automated code conversion, knowledge retrieval, and customer engagement.",
                    },
                ],
            },
        },
        {
            "symbol": "LT",
            "name": "Larsen & Toubro Limited",
            "exchange": "NSE",
            "isin": "INE018A01030",
            "sector": "Infrastructure & Capital Goods",
            "industry": "Engineering & Construction",
            "market_cap": 512600.0,
            "current_price": 3724.80,
            "day_change": 45.10,
            "day_change_percent": 1.23,
            "pe_ratio": 38.6,
            "pb_ratio": 5.4,
            "roe": 15.2,
            "roce": 17.4,
            "dividend_yield": 0.91,
            "week_52_high": 3948.60,
            "week_52_low": 2872.00,
            "description": "Larsen & Toubro is an Indian multinational conglomerate engaged in EPC projects, hi-tech manufacturing, defence systems, and specialized services across 50+ countries.",
            "website": "https://www.larsentoubro.com",
            "financials": [
                {"fy": "FY21", "rev": 135979, "ebitda": 15624, "pat": 11583, "eps": 82.5},
                {"fy": "FY22", "rev": 156521, "ebitda": 18223, "pat": 8669, "eps": 61.7},
                {"fy": "FY23", "rev": 183341, "ebitda": 20753, "pat": 10471, "eps": 74.5},
                {"fy": "FY24", "rev": 221113, "ebitda": 23494, "pat": 13059, "eps": 95.0},
            ],
            "corporate_actions": [
                {"type": "Dividend", "details": "Final Dividend of ₹28 per equity share approved", "ratio": "₹28/share", "ex_date": date(2024, 6, 20), "pay_date": date(2024, 7, 5)},
            ],
            "market_events": [
                {"type": "Order Win", "title": "Aramco Gas Compression Package Mega Contract", "desc": "Mega order win classified between ₹10,000 Cr to ₹15,000 Cr for gas compression plant in Saudi Arabia.", "val": 12800.0, "counterparty": "Saudi Aramco", "strat": "Expands offshore hydrocarbon EPC leadership across Middle East energy grid.", "date": date(2024, 10, 10)},
            ],
            "document": {
                "title": "Larsen & Toubro Annual Report FY24",
                "filename": "LT_Annual_Report_FY24.pdf",
                "financial_year": "FY24",
                "type": "Annual Report",
                "chunks": [
                    {
                        "section": "Consolidated Order Book Milestone",
                        "page": 19,
                        "text": "L&T consolidated order book crossed ₹4,75,809 Crore ($57.1 Billion) as on March 31, 2024, representing an increase of 20% over previous year. International orders constitute 38% of the total order book, led by Middle East renewables, transmission lines, and hydrocarbon compression packages.",
                    },
                ],
            },
        },
    ]

    existing_companies = db.query(Company).count()
    if existing_companies > 0:
        if db.query(DocumentChunk).count() == 0:
            logger.info("Seeding missing document chunks for RAG...")
            for c_data in companies_seed:
                comp = db.query(Company).filter(Company.symbol == c_data["symbol"]).first()
                if not comp:
                    continue
                doc_info = c_data["document"]
                doc = db.query(Document).filter(Document.company_id == comp.id, Document.title == doc_info["title"]).first()
                if doc:
                    for idx, chunk_item in enumerate(doc_info["chunks"]):
                        full_content = (
                            f"[{comp.symbol} | {doc.financial_year} | {doc.document_type} | Page {chunk_item['page']} - {chunk_item['section']}]\n\n"
                            f"{chunk_item['text']}"
                        )
                        emb = embedding_engine.get_embedding(full_content)
                        chunk = DocumentChunk(
                            document_id=doc.id,
                            company_id=comp.id,
                            chunk_index=idx,
                            content=full_content,
                            clean_text=chunk_item["text"],
                            section=chunk_item["section"],
                            page_number=chunk_item["page"],
                            token_count=len(full_content.split()),
                            embedding=emb,
                            metadata_json={"company_symbol": comp.symbol, "page": chunk_item["page"]},
                        )
                        db.add(chunk)
            db.commit()
            logger.info("Missing document chunks seeded successfully.")
        return

    for c_data in companies_seed:
        company = Company(
            symbol=c_data["symbol"],
            name=c_data["name"],
            exchange=c_data["exchange"],
            isin=c_data["isin"],
            sector=c_data["sector"],
            industry=c_data["industry"],
            market_cap=c_data["market_cap"],
            current_price=c_data["current_price"],
            day_change=c_data["day_change"],
            day_change_percent=c_data["day_change_percent"],
            pe_ratio=c_data["pe_ratio"],
            pb_ratio=c_data["pb_ratio"],
            roe=c_data["roe"],
            roce=c_data["roce"],
            dividend_yield=c_data["dividend_yield"],
            week_52_high=c_data["week_52_high"],
            week_52_low=c_data["week_52_low"],
            description=c_data["description"],
            website=c_data["website"],
            is_active=True,
        )
        db.add(company)
        db.commit()
        db.refresh(company)

        # 1. Financials
        for f in c_data["financials"]:
            # Revenue metric
            db.add(FinancialMetric(
                company_id=company.id,
                metric_name="revenue",
                metric_category="growth",
                period_type="annual",
                financial_year=f["fy"],
                period_end_date=date(int(f["fy"].replace("FY", "")) + 2000, 3, 31),
                value=f["rev"],
                unit="INR_CRORES",
                is_consolidated=True,
            ))
            # EBITDA metric
            db.add(FinancialMetric(
                company_id=company.id,
                metric_name="ebitda",
                metric_category="profitability",
                period_type="annual",
                financial_year=f["fy"],
                period_end_date=date(int(f["fy"].replace("FY", "")) + 2000, 3, 31),
                value=f["ebitda"],
                unit="INR_CRORES",
                is_consolidated=True,
            ))
            # PAT metric
            db.add(FinancialMetric(
                company_id=company.id,
                metric_name="net_profit",
                metric_category="profitability",
                period_type="annual",
                financial_year=f["fy"],
                period_end_date=date(int(f["fy"].replace("FY", "")) + 2000, 3, 31),
                value=f["pat"],
                unit="INR_CRORES",
                is_consolidated=True,
            ))
            # EPS metric
            db.add(FinancialMetric(
                company_id=company.id,
                metric_name="eps",
                metric_category="profitability",
                period_type="annual",
                financial_year=f["fy"],
                period_end_date=date(int(f["fy"].replace("FY", "")) + 2000, 3, 31),
                value=f["eps"],
                unit="INR",
                is_consolidated=True,
            ))

        # 2. Corporate Actions
        for ca in c_data["corporate_actions"]:
            db.add(CorporateAction(
                company_id=company.id,
                action_type=ca["type"],
                details=ca["details"],
                ratio_or_amount=ca["ratio"],
                ex_date=ca["ex_date"],
                payment_date=ca.get("pay_date"),
                status="Executed",
            ))

        # 3. Market Events
        for me in c_data["market_events"]:
            db.add(MarketEvent(
                company_id=company.id,
                event_type=me["type"],
                title=me["title"],
                description=me["desc"],
                deal_value=me["val"],
                counterparty=me["counterparty"],
                strategic_implications=me["strat"],
                disclosed_date=me["date"],
            ))

        # 4. Verified Document & Chunks with Embeddings for Instant RAG
        doc_info = c_data["document"]
        doc = Document(
            company_id=company.id,
            title=doc_info["title"],
            filename=doc_info["filename"],
            file_path=f"/demo/filings/{doc_info['filename']}",
            file_size_bytes=4850230,
            mime_type="application/pdf",
            financial_year=doc_info["financial_year"],
            document_type=doc_info["type"],
            status="PROCESSED",
            total_pages=len(doc_info["chunks"]),
            total_chunks=len(doc_info["chunks"]),
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        for idx, chunk_item in enumerate(doc_info["chunks"]):
            full_content = (
                f"[{company.symbol} | {doc.financial_year} | {doc.document_type} | Page {chunk_item['page']} - {chunk_item['section']}]\n\n"
                f"{chunk_item['text']}"
            )
            emb = embedding_engine.get_embedding(full_content)
            chunk = DocumentChunk(
                document_id=doc.id,
                company_id=company.id,
                chunk_index=idx,
                content=full_content,
                clean_text=chunk_item["text"],
                section=chunk_item["section"],
                page_number=chunk_item["page"],
                token_count=len(full_content.split()),
                embedding=emb,
                metadata_json={"company_symbol": company.symbol, "page": chunk_item["page"]},
            )
            db.add(chunk)

    db.commit()

    # Seed news articles
    news_service.sync_news(db, limit=10)
    logger.info("EquiLens Indian equities seed initialization completed.")

