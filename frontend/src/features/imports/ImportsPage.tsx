import { UploadCloud } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import {
  dashboardFixtures,
  futureImportSources,
  importSources,
} from "@/features/dashboard/fixtures";

export function ImportsPage() {
  const [selectedSource, setSelectedSource] = useState<string>(importSources[0]);
  const [dragActive, setDragActive] = useState(false);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Imports</h1>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          Upload brokerage exports, review detected sources, and publish validated portfolio
          snapshots into MIDAS.
        </p>
      </div>

      <div className="grid gap-4 xl:grid-cols-[2fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Upload Portfolio Data</CardTitle>
            <CardDescription>
              Drag and drop a CSV or spreadsheet export. Files are not uploaded during
              development — this workflow demonstrates the intended ingestion path.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div
              className={`rounded-xl border border-dashed px-6 py-10 text-center transition-colors ${
                dragActive
                  ? "border-midas-blue bg-midas-blue-soft/40"
                  : "border-border bg-muted/20"
              }`}
              onDragEnter={(event) => {
                event.preventDefault();
                setDragActive(true);
              }}
              onDragOver={(event) => {
                event.preventDefault();
                setDragActive(true);
              }}
              onDragLeave={() => setDragActive(false)}
              onDrop={(event) => {
                event.preventDefault();
                setDragActive(false);
              }}
            >
              <UploadCloud className="mx-auto h-10 w-10 text-midas-blue" />
              <p className="mt-4 text-sm font-medium text-foreground">
                Drag and drop your export file here
              </p>
              <p className="mt-1 text-sm text-muted-foreground">
                Supported formats: CSV, XLSX
              </p>
              <Button className="mt-4" variant="outline" type="button">
                Choose File
              </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label htmlFor="source" className="text-sm font-medium text-foreground">
                  Source / Institution
                </label>
                <Select
                  id="source"
                  value={selectedSource}
                  onChange={(event) => setSelectedSource(event.target.value)}
                >
                  {importSources.map((source) => (
                    <option key={source} value={source}>
                      {source}
                    </option>
                  ))}
                </Select>
              </div>
              <div className="space-y-2">
                <label htmlFor="detection" className="text-sm font-medium text-foreground">
                  Automatic Detection
                </label>
                <Input
                  id="detection"
                  readOnly
                  value={`Detected source: ${selectedSource}`}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Future Sources</CardTitle>
            <CardDescription>Planned institution adapters</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            {futureImportSources.map((source) => (
              <div
                key={source}
                className="rounded-lg border border-border px-3 py-2 text-foreground"
              >
                {source}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Imports</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {dashboardFixtures.recentImports.map((item) => (
            <div
              key={`${item.source}-${item.timestamp}`}
              className="flex items-center justify-between rounded-lg border border-border px-4 py-3"
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
    </div>
  );
}
