import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency, formatPercent, formatSignedCurrency } from "@/lib/utils";
import type { ImportRecord, ScenarioComparison } from "@/types/portfolio";

export function ScenarioCard({ scenario }: { scenario: ScenarioComparison }) {
  const difference = scenario.hypothetical - scenario.actual;
  const differencePct = (difference / scenario.actual) * 100;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Scenario Analysis</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm leading-relaxed text-muted-foreground">{scenario.title}</p>
        <div className="grid gap-3 sm:grid-cols-3">
          <div className="rounded-lg border border-border bg-muted/30 p-4">
            <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Actual
            </p>
            <p className="mt-2 text-xl font-semibold tabular-nums">
              {formatCurrency(scenario.actual)}
            </p>
          </div>
          <div className="rounded-lg border border-midas-blue/20 bg-midas-blue-soft/40 p-4">
            <p className="text-xs font-medium uppercase tracking-wide text-midas-blue">
              Hypothetical
            </p>
            <p className="mt-2 text-xl font-semibold tabular-nums text-midas-blue">
              {formatCurrency(scenario.hypothetical)}
            </p>
          </div>
          <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 dark:border-emerald-800/70 dark:bg-emerald-950/40">
            <p className="text-xs font-medium uppercase tracking-wide text-positive">
              Difference
            </p>
            <p className="mt-2 text-xl font-semibold tabular-nums text-positive">
              {formatSignedCurrency(difference)} ({formatPercent(differencePct, true)})
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function RecentImportsCard({ imports }: { imports: ImportRecord[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Imports / Snapshots</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {imports.map((item) => (
          <div
            key={`${item.source}-${item.timestamp}`}
            className="flex items-center justify-between gap-3 rounded-lg border border-border px-3 py-2.5"
          >
            <div>
              <p className="font-medium text-foreground">{item.source}</p>
              <p className="text-sm text-muted-foreground">{item.timestamp}</p>
            </div>
            <span className="text-sm font-medium text-positive">{item.status}</span>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
