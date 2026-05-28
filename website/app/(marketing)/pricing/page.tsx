import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import Link from "next/link";
import { PricingToggle } from "./PricingToggle";

export const metadata = {
  title: "Pricing — CogniESL",
  description: "Simple, transparent pricing for CogniESL. Start free, upgrade when ready.",
};

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    description: "Try CogniESL with limited generations. No credit card required.",
    features: [
      "5 generations per month",
      "3 L1 languages",
      "Slides only (no worksheet or activity guide)",
      "Basic difficulty levels",
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
    description: "For individual ESL teachers who want unlimited, full-featured access.",
    features: [
      "Unlimited generations",
      "All 36 L1 languages",
      "All 3 material formats",
      "All difficulty levels",
      "Priority generation",
      "Download as PPTX (slides) or DOCX (worksheets & guides)",
    ],
    cta: "Join Waitlist",
    variant: "primary" as const,
    popular: true,
  },
  {
    name: "School",
    price: "Custom",
    period: "",
    description: "For schools and programs. Volume pricing, admin dashboard, and teacher management.",
    features: [
      "Everything in Pro",
      "Admin dashboard",
      "Teacher management",
      "Usage analytics",
      "SSO integration",
      "Dedicated support",
    ],
    cta: "Contact Us",
    variant: "outline" as const,
    popular: false,
    comingSoon: true,
  },
];

const faqs = [
  { q: "Can I cancel anytime?", a: "Yes. No contracts, no cancellation fees." },
  { q: "Do you offer refunds?", a: "Yes. 14-day money-back guarantee, no questions asked." },
  { q: "Is there a free trial?", a: "The Free plan lets you generate 5 materials per month. No credit card required." },
  { q: "Can I switch plans later?", a: "Absolutely. Upgrade or downgrade at any time." },
];

export default function PricingPage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">Pricing</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Simple, <span className="gradient-text">Transparent</span> Pricing
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto mb-8">
              Start free. Upgrade when you&apos;re ready. No hidden fees, no surprises.
            </p>
            <PricingToggle />
          </div>
        </Container>
      </Section>

      <Section>
        <Container>
          <PricingToggle isSticky />
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
                    {plan.name === "Pro" ? plan.priceMonthly : plan.price}
                  </span>
                  {plan.period && (
                    <span className="text-neutral-500 dark:text-neutral-400 text-sm">{plan.period}</span>
                  )}
                </div>

                <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-6">{plan.description}</p>

                <Button variant={plan.variant} className="w-full mb-6" asChild>
                  <Link href={plan.name === "School" ? "/contact" : "/#waitlist"}>{plan.cta}</Link>
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

          <p className="text-center mt-8 text-sm text-neutral-500 dark:text-neutral-400">
            🔒 14-day money-back guarantee · No questions asked
          </p>
        </Container>
      </Section>

      <Section background="neutral">
        <Container size="md">
          <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-50 text-center mb-8">
            Questions About Pricing?
          </h2>
          <div className="space-y-3 max-w-2xl mx-auto">
            {faqs.map((faq) => (
              <div key={faq.q} className="bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800">
                <h3 className="text-base font-semibold text-neutral-900 dark:text-neutral-100 mb-1">{faq.q}</h3>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">{faq.a}</p>
              </div>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
