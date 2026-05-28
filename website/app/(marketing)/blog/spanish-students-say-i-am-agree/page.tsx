import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import Link from "next/link";
import { AuthorBio } from "@/components/blog/AuthorBio";
import { EmailCapture } from "@/components/blog/EmailCapture";

export const metadata = {
  title: "Why Your Spanish Students Say 'I Am Agree' (And How to Fix It) — CogniESL Blog",
  description: "It's one of the most common errors I see from Spanish-speaking students. The good news? Once you understand why it happens, you can address it in minutes.",
};

export default function BlogPost() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <span className="text-xs font-medium text-accent-600 dark:text-accent-400 bg-accent-50 dark:bg-accent-900/30 px-2.5 py-1 rounded-full">Teaching Tips</span>
              <span className="text-xs text-neutral-400">5 min read</span>
            </div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4 leading-tight">
              Why Your Spanish Students Say
              <br />
              <span className="gradient-text">&quot;I Am Agree&quot; (And How to Fix It)</span>
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto mb-4">
              It&apos;s one of the most common errors I see from Spanish-speaking students. The good news? Once you understand why it happens, you can address it in minutes.
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
            <p>
              &quot;Teacher, I am agree with Maria.&quot;
            </p>

            <p>
              If you teach Spanish-speaking students, you&apos;ve heard this. Maybe you&apos;ve heard it a hundred times. Maybe you correct it every single class. And maybe — like me — you&apos;ve wondered why they keep making the same mistake even after you&apos;ve explained it multiple times.
            </p>

            <p>
              Here&apos;s the thing: it&apos;s not that your students aren&apos;t listening. It&apos;s not that they&apos;re not trying. It&apos;s that they&apos;re doing something completely logical — they&apos;re applying the rules of Spanish to English.
            </p>

            <h2>The Logic Behind the Error</h2>

            <p>
              In Spanish, the phrase for &quot;I agree&quot; is <em>&quot;estoy de acuerdo&quot;</em>. Let&apos;s break that down:
            </p>

            <ul>
              <li><em>Estoy</em> = I am (from the verb <em>estar</em>, one of Spanish&apos;s two &quot;to be&quot; verbs)</li>
              <li><em>de</em> = of</li>
              <li><em>acuerdo</em> = agreement</li>
            </ul>

            <p>
              So <em>&quot;estoy de acuerdo&quot;</em> literally means &quot;I am in agreement.&quot; When your student says &quot;I am agree,&quot; she&apos;s not making a random mistake. She&apos;s translating the structure of her native language — including the verb &quot;to be&quot; — directly into English.
            </p>

            <p>
              This is L1 interference in action. And once you understand it, you can fix it.
            </p>

            <h2>How to Teach It (In 5 Minutes)</h2>

            <p>
              Here&apos;s what I do when this error comes up. It takes about 5 minutes and it works.
            </p>

            <h3>Step 1: Acknowledge the logic</h3>
            <p>
              Start by telling your students: &quot;In Spanish, you say <em>estoy de acuerdo</em> — I am in agreement. That makes sense! But in English, we use a different structure.&quot;
            </p>

            <p>
              This is important. You&apos;re not saying their Spanish is wrong. You&apos;re saying the <em>translation</em> doesn&apos;t work word-for-word. That distinction matters.
            </p>

            <h3>Step 2: Show the pattern</h3>
            <p>
              Write on the board:
            </p>

            <ul>
              <li>Spanish: <em>estar</em> + de acuerdo → English: <em>agree</em> (just the verb!)</li>
              <li>Spanish: <em>estoy</em> feliz → English: <em>I am</em> happy (here we DO use &quot;to be&quot;)</li>
            </ul>

            <p>
              The key insight: in English, &quot;agree&quot; is a verb all by itself. It doesn&apos;t need &quot;to be.&quot; But &quot;happy&quot; is an adjective, so it <em>does</em> need &quot;to be.&quot;
            </p>

            <h3>Step 3: Practice with variations</h3>
            <p>
              Have students practice:
            </p>

            <ul>
              <li>&quot;I agree&quot; / &quot;I don&apos;t agree&quot;</li>
              <li>&quot;She agrees&quot; / &quot;She doesn&apos;t agree&quot;</li>
              <li>&quot;Do you agree?&quot; / &quot;Yes, I agree&quot; / &quot;No, I don&apos;t agree&quot;</li>
            </ul>

            <p>
              Keep it short. Keep it focused. The goal is to replace the L1 pattern with the English pattern.
            </p>

            <h2>Other Common Spanish-to-English Errors</h2>

            <p>
              Once you start looking for L1 interference, you&apos;ll see it everywhere. Here are the most common patterns I see from Spanish-speaking students:
            </p>

            <h3>Age: &quot;I have 25 years&quot;</h3>
            <p>
              Spanish uses <em>tener</em> (to have) for age: <em>&quot;Tengo 25 años.&quot;</em> English uses &quot;to be.&quot; Quick fix: &quot;In English, age uses &apos;to be&apos; — I <em>am</em> 25 years old.&quot;
            </p>

            <h3>Professions: &quot;She is doctor&quot;</h3>
            <p>
              Spanish omits indefinite articles before professions: <em>&quot;Es doctora.&quot;</em> English requires them. Quick fix: &quot;In English, we always use &apos;a/an&apos; before professions — She is <em>a</em> doctor.&quot;
            </p>

            <h3>Wants: &quot;I want that you come&quot;</h3>
            <p>
              Spanish uses <em>que</em> (that) after <em>querer</em> (to want): <em>&quot;Quiero que vengas.&quot;</em> English uses the infinitive. Quick fix: &quot;After &apos;want,&apos; we use &apos;to&apos; — I want you <em>to</em> come.&quot;
            </p>

            <h2>Why This Approach Works</h2>

            <p>
              The traditional approach is to correct the error and move on. &quot;No, it&apos;s &apos;I agree,&apos; not &apos;I am agree.&apos;&quot; And students will repeat it correctly... for about five minutes. Then they go back to &quot;I am agree&quot; because the L1 pattern is deeply ingrained.
            </p>

            <p>
              The L1-aware approach is different. Instead of just correcting the surface error, you&apos;re addressing the <em>root cause</em>. You&apos;re showing students <em>why</em> the English structure is different from what their brain expects. That&apos;s what makes the correction stick.
            </p>

            <h2>The Bigger Picture</h2>

            <p>
              This is just one example. Spanish-to-English interference includes 142 documented patterns covering grammar, vocabulary, pronunciation, and pragmatics. Korean has 98. Arabic has 115. Mandarin has 127.
            </p>

            <p>
              You don&apos;t need to memorize all of them. But knowing the top 5-10 patterns for your students&apos; L1 can transform your teaching. You&apos;ll stop being surprised by errors. You&apos;ll start preventing them. And you&apos;ll become a more empathetic, more effective teacher.
            </p>

            <p>
              That&apos;s what L1 intelligence is all about. And that&apos;s what we&apos;re building into CogniESL — so you don&apos;t have to memorize 142 patterns. The tool does it for you.
            </p>

            <div className="bg-accent-50 dark:bg-accent-900/20 border border-accent-200 dark:border-accent-800 rounded-2xl p-6 mt-10 not-prose">
              <h3 className="font-heading text-lg font-semibold text-accent-800 dark:text-accent-200 mb-2">
                Want the full Spanish L1 guide?
              </h3>
              <p className="text-accent-700 dark:text-accent-300 text-sm mb-4">
                We&apos;ve documented 142 Spanish-to-English interference patterns with examples, corrections, and teaching tips. Free for ESL teachers.
              </p>
              <Link
                href="/l1/spanish"
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-accent-500 text-white hover:bg-accent-600 px-5 py-2.5 text-sm"
              >
                View Spanish L1 Guide →
              </Link>
            </div>

            <EmailCapture source="blog-spanish-i-am-agree" />

            <AuthorBio />
          </div>
        </Container>
      </Section>
    </>
  );
}
