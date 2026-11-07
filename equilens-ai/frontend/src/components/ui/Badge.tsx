import React from 'react';

export interface BadgeProps {
  children: React.ReactNode;
  variant?: 'gain' | 'loss' | 'neutral' | 'brand' | 'warning' | 'outline' | 'terminal';
  size?: 'xs' | 'sm' | 'md';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  size = 'sm',
  className = '',
}) => {
  const sizes = {
    xs: 'text-[10px] px-1.5 py-0.5 font-medium',
    sm: 'text-xs px-2 py-0.5 font-medium',
    md: 'text-xs px-2.5 py-1 font-semibold',
  };

  const variants = {
    gain: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20',
    loss: 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20',
    neutral: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700',
    brand: 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/20',
    warning: 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20',
    outline: 'border border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-400',
    terminal: 'bg-slate-900 text-cyan-400 font-mono border border-cyan-500/40 text-[11px]',
  };

  return (
    <span className={`inline-flex items-center gap-1 rounded-md transition-colors ${sizes[size]} ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

