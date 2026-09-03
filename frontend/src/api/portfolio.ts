import { apiFetch } from "./client";
import type { PortfolioSummary, SectorExposureResponse } from "@/types/portfolio";

export function fetchHealth() {
  return apiFetch<{ status: string }>("/health");
}

export function fetchPortfolioSummary() {
  return apiFetch<PortfolioSummary>("/api/portfolio/summary");
}

export function fetchPortfolioExposure() {
  return apiFetch<SectorExposureResponse>("/api/portfolio/exposure");
}
