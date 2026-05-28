import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";

export const metadata = {
  title: "Privacy Policy — CogniESL",
  description: "CogniESL's privacy policy. Learn how we collect, use, and protect your data.",
};

export default function PrivacyPage() {
  return (
    <Section className="pt-28 lg:pt-32 pb-16">
      <Container size="md">
        <h1 className="font-heading text-3xl font-bold text-neutral-900 dark:text-neutral-50 mb-2">Privacy Policy</h1>
        <p className="text-sm text-neutral-500 mb-8">Last updated: May 16, 2026</p>

        <div className="prose prose-neutral dark:prose-invert max-w-none">
          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">1. Introduction</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            CogniESL (&quot;we,&quot; &quot;our,&quot; or &quot;us&quot;) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your information when you use our website and services.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">2. Information We Collect</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            <strong>Waitlist Signup:</strong> When you join our waitlist, we collect your email address. This is the only personal information we collect at this time.
          </p>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            <strong>Usage Data:</strong> We may collect anonymous usage data through privacy-friendly analytics to understand how visitors use our site. This data is aggregated and cannot be used to identify individual users.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">3. How We Use Your Information</h2>
          <ul className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4 list-disc pl-6 space-y-2">
            <li>To notify you when CogniESL launches</li>
            <li>To send you updates about our product (only if you opt in)</li>
            <li>To improve our website and services based on usage patterns</li>
          </ul>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">4. Student Data &amp; FERPA Compliance</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            CogniESL does not collect, store, or process any student personal information. Teachers describe their teaching needs in general terms (e.g., &quot;Spanish-speaking beginners, present perfect&quot;), and no student data is ever transmitted to our systems. We are fully FERPA compliant.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">5. Data Security</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">6. Third-Party Services</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            We do not sell, trade, or transfer your personal information to third parties. We may use trusted service providers to help us operate our website, subject to confidentiality agreements.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">7. Your Rights</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            You have the right to access, correct, or delete your personal information at any time. To exercise these rights, contact us at privacy@cogniesl.com.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">8. Changes to This Policy</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the &quot;Last updated&quot; date.
          </p>

          <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mt-8 mb-3">9. Contact Us</h2>
          <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
            If you have any questions about this Privacy Policy, please contact us at privacy@cogniesl.com.
          </p>
        </div>
      </Container>
    </Section>
  );
}
