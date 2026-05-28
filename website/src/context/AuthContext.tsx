"use client";

import { createContext, useContext, useState, useEffect, useCallback, useRef, type ReactNode } from "react";
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

interface AuthContextValue extends AuthState {
  isAuthenticated: boolean;
  saveToken: (token: string, user: User) => void;
  logout: () => void;
  register: (email: string, password: string, name: string) => Promise<{ ok: boolean; error?: string }>;
  login: (email: string, password: string) => Promise<{ ok: boolean; error?: string }>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function clearStorage() {
  localStorage.removeItem("cogniesl_token");
  localStorage.removeItem("cogniesl_user");
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({ user: null, token: null, loading: true });
  const idleTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const logout = useCallback(() => {
    clearStorage();
    setState({ user: null, token: null, loading: false });
    router.push(LOGOUT_REDIRECT_URL);
  }, [router]);

  // Idle auto-logout
  useEffect(() => {
    if (typeof window === "undefined") return;
    const resetTimer = () => {
      if (idleTimer.current) clearTimeout(idleTimer.current);
      setState((s) => {
        if (s.user) {
          idleTimer.current = setTimeout(logout, IDLE_TIMEOUT_MINUTES * 60 * 1000);
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

  // Load from localStorage immediately — no loading flicker for returning users
  useEffect(() => {
    try {
      const token = localStorage.getItem("cogniesl_token");
      const userStr = localStorage.getItem("cogniesl_user");
      if (token && userStr) {
        const cached = JSON.parse(userStr) as User;
        setState({ user: cached, token, loading: false });
        fetch(`${API_URL}/api/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
          .then((res) => {
            if (res.ok) return res.json().then((data) => {
              const fresh = { ...cached, ...data };
              localStorage.setItem("cogniesl_user", JSON.stringify(fresh));
              setState({ user: fresh, token, loading: false });
            });
            clearStorage();
            setState({ user: null, token: null, loading: false });
          })
          .catch(() => { /* keep cached user on network error */ });
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

  const register = useCallback(async (email: string, password: string, name: string): Promise<{ ok: boolean; error?: string }> => {
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
  }, [saveToken]);

  const login = useCallback(async (email: string, password: string): Promise<{ ok: boolean; error?: string }> => {
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
  }, [saveToken]);

  return (
    <AuthContext.Provider value={{
      ...state,
      isAuthenticated: !!state.user && !!state.token,
      saveToken,
      logout,
      register,
      login,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
