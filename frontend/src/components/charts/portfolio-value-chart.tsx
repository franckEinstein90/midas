import { useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { formatCurrency } from "@/lib/utils";

const ranges = ["1M", "3M", "YTD", "1Y", "All"] as const;
type RangeKey = (typeof ranges)[number];

export function PortfolioValueChart({
  datasets,
}: {
  datasets: Record<string, Array<{ date: string; value: number }>>;
}) {
  const [range, setRange] = useState<RangeKey>("YTD");
  const data = useMemo(() => datasets[range] ?? [], [datasets, range]);

  return (
    <Card className="col-span-full xl:col-span-2">
      <CardHeader className="flex flex-row items-center justify-between gap-4 space-y-0">
        <CardTitle>Portfolio Value Over Time</CardTitle>
        <Tabs value={range} onValueChange={(value) => setRange(value as RangeKey)}>
          <TabsList>
            {ranges.map((item) => (
              <TabsTrigger key={item} value={item}>
                {item}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </CardHeader>
      <CardContent>
        <div className="h-[320px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="portfolioFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#1e40af" stopOpacity={0.18} />
                  <stop offset="95%" stopColor="#1e40af" stopOpacity={0.01} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis
                dataKey="date"
                tickLine={false}
                axisLine={false}
                tick={{ fill: "var(--muted-foreground)", fontSize: 12 }}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                tick={{ fill: "var(--muted-foreground)", fontSize: 12 }}
                tickFormatter={(value: number) =>
                  formatCurrency(value, "CAD", { compact: true })
                }
              />
              <Tooltip
                formatter={(value) => [
                  formatCurrency(Number(value ?? 0)),
                  "Value",
                ]}
                contentStyle={{
                  borderRadius: 8,
                  backgroundColor: "var(--card)",
                  borderColor: "var(--border)",
                  color: "var(--foreground)",
                  boxShadow: "0 8px 24px rgba(15, 23, 42, 0.18)",
                }}
                labelStyle={{ color: "var(--muted-foreground)" }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#1e40af"
                strokeWidth={2}
                fill="url(#portfolioFill)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
