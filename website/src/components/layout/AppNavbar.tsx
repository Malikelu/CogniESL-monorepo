"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { Sun, Moon } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { usePathname } from "next/navigation";

export function AppNavbar() {
  const { user, loading, isAuthenticated, logout } = useAuth();
  const pathname = usePathname();
  const [dark, setDark] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem("theme");
    const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const isDark = stored === "dark" || (!stored && systemDark);
    setDark(isDark);
    document.documentElement.classList.toggle("dark", isDark);
  }, []);

  const toggleDark = useCallback(() => {
    setDark((prev) => {
      const next = !prev;
      document.documentElement.classList.toggle("dark", next);
      localStorage.setItem("theme", next ? "dark" : "light");
      return next;
    });
  }, []);

  return (
    <header className="sticky top-0 z-50 bg-white dark:bg-neutral-950 border-b border-neutral-200 dark:border-neutral-800">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center" aria-label="CogniESL home">
            <img
              src="/logo-wordmark-light.svg"
              alt="CogniESL"
              height={28}
              className="h-[28px] w-auto hidden dark:hidden"
            />
            <img
              src="/logo-wordmark-dark.svg"
              alt="CogniESL"
              height={28}
              className="h-[28px] w-auto hidden dark:block"
            />
          </Link>

          <div className="hidden sm:flex items-center gap-8">
            <Link
              href="/app"
              className={`text-sm font-medium transition-colors ${
                pathname === "/app"
                  ? "text-primary-600 dark:text-primary-400"
                  : "text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100"
              }`}
            >
              Generator
            </Link>
            <Link
              href="/app/materials"
              className={`text-sm font-medium transition-colors ${
                pathname === "/app/materials"
                  ? "text-primary-600 dark:text-primary-400"
                  : "text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100"
              }`}
            >
              My Materials
            </Link>
            <Link
              href="/blog"
              className={`text-sm font-medium transition-colors ${
                pathname.startsWith("/blog")
                  ? "text-primary-600 dark:text-primary-400"
                  : "text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100"
              }`}
            >
              Blog
            </Link>
            <Link
              href="/pricing"
              className={`text-sm font-medium transition-colors ${
                pathname === "/pricing"
                  ? "text-primary-600 dark:text-primary-400"
                  : "text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100"
              }`}
            >
              Pricing
            </Link>
          </div>

          <div className="flex items-center gap-3">
            {mounted && (
              <button
                onClick={toggleDark}
                className="w-10 h-10 rounded-lg flex items-center justify-center text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-all duration-150 cursor-pointer"
                aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
              >
                {dark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
            )}
            {!loading && !isAuthenticated && (
              <>
                <Link
                  href="/app/signin"
                  className="text-sm font-medium text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors px-3 py-2"
                >
                  Sign In
                </Link>
                <Link
                  href="/app/register"
                  className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 shadow-glow hover:shadow-glow-lg px-4 py-2 text-sm"
                >
                  Get Started
                </Link>
              </>
            )}
            {!loading && isAuthenticated && user && (
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center text-primary-700 dark:text-primary-300 font-semibold text-xs">
                  {(user.name || user.email)[0].toUpperCase()}
                </span>
                <div className="hidden sm:block">
                  <p className="text-sm font-medium text-neutral-700 dark:text-neutral-300 max-w-[140px] truncate">
                    {user.name || user.email}
                  </p>
                  <p className="text-[10px] text-neutral-400 capitalize">{user.subscription_tier} plan</p>
                </div>
                <button
                  onClick={logout}
                  className="text-xs text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300 transition-colors"
                >
                  Sign out
                </button>
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}
