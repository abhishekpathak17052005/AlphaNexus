import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, ArrowUpDown, Building2, TrendingUp, LayoutGrid, List } from 'lucide-react';
import { Card, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { api } from '../services/api';
import { Company } from '../types';

export const ExploreCompaniesPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedExchange, setSelectedExchange] = useState<string>('ALL');
  const [selectedSector, setSelectedSector] = useState<string>('ALL');
  const [sortBy, setSortBy] = useState<string>('market_cap');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchList = async () => {
      try {
        const data = await api.getCompanies();
        setCompanies(data);
      } catch (e) {
        console.error('Failed to load companies:', e);
      } finally {
        setIsLoading(false);
      }
    };
    fetchList();
  }, []);

  const sectors = ['ALL', ...Array.from(new Set(companies.map((c) => c.sector).filter(Boolean)))];

  const filtered = companies
    .filter((c) => {
      const matchSearch =
        c.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchExchange = selectedExchange === 'ALL' || c.exchange === selectedExchange;
      const matchSector = selectedSector === 'ALL' || c.sector === selectedSector;
      return matchSearch && matchExchange && matchSector;
    })
    .sort((a: any, b: any) => {
      if (sortBy === 'market_cap') return (b.market_cap || 0) - (a.market_cap || 0);
      if (sortBy === 'pe_ratio') return (a.pe_ratio || 999) - (b.pe_ratio || 999);
      if (sortBy === 'roe') return (b.roe || 0) - (a.roe || 0);
      if (sortBy === 'current_price') return (b.current_price || 0) - (a.current_price || 0);
      return 0;
    });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Explore Listed Equities
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Browse Indian corporate leaders across NSE & BSE with fundamental valuation metrics
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-1.5 rounded ${viewMode === 'grid' ? 'bg-cyan-500/20 text-cyan-500 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <LayoutGrid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('table')}
            className={`p-1.5 rounded ${viewMode === 'table' ? 'bg-cyan-500/20 text-cyan-500 border border-cyan-500/30' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Filter and Search Controls */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <Input
          placeholder="Search by Symbol or Name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          icon={<Search className="w-4 h-4" />}
        />

        {/* Exchange Selector */}
        <div className="flex items-center gap-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 rounded-md p-1">
          {['ALL', 'NSE', 'BSE'].map((ex) => (
            <button
              key={ex}
              onClick={() => setSelectedExchange(ex)}
              className={`flex-1 py-1 text-xs font-mono font-medium rounded transition-colors ${
                selectedExchange === ex
                  ? 'bg-cyan-600 text-white shadow-xs'
                  : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
              }`}
            >
              {ex}
            </button>
          ))}
        </div>

        {/* Sector Filter */}
        <select
          value={selectedSector}
          onChange={(e) => setSelectedSector(e.target.value)}
          className="rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs text-slate-800 dark:text-slate-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
        >
          {sectors.map((s) => (
            <option key={s} value={s}>
              Sector: {s}
            </option>
          ))}
        </select>

        {/* Sort Selector */}
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs text-slate-800 dark:text-slate-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
        >
          <option value="market_cap">Sort: Market Cap (Highest)</option>
          <option value="pe_ratio">Sort: P/E Ratio (Lowest)</option>
          <option value="roe">Sort: ROE % (Highest)</option>
          <option value="current_price">Sort: Share Price (Highest)</option>
        </select>
      </div>

      {/* Companies List */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((c) => (
            <Card key={c.id} className="hover:border-cyan-500/50 transition-all flex flex-col justify-between group">
              <div className="p-5">
                {/* Symbol & Exchange */}
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/20 flex items-center justify-center font-bold text-sm">
                      {c.symbol.slice(0, 3)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-base text-slate-900 dark:text-slate-100 font-mono">
                          {c.symbol}
                        </span>
                        <Badge variant="terminal" size="xs">
                          {c.exchange}
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-1">{c.name}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-base font-bold font-tabular text-slate-900 dark:text-slate-100">
                      ₹{c.current_price?.toLocaleString('en-IN') || '—'}
                    </div>
                    <div className={`text-xs font-tabular font-medium ${c.day_change && c.day_change >= 0 ? 'text-emerald-500' : 'text-rose-500'}`}>
                      {c.day_change && c.day_change > 0 ? '+' : ''}{c.day_change_percent || 0}%
                    </div>
                  </div>
                </div>

                {/* Sector tag */}
                <div className="mt-3 flex items-center gap-2">
                  <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                    {c.sector}
                  </span>
                </div>

                {/* Fundamental Metrics Matrix */}
                <div className="mt-4 grid grid-cols-3 gap-2 p-3 rounded-lg bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800/60 font-tabular text-xs">
                  <div>
                    <span className="text-[10px] text-slate-400 block font-mono">Mkt Cap</span>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">
                      ₹{c.market_cap ? (c.market_cap / 1000).toFixed(1) + 'k Cr' : '—'}
                    </span>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-mono">P/E</span>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">{c.pe_ratio || '—'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 block font-mono">ROE</span>
                    <span className="font-semibold text-emerald-500">{c.roe ? `${c.roe}%` : '—'}</span>
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <div className="px-5 py-3 border-t border-slate-100 dark:border-slate-800/80 bg-slate-50/50 dark:bg-slate-900/20 rounded-b-lg flex justify-between items-center">
                <span className="text-[11px] font-mono text-slate-400">ISIN: {c.isin || '—'}</span>
                <Link to={`/company/${c.symbol}`}>
                  <Button variant="primary" size="sm">
                    Open Research
                  </Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        /* Table view */
        <Card className="overflow-x-auto">
          <table className="w-full text-left text-xs font-tabular">
            <thead className="bg-slate-50 dark:bg-slate-900 text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 font-mono">
              <tr>
                <th className="p-3">Symbol</th>
                <th className="p-3">Name</th>
                <th className="p-3">Sector</th>
                <th className="p-3 text-right">LTP (₹)</th>
                <th className="p-3 text-right">1D %</th>
                <th className="p-3 text-right">Mkt Cap (₹ Cr)</th>
                <th className="p-3 text-right">P/E</th>
                <th className="p-3 text-right">P/B</th>
                <th className="p-3 text-right">ROE</th>
                <th className="p-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {filtered.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-850/50">
                  <td className="p-3 font-semibold font-mono text-cyan-500">
                    <Link to={`/company/${c.symbol}`}>{c.symbol}</Link>
                  </td>
                  <td className="p-3 text-slate-700 dark:text-slate-200 font-sans">{c.name}</td>
                  <td className="p-3 text-slate-500">{c.sector}</td>
                  <td className="p-3 text-right font-semibold text-slate-900 dark:text-slate-100">
                    ₹{c.current_price?.toLocaleString('en-IN') || '—'}
                  </td>
                  <td className={`p-3 text-right ${c.day_change && c.day_change >= 0 ? 'text-emerald-500' : 'text-rose-500'}`}>
                    {c.day_change && c.day_change > 0 ? '+' : ''}{c.day_change_percent || 0}%
                  </td>
                  <td className="p-3 text-right text-slate-600 dark:text-slate-300">
                    {c.market_cap?.toLocaleString('en-IN') || '—'}
                  </td>
                  <td className="p-3 text-right">{c.pe_ratio || '—'}</td>
                  <td className="p-3 text-right">{c.pb_ratio || '—'}</td>
                  <td className="p-3 text-right text-emerald-500">{c.roe ? `${c.roe}%` : '—'}</td>
                  <td className="p-3 text-center">
                    <Link to={`/company/${c.symbol}`}>
                      <Button variant="outline" size="xs">
                        View
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}
    </div>
  );
};

