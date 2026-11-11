import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import {
  TrendingUp, TrendingDown, Globe, ArrowLeft,
  FileText, Bot, Building2, BarChart2, Newspaper,
  CalendarDays, Briefcase,
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Area, AreaChart,
} from 'recharts';
import { ANButton } from '../components/shared/ANButton';
import { api } from '../services/api';
import type { Company, FinancialMetric, NewsArticle, CorporateAction, MarketEvent } from '../types';

const TABS = [
  { id: 'overview',   label: 'Overview',    icon: Building2 },
  { id: 'financials', label: 'Financials',  icon: BarChart2 },
  { id: 'news',       label: 'News',        icon: Newspaper },
  { id: 'actions',    label: 'Corp Actions', icon: CalendarDays },
  { id: 'events',     label: 'Events',      icon: Briefcase },
  { id: 'research',   label: 'AI Research', icon: Bot },
];

export const CompanyResearchPage: React.FC = () => {
  const { symbol }   = useParams<{ symbol: string }>();
  const navigate     = useNavigate();
  const [tab, setTab] = useState('overview');
  const [company,    setCompany]  = useState<Company | null>(null);
  const [financials, setFinancials] = useState<FinancialMetric[]>([]);
  const [news,       setNews]     = useState<NewsArticle[]>([]);
  const [actions,    setActions]  = useState<CorporateAction[]>([]);
  const [events,     setEvents]   = useState<MarketEvent[]>([]);
  const [loading,    setLoading]  = useState(true);
  const [chatQuery,  setChatQuery] = useState('');
  const [chatResp,   setChatResp] = useState<{ content: string; citations: any[] } | null>(null);
  const [chatLoad,   setChatLoad] = useState(false);

  useEffect(() => {
    if (!symbol) return;
    setLoading(true);
    api.getCompany(symbol).then(async (c) => {
      setCompany(c);
      const [fins, n, acts, evts] = await Promise.all([
        api.getCompanyFinancials(c.id),
        api.getNews({ company_id: c.id }),
        api.getCorporateActions({ company_id: c.id }),
        api.getMarketEvents({ company_id: c.id }),
      ]);
      setFinancials(fins); setNews(n); setActions(acts); setEvents(evts);
    }).catch(() => navigate('/discover'))
    .finally(() => setLoading(false));
  }, [symbol]);

  const revenueData = financials
    .filter((m) => m.metric_name === 'revenue')
    .sort((a, b) => a.financial_year.localeCompare(b.financial_year))
    .map((m) => ({ fy: m.financial_year, value: m.value }));

  const handleChat = async () => {
    if (!chatQuery.trim() || !company) return;
    setChatLoad(true);
    try {
      const res = await api.sendResearchChat({ company_id: company.id, query: chatQuery });
      setChatResp({ content: res.content, citations: res.citations });
    } finally { setChatLoad(false); }
  };

  if (loading) {
    return (
      <div className="page-container py-8 space-y-6">
        <div className="skeleton h-10 w-48 rounded-xl" />
        <div className="skeleton h-40 rounded-2xl" />
        <div className="skeleton h-64 rounded-2xl" />
      </div>
    );
  }

  if (!company) return null;

  return (
    <div className="page-container py-8 space-y-6">
      {/* Back */}
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-sm transition-opacity hover:opacity-70"
        style={{ color: 'var(--text-3)' }}>
        <ArrowLeft className="w-4 h-4" /> Back
      </button>

      {/* Company Header */}
      <motion.div
        className="card p-6"
        initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl flex items-center justify-center font-black text-lg"
              style={{ background: 'var(--brand-muted)', color: 'var(--brand)', border: '1px solid var(--border-brand)' }}>
              {company.symbol.slice(0, 2)}
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight" style={{ color: 'var(--text-1)', letterSpacing: '-0.02em' }}>
                {company.name}
              </h1>
              <div className="flex items-center gap-2 mt-1">
                <span className="font-black font-mono text-sm" style={{ color: 'var(--brand)' }}>{company.symbol}</span>
                <span className="badge badge-muted">{company.exchange}</span>
                {company.sector && <span className="text-xs" style={{ color: 'var(--text-4)' }}>{company.sector}</span>}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-6 text-right">
            {company.current_price && (
              <div>
                <div className="text-2xl font-black font-tabular" style={{ color: 'var(--text-1)' }}>
                  ₹{company.current_price.toLocaleString('en-IN')}
                </div>
                {company.day_change_percent != null && (
                  <div
                    className="text-sm font-bold font-tabular flex items-center gap-1 justify-end"
                    style={{ color: company.day_change_percent >= 0 ? 'var(--positive-text)' : 'var(--negative-text)' }}
                  >
                    {company.day_change_percent >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                    {company.day_change_percent >= 0 ? '+' : ''}{company.day_change_percent}%
                  </div>
                )}
              </div>
            )}
            <div className="flex gap-2">
              <Link to="/research">
                <ANButton variant="brand" size="sm" icon={<Bot className="w-3.5 h-3.5" />}>AI Research</ANButton>
              </Link>
              {company.website && (
                <a href={company.website} target="_blank" rel="noopener noreferrer">
                  <ANButton variant="ghost" size="sm" icon={<Globe className="w-3.5 h-3.5" />}>Website</ANButton>
                </a>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="flex gap-1.5 flex-wrap">
        {TABS.map((t) => {
          const Icon = t.icon;
          return (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all"
              style={{
                background: tab === t.id ? 'var(--brand)' : 'var(--surface-2)',
                color: tab === t.id ? '#fff' : 'var(--text-3)',
                border: `1px solid ${tab === t.id ? 'var(--brand)' : 'var(--border)'}`,
              }}
            >
              <Icon className="w-3.5 h-3.5" />{t.label}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <motion.div key={tab} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
        {/* Overview */}
        {tab === 'overview' && (
          <div className="space-y-5">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { label: 'Market Cap', value: company.market_cap ? `₹${(company.market_cap/1000).toFixed(0)}K Cr` : '—' },
                { label: 'P/E Ratio',  value: company.pe_ratio ? `${company.pe_ratio}x` : '—' },
                { label: 'P/B Ratio',  value: company.pb_ratio ? `${company.pb_ratio}x` : '—' },
                { label: 'Div Yield',  value: company.dividend_yield ? `${company.dividend_yield}%` : '—' },
                { label: 'ROE',        value: company.roe ? `${company.roe}%` : '—' },
                { label: 'ROCE',       value: company.roce ? `${company.roce}%` : '—' },
                { label: '52W High',   value: company.week_52_high ? `₹${company.week_52_high.toLocaleString('en-IN')}` : '—' },
                { label: '52W Low',    value: company.week_52_low  ? `₹${company.week_52_low.toLocaleString('en-IN')}` : '—' },
              ].map((m) => (
                <div key={m.label} className="card p-3.5">
                  <div className="text-[10px] font-bold uppercase tracking-wider mb-1" style={{ color: 'var(--text-4)' }}>{m.label}</div>
                  <div className="text-base font-black font-tabular" style={{ color: 'var(--text-1)' }}>{m.value}</div>
                </div>
              ))}
            </div>
            {company.description && (
              <div className="card p-5">
                <h4 className="font-bold text-sm mb-2" style={{ color: 'var(--text-1)' }}>About</h4>
                <p className="text-sm leading-relaxed" style={{ color: 'var(--text-2)' }}>{company.description}</p>
              </div>
            )}
          </div>
        )}

        {/* Financials */}
        {tab === 'financials' && (
          <div className="card p-5">
            <h4 className="font-bold mb-4" style={{ color: 'var(--text-1)' }}>Revenue Trend (₹ Crores)</h4>
            {revenueData.length === 0 ? (
              <div className="text-sm py-12 text-center" style={{ color: 'var(--text-4)' }}>No financial data available.</div>
            ) : (
              <ResponsiveContainer width="100%" height={260}>
                <AreaChart data={revenueData}>
                  <defs>
                    <linearGradient id="rev" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#1558C9" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#1558C9" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 6" stroke="var(--border)" />
                  <XAxis dataKey="fy" tick={{ fill: 'var(--text-4)', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'var(--text-4)', fontSize: 10 }} axisLine={false} tickLine={false} width={65}
                    tickFormatter={(v) => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v} />
                  <Tooltip contentStyle={{ background: 'var(--surface-3)', border: '1px solid var(--border)', borderRadius: 10, fontSize: 11 }} />
                  <Area type="monotone" dataKey="value" stroke="#1558C9" strokeWidth={2.5}
                    fill="url(#rev)" dot={{ fill: '#1558C9', r: 4 }} name="Revenue (₹ Cr)" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        )}

        {/* News */}
        {tab === 'news' && (
          <div className="space-y-3">
            {news.length === 0 ? (
              <div className="card py-16 text-center text-sm" style={{ color: 'var(--text-4)' }}>No news available.</div>
            ) : news.slice(0, 10).map((item) => (
              <div key={item.id} className="card p-4">
                <div className="text-[10px] mb-1" style={{ color: 'var(--text-4)' }}>
                  {new Date(item.published_at).toLocaleDateString()}
                  {item.publisher && ` · ${item.publisher}`}
                </div>
                <div className="font-semibold text-sm" style={{ color: 'var(--text-1)' }}>{item.title}</div>
              </div>
            ))}
          </div>
        )}

        {/* Corporate Actions */}
        {tab === 'actions' && (
          <div className="card overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead style={{ background: 'var(--surface-2)' }}>
                <tr className="text-[10px] font-bold uppercase tracking-wider" style={{ color: 'var(--text-4)' }}>
                  {['Type', 'Details', 'Ex-Date', 'Status'].map((h) => <th key={h} className="px-4 py-2.5">{h}</th>)}
                </tr>
              </thead>
              <tbody>
                {actions.length === 0 ? (
                  <tr><td colSpan={4} className="px-4 py-10 text-center" style={{ color: 'var(--text-4)' }}>No corporate actions.</td></tr>
                ) : actions.map((a) => (
                  <tr key={a.id} style={{ borderTop: '1px solid var(--border)' }} className="hover:bg-[var(--surface-2)]">
                    <td className="px-4 py-3"><span className="badge badge-brand">{a.action_type}</span></td>
                    <td className="px-4 py-3" style={{ color: 'var(--text-2)' }}>{a.details}</td>
                    <td className="px-4 py-3 font-mono" style={{ color: 'var(--text-3)' }}>{a.ex_date || '—'}</td>
                    <td className="px-4 py-3"><span className="badge badge-lime">{a.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Market Events */}
        {tab === 'events' && (
          <div className="space-y-3">
            {events.length === 0 ? (
              <div className="card py-16 text-center text-sm" style={{ color: 'var(--text-4)' }}>No market events.</div>
            ) : events.map((ev) => (
              <div key={ev.id} className="card p-4 card-hover">
                <div className="flex items-center gap-2 mb-2">
                  <span className="badge badge-brand">{ev.event_type}</span>
                  <span className="text-[10px] font-mono" style={{ color: 'var(--text-4)' }}>{ev.disclosed_date}</span>
                </div>
                <div className="font-bold text-sm" style={{ color: 'var(--text-1)' }}>{ev.title}</div>
                <div className="text-xs mt-1" style={{ color: 'var(--text-3)' }}>{ev.description}</div>
                {ev.deal_value && ev.deal_value > 0 && (
                  <div className="text-sm font-black font-tabular mt-2" style={{ color: 'var(--lime)' }}>
                    ₹{ev.deal_value.toLocaleString('en-IN')} Cr
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* AI Research */}
        {tab === 'research' && (
          <div className="card p-5 space-y-4">
            <h4 className="font-bold" style={{ color: 'var(--text-1)' }}>
              Ask a question about {company.name}
            </h4>
            <div className="flex gap-2">
              <input
                value={chatQuery}
                onChange={(e) => setChatQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleChat()}
                placeholder="e.g. What are the key risk factors in the FY24 annual report?"
                className="input flex-1 px-4 py-2.5 text-sm"
              />
              <ANButton variant="brand" size="md" onClick={handleChat} loading={chatLoad}>Ask</ANButton>
            </div>
            {chatResp && (
              <div className="rounded-xl p-4 text-sm space-y-3" style={{ background: 'var(--surface-2)', border: '1px solid var(--border)' }}>
                <div className="whitespace-pre-wrap leading-relaxed text-xs" style={{ color: 'var(--text-1)' }}>
                  {chatResp.content}
                </div>
                {chatResp.citations.length > 0 && (
                  <div className="space-y-1.5 pt-2" style={{ borderTop: '1px solid var(--border)' }}>
                    <div className="text-[10px] font-bold uppercase tracking-wider" style={{ color: 'var(--text-4)' }}>Sources</div>
                    {chatResp.citations.map((c: any, i: number) => (
                      <div key={i} className="text-[11px] rounded-lg p-2" style={{ background: 'var(--surface-1)', border: '1px solid var(--border)' }}>
                        <span style={{ color: 'var(--brand)' }}>[{i+1}] {c.document_title} · Page {c.page_number ?? '?'}</span>
                        <span style={{ color: 'var(--text-3)' }}> — "{c.excerpt}"</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </motion.div>
    </div>
  );
};
