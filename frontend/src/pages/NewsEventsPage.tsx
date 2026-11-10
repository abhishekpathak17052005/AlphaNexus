import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Newspaper, ExternalLink, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { ANButton } from '../components/shared/ANButton';
import { api } from '../services/api';
import type { NewsArticle, MarketEvent } from '../types';

const SentimentIcon: React.FC<{ sentiment: string }> = ({ sentiment }) => {
  if (sentiment === 'Positive') return <TrendingUp className="w-3.5 h-3.5" style={{ color: 'var(--positive-text)' }} />;
  if (sentiment === 'Negative') return <TrendingDown className="w-3.5 h-3.5" style={{ color: 'var(--negative-text)' }} />;
  return <Minus className="w-3.5 h-3.5" style={{ color: 'var(--text-4)' }} />;
};

export const NewsEventsPage: React.FC = () => {
  const [news,   setNews]   = useState<NewsArticle[]>([]);
  const [events, setEvents] = useState<MarketEvent[]>([]);
  const [tab,    setTab]    = useState<'news' | 'events'>('news');
  const [loading, setLoading] = useState(true);
  const [sentiment, setSentiment] = useState('All');

  useEffect(() => {
    Promise.all([api.getNews(), api.getMarketEvents()]).then(([n, e]) => {
      setNews(n); setEvents(e);
    }).finally(() => setLoading(false));
  }, []);

  const filteredNews = sentiment === 'All' ? news
    : news.filter((n) => n.sentiment_label === sentiment);

  return (
    <div className="page-container py-8 space-y-7">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-black tracking-tight" style={{ color: 'var(--text-1)', letterSpacing: '-0.02em' }}>
          News & <span style={{ color: 'var(--brand)' }}>Events</span>
        </h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>
          Corporate announcements, market deals, and financial news intelligence.
        </p>
      </motion.div>

      {/* Tabs */}
      <div className="flex gap-2">
        {(['news', 'events'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className="px-4 py-2 rounded-xl text-sm font-bold transition-all capitalize"
            style={{
              background: tab === t ? 'var(--brand)' : 'var(--surface-2)',
              color: tab === t ? '#fff' : 'var(--text-2)',
              border: `1px solid ${tab === t ? 'var(--brand)' : 'var(--border)'}`,
            }}
          >
            {t === 'news' ? `News (${news.length})` : `Market Events (${events.length})`}
          </button>
        ))}
      </div>

      {tab === 'news' && (
        <>
          {/* Sentiment filter */}
          <div className="flex gap-2 flex-wrap">
            {['All', 'Positive', 'Negative', 'Neutral'].map((s) => (
              <button
                key={s}
                onClick={() => setSentiment(s)}
                className="px-3 py-1 rounded-lg text-xs font-bold transition-all"
                style={{
                  background: sentiment === s ? 'var(--brand-muted)' : 'var(--surface-2)',
                  color: sentiment === s ? 'var(--brand)' : 'var(--text-3)',
                  border: `1px solid ${sentiment === s ? 'var(--border-brand)' : 'var(--border)'}`,
                }}
              >
                {s}
              </button>
            ))}
          </div>

          <div className="space-y-3">
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => <div key={i} className="skeleton h-20 rounded-xl w-full" />)
            ) : filteredNews.length === 0 ? (
              <div className="text-center py-16 text-sm" style={{ color: 'var(--text-4)' }}>No articles found.</div>
            ) : filteredNews.map((item, i) => (
              <motion.div
                key={item.id}
                className="card p-4 card-hover flex gap-4"
                initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.03 }}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <SentimentIcon sentiment={item.sentiment_label} />
                    <span className="badge badge-muted">{item.category || 'Market'}</span>
                    <span className="text-[10px] font-mono" style={{ color: 'var(--text-4)' }}>
                      {new Date(item.published_at).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                    {item.publisher && (
                      <span className="text-[10px]" style={{ color: 'var(--text-4)' }}>· {item.publisher}</span>
                    )}
                  </div>
                  <h3 className="font-semibold text-sm leading-snug" style={{ color: 'var(--text-1)' }}>{item.title}</h3>
                  {item.ai_summary && (
                    <p className="text-xs mt-1.5 line-clamp-2 leading-relaxed" style={{ color: 'var(--text-3)' }}>
                      {item.ai_summary}
                    </p>
                  )}
                </div>
                {item.url && (
                  <a href={item.url} target="_blank" rel="noopener noreferrer"
                    className="shrink-0 mt-1 p-1.5 rounded-lg transition-opacity hover:opacity-70"
                    style={{ color: 'var(--text-4)' }}>
                    <ExternalLink className="w-4 h-4" />
                  </a>
                )}
              </motion.div>
            ))}
          </div>
        </>
      )}

      {tab === 'events' && (
        <div className="space-y-3">
          {loading ? (
            Array.from({ length: 4 }).map((_, i) => <div key={i} className="skeleton h-24 rounded-xl w-full" />)
          ) : events.length === 0 ? (
            <div className="text-center py-16 text-sm" style={{ color: 'var(--text-4)' }}>No market events found.</div>
          ) : events.map((ev, i) => (
            <motion.div
              key={ev.id}
              className="card p-4 card-hover"
              initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="badge badge-brand">{ev.event_type}</span>
                    <span className="text-[10px] font-mono" style={{ color: 'var(--text-4)' }}>
                      {new Date(ev.disclosed_date).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                  <h3 className="font-bold text-sm leading-snug" style={{ color: 'var(--text-1)' }}>{ev.title}</h3>
                  <p className="text-xs mt-1.5 line-clamp-2 leading-relaxed" style={{ color: 'var(--text-3)' }}>
                    {ev.description}
                  </p>
                  {ev.strategic_implications && (
                    <p className="text-xs mt-1 line-clamp-1" style={{ color: 'var(--brand)' }}>
                      Strategic: {ev.strategic_implications}
                    </p>
                  )}
                </div>
                {ev.deal_value && ev.deal_value > 0 && (
                  <div className="shrink-0 text-right">
                    <div className="text-xs font-bold uppercase tracking-wider mb-0.5" style={{ color: 'var(--text-4)' }}>Deal Value</div>
                    <div className="text-base font-black font-tabular" style={{ color: 'var(--lime)' }}>
                      ₹{ev.deal_value.toLocaleString('en-IN')} Cr
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};
