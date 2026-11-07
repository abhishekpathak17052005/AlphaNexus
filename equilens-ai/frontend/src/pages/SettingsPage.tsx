import React, { useState, useEffect } from 'react';
import {
  Activity,
  Database,
  Cpu,
  Bot,
  Layers,
  Server,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  ShieldCheck,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { useThemeStore } from '../stores/themeStore';
import { api } from '../services/api';
import { EnginesSummary } from '../types';

export const SettingsPage: React.FC = () => {
  const { theme, toggleTheme } = useThemeStore();
  const [engineSummary, setEngineSummary] = useState<EnginesSummary | null>(null);
  const [healthData, setHealthData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchStatus = async () => {
    setIsLoading(true);
    try {
      const [engines, health] = await Promise.all([api.getEngines(), api.getHealth()]);
      setEngineSummary(engines);
      setHealthData(health);
    } catch (e) {
      console.error('Failed to load engines status:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const getStateBadge = (state: string) => {
    switch (state) {
      case 'Ready':
        return (
          <Badge variant="gain" size="sm">
            <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Ready
          </Badge>
        );
      case 'Degraded':
        return (
          <Badge variant="warning" size="sm">
            <AlertTriangle className="w-3.5 h-3.5 mr-1" /> Degraded
          </Badge>
        );
      case 'Disabled':
        return (
          <Badge variant="neutral" size="sm">
            <HelpCircle className="w-3.5 h-3.5 mr-1" /> Disabled
          </Badge>
        );
      case 'Failed':
        return (
          <Badge variant="loss" size="sm">
            <XCircle className="w-3.5 h-3.5 mr-1" /> Failed
          </Badge>
        );
      default:
        return <Badge size="sm">{state}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Central Engine Registry & System Status
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real-time introspection and health monitoring across all backend engines & provider adapters
          </p>
        </div>
        <Button variant="primary" size="sm" onClick={fetchStatus} isLoading={isLoading}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh Engines
        </Button>
      </div>

      {/* Engine Registry Metrics */}
      {engineSummary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-tabular">
          <Card className="p-4">
            <span className="text-xs text-slate-400 font-mono block">Overall Status</span>
            <span
              className={`text-xl font-bold ${
                engineSummary.status === 'Healthy'
                  ? 'text-emerald-500'
                  : engineSummary.status === 'Degraded'
                  ? 'text-amber-500'
                  : 'text-rose-500'
              }`}
            >
              {engineSummary.status}
            </span>
          </Card>
          <Card className="p-4">
            <span className="text-xs text-slate-400 font-mono block">Engines Ready</span>
            <span className="text-xl font-bold text-emerald-500">
              {engineSummary.ready_count} / {engineSummary.total_engines}
            </span>
          </Card>
          <Card className="p-4">
            <span className="text-xs text-slate-400 font-mono block">Degraded / Demo</span>
            <span className="text-xl font-bold text-amber-500">{engineSummary.degraded_count}</span>
          </Card>
          <Card className="p-4">
            <span className="text-xs text-slate-400 font-mono block">Disabled Providers</span>
            <span className="text-xl font-bold text-slate-400">{engineSummary.disabled_count}</span>
          </Card>
        </div>
      )}

      {/* Central Engine Status Grid */}
      <Card>
        <CardHeader>
          <CardTitle>Engine Architecture & Provider Registry</CardTitle>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto">
          {engineSummary ? (
            <table className="w-full text-left text-xs font-tabular">
              <thead className="bg-slate-50 dark:bg-slate-900 text-slate-500 border-b border-slate-200 dark:border-slate-800 font-mono">
                <tr>
                  <th className="p-4">Engine Name</th>
                  <th className="p-4">Status</th>
                  <th className="p-4">Active Provider</th>
                  <th className="p-4">Engine Details / Connectivity</th>
                  <th className="p-4 text-right">Last Verified</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {Object.entries(engineSummary.engines).map(([key, engine]) => (
                  <tr key={key} className="hover:bg-slate-50/80 dark:hover:bg-slate-850/50">
                    <td className="p-4 font-semibold text-slate-900 dark:text-slate-100 font-sans">
                      {engine.name}
                    </td>
                    <td className="p-4">{getStateBadge(engine.state)}</td>
                    <td className="p-4 font-mono text-cyan-500 font-medium">
                      {engine.provider || 'Core Engine'}
                    </td>
                    <td className="p-4 text-slate-600 dark:text-slate-300 font-sans max-w-md">
                      {engine.details}
                    </td>
                    <td className="p-4 text-right text-slate-400 font-mono text-[11px]">
                      {new Date(engine.last_checked).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="py-12 text-center text-xs text-slate-400">Loading engine registry...</div>
          )}
        </CardContent>
      </Card>

      {/* Configuration & Preferences */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-5 space-y-4">
          <CardTitle>Interface & Terminal Appearance</CardTitle>
          <div className="flex items-center justify-between pt-2">
            <div>
              <span className="text-sm font-semibold text-slate-900 dark:text-slate-100 block">
                Color Theme
              </span>
              <span className="text-xs text-slate-400">
                Currently using {theme === 'dark' ? 'Dark Terminal (Default)' : 'Light Fintech'}
              </span>
            </div>
            <Button variant="outline" size="sm" onClick={toggleTheme}>
              Toggle to {theme === 'dark' ? 'Light' : 'Dark'}
            </Button>
          </div>
        </Card>

        <Card className="p-5 space-y-4">
          <CardTitle>Environment & Deployment</CardTitle>
          <div className="space-y-2 text-xs font-mono text-slate-600 dark:text-slate-300">
            <div className="flex justify-between">
              <span>Environment:</span>
              <span className="font-bold text-cyan-500">{healthData?.environment || 'development'}</span>
            </div>
            <div className="flex justify-between">
              <span>Data Mode:</span>
              <span className="font-bold text-emerald-500">{healthData?.data_mode || 'demo'}</span>
            </div>
            <div className="flex justify-between">
              <span>Target Market:</span>
              <span className="font-bold text-slate-100">National Stock Exchange (NSE) + BSE</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

