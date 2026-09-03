import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAppUi } from "@/hooks/use-app-ui-context";

export function ThemeToggle() {
  const { theme, toggleTheme } = useAppUi();
  const isDark = theme === "dark";

  return (
    <Button
      type="button"
      variant="outline"
      size="icon"
      onClick={toggleTheme}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      title={isDark ? "Light mode" : "Dark mode"}
    >
      {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  );
}
