import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { ExposureItem } from "@/types/portfolio";

const COLORS = [
  "#1e40af",
  "#2563eb",
  "#0891b2",
  "#059669",
  "#ca8a04",
  "#ea580c",
  "#9333ea",
  "#64748b",
];

export function SectorExposureChart({ data }: { data: ExposureItem[] }) {
  return (
    <Card className="min-w-0 overflow-hidden">
      <CardHeader>
        <CardTitle>Sector Exposure</CardTitle>
      </CardHeader>
      <CardContent className="min-w-0">
        <div className="flex min-w-0 flex-col items-stretch gap-5 sm:flex-row sm:items-center">
          <div className="mx-auto h-40 w-40 shrink-0 sm:mx-0 sm:h-44 sm:w-44">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  dataKey="percentage"
                  nameKey="name"
                  innerRadius={48}
                  outerRadius={72}
                  paddingAngle={2}
                >
                  {data.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value, _name, item) => [
                    `${Number(value ?? 0).toFixed(1)}%`,
                    String(item?.payload?.name ?? "Sector"),
                  ]}
                  contentStyle={{
                    borderRadius: 8,
                    backgroundColor: "var(--card)",
                    borderColor: "var(--border)",
                    color: "var(--foreground)",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <ul className="min-w-0 flex-1 space-y-2 overflow-hidden">
            {data.map((item, index) => (
              <li
                key={item.name}
                className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-x-3 text-sm"
              >
                <div className="flex min-w-0 items-center gap-2">
                  <span
                    className="h-2.5 w-2.5 shrink-0 rounded-full"
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  />
                  <span className="truncate text-foreground">{item.name}</span>
                </div>
                <span className="text-right font-medium tabular-nums text-foreground">
                  {item.percentage.toFixed(1)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
