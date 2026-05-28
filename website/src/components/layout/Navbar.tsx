"use client";

import { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { Menu, X, Sun, Moon, BookOpen, FileText, CreditCard, Info, Rss } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";

const navLinks = [
  { href: "/how-it-works", label: "How It Works", icon: BookOpen },
  { href: "/samples", label: "Samples", icon: FileText },
  { href: "/blog", label: "Blog", icon: Rss },
  { href: "/pricing", label: "Pricing", icon: CreditCard },
  { href: "/about", label: "About", icon: Info },
];

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [dark, setDark] = useState(false);
  const [mounted, setMounted] = useState(false);
  const { user, loading, isAuthenticated, logout } = useAuth();

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem("theme");
    const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const isDark = stored === "dark" || (!stored && systemDark);
    setDark(isDark);
    document.documentElement.classList.toggle("dark", isDark);
  }, []);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
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
    <header
      className={"sticky top-0 z-50 transition-all duration-200 " + (scrolled ? "bg-white/92 dark:bg-neutral-950/92 backdrop-blur-md shadow-sm border-b border-neutral-200 dark:border-neutral-800" : "bg-white/90 dark:bg-neutral-950/90 backdrop-blur-md")}
      role="banner"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between h-16" aria-label="Main navigation">
          <Link href="/" className="flex items-center shrink-0" aria-label="CogniESL home">
            <img src="/logo-wordmark-light.svg" alt="CogniESL" height={30} className="h-[30px] w-auto hidden dark:hidden" />
            <img src="/logo-wordmark-dark.svg" alt="CogniESL" height={30} className="h-[30px] w-auto hidden dark:block" />
          </Link>
          <div className="hidden lg:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className="text-sm font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors duration-150">
                {link.label}
              </Link>
            ))}
          </div>
          <div className="flex items-center gap-3">
            {mounted && (
              <button onClick={toggleDark} className="w-10 h-10 rounded-lg flex items-center justify-center text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-all duration-150 cursor-pointer" aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}>
                {dark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
            )}
            {!loading && !isAuthenticated && (
              <>
                <Link href="/app/signin" className="hidden sm:inline-flex text-sm font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors px-3 py-2">
                  Sign In
                </Link>
                <Button size="sm" className="hidden sm:inline-flex font-bold" asChild>
                  <Link href="/app/register">Get Started</Link>
                </Button>
              </>
            )}
            {!loading && isAuthenticated && user && (
              <>
                <Link href="/app" className="hidden sm:inline-flex text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 transition-colors px-3 py-2">
                  Generator
                </Link>
                <div className="hidden sm:flex items-center gap-2">
                  <span className="w-7 h-7 rounded-full bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center text-primary-700 dark:text-primary-300 font-semibold text-xs">
                    {(user.name || user.email)[0].toUpperCase()}
                  </span>
                  <button onClick={logout} className="text-xs text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300 transition-colors">
                    Sign out
                  </button>
                </div>
              </>
            )}
            <button onClick={() => setMobileOpen(!mobileOpen)} className="lg:hidden w-10 h-10 rounded-lg flex items-center justify-center text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-all duration-150 cursor-pointer" aria-label={mobileOpen ? "Close menu" : "Open menu"} aria-expanded={mobileOpen}>
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </nav>
      </div>
      {mobileOpen && (
        <div className="lg:hidden border-t border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4 space-y-1">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className="flex items-center gap-3 px-4 py-3 text-base text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-lg transition-colors duration-150" onClick={() => setMobileOpen(false)}>
                <link.icon className="w-5 h-5" />
                {link.label}
              </Link>
            ))}
            <div className="pt-4 px-4 space-y-2">
              {!isAuthenticated ? (
                <>
                  <Link href="/app/signin" className="block text-center text-sm font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 transition-colors px-4 py-2.5 rounded-xl border border-neutral-300 dark:border-neutral-600" onClick={() => setMobileOpen(false)}>
                    Sign In
                  </Link>
                  <Button className="w-full font-bold" asChild>
                    <Link href="/app/register" onClick={() => setMobileOpen(false)}>Get Started</Link>
                  </Button>
                </>
              ) : (
                <>
                  <Link href="/app" className="block text-center text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 transition-colors px-4 py-2.5 rounded-xl border border-primary-300 dark:border-primary-700" onClick={() => setMobileOpen(false)}>
                    Generator
                  </Link>
                  <button onClick={() => { logout(); setMobileOpen(false); }} className="w-full text-center text-sm text-neutral-400 hover:text-neutral-600 transition-colors px-4 py-2">
                    Sign out
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
