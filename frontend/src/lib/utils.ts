import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(
  value: number,
  currency = "CAD",
  options?: { compact?: boolean },
): string {
  return new Intl.NumberFormat("en-CA", {
    style: "currency",
    currency,
    notation: options?.compact ? "compact" : "standard",
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatPercent(value: number, signed = false): string {
  const formatted = new Intl.NumberFormat("en-CA", {
    style: "percent",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value / 100);
  if (signed && value > 0) return `+${formatted}`;
  return formatted;
}

export function formatSignedCurrency(value: number, currency = "CAD"): string {
  const prefix = value > 0 ? "+" : value < 0 ? "-" : "";
  return `${prefix}${formatCurrency(Math.abs(value), currency)}`;
}
