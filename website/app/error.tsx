"use client";

import { useEffect } from "react";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    console.error("Page error:", error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50 dark:bg-neutral-950 px-4">
      <div className="text-center max-w-md">
        <div className="text-5xl mb-4">😕</div>
        <h1 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">
          Something went wrong
        </h1>
        <p className="text-neutral-600 dark:text-neutral-400 mb-6 text-sm">
          We&apos;re sorry, but something unexpected happened. Please try again.
        </p>
        <button
          onClick={reset}
          className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 px-6 py-3"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
