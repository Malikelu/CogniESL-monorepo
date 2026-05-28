import { Badge } from "@/components/ui/Badge";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { l1Languages } from "@/lib/l1-data";
import Link from "next/link";

export const metadata = {
  title: "Resources for ESL Teachers — CogniESL",
  description: "Free resources for ESL teachers: L1 interference guides, teaching tips, blog posts, and tools to save you time.",
};

const blogPosts = [
  {
    slug: "/blog/what-is-l1-interference",
    title: "What Is L1 Interference? (And Why It Changes Everything)",
    category: "L1 Interference",
  },
  {
    slug: "/blog/ai-fatigue-teachers",
    title: "AI Fatigue Is Real: How to Use AI Without Losing Your Teaching Soul",
    category: "AI in ESL",
  },
  {
    slug: "/blog/spanish-students-say-i-am-agree",
    title: "Why Your Spanish Students Say 'I Am Agree' (And How to Fix It)",
    category: "Teaching Tips",
  },
];

export default function ResourcesPage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">Resources</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Free Resources for{" "}
              <span className="gradient-text">ESL Teachers</span>
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Everything we know about L1 interference, teaching smarter with AI, and saving time on material prep. All free.
            </p>
          </div>
        </Container>
      </Section>

      {/* L1 Interference Guides */}
      <Section>
        <Container>
          <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-2">
            L1 Interference Guides
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6 max-w-2xl">
            Detailed guides for each language, with common errors, interference patterns, and teaching tips.
          </p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {l1Languages.map((lang) => (
              <Link
                key={lang.code}
                href={`/l1/${lang.code}`}
                className="group bg-white dark:bg-neutral-900 rounded-xl p-4 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
              >
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-2xl">{lang.flag}</span>
                  <div>
                    <h3 className="font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                      {lang.name}
                    </h3>
                    <p className="text-xs text-neutral-500">{lang.interferencePatterns.length} patterns</p>
                  </div>
                </div>
                <div className="flex flex-wrap gap-1">
                  {lang.interferencePatterns.map((p) => (
                    <span key={p.category} className="text-xs px-2 py-0.5 rounded-full bg-neutral-100 dark:bg-neutral-800 text-neutral-500">
                      {p.category}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </Section>

      {/* Blog Posts */}
      <Section background="neutral">
        <Container>
          <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-2">
            Teaching Tips & Insights
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6 max-w-2xl">
            Practical advice from experienced ESL teachers. Real classroom strategies you can use Monday morning.
          </p>
          <div className="grid md:grid-cols-3 gap-5">
            {blogPosts.map((post) => (
              <Link
                key={post.slug}
                href={post.slug}
                className="group bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
              >
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 mb-3">
                  {post.category}
                </span>
                <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors leading-snug">
                  {post.title}
                </h3>
              </Link>
            ))}
          </div>
        </Container>
      </Section>

      {/* Interactive Tools */}
      <Section>
        <Container>
          <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-2">
            Interactive Tools
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6 max-w-2xl">
            Explore L1 interference patterns interactively. Click any language to see real examples.
          </p>
          <div className="grid sm:grid-cols-2 gap-4">
            <Link
              href="/l1-explorer"
              className="group bg-white dark:bg-neutral-900 rounded-xl p-6 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
            >
              <div className="text-3xl mb-3">🌍</div>
              <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors mb-1">
                L1 Interference Explorer
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Browse interference patterns by language. See common errors and corrections.
              </p>
            </Link>
            <Link
              href="/samples"
              className="group bg-white dark:bg-neutral-900 rounded-xl p-6 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
            >
              <div className="text-3xl mb-3">📊</div>
              <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors mb-1">
                Sample Materials
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                See examples of materials CogniESL generates, tailored to specific L1 backgrounds.
              </p>
            </Link>
          </div>
        </Container>
      </Section>

      {/* CTA */}
      <Section background="neutral">
        <Container size="md">
          <div className="text-center bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl p-8">
            <h2 className="font-heading text-2xl font-bold text-white mb-3">
              Ready to Save Time on Prep?
            </h2>
            <p className="text-primary-100 mb-6 max-w-lg mx-auto">
              Join the waitlist and be first to know when CogniESL launches. Early adopters get exclusive founding member pricing.
            </p>
            <Link
              href="/#waitlist"
              className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-white text-primary-700 hover:bg-primary-50 px-8 py-3"
            >
              Join the Waitlist — It&apos;s Free
            </Link>
          </div>
        </Container>
      </Section>
    </>
  );
}
