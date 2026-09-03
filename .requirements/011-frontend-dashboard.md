# 011 — Frontend Dashboard

## Purpose

The MIDAS web frontend provides a professional portfolio-management interface for visualizing consolidated holdings, exposure, history, imports, and scenario analysis. It is a presentation and interaction layer — not the financial system of record.

## Stack

| Technology | Role |
|------------|------|
| React 19 | UI framework |
| TypeScript (strict) | Type safety |
| Vite | Build tool and dev server |
| pnpm | Package manager |
| Tailwind CSS v4 | Styling |
| shadcn/ui patterns | Reusable UI primitives |
| React Router | Client-side routing |
| TanStack Query | Server/backend state |
| TanStack Table | Holdings and tabular data |
| Recharts | Portfolio and exposure charts |
| Lucide | Icons |

Redux is intentionally omitted. TanStack Query owns backend state; simple UI state (search, reporting currency) lives in a small React context.

## Application layout

```text
frontend/src/
  app/           Router and providers
  components/    Shared layout, UI, charts
  features/      Route-level pages and fixtures
  api/           Typed fetch layer
  hooks/         Query hooks and UI context
  types/         Shared TypeScript types
  lib/           Utilities (formatting, cn)
  styles/        Global Tailwind theme
```

The shell includes:

- Top navigation for all primary routes
- Optional left icon rail on large screens
- Global search field
- Reporting currency selector (CAD default)
- Compact profile area
- Responsive mobile navigation

## Routes

| Route | Status |
|-------|--------|
| `/` | Dashboard implemented |
| `/accounts` | Placeholder |
| `/holdings` | Placeholder |
| `/history` | Placeholder |
| `/exposure` | Placeholder |
| `/imports` | Basic upload workflow UI |
| `/scenarios` | Placeholder |

All routes share `AppLayout`.

## Dashboard requirements

The dashboard (`Portfolio Overview`) includes:

1. KPI cards — total value, daily change, YTD return, cash/liquidity
2. Value by institution — Wealthsimple, Scotia, IB (not connected)
3. Value by account — TFSA, RRSP, LRSP, FHSA, Taxable
4. Portfolio value over time — Recharts with 1M/3M/YTD/1Y/All toggles
5. Sector exposure — donut chart with percentage legend
6. Holdings table — TanStack Table with sorting
7. Scenario analysis — actual vs hypothetical sample card
8. Recent imports — snapshot/import status list

Synthetic development data lives in `src/features/dashboard/fixtures.ts` and must not be scattered through components.

## API integration strategy

```text
PostgreSQL
    ↓
MIDAS application services
    ↓
FastAPI (/api/*)
    ↓
TanStack Query hooks
    ↓
React components
```

Configured via `VITE_API_BASE_URL` (default `http://localhost:8000`).

Prepared query hooks:

| Hook | Endpoint |
|------|----------|
| `useHealthQuery` | `GET /health` |
| `usePortfolioSummaryQuery` | `GET /api/portfolio/summary` |
| `usePortfolioExposureQuery` | `GET /api/portfolio/exposure` |
| `useHoldingsQuery` | `GET /api/portfolio/holdings` |
| `useAccountsQuery` | `GET /api/accounts` |
| `useSnapshotsQuery` | `GET /api/snapshots` |

When the API is unavailable, the dashboard shows a warning banner and falls back to fixtures. When live data is present (e.g. portfolio summary total, sector exposure), those values are merged into the UI without recomputing totals in the browser.

## Visualization responsibilities

| Data | Source |
|------|--------|
| Portfolio total (when live) | FastAPI summary |
| Sector exposure (when live) | FastAPI exposure |
| KPI cards, institutions, accounts, chart ranges, holdings rows, scenario card, imports | Fixtures (until backend provides richer payloads) |
| Historical chart series | Synthetic datasets (until snapshot API is wired to chart) |

The frontend must not independently calculate authoritative portfolio totals when FastAPI already exposes them.

## Backend vs frontend calculations

- **Backend:** holdings, exposure percentages, snapshot totals, account lists
- **Frontend:** formatting, chart rendering, layout, sorting UI, scenario presentation of pre-computed values

Counterfactual scenario calculation remains a backend concern. The dashboard scenario card is presentation-only sample data.

## Development commands

```bash
cd frontend
pnpm install
pnpm typecheck
pnpm lint
pnpm build
pnpm dev
```

## Future work

- Wire portfolio history chart to `/api/snapshots`
- Replace holdings table fixtures with `/api/portfolio/holdings`
- Implement remaining route pages
- Add filtering/grouping to holdings table
- Connect imports page to backend ingestion API
