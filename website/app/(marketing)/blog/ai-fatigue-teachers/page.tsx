import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import Link from "next/link";
import { AuthorBio } from "@/components/blog/AuthorBio";
import { EmailCapture } from "@/components/blog/EmailCapture";

export const metadata = {
  title: "AI Fatigue Is Real: How to Use AI Without Losing Your Teaching Soul — CogniESL Blog",
  description: "We've all seen the hype. But what happens when you actually try to use AI in your ESL classroom? Here's an honest look at what works, what doesn't, and how to find the balance.",
};

export default function BlogPost() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <span className="text-xs font-medium text-secondary-600 dark:text-secondary-400 bg-secondary-50 dark:bg-secondary-900/30 px-2.5 py-1 rounded-full">AI in ESL</span>
              <span className="text-xs text-neutral-400">6 min read</span>
            </div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4 leading-tight">
              AI Fatigue Is Real
              <br />
              <span className="gradient-text-warm">How to Use AI Without Losing Your Teaching Soul</span>
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto mb-4">
              We&apos;ve all seen the hype. But what happens when you actually try to use AI in your ESL classroom? Here&apos;s an honest look at what works, what doesn&apos;t, and how to find the balance.
            </p>
            <div className="flex items-center justify-center gap-3 text-sm text-neutral-500">
              <span>May 16, 2026</span>
              <span>·</span>
              <span>Written for ESL teachers</span>
            </div>
          </div>
        </Container>
      </Section>

      <Section>
        <Container size="md">
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              Can I be honest with you for a minute?
            </p>

            <p>
              When ChatGPT first came out, I was excited. Really excited. I thought, &quot;This is it. This is going to change everything. No more Sunday night prep. No more searching for hours for the perfect worksheet.&quot;
            </p>

            <p>
              So I tried it. And you know what? It was... fine. It gave me some activity ideas. It wrote me a decent lesson plan. But then I spent 45 minutes formatting the output, fixing the errors, and adapting it to my students&apos; level. By the time I was done, I could have just written it myself.
            </p>

            <p>
              That&apos;s AI fatigue. And if you&apos;ve felt it too, you&apos;re not alone.
            </p>

            <h2>The Hype vs. Reality</h2>

            <p>
              Let&apos;s be real about what AI can and can&apos;t do for ESL teachers right now.
            </p>

            <p>
              <strong>What AI is good at:</strong> Generating ideas, creating rough drafts, explaining grammar concepts, suggesting activities. It&apos;s like having a teaching assistant who works fast but doesn&apos;t really understand your students.
            </p>

            <p>
              <strong>What AI is bad at:</strong> Understanding why your specific students make specific mistakes. Creating materials that are formatted and ready to use. Knowing that your Korean students will drop articles but your Spanish students won&apos;t. Understanding the difference between teaching adults and teaching kids.
            </p>

            <p>
              The problem isn&apos;t that AI is useless. The problem is that most AI tools were built for everyone, which means they were built for no one. Generic AI gives you generic results. And as ESL teachers, we know that generic doesn&apos;t work.
            </p>

            <h2>The Format Gap</h2>

            <p>
              Here&apos;s the thing nobody talks about: the biggest time sink isn&apos;t creating content. It&apos;s <em>formatting</em> it.
            </p>

            <p>
              You ask ChatGPT for a worksheet on present perfect. It gives you text. Then you copy it into Google Docs. Then you format it — add headings, adjust spacing, make it printable, create an answer key. That takes 20-30 minutes. The AI saved you maybe 10 minutes of brainstorming, but you still spent half an hour on the actual material.
            </p>

            <p>
              This is what I call the &quot;format gap&quot; — the distance between what AI gives you and what you actually need in your classroom. Until that gap closes, AI will feel like more work than it&apos;s worth.
            </p>

            <h2>So Should We Just Give Up on AI?</h2>

            <p>
              Absolutely not. But we need to be smarter about how we use it.
            </p>

            <p>
              Here&apos;s what I&apos;ve learned after two years of experimenting with AI in my classroom:
            </p>

            <h3>1. Use AI for what it&apos;s good at — brainstorming</h3>
            <p>
              When I&apos;m stuck on how to teach a grammar point, I&apos;ll ask AI for activity ideas. Not for the final material — just for inspiration. It&apos;s great at suggesting approaches I might not have thought of. Then I take those ideas and build the actual materials myself.
            </p>

            <h3>2. Don&apos;t trust the answer key</h3>
            <p>
              This is a big one. AI makes mistakes on answer keys. About 1 in 10 answers can be wrong, oversimplified, or missing alternative correct answers. If you&apos;re going to use AI-generated exercises, <em>always</em> check the answer key yourself before giving it to students. Trust me on this one.
            </p>

            <h3>3. Be specific about L1</h3>
            <p>
              If you&apos;re going to use AI, tell it what language your students speak. Instead of &quot;create a worksheet on articles,&quot; try &quot;create a worksheet on articles for Korean-speaking students who tend to drop articles because Korean has no article system.&quot; The more specific you are, the better the output. But even then, you&apos;ll need to adapt it.
            </p>

            <h3>4. Keep your teaching soul</h3>
            <p>
              This is the most important one. AI can help you prep faster, but it can&apos;t replace what makes you a good teacher. It can&apos;t read the room. It can&apos;t see that Maria is having a bad day and needs a gentler approach. It can&apos;t improvise when your lesson plan falls apart because the internet went down.
            </p>

            <p>
              Your experience, your intuition, your relationship with your students — that&apos;s your teaching soul. AI is just a tool. Use it to save time on the boring stuff so you can focus on the important stuff: actually teaching.
            </p>

            <h2>What Good AI for ESL Looks Like</h2>

            <p>
              I&apos;ve been thinking a lot about what an AI tool built <em>for</em> ESL teachers would look like. Not a generic AI that happens to work for teaching, but a tool designed specifically for our workflow.
            </p>

            <p>
              Here&apos;s what I&apos;d want:
            </p>

            <ul>
              <li><strong>Finished files, not text.</strong> Give me a printable PDF worksheet and a PowerPoint deck. Not something I have to copy-paste and format.</li>
              <li><strong>L1 intelligence built in.</strong> I shouldn&apos;t have to explain that Korean students drop articles. The tool should already know that.</li>
              <li><strong>Reliable answer keys.</strong> If I&apos;m giving a worksheet to 30 students, I need to know the answers are correct.</li>
              <li><strong>Pedagogically sound.</strong> The exercises should follow ESL best practices, not just random grammar drills.</li>
              <li><strong>Fast.</strong> If it takes me 30 minutes to adapt AI output, it&apos;s not saving me time.</li>
            </ul>

            <p>
              That&apos;s what we&apos;re building with CogniESL. Not because we think AI is magic, but because we think teachers deserve tools that actually work for them.
            </p>

            <h2>The Bottom Line</h2>

            <p>
              AI fatigue is real. The hype is exhausting. And most AI tools for teachers are disappointing.
            </p>

            <p>
              But the underlying technology is getting better. And when it&apos;s purpose-built for ESL teachers — when it understands L1 interference, outputs finished files, and respects our pedagogy — it can genuinely give us our weekends back.
            </p>

            <p>
              Until then, use AI as a brainstorming partner, not a replacement. Check everything it gives you. And never let it replace the thing that makes you a great teacher: <em>you</em>.
            </p>

            <div className="bg-secondary-50 dark:bg-secondary-900/20 border border-secondary-200 dark:border-secondary-800 rounded-2xl p-6 mt-10 not-prose">
              <h3 className="font-heading text-lg font-semibold text-secondary-800 dark:text-secondary-200 mb-2">
                Tired of formatting AI output?
              </h3>
              <p className="text-secondary-700 dark:text-secondary-300 text-sm mb-4">
                CogniESL generates finished materials — slides, worksheets, and activity guides — with L1 intelligence built in. No copy-paste. No formatting. Just describe your class and get materials ready for Monday.
              </p>
              <Link
                href="/#waitlist"
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-secondary-500 text-white hover:bg-secondary-600 px-5 py-2.5 text-sm"
              >
                Join the Waitlist →
              </Link>
            </div>

            <EmailCapture source="blog-ai-fatigue" />

            <AuthorBio />
          </div>
        </Container>
      </Section>
    </>
  );
}
