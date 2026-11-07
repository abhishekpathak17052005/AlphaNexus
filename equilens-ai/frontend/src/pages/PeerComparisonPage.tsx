import React, { useState, useEffect } from 'react';
import { GitCompare, Plus, Check } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { api } from '../services/api';
import { Company } from '../types';

export const PeerComparisonPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedSymbols, setSelectedSymbols] = useState<string[]>(['RELIANCE', 'TCS', 'INFY']);
  const [compareResult, setCompareResult] = useState<any>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const comps = await api.getCompanies();
        setCompanies(comps);
        const res = await api.comparePeers(['RELIANCE', 'TCS', 'INFY']);
        setCompareResult(res);
      } catch (e) {
        console.error('Error fetching peer comparison:', e);
      }
    };
    init();
  }, []);

  const toggleCompany = async (symbol: string) => {
    let next: string[];
    if (selectedSymbols.includes(symbol)) {
      if (selectedSymbols.length <= 2) return; // Keep at least 2
      next = selectedSymbols.filter((s) => s !== symbol);
    } else {
      if (selectedSymbols.length >= 5) return; // Max 5
      next = [...selectedSymbols, symbol];
    }
    setSelectedSymbols(next);
    const res = await api.comparePeers(next);
    setCompareResult(res);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
        <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
          Peer Benchmarking & Relative Valuation
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
          Side-by-side valuation multiples, capital returns, and operating efficiency analysis
        </p>
      </div>

      {/* Select Peers Pills */}
      <Card className="p-4">
        <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 block mb-2 font-mono">
          Select Equities to Compare (2 to 5 peers):
        </span>
        <div className="flex flex-wrap gap-2">
          {companies.map((c) => {
            const isSelected = selectedSymbols.includes(c.symbol);
            return (
              <button
                key={c.id}
                onClick={() => toggleCompany(c.symbol)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono transition-all ${
                  isSelected
                    ? 'bg-cyan-600 text-white font-bold shadow-xs'
                    : 'bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800'
                }`}
              >
                {isSelected && <Check className="w-3.5 h-3.5" />}
                {c.symbol}
              </button>
            );
          })}
        </div>
      </Card>

      {/* Comparison Matrix */}
      {compareResult && (
        <Card>
          <CardHeader>
            <CardTitle>Comparative Valuation Matrix</CardTitle>
          </CardHeader>
          <CardContent className="p-0 overflow-x-auto">
            <table className="w-full text-left text-xs font-tabular">
              <thead className="bg-slate-50 dark:bg-slate-900 text-slate-500 border-b border-slate-200 dark:border-slate-800 font-mono">
                <tr>
                  <th className="p-4">Financial Metric</th>
                  {compareResult.peers.map((p: any) => (
                    <th key={p.id} className="p-4 text-right font-bold text-slate-900 dark:text-slate-100 font-mono">
                      {p.symbol}
                    </th>
                  ))}
                  <th className="p-4 text-right text-cyan-500 font-mono">Peer Median</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                <tr>
                  <td className="p-4 font-semibold text-slate-800 dark:text-slate-200">Market Cap (₹ Cr)</td>
                  {compareResult.peers.map((p: any) => (
                    <td key={p.id} className="p-4 text-right font-bold text-slate-900 dark:text-slate-100">
                      ₹{p.market_cap ? p.market_cap.toLocaleString('en-IN') : '—'}
                    </td>
                  ))}
                  <td className="p-4 text-right text-cyan-500 font-bold">
                    ₹{compareResult.benchmarks?.market_cap?.median?.toLocaleString('en-IN') || '—'}
                  </td>
                </tr>

                <tr>
                  <td className="p-4 font-semibold text-slate-800 dark:text-slate-200">Price-to-Earnings (P/E)</td>
                  {compareResult.peers.map((p: any) => (
                    <td key={p.id} className="p-4 text-right text-slate-900 dark:text-slate-100">
                      {p.pe_ratio || '—'}
                    </td>
                  ))}
                  <td className="p-4 text-right text-cyan-500 font-semibold">
                    {compareResult.benchmarks?.pe_ratio?.median || '—'}
                  </td>
                </tr>

                <tr>
                  <td className="p-4 font-semibold text-slate-800 dark:text-slate-200">Price-to-Book (P/B)</td>
                  {compareResult.peers.map((p: any) => (
                    <td key={p.id} className="p-4 text-right text-slate-900 dark:text-slate-100">
                      {p.pb_ratio || '—'}
                    </td>
                  ))}
                  <td className="p-4 text-right text-cyan-500 font-semibold">
                    {compareResult.benchmarks?.pb_ratio?.median || '—'}
                  </td>
                </tr>

                <tr>
                  <td className="p-4 font-semibold text-slate-800 dark:text-slate-200">Return on Equity (ROE %)</td>
                  {compareResult.peers.map((p: any) => (
                    <td key={p.id} className="p-4 text-right font-bold text-emerald-500">
                      {p.roe ? `${p.roe}%` : '—'}
                    </td>
                  ))}
                  <td className="p-4 text-right text-emerald-500 font-semibold">
                    {compareResult.benchmarks?.roe?.median ? `${compareResult.benchmarks.roe.median}%` : '—'}
                  </td>
                </tr>

                <tr>
                  <td className="p-4 font-semibold text-slate-800 dark:text-slate-200">Return on Capital (ROCE %)</td>
                  {compareResult.peers.map((p: any) => (
                    <td key={p.id} className="p-4 text-right font-bold text-cyan-500">
                      {p.roce ? `${p.roce}%` : '—'}
                    </td>
                  ))}
                  <td className="p-4 text-right text-cyan-500 font-semibold">
                    {compareResult.benchmarks?.roce?.median ? `${compareResult.benchmarks.roce.median}%` : '—'}
                  </td>
                </tr>

                <tr>
                  <td className="p-4 font-semibold text-slate-800 dark:text-slate-200">Dividend Yield %</td>
                  {compareResult.peers.map((p: any) => (
                    <td key={p.id} className="p-4 text-right text-slate-900 dark:text-slate-100">
                      {p.dividend_yield ? `${p.dividend_yield}%` : '—'}
                    </td>
                  ))}
                  <td className="p-4 text-right text-cyan-500 font-semibold">
                    {compareResult.benchmarks?.dividend_yield?.median ? `${compareResult.benchmarks.dividend_yield.median}%` : '—'}
                  </td>
                </tr>
              </tbody>
            </table>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

