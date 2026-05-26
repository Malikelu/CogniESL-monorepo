"use client";

import { useState, useRef, useEffect, useCallback } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

// After this many ms with no server response, show the progress indicator.
// Quick chat turns resolve in <10s. Generation takes 5–10 min.
const PREPARING_DELAY_MS = 8_000;

// Keywords that indicate the teacher has approved and generation should begin.
// When detected, we lock in the progress card until download links arrive.
const APPROVAL_RE = /\b(yes|go ahead|looks good|start|generate|approved|go|ok|okay|sure|let'?s go|sounds good|perfect|great|go for it|make it|create it|build it|proceed|do it)\b/i;

// Progress phases shown during generation
const PROGRESS_PHASES = [
  { label: "Searching grammar database…", pct: 12 },
  { label: "Loading L1 interference patterns…", pct: 28 },
  { label: "Building slide plan…", pct: 42 },
  { label: "Writing slides (this takes a few minutes)…", pct: 55 },
  { label: "Validating content quality…", pct: 75 },
  { label: "Building your presentation…", pct: 88 },
  { label: "Almost done…", pct: 95 },
];

// Quick-start prompts shown below the welcome message
const STARTER_PROMPTS = [
  "📊 I need slides",
  "📝 I need a worksheet",
  "🎮 I need an activity guide",
  "🃏 I need flashcards",
  "✨ I need everything",
];

// Download-link pattern: /download/{job_id}/{filename}
const DOWNLOAD_RE = /\/download\/([a-z0-9-]+)\/([^\s"')]+\.(pptx|docx|pdf))/gi;

function getOrCreateSessionId(): string {
  if (typeof window === "undefined") return "server";
  let id = localStorage.getItem("cogniesl_session_id");
  if (!id) {
    id = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
    localStorage.setItem("cogniesl_session_id", id);
  }
  return id;
}

function cleanResponse(text: string): string {
  text = text.replace(/<memory-context>[\s\S]*?<\/memory-context>/gi, "");
  text = text.replace(/\[System note:[\s\S]*?\]/gi, "");
  text = text.replace(/<memory-context>[\s\S]*/gi, "");
  text = text.replace(/\n{3,}/g, "\n\n").trim();
  return text;
}

/** Minimal markdown renderer: bold, bullets, code spans. Safe — no HTML injection. */
function renderMarkdown(text: string): React.ReactNode[] {
  const lines = text.split("\n");
  const nodes: React.ReactNode[] = [];

  lines.forEach((line, i) => {
    // Bullet line
    if (/^[\*\-•]\s/.test(line)) {
      nodes.push(
        <li key={i} className="ml-4 list-disc">
          {renderInline(line.slice(2))}
        </li>
      );
    } else if (line === "") {
      nodes.push(<br key={i} />);
    } else {
      nodes.push(<p key={i} className="leading-relaxed">{renderInline(line)}</p>);
    }
  });
  return nodes;
}

function renderInline(text: string): React.ReactNode {
  // Bold **text** and `code`
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**"))
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    if (part.startsWith("`") && part.endsWith("`"))
      return <code key={i} className="bg-gray-100 rounded px-1 text-xs font-mono">{part.slice(1, -1)}</code>;
    return part;
  });
}

/** Extract download links from assistant message and render as buttons. */
function DownloadButtons({ content }: { content: string }) {
  const matches: { href: string; filename: string; ext: string }[] = [];
  let m: RegExpExecArray | null;
  const re = /\/download\/([a-z0-9-]+)\/([^\s"')]+\.(html|pptx|docx|pdf))/gi;
  while ((m = re.exec(content)) !== null) {
    matches.push({ href: m[0], filename: m[2], ext: m[3] });
  }
  if (matches.length === 0) return null;

  const icon: Record<string, string> = { html: "🎬", pptx: "📊", docx: "📝", pdf: "📄" };
  const label = (filename: string, ext: string): string => {
    if (ext === "html") return "Presentation (.html — full animations)";
    if (ext === "pptx") return "Slides (.pptx)";
    if (ext === "docx") return filename.includes("activity") ? "Activity Guide (.docx)" : "Worksheet (.docx)";
    if (ext === "pdf") {
      if (filename.includes("flashcard")) return "Flashcards (.pdf)";
      if (filename.includes("progress-tracker")) return "Progress Tracker (.pdf)";
      if (filename.includes("activity")) return "Activity Guide (.pdf)";
      return "Worksheet (.pdf)";
    }
    return filename;
  };

  return (
    <div className="mt-3 flex flex-col gap-1.5 sm:flex-row sm:flex-wrap">
      {matches.map(({ href, filename, ext }) => (
        <a
          key={href}
          href={href}
          download={filename}
          className="inline-flex items-center justify-center gap-1.5 bg-teal text-white text-xs font-semibold px-3 py-2 rounded-lg hover:bg-teal-dark transition-colors sm:justify-start"
        >
          {icon[ext] ?? "📎"} {label(filename, ext)}
        </a>
      ))}
    </div>
  );
}

/** Animated progress card shown during generation. */
function ProgressCard() {
  const [phaseIdx, setPhaseIdx] = useState(0);
  const [pct, setPct] = useState(0);

  useEffect(() => {
    // Advance through phases roughly every 60s
    const interval = setInterval(() => {
      setPhaseIdx((prev) => {
        const next = Math.min(prev + 1, PROGRESS_PHASES.length - 1);
        setPct(PROGRESS_PHASES[next].pct);
        return next;
      });
    }, 60_000);

    // Smooth the bar forward 1% every 4s within the current phase range
    const ticker = setInterval(() => {
      setPct((prev) => {
        const cap = PROGRESS_PHASES[phaseIdx]?.pct ?? 95;
        return prev < cap ? prev + 1 : prev;
      });
    }, 4_000);

    // Kick off initial value
    setPct(PROGRESS_PHASES[0].pct);

    return () => {
      clearInterval(interval);
      clearInterval(ticker);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const phase = PROGRESS_PHASES[phaseIdx];

  return (
    <div className="bg-white border border-gray-200 rounded-2xl px-4 py-4 rounded-bl-sm shadow-sm max-w-[80%] space-y-3">
      <p className="text-sm font-medium text-gray-700">{phase.label}</p>
      <div className="w-full bg-gray-100 rounded-full h-2">
        <div
          className="bg-teal h-2 rounded-full transition-all duration-[4000ms] ease-linear"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-[11px] text-gray-400">
        Materials are crafted individually — takes 5–10 min. Safe to close this tab or lock your phone — you&apos;ll get an email when ready.
      </p>
    </div>
  );
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hi! I'm CogniESL — your AI teaching assistant. Tell me what materials you need and I'll generate them from our validated ESL database.\n\nFor example:\n- \"Slides for present simple for Brazilian adults\"\n- \"Worksheet on articles for Spanish-speaking teens\"\n- \"Flashcards for past simple errors for Chinese speakers\"\n- \"Activity guide for third conditional for Japanese adults\"",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [preparingVisible, setPreparingVisible] = useState(false);
  // Stays true from approval → until download links land, even across multiple turns.
  const [isGenerating, setIsGenerating] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const preparingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const preparingShownRef = useRef(false);
  // Track user message count via ref so submit() always reads the live value
  // even though it's only recreated when isLoading changes (stale closure guard).
  const userMessageCountRef = useRef(0);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => { scrollToBottom(); }, [messages, preparingVisible]);

  // Auto-expand textarea
  const resizeTextarea = useCallback(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 120)}px`;
  }, []);

  const submit = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    };

    // Increment before setMessages so the count is live inside this call
    userMessageCountRef.current += 1;

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    setIsLoading(true);
    setPreparingVisible(false);
    preparingShownRef.current = false;

    // If this looks like a generation approval (past the initial Q&A), lock in the
    // progress card — it will stay until download links appear in a response.
    // Use the ref counter (not stale messages array) to get the true message count.
    const pastInitialChat = userMessageCountRef.current >= 2;
    if (pastInitialChat && APPROVAL_RE.test(trimmed)) {
      setIsGenerating(true);
    }

    preparingTimerRef.current = setTimeout(() => {
      if (!preparingShownRef.current) {
        preparingShownRef.current = true;
        setPreparingVisible(true);
      }
    }, PREPARING_DELAY_MS);

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 1_800_000); // 30 min

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "/cogniesl/get_response";
      const authToken = typeof window !== "undefined" ? localStorage.getItem("cogniesl_token") : null;
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Session-ID": getOrCreateSessionId(),
          ...(authToken ? { "Authorization": `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify({ message: trimmed }),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!response.ok) throw new Error(`Server responded with ${response.status}`);

      const data = await response.json();
      const cleaned = cleanResponse(data.response || "");

      // If the response contains download links, materials are ready — stop the generating state.
      if (cleaned.includes("/download/")) {
        setIsGenerating(false);
      }

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: cleaned || "Sorry, I couldn't process that request.",
          timestamp: new Date(),
        },
      ]);
    } catch (err) {
      setIsGenerating(false);
      const errorMsg =
        err instanceof Error && err.name === "AbortError"
          ? "Generation is taking longer than expected. Your download link will arrive by email when ready."
          : "Sorry, there was an error connecting to the server. Please try again.";

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: errorMsg,
          timestamp: new Date(),
        },
      ]);
    } finally {
      if (preparingTimerRef.current) {
        clearTimeout(preparingTimerRef.current);
        preparingTimerRef.current = null;
      }
      preparingShownRef.current = true;
      setPreparingVisible(false);
      setIsLoading(false);
    }
  }, [isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submit(input);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit(input);
    }
  };

  const isOnlyWelcome = messages.length === 1 && messages[0].id === "welcome";

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
                msg.role === "user"
                  ? "bg-teal text-white rounded-br-sm"
                  : "bg-white border border-gray-200 text-gray-800 rounded-bl-sm shadow-sm"
              }`}
            >
              <div className="space-y-0.5">
                {renderMarkdown(msg.content)}
              </div>
              {msg.role === "assistant" && <DownloadButtons content={msg.content} />}
              {/* Quick-start chips — only under the welcome message */}
              {msg.id === "welcome" && isOnlyWelcome && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {STARTER_PROMPTS.map((p) => (
                    <button
                      key={p}
                      onClick={() => submit(p)}
                      className="text-xs bg-teal/10 hover:bg-teal/20 text-teal border border-teal/30 rounded-full px-3 py-1.5 transition-colors text-left"
                      disabled={isLoading}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              )}
              <span
                suppressHydrationWarning
                className={`text-[10px] mt-1 block ${
                  msg.role === "user" ? "text-white/60" : "text-gray-400"
                }`}
              >
                {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </span>
            </div>
          </div>
        ))}

        {/* Progress card — shown during generation (either after 8s loading delay, or if
            user sent an approval and we're waiting for materials across multiple turns) */}
        {(preparingVisible || isGenerating) && (
          <div className="flex justify-start">
            <ProgressCard />
          </div>
        )}

        {/* Typing dots — shown during short waits (normal conversation) */}
        {isLoading && !preparingVisible && !isGenerating && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 rounded-bl-sm shadow-sm">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-teal rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-coral rounded-full animate-bounce [animation-delay:0.1s]" />
                <div className="w-2 h-2 bg-gold rounded-full animate-bounce [animation-delay:0.2s]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4 bg-white">
        <div className="flex items-end space-x-3 max-w-4xl mx-auto">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => { setInput(e.target.value); resizeTextarea(); }}
            onKeyDown={handleKeyDown}
            placeholder="Describe what materials you need… (Enter to send, Shift+Enter for newline)"
            rows={1}
            className="flex-1 rounded-2xl border border-gray-300 px-5 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent resize-none overflow-hidden leading-relaxed"
            disabled={isLoading}
            style={{ minHeight: "48px", maxHeight: "120px" }}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-teal hover:bg-teal-dark text-white rounded-full p-3 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex-shrink-0"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
              <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
            </svg>
          </button>
        </div>
        <p className="text-[10px] text-gray-400 text-center mt-2">
          Enter to send · Shift+Enter for newline · Materials delivered to your email
        </p>
      </form>
    </div>
  );
}
