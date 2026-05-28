import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import Link from "next/link";

export const metadata = {
  title: "How It Works — CogniESL",
  description: "See how CogniESL generates custom ESL teaching materials in minutes with L1 interference intelligence.",
};

const steps = [
  {
    number: "01",
    icon: "💬",
    title: "Tell Us What You're Teaching",
    description: "Simply describe your lesson. What grammar point, topic, or skill? Who are your students? What languages do they speak?",
    example: '"Present perfect for Spanish speakers, intermediate level"',
    color: "primary" as const,
  },
  {
    number: "02",
    icon: "🧠",
    title: "L1 Intelligence Analyzes Patterns",
    description: "CogniESL's AI analyzes interference patterns from your students' native languages. It identifies specific errors they're likely to make and why.",
    details: [
      "Common error patterns for each L1 language",
      "False cognates and vocabulary traps",
      "Grammar transfer issues (word order, tense, articles)",
    ],
    color: "accent" as const,
  },
  {
    number: "03",
    icon: "📥",
    title: "Download & Teach",
    description: "Get finished materials in multiple formats — all tailored to your students' specific needs. No formatting required.",
    formats: ["📊 Slide Deck (PPTX)", "📝 Worksheet", "🎮 Activity Guide"],
    color: "secondary" as const,
  },
];

const colorStyles = {
  primary: {
    bg: "bg-primary-50 dark:bg-primary-900/20",
    border: "border-primary-200 dark:border-primary-800",
    icon: "bg-primary-100 dark:bg-primary-900/30",
    badge: "bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300",
  },
  accent: {
    bg: "bg-accent-50 dark:bg-accent-900/20",
    border: "border-accent-200 dark:border-accent-800",
    icon: "bg-accent-100 dark:bg-accent-900/30",
    badge: "bg-accent-100 dark:bg-accent-900/30 text-accent-700 dark:text-accent-300",
  },
  secondary: {
    bg: "bg-secondary-50 dark:bg-secondary-900/20",
    border: "border-secondary-200 dark:border-secondary-800",
    icon: "bg-secondary-100 dark:bg-secondary-900/30",
    badge: "bg-secondary-100 dark:bg-secondary-900/30 text-secondary-700 dark:text-secondary-300",
  },
};

export default function HowItWorksPage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">How It Works</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              From Lesson Idea to{" "}
              <span className="gradient-text">Classroom-Ready Materials</span>
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Three simple steps. Minutes, not hours. Here&apos;s exactly how it works.
            </p>
          </div>
        </Container>
      </Section>

      <Section>
        <Container size="md">
          <div className="space-y-8">
            {steps.map((step, i) => {
              const styles = colorStyles[step.color];
              return (
                <div key={step.number} className="relative">
                  {/* Connecting line */}
                  {i < steps.length - 1 && (
                    <div className="absolute left-6 top-20 bottom-0 w-0.5 bg-gradient-to-b from-neutral-200 to-neutral-100 dark:from-neutral-700 dark:to-neutral-800 hidden md:block" />
                  )}

                  <div className={`rounded-2xl p-6 md:p-8 border ${styles.bg} ${styles.border}`}>
                    <div className="flex items-start gap-5">
                      {/* Step number + icon */}
                      <div className="flex-shrink-0">
                        <div className={`w-12 h-12 rounded-2xl ${styles.icon} flex items-center justify-center text-2xl mb-2`}>
                          {step.icon}
                        </div>
                        <div className="text-xs font-bold text-neutral-400 dark:text-neutral-500 text-center tracking-widest">
                          STEP {step.number}
                        </div>
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-2">
                          {step.title}
                        </h2>
                        <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
                          {step.description}
                        </p>

                        {/* Example box for step 1 */}
                        {step.example && (
                          <div className="bg-white dark:bg-neutral-900 rounded-xl p-4 border border-neutral-200 dark:border-neutral-700 mb-4">
                            <p className="text-xs font-medium text-neutral-400 mb-1">Example request:</p>
                            <p className="text-sm text-neutral-700 dark:text-neutral-300 italic">{step.example}</p>
                          </div>
                        )}

                        {/* Details list for step 2 */}
                        {step.details && (
                          <ul className="space-y-2 mb-4">
                            {step.details.map((detail) => (
                              <li key={detail} className="flex items-start gap-2 text-sm text-neutral-600 dark:text-neutral-400">
                                <span className="text-success-500 mt-0.5">✓</span>
                                {detail}
                              </li>
                            ))}
                          </ul>
                        )}

                        {/* Format badges for step 3 */}
                        {step.formats && (
                          <div className="flex flex-wrap gap-2">
                            {step.formats.map((format) => (
                              <span key={format} className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium ${styles.badge}`}>
                                {format}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </Container>
      </Section>

      <Section background="neutral">
        <Container size="md">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Ready to Get Your Weekends Back?
            </h2>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 mb-8 max-w-xl mx-auto">
              Join the waitlist and be first to know when CogniESL launches. Early adopters get exclusive founding member pricing.
            </p>
            <Button size="lg" asChild>
              <Link href="/#waitlist">Join the Waitlist — It&apos;s Free</Link>
            </Button>
          </div>
        </Container>
      </Section>
    </>
  );
}
