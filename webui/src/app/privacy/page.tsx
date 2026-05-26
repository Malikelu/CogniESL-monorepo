"use client";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";

export default function PrivacyPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />
      <main className="flex-1 max-w-2xl mx-auto w-full px-4 py-10">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-2">Privacy Policy</h1>
        <p className="text-sm text-gray-400 mb-8">Last updated: May 2026</p>

        <div className="prose prose-sm text-gray-700 space-y-6">

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">1. Who We Are</h2>
            <p>CogniESL (&ldquo;we&rdquo;, &ldquo;our&rdquo;, &ldquo;us&rdquo;) is a service that generates ESL teaching materials. We are operated by Marcos Itiro. Contact: <a href="mailto:mitiro@gmail.com" className="text-teal underline">mitiro@gmail.com</a></p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">2. What Data We Collect</h2>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>Account data:</strong> Your email address and hashed password when you register.</li>
              <li><strong>Usage data:</strong> Grammar topics requested, native languages selected, formats generated, and timestamps. We do not store the full text of your generated materials on our servers indefinitely.</li>
              <li><strong>Files:</strong> Generated PPTX, PDF, and HTML files are stored on our server temporarily so you can download them. Files may be deleted after 30 days or on service redeploys.</li>
              <li><strong>Analytics:</strong> We use Plausible Analytics (privacy-friendly, no cookies, no cross-site tracking) to understand which pages are visited.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">3. How We Use Your Data</h2>
            <ul className="list-disc list-inside space-y-1">
              <li>To provide and improve the CogniESL service.</li>
              <li>To send you your generated materials by email (via Resend).</li>
              <li>To enforce usage limits on your account tier.</li>
              <li>We do not sell your data. We do not use your data for advertising.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">4. Third-Party Services</h2>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>Resend</strong> — Email delivery. Your email address is shared with Resend solely to send you materials and transactional messages.</li>
              <li><strong>Stripe</strong> — Payment processing. We never store your payment card details. Stripe handles all payment data under their own privacy policy.</li>
              <li><strong>Railway</strong> — Hosting provider. Our server runs on Railway infrastructure.</li>
              <li><strong>Plausible Analytics</strong> — Privacy-friendly website analytics. No cookies. No personal data collected.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">5. Data Retention</h2>
            <p>We keep your account data for as long as your account is active. Generated material files are kept on our server for up to 30 days. You can delete your account at any time from <Link href="/settings" className="text-teal underline">Account Settings</Link>, which permanently removes all your data.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">6. Your Rights</h2>
            <p>You have the right to access, correct, or delete your personal data at any time. To delete your account and all associated data, use the &ldquo;Delete Account&rdquo; button in <Link href="/settings" className="text-teal underline">Settings</Link>. For other requests, email <a href="mailto:mitiro@gmail.com" className="text-teal underline">mitiro@gmail.com</a>.</p>
            <p className="mt-2">If you are in the European Union, you also have rights under GDPR, including the right to data portability and the right to lodge a complaint with your local supervisory authority.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">7. Cookies</h2>
            <p>CogniESL does not use tracking cookies. We use your browser&apos;s localStorage solely to keep you signed in (storing a JWT token). Plausible Analytics uses no cookies.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">8. Changes to This Policy</h2>
            <p>We may update this policy as the service evolves. Material changes will be communicated by email to registered users. The &ldquo;Last updated&rdquo; date at the top of this page reflects the most recent revision.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">9. Contact</h2>
            <p>Questions about this policy? Email <a href="mailto:mitiro@gmail.com" className="text-teal underline">mitiro@gmail.com</a>.</p>
          </section>
        </div>
      </main>

      <footer className="border-t border-gray-200 py-6">
        <div className="max-w-2xl mx-auto px-4 flex gap-4 text-xs text-gray-400">
          <Link href="/privacy" className="hover:text-gray-600">Privacy Policy</Link>
          <Link href="/terms" className="hover:text-gray-600">Terms of Service</Link>
          <Link href="/" className="hover:text-gray-600">← Back to CogniESL</Link>
        </div>
      </footer>
    </div>
  );
}
