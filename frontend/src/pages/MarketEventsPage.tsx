import React, { useState, useEffect } from 'react';
import { Briefcase, Building2, TrendingUp, Handshake, ShieldAlert, DollarSign } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { api } from '../services/api';
import { MarketEvent, Company } from '../types';

export const MarketEventsPage: React.FC = () => {
  const [events, setEvents] = useState<MarketEvent[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const [evData, comps] = await Promise.all([
          api.getMarketEvents(),
          api.getCompanies(),
        ]);
        setEvents(evData);
        setCompanies(comps);
      } catch (e) {
        console.error('Error fetching market events:', e);
      }
    };
    fetchEvents();
  }, []);

  const companyMap = new Map(companies.map((c) => [c.id, c]));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
        <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Market Events & Major Deals Intelligence
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
          Tracking order wins, multi-billion rupee contracts, M&A, joint ventures, and strategic capex
        </p>
      </div>

      {/* Events Feed */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {events.map((ev) => {
          const comp = companyMap.get(ev.company_id);
          return (
            <Card key={ev.id} className="p-5 space-y-3 hover:border-cyan-500/40 transition-all">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="font-bold font-mono text-cyan-500 text-sm">
                    {comp ? comp.symbol : 'EQUITY'}
                  </span>
                  <Badge variant="brand" size="xs">
                    {ev.event_type}
                  </Badge>
                </div>
                {ev.deal_value && (
                  <Badge variant="terminal" size="xs">
                    ₹{ev.deal_value.toLocaleString('en-IN')} Cr
                  </Badge>
                )}
              </div>

              <div>
                <h3 className="font-semibold text-sm sm:text-base text-slate-900 dark:text-slate-100 leading-snug">
                  {ev.title}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
                  {ev.description}
                </p>
              </div>

              {ev.counterparty && (
                <div className="text-xs text-slate-400 flex items-center gap-1.5 font-mono">
                  <Handshake className="w-3.5 h-3.5 text-cyan-500" /> Counterparty: {ev.counterparty}
                </div>
              )}

              {ev.strategic_implications && (
                <div className="p-3 rounded-lg bg-cyan-500/5 border border-cyan-500/20 text-xs">
                  <span className="font-semibold text-cyan-600 dark:text-cyan-400 block mb-0.5">
                    Strategic Business Implications:
                  </span>
                  <p className="text-slate-600 dark:text-slate-300 leading-relaxed text-[11px]">
                    {ev.strategic_implications}
                  </p>
                </div>
              )}

              <div className="pt-2 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center text-[11px] text-slate-400 font-mono">
                <span>Disclosed: {ev.disclosed_date}</span>
                <span className="text-emerald-500 font-medium">Exchange Disclosed</span>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

