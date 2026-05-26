"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { AuthModal } from "@/components/AuthModal";
import { Navbar } from "@/components/Navbar";

const API_BASE = process.env.NEXT_PUBLIC_API_URL?.replace("/cogniesl/get_response", "") ?? "";

export default function SettingsPage() {
  const { user, loading, saveToken, logout } = useAuth();
  const router = useRouter();
  const [showAuth, setShowAuth] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState("");

  const handleDeleteAccount = async () => {
    if (deleteConfirm !== "DELETE") {
      setDeleteError("Type DELETE (all caps) to confirm.");
      return;
    }
    setDeleting(true);
    setDeleteError("");
    try {
      const token = localStorage.getItem("cogniesl_token");
      const res = await fetch(`${API_BASE}/api/auth/me`, {
        method: "DELETE",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) {
        logout?.();
        router.push("/");
      } else {
        setDeleteError("Something went wrong. Please try again.");
      }
    } catch {
      setDeleteError("Network error. Please try again.");
    } finally {
      setDeleting(false);
    }
  };

  const tierLabel: Record<string, string> = {
    free: "Free",
    pro: "Pro",
    founding_member: "Pro — Founding Member",
    school: "School",
  };

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />

      <main className="flex-1 max-w-xl mx-auto w-full px-4 py-8">
        <h1 className="text-2xl font-display font-bold text-gray-900 mb-6">Account Settings</h1>

        {/* Not logged in */}
        {!loading && !user && (
          <div className="text-center py-16">
            <p className="text-gray-500 mb-4">Sign in to manage your account.</p>
            <button
              onClick={() => setShowAuth(true)}
              className="bg-teal hover:bg-teal-dark text-white font-semibold px-6 py-2.5 rounded-xl text-sm transition-colors"
            >
              Sign In
            </button>
          </div>
        )}

        {/* Logged in */}
        {!loading && user && (
          <div className="space-y-6">

            {/* Account info */}
            <section className="bg-white border border-gray-200 rounded-2xl p-5">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Account</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Email</span>
                  <span className="text-sm font-medium text-gray-900">{user.email}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Member since</span>
                  <span className="text-sm text-gray-900">
                    {new Date(user.created_at).toLocaleDateString(undefined, {
                      month: "long", day: "numeric", year: "numeric",
                    })}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Plan</span>
                  <span className={`text-sm font-semibold ${user.subscription_tier === "free" ? "text-gray-500" : "text-teal"}`}>
                    {tierLabel[user.subscription_tier] ?? user.subscription_tier}
                  </span>
                </div>
              </div>
            </section>

            {/* Subscription */}
            <section className="bg-white border border-gray-200 rounded-2xl p-5">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Subscription</h2>
              {user.subscription_tier === "free" ? (
                <div>
                  <p className="text-sm text-gray-600 mb-4">
                    You&apos;re on the Free plan — 5 generations per month, slides only.
                    Upgrade to Pro for 20 generations, all 36 L1 languages, and worksheets + activity guides.
                  </p>
                  <a
                    href="/pricing"
                    className="inline-block bg-teal hover:bg-teal-dark text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
                  >
                    Upgrade to Pro →
                  </a>
                </div>
              ) : (
                <div>
                  <p className="text-sm text-gray-600 mb-4">
                    You&apos;re on the <strong>{tierLabel[user.subscription_tier]}</strong> plan.
                    To manage your subscription or update billing, contact us at{" "}
                    <a href="mailto:mitiro@gmail.com" className="text-teal underline">mitiro@gmail.com</a>.
                  </p>
                  <p className="text-xs text-gray-400">Stripe customer portal coming soon.</p>
                </div>
              )}
            </section>

            {/* Danger Zone */}
            <section className="bg-white border border-red-200 rounded-2xl p-5">
              <h2 className="text-sm font-semibold text-red-500 uppercase tracking-wide mb-4">Danger Zone</h2>
              <p className="text-sm text-gray-600 mb-4">
                Permanently delete your account and all your materials. This cannot be undone.
              </p>
              <div className="space-y-3">
                <input
                  type="text"
                  placeholder="Type DELETE to confirm"
                  value={deleteConfirm}
                  onChange={(e) => { setDeleteConfirm(e.target.value); setDeleteError(""); }}
                  className="w-full text-sm border border-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent"
                />
                {deleteError && (
                  <p className="text-xs text-red-500">{deleteError}</p>
                )}
                <button
                  onClick={handleDeleteAccount}
                  disabled={deleting || deleteConfirm !== "DELETE"}
                  className="w-full bg-red-600 hover:bg-red-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
                >
                  {deleting ? "Deleting…" : "Delete My Account Permanently"}
                </button>
              </div>
            </section>

          </div>
        )}
      </main>

      {showAuth && (
        <AuthModal
          onSuccess={(token, userData) => {
            saveToken(token, userData);
            setShowAuth(false);
          }}
          onClose={() => setShowAuth(false)}
        />
      )}
    </div>
  );
}
