import React from 'react';
import { motion } from 'motion/react';
import { clsx } from 'clsx';
import { Loader2 } from 'lucide-react';

interface ANButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'brand' | 'lime' | 'ghost' | 'danger';
  size?: 'xs' | 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  iconRight?: boolean;
}

const sizeMap = {
  xs: 'text-[11px] px-2.5 py-1 gap-1',
  sm: 'text-xs px-3 py-1.5 gap-1.5',
  md: 'text-sm px-4 py-2 gap-2',
  lg: 'text-sm px-5 py-2.5 gap-2',
};

export const ANButton: React.FC<ANButtonProps> = ({
  children, variant = 'brand', size = 'md', loading = false,
  icon, iconRight = false, className, disabled, ...rest
}) => {
  const variantClass = {
    brand: 'btn-brand',
    lime:  'btn-lime',
    ghost: 'btn-ghost',
    danger: '',
  }[variant];

  return (
    <motion.button
      whileTap={{ scale: 0.96 }}
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.1 }}
      disabled={disabled || loading}
      className={clsx(
        'inline-flex items-center justify-center font-semibold rounded-lg transition-all select-none',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variant === 'danger' && 'bg-red-600 hover:bg-red-700 text-white border-none',
        variantClass,
        sizeMap[size],
        className,
      )}
      {...(rest as any)}
    >
      {loading ? (
        <Loader2 className="w-3.5 h-3.5 animate-spin" />
      ) : (
        <>
          {!iconRight && icon && <span className="shrink-0">{icon}</span>}
          {children}
          {iconRight && icon && <span className="shrink-0">{icon}</span>}
        </>
      )}
    </motion.button>
  );
};
