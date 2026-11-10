import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { Search, Building2, TrendingUp, TrendingDown, Filter, ArrowUpRight } from 'lucide-react';
import { ANCard } from '../components/shared/ANCard';
import { ANButton } from '../components/shared/ANButton';
import { api } from '../services/api';
import type { Company } from '../types';

const EXCHANGES = ['All', 'NSE', 'BSE'];
const SECTORS   = ['All', 'Information Technology', 'Banking & Financial Services', 'Energy & Conglomerate', 'Infrastructure & Capital Goods'];

export const DiscoverPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [filtered,  setFiltered]  = useState<Company[]>([]);
  const [query,     setQuery]     = useState('');
  const [exchange,  setExchange]  = useState('All');
  const [sector,    setSector]    = useState('All');
  const [loading,   setLoading]   = useState(true);

  useEffect(() => {
    api.getCompanies().then((d) => { setCompanies(d); setFiltered(d); }).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    let res = [...companies];
    if (query)              res = res.filter((c) => c.name.toLowerCase().includes(query.toLowerCase()) || c.symbol.toLowerCase().includes(query.toLowerCase()));
    if (exchange !== 'All') res = res.filter((c) => c.exchange === exchange);
    if (sector   !== 'All') res = res.filter((c) => c.sector   === sector);
    setFiltered(res);
  }, [query, exchange, sector, companies]);

  return (
    <div className="page-container py-8 space-y-7">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-1">
        <h1 className="text-3xl font-black tracking-tight" style={{ color: 'var(--text-1)', letterSpacing: '-0.02em' }}>
          Discover <span style={{ color: 'var(--brand)' }}>Companies</span>
        </h1>
        <p className="text-sm" style={{ color: 'var(--text-3)' }}>Search and explore NSE / BSE listed equities.</p>
      </motion.div>

      {/* Search + Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: 'var(--text-4)' }} />
          <input
            className="input w-full pl-9 pr-4 py-2 text-sm"
            placeholder="Company name or ticker…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <select
          value={exchange}
          onChange={(e) => setExchange(e.target.value)}
          className="input px-3 py-2 text-sm"
          style={{ minWidth: 100 }}
        >
          {EXCHANGES.map((e) => <option key={e} value={e}>{e}</option>)}
        </select>
        <select
          value={sector}
          onChange={(e) => setSector(e.target.value)}
          className="input px-3 py-2 text-sm"
          style={{ minWidth: 180 }}
        >
          {SECTORS.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>

      <div className="text-xs" style={{ color: 'var(--text-4)' }}>
        {filtered.length} compan{filtered.length === 1 ? 'y' : 'ies'} found
      </div>

      {/* Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading
          ? Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="card p-5 space-y-3">
                <div className="skeleton h-5 w-20 rounded" />
                <div className="skeleton h-3 w-40 rounded" />
                <div className="skeleton h-3 w-32 rounded" />
              </div>
            ))
          : filtered.map((c, i) => (
              <motion.div
                key={c.id}
                className="card card-hover p-5 group"
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="text-lg font-black font-mono" style={{ color: 'var(--brand)' }}>{c.symbol}</div>
                    <div className="text-xs font-semibold mt-0.5 leading-snug line-clamp-2" style={{ color: 'var(--text-1)' }}>{c.name}</div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <span className="badge badge-muted">{c.exchange}</span>
                    {c.day_change_percent != null && (
                      <span
                        className="badge"
                        style={{
                          background: (c.day_change_percent >= 0) ? 'var(--lime-muted)' : 'rgba(255,100,110,.08)',
                          color:      (c.day_change_percent >= 0) ? 'var(--positive-text)' : 'var(--negative-text)',
                          border: `1px solid ${(c.day_change_percent >= 0) ? 'rgba(212,255,36,.25)' : 'rgba(255,100,110,.2)'}`,
                        }}
                      >
                        {c.day_change_percent >= 0 ? '▲' : '▼'} {Math.abs(c.day_change_percent)}%
                      </span>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 text-center mb-4">
                  {[
                    { label: 'Price', value: c.current_price ? `₹${c.current_price.toLocaleString('en-IN')}` : '—' },
                    { label: 'P/E',   value: c.pe_ratio ?? '—' },
                    { label: 'ROE',   value: c.roe != null ? `${c.roe}%` : '—' },
                  ].map((m) => (
                    <div key={m.label} className="rounded-lg p-1.5" style={{ background: 'var(--surface-2)' }}>
                      <div className="text-xs font-black font-tabular" style={{ color: 'var(--text-1)' }}>{m.value}</div>
                      <div className="text-[9px] uppercase tracking-wider font-semibold" style={{ color: 'var(--text-4)' }}>{m.label}</div>
                    </div>
                  ))}
                </div>

                {c.sector && (
                  <div className="text-[10px] mb-3" style={{ color: 'var(--text-4)' }}>{c.sector}</div>
                )}

                <Link to={`/company/${c.symbol}`} className="block">
                  <ANButton variant="brand" size="sm" className="w-full" icon={<ArrowUpRight className="w-3.5 h-3.5" />} iconRight>
                    Research
                  </ANButton>
                </Link>
              </motion.div>
            ))}
      </div>
    </div>
  );
};
