"use client";
import Link from "next/link";
import { Navbar } from "@/components/Navbar";

export default function TermsPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Navbar />
      <main className="flex-1 max-w-2xl mx-auto w-full px-4 py-10">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-2">Terms of Service</h1>
        <p className="text-sm text-gray-400 mb-8">Last updated: May 2026</p>

        <div className="prose prose-sm text-gray-700 space-y-6">

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">1. Acceptance of Terms</h2>
            <p>By creating a CogniESL account or using our service, you agree to these Terms of Service. If you do not agree, please do not use CogniESL. CogniESL is operated by Marcos Itiro (&ldquo;we&rdquo;, &ldquo;us&rdquo;).</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">2. Description of Service</h2>
            <p>CogniESL is an AI-powered tool that generates ESL (English as a Second Language) teaching materials including slide decks, worksheets, and activity guides. Materials are generated based on grammar topics, student native languages, and proficiency levels you specify.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">3. Account Registration</h2>
            <p>You must provide a valid email address to create an account. You are responsible for keeping your password confidential. You must be at least 18 years old to create an account. One person may not create multiple free accounts to circumvent usage limits.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">4. Subscription Plans and Payments</h2>
            <p>CogniESL offers a Free tier and paid Pro tier. Payments are processed by Stripe. Subscriptions renew automatically unless cancelled. Founding Member pricing ($7/month annual) is locked permanently for the first 100 subscribers who purchase it — this price will not increase for those accounts.</p>
            <p className="mt-2">Refunds are evaluated case by case. Contact <a href="mailto:mitiro@gmail.com" className="text-teal underline">mitiro@gmail.com</a> within 7 days of a charge for refund requests.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">5. Usage Limits</h2>
            <p>Free accounts are limited to 5 material generations per calendar month. Pro accounts are limited to 20 generations per month (soft cap). Usage limits reset on the 1st of each calendar month. We reserve the right to adjust limits with 30 days&apos; notice.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">6. Your Content and Materials</h2>
            <p>You retain ownership of the teaching materials generated through your CogniESL account. The underlying database of grammar rules and L1 interference patterns used to generate materials is proprietary to CogniESL. You may use generated materials for teaching purposes, including commercial tutoring.</p>
            <p className="mt-2">You may not: resell CogniESL-generated materials as a competing service; represent the materials as entirely your own original work if distributing at scale; or use the service to generate content for non-educational purposes.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">7. Acceptable Use</h2>
            <p>You agree not to: attempt to circumvent usage limits; scrape, reverse-engineer, or copy the CogniESL database; share your account credentials with others; use the service for any illegal purpose; or attempt to disrupt the service.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">8. Service Availability</h2>
            <p>We aim for high availability but do not guarantee uninterrupted service. Generated materials are stored on our servers for download. Files may be unavailable after service updates or after 30 days. We recommend downloading your materials promptly after generation.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">9. Disclaimer of Warranties</h2>
            <p>CogniESL is provided &ldquo;as is&rdquo;. We do not guarantee that generated materials are free of errors or suitable for every teaching context. You are responsible for reviewing materials before use in the classroom. Our pedagogical database is research-backed, but we are not liable for outcomes in your specific teaching context.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">10. Limitation of Liability</h2>
            <p>To the fullest extent permitted by law, CogniESL&apos;s liability to you is limited to the amount you paid in the 3 months preceding any claim. We are not liable for indirect, incidental, or consequential damages.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">11. Account Termination</h2>
            <p>You may delete your account at any time from <Link href="/settings" className="text-teal underline">Account Settings</Link>. We may suspend accounts that violate these terms. Upon termination, your data is deleted per our Privacy Policy.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">12. Changes to Terms</h2>
            <p>We may update these terms. Material changes will be communicated by email at least 14 days in advance. Continued use of the service after changes constitutes acceptance of the new terms.</p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">13. Contact</h2>
            <p>Questions about these terms? Email <a href="mailto:mitiro@gmail.com" className="text-teal underline">mitiro@gmail.com</a>.</p>
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
