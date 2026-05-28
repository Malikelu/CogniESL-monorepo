import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import Link from "next/link";

const steps = [
  {
    number: "01",
    title: "Describe your class in plain English",
    detail: "\"Present simple for my Spanish B1 students. Need slides and a worksheet.\"",
    description: "No forms, no dropdowns. Just talk to CogniESL like you'd describe the lesson to a colleague.",
    icon: "💬",
    time: "~2 minutes",
  },
  {
    number: "02",
    title: "L1 intelligence does the heavy lifting",
    detail: "CogniESL pulls from 36 validated interference databases to find what your specific students get wrong — and why.",
    description: "It doesn't guess. It reads from a research-backed database of 302 grammar files and language-specific error patterns.",
    icon: "🧠",
    time: "Automatic",
  },
  {
    number: "03",
    title: "Open your email. Teach.",
    detail: "Slides, worksheet, and activity guide — all with your students' L1 errors highlighted and explained.",
    description: "PPTX download, printable worksheet with answer key, step-by-step activity guide with teacher script. Ready to use Monday morning.",
    icon: "📬",
    time: "Materials in your inbox",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-950">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-semibold mb-4">
            How it works
          </span>
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            Three steps.{" "}
            <span className="gradient-text">One conversation.</span>
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed">
            No learning curve. No templates. No guesswork.
            CogniESL does the research while you do the teaching.
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-4">
          {steps.map((step, idx) => (
            <div
              key={step.number}
              className="relative bg-white dark:bg-neutral-900 rounded-2xl p-6 md:p-8 border border-neutral-200/80 dark:border-neutral-800 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-card-hover transition-all duration-300"
            >
              <div className="flex gap-5 items-start">
                {/* Number + connector line */}
                <div className="flex flex-col items-center flex-shrink-0">
                  <div className="w-12 h-12 rounded-xl bg-primary-500 text-white flex items-center justify-center font-heading font-bold text-lg shadow-glow">
                    {idx + 1}
                  </div>
                  {idx < steps.length - 1 && (
                    <div className="w-0.5 h-full min-h-[24px] bg-gradient-to-b from-primary-300 to-transparent dark:from-primary-700 mt-2" />
                  )}
                </div>

                <div className="flex-1 min-w-0 pb-2">
                  <div className="flex items-center gap-3 mb-2 flex-wrap">
                    <span className="text-2xl">{step.icon}</span>
                    <h3 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100">
                      {step.title}
                    </h3>
                    <span className="text-xs font-medium text-success-600 dark:text-success-400 bg-success-50 dark:bg-success-900/30 px-2.5 py-1 rounded-full ml-auto">
                      {step.time}
                    </span>
                  </div>

                  {/* The vivid real-world example */}
                  <p className="text-sm text-primary-700 dark:text-primary-300 bg-primary-50/60 dark:bg-primary-900/20 rounded-lg px-4 py-2.5 mb-3 font-medium leading-relaxed border-l-2 border-primary-400 dark:border-primary-600">
                    {step.detail}
                  </p>

                  <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-10">
          <Button size="lg" asChild>
            <Link href="#waitlist">Get Early Access — Free</Link>
          </Button>
          <p className="text-sm text-neutral-400 mt-3">No credit card required. Join 47 teachers already on the waitlist.</p>
        </div>
      </Container>
    </section>
  );
}
