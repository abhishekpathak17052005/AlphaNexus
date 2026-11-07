export interface Company {
  id: string;
  symbol: string;
  name: string;
  exchange: 'NSE' | 'BSE' | string;
  isin?: string;
  sector?: string;
  industry?: string;
  market_cap?: number;
  current_price?: number;
  day_change?: number;
  day_change_percent?: number;
  pe_ratio?: number;
  pb_ratio?: number;
  roe?: number;
  roce?: number;
  dividend_yield?: number;
  week_52_high?: number;
  week_52_low?: number;
  currency: string;
  description?: string;
  website?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface FinancialMetric {
  id: string;
  company_id: string;
  metric_name: string;
  metric_category: string;
  period_type: string;
  financial_year: string;
  quarter?: string;
  period_end_date: string;
  value: number;
  unit: string;
  currency: string;
  yoy_growth?: number;
  qoq_growth?: number;
  is_consolidated: boolean;
}

export interface DocumentItem {
  id: string;
  company_id: string;
  title: string;
  filename: string;
  file_size_bytes: number;
  mime_type: string;
  financial_year?: string;
  document_type: string;
  status: 'UPLOADED' | 'QUEUED' | 'PROCESSING' | 'PROCESSED' | 'FAILED';
  error_message?: string;
  total_pages: number;
  total_chunks: number;
  created_at: string;
}

export interface CitationItem {
  id?: string;
  document_id?: string;
  document_chunk_id?: string;
  document_title?: string;
  page_number?: number;
  section?: string;
  excerpt: string;
  source_url?: string;
  confidence_score: number;
}

export interface ResearchMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  message_type: 'fact_grounded' | 'calculated' | 'synthesis' | 'user_query';
  tokens_used: number;
  citations: CitationItem[];
  created_at: string;
}

export interface ResearchSession {
  id: string;
  title: string;
  company_id?: string;
  created_at: string;
  updated_at: string;
  messages: ResearchMessage[];
}

export interface NewsArticle {
  id: string;
  company_id?: string;
  title: string;
  description?: string;
  content?: string;
  url: string;
  source: string;
  publisher?: string;
  published_at: string;
  category: string;
  sentiment_label: 'Positive' | 'Negative' | 'Neutral';
  sentiment_score?: number;
  ai_summary?: string;
  financial_impact?: string;
  created_at: string;
}

export interface CorporateAction {
  id: string;
  company_id: string;
  action_type: string;
  details: string;
  ratio_or_amount?: string;
  announcement_date?: string;
  ex_date?: string;
  record_date?: string;
  payment_date?: string;
  status: string;
  source: string;
  created_at: string;
}

export interface MarketEvent {
  id: string;
  company_id: string;
  event_type: string;
  title: string;
  description: string;
  deal_value?: number;
  deal_currency: string;
  counterparty?: string;
  strategic_implications?: string;
  disclosed_date: string;
  source_url?: string;
  created_at: string;
}

export interface ForecastPeriod {
  period: string;
  base: number;
  bullish: number;
  bearish: number;
  confidence_intervals: {
    ci_95: { lower: number; upper: number };
    ci_80: { lower: number; upper: number };
  };
}

export interface ForecastResponseData {
  status: string;
  company_id: string;
  company_symbol: string;
  metric_name: string;
  historical: { period: string; value: number }[];
  forecasts: ForecastPeriod[];
  evaluation?: {
    mae: number;
    rmse: number;
    mape: number;
    directional_accuracy: number;
  };
  disclaimer: string;
}

export interface EngineDetail {
  name: string;
  state: 'Ready' | 'Degraded' | 'Disabled' | 'Initializing' | 'Failed';
  provider?: string;
  version?: string;
  details?: string;
  last_checked: string;
}

export interface EnginesSummary {
  status: string;
  timestamp: string;
  total_engines: number;
  ready_count: number;
  degraded_count: number;
  disabled_count: number;
  failed_count: number;
  engines: Record<string, EngineDetail>;
}

export interface WatchlistItem {
  id: string;
  user_id: string;
  company_id: string;
  target_price?: number;
  alert_threshold_percent?: number;
  notes?: string;
  created_at: string;
  company?: Company;
}

