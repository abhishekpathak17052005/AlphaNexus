import React, { useState, useEffect } from 'react';
import { CalendarDays, Filter, DollarSign, Share2, Layers } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { api } from '../services/api';
import { CorporateAction, Company } from '../types';

export const CorporateActionsPage: React.FC = () => {
  const [actions, setActions] = useState<CorporateAction[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedType, setSelectedType] = useState<string>('ALL');

  useEffect(() => {
    const fetchActions = async () => {
      try {
        const [actData, comps] = await Promise.all([
          api.getCorporateActions({
            action_type: selectedType !== 'ALL' ? selectedType : undefined,
          }),
          api.getCompanies(),
        ]);
        setActions(actData);
        setCompanies(comps);
      } catch (e) {
        console.error('Error fetching corporate actions:', e);
      }
    };
    fetchActions();
  }, [selectedType]);

  const companyMap = new Map(companies.map((c) => [c.id, c]));

  const TYPES = ['ALL', 'Dividend', 'Bonus', 'Stock Split', 'Buyback', 'Rights Issue'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
        <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Corporate Actions Intelligence
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
          Dividends, Bonus shares, Stock splits, Buybacks, and Record Date timeline across Indian equities
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        {TYPES.map((t) => (
          <button
            key={t}
            onClick={() => setSelectedType(t)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              selectedType === t
                ? 'bg-cyan-600 text-white font-semibold'
                : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Corporate Actions Table */}
      <Card>
        <CardHeader>
          <CardTitle>Corporate Actions Schedule</CardTitle>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto">
          <table className="w-full text-left text-xs font-tabular">
            <thead className="bg-slate-50 dark:bg-slate-900 text-slate-500 border-b border-slate-200 dark:border-slate-800 font-mono">
              <tr>
                <th className="p-3">Company</th>
                <th className="p-3">Type</th>
                <th className="p-3">Details & Rationale</th>
                <th className="p-3 text-right">Ratio / Amount</th>
                <th className="p-3 text-right">Ex-Date</th>
                <th className="p-3 text-right">Payment Date</th>
                <th className="p-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {actions.map((act) => {
                const comp = companyMap.get(act.company_id);
                return (
                  <tr key={act.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-850/50">
                    <td className="p-3 font-semibold font-mono text-cyan-500">
                      {comp ? comp.symbol : 'EQUITY'}
                    </td>
                    <td className="p-3">
                      <Badge variant="brand" size="xs">
                        {act.action_type}
                      </Badge>
                    </td>
                    <td className="p-3 text-slate-700 dark:text-slate-300 font-sans max-w-md">
                      {act.details}
                    </td>
                    <td className="p-3 text-right font-bold text-slate-900 dark:text-slate-100">
                      {act.ratio_or_amount || '—'}
                    </td>
                    <td className="p-3 text-right text-slate-600 dark:text-slate-400 font-mono">
                      {act.ex_date || '—'}
                    </td>
                    <td className="p-3 text-right text-slate-600 dark:text-slate-400 font-mono">
                      {act.payment_date || '—'}
                    </td>
                    <td className="p-3 text-center">
                      <Badge variant="gain" size="xs">
                        {act.status}
                      </Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
};

