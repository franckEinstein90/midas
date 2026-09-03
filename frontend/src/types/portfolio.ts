export type ReportingCurrency = "CAD" | "USD";

export interface PortfolioSummary {
  as_of_date: string | null;
  reporting_currency: string;
  total_market_value: number;
  holding_count: number;
  account_count: number;
  institution_count: number;
  message?: string;
}

export interface HoldingRow {
  account_id: number;
  account_name: string;
  account_type: string;
  institution: string;
  instrument_id: number;
  symbol: string | null;
  instrument_name: string;
  asset_class: string;
  currency: string;
  quantity: number;
  market_price: number | null;
  market_value: number;
  as_of_date: string;
  sector?: string;
  tags?: string[];
}

export interface ExposureItem {
  name: string;
  market_value: number;
  percentage: number;
}

export interface SectorExposureResponse {
  as_of_date: string | null;
  portfolio_total: number;
  sector: ExposureItem[];
  message?: string;
}

export interface AccountSummary {
  id: number;
  account_name: string;
  account_type: string;
  currency: string;
  institution: string;
}

export interface SnapshotPoint {
  as_of_date: string;
  total_market_value: number;
  reporting_currency: string;
}

export interface KpiMetric {
  label: string;
  value: string;
  subValue: string;
  trend?: number[];
  positive?: boolean;
}

export interface InstitutionAllocation {
  name: string;
  value: number;
  percentage: number;
  connected: boolean;
}

export interface AccountAllocation {
  name: string;
  value: number;
  percentage: number;
}

export interface ScenarioComparison {
  title: string;
  actual: number;
  hypothetical: number;
}

export interface ImportRecord {
  source: string;
  timestamp: string;
  status: "Success" | "Failed" | "Pending";
}

export interface DashboardData {
  kpis: {
    totalValue: KpiMetric;
    dailyChange: KpiMetric;
    ytdReturn: KpiMetric;
    cashLiquidity: KpiMetric;
  };
  institutions: InstitutionAllocation[];
  accounts: AccountAllocation[];
  portfolioHistory: Record<string, Array<{ date: string; value: number }>>;
  sectorExposure: ExposureItem[];
  holdings: Array<{
    symbol: string;
    account: string;
    quantity: number;
    value: number;
    sector: string;
    currency: string;
    tags: string[];
  }>;
  scenario: ScenarioComparison;
  recentImports: ImportRecord[];
}
