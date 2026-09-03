import { useEffect, useRef, useState } from "react";
import { Bot, ChevronDown, Loader2, SendHorizontal, Sparkles, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { sendAgentMessage, type AgentChatMessage } from "@/api/agent";
import { useAppUi } from "@/hooks/use-app-ui-context";

const STARTER = {
  role: "assistant" as const,
  content:
    "I'm the MIDAS portfolio agent. Ask about holdings, exposure, accounts, or recent portfolio value.",
};

export function AgentChatTray() {
  const { chatOpen, setChatOpen, toggleChat, reportingCurrency } = useAppUi();
  const [messages, setMessages] = useState<AgentChatMessage[]>([STARTER]);
  const [draft, setDraft] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (chatOpen) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
      inputRef.current?.focus();
    }
  }, [chatOpen, messages, pending]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const text = draft.trim();
    if (!text || pending) return;

    const nextMessages: AgentChatMessage[] = [
      ...messages,
      { role: "user", content: text },
    ];
    setMessages(nextMessages);
    setDraft("");
    setPending(true);
    setError(null);

    try {
      const reply = await sendAgentMessage(nextMessages, reportingCurrency);
      setMessages((current) => [...current, { role: "assistant", content: reply }]);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Could not reach the portfolio agent.";
      setError(message);
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "I couldn't complete that request. Check that the API is running, then try again.",
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  return (
    <>
      {!chatOpen && (
        <button
          type="button"
          onClick={toggleChat}
          className="fixed bottom-5 right-5 z-50 inline-flex items-center gap-2 rounded-full border border-midas-blue/20 bg-midas-blue px-4 py-2.5 text-sm font-medium text-white shadow-lg transition hover:bg-midas-blue/90"
        >
          <Sparkles className="h-4 w-4" />
          Ask MIDAS
        </button>
      )}

      <div
        className={cn(
          "fixed inset-x-0 bottom-0 z-50 flex justify-center px-3 pb-3 transition-transform duration-300 ease-out sm:px-6",
          chatOpen ? "translate-y-0" : "pointer-events-none translate-y-[110%]",
        )}
        aria-hidden={!chatOpen}
      >
        <section
          className="flex h-[min(52vh,420px)] w-full max-w-3xl flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-2xl"
          role="dialog"
          aria-label="MIDAS agent chat"
        >
          <header className="flex items-center gap-3 border-b border-border px-4 py-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-midas-blue-soft text-midas-blue">
              <Bot className="h-4 w-4" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold text-foreground">Portfolio agent</p>
              <p className="truncate text-xs text-muted-foreground">
                Ask about holdings, exposure, and portfolio history
              </p>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => setChatOpen(false)}
              aria-label="Minimize chat"
            >
              <ChevronDown className="h-4 w-4" />
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => setChatOpen(false)}
              aria-label="Close chat"
            >
              <X className="h-4 w-4" />
            </Button>
          </header>

          <div className="flex-1 space-y-3 overflow-y-auto bg-muted/40 px-4 py-4">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={cn(
                  "flex",
                  message.role === "user" ? "justify-end" : "justify-start",
                )}
              >
                <div
                  className={cn(
                    "max-w-[85%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed",
                    message.role === "user"
                      ? "bg-midas-blue text-white"
                      : "border border-border bg-card text-foreground",
                  )}
                >
                  {message.content}
                </div>
              </div>
            ))}
            {pending && (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                Thinking…
              </div>
            )}
            {error && <p className="text-xs text-destructive">{error}</p>}
            <div ref={bottomRef} />
          </div>

          <form
            onSubmit={handleSubmit}
            className="flex items-end gap-2 border-t border-border bg-card p-3"
          >
            <textarea
              ref={inputRef}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  void handleSubmit(event);
                }
              }}
              rows={1}
              placeholder="Ask about your portfolio…"
              className="max-h-28 min-h-10 flex-1 resize-none rounded-xl border border-input bg-background px-3 py-2.5 text-sm shadow-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              disabled={pending}
            />
            <Button
              type="submit"
              size="icon"
              disabled={pending || !draft.trim()}
              aria-label="Send message"
              className="h-10 w-10 shrink-0 rounded-xl"
            >
              {pending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <SendHorizontal className="h-4 w-4" />
              )}
            </Button>
          </form>
        </section>
      </div>
    </>
  );
}
