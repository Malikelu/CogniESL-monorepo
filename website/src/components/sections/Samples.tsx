"use client";

import { useState, useEffect } from "react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import Link from "next/link";

const GENERATION_STEPS = [
  { label: "Analyzing request...", duration: 800 },
  { label: "Loading L1 database (Spanish)...", duration: 600 },
  { label: "Scanning 302 grammar files...", duration: 700 },
  { label: "Identifying interference patterns...", duration: 900 },
  { label: "Building slide deck (16 slides)...", duration: 1200 },
  { label: "Generating worksheet (Sections A–E)...", duration: 1000 },
  { label: "Creating activity guide...", duration: 800 },
  { label: "Adding speaker notes...", duration: 600 },
  { label: "Packaging for delivery...", duration: 500 },
];

function GenerationPreview() {
  const [step, setStep] = useState(-1);
  const [slideContent, setSlideContent] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;
    if (step >= GENERATION_STEPS.length) {
      setTimeout(() => {
        setStep(-1);
        setSlideContent(0);
        setIsRunning(false);
      }, 4000);
      return;
    }
    const duration = step === -1 ? 400 : GENERATION_STEPS[step].duration;
    const timer = setTimeout(() => {
      setStep((s) => s + 1);
      if (step >= 4) {
        setSlideContent((c) => Math.min(c + 1, 3));
      }
    }, duration);
    return () => clearTimeout(timer);
  }, [step, isRunning]);

  const startGeneration = () => {
    setStep(-1);
    setSlideContent(0);
    setIsRunning(true);
    setTimeout(() => setStep(0), 100);
  };

  const isComplete = step >= GENERATION_STEPS.length;
  const currentLabel = step >= 0 && step < GENERATION_STEPS.length ? GENERATION_STEPS[step].label : "";

  return (
    <div className="relative mx-auto max-w-3xl">
      {/* Browser chrome */}
      <div className="bg-white dark:bg-neutral-900 rounded-xl overflow-hidden border border-neutral-200 dark:border-neutral-800 shadow-elevated">
        {/* Title bar */}
        <div className="flex items-center gap-2 px-4 py-3 bg-neutral-50 dark:bg-neutral-800/80 border-b border-neutral-200/60 dark:border-neutral-700/60">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-secondary-400" />
            <div className="w-3 h-3 rounded-full bg-accent-400" />
            <div className="w-3 h-3 rounded-full bg-success-400" />
          </div>
          <div className="flex-1 mx-4">
            <div className="bg-neutral-200/60 dark:bg-neutral-700/60 rounded-md px-3 py-1 text-xs text-neutral-500 dark:text-neutral-400 text-center">
              app.cogniesl.com
            </div>
          </div>
        </div>

        {/* Generation status bar */}
        <div className="px-4 py-2.5 bg-primary-50 dark:bg-primary-900/20 border-b border-primary-100 dark:border-primary-800/30">
          <div className="flex items-center gap-2 text-sm">
            {!isRunning && !isComplete && (
              <span className="text-primary-700 dark:text-primary-300 font-medium">Ready to generate</span>
            )}
            {isRunning && !isComplete && (
              <>
                <div className="w-3 h-3 rounded-full bg-primary-500 animate-pulse flex-shrink-0" />
                <span className="text-primary-700 dark:text-primary-300 font-medium truncate">{currentLabel}</span>
              </>
            )}
            {isComplete && (
              <>
                <svg className="w-4 h-4 text-success-600 dark:text-success-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-success-700 dark:text-success-400 font-medium">3 files ready — delivered to your inbox</span>
              </>
            )}
          </div>
          {/* Progress bar */}
          {(isRunning || isComplete) && (
            <div className="mt-2 w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-1.5 overflow-hidden">
              <div
                className="bg-gradient-to-r from-primary-500 to-success-500 h-1.5 rounded-full transition-all duration-500 ease-out"
                style={{ width: isComplete ? "100%" : `${((step + 1) / GENERATION_STEPS.length) * 100}%` }}
              />
            </div>
          )}
        </div>

        {/* Slide preview area */}
        <div className="p-4 min-h-[320px] bg-white dark:bg-neutral-900">
          {!isRunning && !isComplete && (
            <div className="flex flex-col items-center justify-center h-[280px] text-center">
              <div className="w-16 h-16 rounded-2xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
              </div>
              <p className="text-neutral-500 dark:text-neutral-400 mb-4 text-sm">See how CogniESL generates a complete lesson set</p>
              <button
                onClick={startGeneration}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary-500 hover:bg-primary-600 text-white font-semibold text-sm transition-colors cursor-pointer"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 010 1.972l-11.54 6.347a1.125 1.125 0 01-1.667-.986V5.653z" />
                </svg>
                Watch it generate
              </button>
            </div>
          )}

          {(isRunning || isComplete) && (
            <div className="space-y-3">
              {/* Simulated slide being built */}
              <div className="rounded-lg border border-neutral-200 dark:border-neutral-700 overflow-hidden">
                {/* Slide header */}
                <div className={`px-3 py-2 bg-gradient-to-r from-teal-600 to-teal-700 text-white text-xs font-semibold flex items-center justify-between transition-opacity duration-500 ${slideContent >= 1 ? "opacity-100" : "opacity-0"}`}>
                  <span>📊 L1 Oracle — Spanish Speakers</span>
                  <span className="text-white/60 text-[10px]">Slide 7 of 16</span>
                </div>

                {/* Slide body */}
                <div className="p-3 space-y-2">
                  {/* Error example */}
                  <div className={`rounded-md border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 px-2.5 py-2 transition-all duration-500 ${slideContent >= 2 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"}`}>
                    <div className="text-[10px] text-red-400 font-bold mb-0.5">❌ INCORRECT</div>
                    <div className="text-xs text-red-700 dark:text-red-300 font-mono font-semibold">&ldquo;He walk to school every day.&rdquo;</div>
                    <div className="text-[10px] text-neutral-500 dark:text-neutral-400 mt-0.5">Third-person -s dropped — frequency: very high</div>
                  </div>

                  {/* Correct example */}
                  <div className={`rounded-md border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-900/20 px-2.5 py-2 transition-all duration-500 delay-200 ${slideContent >= 2 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"}`}>
                    <div className="text-[10px] text-emerald-500 font-bold mb-0.5">✅ CORRECT</div>
                    <div className="text-xs text-emerald-700 dark:text-emerald-300 font-mono font-semibold">
                      &ldquo;He walk<span className="bg-emerald-300 dark:bg-emerald-700 text-emerald-900 dark:text-white px-0.5 rounded">s</span> to school every day.&rdquo;
                    </div>
                  </div>

                  {/* Why box */}
                  <div className={`rounded-md bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 px-2.5 py-2 transition-all duration-500 delay-300 ${slideContent >= 3 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"}`}>
                    <div className="text-[10px] text-blue-600 dark:text-blue-400 font-bold mb-0.5">💡 WHY THIS HAPPENS</div>
                    <div className="text-[10px] text-blue-800 dark:text-blue-200 leading-relaxed">
                      Spanish verbs have different endings per subject, but there&apos;s no separate suffix rule for 3rd person. Students transfer &ldquo;caminar&rdquo; directly without adding -s.
                    </div>
                  </div>
                </div>
              </div>

              {/* File generation indicators */}
              <div className="grid grid-cols-3 gap-2">
                {[
                  { label: "Slide Deck", icon: "📊", count: "16 slides", threshold: 5 },
                  { label: "Worksheet", icon: "📝", count: "Sections A–E", threshold: 6 },
                  { label: "Activity Guide", icon: "🎮", count: "Step-by-step", threshold: 7 },
                ].map((file) => (
                  <div
                    key={file.label}
                    className={`rounded-lg border px-2.5 py-2 text-center transition-all duration-500 ${
                      slideContent >= file.threshold
                        ? "border-success-300 dark:border-success-700 bg-success-50 dark:bg-success-900/20"
                        : "border-neutral-200 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800/50"
                    }`}
                  >
                    <div className={`text-lg mb-0.5 transition-opacity duration-300 ${slideContent >= file.threshold ? "opacity-100" : "opacity-30"}`}>{file.icon}</div>
                    <div className={`text-[10px] font-semibold transition-colors duration-300 ${slideContent >= file.threshold ? "text-success-700 dark:text-success-400" : "text-neutral-400"}`}>{file.label}</div>
                    <div className="text-[9px] text-neutral-500">{file.count}</div>
                    {slideContent >= file.threshold && (
                      <div className="mt-1">
                        <svg className="w-3 h-3 text-success-500 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Bottom bar */}
        <div className="px-4 py-2 bg-neutral-50 dark:bg-neutral-800 border-t border-neutral-100 dark:border-neutral-700 flex items-center justify-between">
          <div className="text-[10px] text-neutral-400">
            {isComplete ? "Generated in 6.2 seconds" : isRunning ? "Generating..." : "Present Simple · Spanish L1 · B1"}
          </div>
          {isComplete && (
            <button
              onClick={startGeneration}
              className="text-[10px] text-primary-600 dark:text-primary-400 font-semibold hover:underline cursor-pointer"
            >
              Run again →
            </button>
          )}
        </div>
      </div>

      <p className="text-center text-xs text-neutral-400 dark:text-neutral-500 mt-3">
        This is a real sample from a generated deck — Spanish speakers, Present Simple, B1
      </p>
    </div>
  );
}

const deliverables = [
  {
    type: "Slide Deck",
    icon: "📊",
    count: "15–18 slides",
    color: "bg-primary-500",
    items: [
      "Concept Check Questions before rules",
      "L1 Oracle slide (red/green error callouts)",
      "Formation rules with visual anchors",
      "Practice → Production activities",
      "Full speaker notes on every slide",
    ],
  },
  {
    type: "Worksheet",
    icon: "📝",
    count: "Sections A–E + answer key",
    color: "bg-secondary-500",
    items: [
      "Section A: Guided production",
      "Section B: Error identification",
      "Section C: Transformation drills",
      "Section D: Communicative tasks",
      "Section E: Free writing prompt",
      "Answer key explains the L1 reason",
    ],
  },
  {
    type: "Activity Guide",
    icon: "🎮",
    count: "Step-by-step teacher script",
    color: "bg-accent-500",
    items: [
      "Exact words to say — no improvising",
      "Timing guide per activity stage",
      "Differentiation for A and B classes",
      "L1-specific watch-fors and tips",
      "Extension tasks for fast finishers",
    ],
  },
];

export function Samples() {
  return (
    <section id="samples" className="py-20 lg:py-28 bg-white dark:bg-neutral-900">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-semibold mb-4">
            What you receive
          </span>
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            Three complete formats.
            <br />
            <span className="gradient-text">Open Monday. Teach Monday.</span>
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed">
            One request. Materials delivered to your inbox. Here&apos;s exactly what&apos;s inside.
          </p>
        </div>

        {/* Animated generation preview */}
        <div className="mb-20">
          <GenerationPreview />
        </div>

        {/* Three deliverable cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto mb-12">
          {deliverables.map((d) => (
            <div
              key={d.type}
              className="rounded-2xl bg-neutral-50 dark:bg-neutral-800/50 border border-neutral-200/80 dark:border-neutral-700/60 overflow-hidden hover:-translate-y-0.5 hover:shadow-card-hover transition-all duration-300"
            >
              <div className={`${d.color} px-5 py-4 flex items-center gap-3`}>
                <span className="text-2xl">{d.icon}</span>
                <div>
                  <div className="text-white font-bold text-sm">{d.type}</div>
                  <div className="text-white/70 text-xs">{d.count}</div>
                </div>
              </div>
              <ul className="p-5 space-y-2.5">
                {d.items.map((item) => (
                  <li key={item} className="flex items-start gap-2.5 text-sm">
                    <svg className="w-4 h-4 text-success-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-neutral-600 dark:text-neutral-400">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="text-center">
          <Button variant="outline" asChild>
            <Link href="/samples">View full output samples →</Link>
          </Button>
        </div>
      </Container>
    </section>
  );
}
