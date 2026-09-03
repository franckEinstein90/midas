import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function PlaceholderPage({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        <p className="mt-1 max-w-2xl text-sm text-muted-foreground">{description}</p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Coming soon</CardTitle>
          <CardDescription>
            This section will connect to MIDAS backend services as the portfolio platform
            expands.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground">
          The navigation, layout, and API layer are in place. Detailed functionality for this
          route will be implemented in a follow-up iteration.
        </CardContent>
      </Card>
    </div>
  );
}
