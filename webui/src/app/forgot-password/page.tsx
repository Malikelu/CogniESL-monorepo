"use client";

import { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";

const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace("/cogniesl/get_response", "") ?? "";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes("@")) {
      setError("Please enter a valid email address.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await fetch(`${API_BASE}/api/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      // Always show success — never reveal whether email exists
      setSubmitted(true);
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
            {!submitted ? (
              <>
                <h1 className="text-xl font-display font-bold text-gray-900 mb-2">Reset your password</h1>
                <p className="text-sm text-gray-500 mb-6">
                  Enter your email and we&apos;ll send you a reset link if an account exists.
                </p>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <input
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => { setEmail(e.target.value); setError(""); }}
                    required
                    className="w-full text-sm border border-gray-300 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
                  />
                  {error && <p className="text-xs text-red-500">{error}</p>}
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-teal hover:bg-teal-dark disabled:opacity-60 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
                  >
                    {loading ? "Sending…" : "Send reset link"}
                  </button>
                </form>
                <p className="text-center text-xs text-gray-400 mt-5">
                  Remember your password?{" "}
                  <Link href="/" className="text-teal hover:underline">Sign in</Link>
                </p>
              </>
            ) : (
              <>
                <div className="text-center">
                  <div className="text-4xl mb-4">✉️</div>
                  <h1 className="text-xl font-display font-bold text-gray-900 mb-2">Check your email</h1>
                  <p className="text-sm text-gray-500 mb-6">
                    If <strong>{email}</strong> has an account, you&apos;ll receive a reset link shortly.
                    The link expires in 2 hours.
                  </p>
                  <Link
                    href="/"
                    className="inline-block text-sm text-teal hover:underline font-medium"
                  >
                    ← Back to CogniESL
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
