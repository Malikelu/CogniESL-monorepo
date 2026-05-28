import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";

export const metadata = {
  title: "Cookie Policy — CogniESL",
  description: "CogniESL's cookie policy. Learn how we use cookies and similar technologies.",
};

export default function CookiePolicyPage() {
  return (
    <Section className="pt-28 lg:pt-32 pb-16">
      <Container size="md">
        <h1 className="font-heading text-3xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">Cookie Policy</h1>
        <p className="text-sm text-neutral-500 mb-8">Last updated: May 16, 2026</p>

        <div className="prose prose-neutral dark:prose-invert max-w-none">
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            This Cookie Policy explains how CogniESL uses cookies and similar technologies to recognize you when you visit our website.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">What Are Cookies?</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            Cookies are small data files placed on your device when you visit a website. They help the website remember your preferences and improve your experience.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">How We Use Cookies</h2>
          <ul className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4 list-disc pl-6 space-y-2">
            <li><strong>Essential Cookies:</strong> Required for the website to function properly (e.g., dark mode preference).</li>
            <li><strong>Analytics Cookies:</strong> Anonymous usage data to help us improve our service (if enabled).</li>
          </ul>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">Your Choices</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            You can control and delete cookies through your browser settings. Note that disabling cookies may affect website functionality.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">Changes to This Policy</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            We may update this Cookie Policy from time to time. Changes will be posted on this page.
          </p>
        </div>
      </Container>
    </Section>
  );
}
