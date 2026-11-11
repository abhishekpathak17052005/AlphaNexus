import { create } from 'zustand';

type Theme = 'dark' | 'light';

interface ThemeState {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

function applyTheme(theme: Theme) {
  document.documentElement.setAttribute('data-theme', theme);
  // Keep the .dark class for Tailwind dark: utilities
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}

const stored = (localStorage.getItem('alphanexus-theme') as Theme) || 'dark';
applyTheme(stored);

export const useThemeStore = create<ThemeState>((set) => ({
  theme: stored,
  toggleTheme: () =>
    set((state) => {
      const next: Theme = state.theme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('alphanexus-theme', next);
      applyTheme(next);
      return { theme: next };
    }),
  setTheme: (theme: Theme) => {
    localStorage.setItem('alphanexus-theme', theme);
    applyTheme(theme);
    set({ theme });
  },
}));
