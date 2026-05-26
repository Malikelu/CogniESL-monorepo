"use client";
import { useState } from "react";
import { AuthUser, API_BASE, TOKEN_KEY } from "@/hooks/useAuth";

interface Props {
  onSuccess: (token: string, user: AuthUser) => void;
  onClose: () => void;
}

export function AuthModal({ onSuccess, onClose }: Props) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (mode === "register" && !agreedToTerms) {
      setError("Please agree to the Terms of Service and Privacy Policy to create an account.");
      return;
    }
    setLoading(true);
    try {
      const endpoint = mode === "login" ? "/api/auth/login" : "/api/auth/register";
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      // Safely parse JSON — server may return HTML on unexpected 5xx errors
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let data: any = {};
      try { data = await res.json(); } catch (_e) { /* non-JSON response */ }
      if (!res.ok) {
        setError(data?.error || `Something went wrong (${res.status}). Please try again.`);
        return;
      }
      localStorage.setItem(TOKEN_KEY, data.token);
      onSuccess(data.token, data.user);
    } catch {
      setError("Could not connect to server. Please check your internet connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-sm mx-4 p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-lg font-bold text-gray-900">
              {mode === "login" ? "Sign in to CogniESL" : "Create your account"}
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              {mode === "login" ? "Access your saved materials" : "Free to get started"}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
              <path fillRule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        {/* Form */}
        <form onSubmit={submit} className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@school.com"
              required
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={mode === "register" ? "At least 8 characters" : ""}
              required
              minLength={mode === "register" ? 8 : undefined}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal focus:border-transparent"
            />
          </div>

          {mode === "register" && (
            <label className="flex items-start gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={agreedToTerms}
                onChange={(e) => { setAgreedToTerms(e.target.checked); setError(""); }}
                className="mt-0.5 accent-teal"
              />
              <span className="text-xs text-gray-500 leading-relaxed">
                I agree to the{" "}
                <a href="/terms" target="_blank" className="text-teal underline">Terms of Service</a>
                {" "}and{" "}
                <a href="/privacy" target="_blank" className="text-teal underline">Privacy Policy</a>
              </span>
            </label>
          )}

          {error && (
            <p className="text-xs text-red-600 bg-red-50 rounded-lg px-3 py-2">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading || (mode === "register" && !agreedToTerms)}
            className="w-full bg-teal hover:bg-teal-dark text-white font-semibold rounded-xl py-2.5 text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Please wait…" : mode === "login" ? "Sign In" : "Create Account"}
          </button>
        </form>

        {/* Forgot password (login mode only) */}
        {mode === "login" && (
          <p className="text-center text-xs text-gray-400 mt-3">
            <a href="/forgot-password" className="hover:text-teal hover:underline transition-colors">
              Forgot your password?
            </a>
          </p>
        )}

        {/* Toggle mode */}
        <p className="text-center text-xs text-gray-500 mt-3">
          {mode === "login" ? (
            <>Don&apos;t have an account?{" "}
              <button onClick={() => { setMode("register"); setError(""); }} className="text-teal font-medium hover:underline">
                Create one
              </button>
            </>
          ) : (
            <>Already have an account?{" "}
              <button onClick={() => { setMode("login"); setError(""); }} className="text-teal font-medium hover:underline">
                Sign in
              </button>
            </>
          )}
        </p>
      </div>
    </div>
  );
}
