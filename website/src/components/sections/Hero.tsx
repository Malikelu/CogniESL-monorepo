"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";

const demoConversations = [
  {
    l1: "Spanish",
    flag: "🇪🇸",
    user: "Teaching present perfect tomorrow. My students are Spanish speakers, B1 level.",
    responses: [
      { type: "thinking", text: "Scanning L1 database for Spanish interference patterns..." },
      { type: "insight", text: "3 high-priority interference patterns found:" },
      { type: "bullet", text: "Preterite transfer — \"I have seen him yesterday\"" },
      { type: "bullet", text: "\"Ya\" → \"already\" overuse (frequency: high)" },
      { type: "bullet", text: "Dropped auxiliary: \"She seen the film?\"" },
      { type: "generating", text: "Building your materials..." },
      { type: "done", text: "Ready: 15-slide deck · Worksheet (Sections A–E + answer key) · Activity guide" },
    ],
  },
  {
    l1: "Korean",
    flag: "🇰🇷",
    user: "Korean students keep dropping articles. Intermediate, adult learners.",
    responses: [
      { type: "thinking", text: "Scanning L1 database for Korean interference patterns..." },
      { type: "insight", text: "5 critical patterns — Korean has no article system:" },
      { type: "bullet", text: "a/an/the all omitted — \"I went to store\"" },
      { type: "bullet", text: "\"The\" overused with proper nouns" },
      { type: "bullet", text: "Definiteness marked by context, not articles" },
      { type: "generating", text: "Building your materials..." },
      { type: "done", text: "Ready: Discovery worksheet · Error correction cards · Visual reference" },
    ],
  },
  {
    l1: "Arabic",
    flag: "🇸🇦",
    user: "Conditionals for my Arabic class, intermediate. Need role-play activities.",
    responses: [
      { type: "thinking", text: "Scanning L1 database for Arabic interference patterns..." },
      { type: "insight", text: "4 patterns identified — tense system differs significantly:" },
      { type: "bullet", text: "If-clause word order transfer" },
      { type: "bullet", text: "Tense backshifting errors in 2nd/3rd conditional" },
      { type: "bullet", text: "\"Unless\" confused with \"if not\"" },
      { type: "generating", text: "Building your materials..." },
      { type: "done", text: "Ready: Role-play cards · Conditional maze · Error analysis sheet" },
    ],
  },
];

export function Hero() {
  const [activeDemo, setActiveDemo] = useState(0);
  const [visibleLines, setVisibleLines] = useState(0);
  const [isTyping, setIsTyping] = useState(true);
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const demo = demoConversations[activeDemo];
  const totalLines = 1 + demo.responses.length;

  useEffect(() => {
    setVisibleLines(0);
    setIsTyping(true);

    if (intervalRef.current) clearInterval(intervalRef.current);

    intervalRef.current = setInterval(() => {
      setVisibleLines((prev) => {
        if (prev >= totalLines) {
          if (intervalRef.current) clearInterval(intervalRef.current);
          setIsTyping(false);
          setTimeout(() => {
            setActiveDemo((d) => (d + 1) % demoConversations.length);
          }, 3500);
          return prev;
        }
        return prev + 1;
      });
    }, 480);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [activeDemo, totalLines]);

  const handleWaitlist = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setLoading(true);
    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error();
      setSubmitted(true);
    } catch {
      // fail silently, let user try again
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="relative pt-24 pb-16 lg:pt-32 lg:pb-24 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-primary-50/50 via-neutral-50 to-neutral-50 dark:from-neutral-950 dark:via-neutral-950 dark:to-neutral-950" />
      {/* Orbs */}
      <div className="absolute top-20 right-[10%] w-[500px] h-[500px] bg-primary-300/10 dark:bg-primary-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-20 left-[5%] w-[400px] h-[400px] bg-secondary-300/10 dark:bg-secondary-500/5 rounded-full blur-3xl pointer-events-none" />

      <Container className="relative">
        {/* Center-aligned headline block */}
        <div className="max-w-4xl mx-auto text-center mb-12 lg:mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100/80 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-semibold mb-8 backdrop-blur-sm border border-primary-200/50 dark:border-primary-800/50">
            <span className="w-2 h-2 rounded-full bg-success-500 animate-pulse-soft flex-shrink-0" />
            Private beta · 47 ESL teachers already using it
          </div>

          <h1 className="font-heading text-4xl md:text-5xl lg:text-[3.75rem] font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-[1.08] tracking-tight">
            Your Spanish students drop third-person&nbsp;-s.
            <br />
            <span className="gradient-text">Your materials should already know that.</span>
          </h1>

          <p className="text-xl md:text-2xl text-neutral-600 dark:text-neutral-400 mb-10 leading-relaxed max-w-2xl mx-auto">
            Tell CogniESL your students&apos; native language. Get slides, worksheets, and activity guides built around{" "}
            <strong className="text-neutral-900 dark:text-neutral-100">the specific errors their L1 causes</strong> — backed by peer-reviewed linguistics, not guesswork.
          </p>

          {/* Dual CTA: email capture + direct "try it free" */}
          {!submitted ? (
            <div className="flex flex-col items-center gap-4 mb-6">
              <form onSubmit={handleWaitlist} className="flex flex-col sm:flex-row gap-3 w-full max-w-md">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your@email.com"
                  required
                  className="flex-1 px-5 py-4 rounded-xl bg-white dark:bg-neutral-900 border border-neutral-300 dark:border-neutral-700 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 text-base shadow-sm"
                />
                <Button type="submit" disabled={loading} size="lg">
                  {loading ? "Joining..." : "Get Early Access"}
                </Button>
              </form>
              <div className="flex items-center gap-3 text-sm text-neutral-500 dark:text-neutral-400">
                <span>Already have an account?</span>
                <a href="/app" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
                  Start generating →
                </a>
              </div>
            </div>
          ) : (
            <div className="inline-flex items-center gap-3 px-6 py-4 rounded-xl bg-success-50 dark:bg-success-900/20 border border-success-200 dark:border-success-800 text-success-700 dark:text-success-300 text-base font-semibold mb-6 animate-fade-in">
              <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              You&apos;re on the list! We&apos;ll be in touch soon.
            </div>
          )}

          <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-neutral-500 dark:text-neutral-400">
            {[
              "No credit card · Free plan available",
              "36 L1 languages — Spanish to Korean to Arabic",
              "First 100 get Pro at $7/mo — locked forever",
            ].map((item) => (
              <div key={item} className="flex items-center gap-1.5">
                <svg className="w-4 h-4 text-success-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                {item}
              </div>
            ))}
          </div>
        </div>

        {/* Live demo panel — full width, prominent */}
        <div className="max-w-2xl mx-auto">
          <div className="relative">
            {/* Glow behind panel */}
            <div className="absolute -inset-px bg-gradient-to-r from-primary-500/20 via-accent-500/15 to-secondary-500/20 rounded-2xl blur-xl" />

            <div className="relative bg-white dark:bg-neutral-900 rounded-2xl shadow-elevated border border-neutral-200/80 dark:border-neutral-800 overflow-hidden">
              {/* Browser chrome */}
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
                {/* L1 selector dots */}
                <div className="flex gap-1.5">
                  {demoConversations.map((d, i) => (
                    <button
                      key={i}
                      onClick={() => setActiveDemo(i)}
                      className={`flex items-center gap-1 text-xs px-2 py-0.5 rounded-full transition-all font-medium ${
                        i === activeDemo
                          ? "bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300"
                          : "text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300"
                      }`}
                      aria-label={`Show ${d.l1} demo`}
                    >
                      {d.flag} {d.l1}
                    </button>
                  ))}
                </div>
              </div>

              {/* Chat area */}
              <div className="p-5 h-[340px] space-y-3 font-mono text-sm overflow-hidden">
                {visibleLines >= 1 && (
                  <div className="flex justify-end animate-fade-in">
                    <div className="bg-primary-500 text-white rounded-2xl rounded-br-sm px-4 py-2.5 max-w-[85%] leading-relaxed text-[0.82rem]">
                      {demo.user}
                    </div>
                  </div>
                )}

                {visibleLines >= 2 && (
                  <div className="flex justify-start animate-fade-in">
                    <div className="bg-neutral-100 dark:bg-neutral-800 rounded-2xl rounded-bl-sm px-4 py-3 max-w-[90%] space-y-1.5">
                      {demo.responses.slice(0, visibleLines - 1).map((response, i) => {
                        let cls = "text-neutral-600 dark:text-neutral-300 text-[0.8rem]";
                        if (response.type === "thinking") cls = "text-accent-600 dark:text-accent-400 font-medium text-[0.8rem] italic";
                        if (response.type === "insight") cls = "text-primary-700 dark:text-primary-300 font-semibold text-[0.8rem]";
                        if (response.type === "bullet") cls = "text-neutral-500 dark:text-neutral-400 pl-3 text-[0.75rem] border-l-2 border-primary-200 dark:border-primary-800";
                        if (response.type === "generating") cls = "text-neutral-500 dark:text-neutral-400 text-[0.78rem] italic";
                        if (response.type === "done") cls = "text-success-700 dark:text-success-400 font-semibold text-[0.82rem]";
                        return (
                          <p key={i} className={cls}>
                            {response.text}
                          </p>
                        );
                      })}

                      {isTyping && visibleLines < totalLines && (
                        <div className="flex gap-1 pt-1">
                          <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                          <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                          <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Footer hint */}
              <div className="px-5 pb-4 text-center">
                <p className="text-xs text-neutral-400 dark:text-neutral-500">
                  Live demo — {demo.l1} speakers · click a language above to switch
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Secondary CTA */}
        <div className="text-center mt-10">
          <Button variant="ghost" asChild>
            <Link href="#how-it-works" className="flex items-center gap-2 mx-auto w-fit">
              See how it works
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </Link>
          </Button>
        </div>
      </Container>
    </section>
  );
}
