import { useLayoutEffect, useMemo, useState, type ReactNode } from "react";
import { AppUiContext, type Theme } from "@/hooks/app-ui-context";
import type { ReportingCurrency } from "@/types/portfolio";

const RAIL_STORAGE_KEY = "midas.railCollapsed";
const THEME_STORAGE_KEY = "midas.theme";

function readRailCollapsed(): boolean {
  try {
    return localStorage.getItem(RAIL_STORAGE_KEY) === "1";
  } catch {
    return false;
  }
}

function prefersDark(): boolean {
  try {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  } catch {
    return false;
  }
}

function readTheme(): Theme {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    if (stored === "light" || stored === "dark") return stored;
  } catch {
    // ignore storage failures
  }
  return prefersDark() ? "dark" : "light";
}

function applyTheme(theme: Theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
}

export function AppUiProvider({ children }: { children: ReactNode }) {
  const [reportingCurrency, setReportingCurrency] = useState<ReportingCurrency>("CAD");
  const [searchQuery, setSearchQuery] = useState("");
  const [railCollapsed, setRailCollapsedState] = useState(readRailCollapsed);
  const [chatOpen, setChatOpen] = useState(false);
  const [theme, setThemeState] = useState<Theme>(readTheme);

  useLayoutEffect(() => {
    applyTheme(theme);
  }, [theme]);

  const setRailCollapsed = (collapsed: boolean) => {
    setRailCollapsedState(collapsed);
    try {
      localStorage.setItem(RAIL_STORAGE_KEY, collapsed ? "1" : "0");
    } catch {
      // ignore storage failures
    }
  };

  const setTheme = (next: Theme) => {
    setThemeState(next);
    applyTheme(next);
    try {
      localStorage.setItem(THEME_STORAGE_KEY, next);
    } catch {
      // ignore storage failures
    }
  };

  const value = useMemo(
    () => ({
      reportingCurrency,
      setReportingCurrency,
      searchQuery,
      setSearchQuery,
      railCollapsed,
      setRailCollapsed,
      toggleRail: () => setRailCollapsed(!railCollapsed),
      chatOpen,
      setChatOpen,
      toggleChat: () => setChatOpen((open) => !open),
      theme,
      setTheme,
      toggleTheme: () => setTheme(theme === "dark" ? "light" : "dark"),
    }),
    [reportingCurrency, searchQuery, railCollapsed, chatOpen, theme],
  );

  return <AppUiContext.Provider value={value}>{children}</AppUiContext.Provider>;
}
