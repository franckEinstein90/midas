import type { DashboardData } from "@/types/portfolio";

export const dashboardFixtures: DashboardData = {
  kpis: {
    totalValue: {
      label: "Total Portfolio Value",
      value: "$1,246,753.62",
      subValue: "+1.32% today",
      trend: [1180000, 1195000, 1210000, 1228000, 1235000, 1246753],
      positive: true,
    },
    dailyChange: {
      label: "Daily Change",
      value: "+$16,187.54",
      subValue: "+1.32%",
      positive: true,
    },
    ytdReturn: {
      label: "YTD Return",
      value: "+$112,352.48",
      subValue: "+9.92%",
      positive: true,
    },
    cashLiquidity: {
      label: "Cash / Available Liquidity",
      value: "$78,642.11",
      subValue: "6.31% of portfolio",
    },
  },
  institutions: [
    { name: "Wealthsimple", value: 612430.18, percentage: 49.1, connected: true },
    { name: "Scotia / ScotiaMcLeod", value: 555681.33, percentage: 44.6, connected: true },
    { name: "Interactive Brokers", value: 0, percentage: 0, connected: false },
  ],
  accounts: [
    { name: "TFSA", value: 342118.44, percentage: 27.4 },
    { name: "RRSP", value: 398220.17, percentage: 31.9 },
    { name: "LRSP", value: 214512.8, percentage: 17.2 },
    { name: "FHSA", value: 87240.1, percentage: 7.0 },
    { name: "Taxable", value: 204662.11, percentage: 16.4 },
  ],
  portfolioHistory: {
    "1M": [
      { date: "Apr 1", value: 1210000 },
      { date: "Apr 8", value: 1218500 },
      { date: "Apr 15", value: 1223000 },
      { date: "Apr 22", value: 1231500 },
      { date: "Apr 29", value: 1239800 },
      { date: "May 6", value: 1242100 },
      { date: "May 13", value: 1246753 },
    ],
    "3M": [
      { date: "Feb 15", value: 1162000 },
      { date: "Mar 1", value: 1178000 },
      { date: "Mar 15", value: 1194000 },
      { date: "Apr 1", value: 1210000 },
      { date: "Apr 15", value: 1223000 },
      { date: "May 1", value: 1237000 },
      { date: "May 16", value: 1246753 },
    ],
    YTD: [
      { date: "Jan", value: 1134400 },
      { date: "Feb", value: 1162000 },
      { date: "Mar", value: 1194000 },
      { date: "Apr", value: 1223000 },
      { date: "May", value: 1246753 },
    ],
    "1Y": [
      { date: "Jun", value: 1080000 },
      { date: "Aug", value: 1110000 },
      { date: "Oct", value: 1155000 },
      { date: "Dec", value: 1185000 },
      { date: "Feb", value: 1215000 },
      { date: "May", value: 1246753 },
    ],
    All: [
      { date: "2022", value: 820000 },
      { date: "2023", value: 980000 },
      { date: "2024", value: 1134400 },
      { date: "2025", value: 1246753 },
    ],
  },
  sectorExposure: [
    { name: "Financials", market_value: 312000, percentage: 25.0 },
    { name: "Energy", market_value: 187000, percentage: 15.0 },
    { name: "Technology", market_value: 249000, percentage: 20.0 },
    { name: "Healthcare", market_value: 125000, percentage: 10.0 },
    { name: "Industrials", market_value: 150000, percentage: 12.0 },
    { name: "Materials", market_value: 100000, percentage: 8.0 },
    { name: "Consumer Staples", market_value: 75000, percentage: 6.0 },
    { name: "Utilities", market_value: 48753, percentage: 4.0 },
  ],
  holdings: [
    {
      symbol: "AAPL",
      account: "TFSA",
      quantity: 120,
      value: 32400,
      sector: "Technology",
      currency: "USD",
      tags: ["Core", "Large Cap"],
    },
    {
      symbol: "RY",
      account: "RRSP",
      quantity: 450,
      value: 67500,
      sector: "Financials",
      currency: "CAD",
      tags: ["Dividend", "Core"],
    },
    {
      symbol: "XIC",
      account: "TFSA",
      quantity: 820,
      value: 28700,
      sector: "ETF",
      currency: "CAD",
      tags: ["ETF", "Core"],
    },
    {
      symbol: "MSFT",
      account: "Taxable",
      quantity: 85,
      value: 41200,
      sector: "Technology",
      currency: "USD",
      tags: ["Large Cap"],
    },
    {
      symbol: "ENB",
      account: "LRSP",
      quantity: 600,
      value: 35400,
      sector: "Energy",
      currency: "CAD",
      tags: ["Dividend"],
    },
  ],
  scenario: {
    title: "What if I had not sold NVIDIA on March 10, 2025?",
    actual: 1246753.62,
    hypothetical: 1307812.0,
  },
  recentImports: [
    { source: "Wealthsimple", timestamp: "May 16, 4:15 PM", status: "Success" },
    { source: "ScotiaMcLeod", timestamp: "May 16, 3:52 PM", status: "Success" },
    { source: "Manual Upload", timestamp: "May 15, 9:14 PM", status: "Success" },
  ],
};

export const importSources = [
  "Wealthsimple",
  "Scotia / ScotiaMcLeod",
  "Manual / Generic CSV",
] as const;

export const futureImportSources = ["Interactive Brokers"] as const;
