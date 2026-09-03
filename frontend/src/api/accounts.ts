import { apiFetch } from "./client";
import type { AccountSummary } from "@/types/portfolio";

export function fetchAccounts() {
  return apiFetch<AccountSummary[]>("/api/accounts");
}
