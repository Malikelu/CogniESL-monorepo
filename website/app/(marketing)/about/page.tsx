import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

export const metadata = {
  title: "About — CogniESL",
  description: "Learn about CogniESL — why we built it, who we are, and our mission to help ESL teachers save time.",
};

export default function AboutPage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12" background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">About</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Built by a teacher. For teachers.
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              CogniESL was born from real classroom experience — and a frustration with how much time teachers waste on material prep.
            </p>
          </div>
        </Container>
      </Section>

      <Section>
        <Container size="md">
          <div className="prose prose-lg max-w-none">
            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">The Problem We Saw</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              As an ESL teacher, I watched colleagues spend countless hours every week creating worksheets, formatting slides, and searching for activities that actually addressed their students&apos; specific needs. The worst part? Most of those materials were generic — they didn&apos;t account for the fact that a Spanish speaker&apos;s challenges with English are completely different from a Korean speaker&apos;s.
            </p>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              There had to be a better way. AI was getting powerful enough to generate content, but no tool was purpose-built for ESL teachers. ChatGPT could write text, but it didn&apos;t understand L1 interference. It couldn&apos;t create formatted classroom materials. And it certainly didn&apos;t know why your Arabic-speaking students keep saying &quot;He didn&apos;t went.&quot;
            </p>

            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4 mt-10">Why L1 Intelligence Matters</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              L1 interference (or &quot;language transfer&quot;) is the #1 reason ESL students make specific mistakes. When a Spanish speaker says &quot;I have 25 years&quot; instead of &quot;I am 25 years old,&quot; it&apos;s not a random error — it&apos;s a direct transfer from how Spanish works. When Korean students drop articles, it&apos;s because Korean doesn&apos;t have an article system.
            </p>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              Understanding these patterns doesn&apos;t just help you correct errors — it helps you <em>prevent</em> them. When you know what mistakes a student is likely to make, you can design materials that specifically address those patterns. That&apos;s what CogniESL does automatically.
            </p>

            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4 mt-10">Our Mission</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              We believe teachers should spend their time teaching — not prepping. We believe every ESL teacher should have access to the same linguistic insights that only specialists currently have. And we believe that AI, when purpose-built for education, can give teachers their evenings back.
            </p>
          </div>
        </Container>
      </Section>

      <Section background="neutral">
        <Container size="md">
          <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-8 text-center">
            What Makes Us Different
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: "🎯",
                title: "Purpose-Built for ESL",
                desc: "Not a generic AI tool. Every feature is designed specifically for ESL teachers and their students' needs.",
              },
              {
                icon: "🧠",
                title: "L1 Intelligence",
                desc: "36 L1 languages with real linguistic analysis. We don't just correct errors — we explain them.",
              },
              {
                icon: "⚡",
                title: "Classroom-Ready Output",
                desc: "Materials come formatted and ready to use — PPTX, PDF, printable worksheets. No extra work required.",
              },
            ].map((item) => (
              <Card key={item.title} className="text-center">
                <div className="text-3xl mb-3">{item.icon}</div>
                <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-2">
                  {item.title}
                </h3>
                <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">{item.desc}</p>
              </Card>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
