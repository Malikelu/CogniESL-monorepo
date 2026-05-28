"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";

const API_URL = "https://cogniesl-production.up.railway.app";

// ── Change this to redirect users somewhere else after logout ─────────────────
// Examples: "/blog", "/pricing", "https://cogniesl.com"
const LOGOUT_REDIRECT_URL = "/";

// Auto-logout after this many minutes of inactivity (mouse/keyboard idle)
const IDLE_TIMEOUT_MINUTES = 60;

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  subscription_tier: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
}

export function useAuth() {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    token: null,
    loading: true,
  });
  const idleTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearStorage = () => {
    localStorage.removeItem("cogniesl_token");
    localStorage.removeItem("cogniesl_user");
  };

  const logout = useCallback(() => {
    clearStorage();
    setState({ user: null, token: null, loading: false });
    router.push(LOGOUT_REDIRECT_URL);
  }, [router]);

  // Idle auto-logout: reset timer on any user activity
  useEffect(() => {
    if (typeof window === "undefined") return;

    const resetTimer = () => {
      if (idleTimer.current) clearTimeout(idleTimer.current);
      // Only arm the timer when a user is actually logged in
      setState((s) => {
        if (s.user) {
          idleTimer.current = setTimeout(() => {
            logout();
          }, IDLE_TIMEOUT_MINUTES * 60 * 1000);
        }
        return s;
      });
    };

    const events = ["mousemove", "mousedown", "keydown", "touchstart", "scroll"];
    events.forEach((e) => window.addEventListener(e, resetTimer, { passive: true }));
    resetTimer();

    return () => {
      events.forEach((e) => window.removeEventListener(e, resetTimer));
      if (idleTimer.current) clearTimeout(idleTimer.current);
    };
  }, [logout]);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const token = localStorage.getItem("cogniesl_token");
      const userStr = localStorage.getItem("cogniesl_user");
      if (token && userStr) {
        const user = JSON.parse(userStr) as User;
        fetch(`${API_URL}/api/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
          .then((res) => {
            if (res.ok) return res.json().then((data) => setState({ user: { ...user, ...data }, token, loading: false }));
            clearStorage();
            setState({ user: null, token: null, loading: false });
          })
          .catch(() => {
            setState({ user: null, token: null, loading: false });
          });
      } else {
        setState({ user: null, token: null, loading: false });
      }
    } catch {
      setState({ user: null, token: null, loading: false });
    }
  }, []);

  const saveToken = useCallback((token: string, user: User) => {
    localStorage.setItem("cogniesl_token", token);
    localStorage.setItem("cogniesl_user", JSON.stringify(user));
    setState({ user, token, loading: false });
  }, []);

  const register = useCallback(
    async (email: string, password: string, name: string): Promise<{ ok: boolean; error?: string }> => {
      try {
        const res = await fetch(`${API_URL}/api/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, name }),
        });
        const data = await res.json();
        if (!res.ok) return { ok: false, error: data.error || "Registration failed" };
        saveToken(data.token, data.user);
        return { ok: true };
      } catch {
        return { ok: false, error: "Network error. Please try again." };
      }
    },
    [saveToken]
  );

  const login = useCallback(
    async (email: string, password: string): Promise<{ ok: boolean; error?: string }> => {
      try {
        const res = await fetch(`${API_URL}/api/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });
        const data = await res.json();
        if (!res.ok) return { ok: false, error: data.error || "Login failed" };
        saveToken(data.token, data.user);
        return { ok: true };
      } catch {
        return { ok: false, error: "Network error. Please try again." };
      }
    },
    [saveToken]
  );

  return {
    user: state.user,
    token: state.token,
    loading: state.loading,
    isAuthenticated: !!state.user && !!state.token,
    saveToken,
    logout,
    register,
    login,
  };
}
