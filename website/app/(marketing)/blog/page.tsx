import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Badge } from "@/components/ui/Badge";
import Link from "next/link";

const posts = [
  {
    slug: "what-is-l1-interference",
    title: "What Is L1 Interference? (And Why It Changes Everything)",
    excerpt: "If you've ever wondered why your Spanish students say 'I am agree' or your Korean students drop articles, you've encountered L1 interference. Here's what every ESL teacher should know.",
    date: "May 16, 2026",
    readTime: "8 min read",
    category: "L1 Interference",
    featured: true,
  },
  {
    slug: "ai-fatigue-teachers",
    title: "AI Fatigue Is Real: How to Use AI Without Losing Your Teaching Soul",
    excerpt: "We've all seen the hype. But what happens when you actually try to use AI in your ESL classroom? Here's an honest look at what works, what doesn't, and how to find the balance.",
    date: "May 16, 2026",
    readTime: "6 min read",
    category: "AI in ESL",
    featured: true,
  },
  {
    slug: "spanish-students-say-i-am-agree",
    title: "Why Your Spanish Students Say 'I Am Agree' (And How to Fix It)",
    excerpt: "It's one of the most common errors I see from Spanish-speaking students. The good news? Once you understand why it happens, you can address it in minutes.",
    date: "May 16, 2026",
    readTime: "5 min read",
    category: "Teaching Tips",
    featured: false,
  },
];

export const metadata = {
  title: "Blog — CogniESL",
  description: "Practical tips and insights for ESL teachers. Learn about L1 interference, AI in the classroom, and how to save time on material prep.",
};

export default function BlogIndexPage() {
  const featured = posts.filter((p) => p.featured);
  const regular = posts.filter((p) => !p.featured);

  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">Blog</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              Thoughts from the Classroom
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Practical tips, honest insights, and real talk about ESL teaching. Written by teachers, for teachers.
            </p>
          </div>
        </Container>
      </Section>

      <Section>
        <Container>
          {/* Featured posts */}
          <div className="grid md:grid-cols-2 gap-6 mb-10">
            {featured.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group bg-white dark:bg-neutral-900 rounded-2xl p-6 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30 px-2.5 py-1 rounded-full">{post.category}</span>
                  <span className="text-xs text-neutral-400">{post.readTime}</span>
                </div>
                <h2 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                  {post.title}
                </h2>
                <p className="text-neutral-600 dark:text-neutral-400 text-sm leading-relaxed mb-3">{post.excerpt}</p>
                <span className="text-xs text-neutral-400">{post.date}</span>
              </Link>
            ))}
          </div>

          {/* Regular posts */}
          <div className="space-y-4">
            {regular.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group flex items-start gap-4 bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30 px-2.5 py-1 rounded-full">{post.category}</span>
                    <span className="text-xs text-neutral-400">{post.readTime}</span>
                  </div>
                  <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                    {post.title}
                  </h3>
                  <p className="text-neutral-600 dark:text-neutral-400 text-sm leading-relaxed">{post.excerpt}</p>
                </div>
                <span className="text-xs text-neutral-400 whitespace-nowrap mt-1">{post.date}</span>
              </Link>
            ))}
          </div>
        </Container>
      </Section>
    </>
  );
}
