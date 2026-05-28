"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { MessageSquare } from "lucide-react";

export function ContactForm() {
  const [submitted, setSubmitted] = useState(false);

  return submitted ? (
    <div className="text-center py-12">
      <div className="w-16 h-16 rounded-full bg-primary-50 dark:bg-primary-950 flex items-center justify-center mx-auto mb-4">
        <MessageSquare className="w-8 h-8 text-primary-500" />
      </div>
      <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">Message sent!</h2>
      <p className="text-neutral-600 dark:text-neutral-400">We&apos;ll get back to you within 24 hours.</p>
    </div>
  ) : (
    <form
      onSubmit={(e) => { e.preventDefault(); setSubmitted(true); }}
      className="space-y-6"
    >
      <div className="grid sm:grid-cols-2 gap-4">
        <Input id="name" label="Name" placeholder="Your name" required />
        <Input id="email" label="Email" type="email" placeholder="you@school.edu" required />
      </div>
      <Input id="subject" label="Subject" placeholder="What&apos;s this about?" required />
      <div>
        <label htmlFor="message" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Message</label>
        <textarea
          id="message"
          rows={6}
          required
          placeholder="Tell us what&apos;s on your mind..."
          className="w-full px-4 py-3 rounded-xl border border-neutral-300 dark:border-neutral-600 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100 placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 resize-none"
        />
      </div>
      <Button type="submit" size="lg" className="w-full">
        Send Message
      </Button>
    </form>
  );
}
