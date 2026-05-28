import Link from "next/link";
import { Badge } from "@/components/ui/Badge";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";

const posts = [
  {
    slug: "/blog/what-is-l1-interference",
    title: "What Is L1 Interference? (And Why It Changes Everything)",
    excerpt: "If you've ever wondered why your Spanish students say 'I am agree' or your Korean students drop articles, you've encountered L1 interference.",
    date: "May 16, 2026",
    category: "L1 Interference",
  },
  {
    slug: "/blog/ai-fatigue-teachers",
    title: "AI Fatigue Is Real: How to Use AI Without Losing Your Teaching Soul",
    excerpt: "We've all seen the hype. But what happens when you actually try to use AI in your ESL classroom? Here's an honest look at what works.",
    date: "May 16, 2026",
    category: "AI in ESL",
  },
  {
    slug: "/blog/spanish-students-say-i-am-agree",
    title: "Why Your Spanish Students Say 'I Am Agree' (And How to Fix It)",
    excerpt: "It's one of the most common errors I see from Spanish-speaking students. Once you understand why it happens, you can address it in minutes.",
    date: "May 16, 2026",
    category: "Teaching Tips",
  },
];

export function BlogPreview() {
  return (
    <section className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-950">
      <Container>
        <div className="text-center mb-12">
          <Badge variant="primary" className="mb-4">From the Blog</Badge>
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
            Practical Tips for{" "}
            <span className="gradient-text">ESL Teachers</span>
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
            Honest insights, real classroom experience, and practical strategies you can use Monday morning.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-5 max-w-5xl mx-auto mb-10">
          {posts.map((post) => (
            <Link
              key={post.slug}
              href={post.slug}
              className="group bg-white dark:bg-neutral-900 rounded-2xl p-6 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300"
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30 px-2.5 py-1 rounded-full">
                  {post.category}
                </span>
              </div>
              <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors leading-snug">
                {post.title}
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed mb-3">{post.excerpt}</p>
              <span className="text-xs text-neutral-400">{post.date}</span>
            </Link>
          ))}
        </div>

        <div className="text-center">
          <Button variant="outline" size="lg" asChild>
            <Link href="/blog">View All Posts</Link>
          </Button>
        </div>
      </Container>
    </section>
  );
}
