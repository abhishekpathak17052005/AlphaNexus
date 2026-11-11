import React from 'react';
import { motion } from 'motion/react';

interface NavigationIndicatorProps {
  layoutId?: string;
  showDot?: boolean;
}

/**
 * NavigationIndicator renders the sliding frosted glass active pill
 * and the restrained Acid Lime glow indicator using Motion layout animations.
 */
export const NavigationIndicator: React.FC<NavigationIndicatorProps> = ({
  layoutId = 'liquid-nav-active-pill',
  showDot = true,
}) => {
  return (
    <>
      {/* Frosted brand pill background */}
      <motion.div
        layoutId={layoutId}
        className="absolute inset-0 rounded-xl pointer-events-none z-0"
        style={{
          background: 'var(--brand-muted)',
          border: '1px solid var(--border-brand)',
          boxShadow: '0 2px 12px rgba(21, 88, 201, 0.16), inset 0 1px 0 rgba(255, 255, 255, 0.12)',
        }}
        transition={{
          type: 'spring',
          stiffness: 450,
          damping: 34,
        }}
      />

      {/* Acid Lime active dot */}
      {showDot && (
        <span
          className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full pointer-events-none z-10"
          style={{
            background: 'var(--lime)',
            boxShadow: '0 0 8px var(--lime)',
          }}
          aria-hidden="true"
        />
      )}
    </>
  );
};

