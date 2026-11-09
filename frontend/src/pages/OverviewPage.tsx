import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  TrendingUp,
  TrendingDown,
  ArrowUpRight,
  ShieldCheck,
  Zap,
  FileText,
  AlertTriangle,
  Bot,
  ExternalLink,
  Plus,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { MarketChart } from '../components/charts/MarketChart';
import { api } from '../services/api';
import { Company, NewsArticle, MarketEvent, WatchlistItem } from '../types';

export const OverviewPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [events, setEvents] = useState<MarketEvent[]>([]);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [comps, newsData, eventsData, watchData] = await Promise.all([
          api.getCompanies(),
          api.getNews(),
          api.getMarketEvents(),
          api.getWatchlist(),
        ]);
        setCompanies(comps);
        setNews(newsData.slice(0, 5));
        setEvents(eventsData.slice(0, 5));
        setWatchlist(watchData);
      } catch (e) {
        console.error('Error loading dashboard:', e);
      } finally {
        setIsLoading(false);
      }
    };
    loadDashboardData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner / Market Overview Tickers */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* NIFTY 50 */}
        <Card className="p-4 bg-gradient-to-br from-white to-slate-50 dark:from-[#0a0f1d] dark:to-[#080d1a]">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
            <span>INDEX • NSE</span>
            <Badge variant="gain" size="xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Market Open
            </Badge>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-xl font-bold font-tabular tracking-tight text-slate-900 dark:text-slate-100">
              NIFTY 50
            </span>
            <span className="text-sm font-semibold font-tabular text-emerald-500 flex items-center">
              <TrendingUp className="w-3.5 h-3.5 mr-1" />
              +142.80 (+0.59%)
            </span>
          </div>
          <div className="mt-1 flex justify-between text-xs text-slate-500 dark:text-slate-400 font-tabular font-mono">
            <span>24,530.90</span>
            <span>Range: 24,310 - 24,550</span>
          </div>
        </Card>

        {/* SENSEX */}
        <Card className="p-4 bg-gradient-to-br from-white to-slate-50 dark:from-[#0a0f1d] dark:to-[#080d1a]">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
            <span>INDEX • BSE</span>
            <Badge variant="terminal" size="xs">
              BSE LIVE
            </Badge>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-xl font-bold font-tabular tracking-tight text-slate-900 dark:text-slate-100">
              SENSEX
            </span>
            <span className="text-sm font-semibold font-tabular text-emerald-500 flex items-center">
              <TrendingUp className="w-3.5 h-3.5 mr-1" />
              +486.25 (+0.61%)
            </span>
          </div>
          <div className="mt-1 flex justify-between text-xs text-slate-500 dark:text-slate-400 font-tabular font-mono">
            <span>80,436.84</span>
            <span>Range: 79,820 - 80,510</span>
          </div>
        </Card>

        {/* NIFTY BANK */}
        <Card className="p-4 bg-gradient-to-br from-white to-slate-50 dark:from-[#0a0f1d] dark:to-[#080d1a]">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
            <span>SECTOR • BFSI</span>
            <span className="text-[10px] text-slate-400">12 Banks</span>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-xl font-bold font-tabular tracking-tight text-slate-900 dark:text-slate-100">
              NIFTY BANK
            </span>
            <span className="text-sm font-semibold font-tabular text-emerald-500 flex items-center">
              <TrendingUp className="w-3.5 h-3.5 mr-1" />
              +382.40 (+0.74%)
            </span>
          </div>
          <div className="mt-1 flex justify-between text-xs text-slate-500 dark:text-slate-400 font-tabular font-mono">
            <span>52,190.20</span>
            <span>Range: 51,750 - 52,240</span>
          </div>
        </Card>

        {/* India VIX / Volatility */}
        <Card className="p-4 bg-gradient-to-br from-white to-slate-50 dark:from-[#0a0f1d] dark:to-[#080d1a]">
          <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
            <span>VOLATILITY</span>
            <Badge variant="gain" size="xs">
              Stable
            </Badge>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-xl font-bold font-tabular tracking-tight text-slate-900 dark:text-slate-100">
              INDIA VIX
            </span>
            <span className="text-sm font-semibold font-tabular text-rose-500 flex items-center">
              <TrendingDown className="w-3.5 h-3.5 mr-1" />
              -0.45 (-3.25%)
            </span>
          </div>
          <div className="mt-1 flex justify-between text-xs text-slate-500 dark:text-slate-400 font-tabular font-mono">
            <span>13.42</span>
            <span>Low risk regime</span>
          </div>
        </Card>
      </div>

      {/* Main Grid: Intraday Market Chart & AI Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Interactive Chart */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>NIFTY 50 Intraday Momentum</CardTitle>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Indian benchmark index trend across today's trading session
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="terminal" size="sm">
                NSE FEED
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <MarketChart isGain={true} />
          </CardContent>
        </Card>

        {/* AI Financial Intelligence Insights Card */}
        <Card className="flex flex-col">
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-md bg-cyan-500/10 text-cyan-500">
                <Bot className="w-4 h-4" />
              </div>
              <CardTitle>AI Equity Insights</CardTitle>
            </div>
            <Badge variant="brand" size="xs">
              SYNTHESIS
            </Badge>
          </CardHeader>
          <CardContent className="space-y-3.5 flex-1 overflow-y-auto">
            {/* Growth indicator */}
            <div className="p-3 rounded-lg bg-emerald-500/5 border border-emerald-500/20 text-xs">
              <div className="flex items-center justify-between font-semibold text-emerald-600 dark:text-emerald-400 mb-1">
                <span className="flex items-center gap-1.5">
                  <TrendingUp className="w-3.5 h-3.5" /> Capex Acceleration
                </span>
                <span className="font-mono text-[11px] font-bold">RELIANCE</span>
              </div>
              <p className="text-slate-600 dark:text-slate-300">
                SECI 10 GWh battery storage win initiates commercial scaling for Jamnagar new energy giga-factories.
              </p>
            </div>

            {/* Profitability change */}
            <div className="p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/20 text-xs">
              <div className="flex items-center justify-between font-semibold text-cyan-600 dark:text-cyan-400 mb-1">
                <span className="flex items-center gap-1.5">
                  <Zap className="w-3.5 h-3.5" /> Margin Resilience
                </span>
                <span className="font-mono text-[11px] font-bold">TCS</span>
              </div>
              <p className="text-slate-600 dark:text-slate-300">
                Operating margin holds at 24.6% (+50 bps) driven by subcontractor rationalization and $42.7B annual TCV.
              </p>
            </div>

            {/* Risk Alert */}
            <div className="p-3 rounded-lg bg-amber-500/5 border border-amber-500/20 text-xs">
              <div className="flex items-center justify-between font-semibold text-amber-600 dark:text-amber-400 mb-1">
                <span className="flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" /> Credit-to-Deposit Focus
                </span>
                <span className="font-mono text-[11px] font-bold">HDFCBANK</span>
              </div>
              <p className="text-slate-600 dark:text-slate-300">
                Deposit growth outpaced loan growth by 300 bps in Q3; monitoring progress toward 85% post-merger LDR target.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Secondary Grid: Top Listed Equities & Intelligence Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Watchlist & Top Equities Table */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Market Leaders (NSE/BSE)</CardTitle>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Tracked corporate equities with verified filings & valuation metrics
              </p>
            </div>
            <Link to="/explore">
              <Button variant="ghost" size="xs">
                Explore All <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent className="p-0 overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-900/60 text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 font-mono">
                <tr>
                  <th className="py-2.5 px-4 font-medium">Symbol</th>
                  <th className="py-2.5 px-4 font-medium">Company</th>
                  <th className="py-2.5 px-4 font-medium text-right">LTP (₹)</th>
                  <th className="py-2.5 px-4 font-medium text-right">Change</th>
                  <th className="py-2.5 px-4 font-medium text-right">P/E</th>
                  <th className="py-2.5 px-4 font-medium text-right">ROE</th>
                  <th className="py-2.5 px-4 font-medium text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-tabular">
                {companies.map((c) => (
                  <tr
                    key={c.id}
                    className="hover:bg-slate-50/80 dark:hover:bg-slate-850/50 transition-colors"
                  >
                    <td className="py-3 px-4 font-semibold text-slate-900 dark:text-slate-100 font-mono">
                      <Link to={`/company/${c.symbol}`} className="hover:text-cyan-500 flex items-center gap-1.5">
                        {c.symbol}
                        <Badge variant="terminal" size="xs">
                          {c.exchange}
                        </Badge>
                      </Link>
                    </td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-300 max-w-xs truncate">
                      {c.name}
                    </td>
                    <td className="py-3 px-4 text-right font-semibold text-slate-900 dark:text-slate-100">
                      ₹{c.current_price?.toLocaleString('en-IN') || '—'}
                    </td>
                    <td className="py-3 px-4 text-right font-medium">
                      <span className={c.day_change && c.day_change >= 0 ? 'text-emerald-500' : 'text-rose-500'}>
                        {c.day_change && c.day_change > 0 ? '+' : ''}{c.day_change_percent || 0}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right text-slate-600 dark:text-slate-300">
                      {c.pe_ratio || '—'}
                    </td>
                    <td className="py-3 px-4 text-right text-slate-600 dark:text-slate-300">
                      {c.roe ? `${c.roe}%` : '—'}
                    </td>
                    <td className="py-3 px-4 text-center">
                      <Link to={`/company/${c.symbol}`}>
                        <Button variant="outline" size="xs">
                          Research
                        </Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>

        {/* Real-time Intelligence Feed */}
        <Card className="flex flex-col">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Market Intelligence Feed</CardTitle>
            <Link to="/news">
              <Button variant="ghost" size="xs">
                View All
              </Button>
            </Link>
          </CardHeader>
          <CardContent className="space-y-3 p-4 flex-1 overflow-y-auto">
            {news.map((item) => (
              <div
                key={item.id}
                className="p-3 rounded-lg border border-slate-100 dark:border-slate-800/70 hover:border-cyan-500/30 transition-all text-xs space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="brand" size="xs">
                    {item.category}
                  </Badge>
                  <span className="text-[10px] text-slate-400 font-mono">
                    {new Date(item.published_at).toLocaleDateString('en-IN', {
                      month: 'short',
                      day: 'numeric',
                    })}
                  </span>
                </div>
                <h4 className="font-semibold text-slate-900 dark:text-slate-100 line-clamp-2 leading-snug">
                  {item.title}
                </h4>
                {item.financial_impact && (
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2">
                    <span className="text-cyan-500 font-medium">Impact:</span> {item.financial_impact}
                  </p>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

