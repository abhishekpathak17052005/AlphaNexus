import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  Bot, Send, Plus, Copy, Check, Sparkles, FileText,
  ChevronRight, Loader2, Building2,
} from 'lucide-react';
import { ANButton } from '../components/shared/ANButton';
import { api } from '../services/api';
import type { Company, ResearchMessage, ResearchSession, CitationItem } from '../types';

const SAMPLE_PROMPTS = [
  'What are Reliance Industries key capex initiatives in green energy for FY24?',
  'Analyze TCS operating margins and subcontractor expenses in FY24',
  'Summarize HDFC Bank asset quality and Gross NPA trends post-merger',
  'What is L&T consolidated order book as of FY24?',
];

export const AIResearchPage: React.FC = () => {
  const [sessions,   setSessions]   = useState<ResearchSession[]>([]);
  const [sessionId,  setSessionId]  = useState<string | null>(null);
  const [messages,   setMessages]   = useState<ResearchMessage[]>([]);
  const [companies,  setCompanies]  = useState<Company[]>([]);
  const [companyId,  setCompanyId]  = useState('');
  const [query,      setQuery]      = useState('');
  const [loading,    setLoading]    = useState(false);
  const [copied,     setCopied]     = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    Promise.all([api.getResearchSessions(), api.getCompanies()]).then(([sess, comps]) => {
      setSessions(sess);
      setCompanies(comps);
      if (comps.length) setCompanyId(comps[0].id);
    });
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!query.trim() || loading) return;
    const q = query;
    setQuery('');
    setLoading(true);

    const userMsg: ResearchMessage = {
      id: Date.now().toString(),
      session_id: sessionId || '',
      role: 'user',
      content: q,
      message_type: 'user_query',
      tokens_used: 0,
      citations: [],
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await api.sendResearchChat({
        session_id: sessionId || undefined,
        company_id: companyId || undefined,
        query: q,
      });
      setMessages((prev) => [...prev, res]);
      if (!sessionId) {
        setSessionId(res.session_id);
        const updated = await api.getResearchSessions();
        setSessions(updated);
      }
    } catch (e) {
      setMessages((prev) => [...prev, {
        id: Date.now().toString() + '-err',
        session_id: '',
        role: 'assistant',
        content: '⚠️ Request failed. Please check the backend connection.',
        message_type: 'synthesis',
        tokens_used: 0,
        citations: [],
        created_at: new Date().toISOString(),
      }]);
    } finally {
      setLoading(false);
    }
  };

  const copy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  const startNew = () => { setSessionId(null); setMessages([]); };

  return (
    <div className="h-[calc(100vh-100px)] flex gap-4 page-container py-4">
      {/* Sidebar */}
      <aside className="hidden md:flex flex-col w-56 shrink-0 rounded-2xl overflow-hidden"
        style={{ background: 'var(--surface-1)', border: '1px solid var(--border)' }}>
        <div className="p-3" style={{ borderBottom: '1px solid var(--border)' }}>
          <ANButton variant="brand" size="sm" className="w-full" icon={<Plus className="w-3.5 h-3.5" />} onClick={startNew}>
            New Session
          </ANButton>
        </div>
        <div className="p-2 text-[10px] font-bold uppercase tracking-wider px-3 py-2" style={{ color: 'var(--text-4)' }}>
          Recent
        </div>
        <div className="flex-1 overflow-y-auto space-y-0.5 px-1.5 pb-2">
          {sessions.map((s) => (
            <button
              key={s.id}
              onClick={async () => {
                setSessionId(s.id);
                const full = await api.getResearchSession(s.id);
                setMessages(full.messages);
              }}
              className="w-full text-left px-2.5 py-2 rounded-lg text-xs font-medium transition-colors"
              style={{
                background: sessionId === s.id ? 'var(--brand-muted)' : 'transparent',
                color: sessionId === s.id ? 'var(--brand)' : 'var(--text-2)',
              }}
            >
              <div className="truncate">{s.title || 'Research Session'}</div>
            </button>
          ))}
        </div>
      </aside>

      {/* Main chat */}
      <div className="flex-1 flex flex-col rounded-2xl overflow-hidden"
        style={{ background: 'var(--surface-1)', border: '1px solid var(--border)' }}>
        {/* Header */}
        <div className="flex flex-wrap items-center gap-3 p-4" style={{ borderBottom: '1px solid var(--border)' }}>
          <div className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0"
            style={{ background: 'var(--brand-muted)', border: '1px solid var(--border-brand)' }}>
            <Bot className="w-4 h-4" style={{ color: 'var(--brand)' }} />
          </div>
          <div>
            <div className="text-sm font-bold" style={{ color: 'var(--text-1)' }}>AlphaNexus Intelligence Agent</div>
            <div className="text-[10px]" style={{ color: 'var(--text-4)' }}>
              bge-base-en-v1.5 · pgvector ANN · Gemini synthesis
            </div>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <select
              value={companyId}
              onChange={(e) => setCompanyId(e.target.value)}
              className="input text-xs px-2.5 py-1.5"
            >
              <option value="">All Companies</option>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>{c.symbol} — {c.name}</option>
              ))}
            </select>
            <span className="badge badge-lime">RAG ACTIVE</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-5">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-5 py-16">
              <div className="w-14 h-14 rounded-2xl flex items-center justify-center"
                style={{ background: 'var(--brand-muted)', border: '1px solid var(--border-brand)' }}>
                <Sparkles className="w-6 h-6" style={{ color: 'var(--brand)' }} />
              </div>
              <div>
                <div className="font-bold text-lg" style={{ color: 'var(--text-1)' }}>Ask anything about company filings</div>
                <div className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>
                  Every answer is grounded in verified corporate documents with page-level citations.
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-2 w-full max-w-lg text-left">
                {SAMPLE_PROMPTS.map((p) => (
                  <button
                    key={p}
                    onClick={() => setQuery(p)}
                    className="p-3 rounded-xl text-xs font-medium text-left transition-colors"
                    style={{ background: 'var(--surface-2)', border: '1px solid var(--border)', color: 'var(--text-2)' }}
                  >
                    "{p}"
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m) => (
            <div key={m.id} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className="max-w-[85%] rounded-2xl p-4 text-sm space-y-3"
                style={{
                  background: m.role === 'user' ? 'var(--brand)' : 'var(--surface-2)',
                  color: m.role === 'user' ? '#fff' : 'var(--text-1)',
                  border: m.role === 'user' ? 'none' : '1px solid var(--border)',
                }}
              >
                {m.role === 'assistant' && (
                  <div className="flex items-center justify-between pb-2" style={{ borderBottom: '1px solid var(--border)' }}>
                    <div className="flex items-center gap-2 text-xs font-bold" style={{ color: 'var(--brand)' }}>
                      <Bot className="w-3.5 h-3.5" /> AlphaNexus Agent
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="badge badge-brand">{m.message_type === 'fact_grounded' ? 'Fact-Grounded' : 'Synthesis'}</span>
                      <button onClick={() => copy(m.content, m.id)} style={{ color: 'var(--text-4)' }}>
                        {copied === m.id ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  </div>
                )}
                <div className="whitespace-pre-wrap leading-relaxed text-xs md:text-sm">{m.content}</div>

                {/* Citations */}
                {m.citations.length > 0 && (
                  <div className="pt-3 space-y-2" style={{ borderTop: '1px solid var(--border)' }}>
                    <div className="text-[10px] font-bold uppercase tracking-wider" style={{ color: 'var(--text-4)' }}>
                      Sources ({m.citations.length})
                    </div>
                    {m.citations.map((c, ci) => (
                      <div key={ci} className="rounded-lg p-2.5 text-xs space-y-1"
                        style={{ background: 'var(--surface-1)', border: '1px solid var(--border)' }}>
                        <div className="flex items-center justify-between font-semibold" style={{ color: 'var(--brand)' }}>
                          <span>[{ci + 1}] {c.document_title || 'Annual Report'} · Page {c.page_number ?? 'N/A'}</span>
                          <span className="text-[10px] font-mono" style={{ color: 'var(--text-4)' }}>
                            {(c.confidence_score * 100).toFixed(0)}% match
                          </span>
                        </div>
                        <p className="italic text-[11px] leading-relaxed" style={{ color: 'var(--text-3)' }}>
                          "{c.excerpt}"
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2.5 text-xs font-mono animate-pulse" style={{ color: 'var(--brand)' }}>
              <Loader2 className="w-4 h-4 animate-spin" />
              Searching indexed filings and synthesizing response…
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="p-3" style={{ borderTop: '1px solid var(--border)' }}>
          <div className="flex gap-2">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
              placeholder="Ask a research question grounded in official corporate filings…"
              className="input flex-1 px-4 py-2.5 text-sm"
            />
            <ANButton
              variant="brand"
              size="md"
              icon={<Send className="w-4 h-4" />}
              iconRight
              onClick={handleSend}
              disabled={loading || !query.trim()}
            >
              Research
            </ANButton>
          </div>
        </div>
      </div>
    </div>
  );
};
