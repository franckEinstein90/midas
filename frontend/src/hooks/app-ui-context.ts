import { createContext } from "react";
import type { ReportingCurrency } from "@/types/portfolio";

export type Theme = "light" | "dark";

export interface AppUiContextValue {
  reportingCurrency: ReportingCurrency;
  setReportingCurrency: (currency: ReportingCurrency) => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  railCollapsed: boolean;
  setRailCollapsed: (collapsed: boolean) => void;
  toggleRail: () => void;
  chatOpen: boolean;
  setChatOpen: (open: boolean) => void;
  toggleChat: () => void;
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

export const AppUiContext = createContext<AppUiContextValue | undefined>(undefined);
