const API_URL = "https://cogniesl-production.up.railway.app";

export function getAuthToken(): string | null {
  try {
    return localStorage.getItem("cogniesl_token");
  } catch {
    return null;
  }
}

export function getSessionId(): string {
  if (typeof window === "undefined") return "server";
  let id = localStorage.getItem("cogniesl_session_id");
  if (!id) {
    id = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
    localStorage.setItem("cogniesl_session_id", id);
  }
  return id;
}

function getHeaders(): Record<string, string> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  headers["X-Session-ID"] = getSessionId();
  const token = getAuthToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

// ─── Auth ─────────────────────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  created_at: string;
  subscription_tier: string;
}

export async function apiRegister(email: string, password: string): Promise<{ ok: boolean; token?: string; user?: User; error?: string }> {
  const res = await fetch(`${API_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  if (!res.ok) return { ok: false, error: data.error || "Registration failed" };
  return { ok: true, token: data.token, user: data.user };
}

export async function apiLogin(email: string, password: string): Promise<{ ok: boolean; token?: string; user?: User; error?: string }> {
  const res = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  if (!res.ok) return { ok: false, error: data.error || "Login failed" };
  return { ok: true, token: data.token, user: data.user };
}

export async function apiMe(): Promise<User | null> {
  const token = getAuthToken();
  if (!token) return null;
  const res = await fetch(`${API_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  return res.json();
}

export async function apiUsage(): Promise<{ monthly_generations: number; tier_limit: number; subscription_tier: string } | null> {
  const token = getAuthToken();
  if (!token) return null;
  const res = await fetch(`${API_URL}/api/auth/usage`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  return res.json();
}

export interface UserStats {
  total_generations: number;
  hours_saved: number;
  languages_taught: string[];
  languages_count: number;
  member_since: string;
}

export async function apiStats(): Promise<UserStats | null> {
  const token = getAuthToken();
  if (!token) return null;
  const res = await fetch(`${API_URL}/api/auth/stats`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  return res.json();
}

// ─── Chat ─────────────────────────────────────────────────────────────────────

export async function apiChat(message: string): Promise<{ response: string }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 1_800_000); // 30 min

  const res = await fetch(`${API_URL}/cogniesl/get_response`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ message }),
    signal: controller.signal,
  });

  clearTimeout(timeout);

  if (!res.ok) throw new Error(`Server responded with ${res.status}`);
  const data = await res.json();
  return { response: data.response || "" };
}

// ─── Jobs ─────────────────────────────────────────────────────────────────────

export interface Job {
  job_id: string;
  status: "pending" | "done" | "error";
  email: string;
  project_name: string;
  grammar_point: string;
  l1_languages: string;
  age_group: string;
  formats: string[];
  file_paths: string[];
  created_at: string;
  completed_at: string;
  error: string;
}

export async function apiJobStatus(jobId: string): Promise<Job | null> {
  const res = await fetch(`${API_URL}/api/jobs/${jobId}`);
  if (!res.ok) return null;
  return res.json();
}

export function getDownloadUrl(jobId: string, filename: string): string {
  return `${API_URL}/download/${jobId}/${filename}`;
}
