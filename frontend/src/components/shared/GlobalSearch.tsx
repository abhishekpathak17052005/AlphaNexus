import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Search, X, TrendingUp, Building2, FileText, Bot } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import type { Company } from '../../types';

interface GlobalSearchProps {
  open: boolean;
  onClose: () => void;
}

export const GlobalSearch: React.FC<GlobalSearchProps> = ({ open, onClose }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Company[]>([]);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 80);
      setQuery('');
      setResults([]);
    }
  }, [open]);

  useEffect(() => {
    if (!query.trim() || query.length < 2) { setResults([]); return; }
    setLoading(true);
    const timer = setTimeout(async () => {
      try {
        const data = await api.searchCompanies(query);
        setResults(data.slice(0, 6));
      } catch { setResults([]); }
      finally { setLoading(false); }
    }, 280);
    return () => clearTimeout(timer);
  }, [query]);

  const goTo = (symbol: string) => {
    navigate(`/company/${symbol}`);
    onClose();
  };

  const quickLinks = [
    { label: 'AI Research', path: '/research', icon: Bot },
    { label: 'Document Intelligence', path: '/documents', icon: FileText },
    { label: 'Financial Analytics', path: '/analytics', icon: TrendingUp },
    { label: 'Discover Companies', path: '/discover', icon: Building2 },
  ];

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 z-50"
            style={{ background: 'rgba(3,4,7,0.75)', backdropFilter: 'blur(8px)' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            className="fixed left-1/2 top-24 z-50 w-full max-w-xl"
            style={{ transform: 'translateX(-50%)' }}
            initial={{ y: -20, opacity: 0, scale: 0.96 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: -16, opacity: 0, scale: 0.96 }}
            transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="glass-navbar rounded-2xl overflow-hidden mx-4" style={{ border: '1px solid var(--border-strong)' }}>
              {/* Input */}
              <div className="flex items-center gap-3 p-4" style={{ borderBottom: '1px solid var(--border)' }}>
                <Search className="w-4 h-4 shrink-0" style={{ color: 'var(--text-3)' }} />
                <input
                  ref={inputRef}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search companies, tickers, news…"
                  className="flex-1 bg-transparent text-sm font-medium focus:outline-none"
                  style={{ color: 'var(--text-1)' }}
                  onKeyDown={(e) => { if (e.key === 'Escape') onClose(); }}
                />
                {query && (
                  <button onClick={() => setQuery('')} style={{ color: 'var(--text-4)' }}>
                    <X className="w-4 h-4" />
                  </button>
                )}
                <kbd
                  className="text-[10px] px-1.5 py-0.5 rounded font-mono"
                  style={{ background: 'var(--surface-3)', color: 'var(--text-4)', border: '1px solid var(--border)' }}
                >
                  ESC
                </kbd>
              </div>

              {/* Results */}
              <div className="max-h-72 overflow-y-auto p-2">
                {results.length > 0 ? (
                  <>
                    <p className="text-[10px] font-bold uppercase tracking-wider px-2 py-1.5" style={{ color: 'var(--text-4)' }}>
                      Companies
                    </p>
                    {results.map((c) => (
                      <button
                        key={c.id}
                        onClick={() => goTo(c.symbol)}
                        className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors hover:bg-[var(--brand-muted)]"
                      >
                        <div
                          className="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-black shrink-0"
                          style={{ background: 'var(--brand-muted)', color: 'var(--brand)' }}
                        >
                          {c.symbol.slice(0, 2)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-semibold truncate" style={{ color: 'var(--text-1)' }}>{c.name}</div>
                          <div className="text-xs font-mono" style={{ color: 'var(--text-3)' }}>
                            {c.symbol} · {c.exchange}
                          </div>
                        </div>
                        {c.current_price && (
                          <div className="text-sm font-bold font-tabular" style={{ color: 'var(--text-1)' }}>
                            ₹{c.current_price.toLocaleString('en-IN')}
                          </div>
                        )}
                      </button>
                    ))}
                  </>
                ) : query.length >= 2 && !loading ? (
                  <div className="py-8 text-center text-sm" style={{ color: 'var(--text-3)' }}>
                    No companies found for "{query}"
                  </div>
                ) : !query ? (
                  <>
                    <p className="text-[10px] font-bold uppercase tracking-wider px-2 py-1.5" style={{ color: 'var(--text-4)' }}>
                      Quick Access
                    </p>
                    {quickLinks.map((link) => {
                      const Icon = link.icon;
                      return (
                        <button
                          key={link.path}
                          onClick={() => { navigate(link.path); onClose(); }}
                          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-colors hover:bg-[var(--surface-2)]"
                        >
                          <div className="w-7 h-7 rounded-lg flex items-center justify-center" style={{ background: 'var(--surface-3)' }}>
                            <Icon className="w-3.5 h-3.5" style={{ color: 'var(--brand)' }} />
                          </div>
                          <span className="text-sm font-medium" style={{ color: 'var(--text-2)' }}>{link.label}</span>
                        </button>
                      );
                    })}
                  </>
                ) : null}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
