import { apiFetch } from "./client";
import type { HoldingRow } from "@/types/portfolio";

export function fetchHoldings() {
  return apiFetch<HoldingRow[]>("/api/portfolio/holdings");
}
