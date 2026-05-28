"use client";

import { useState } from "react";

export function PricingToggle({ isSticky = false }: { isSticky?: boolean }) {
  const [annual, setAnnual] = useState(false);

  return (
    <div className={`flex justify-center mb-8 ${isSticky ? "sticky top-20 z-10 py-3 bg-neutral-50/95 dark:bg-neutral-950/95 backdrop-blur-sm" : ""}`}>
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
  );
}
