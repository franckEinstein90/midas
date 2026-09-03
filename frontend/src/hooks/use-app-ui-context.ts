import { useContext } from "react";
import { AppUiContext } from "@/hooks/app-ui-context";

export function useAppUi() {
  const context = useContext(AppUiContext);
  if (!context) {
    throw new Error("useAppUi must be used within AppUiProvider");
  }
  return context;
}
