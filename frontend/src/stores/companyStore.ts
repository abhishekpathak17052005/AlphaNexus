import { create } from 'zustand';
import { Company } from '../types';

interface CompanyState {
  selectedCompany: Company | null;
  activeTab: string;
  setSelectedCompany: (company: Company | null) => void;
  setActiveTab: (tab: string) => void;
}

export const useCompanyStore = create<CompanyState>((set) => ({
  selectedCompany: null,
  activeTab: 'overview',
  setSelectedCompany: (company) => set({ selectedCompany: company }),
  setActiveTab: (tab) => set({ activeTab: tab }),
}));

