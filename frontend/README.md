# ALPHANEXUS Frontend – Liquid Glass Financial Terminal

AI-powered financial intelligence and equity research workspace for **ALPHANEXUS** ("See Beyond the Stock Price"). Built on Streamlit, Plotly, custom Liquid Glass CSS design tokens, and React Vite components.

---

## Architecture

```
frontend/
├── streamlit_app.py         # Primary Streamlit application entrypoint
├── config/                  # Configuration, themes, tokens, and navigation
│   ├── settings.py          # Backend endpoints and market defaults
│   ├── theme.py             # Color palettes
│   ├── design_tokens.py     # Translucent glass filters & radii
│   └── navigation.py        # Workspace pages routing table
├── api/                     # Type-safe API client wrappers
│   ├── client.py            # HTTP client with retry and error handling
│   ├── auth.py              # Session and analyst login
│   ├── companies.py         # Directory and ticker search
│   ├── documents.py         # Document upload and indexing API
│   ├── rag.py               # RAG query and retrieval benchmark API
│   ├── financials.py        # Financial statements and DuPont analysis
│   ├── news.py              # Marketaux news and sentiment
│   └── forecasting.py       # Monte Carlo and econometric projections
├── pages/                   # Multi-page analyst workspaces
│   ├── 1_📊_Overview_Dashboard.py
│   ├── 2_🏢_Company_Research.py
│   ├── 3_📄_Document_Intelligence.py
│   ├── 4_🤖_AI_Research_Assistant.py
│   ├── 5_📈_Financial_Analysis.py
│   ├── 6_📰_News_and_Corporate_Actions.py
│   ├── 7_🔮_Performance_Forecasting.py
│   └── 8_⚙️_RAG_Administration.py
├── components/              # Reusable UI component modules
│   ├── navbar/              # Top ticker bar
│   ├── sidebar/             # Company selection and workspace navigation
│   ├── cards/               # Liquid glass metric cards
│   ├── buttons/             # Translucent action triggers
│   ├── inputs/              # Search fields
│   ├── charts/              # Plotly financial visualizations
│   ├── tables/              # Formatted data tables
│   ├── chat/                # Evidentiary citation chat bubbles
│   ├── citations/           # Source document snippet inspector
│   ├── document_cards/      # Ingestion status and metadata cards
│   └── notifications/       # Toast and alert banners
├── custom_components/       # Bi-directional Streamlit React components
│   └── liquid_navigation/   # Floating frosted glass navigation pill
├── styles/                  # Modular CSS stylesheets
└── assets/                  # Logos, icons, and image resources
```

---

## Launching the Frontend

```bash
# Start Streamlit application
streamlit run streamlit_app.py --server.port 8501
```
