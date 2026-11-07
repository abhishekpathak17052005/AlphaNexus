import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppLayout } from './components/layout/AppLayout';
import { OverviewPage } from './pages/OverviewPage';
import { ExploreCompaniesPage } from './pages/ExploreCompaniesPage';
import { CompanyDetailPage } from './pages/CompanyDetailPage';
import { DocumentIntelligencePage } from './pages/DocumentIntelligencePage';
import { AIResearchPage } from './pages/AIResearchPage';
import { ForecastsPage } from './pages/ForecastsPage';
import { NewsIntelligencePage } from './pages/NewsIntelligencePage';
import { CorporateActionsPage } from './pages/CorporateActionsPage';
import { MarketEventsPage } from './pages/MarketEventsPage';
import { PeerComparisonPage } from './pages/PeerComparisonPage';
import { WatchlistPage } from './pages/WatchlistPage';
import { ResearchReportsPage } from './pages/ResearchReportsPage';
import { SettingsPage } from './pages/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout />}>
            <Route index element={<OverviewPage />} />
            <Route path="explore" element={<ExploreCompaniesPage />} />
            <Route path="company/:symbol" element={<CompanyDetailPage />} />
            <Route path="documents" element={<DocumentIntelligencePage />} />
            <Route path="research" element={<AIResearchPage />} />
            <Route path="forecasts" element={<ForecastsPage />} />
            <Route path="news" element={<NewsIntelligencePage />} />
            <Route path="corporate-actions" element={<CorporateActionsPage />} />
            <Route path="market-events" element={<MarketEventsPage />} />
            <Route path="compare" element={<PeerComparisonPage />} />
            <Route path="watchlist" element={<WatchlistPage />} />
            <Route path="reports" element={<ResearchReportsPage />} />
            <Route path="financials" element={<ExploreCompaniesPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
