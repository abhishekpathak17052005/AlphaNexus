import React, { useState, useEffect } from 'react';
import {
  Bot,
  Send,
  Plus,
  Bookmark,
  Share2,
  Copy,
  Check,
  Building2,
  FileText,
  Clock,
  Sparkles,
  ExternalLink,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import { Company, ResearchMessage, ResearchSession } from '../types';

export const AIResearchPage: React.FC = () => {
  const [sessions, setSessions] = useState<ResearchSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ResearchMessage[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string>('');
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const [sessList, comps] = await Promise.all([
          api.getResearchSessions(),
          api.getCompanies(),
        ]);
        setSessions(sessList);
        setCompanies(comps);
        if (comps.length > 0) setSelectedCompanyId(comps[0].id);

        if (sessList.length > 0) {
          setCurrentSessionId(sessList[0].id);
          const fullSession = await api.getResearchSession(sessList[0].id);
          setMessages(fullSession.messages);
        }
      } catch (e) {
        console.error('Error initializing AI Research:', e);
      }
    };
    init();
  }, []);

  const handleSelectSession = async (sessId: string) => {
    setCurrentSessionId(sessId);
    try {
      const full = await api.getResearchSession(sessId);
      setMessages(full.messages);
    } catch (e) {
      console.error('Failed to load session:', e);
    }
  };

  const handleNewSession = () => {
    setCurrentSessionId(null);
    setMessages([]);
  };

  const handleSend = async () => {
    if (!query.trim()) return;
    const userMsg: any = {
      id: Date.now().toString(),
      session_id: currentSessionId || '',
      role: 'user',
      content: query,
      message_type: 'user_query',
      tokens_used: 0,
      citations: [],
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    const q = query;
    setQuery('');
    setIsLoading(true);

    try {
      const res = await api.sendResearchChat({
        session_id: currentSessionId || undefined,
        company_id: selectedCompanyId || undefined,
        query: q,
      });

      setMessages((prev) => [...prev, res]);
      if (!currentSessionId && res.session_id) {
        setCurrentSessionId(res.session_id);
        const updatedSessions = await api.getResearchSessions();
        setSessions(updatedSessions);
      }
    } catch (e: any) {
      console.error('Research error:', e);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="h-[calc(100vh-6.5rem)] flex gap-4 overflow-hidden">
      {/* Session History Sidebar */}
      <div className="hidden md:flex flex-col w-64 bg-white dark:bg-[#0c1222] border border-slate-200 dark:border-slate-800 rounded-xl p-3 shrink-0">
        <Button variant="primary" size="sm" className="w-full mb-3" onClick={handleNewSession}>
          <Plus className="w-4 h-4 mr-1.5" /> New Research Query
        </Button>
        <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider px-2 py-1">
          Recent Sessions
        </div>
        <div className="flex-1 overflow-y-auto space-y-1">
          {sessions.map((s) => (
            <button
              key={s.id}
              onClick={() => handleSelectSession(s.id)}
              className={`w-full text-left p-2.5 rounded-lg text-xs transition-colors flex flex-col gap-0.5 ${
                currentSessionId === s.id
                  ? 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 font-semibold border border-cyan-500/30'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-850'
              }`}
            >
              <span className="truncate">{s.title || 'Equity Inquiry'}</span>
              <span className="text-[10px] text-slate-400 font-mono">
                {new Date(s.created_at).toLocaleDateString()}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Workspace */}
      <Card className="flex-1 flex flex-col overflow-hidden">
        {/* Session Header / Controls */}
        <div className="p-3.5 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-900/30">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-cyan-500/10 text-cyan-500 border border-cyan-500/20 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Evidence-Grounded Equity Analyst
              </h2>
              <p className="text-[11px] text-slate-400">
                Dual pipeline: BAAI/bge-small-en-v1.5 pgvector search + Gemini 1.5 synthesis
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <select
              value={selectedCompanyId}
              onChange={(e) => setSelectedCompanyId(e.target.value)}
              className="rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-2.5 py-1.5 text-slate-800 dark:text-slate-200 font-mono focus:outline-none"
            >
              <option value="">All Tracked Companies</option>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.symbol} - {c.name}
                </option>
              ))}
            </select>
            <Badge variant="gain" size="xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse mr-1" /> RAG ACTIVE
            </Badge>
          </div>
        </div>

        {/* Messages Feed */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-4 max-w-md mx-auto">
              <div className="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-500 border border-cyan-500/20 flex items-center justify-center">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                  Ask Anything Across Company Filings
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  Query balance sheet footnotes, capex plans, segment EBITDA, or major contract wins.
                  Every answer provides verbatim citations.
                </p>
              </div>

              <div className="w-full space-y-2 text-left text-xs pt-2">
                {[
                  'What are Reliance Industries key capex initiatives in green energy for FY24?',
                  'Analyze TCS operating margins and subcontractor expenses in FY24',
                  'Summarize HDFC Bank asset quality and Gross NPA trends',
                ].map((sample, i) => (
                  <button
                    key={i}
                    onClick={() => setQuery(sample)}
                    className="w-full p-2.5 rounded-lg bg-slate-50 hover:bg-slate-100 dark:bg-slate-900/60 dark:hover:bg-slate-850 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 transition-colors"
                  >
                    "{sample}"
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((m) => (
              <div
                key={m.id}
                className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-xl p-4 sm:p-5 text-xs sm:text-sm space-y-3 ${
                    m.role === 'user'
                      ? 'bg-cyan-600 text-white font-medium'
                      : 'bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-100'
                  }`}
                >
                  {m.role === 'assistant' && (
                    <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
                      <div className="flex items-center gap-2">
                        <Bot className="w-4 h-4 text-cyan-500" />
                        <span className="font-semibold text-xs text-cyan-500 font-mono">
                          EquiLens Intelligence Agent
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant="gain" size="xs">
                          {m.message_type === 'fact_grounded' ? 'Fact Grounded' : 'Synthesis'}
                        </Badge>
                        <button
                          onClick={() => copyToClipboard(m.content, m.id)}
                          className="text-slate-400 hover:text-slate-200"
                          title="Copy response"
                        >
                          {copiedId === m.id ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="whitespace-pre-wrap leading-relaxed">{m.content}</div>

                  {/* Citations Box */}
                  {m.citations && m.citations.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800 space-y-2">
                      <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono flex items-center justify-between">
                        <span>Grounded Document Sources ({m.citations.length})</span>
                      </div>
                      <div className="grid grid-cols-1 gap-2">
                        {m.citations.map((c, cIdx) => (
                          <div
                            key={cIdx}
                            className="p-2.5 rounded-lg bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs"
                          >
                            <div className="flex items-center justify-between text-cyan-500 font-semibold mb-1">
                              <span>
                                [{cIdx + 1}] {c.document_title || 'Annual Report'} • Page {c.page_number || 'N/A'}
                              </span>
                              <span className="text-[10px] text-slate-400 font-mono">
                                Match: {(c.confidence_score * 100).toFixed(0)}%
                              </span>
                            </div>
                            <p className="text-slate-500 dark:text-slate-400 italic">
                              "{c.excerpt}"
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex items-center gap-2.5 text-xs text-cyan-500 font-mono animate-pulse p-3 bg-slate-50 dark:bg-slate-900/40 rounded-lg max-w-sm">
              <Bot className="w-4 h-4 animate-spin" />
              Executing pgvector search & generating citations...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-3 sm:p-4 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0c1222]">
          <div className="flex items-center gap-2">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask an equity research question grounded in official corporate filings..."
              className="flex-1 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg px-4 py-2.5 text-xs sm:text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            />
            <Button
              variant="primary"
              onClick={handleSend}
              disabled={isLoading || !query.trim()}
              className="shrink-0"
            >
              <Send className="w-4 h-4 mr-1.5" /> Research
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

