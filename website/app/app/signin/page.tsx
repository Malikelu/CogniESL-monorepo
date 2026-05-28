"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Container } from "@/components/ui/Container";

export default function SignInPage() {
  const router = useRouter();
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Redirect if already logged in
  if (isAuthenticated) {
    router.push("/app");
    return null;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    const result = await login(email, password);
    if (result.ok) {
      router.push("/app");
    } else {
      setError(result.error || "Sign in failed");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center py-12">
      <Container size="sm">
        <div className="bg-white dark:bg-neutral-900 rounded-2xl border border-neutral-200 dark:border-neutral-800 p-8 shadow-card">
          <div className="text-center mb-8">
            <Link href="/" className="inline-flex items-center mb-6">
              <img
                src="/logo-wordmark-light.svg"
                alt="CogniESL"
                height={32}
                className="h-[32px] w-auto hidden dark:hidden"
              />
              <img
                src="/logo-wordmark-dark.svg"
                alt="CogniESL"
                height={32}
                className="h-[32px] w-auto hidden dark:block"
              />
            </Link>
            <h1 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">
              Welcome back
            </h1>
            <p className="text-neutral-500 dark:text-neutral-400 text-sm">
              Sign in to generate ESL teaching materials
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-secondary-50 dark:bg-secondary-900/20 border border-secondary-200 dark:border-secondary-800 text-secondary-700 dark:text-secondary-300 text-sm rounded-xl px-4 py-3">
                {error}
              </div>
            )}

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

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label htmlFor="password" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300">
                  Password
                </label>
                <Link href="/forgot-password" className="text-xs text-primary-600 dark:text-primary-400 hover:underline">
                  Forgot password?
                </Link>
              </div>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                placeholder="••••••••"
                className="w-full rounded-xl border border-neutral-300 dark:border-neutral-600 px-4 py-3 text-sm bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 shadow-glow hover:shadow-glow-lg px-6 py-3 text-base disabled:opacity-50"
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-neutral-500 dark:text-neutral-400">
            Don&apos;t have an account?{" "}
            <Link href="/app/register" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
              Create one
            </Link>
          </div>
        </div>
      </Container>
    </div>
  );
}
