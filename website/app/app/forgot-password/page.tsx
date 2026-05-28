"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { Container } from "@/components/ui/Container";

const API_URL = "https://cogniesl-production.up.railway.app";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await fetch(`${API_URL}/api/auth/forgot-password`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    // Always show success — never reveal whether email exists
    setSubmitted(true);
    setLoading(false);
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
              Reset your password
            </h1>
            <p className="text-neutral-500 dark:text-neutral-400 text-sm">
              Enter your email and we'll send you a reset link
            </p>
          </div>

          {submitted ? (
            <div className="text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center mx-auto">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6 text-primary-600 dark:text-primary-400">
                  <path fillRule="evenodd" d="M19.916 4.626a.75.75 0 01.208 1.04l-9 13.5a.75.75 0 01-1.154.114l-6-6a.75.75 0 011.06-1.06l5.353 5.353 8.493-12.739a.75.75 0 011.04-.208z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                If an account exists for <strong>{email}</strong>, you'll receive a reset link shortly.
              </p>
              <Link href="/app/signin" className="text-sm text-primary-600 dark:text-primary-400 font-semibold hover:underline">
                Back to sign in
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                  placeholder="you@school.edu"
                  className="w-full rounded-xl border border-neutral-300 dark:border-neutral-600 px-4 py-3 text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 shadow-glow hover:shadow-glow-lg px-6 py-3 text-base disabled:opacity-50"
              >
                {loading ? "Sending…" : "Send reset link"}
              </button>
              <div className="text-center">
                <Link href="/app/signin" className="text-sm text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300">
                  Back to sign in
                </Link>
              </div>
            </form>
          )}
        </div>
      </Container>
    </div>
  );
}
