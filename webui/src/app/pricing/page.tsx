"use client";
import Link from "next/link";
import { useState, useEffect } from "react";
import { Navbar } from "@/components/Navbar";

interface FoundingStatus {
  slots_used: number;
  slots_total: number;
}

export default function PricingPage() {
  const [annual, setAnnual] = useState(true);
  const [founding, setFounding] = useState<FoundingStatus | null>(null);
  const [loadingCheckout, setLoadingCheckout] = useState<string | null>(null);
  const [checkoutError, setCheckoutError] = useState("");

  useEffect(() => {
    fetch("/api/stripe/founding-member-status")
      .then((r) => r.json())
      .then((d) => setFounding(d))
      .catch(() => {});
  }, []);

  const slotsRemaining = founding
    ? founding.slots_total - founding.slots_used
    : null;
  const foundingFull = slotsRemaining !== null && slotsRemaining <= 0;

  async function handleCheckout(priceKey: string) {
    setCheckoutError("");
    setLoadingCheckout(priceKey);
    const token =
      typeof window !== "undefined" ? localStorage.getItem("cogniesl_token") : null;
    if (!token) {
      // Redirect to sign-in — they'll need an account first
      window.location.href = "/?signup=1";
      return;
    }
    try {
      const priceId = getPriceId(priceKey);
      if (!priceId) {
        setCheckoutError("Stripe price not configured yet. Please try again soon.");
        setLoadingCheckout(null);
        return;
      }
      const res = await fetch("/api/stripe/create-checkout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ price_id: priceId }),
      });
      const data = await res.json();
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        setCheckoutError(data.error || "Something went wrong. Please try again.");
      }
    } catch {
      setCheckoutError("Network error. Please check your connection and try again.");
    } finally {
      setLoadingCheckout(null);
    }
  }

  function getPriceId(key: string): string {
    // These are read from the page's meta or env at build time.
    // In production they are set via Railway env vars passed to Next.js at build.
    const ids: Record<string, string> = {
      pro_monthly: process.env.NEXT_PUBLIC_STRIPE_PRO_MONTHLY_PRICE_ID || "",
      pro_annual: process.env.NEXT_PUBLIC_STRIPE_PRO_ANNUAL_PRICE_ID || "",
      founding: process.env.NEXT_PUBLIC_STRIPE_FOUNDING_PRICE_ID || "",
    };
    return ids[key] || "";
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />

      <main className="flex-1 px-4 py-12">
        {/* Header */}
        <div className="max-w-3xl mx-auto text-center mb-10">
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-3">
            Simple, honest pricing
          </h1>
          <p className="text-lg text-gray-500">
            Generate professional ESL materials in minutes. Cancel any time.
          </p>

          {/* Annual / Monthly toggle */}
          <div className="mt-6 inline-flex items-center gap-3 bg-gray-100 rounded-full px-2 py-1">
            <button
              onClick={() => setAnnual(false)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                !annual ? "bg-white shadow text-gray-900" : "text-gray-500 hover:text-gray-700"
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setAnnual(true)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                annual ? "bg-white shadow text-gray-900" : "text-gray-500 hover:text-gray-700"
              }`}
            >
              Annual
              <span className="ml-1.5 text-xs text-teal font-semibold">Save 25%</span>
            </button>
          </div>
        </div>

        {/* Cards */}
        <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">

          {/* Free */}
          <div className="bg-white border border-gray-200 rounded-2xl p-7 flex flex-col">
            <div className="mb-4">
              <span className="text-xs font-semibold uppercase tracking-widest text-gray-400">Free</span>
              <div className="mt-2 flex items-end gap-1">
                <span className="text-4xl font-bold text-gray-900">$0</span>
                <span className="text-gray-400 mb-1">/ month</span>
              </div>
              <p className="mt-2 text-sm text-gray-500">
                Try the product — no credit card required.
              </p>
            </div>

            <ul className="space-y-2.5 text-sm text-gray-600 flex-1">
              <FeatureLine>5 generations per month</FeatureLine>
              <FeatureLine>5 native languages (L1s)</FeatureLine>
              <FeatureLine>Slides only (no worksheet / activity guide)</FeatureLine>
              <FeatureLine>Email delivery</FeatureLine>
            </ul>

            <div className="mt-6">
              <Link
                href="/"
                className="block w-full text-center rounded-xl border border-gray-300 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
              >
                Get started free
              </Link>
            </div>
          </div>

          {/* Pro */}
          <div className="bg-white border-2 border-teal rounded-2xl p-7 flex flex-col relative shadow-lg">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2">
              <span className="bg-teal text-white text-xs font-semibold px-3 py-1 rounded-full">
                Most popular
              </span>
            </div>

            <div className="mb-4">
              <span className="text-xs font-semibold uppercase tracking-widest text-teal">Pro</span>
              <div className="mt-2 flex items-end gap-1">
                <span className="text-4xl font-bold text-gray-900">
                  ${annual ? "9" : "12"}
                </span>
                <span className="text-gray-400 mb-1">/ month</span>
              </div>
              {annual && (
                <p className="text-xs text-gray-400 mt-0.5">billed $108/year</p>
              )}
              <p className="mt-2 text-sm text-gray-500">
                For teachers who generate materials regularly.
              </p>
            </div>

            <ul className="space-y-2.5 text-sm text-gray-600 flex-1">
              <FeatureLine highlight>20 generations per month</FeatureLine>
              <FeatureLine highlight>All 36 native languages</FeatureLine>
              <FeatureLine highlight>Slides + Worksheet + Activity Guide</FeatureLine>
              <FeatureLine highlight>Email delivery</FeatureLine>
              <FeatureLine highlight>Priority support</FeatureLine>
            </ul>

            <div className="mt-6">
              <button
                onClick={() => handleCheckout(annual ? "pro_annual" : "pro_monthly")}
                disabled={loadingCheckout !== null}
                className="block w-full text-center rounded-xl bg-teal text-white py-2.5 text-sm font-semibold hover:bg-teal-dark transition-colors disabled:opacity-60"
              >
                {loadingCheckout === "pro_annual" || loadingCheckout === "pro_monthly"
                  ? "Redirecting…"
                  : "Start Pro →"}
              </button>
            </div>
          </div>

          {/* Founding Member */}
          <div
            className={`rounded-2xl p-7 flex flex-col relative ${
              foundingFull
                ? "bg-gray-50 border border-gray-200 opacity-70"
                : "bg-amber-50 border-2 border-amber-400"
            }`}
          >
            {!foundingFull && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <span className="bg-amber-400 text-white text-xs font-semibold px-3 py-1 rounded-full">
                  🔥 Limited offer
                </span>
              </div>
            )}

            <div className="mb-4">
              <span className="text-xs font-semibold uppercase tracking-widest text-amber-600">
                Founding Member
              </span>
              <div className="mt-2 flex items-end gap-1">
                <span className="text-4xl font-bold text-gray-900">$7</span>
                <span className="text-gray-400 mb-1">/ month</span>
              </div>
              <p className="text-xs text-gray-400 mt-0.5">billed $84/year · locked in forever</p>
              <p className="mt-2 text-sm text-gray-600">
                First 100 members only. Everything in Pro, permanently at this price.
              </p>
            </div>

            {/* Slot counter */}
            <div className="mb-4">
              {founding ? (
                <div>
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>{slotsRemaining} slots remaining</span>
                    <span>{founding.slots_used} / {founding.slots_total} taken</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-amber-400 rounded-full transition-all"
                      style={{
                        width: `${(founding.slots_used / founding.slots_total) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ) : (
                <div className="h-2 bg-gray-200 rounded-full animate-pulse" />
              )}
            </div>

            <ul className="space-y-2.5 text-sm text-gray-600 flex-1">
              <FeatureLine highlight>Everything in Pro</FeatureLine>
              <FeatureLine highlight>Price locked in for life</FeatureLine>
              <FeatureLine highlight>Founding Member badge</FeatureLine>
              <FeatureLine highlight>Input on new features</FeatureLine>
            </ul>

            <div className="mt-6">
              {foundingFull ? (
                <div className="block w-full text-center rounded-xl border border-gray-300 py-2.5 text-sm font-medium text-gray-400">
                  All slots filled
                </div>
              ) : (
                <button
                  onClick={() => handleCheckout("founding")}
                  disabled={loadingCheckout !== null}
                  className="block w-full text-center rounded-xl bg-amber-400 text-white py-2.5 text-sm font-semibold hover:bg-amber-500 transition-colors disabled:opacity-60"
                >
                  {loadingCheckout === "founding" ? "Redirecting…" : "Claim Founding Member →"}
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Error message */}
        {checkoutError && (
          <div className="max-w-xl mx-auto mt-6 text-center">
            <p className="text-sm text-red-500">{checkoutError}</p>
          </div>
        )}

        {/* FAQ */}
        <div className="max-w-2xl mx-auto mt-16 space-y-6">
          <h2 className="text-xl font-semibold text-gray-900 text-center mb-8">
            Frequently asked questions
          </h2>
          <FAQ q="Can I try before I pay?">
            Yes. The free plan gives you 5 generations per month with no credit card required.
            Upgrade any time when you're ready.
          </FAQ>
          <FAQ q="What happens when I hit my limit?">
            For free users, you'll be prompted to upgrade. Pro users get 20 generations per
            month — enough for any active teacher.
          </FAQ>
          <FAQ q="What formats do I get?">
            Pro users get a PowerPoint slide deck (PPTX), a student worksheet (PDF), and a
            teacher activity guide (PDF) — all generated from the same request. Free users
            receive the slide deck only.
          </FAQ>
          <FAQ q="Can I cancel?">
            Yes, any time. Cancel from your account settings and you keep access until the end
            of your billing period. No questions asked.
          </FAQ>
          <FAQ q="What is a Founding Member?">
            The first 100 subscribers who lock in the $7/month rate forever — even as the
            price increases for new subscribers. It's our way of rewarding early supporters.
          </FAQ>
          <FAQ q="How is payment handled?">
            Payments are processed securely by Stripe. We never see or store your card details.
          </FAQ>
        </div>
      </main>

      <footer className="border-t border-gray-200 py-6 mt-12">
        <div className="max-w-4xl mx-auto px-4 flex gap-4 text-xs text-gray-400 justify-center">
          <Link href="/privacy" className="hover:text-gray-600">Privacy Policy</Link>
          <Link href="/terms" className="hover:text-gray-600">Terms of Service</Link>
          <Link href="/" className="hover:text-gray-600">← Back to CogniESL</Link>
        </div>
      </footer>
    </div>
  );
}

function FeatureLine({
  children,
  highlight,
}: {
  children: React.ReactNode;
  highlight?: boolean;
}) {
  return (
    <li className="flex items-start gap-2">
      <span className={`mt-0.5 flex-shrink-0 ${highlight ? "text-teal" : "text-gray-400"}`}>
        ✓
      </span>
      <span>{children}</span>
    </li>
  );
}

function FAQ({ q, children }: { q: string; children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b border-gray-200 pb-4">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center text-left text-sm font-medium text-gray-800 hover:text-gray-900"
      >
        {q}
        <span className="ml-4 text-gray-400">{open ? "−" : "+"}</span>
      </button>
      {open && <p className="mt-2 text-sm text-gray-500">{children}</p>}
    </div>
  );
}
