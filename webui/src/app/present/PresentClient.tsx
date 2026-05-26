"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useSearchParams } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace("/cogniesl/get_response", "") ?? "";

interface SlideInfo {
  index: number;
  url: string;
  notes: string;
}

interface SlidesData {
  job_id: string;
  project_name: string;
  grammar_point: string;
  l1_languages: string;
  total: number;
  slides: SlideInfo[];
  pptx_filename: string | null;
}

export default function PresentClient() {
  const searchParams = useSearchParams();
  const jobId = searchParams.get("jobId") ?? "";

  const [data, setData] = useState<SlidesData | null>(null);
  const [current, setCurrent] = useState(0);
  const [notesOpen, setNotesOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [scale, setScale] = useState(1);

  const containerRef = useRef<HTMLDivElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Fetch slide list
  useEffect(() => {
    if (!jobId) return;
    fetch(`${API_BASE}/api/jobs/${jobId}/slides`)
      .then((r) => r.ok ? r.json() : Promise.reject(r.status))
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => { setError("Slides not found or not yet ready."); setLoading(false); });
  }, [jobId]);

  // Scale iframe to fit container
  const recalcScale = useCallback(() => {
    if (!containerRef.current) return;
    const cw = containerRef.current.clientWidth - 32;
    const ch = containerRef.current.clientHeight - 32;
    setScale(Math.min(cw / 1280, ch / 720));
  }, []);

  useEffect(() => {
    recalcScale();
    window.addEventListener("resize", recalcScale);
    return () => window.removeEventListener("resize", recalcScale);
  }, [recalcScale, notesOpen]);

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === " ") {
        e.preventDefault();
        setCurrent((c) => (data ? Math.min(c + 1, data.total - 1) : c));
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        setCurrent((c) => Math.max(c - 1, 0));
      } else if (e.key === "n" || e.key === "N") {
        setNotesOpen((o) => !o);
      } else if (e.key === "f" || e.key === "F") {
        toggleFullscreen();
      } else if (e.key === "Escape" && !document.fullscreenElement) {
        window.history.back();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [data]);

  // Fullscreen change listener
  useEffect(() => {
    const handler = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", handler);
    return () => document.removeEventListener("fullscreenchange", handler);
  }, []);

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  const title = data
    ? `${data.grammar_point.replace(/_/g, " ")} — ${data.l1_languages}`
    : "CogniESL Presenter";

  const currentSlide = data?.slides[current];
  const notes = currentSlide?.notes || "(No speaker notes for this slide)";

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-black text-gray-400 text-sm">
        Loading slides…
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-black text-gray-400 gap-4">
        <p className="text-red-400">{error}</p>
        <a href="/materials" className="text-teal text-sm underline">← Back to My Materials</a>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-[#0a0a0a] overflow-hidden">
      {/* Controls bar */}
      <div className="flex items-center gap-2 px-4 py-2 bg-[#111] border-b border-[#222] flex-shrink-0">
        <a
          href="/materials"
          className="text-gray-500 hover:text-gray-300 text-xs mr-1 flex-shrink-0"
          title="Back to My Materials"
        >
          ←
        </a>
        <span className="text-gray-500 text-xs flex-1 truncate">{title}</span>

        {/* Slide counter */}
        <span className="text-gray-600 text-xs tabular-nums flex-shrink-0">
          {current + 1} / {data?.total}
        </span>

        {/* Prev / Next */}
        <button
          onClick={() => setCurrent((c) => Math.max(c - 1, 0))}
          disabled={current === 0}
          className="text-gray-400 hover:text-white disabled:opacity-25 text-sm px-2 py-1 rounded bg-[#1e1e1e] border border-[#333] hover:border-[#555] transition-colors flex-shrink-0"
        >
          ◀
        </button>
        <button
          onClick={() => setCurrent((c) => (data ? Math.min(c + 1, data.total - 1) : c))}
          disabled={!data || current === data.total - 1}
          className="text-gray-400 hover:text-white disabled:opacity-25 text-sm px-2 py-1 rounded bg-[#1e1e1e] border border-[#333] hover:border-[#555] transition-colors flex-shrink-0"
        >
          ▶
        </button>

        {/* Notes toggle */}
        <button
          onClick={() => { setNotesOpen((o) => !o); setTimeout(recalcScale, 50); }}
          className={`text-xs px-2.5 py-1 rounded border transition-colors flex-shrink-0 ${
            notesOpen
              ? "bg-teal text-white border-teal"
              : "bg-[#1e1e1e] text-gray-400 border-[#333] hover:text-white hover:border-[#555]"
          }`}
        >
          📝 Notes
        </button>

        {/* Fullscreen */}
        <button
          onClick={toggleFullscreen}
          className={`text-xs px-2.5 py-1 rounded border transition-colors flex-shrink-0 ${
            isFullscreen
              ? "bg-[#2a2a2a] text-white border-[#555]"
              : "bg-[#1e1e1e] text-gray-400 border-[#333] hover:text-white hover:border-[#555]"
          }`}
          title="F"
        >
          ⛶
        </button>

        {/* Downloads */}
        {data?.pptx_filename && (
          <a
            href={`/download/${jobId}/${data.pptx_filename}`}
            download
            className="text-xs px-2.5 py-1 rounded bg-[#1e1e1e] text-gray-400 border border-[#333] hover:text-white hover:border-[#555] transition-colors flex-shrink-0"
          >
            📊 PPTX
          </a>
        )}
        <a
          href={`${API_BASE}/api/jobs/${jobId}/bundle.html`}
          download
          className="text-xs px-2.5 py-1 rounded bg-[#1e1e1e] text-gray-400 border border-[#333] hover:text-white hover:border-[#555] transition-colors flex-shrink-0"
        >
          📦 Bundle
        </a>
      </div>

      {/* Stage */}
      <div className="flex flex-1 overflow-hidden">
        {/* Slide viewport */}
        <div
          ref={containerRef}
          className="flex-1 flex items-center justify-center overflow-hidden relative"
        >
          {currentSlide && (
            <iframe
              ref={iframeRef}
              key={currentSlide.url}
              src={currentSlide.url}
              title={`Slide ${current + 1}`}
              sandbox="allow-same-origin allow-scripts"
              style={{
                width: 1280,
                height: 720,
                border: "none",
                transformOrigin: "center center",
                transform: `scale(${scale})`,
                display: "block",
              }}
              onLoad={recalcScale}
            />
          )}

          {/* Slide thumbnail strip at bottom */}
          {data && data.total > 1 && (
            <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-1.5 items-center">
              {data.slides.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  className={`rounded-full transition-all ${
                    i === current
                      ? "w-3 h-3 bg-teal"
                      : "w-2 h-2 bg-[#333] hover:bg-[#555]"
                  }`}
                  title={`Slide ${i + 1}`}
                />
              ))}
            </div>
          )}

          {/* Keyboard hint */}
          <p className="absolute bottom-10 left-1/2 -translate-x-1/2 text-[#1e1e1e] text-xs pointer-events-none select-none whitespace-nowrap">
            ← → navigate &nbsp;·&nbsp; N notes &nbsp;·&nbsp; F fullscreen &nbsp;·&nbsp; Esc back
          </p>
        </div>

        {/* Speaker notes panel */}
        {notesOpen && (
          <div className="w-72 bg-[#111] border-l border-[#222] p-5 flex flex-col flex-shrink-0 overflow-hidden">
            <h2 className="text-[#0d9488] text-[10px] font-bold tracking-widest uppercase mb-3 flex-shrink-0">
              Speaker Notes — Slide {current + 1}
            </h2>
            <div className="flex-1 overflow-y-auto">
              <p className="text-gray-400 text-xs leading-relaxed whitespace-pre-wrap">{notes}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
