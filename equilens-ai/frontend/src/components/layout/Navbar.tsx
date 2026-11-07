import React, { useState, useEffect } from 'react';
import { Search, Sun, Moon, Bell, Activity, ShieldCheck, User as UserIcon } from 'lucide-react';
import { useThemeStore } from '../../stores/themeStore';
import { api } from '../../services/api';
import { EnginesSummary } from '../../types';
import { Link } from 'react-router-dom';

interface NavbarProps {
  onOpenSearch: () => void;
  isSidebarCollapsed: boolean;
  onToggleSidebar: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenSearch }) => {
  const { theme, toggleTheme } = useThemeStore();
  const [engineSummary, setEngineSummary] = useState<EnginesSummary | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await api.getEngines();
        setEngineSummary(data);
      } catch (e) {
        // Fallback
      }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'Healthy':
        return 'bg-emerald-500';
      case 'Degraded':
        return 'bg-amber-500';
      case 'Critical':
        return 'bg-rose-500';
      default:
        return 'bg-cyan-500';
    }
  };

  return (
    <header className="sticky top-0 z-30 h-14 bg-white/95 dark:bg-[#080d1a]/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800/80 px-4 sm:px-6 flex items-center justify-between">
      {/* Left: Global Search trigger */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenSearch}
          className="flex items-center gap-3 px-3 py-1.5 text-xs text-slate-500 dark:text-slate-400 bg-slate-100 hover:bg-slate-200/80 dark:bg-slate-900/90 dark:hover:bg-slate-850 border border-slate-200 dark:border-slate-800 rounded-md transition-all w-48 sm:w-72 justify-between group"
        >
          <span className="flex items-center gap-2">
            <Search className="w-3.5 h-3.5 text-slate-400 group-hover:text-cyan-500 transition-colors" />
            <span className="truncate">Search Indian Equities (NSE/BSE)...</span>
          </span>
          <kbd className="hidden sm:inline-block text-[10px] bg-slate-200 dark:bg-slate-800 text-slate-500 dark:text-slate-400 px-1.5 py-0.5 rounded border border-slate-300 dark:border-slate-700 font-mono">
            ⌘K
          </kbd>
        </button>
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Engine Registry Health Pill */}
        <Link
          to="/settings"
          className="hidden md:flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 hover:bg-slate-200 dark:bg-slate-900 dark:hover:bg-slate-800/80 border border-slate-200 dark:border-slate-800 transition-colors"
          title="Click to view Central Engine Registry"
        >
          <span className={`w-2 h-2 rounded-full animate-pulse ${getStatusColor(engineSummary?.status)}`} />
          <span className="text-slate-700 dark:text-slate-300">
            {engineSummary ? `Engines: ${engineSummary.ready_count}/${engineSummary.total_engines} Ready` : 'Checking Engines...'}
          </span>
        </Link>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-100 rounded-md hover:bg-slate-100 dark:hover:bg-slate-850 transition-colors"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Theme`}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-700" />}
        </button>

        {/* Notification center */}
        <button
          className="relative p-2 text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-100 rounded-md hover:bg-slate-100 dark:hover:bg-slate-850 transition-colors"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-cyan-500 rounded-full" />
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-200 dark:border-slate-800">
          <div className="w-7 h-7 rounded-full bg-cyan-600/20 text-cyan-500 dark:text-cyan-400 border border-cyan-500/30 flex items-center justify-center font-semibold text-xs">
            EA
          </div>
          <span className="hidden lg:inline-block text-xs font-medium text-slate-800 dark:text-slate-200">
            Lead Analyst
          </span>
        </div>
      </div>
    </header>
  );
};

