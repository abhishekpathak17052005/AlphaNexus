import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Bookmark, Plus, Trash2, ArrowUpRight, TrendingUp, TrendingDown, Target } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Modal } from '../components/ui/Modal';
import { api } from '../services/api';
import { WatchlistItem, Company } from '../types';

export const WatchlistPage: React.FC = () => {
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [selectedCompId, setSelectedCompId] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [notes, setNotes] = useState('');

  const loadData = async () => {
    try {
      const [wData, comps] = await Promise.all([api.getWatchlist(), api.getCompanies()]);
      setWatchlist(wData);
      setCompanies(comps);
      if (comps.length > 0) setSelectedCompId(comps[0].id);
    } catch (e) {
      console.error('Error fetching watchlist:', e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAdd = async () => {
    if (!selectedCompId) return;
    try {
      await api.addToWatchlist({
        company_id: selectedCompId,
        target_price: targetPrice ? parseFloat(targetPrice) : undefined,
        notes: notes.trim() || undefined,
      });
      setIsAddOpen(false);
      setTargetPrice('');
      setNotes('');
      await loadData();
    } catch (e: any) {
      alert(`Error adding to watchlist: ${e.message}`);
    }
  };

  const handleRemove = async (compId: string) => {
    try {
      await api.removeFromWatchlist(compId);
      await loadData();
    } catch (e: any) {
      alert(`Error removing: ${e.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Equity Watchlist & Price Targets
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Personalized monitoring workspace with target price tracking and valuation alerts
          </p>
        </div>
        <Button variant="primary" size="sm" onClick={() => setIsAddOpen(true)}>
          <Plus className="w-3.5 h-3.5 mr-1.5" /> Add Company
        </Button>
      </div>

      {/* Watchlist Table */}
      <Card>
        <CardHeader>
          <CardTitle>Tracked Equities ({watchlist.length})</CardTitle>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto">
          {watchlist.length === 0 ? (
            <div className="py-16 text-center text-xs text-slate-400">
              <Bookmark className="w-8 h-8 text-cyan-500 mx-auto mb-2 opacity-50" />
              Your equity watchlist is currently empty. Add stocks to monitor prices and targets.
            </div>
          ) : (
            <table className="w-full text-left text-xs font-tabular">
              <thead className="bg-slate-50 dark:bg-slate-900 text-slate-500 border-b border-slate-200 dark:border-slate-800 font-mono">
                <tr>
                  <th className="p-3">Symbol</th>
                  <th className="p-3">Company</th>
                  <th className="p-3 text-right">LTP (₹)</th>
                  <th className="p-3 text-right">1D Change</th>
                  <th className="p-3 text-right">Target Price (₹)</th>
                  <th className="p-3">Analyst Notes</th>
                  <th className="p-3 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {watchlist.map((item) => {
                  const comp = item.company;
                  return (
                    <tr key={item.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-850/50">
                      <td className="p-3 font-semibold font-mono text-cyan-500">
                        {comp ? <Link to={`/company/${comp.symbol}`}>{comp.symbol}</Link> : '—'}
                      </td>
                      <td className="p-3 font-sans text-slate-800 dark:text-slate-200">{comp?.name}</td>
                      <td className="p-3 text-right font-bold text-slate-900 dark:text-slate-100">
                        ₹{comp?.current_price?.toLocaleString('en-IN') || '—'}
                      </td>
                      <td
                        className={`p-3 text-right font-medium ${
                          comp?.day_change && comp.day_change >= 0 ? 'text-emerald-500' : 'text-rose-500'
                        }`}
                      >
                        {comp?.day_change && comp.day_change > 0 ? '+' : ''}
                        {comp?.day_change_percent || 0}%
                      </td>
                      <td className="p-3 text-right font-bold text-cyan-500">
                        {item.target_price ? `₹${item.target_price.toLocaleString('en-IN')}` : '—'}
                      </td>
                      <td className="p-3 text-slate-500 font-sans max-w-xs truncate">{item.notes || '—'}</td>
                      <td className="p-3 text-center">
                        <button
                          onClick={() => handleRemove(item.company_id)}
                          className="p-1 text-slate-400 hover:text-rose-500 transition-colors"
                          title="Remove from watchlist"
                        >
                          <Trash2 className="w-4 h-4 inline" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </CardContent>
      </Card>

      {/* Add Modal */}
      <Modal isOpen={isAddOpen} onClose={() => setIsAddOpen(false)} title="Add Company to Watchlist">
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Select Company
            </label>
            <select
              value={selectedCompId}
              onChange={(e) => setSelectedCompId(e.target.value)}
              className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none"
            >
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.symbol} - {c.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Target Price (₹) (Optional)
            </label>
            <input
              type="number"
              placeholder="e.g. 3200"
              value={targetPrice}
              onChange={(e) => setTargetPrice(e.target.value)}
              className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Investment Thesis / Notes (Optional)
            </label>
            <textarea
              rows={3}
              placeholder="Thesis: Capex expansion into green energy; target P/E re-rating to 30x."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none"
            />
          </div>

          <div className="pt-2 flex justify-end gap-2">
            <Button variant="outline" size="sm" onClick={() => setIsAddOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" size="sm" onClick={handleAdd}>
              Save to Watchlist
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

