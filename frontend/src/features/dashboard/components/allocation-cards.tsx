import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/input";
import { formatCurrency } from "@/lib/utils";
import type { AccountAllocation, InstitutionAllocation } from "@/types/portfolio";

function AllocationBar({ percentage }: { percentage: number }) {
  return (
    <div className="h-2 overflow-hidden rounded-full bg-muted">
      <div
        className="h-full rounded-full bg-midas-blue"
        style={{ width: `${Math.max(percentage, 0)}%` }}
      />
    </div>
  );
}

export function InstitutionAllocationCard({
  institutions,
}: {
  institutions: InstitutionAllocation[];
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Value by Institution</CardTitle>
      </CardHeader>
      <CardContent className="space-y-5">
        {institutions.map((institution) => (
          <div key={institution.name} className="space-y-2">
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <p className="truncate font-medium text-foreground">{institution.name}</p>
                {institution.connected ? (
                  <p className="text-sm tabular-nums text-muted-foreground">
                    {formatCurrency(institution.value)} · {institution.percentage.toFixed(1)}%
                  </p>
                ) : (
                  <Badge variant="outline">Not connected</Badge>
                )}
              </div>
            </div>
            <AllocationBar percentage={institution.percentage} />
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export function AccountAllocationCard({
  accounts,
}: {
  accounts: AccountAllocation[];
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Value by Account</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {accounts.map((account) => (
          <div key={account.name} className="space-y-2">
            <div className="flex items-center justify-between gap-3 text-sm">
              <span className="font-medium text-foreground">{account.name}</span>
              <span className="tabular-nums text-muted-foreground">
                {formatCurrency(account.value)} · {account.percentage.toFixed(1)}%
              </span>
            </div>
            <AllocationBar percentage={account.percentage} />
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
