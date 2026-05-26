"use client";
import { useState, useEffect, useCallback } from "react";

export interface AuthUser {
  id: string;
  email: string;
  created_at: string;
  subscription_tier: string;
}

const TOKEN_KEY = "cogniesl_token";
const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace("/cogniesl/get_response", "") ?? "";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMe = useCallback(async (token: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.status === 401) {
        // Token is genuinely invalid/expired — clear it.
        localStorage.removeItem(TOKEN_KEY);
        setUser(null);
        return;
      }
      if (!res.ok) {
        // Server error (5xx) or network hiccup — keep the token, just show as logged out
        // temporarily. Don't destroy a valid token because the server is temporarily down.
        setUser(null);
        return;
      }
      const data = await res.json();
      setUser(data);
    } catch {
      // Network error — keep the token, user may regain connectivity.
      setUser(null);
    }
  }, []);

  useEffect(() => {
    const token = getToken();
    if (token) {
      fetchMe(token).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [fetchMe]);

  const saveToken = useCallback((token: string, userData: AuthUser) => {
    localStorage.setItem(TOKEN_KEY, token);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
  }, []);

  return { user, loading, saveToken, logout, getToken };
}

export { getToken, TOKEN_KEY, API_BASE };
