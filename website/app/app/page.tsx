"use client";

import { useState, useRef, useEffect, useCallback, type FormEvent, type KeyboardEvent, Suspense } from "react";
import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { useSearchParams } from "next/navigation";
import { apiChat, apiStats, apiGetMaterial, apiLogEdit, getDownloadUrl, type UserStats, type Material } from "@/lib/api";
import { Container } from "@/components/ui/Container";

// ─── Types ───────────────────────────────────────────────────────────────────

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const PREPARING_DELAY_MS = 8_000;

const GENERATION_PHASES = [
  { label: "Searching grammar database…", pct: 12 },
  { label: "Loading L1 interference patterns…", pct: 28 },
  { label: "Building slide plan…", pct: 42 },
  { label: "Writing slides (this takes a few minutes)…", pct: 55 },
  { label: "Validating content quality…", pct: 75 },
  { label: "Building your presentation…", pct: 88 },
  { label: "Almost done…", pct: 95 },
];

const STARTER_PROMPTS = [
  { emoji: "📊", label: "I need slides", message: "I need slides" },
  { emoji: "📝", label: "I need a worksheet", message: "I need a worksheet" },
  { emoji: "🎮", label: "I need an activity guide", message: "I need an activity guide" },
  { emoji: "🃏", label: "I need flashcards", message: "I need flashcards" },
  { emoji: "✨", label: "I need everything", message: "I need everything" },
];

const DOWNLOAD_RE = /\/download\/([a-z0-9-]+)\/([^"'\s)]+\.(html|pptx|docx|pdf))/gi;

// ─── Helpers ─────────────────────────────────────────────────────────────────

function cleanResponse(text: string): string {
  text = text.replace(/<memory-context>[\s\S]*?<\/memory-context>/gi, "");
  text = text.replace(/\[System note:[\s\S]*?\]/gi, "");
  text = text.replace(/<memory-context>[\s\S]*/gi, "");
  text = text.replace(/\n{3,}/g, "\n\n").trim();
  return text;
}

function extractDownloadLinks(content: string): { href: string; jobId: string; filename: string; ext: string }[] {
  const matches: { href: string; jobId: string; filename: string; ext: string }[] = [];
  let m: RegExpExecArray | null;
  const re = DOWNLOAD_RE;
  while ((m = re.exec(content)) !== null) {
    matches.push({ href: m[0], jobId: m[1], filename: m[2], ext: m[3] });
  }
  return matches;
}

function getFileLabel(filename: string, ext: string): string {
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
}

const FILE_ICONS: Record<string, string> = { html: "🎬", pptx: "📊", docx: "📝", pdf: "📄" };

// ─── Components ──────────────────────────────────────────────────────────────

function ProgressCard() {
  const [phaseIdx, setPhaseIdx] = useState(0);
  const [pct, setPct] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPhaseIdx((prev) => {
        const next = Math.min(prev + 1, GENERATION_PHASES.length - 1);
        setPct(GENERATION_PHASES[next].pct);
        return next;
      });
    }, 60_000);
    const ticker = setInterval(() => {
      setPct((prev) => {
        const cap = GENERATION_PHASES[phaseIdx]?.pct ?? 95;
        return prev < cap ? prev + 1 : prev;
      });
    }, 4_000);
    setPct(GENERATION_PHASES[0].pct);
    return () => { clearInterval(interval); clearInterval(ticker); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const phase = GENERATION_PHASES[phaseIdx];

  return (
    <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 rounded-2xl px-4 py-4 rounded-bl-sm shadow-sm max-w-[80%] space-y-3">
      <p className="text-sm font-medium text-neutral-700 dark:text-neutral-300">{phase.label}</p>
      <div className="w-full bg-neutral-100 dark:bg-neutral-800 rounded-full h-2">
        <div
          className="bg-gradient-to-r from-primary-500 to-success-500 h-2 rounded-full transition-all duration-[4000ms] ease-linear"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-[11px] text-neutral-400 dark:text-neutral-500">
        Materials are crafted individually — takes 5–10 min. Safe to close this tab or lock your phone — you&apos;ll get an email when ready.
      </p>
    </div>
  );
}

function DownloadButtons({ content }: { content: string }) {
  const links = extractDownloadLinks(content);
  if (links.length === 0) return null;

  return (
    <div className="mt-4 flex flex-col gap-2 sm:flex-row sm:flex-wrap">
      {links.map(({ href, jobId, filename, ext }) => (
        <a
          key={href}
          href={getDownloadUrl(jobId, filename)}
          download={filename}
          className="inline-flex items-center justify-center gap-2 bg-primary-500 text-white text-xs font-semibold px-4 py-2.5 rounded-xl hover:bg-primary-600 transition-colors"
        >
          {FILE_ICONS[ext] ?? "📎"} {getFileLabel(filename, ext)}
        </a>
      ))}
    </div>
  );
}

function renderMarkdown(text: string): React.ReactNode[] {
  const lines = text.split("\n");
  const nodes: React.ReactNode[] = [];
  lines.forEach((line, i) => {
    if (/^[\*•-]\s/.test(line)) {
      nodes.push(
        <li key={i} className="ml-4 list-disc marker:text-primary-500">
          {renderInline(line.replace(/^[\*•-]\s/, ""))}
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
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**"))
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    if (part.startsWith("`") && part.endsWith("`"))
      return <code key={i} className="bg-neutral-100 dark:bg-neutral-800 rounded px-1 text-xs font-mono">{part.slice(1, -1)}</code>;
    return part;
  });
}

// ─── Main Page ───────────────────────────────────────────────────────────────

function ChatPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const searchParams = useSearchParams();
  const editMaterialId = searchParams.get("edit");

  const [stats, setStats] = useState<UserStats | null>(null);
  const [editMaterial, setEditMaterial] = useState<Material | null>(null);
  const [editContextInjected, setEditContextInjected] = useState(false);

  const WELCOME_MESSAGE: Message = {
    id: "welcome",
    role: "assistant" as const,
    content:
      "Hi! I'm CogniESL — your AI teaching assistant.\n\nTell me what materials you need and I'll generate them from our validated ESL database.\n\n**For example:**\n- \"Slides for present simple for Brazilian adults\"\n- \"Worksheet on articles for Spanish-speaking teens\"\n- \"Flashcards for past simple errors for Chinese speakers\"\n- \"Activity guide for third conditional for Japanese adults\"",
    timestamp: new Date(),
  };

  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [preparingVisible, setPreparingVisible] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const preparingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const userMessageCountRef = useRef(0);

  // Load stats once after auth is confirmed
  useEffect(() => {
    if (isAuthenticated) {
      apiStats().then((s) => { if (s) setStats(s); });
    }
  }, [isAuthenticated]);

  // Load the material being edited and inject context into the agent
  useEffect(() => {
    if (!editMaterialId || !isAuthenticated || editContextInjected) return;
    apiGetMaterial(editMaterialId).then((mat) => {
      if (!mat) return;
      setEditMaterial(mat);

      // Replace welcome message with edit-mode greeting
      setMessages([{
        id: "welcome",
        role: "assistant" as const,
        content: `I've loaded your material: **${mat.grammar_point}** (${mat.l1_languages}, ${mat.age_group}).\n\nWhat would you like to change? For example:\n- "Change the L1 slides to Korean"\n- "Add more practice examples"\n- "Fix slide 3 — the example is wrong"`,
        timestamp: new Date(),
      }]);

      // Silently inject context into the agent session so it knows the job
      const contextMsg =
        `<memory-context>EDIT SESSION — do NOT generate new materials from scratch. ` +
        `The teacher is editing an existing set. ` +
        `job_id=${mat.job_id} project_name=${mat.project_name} ` +
        `grammar_point=${mat.grammar_point} l1_languages=${mat.l1_languages} ` +
        `age_group=${mat.age_group} ` +
        `html_bundle_path=${mat.html_bundle_path ?? "none"} ` +
        `Use ModifySlide to change specific slides, then BuildOfflineBundle to rebuild. ` +
        `Do NOT call QueueGenerationJob.</memory-context> ` +
        `I am editing existing materials for: ${mat.grammar_point}, ${mat.l1_languages}, ${mat.age_group}. Please confirm you have loaded this context.`;

      apiChat(contextMsg).catch(() => {});
      setEditContextInjected(true);
    });
  }, [editMaterialId, isAuthenticated, editContextInjected]);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages, preparingVisible, scrollToBottom]);

  const submit = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    };
    userMessageCountRef.current += 1;
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    setIsLoading(true);
    setPreparingVisible(false);

    const pastInitialChat = userMessageCountRef.current >= 2;
    if (pastInitialChat && /yes|go ahead|looks good|start|generate|approved|ok(ay)?|sure|let'?s go|sounds good|perfect|great/i.test(trimmed)) {
      setIsGenerating(true);
    }

    preparingTimerRef.current = setTimeout(() => {
      setPreparingVisible(true);
    }, PREPARING_DELAY_MS);

    try {
      const { response } = await apiChat(trimmed);
      const cleaned = cleanResponse(response);

      if (cleaned.includes("/download/")) {
        setIsGenerating(false);
        // Log the edit if this was an edit session
        if (editMaterial) {
          apiLogEdit(editMaterial.id, "slide_change", trimmed).catch(() => {});
        }
      }

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant" as const,
          content: cleaned || "Sorry, I couldn't process that request.",
          timestamp: new Date(),
        },
      ]);
    } catch (err) {
      setIsGenerating(false);
      const errorMsg =
        err instanceof Error && err.name === "AbortError"
          ? "Generation is taking longer than expected. Please refresh the page in a few minutes — your materials will be ready to view here."
          : "Sorry, there was an error connecting to the server. Please try again.";
      setMessages((prev) => [
        ...prev,
        { id: (Date.now() + 1).toString(), role: "assistant" as const, content: errorMsg, timestamp: new Date() },
      ]);
    } finally {
      if (preparingTimerRef.current) clearTimeout(preparingTimerRef.current);
      setPreparingVisible(false);
      setIsLoading(false);
    }
  }, [isLoading]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    submit(input);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit(input);
    }
  };

  const isOnlyWelcome = messages.length === 1 && messages[0].id === "welcome" && !editMaterial;

  // Redirect to sign in if not authenticated
  if (!authLoading && !isAuthenticated) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <Container size="sm">
          <div className="text-center py-16">
            <h1 className="font-heading text-3xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Sign in to generate materials
            </h1>
            <p className="text-neutral-600 dark:text-neutral-400 mb-8">
              Create an account or sign in to start generating ESL teaching materials.
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link
                href="/app/signin"
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 shadow-glow hover:shadow-glow-lg px-6 py-3 text-base"
              >
                Sign In
              </Link>
              <Link
                href="/app/register"
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 border-2 border-primary-500 text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/20 px-6 py-3 text-base"
              >
                Create Account
              </Link>
            </div>
          </div>
        </Container>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-64px)]">
      {/* Edit mode banner */}
      {editMaterial && (
        <div className="border-b border-primary-200 dark:border-primary-800 bg-primary-50 dark:bg-primary-900/20 px-4 py-2">
          <div className="mx-auto max-w-3xl flex items-center justify-between text-xs">
            <span className="text-primary-700 dark:text-primary-300 font-medium">
              ✏️ Editing: <strong>{editMaterial.grammar_point}</strong> · {editMaterial.l1_languages} · {editMaterial.age_group}
            </span>
            <a href="/app/materials" className="text-primary-600 dark:text-primary-400 hover:underline">
              ← Back to My Materials
            </a>
          </div>
        </div>
      )}
      {/* Stats bar — only shown when user has at least one generation */}
      {!editMaterial && stats && stats.total_generations > 0 && (
        <div className="border-b border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 px-4 py-2">
          <div className="mx-auto max-w-3xl flex items-center gap-6 text-xs text-neutral-500 dark:text-neutral-400">
            <span>
              Welcome back{user?.name ? `, ${user.name.split(" ")[0]}` : ""}!
            </span>
            <span className="flex items-center gap-1">
              <span className="font-semibold text-primary-600 dark:text-primary-400">{stats.total_generations}</span>
              {stats.total_generations === 1 ? "material generated" : "materials generated"}
            </span>
            <span className="flex items-center gap-1">
              <span className="font-semibold text-primary-600 dark:text-primary-400">{stats.hours_saved}h</span>
              saved
            </span>
            {stats.languages_count > 0 && (
              <span className="flex items-center gap-1">
                <span className="font-semibold text-primary-600 dark:text-primary-400">{stats.languages_count}</span>
                {stats.languages_count === 1 ? "language" : "languages"}
              </span>
            )}
          </div>
        </div>
      )}
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-neutral-50 dark:bg-neutral-950">
        <Container size="md">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} mb-4`}>
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm ${
                  msg.role === "user"
                    ? "bg-primary-500 text-white rounded-br-sm"
                    : "bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 text-neutral-800 dark:text-neutral-200 rounded-bl-sm shadow-sm"
                }`}
              >
                <div className="space-y-0.5">{renderMarkdown(msg.content)}</div>
                {msg.role === "assistant" && <DownloadButtons content={msg.content} />}
                {msg.id === "welcome" && isOnlyWelcome && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {STARTER_PROMPTS.map((p) => (
                      <button
                        key={p.message}
                        onClick={() => submit(p.message)}
                        className="text-xs bg-primary-50 dark:bg-primary-900/20 hover:bg-primary-100 dark:hover:bg-primary-900/40 text-primary-700 dark:text-primary-300 border border-primary-200 dark:border-primary-800 rounded-full px-3 py-1.5 transition-colors text-left font-medium"
                        disabled={isLoading}
                      >
                        {p.emoji} {p.label}
                      </button>
                    ))}
                  </div>
                )}
                <span
                  className={`text-[10px] mt-1 block ${msg.role === "user" ? "text-white/60" : "text-neutral-400"}`}
                >
                  {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
            </div>
          ))}

          {(preparingVisible || isGenerating) && (
            <div className="flex justify-start mb-4">
              <ProgressCard />
            </div>
          )}

          {isLoading && !preparingVisible && !isGenerating && (
            <div className="flex justify-start mb-4">
              <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 rounded-2xl px-4 py-3 rounded-bl-sm shadow-sm">
                <div className="flex space-x-1.5">
                  <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-accent-400 rounded-full animate-bounce [animation-delay:0.1s]" />
                  <div className="w-2 h-2 bg-secondary-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </Container>
      </div>

      {/* Input */}
      <div className="border-t border-neutral-200 dark:border-neutral-800 p-4 bg-white dark:bg-neutral-900">
        <Container size="md">
          <form onSubmit={handleSubmit}>
            <div className="flex items-end space-x-3">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => {
                  setInput(e.target.value);
                  const ta = e.target;
                  ta.style.height = "auto";
                  ta.style.height = `${Math.min(ta.scrollHeight, 120)}px`;
                }}
                onKeyDown={handleKeyDown}
                placeholder="Describe what materials you need… (Enter to send, Shift+Enter for newline)"
                rows={1}
                className="flex-1 rounded-2xl border border-neutral-300 dark:border-neutral-600 px-5 py-3 text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none overflow-hidden leading-relaxed"
                disabled={isLoading}
                style={{ minHeight: "48px", maxHeight: "120px" }}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-primary-500 hover:bg-primary-600 text-white rounded-full p-3 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex-shrink-0"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                  <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                </svg>
              </button>
            </div>
            <p className="text-[10px] text-neutral-400 text-center mt-2">
              Enter to send · Shift+Enter for newline · View and present your materials right here
            </p>
          </form>
        </Container>
      </div>
    </div>
  );
}

export default function ChatPageWrapper() {
  return (
    <Suspense>
      <ChatPage />
    </Suspense>
  );
}
