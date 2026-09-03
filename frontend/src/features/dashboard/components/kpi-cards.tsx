import { Card, CardContent } from "@/components/ui/card";
import { Sparkline } from "@/components/charts/sparkline";
import { cn } from "@/lib/utils";
import type { KpiMetric } from "@/types/portfolio";

export function KpiCard({ metric }: { metric: KpiMetric }) {
  return (
    <Card>
      <CardContent className="flex items-start justify-between gap-3 p-5">
        <div className="min-w-0 space-y-2">
          <p className="text-sm font-medium text-muted-foreground">{metric.label}</p>
          <p className="text-2xl font-semibold tracking-tight text-foreground tabular-nums">
            {metric.value}
          </p>
          <p
            className={cn(
              "text-sm font-medium tabular-nums",
              metric.positive === true && "text-positive",
              metric.positive === false && "text-destructive",
              metric.positive === undefined && "text-muted-foreground",
            )}
          >
            {metric.subValue}
          </p>
        </div>
        {metric.trend ? <Sparkline data={metric.trend} positive={metric.positive} /> : null}
      </CardContent>
    </Card>
  );
}

export function KpiGrid({ metrics }: { metrics: KpiMetric[] }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => (
        <KpiCard key={metric.label} metric={metric} />
      ))}
    </div>
  );
}
