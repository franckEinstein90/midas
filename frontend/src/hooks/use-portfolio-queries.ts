import { useQuery } from "@tanstack/react-query";
import { fetchAccounts } from "@/api/accounts";
import { fetchHoldings } from "@/api/holdings";
import {
  fetchHealth,
  fetchPortfolioExposure,
  fetchPortfolioSummary,
} from "@/api/portfolio";
import { fetchSnapshots } from "@/api/snapshots";

export function useHealthQuery() {
  return useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    retry: 1,
    staleTime: 30_000,
  });
}

export function usePortfolioSummaryQuery() {
  return useQuery({
    queryKey: ["portfolio", "summary"],
    queryFn: fetchPortfolioSummary,
    retry: 1,
    staleTime: 60_000,
  });
}

export function usePortfolioExposureQuery() {
  return useQuery({
    queryKey: ["portfolio", "exposure"],
    queryFn: fetchPortfolioExposure,
    retry: 1,
    staleTime: 60_000,
  });
}

export function useHoldingsQuery() {
  return useQuery({
    queryKey: ["portfolio", "holdings"],
    queryFn: fetchHoldings,
    retry: 1,
    staleTime: 60_000,
  });
}

export function useAccountsQuery() {
  return useQuery({
    queryKey: ["accounts"],
    queryFn: fetchAccounts,
    retry: 1,
    staleTime: 60_000,
  });
}

export function useSnapshotsQuery() {
  return useQuery({
    queryKey: ["snapshots"],
    queryFn: fetchSnapshots,
    retry: 1,
    staleTime: 60_000,
  });
}
