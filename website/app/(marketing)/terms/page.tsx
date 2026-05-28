import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";

export const metadata = {
  title: "Terms of Service — CogniESL",
  description: "CogniESL's terms of service. Read our terms and conditions for using our website and services.",
};

export default function TermsPage() {
  return (
    <Section className="pt-28 lg:pt-32 pb-16">
      <Container size="md">
        <h1 className="font-heading text-3xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">Terms of Service</h1>
        <p className="text-sm text-neutral-500 mb-8">Last updated: May 16, 2026</p>

        <div className="prose prose-neutral dark:prose-invert max-w-none">
          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">1. Acceptance of Terms</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            By accessing and using CogniESL (&quot;the Service&quot;), you accept and agree to be bound by the terms and provisions of this agreement.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">2. Description of Service</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            CogniESL is an AI-powered web application that helps ESL teachers generate custom teaching materials including PowerPoint slide decks, worksheets, and activity guides. The service includes L1 interference intelligence for 36 languages.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">3. User Accounts</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            When you create an account, you agree to provide accurate and complete information. You are responsible for maintaining the confidentiality of your account credentials and for all activities under your account.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">4. Acceptable Use</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            You agree to use the Service only for lawful purposes and in accordance with these Terms. You may not:
          </p>
          <ul className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4 list-disc pl-6 space-y-2">
            <li>Use the Service to generate content that is harmful, discriminatory, or inappropriate for educational settings</li>
            <li>Attempt to reverse-engineer, decompile, or disassemble any part of the Service</li>
            <li>Share your account credentials with others</li>
            <li>Use automated systems to access the Service without our permission</li>
          </ul>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">5. Intellectual Property</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            The Service and its original content, features, and functionality are owned by CogniESL and are protected by international copyright, trademark, and other intellectual property laws. Materials generated through the Service are yours to use for educational purposes.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">6. AI-Generated Content</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            CogniESL uses artificial intelligence to generate teaching materials. While we strive for accuracy, AI-generated content may contain errors. We recommend reviewing all materials before classroom use. CogniESL is not responsible for the accuracy of AI-generated content.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">7. Limitation of Liability</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            CogniESL is provided on an &quot;as is&quot; and &quot;as available&quot; basis. We do not warrant that the Service will be uninterrupted, error-free, or free of harmful components. In no event shall CogniESL be liable for any indirect, incidental, special, or consequential damages.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">8. Changes to Terms</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            We reserve the right to modify these Terms at any time. We will notify users of significant changes by posting the updated Terms on this page.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">9. Contact</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            For questions about these Terms, contact us at legal@cogniesl.com.
          </p>
        </div>
      </Container>
    </Section>
  );
}
