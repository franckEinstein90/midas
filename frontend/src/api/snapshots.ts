import { apiFetch } from "./client";
import type { SnapshotPoint } from "@/types/portfolio";

export function fetchSnapshots() {
  return apiFetch<SnapshotPoint[]>("/api/snapshots");
}
