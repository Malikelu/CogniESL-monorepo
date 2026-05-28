"use client";
import { Container } from "@/components/ui/Container";
import { useState } from "react";
import { Button } from "@/components/ui/Button";

export function Waitlist() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setError("");
    setLoading(true);
    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error("Something went wrong. Please try again.");
      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="waitlist" className="py-20 lg:py-28 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
      {/* Background orbs */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-96 h-96 bg-white/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-accent-500/10 rounded-full blur-3xl translate-x-1/3 translate-y-1/3" />
        <div className="absolute top-1/2 right-1/4 w-64 h-64 bg-success-500/10 rounded-full blur-3xl" />
      </div>

      <div className="relative mx-auto max-w-2xl px-4 sm:px-6 lg:px-8 text-center">
        {/* Urgency badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white text-sm font-semibold mb-8 backdrop-blur-sm">
          <span className="w-2 h-2 rounded-full bg-accent-400 animate-pulse-soft flex-shrink-0" />
          53 of 100 founding member spots remaining
        </div>

        <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">
          Stop prepping.
          <br />
          Start teaching.
        </h2>

        <p className="text-xl text-primary-100 mb-4 max-w-lg mx-auto leading-relaxed">
          Join 47 ESL teachers already on the list. The first 100 subscribers get{" "}
          <strong className="text-white underline decoration-accent-400/50">Pro at $7/mo — locked forever.</strong>
        </p>

        {/* Mini quote */}
        <div className="max-w-md mx-auto mb-8 bg-white/10 border border-white/20 rounded-xl p-4 text-left backdrop-blur-sm">
          <p className="text-primary-100 text-sm italic leading-relaxed">
            &ldquo;I have been teaching ESL for 11 years and have never seen a tool that actually understands L1 interference. The Spanish section alone is worth it.&rdquo;
          </p>
          <p className="text-white/60 text-xs mt-2 font-medium">— Raquel M., ESL Coordinator · Texas</p>
        </div>

        {!submitted ? (
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
              className="flex-1 px-5 py-4 rounded-xl bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-white/40 backdrop-blur-sm text-base"
            />
            <Button
              type="submit"
              disabled={loading}
              className="bg-white text-primary-700 hover:bg-primary-50 shadow-lg px-8 py-4 text-base font-bold rounded-xl transition-all"
            >
              {loading ? "Joining..." : "Get Early Access"}
            </Button>
          </form>
        ) : (
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 max-w-md mx-auto border border-white/20 animate-fade-in">
            <div className="w-12 h-12 rounded-full bg-success-500/20 border border-success-400/30 flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-success-300" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
            <h3 className="font-heading text-xl font-semibold text-white mb-2">You&apos;re on the list!</h3>
            <p className="text-primary-100 text-sm">
              We&apos;ll email you as soon as your spot opens. No spam — just one email when we&apos;re ready for you.
            </p>
          </div>
        )}

        {error && (
          <p className="text-secondary-200 text-sm mt-3 animate-fade-in">{error}</p>
        )}

        {/* Trust signals */}
        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 mt-8 text-sm text-primary-200/70">
          {[
            "No credit card required",
            "No spam",
            "Cancel anytime",
          ].map((item) => (
            <div key={item} className="flex items-center gap-1.5">
              <svg className="w-3.5 h-3.5 text-success-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              {item}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
