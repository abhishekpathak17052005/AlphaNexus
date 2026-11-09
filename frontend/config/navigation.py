"""
ALPHANEXUS – Navigation Configuration
======================================
Defines the main navigation routes, sidebar labels, and icon associations.
"""

NAV_ITEMS = [
    {
        "id": "dashboard",
        "title": "Overview Dashboard",
        "icon": "📊",
        "path": "pages/1_📊_Overview_Dashboard.py",
        "description": "Market breadth, indices, watchlist, and platform status",
    },
    {
        "id": "company_research",
        "title": "Company Research",
        "icon": "🏢",
        "path": "pages/2_🏢_Company_Research.py",
        "description": "Deep corporate profiles, valuation ratios, and financial health",
    },
    {
        "id": "document_intelligence",
        "title": "Document Intelligence",
        "icon": "📄",
        "path": "pages/3_📄_Document_Intelligence.py",
        "description": "Upload, parse, chunk, and index annual reports and filings",
    },
    {
        "id": "ai_research_assistant",
        "title": "AI Research Assistant",
        "icon": "🤖",
        "path": "pages/4_🤖_AI_Research_Assistant.py",
        "description": "Grounded conversational financial QA with source citations",
    },
    {
        "id": "financial_analysis",
        "title": "Financial Analysis",
        "icon": "📈",
        "path": "pages/5_📈_Financial_Analysis.py",
        "description": "Interactive statements, DuPont breakdown, and peer benchmarks",
    },
    {
        "id": "news_events",
        "title": "News & Corporate Actions",
        "icon": "📰",
        "path": "pages/6_📰_News_and_Corporate_Actions.py",
        "description": "Real-time market news sentiment, insider deals, and dividends",
    },
    {
        "id": "forecasting",
        "title": "Performance Forecasting",
        "icon": "🔮",
        "path": "pages/7_🔮_Performance_Forecasting.py",
        "description": "Monte Carlo scenarios, bull/bear projections, and sensitivity analysis",
    },
    {
        "id": "rag_administration",
        "title": "RAG Administration",
        "icon": "⚙️",
        "path": "pages/8_⚙️_RAG_Administration.py",
        "description": "Vector store health, chunk inspectors, and retrieval benchmarks",
    },
]
