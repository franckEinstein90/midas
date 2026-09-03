# MIDAS Frontend

React + TypeScript portfolio dashboard for MIDAS.

## Stack

React, Vite, TypeScript, pnpm, Tailwind CSS, shadcn/ui patterns, React Router, TanStack Query, TanStack Table, Recharts, Lucide.

## Setup

```powershell
cd frontend
pnpm install
copy .env.example .env
```

## Commands

```powershell
pnpm dev          # http://localhost:5173
pnpm typecheck
pnpm lint
pnpm build
pnpm preview
```

## API

Set `VITE_API_BASE_URL` in `.env` (default `http://localhost:8000`).

The Vite dev server proxies `/api` and `/health` to the backend when running locally.

## Routes

- `/` — Dashboard (implemented)
- `/accounts`, `/holdings`, `/history`, `/exposure`, `/scenarios` — placeholders
- `/imports` — upload workflow UI

Synthetic dashboard data lives in `src/features/dashboard/fixtures.ts`.
