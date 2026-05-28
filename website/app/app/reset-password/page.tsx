"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Container } from "@/components/ui/Container";

const API_URL = "https://cogniesl-production.up.railway.app";

export default function ResetPasswordPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (!token) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center py-12">
        <Container size="sm">
          <div className="text-center space-y-4">
            <p className="text-neutral-600 dark:text-neutral-400">Invalid or missing reset token.</p>
            <Link href="/app/forgot-password" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
              Request a new link
            </Link>
          </div>
        </Container>
      </div>
    );
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (password.length < 8) { setError("Password must be at least 8 characters"); return; }
    if (password !== confirm) { setError("Passwords don't match"); return; }
    setLoading(true);
    const res = await fetch(`${API_URL}/api/auth/reset-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, new_password: password }),
    });
    const data = await res.json();
    if (!res.ok) { setError(data.error || "Reset failed. The link may have expired."); setLoading(false); return; }
    router.push("/app/signin?reset=1");
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center py-12">
      <Container size="sm">
        <div className="bg-white dark:bg-neutral-900 rounded-2xl border border-neutral-200 dark:border-neutral-800 p-8 shadow-card">
          <div className="text-center mb-8">
            <Link href="/" className="inline-flex items-center mb-6">
              <img src="/logo-wordmark-light.svg" alt="CogniESL" height={32} className="h-[32px] w-auto dark:hidden" />
              <img src="/logo-wordmark-dark.svg" alt="CogniESL" height={32} className="h-[32px] w-auto hidden dark:block" />
            </Link>
            <h1 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">
              Choose a new password
            </h1>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-secondary-50 dark:bg-secondary-900/20 border border-secondary-200 dark:border-secondary-800 text-secondary-700 dark:text-secondary-300 text-sm rounded-xl px-4 py-3">
                {error}
              </div>
            )}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
                New password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Min. 8 characters"
                className="w-full rounded-xl border border-neutral-300 dark:border-neutral-600 px-4 py-3 text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label htmlFor="confirm" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
                Confirm password
              </label>
              <input
                id="confirm"
                type="password"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                required
                placeholder="Re-enter your password"
                className="w-full rounded-xl border border-neutral-300 dark:border-neutral-600 px-4 py-3 text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 shadow-glow hover:shadow-glow-lg px-6 py-3 text-base disabled:opacity-50"
            >
              {loading ? "Saving…" : "Set new password"}
            </button>
          </form>
        </div>
      </Container>
    </div>
  );
}
