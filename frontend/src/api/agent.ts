import { ApiError, apiFetch } from "@/api/client";
import type { ReportingCurrency } from "@/types/portfolio";

export type AgentChatRole = "user" | "assistant" | "system";

export interface AgentChatMessage {
  role: AgentChatRole;
  content: string;
}

interface AgentChatResponse {
  reply: string;
}

export async function sendAgentMessage(
  messages: AgentChatMessage[],
  reportingCurrency: ReportingCurrency,
): Promise<string> {
  try {
    const data = await apiFetch<AgentChatResponse>("/api/agent/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: messages.map(({ role, content }) => ({ role, content })),
        reporting_currency: reportingCurrency,
      }),
    });
    return data.reply;
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      throw new Error("Agent chat endpoint is not available on the API.");
    }
    throw error;
  }
}
