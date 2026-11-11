import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppLayout } from './components/layout/AppLayout';
import { OverviewPage }             from './pages/OverviewPage';
import { DiscoverPage }             from './pages/DiscoverPage';
import { CompanyResearchPage }      from './pages/CompanyResearchPage';
import { DocumentIntelligencePage } from './pages/DocumentIntelligencePage';
import { AIResearchPage }           from './pages/AIResearchPage';
import { FinancialAnalyticsPage }   from './pages/FinancialAnalyticsPage';
import { NewsEventsPage }           from './pages/NewsEventsPage';
import { ForecastsPage }            from './pages/ForecastsPage';

// Legacy pages preserved until deprecated
import { CorporateActionsPage }   from './pages/CorporateActionsPage';
import { MarketEventsPage }       from './pages/MarketEventsPage';
import { PeerComparisonPage }     from './pages/PeerComparisonPage';
import { WatchlistPage }          from './pages/WatchlistPage';
import { ResearchReportsPage }    from './pages/ResearchReportsPage';
import { SettingsPage }           from './pages/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30_000,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout />}>
            {/* Primary routes */}
            <Route index                        element={<OverviewPage />} />
            <Route path="discover"              element={<DiscoverPage />} />
            <Route path="company/:symbol"       element={<CompanyResearchPage />} />
            <Route path="documents"             element={<DocumentIntelligencePage />} />
            <Route path="research"              element={<AIResearchPage />} />
            <Route path="analytics"             element={<FinancialAnalyticsPage />} />
            <Route path="news"                  element={<NewsEventsPage />} />
            <Route path="forecasts"             element={<ForecastsPage />} />

            {/* Legacy routes — mapped to nearest equivalent */}
            <Route path="explore"               element={<DiscoverPage />} />
            <Route path="financials"            element={<FinancialAnalyticsPage />} />
            <Route path="corporate-actions"     element={<CorporateActionsPage />} />
            <Route path="market-events"         element={<MarketEventsPage />} />
            <Route path="compare"               element={<PeerComparisonPage />} />
            <Route path="watchlist"             element={<WatchlistPage />} />
            <Route path="reports"               element={<ResearchReportsPage />} />
            <Route path="settings"              element={<SettingsPage />} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
