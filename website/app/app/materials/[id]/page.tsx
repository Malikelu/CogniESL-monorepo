"use client";

import { useState, useEffect, useRef, useCallback, type FormEvent, type KeyboardEvent } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import {
  apiGetMaterial,
  apiGetMaterialSlides,
  apiChat,
  apiLogEdit,
  type Material,
  type Slide,
} from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

function renderMarkdown(text: string): React.ReactNode[] {
  const lines = text.split("\n");
  const nodes: React.ReactNode[] = [];
  lines.forEach((line, i) => {
    if (/^[\*•-]\s/.test(line)) {
      nodes.push(
        <li key={i} className="ml-4 list-disc marker:text-primary-500 text-sm">
          {line.replace(/^[\*•-]\s/, "")}
        </li>
      );
    } else if (line === "") {
      nodes.push(<br key={i} />);
    } else {
      const parts = line.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
      const rendered = parts.map((part, j) => {
        if (part.startsWith("**") && part.endsWith("**"))
          return <strong key={j}>{part.slice(2, -2)}</strong>;
        if (part.startsWith("`") && part.endsWith("`"))
          return (
            <code key={j} className="bg-neutral-100 dark:bg-neutral-800 rounded px-1 text-xs font-mono">
              {part.slice(1, -1)}
            </code>
          );
        return part;
      });
      nodes.push(
        <p key={i} className="leading-relaxed text-sm">
          {rendered}
        </p>
      );
    }
  });
  return nodes;
}

function cleanResponse(text: string): string {
  text = text.replace(/<memory-context>[\s\S]*?<\/memory-context>/gi, "");
  text = text.replace(/\[System note:[\s\S]*?\]/gi, "");
  text = text.replace(/<memory-context>[\s\S]*/gi, "");
  text = text.replace(/\n{3,}/g, "\n\n").trim();
  return text;
}

export default function MaterialDetailPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const materialId = params.id as string;

  const [material, setMaterial] = useState<Material | null>(null);
  const [slides, setSlides] = useState<Slide[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedSlide, setSelectedSlide] = useState<number | null>(null);
  const [messages, setMessages] = useState<Record<number, Message[]>>({});
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [contextInjected, setContextInjected] = useState(false);
  const [slideLoadErrors, setSlideLoadErrors] = useState<Record<number, boolean>>({});
  const [panelOpen, setPanelOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  // Redirect to sign in
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/app/signin");
    }
  }, [authLoading, isAuthenticated, router]);

  // Load material + slides
  useEffect(() => {
    if (!isAuthenticated || !materialId) return;

    Promise.all([apiGetMaterial(materialId), apiGetMaterialSlides(materialId)]).then(
      ([mat, slideList]) => {
        if (mat) setMaterial(mat);
        setSlides(slideList);
        setLoading(false);
      }
    );
  }, [materialId, isAuthenticated]);

  // Inject edit context into agent session (silent, once)
  useEffect(() => {
    if (!material || contextInjected) return;
    const contextMsg =
      `<memory-context>EDIT SESSION — do NOT generate new materials from scratch. ` +
      `The teacher is editing an existing set. ` +
      `job_id=${material.job_id} project_name=${material.project_name} ` +
      `grammar_point=${material.grammar_point} l1_languages=${material.l1_languages} ` +
      `age_group=${material.age_group} ` +
      `html_bundle_path=${material.html_bundle_path ?? "none"} ` +
      `Use ModifySlide to change specific slides, then BuildOfflineBundle to rebuild. ` +
      `Do NOT call QueueGenerationJob.</memory-context> ` +
      `I am editing existing materials for: ${material.grammar_point}, ${material.l1_languages}, ${material.age_group}. Please confirm you have loaded this context.`;

    apiChat(contextMsg).catch(() => {});
    setContextInjected(true);
  }, [material, contextInjected]);

  // Scroll chat to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, selectedSlide]);

  // Close panel on escape
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && panelOpen) {
        setSelectedSlide(null);
        setPanelOpen(false);
      }
    };
    window.addEventListener("keydown", handleKey as any);
    return () => window.removeEventListener("keydown", handleKey as any);
  }, [panelOpen]);

  const handleSlideClick = useCallback(
    (slideIndex: number) => {
      setSelectedSlide(slideIndex);
      setPanelOpen(true);
      // Scroll to the selected slide thumbnail
      const el = document.getElementById(`slide-thumb-${slideIndex}`);
      el?.scrollIntoView({ behavior: "smooth", block: "center" });
    },
    []
  );

  const handleSubmit = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading || selectedSlide === null || !material) return;

      const userMsg: Message = {
        id: Date.now().toString(),
        role: "user",
        content: trimmed,
      };

      // Prepend slide context to constrain the agent
      const contextWrapped =
        `<slide-context>Editing slide ${selectedSlide} of project ${material.project_name}. ` +
        `Only modify this slide. Do NOT regenerate other slides or call QueueGenerationJob.</slide-context>\n${trimmed}`;

      setMessages((prev) => ({
        ...prev,
        [selectedSlide]: [...(prev[selectedSlide] ?? []), userMsg],
      }));
      setInput("");
      setIsLoading(true);

      try {
        const { response } = await apiChat(contextWrapped);
        const cleaned = cleanResponse(response);

        const assistantMsg: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: cleaned || "Done. The slide has been updated.",
        };

        setMessages((prev) => ({
          ...prev,
          [selectedSlide]: [...(prev[selectedSlide] ?? []), assistantMsg],
        }));

        // Log the edit
        apiLogEdit(material.id, "slide_change", trimmed, selectedSlide).catch(() => {});

        // If response contains download/ or .html references, reload the slide iframe
        if (response.includes("/download/") || response.includes(".html")) {
          const cacheBuster = `?cb=${Date.now()}`;
          setSlides((prev) =>
            prev.map((s) =>
              s.index === selectedSlide ? { ...s, url: s.url.split("?")[0] + cacheBuster } : s
            )
          );
          setSlideLoadErrors((prev) => ({ ...prev, [selectedSlide]: false }));
        }
      } catch {
        const assistantMsg: Message = {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "Sorry, there was an error. Please try again.",
        };
        setMessages((prev) => ({
          ...prev,
          [selectedSlide]: [...(prev[selectedSlide] ?? []), assistantMsg],
        }));
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, selectedSlide, material]
  );

  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();
    handleSubmit(input);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(input);
    }
  };

  // Auth guard
  if (!authLoading && !isAuthenticated) return null;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-neutral-400">Loading material…</div>
      </div>
    );
  }

  if (!material) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <p className="text-neutral-500 mb-4">Material not found.</p>
          <Link
            href="/app/materials"
            className="text-primary-600 dark:text-primary-400 font-semibold hover:underline"
          >
            ← Back to My Materials
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-[calc(100vh-64px)] overflow-hidden">
      {/* ─── Left pane: slide grid ─── */}
      <div
        className={`flex flex-col overflow-hidden transition-all duration-300 ${
          panelOpen ? "w-3/5 border-r border-neutral-200 dark:border-neutral-800" : "w-full"
        }`}
      >
        {/* Header */}
        <div className="shrink-0 px-5 py-3 border-b border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900">
          <div className="flex items-center justify-between">
            <div>
              <Link
                href="/app/materials"
                className="text-xs text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300 transition-colors"
              >
                ← My Materials
              </Link>
              <h1 className="font-heading text-lg font-bold text-neutral-900 dark:text-neutral-50 mt-0.5">
                {material.grammar_point}
              </h1>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                {material.l1_languages} · {material.age_group} · {slides.length} slides
              </p>
            </div>
            <Link
              href={`/app?edit=${material.id}`}
              className="inline-flex items-center gap-1.5 text-xs font-semibold bg-primary-500 text-white hover:bg-primary-600 rounded-lg px-3 py-1.5 transition-colors shrink-0"
            >
              Edit whole material
            </Link>
          </div>
        </div>

        {/* Slide grid */}
        <div className="flex-1 overflow-y-auto p-4 bg-neutral-50 dark:bg-neutral-950">
          {slides.length === 0 ? (
            <div className="text-center py-16 text-neutral-400 text-sm">
              No slides found for this material.
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {slides.map((slide) => (
                <button
                  key={slide.index}
                  id={`slide-thumb-${slide.index}`}
                  onClick={() => handleSlideClick(slide.index)}
                  className={`relative group rounded-xl overflow-hidden border-2 transition-all duration-200 text-left ${
                    selectedSlide === slide.index && panelOpen
                      ? "border-primary-500 ring-2 ring-primary-500/30 shadow-lg"
                      : "border-neutral-200 dark:border-neutral-700 hover:border-primary-300 dark:hover:border-primary-600 shadow-sm"
                  } bg-white dark:bg-neutral-800`}
                >
                  {/* Thumbnail */}
                  <div className="aspect-[4/3] bg-neutral-100 dark:bg-neutral-800 overflow-hidden relative">
                    <iframe
                      src={slide.url}
                      className="w-full h-full pointer-events-none"
                      title={`Slide ${slide.index}`}
                      onError={() =>
                        setSlideLoadErrors((prev) => ({ ...prev, [slide.index]: true }))
                      }
                      style={{ minHeight: "100%" }}
                    />
                    {slideLoadErrors[slide.index] && (
                      <div className="absolute inset-0 flex items-center justify-center bg-neutral-100 dark:bg-neutral-800 text-neutral-400 text-xs">
                        Preview unavailable
                      </div>
                    )}
                  </div>
                  {/* Label */}
                  <div className="px-2.5 py-1.5 flex items-center justify-between">
                    <span className="text-xs font-medium text-neutral-700 dark:text-neutral-300">
                      Slide {slide.index}
                    </span>
                    <span className="text-[10px] text-neutral-400 opacity-0 group-hover:opacity-100 transition-opacity">
                      Click to edit
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ─── Right panel: per-slide chat ─── */}
      {panelOpen && selectedSlide !== null && (
        <div
          ref={panelRef}
          className="w-2/5 flex flex-col bg-white dark:bg-neutral-900 overflow-hidden animate-slide-in-right"
        >
          {/* Panel header */}
          <div className="shrink-0 px-5 py-3 border-b border-neutral-200 dark:border-neutral-800 flex items-center justify-between">
            <div>
              <h2 className="font-semibold text-neutral-900 dark:text-neutral-50 text-sm">
                Slide {selectedSlide}
              </h2>
              <p className="text-[11px] text-neutral-500">
                {slides.find((s) => s.index === selectedSlide)?.notes
                  ? "Has speaker notes"
                  : "No speaker notes"}
              </p>
            </div>
            <button
              onClick={() => {
                setSelectedSlide(null);
                setPanelOpen(false);
              }}
              className="text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300 transition-colors p-1"
              aria-label="Close panel"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>

          {/* Slide preview */}
          <div className="shrink-0 border-b border-neutral-100 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-950">
            <div className="aspect-[4/3] mx-auto max-w-[90%] py-2">
              <iframe
                src={slides.find((s) => s.index === selectedSlide)?.url ?? ""}
                className="w-full h-full pointer-events-none rounded-lg shadow-sm border border-neutral-200 dark:border-neutral-700"
                title={`Slide ${selectedSlide} preview`}
              />
            </div>
          </div>

          {/* Chat messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {(!messages[selectedSlide] || messages[selectedSlide].length === 0) && (
              <div className="text-center py-8">
                <p className="text-xs text-neutral-400">
                  What would you like to change about this slide?
                </p>
                <p className="text-[10px] text-neutral-300 mt-1">
                  Try: &quot;Change the L1 to Korean&quot; or &quot;Fix the example in the second bullet&quot;
                </p>
              </div>
            )}
            {(messages[selectedSlide] ?? []).map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[90%] rounded-2xl px-3.5 py-2 ${
                    msg.role === "user"
                      ? "bg-primary-500 text-white rounded-br-sm"
                      : "bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200 rounded-bl-sm text-sm"
                  }`}
                >
                  {renderMarkdown(msg.content)}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="shrink-0 border-t border-neutral-200 dark:border-neutral-800 p-3">
            <form onSubmit={handleFormSubmit}>
              <div className="flex items-end gap-2">
                <textarea
                  value={input}
                  onChange={(e) => {
                    setInput(e.target.value);
                    const ta = e.target;
                    ta.style.height = "auto";
                    ta.style.height = `${Math.min(ta.scrollHeight, 80)}px`;
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder="What should change on Slide {selectedSlide}..."
                  rows={1}
                  className="flex-1 rounded-xl border border-neutral-300 dark:border-neutral-600 px-3.5 py-2 text-xs bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none overflow-hidden"
                  disabled={isLoading}
                  style={{ minHeight: "36px", maxHeight: "80px" }}
                />
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="bg-primary-500 hover:bg-primary-600 text-white rounded-full p-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shrink-0"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                    <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                  </svg>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
