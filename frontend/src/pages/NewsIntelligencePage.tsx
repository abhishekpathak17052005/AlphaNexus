import React, { useState, useEffect } from 'react';
import { Newspaper, ExternalLink, RefreshCw, Filter, Sparkles, Building2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Modal } from '../components/ui/Modal';
import { api } from '../services/api';
import { NewsArticle, Company } from '../types';

export const NewsIntelligencePage: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedSentiment, setSelectedSentiment] = useState<string>('ALL');
  const [selectedCompanyId, setSelectedCompanyId] = useState<string>('');
  const [activeArticle, setActiveArticle] = useState<NewsArticle | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);

  const loadNews = async () => {
    try {
      const [newsData, comps] = await Promise.all([
        api.getNews({
          category: selectedCategory !== 'ALL' ? selectedCategory : undefined,
          sentiment: selectedSentiment !== 'ALL' ? selectedSentiment : undefined,
          company_id: selectedCompanyId || undefined,
        }),
        api.getCompanies(),
      ]);
      setArticles(newsData);
      setCompanies(comps);
    } catch (e) {
      console.error('Error fetching news:', e);
    }
  };

  useEffect(() => {
    loadNews();
  }, [selectedCategory, selectedSentiment, selectedCompanyId]);

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      await api.syncNews();
      await loadNews();
    } catch (e) {
      console.error('Error syncing news:', e);
    } finally {
      setIsSyncing(false);
    }
  };

  const CATEGORIES = [
    'ALL',
    'Earnings',
    'Acquisitions',
    'Contracts',
    'Partnerships',
    'Government orders',
    'Regulatory action',
    'Dividends',
    'Industry news',
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            News & Announcement Intelligence
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real-time corporate news feed, entity matching, sentiment indicators, and AI synthesis
          </p>
        </div>
        <Button variant="primary" size="sm" onClick={handleSync} isLoading={isSyncing}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Sync Latest News
        </Button>
      </div>

      {/* Filter Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Category filter */}
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none"
        >
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>
              Category: {cat}
            </option>
          ))}
        </select>

        {/* Sentiment filter */}
        <select
          value={selectedSentiment}
          onChange={(e) => setSelectedSentiment(e.target.value)}
          className="rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none"
        >
          <option value="ALL">Sentiment: All</option>
          <option value="Positive">Sentiment: Positive (Bullish)</option>
          <option value="Negative">Sentiment: Negative (Bearish)</option>
          <option value="Neutral">Sentiment: Neutral</option>
        </select>

        {/* Company filter */}
        <select
          value={selectedCompanyId}
          onChange={(e) => setSelectedCompanyId(e.target.value)}
          className="rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 font-mono focus:outline-none"
        >
          <option value="">Company: All Tracked</option>
          {companies.map((c) => (
            <option key={c.id} value={c.id}>
              {c.symbol} - {c.name}
            </option>
          ))}
        </select>
      </div>

      {/* News Stream Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {articles.map((item) => (
          <Card
            key={item.id}
            className="p-5 flex flex-col justify-between hover:border-cyan-500/40 transition-all space-y-3"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant="brand" size="xs">
                    {item.category}
                  </Badge>
                  <Badge
                    variant={
                      item.sentiment_label === 'Positive'
                        ? 'gain'
                        : item.sentiment_label === 'Negative'
                        ? 'loss'
                        : 'neutral'
                    }
                    size="xs"
                  >
                    {item.sentiment_label}
                  </Badge>
                </div>
                <span className="text-[10px] text-slate-400 font-mono">
                  {new Date(item.published_at).toLocaleDateString('en-IN', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                  })}
                </span>
              </div>

              <h3 className="font-semibold text-sm sm:text-base text-slate-900 dark:text-slate-100 line-clamp-2 leading-snug">
                {item.title}
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2">
                {item.description}
              </p>
            </div>

            {/* AI Summary excerpt */}
            {item.ai_summary && (
              <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800 text-xs">
                <span className="text-cyan-500 font-semibold flex items-center gap-1 mb-1">
                  <Sparkles className="w-3 h-3" /> AI Summary & Financial Impact
                </span>
                <p className="text-slate-600 dark:text-slate-300 line-clamp-2 text-[11px]">
                  {item.ai_summary}
                </p>
              </div>
            )}

            {/* Card footer */}
            <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span className="font-mono">{item.publisher || item.source}</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveArticle(item)}
                  className="text-cyan-500 hover:underline font-medium text-xs"
                >
                  Read AI Analysis
                </button>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-slate-400 hover:text-slate-200"
                  title="Open source article"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Article Detail Modal */}
      <Modal
        isOpen={!!activeArticle}
        onClose={() => setActiveArticle(null)}
        title={activeArticle?.title}
        maxWidth="2xl"
      >
        {activeArticle && (
          <div className="space-y-4 text-xs">
            <div className="flex items-center gap-2">
              <Badge variant="brand" size="xs">{activeArticle.category}</Badge>
              <Badge variant="gain" size="xs">Sentiment: {activeArticle.sentiment_label}</Badge>
              <span className="text-slate-400 font-mono ml-auto">
                {activeArticle.publisher} • {new Date(activeArticle.published_at).toLocaleString()}
              </span>
            </div>

            <p className="text-slate-700 dark:text-slate-300 leading-relaxed text-sm">
              {activeArticle.description}
            </p>

            {activeArticle.ai_summary && (
              <div className="p-4 rounded-xl bg-cyan-500/5 border border-cyan-500/20 space-y-2">
                <h4 className="font-bold text-cyan-600 dark:text-cyan-400 text-xs uppercase tracking-wider font-mono">
                  AI Financial Implications Analysis
                </h4>
                <p className="text-slate-800 dark:text-slate-200 leading-relaxed">
                  {activeArticle.ai_summary}
                </p>
                {activeArticle.financial_impact && (
                  <p className="text-slate-600 dark:text-slate-400 font-mono text-[11px] pt-1 border-t border-cyan-500/20">
                    <span className="font-bold">Projected Segment Impact:</span> {activeArticle.financial_impact}
                  </p>
                )}
              </div>
            )}

            <div className="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end">
              <a
                href={activeArticle.url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 px-4 py-2 bg-slate-900 text-white rounded-md text-xs font-semibold hover:bg-slate-800"
              >
                View Full Original Article <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

