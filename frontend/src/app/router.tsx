import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "@/components/layout/app-layout";
import { PlaceholderPage } from "@/components/layout/placeholder-page";
import { DashboardPage } from "@/features/dashboard/DashboardPage";
import { ImportsPage } from "@/features/imports/ImportsPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      {
        path: "accounts",
        element: (
          <PlaceholderPage
            title="Accounts"
            description="Review institutions, account types, and balances across your portfolio."
          />
        ),
      },
      {
        path: "holdings",
        element: (
          <PlaceholderPage
            title="Holdings"
            description="Inspect positions by account, instrument, and valuation date."
          />
        ),
      },
      {
        path: "history",
        element: (
          <PlaceholderPage
            title="History"
            description="Explore dated portfolio snapshots and value changes over time."
          />
        ),
      },
      {
        path: "exposure",
        element: (
          <PlaceholderPage
            title="Exposure"
            description="Analyze sector, geography, currency, and tag-based allocation."
          />
        ),
      },
      { path: "imports", element: <ImportsPage /> },
      {
        path: "scenarios",
        element: (
          <PlaceholderPage
            title="Scenarios"
            description="Compare actual portfolio history with counterfactual investment decisions."
          />
        ),
      },
    ],
  },
]);
