"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";

const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace("/cogniesl/get_response", "") ?? "";

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token") ?? "";

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (!token) setError("Invalid or missing reset link. Please request a new one.");
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? "Something went wrong. Please request a new link.");
        return;
      }
      setSuccess(true);
      setTimeout(() => router.push("/"), 3000);
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-sm">
      <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
        {success ? (
          <div className="text-center">
            <div className="text-4xl mb-4">✅</div>
            <h1 className="text-xl font-display font-bold text-gray-900 mb-2">Password updated!</h1>
            <p className="text-sm text-gray-500">Redirecting you to CogniESL…</p>
          </div>
        ) : (
          <>
            <h1 className="text-xl font-display font-bold text-gray-900 mb-2">Set a new password</h1>
            <p className="text-sm text-gray-500 mb-6">Choose a strong password with at least 8 characters.</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="password"
                placeholder="New password"
                value={password}
                onChange={(e) => { setPassword(e.target.value); setError(""); }}
                required
                minLength={8}
                className="w-full text-sm border border-gray-300 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
              />
              <input
                type="password"
                placeholder="Confirm new password"
                value={confirm}
                onChange={(e) => { setConfirm(e.target.value); setError(""); }}
                required
                className="w-full text-sm border border-gray-300 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
              />
              {error && <p className="text-xs text-red-500">{error}</p>}
              <button
                type="submit"
                disabled={loading || !token}
                className="w-full bg-teal hover:bg-teal-dark disabled:opacity-60 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
              >
                {loading ? "Updating…" : "Update password"}
              </button>
            </form>
            <p className="text-center text-xs text-gray-400 mt-5">
              Need a new link?{" "}
              <Link href="/forgot-password" className="text-teal hover:underline">Request again</Link>
            </p>
          </>
        )}
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />
      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <Suspense fallback={<div className="text-sm text-gray-400">Loading…</div>}>
          <ResetPasswordForm />
        </Suspense>
      </main>
    </div>
  );
}
