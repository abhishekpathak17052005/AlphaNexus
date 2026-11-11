import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { motion } from 'motion/react';
import { LiquidNavbar } from '../navigation/LiquidNavbar';
import { GlobalSearch } from '../shared/GlobalSearch';

export const AppLayout: React.FC = () => {
  const [searchOpen, setSearchOpen] = useState(false);

  // ⌘K / Ctrl+K shortcut
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setSearchOpen(true);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  return (
    <div
      className="min-h-screen w-full max-w-full overflow-x-hidden"
      style={{ background: 'var(--bg)', color: 'var(--text-1)' }}
    >
      <LiquidNavbar onSearchOpen={() => setSearchOpen(true)} />

      <motion.main
        key="main"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
        className="pb-16 w-full max-w-full overflow-x-hidden"
      >
        <Outlet />
      </motion.main>

      <GlobalSearch open={searchOpen} onClose={() => setSearchOpen(false)} />
    </div>
  );
};
