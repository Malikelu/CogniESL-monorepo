"use client";
import { Container } from "@/components/ui/Container";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import Link from "next/link";

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    description: "Try CogniESL with real L1 intelligence. No credit card required.",
    features: [
      "5 generations per month",
      "5 L1 languages (Spanish, Mandarin, French, Arabic, Portuguese)",
      "Slides format only",
      "Subtle footer watermark",
      "Email delivery",
    ],
    cta: "Start Free",
    variant: "outline" as const,
    popular: false,
  },
  {
    name: "Pro",
    priceMonthly: "$12",
    priceAnnually: "$9",
    period: "/month",
    description: "For individual ESL teachers who want full L1 coverage and all material formats.",
    features: [
      "20 generations per month",
      "All 36 L1 languages",
      "All 3 formats: slides + worksheet + activity guide",
      "All proficiency levels (A1–C1)",
      "Priority generation queue",
      "No watermark",
      "My Materials library (coming soon)",
    ],
    cta: "Join Waitlist",
    variant: "primary" as const,
    popular: true,
  },
  {
    name: "School",
    price: "Custom",
    period: "",
    description: "For language programs and schools. Volume pricing, admin dashboard, and multi-teacher accounts.",
    features: [
      "Everything in Pro",
      "Multi-teacher accounts",
      "Admin usage dashboard",
      "Invoice / PO billing",
      "Dedicated onboarding call",
      "Priority support",
    ],
    cta: "Contact Us",
    variant: "outline" as const,
    popular: false,
    comingSoon: true,
  },
];

export function Pricing() {
  const [annual, setAnnual] = useState(false);

  return (
    <section id="pricing" className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-950">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full bg-accent-100 dark:bg-accent-900/30 text-accent-700 dark:text-accent-300 text-sm font-semibold mb-4">
            Pricing
          </span>
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            Start free.{" "}
            <span className="gradient-text">Less than a coffee per week.</span>
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed mb-8">
            No hidden fees. No annual lock-in. Cancel anytime.
            And if you&apos;re in the first 100 — you get Pro pricing locked forever.
          </p>

          {/* Annual toggle */}
          <div className="inline-flex items-center gap-3 bg-neutral-100 dark:bg-neutral-800 rounded-full p-1">
            <button
              onClick={() => setAnnual(false)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                !annual
                  ? "bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-sm"
                  : "text-neutral-500 dark:text-neutral-400"
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setAnnual(true)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                annual
                  ? "bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-sm"
                  : "text-neutral-500 dark:text-neutral-400"
              }`}
            >
              Annual{" "}
              <span className="text-success-600 dark:text-success-400 text-xs font-bold">Save 25%</span>
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-5 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl p-7 border transition-all duration-300 ${
                plan.popular
                  ? "bg-white dark:bg-neutral-900 border-primary-500 shadow-glow-lg scale-[1.02] z-10"
                  : "bg-white dark:bg-neutral-900 border-neutral-200/80 dark:border-neutral-800"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-primary-500 text-white text-xs font-semibold rounded-full">
                  Most Popular
                </div>
              )}
              {plan.comingSoon && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-neutral-400 text-white text-xs font-semibold rounded-full">
                  Coming Soon
                </div>
              )}

              <h3 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-1">
                {plan.name}
              </h3>

              <div className="flex items-baseline gap-1 mb-1">
                <span className="font-heading text-4xl font-bold text-neutral-900 dark:text-neutral-50">
                  {plan.name === "Pro"
                    ? annual
                      ? plan.priceAnnually
                      : plan.priceMonthly
                    : plan.price}
                </span>
                {plan.period && (
                  <span className="text-neutral-500 dark:text-neutral-400 text-sm">{plan.period}</span>
                )}
              </div>

              {plan.name === "Pro" && annual && (
                <p className="text-xs text-success-600 dark:text-success-400 font-medium mb-2">
                  Billed annually (${Number(plan.priceAnnually) * 12}/year)
                </p>
              )}
              {plan.name === "Pro" && !annual && (
                <p className="text-xs text-neutral-400 mb-2">
                  or ${Number(plan.priceAnnually) * 12}/year billed annually
                </p>
              )}

              <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-6">{plan.description}</p>

              <Button variant={plan.variant} className="w-full mb-6" asChild>
                <Link href="#waitlist">{plan.cta}</Link>
              </Button>

              <ul className="space-y-2.5">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-2.5 text-sm">
                    <svg className="w-4 h-4 text-success-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-neutral-600 dark:text-neutral-400">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Founding Member callout with progress bar */}
        <div className="max-w-2xl mx-auto mt-10 rounded-2xl bg-gradient-to-r from-accent-50 to-primary-50 dark:from-accent-900/20 dark:to-primary-900/20 border border-accent-200/60 dark:border-accent-800/40 p-6 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-100 dark:bg-accent-900/40 text-accent-700 dark:text-accent-300 text-xs font-semibold mb-4">
            🌟 Founding Member Offer
          </div>
          <p className="text-neutral-700 dark:text-neutral-300 text-sm leading-relaxed mb-4">
            <strong className="text-neutral-900 dark:text-neutral-100">First 100 subscribers get Pro at $7/mo billed annually — locked forever.</strong>{" "}
            Regular price will be $9/mo annual. This pricing closes permanently when all 100 spots fill.
          </p>
          {/* Progress bar */}
          <div className="max-w-sm mx-auto">
            <div className="flex justify-between text-xs text-neutral-500 dark:text-neutral-400 mb-1.5">
              <span className="font-semibold text-accent-600 dark:text-accent-400">47 spots claimed</span>
              <span>100 total</span>
            </div>
            <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2.5 overflow-hidden">
              <div
                className="bg-gradient-to-r from-accent-500 to-primary-500 h-2.5 rounded-full transition-all"
                style={{ width: "47%" }}
              />
            </div>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1.5">53 spots remaining at $7/mo</p>
          </div>
        </div>

        <div className="text-center mt-6">
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            🔒 14-day money-back guarantee · No questions asked · Cancel anytime
          </p>
        </div>
      </Container>
    </section>
  );
}
