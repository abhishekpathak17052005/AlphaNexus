import axios from 'axios';
import {
  Company,
  DocumentItem,
  ResearchMessage,
  ResearchSession,
  NewsArticle,
  CorporateAction,
  MarketEvent,
  ForecastResponseData,
  EnginesSummary,
  WatchlistItem,
  FinancialMetric,
} from '../types';

const API_BASE = '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for clear error surfacing
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const api = {
  // Health & Engines
  getHealth: async () => {
    const res = await apiClient.get('/health');
    return res.data;
  },
  getEngines: async (): Promise<EnginesSummary> => {
    const res = await apiClient.get('/health/engines');
    return res.data;
  },

  // Companies
  getCompanies: async (params?: { exchange?: string; sector?: string; search?: string }): Promise<Company[]> => {
    const res = await apiClient.get('/companies', { params });
    return res.data;
  },
  searchCompanies: async (q: string): Promise<Company[]> => {
    const res = await apiClient.get('/companies/search', { params: { q } });
    return res.data;
  },
  getCompany: async (idOrSymbol: string): Promise<Company> => {
    const res = await apiClient.get(`/companies/${idOrSymbol}`);
    return res.data;
  },

  // Documents
  getDocuments: async (params?: { company_id?: string; document_type?: string; status?: string }): Promise<DocumentItem[]> => {
    const res = await apiClient.get('/documents', { params });
    return res.data;
  },
  uploadDocument: async (formData: FormData): Promise<any> => {
    const res = await apiClient.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },
  processDocument: async (documentId: string): Promise<any> => {
    const res = await apiClient.post(`/documents/${documentId}/process`);
    return res.data;
  },
  deleteDocument: async (documentId: string): Promise<any> => {
    const res = await apiClient.delete(`/documents/${documentId}`);
    return res.data;
  },

  // AI Research & RAG
  sendResearchChat: async (payload: {
    session_id?: string;
    company_id?: string;
    query: string;
    financial_year?: string;
    document_type?: string;
    top_k?: number;
  }): Promise<ResearchMessage> => {
    const res = await apiClient.post('/research/chat', payload);
    return res.data;
  },
  getResearchSessions: async (): Promise<ResearchSession[]> => {
    const res = await apiClient.get('/research/sessions');
    return res.data;
  },
  getResearchSession: async (sessionId: string): Promise<ResearchSession> => {
    const res = await apiClient.get(`/research/sessions/${sessionId}`);
    return res.data;
  },

  // News Intelligence
  getNews: async (params?: { company_id?: string; category?: string; sentiment?: string }): Promise<NewsArticle[]> => {
    const res = await apiClient.get('/news', { params });
    return res.data;
  },
  syncNews: async (): Promise<any> => {
    const res = await apiClient.post('/news/sync');
    return res.data;
  },

  // Financial Analytics
  getCompanyFinancials: async (companyId: string, periodType: string = 'annual'): Promise<FinancialMetric[]> => {
    const res = await apiClient.get(`/companies/${companyId}/financials`, { params: { period_type: periodType } });
    return res.data;
  },
  getCompanyStatements: async (companyId: string, statementType?: string): Promise<any[]> => {
    const res = await apiClient.get(`/companies/${companyId}/statements`, { params: { statement_type: statementType } });
    return res.data;
  },
  getCompanyRatios: async (companyId: string): Promise<{ company_symbol: string; computed_metrics: Record<string, any> }> => {
    const res = await apiClient.get(`/companies/${companyId}/ratios`);
    return res.data;
  },
  comparePeers: async (companyIds: string[]): Promise<any> => {
    const res = await apiClient.post('/companies/compare', { company_ids: companyIds });
    return res.data;
  },

  // Corporate Actions
  getCorporateActions: async (params?: { company_id?: string; action_type?: string }): Promise<CorporateAction[]> => {
    const res = await apiClient.get('/corporate-actions', { params });
    return res.data;
  },

  // Market Events
  getMarketEvents: async (params?: { company_id?: string; event_type?: string }): Promise<MarketEvent[]> => {
    const res = await apiClient.get('/market-events', { params });
    return res.data;
  },

  // Forecasts
  getForecasts: async (companyId: string, metricName: string = 'revenue'): Promise<ForecastResponseData> => {
    const res = await apiClient.get(`/companies/${companyId}/forecasts`, { params: { metric_name: metricName } });
    return res.data;
  },
  generateForecast: async (companyId: string, payload: { metric_name: string; forecast_horizon_years: number }): Promise<ForecastResponseData> => {
    const res = await apiClient.post(`/companies/${companyId}/forecasts/generate`, payload);
    return res.data;
  },

  // Watchlist
  getWatchlist: async (): Promise<WatchlistItem[]> => {
    const res = await apiClient.get('/watchlist');
    return res.data;
  },
  addToWatchlist: async (payload: { company_id: string; target_price?: number; notes?: string }): Promise<WatchlistItem> => {
    const res = await apiClient.post('/watchlist', payload);
    return res.data;
  },
  removeFromWatchlist: async (companyId: string): Promise<any> => {
    const res = await apiClient.delete(`/watchlist/${companyId}`);
    return res.data;
  },
};

