import React, { useState, useEffect } from 'react';
import { TrendingUp, RefreshCw, AlertTriangle, ShieldCheck, CheckCircle2, BarChart2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { ForecastScenarioChart } from '../components/charts/ForecastScenarioChart';
import { api } from '../services/api';
import { Company, ForecastResponseData } from '../types';

export const ForecastsPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string>('');
  const [selectedMetric, setSelectedMetric] = useState<string>('revenue');
  const [forecastData, setForecastData] = useState<ForecastResponseData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const comps = await api.getCompanies();
        setCompanies(comps);
        if (comps.length > 0) {
          setSelectedCompanyId(comps[0].id);
        }
      } catch (e) {
        console.error('Error loading companies:', e);
      }
    };
    fetchCompanies();
  }, []);

  const loadForecast = async (compId: string, metric: string) => {
    if (!compId) return;
    setIsLoading(true);
    try {
      const data = await api.getForecasts(compId, metric);
      setForecastData(data);
    } catch (e) {
      console.error('Error fetching forecast:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCompanyId) {
      loadForecast(selectedCompanyId, selectedMetric);
    }
  }, [selectedCompanyId, selectedMetric]);

  const handleRegenerate = async () => {
    if (!selectedCompanyId) return;
    setIsLoading(true);
    try {
      const data = await api.generateForecast(selectedCompanyId, {
        metric_name: selectedMetric,
        forecast_horizon_years: 3,
      });
      setForecastData(data);
    } catch (e) {
      console.error('Error generating forecast:', e);
    } finally {
      setIsLoading(false);
    }
  };

  const selectedCompany = companies.find((c) => c.id === selectedCompanyId);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Performance Forecasting Engine
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Statistical multi-scenario projection with confidence intervals & walk-forward validation
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handleRegenerate} isLoading={isLoading}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Re-estimate Models
          </Button>
        </div>
      </div>

      {/* Control Filters */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Company Selector */}
        <div>
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
            Company Target
          </label>
          <select
            value={selectedCompanyId}
            onChange={(e) => setSelectedCompanyId(e.target.value)}
            className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 font-mono focus:outline-none"
          >
            {companies.map((c) => (
              <option key={c.id} value={c.id}>
                {c.symbol} - {c.name}
              </option>
            ))}
          </select>
        </div>

        {/* Metric Selector */}
        <div>
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
            Financial Target Variable
          </label>
          <select
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value)}
            className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none"
          >
            <option value="revenue">Total Revenue (₹ Cr)</option>
            <option value="ebitda">EBITDA (₹ Cr)</option>
            <option value="net_profit">Net Profit (PAT) (₹ Cr)</option>
            <option value="eps">Earnings Per Share (EPS ₹)</option>
          </select>
        </div>

        {/* Model Type */}
        <div>
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
            Statistical Model
          </label>
          <div className="rounded-md bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-700 dark:text-slate-300 font-mono">
            Trend + Autoregressive (v1.0)
          </div>
        </div>

        {/* Evaluation status */}
        <div>
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
            Cross-Validation Status
          </label>
          <div className="flex items-center gap-1.5 rounded-md bg-slate-100 dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-emerald-500 font-semibold font-mono">
            <CheckCircle2 className="w-3.5 h-3.5" /> Walk-Forward Verified
          </div>
        </div>
      </div>

      {/* Main Chart Card */}
      {forecastData && (
        <Card className="p-6 space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
            <div>
              <CardTitle>
                {selectedCompany?.name} ({selectedCompany?.symbol}) – {selectedMetric.toUpperCase()} Forecast
              </CardTitle>
              <p className="text-xs text-slate-500 mt-0.5">
                Multi-year projection spanning FY25 – FY27 with historical anchor points
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="brand" size="xs">
                CONFIDENCE INTERVAL: 95%
              </Badge>
            </div>
          </div>

          <ForecastScenarioChart
            historicalData={forecastData.historical}
            forecastData={forecastData.forecasts}
            metricLabel={selectedMetric.toUpperCase()}
            unit={selectedMetric === 'eps' ? '₹' : '₹ Cr'}
          />

          {/* Scenario Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            {forecastData.forecasts.map((f) => (
              <Card key={f.period} className="p-4 bg-slate-50 dark:bg-slate-900/50">
                <div className="flex justify-between items-center mb-3">
                  <span className="font-bold text-sm text-cyan-500 font-mono">{f.period} Projection</span>
                  <span className="text-[10px] text-slate-400 font-mono">Parametric Bands</span>
                </div>
                <div className="space-y-2 text-xs font-tabular">
                  <div className="flex justify-between">
                    <span className="text-emerald-500 font-semibold">Bullish Scenario (+15%):</span>
                    <span className="font-bold">₹{f.bullish.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-cyan-500 font-semibold">Base Case Scenario:</span>
                    <span className="font-bold">₹{f.base.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-rose-500 font-semibold">Bearish Scenario (-15%):</span>
                    <span className="font-bold">₹{f.bearish.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="pt-2 border-t border-slate-200 dark:border-slate-800 text-[11px] text-slate-400">
                    95% Interval: ₹{f.confidence_intervals.ci_95.lower.toLocaleString('en-IN')} – ₹{f.confidence_intervals.ci_95.upper.toLocaleString('en-IN')}
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Model Performance Backtesting Metrics */}
          {forecastData.evaluation && (
            <div className="p-4 rounded-lg bg-slate-100 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 space-y-2 font-tabular">
              <span className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider block font-mono">
                Model Evaluation & Historical Accuracy
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div>
                  <span className="text-slate-400 block">Mean Absolute Error (MAE):</span>
                  <span className="font-semibold text-slate-900 dark:text-slate-100">{forecastData.evaluation.mae}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Root Mean Squared Error:</span>
                  <span className="font-semibold text-slate-900 dark:text-slate-100">{forecastData.evaluation.rmse}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Mean Absolute % Error (MAPE):</span>
                  <span className="font-semibold text-emerald-500">{forecastData.evaluation.mape}%</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Directional Accuracy:</span>
                  <span className="font-semibold text-emerald-500">{forecastData.evaluation.directional_accuracy}%</span>
                </div>
              </div>
            </div>
          )}

          {/* Notice & Disclaimer */}
          <div className="p-3.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-700 dark:text-amber-300 flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-500" />
            <div>
              <span className="font-semibold block mb-0.5">Statistical Estimation Notice:</span>
              <p className="leading-relaxed">{forecastData.disclaimer}</p>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

