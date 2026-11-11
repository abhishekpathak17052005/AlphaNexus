import React from 'react';
import { motion } from 'motion/react';
import { clsx } from 'clsx';

interface ANCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glass?: boolean;
  onClick?: () => void;
  style?: React.CSSProperties;
}

export const ANCard: React.FC<ANCardProps> = ({
  children, className, hover = false, glass = false, onClick, style,
}) => {
  const base = glass ? 'glass-card' : 'card';
  const Tag = onClick ? motion.button : motion.div;

  return (
    <Tag
      className={clsx(base, hover && 'card-hover cursor-pointer', 'overflow-hidden', className)}
      style={style}
      onClick={onClick}
      whileHover={hover ? { y: -2 } : undefined}
      transition={{ duration: 0.18 }}
    >
      {children}
    </Tag>
  );
};

interface KPICardProps {
  label: string;
  value: string;
  change?: string;
  positive?: boolean;
  negative?: boolean;
  icon?: React.ReactNode;
  delay?: number;
}

export const KPICard: React.FC<KPICardProps> = ({
  label, value, change, positive, negative, icon, delay = 0,
}) => {
  return (
    <motion.div
      className="card p-4 card-hover"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className="flex items-start justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-3)' }}>
          {label}
        </span>
        {icon && (
          <div
            className="w-7 h-7 rounded-lg flex items-center justify-center"
            style={{ background: 'var(--brand-muted)' }}
          >
            <span style={{ color: 'var(--brand)' }}>{icon}</span>
          </div>
        )}
      </div>
      <div className="text-2xl font-black tracking-tight font-tabular" style={{ color: 'var(--text-1)' }}>
        {value}
      </div>
      {change && (
        <div
          className="text-xs font-semibold mt-1 font-tabular"
          style={{ color: positive ? 'var(--positive-text)' : negative ? 'var(--negative-text)' : 'var(--text-3)' }}
        >
          {change}
        </div>
      )}
    </motion.div>
  );
};
