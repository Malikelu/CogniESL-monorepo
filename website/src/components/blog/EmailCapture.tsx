"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export function EmailCapture({ source = "blog" }: { source?: string }) {
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
        body: JSON.stringify({ email, source }),
      });

      if (!res.ok) throw new Error("Something went wrong. Please try again.");

      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="bg-success-50 dark:bg-success-900/20 border border-success-200 dark:border-success-800 rounded-xl p-4 text-center">
        <p className="text-success-700 dark:text-success-300 text-sm font-medium">
          🎉 You&apos;re on the list! We&apos;ll send you practical ESL teaching tips.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-neutral-50 dark:bg-neutral-800/50 border border-neutral-200 dark:border-neutral-700 rounded-xl p-5">
      <h4 className="font-heading text-base font-semibold text-neutral-900 dark:text-neutral-100 mb-1">
        Enjoyed this post?
      </h4>
      <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
        Join 200+ ESL teachers getting practical tips and insights. No spam, we promise.
      </p>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your@email.com"
          required
          className="flex-1"
        />
        <Button type="submit" disabled={loading} className="whitespace-nowrap">
          {loading ? "Joining..." : "Subscribe"}
        </Button>
      </form>
      {error && <p className="text-secondary-600 dark:text-secondary-400 text-xs mt-2">{error}</p>}
    </div>
  );
}
