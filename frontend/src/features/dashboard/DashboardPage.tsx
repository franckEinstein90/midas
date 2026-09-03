import { AlertCircle } from "lucide-react";
import { PortfolioValueChart } from "@/components/charts/portfolio-value-chart";
import { SectorExposureChart } from "@/components/charts/sector-exposure-chart";
import { AccountAllocationCard, InstitutionAllocationCard } from "@/features/dashboard/components/allocation-cards";
import { HoldingsTable } from "@/features/dashboard/components/holdings-table";
import { KpiGrid } from "@/features/dashboard/components/kpi-cards";
import { RecentImportsCard, ScenarioCard } from "@/features/dashboard/components/scenario-import-cards";
import { dashboardFixtures } from "@/features/dashboard/fixtures";
import {
  useHealthQuery,
  usePortfolioExposureQuery,
  usePortfolioSummaryQuery,
} from "@/hooks/use-portfolio-queries";
import { formatCurrency, formatPercent } from "@/lib/utils";

export function DashboardPage() {
  const healthQuery = useHealthQuery();
  const summaryQuery = usePortfolioSummaryQuery();
  const exposureQuery = usePortfolioExposureQuery();

  const apiConnected = healthQuery.isSuccess;
  const showApiWarning = healthQuery.isError;

  const kpiMetrics = [
    dashboardFixtures.kpis.totalValue,
    dashboardFixtures.kpis.dailyChange,
    dashboardFixtures.kpis.ytdReturn,
    dashboardFixtures.kpis.cashLiquidity,
  ];

  if (
    summaryQuery.isSuccess &&
    summaryQuery.data.total_market_value > 0 &&
    !summaryQuery.data.message
  ) {
    kpiMetrics[0] = {
      ...dashboardFixtures.kpis.totalValue,
      value: formatCurrency(summaryQuery.data.total_market_value),
      subValue: summaryQuery.data.as_of_date
        ? `As of ${summaryQuery.data.as_of_date}`
        : dashboardFixtures.kpis.totalValue.subValue,
    };
  }

  const sectorData =
    exposureQuery.isSuccess && exposureQuery.data.sector.length > 0
      ? exposureQuery.data.sector.map((item) => ({
          name: item.name.charAt(0).toUpperCase() + item.name.slice(1),
          market_value: item.market_value,
          percentage: item.percentage,
        }))
      : dashboardFixtures.sectorExposure;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">
          Portfolio Overview
        </h1>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          Consolidated view of your investments across all institutions and accounts.
        </p>
      </div>

      {showApiWarning ? (
        <div className="flex items-start gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900 dark:border-amber-800/70 dark:bg-amber-950/40 dark:text-amber-100">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <div>
            <p className="font-medium">Backend unavailable — showing development fixtures.</p>
            <p className="mt-1 text-amber-800/90 dark:text-amber-200/90">
              Start the FastAPI server on port 8000 to load live portfolio data.
            </p>
          </div>
        </div>
      ) : null}

      {apiConnected ? (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-800 dark:border-emerald-800/70 dark:bg-emerald-950/40 dark:text-emerald-200">
          Connected to MIDAS API
          {summaryQuery.data?.total_market_value
            ? ` · Live total ${formatCurrency(summaryQuery.data.total_market_value)}`
            : ""}
          {exposureQuery.data?.sector?.[0]
            ? ` · Top sector ${exposureQuery.data.sector[0].name} ${formatPercent(exposureQuery.data.sector[0].percentage)}`
            : ""}
        </div>
      ) : null}

      <KpiGrid metrics={kpiMetrics} />

      <div className="grid gap-4 xl:grid-cols-2">
        <InstitutionAllocationCard institutions={dashboardFixtures.institutions} />
        <AccountAllocationCard accounts={dashboardFixtures.accounts} />
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        <PortfolioValueChart datasets={dashboardFixtures.portfolioHistory} />
        <div className="min-w-0">
          <SectorExposureChart data={sectorData} />
        </div>
      </div>

      <HoldingsTable rows={dashboardFixtures.holdings} />

      <div className="grid gap-4 xl:grid-cols-2">
        <ScenarioCard scenario={dashboardFixtures.scenario} />
        <RecentImportsCard imports={dashboardFixtures.recentImports} />
      </div>
    </div>
  );
}
