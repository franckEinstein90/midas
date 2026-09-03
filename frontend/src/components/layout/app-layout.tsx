import { NavLink, Outlet } from "react-router-dom";
import {
  BarChart3,
  BriefcaseBusiness,
  ChevronLeft,
  ChevronRight,
  Clock3,
  GitCompare,
  LayoutDashboard,
  MessageSquare,
  PieChart,
  Search,
  Upload,
  UserRound,
  Wallet,
} from "lucide-react";
import { AgentChatTray } from "@/components/layout/agent-chat-tray";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Input, Select } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useAppUi } from "@/hooks/use-app-ui-context";

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/accounts", label: "Accounts", icon: Wallet },
  { to: "/holdings", label: "Holdings", icon: BriefcaseBusiness },
  { to: "/history", label: "History", icon: Clock3 },
  { to: "/exposure", label: "Exposure", icon: PieChart },
  { to: "/imports", label: "Imports", icon: Upload },
  { to: "/scenarios", label: "Scenarios", icon: GitCompare },
] as const;

export function AppLayout() {
  const {
    reportingCurrency,
    setReportingCurrency,
    searchQuery,
    setSearchQuery,
    railCollapsed,
    toggleRail,
    toggleChat,
  } = useAppUi();

  return (
    <div className="min-h-screen bg-background pb-24">
      <header className="sticky top-0 z-40 border-b border-border bg-background/90 backdrop-blur">
        <div className="mx-auto flex max-w-[1600px] items-center gap-4 px-4 py-3 lg:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-midas-blue text-sm font-bold text-white">
              M
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold tracking-tight text-foreground">
                MIDAS
              </p>
              <p className="hidden text-xs text-muted-foreground sm:block">
                Portfolio Intelligence
              </p>
            </div>
          </div>

          <nav className="hidden flex-1 items-center gap-1 xl:flex">
            {navItems.map(({ to, label, icon: Icon, ...rest }) => (
              <NavLink
                key={to}
                to={to}
                end={"end" in rest ? rest.end : false}
                className={({ isActive }) =>
                  cn(
                    "inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground",
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="ml-auto flex items-center gap-2 sm:gap-3">
            <div className="relative hidden md:block">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
                placeholder="Search holdings, accounts, tags..."
                className="w-56 pl-9 lg:w-72"
              />
            </div>

            <Select
              aria-label="Reporting currency"
              value={reportingCurrency}
              onChange={(event) =>
                setReportingCurrency(event.target.value as "CAD" | "USD")
              }
              className="w-[88px]"
            >
              <option value="CAD">CAD</option>
              <option value="USD">USD</option>
            </Select>

            <ThemeToggle />

            <Button
              type="button"
              variant="outline"
              size="icon"
              className="hidden sm:inline-flex"
              onClick={toggleChat}
              aria-label="Open agent chat"
            >
              <MessageSquare className="h-4 w-4" />
            </Button>

            <button
              type="button"
              className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-border bg-card text-muted-foreground hover:bg-muted"
              aria-label="Profile"
            >
              <UserRound className="h-4 w-4" />
            </button>
          </div>
        </div>

        <div className="border-t border-border xl:hidden">
          <nav className="mx-auto flex max-w-[1600px] gap-1 overflow-x-auto px-4 py-2">
            {navItems.map(({ to, label, icon: Icon, ...rest }) => (
              <NavLink
                key={to}
                to={to}
                end={"end" in rest ? rest.end : false}
                className={({ isActive }) =>
                  cn(
                    "inline-flex shrink-0 items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium",
                    isActive
                      ? "bg-accent text-accent-foreground"
                      : "text-muted-foreground hover:bg-muted",
                  )
                }
              >
                <Icon className="h-3.5 w-3.5" />
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <div className="mx-auto flex max-w-[1600px] gap-4 px-4 py-6 lg:gap-6 lg:px-6">
        <aside
          className={cn(
            "hidden shrink-0 transition-[width] duration-200 ease-out lg:block",
            railCollapsed ? "w-12" : "w-52",
          )}
        >
          <div className="sticky top-24 flex flex-col gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={toggleRail}
              className={cn(
                "justify-center gap-2 border-border bg-card text-muted-foreground hover:text-foreground",
                railCollapsed ? "h-10 w-10 px-0" : "w-full",
              )}
              aria-label={railCollapsed ? "Expand navigation" : "Collapse navigation"}
              title={railCollapsed ? "Expand" : "Collapse"}
            >
              {railCollapsed ? (
                <ChevronRight className="h-4 w-4" />
              ) : (
                <>
                  <ChevronLeft className="h-4 w-4" />
                  <span>Collapse</span>
                </>
              )}
            </Button>

            <div className="space-y-1.5 rounded-xl border border-border bg-card/70 p-1.5 shadow-xs">
              {navItems.map(({ to, label, icon: Icon, ...rest }) => (
                <NavLink
                  key={`rail-${to}`}
                  to={to}
                  end={"end" in rest ? rest.end : false}
                  title={label}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center rounded-lg border transition-colors",
                      railCollapsed
                        ? "h-10 w-10 justify-center"
                        : "h-10 gap-2.5 px-3",
                      isActive
                        ? "border-midas-blue/20 bg-midas-blue-soft text-midas-blue"
                        : "border-transparent text-muted-foreground hover:border-border hover:bg-muted hover:text-foreground",
                    )
                  }
                >
                  <Icon className="h-4 w-4 shrink-0" />
                  {!railCollapsed && (
                    <span className="truncate text-sm font-medium">{label}</span>
                  )}
                </NavLink>
              ))}

              <div
                className={cn(
                  "flex items-center rounded-lg text-muted-foreground",
                  railCollapsed ? "h-10 w-10 justify-center" : "h-10 gap-2.5 px-3",
                )}
                title="Analytics"
              >
                <BarChart3 className="h-4 w-4 shrink-0" />
                {!railCollapsed && (
                  <span className="truncate text-sm font-medium">Analytics</span>
                )}
              </div>
            </div>

            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={toggleChat}
              className={cn(
                "justify-center gap-2",
                railCollapsed ? "h-10 w-10 px-0" : "w-full",
              )}
              aria-label="Open agent chat"
              title="Ask MIDAS"
            >
              <MessageSquare className="h-4 w-4" />
              {!railCollapsed && <span>Ask MIDAS</span>}
            </Button>
          </div>
        </aside>

        <main className="min-w-0 flex-1">
          <Outlet />
        </main>
      </div>

      <AgentChatTray />
    </div>
  );
}
