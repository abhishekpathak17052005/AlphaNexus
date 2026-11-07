-- EquiLens AI: Initial PostgreSQL + pgvector Migration Schema
-- Target: PostgreSQL 15+ / Supabase with pgvector extension

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255),
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'analyst',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 2. Companies (Indian Equities NSE/BSE + Global)
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    exchange VARCHAR(20) DEFAULT 'NSE',
    isin VARCHAR(50),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap NUMERIC(18, 2), -- INR Crores
    current_price NUMERIC(12, 2),
    day_change NUMERIC(10, 2),
    day_change_percent NUMERIC(8, 2),
    pe_ratio NUMERIC(10, 2),
    pb_ratio NUMERIC(10, 2),
    roe NUMERIC(8, 2),
    roce NUMERIC(8, 2),
    dividend_yield NUMERIC(8, 2),
    week_52_high NUMERIC(12, 2),
    week_52_low NUMERIC(12, 2),
    currency VARCHAR(10) DEFAULT 'INR',
    description TEXT,
    website VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE INDEX IF NOT EXISTS idx_companies_symbol ON companies(symbol);
CREATE INDEX IF NOT EXISTS idx_companies_sector ON companies(sector);
CREATE INDEX IF NOT EXISTS idx_companies_exchange ON companies(exchange);

-- 3. Company Identifiers
CREATE TABLE IF NOT EXISTS company_identifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    identifier_type VARCHAR(50) NOT NULL,
    identifier_value VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);
CREATE INDEX IF NOT EXISTS idx_comp_ident ON company_identifiers(identifier_type, identifier_value);

-- 4. Documents
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_hash VARCHAR(64),
    financial_year VARCHAR(20),
    document_type VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'UPLOADED',
    error_message TEXT,
    total_pages INTEGER DEFAULT 0,
    total_chunks INTEGER DEFAULT 0,
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);
CREATE INDEX IF NOT EXISTS idx_docs_company_fy ON documents(company_id, financial_year);

-- 5. Document Chunks with Vector Embeddings (BAAI/bge-small-en-v1.5 = 384 dimensions)
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    clean_text TEXT,
    section VARCHAR(100),
    page_number INTEGER,
    token_count INTEGER DEFAULT 0,
    embedding vector(384),
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);
CREATE INDEX IF NOT EXISTS idx_chunks_company_page ON document_chunks(company_id, page_number);

-- 6. Financial Statements
CREATE TABLE IF NOT EXISTS financial_statements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    statement_type VARCHAR(50) NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    financial_year VARCHAR(20) NOT NULL,
    quarter VARCHAR(10),
    period_end_date DATE NOT NULL,
    is_consolidated BOOLEAN DEFAULT TRUE,
    currency VARCHAR(10) DEFAULT 'INR',
    unit VARCHAR(20) DEFAULT 'INR_CRORES',
    raw_data JSONB DEFAULT '{}'::jsonb,
    is_audited BOOLEAN DEFAULT TRUE,
    source VARCHAR(100) DEFAULT 'NSE_FILING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 7. Financial Metrics
CREATE TABLE IF NOT EXISTS financial_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_category VARCHAR(50) NOT NULL,
    period_type VARCHAR(20) NOT NULL,
    financial_year VARCHAR(20) NOT NULL,
    quarter VARCHAR(10),
    period_end_date DATE NOT NULL,
    value NUMERIC(18, 4) NOT NULL,
    unit VARCHAR(20) DEFAULT 'INR_CRORES',
    currency VARCHAR(10) DEFAULT 'INR',
    yoy_growth NUMERIC(8, 2),
    qoq_growth NUMERIC(8, 2),
    is_consolidated BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 8. Stock Prices
CREATE TABLE IF NOT EXISTS stock_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    open NUMERIC(12, 2) NOT NULL,
    high NUMERIC(12, 2) NOT NULL,
    low NUMERIC(12, 2) NOT NULL,
    close NUMERIC(12, 2) NOT NULL,
    adjusted_close NUMERIC(12, 2),
    volume NUMERIC(18, 0) NOT NULL,
    vwap NUMERIC(12, 2),
    currency VARCHAR(10) DEFAULT 'INR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 9. News Articles
CREATE TABLE IF NOT EXISTS news_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) ON DELETE SET NULL,
    external_id VARCHAR(255) UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    content TEXT,
    url VARCHAR(1000) NOT NULL,
    source VARCHAR(100) DEFAULT 'Marketaux',
    publisher VARCHAR(150),
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    category VARCHAR(50) DEFAULT 'General',
    sentiment_label VARCHAR(20) DEFAULT 'Neutral',
    sentiment_score NUMERIC(5, 4),
    ai_summary TEXT,
    financial_impact TEXT,
    is_duplicate BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 10. Corporate Actions
CREATE TABLE IF NOT EXISTS corporate_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,
    details TEXT NOT NULL,
    ratio_or_amount VARCHAR(50),
    announcement_date DATE,
    ex_date DATE,
    record_date DATE,
    payment_date DATE,
    status VARCHAR(30) DEFAULT 'Announced',
    source VARCHAR(100) DEFAULT 'NSE_EXCHANGE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 11. Market Events & Deals
CREATE TABLE IF NOT EXISTS market_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    deal_value NUMERIC(18, 2),
    deal_currency VARCHAR(10) DEFAULT 'INR',
    counterparty VARCHAR(255),
    strategic_implications TEXT,
    disclosed_date DATE NOT NULL,
    source_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 12. Forecasts & Evaluations
CREATE TABLE IF NOT EXISTS forecasts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    model_version VARCHAR(20) DEFAULT '1.0',
    forecast_period VARCHAR(20) NOT NULL,
    target_date DATE NOT NULL,
    predicted_value NUMERIC(18, 4) NOT NULL,
    scenario VARCHAR(20) DEFAULT 'Base',
    confidence_interval_lower NUMERIC(18, 4),
    confidence_interval_upper NUMERIC(18, 4),
    confidence_level NUMERIC(4, 2) DEFAULT 0.95,
    assumptions JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE TABLE IF NOT EXISTS forecast_evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    model_type VARCHAR(50) NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    evaluation_date TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    train_start_date DATE NOT NULL,
    train_end_date DATE NOT NULL,
    test_start_date DATE NOT NULL,
    test_end_date DATE NOT NULL,
    mae NUMERIC(12, 4) NOT NULL,
    rmse NUMERIC(12, 4) NOT NULL,
    mape NUMERIC(8, 4),
    directional_accuracy NUMERIC(6, 2),
    sample_count INTEGER DEFAULT 0,
    features_used JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 13. Research Sessions, Messages, Citations
CREATE TABLE IF NOT EXISTS research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    company_id UUID REFERENCES companies(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE TABLE IF NOT EXISTS research_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES research_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    message_type VARCHAR(30) DEFAULT 'synthesis',
    token_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE TABLE IF NOT EXISTS citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES research_messages(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    document_chunk_id UUID REFERENCES document_chunks(id) ON DELETE SET NULL,
    chunk_index INTEGER,
    page_number INTEGER,
    section VARCHAR(100),
    excerpt TEXT NOT NULL,
    source_url VARCHAR(500),
    confidence_score NUMERIC(5, 4) DEFAULT 0.9500,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 14. Watchlists
CREATE TABLE IF NOT EXISTS watchlists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    target_price NUMERIC(12, 2),
    alert_threshold_percent NUMERIC(5, 2),
    notes VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    CONSTRAINT uq_user_company_watch UNIQUE (user_id, company_id)
);

