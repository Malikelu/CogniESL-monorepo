import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Badge } from "@/components/ui/Badge";
import Link from "next/link";

const languages = [
  { code: "es", name: "Spanish", flag: "🇪🇸", patterns: 142 },
  { code: "ko", name: "Korean", flag: "🇰🇷", patterns: 98 },
  { code: "ar", name: "Arabic", flag: "🇸🇦", patterns: 115 },
  { code: "zh", name: "Mandarin", flag: "🇨🇳", patterns: 127 },
  { code: "ja", name: "Japanese", flag: "🇯🇵", patterns: 103 },
  { code: "pt", name: "Portuguese", flag: "🇧🇷", patterns: 89 },
  { code: "ru", name: "Russian", flag: "🇷🇺", patterns: 94 },
  { code: "vi", name: "Vietnamese", flag: "🇻🇳", patterns: 76 },
  { code: "hi", name: "Hindi", flag: "🇮🇳", patterns: 82 },
  { code: "fr", name: "French", flag: "🇫🇷", patterns: 71 },
  { code: "de", name: "German", flag: "🇩🇪", patterns: 68 },
  { code: "tl", name: "Tagalog", flag: "🇵🇭", patterns: 59 },
];

export const metadata = {
  title: "L1 Interference Guide — CogniESL",
  description: "Complete guide to L1 interference for ESL teachers. Understand why students from different language backgrounds make specific mistakes — and how to address them.",
};

export default function L1GuidePage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="primary" className="mb-4">Complete Guide</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              L1 Interference: The Complete Guide for ESL Teachers
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Understanding why your students make specific mistakes — and how to address them before they happen.
            </p>
          </div>
        </Container>
      </Section>

      <Section>
        <Container size="md">
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">What Is L1 Interference?</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
              L1 interference (also called &quot;language transfer&quot;) occurs when a student&apos;s native language (L1) influences how they learn and use English. It&apos;s the single most important factor in understanding why ESL students make specific, predictable errors.
            </p>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
              When a Spanish speaker says &quot;I have 25 years&quot; instead of &quot;I am 25 years old,&quot; it&apos;s not a random mistake — it&apos;s a direct transfer from Spanish, where the verb &quot;tener&quot; (to have) is used for age. When Korean students drop articles (&quot;I went to store&quot;), it&apos;s because Korean has no article system.
            </p>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              Understanding L1 interference doesn&apos;t just help you correct errors — it helps you <strong>prevent</strong> them. When you know what mistakes a student is likely to make, you can design materials that specifically address those patterns.
            </p>

            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4 mt-10">Why Most ESL Materials Fail</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
              Most ESL textbooks and worksheets are designed for a generic student. They don&apos;t account for the fact that a Spanish speaker&apos;s challenges with English are completely different from a Korean speaker&apos;s. A worksheet on articles might be perfect for Korean students but useless for Spanish speakers, who have a different relationship with articles.
            </p>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              This is why CogniESL was built. Our AI analyzes interference patterns from 36 L1 languages and builds them directly into your materials. Your worksheets, slides, and activities are tailored to your students&apos; specific language backgrounds.
            </p>

            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4 mt-10">How to Use This Guide</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
              Click on any language below to see the most common interference patterns, example errors, and teaching tips. Each page includes real examples you can use in your classroom.
            </p>
          </div>
        </Container>
      </Section>

      <Section background="neutral">
        <Container>
          <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-8 text-center">
            L1 Interference Patterns by Language
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl mx-auto">
            {languages.map((lang) => (
              <Link
                key={lang.code}
                href={`/l1/${lang.code}`}
                className="flex items-center gap-4 bg-white dark:bg-neutral-900 rounded-xl p-4 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover transition-all duration-300 group"
              >
                <span className="text-3xl">{lang.flag}</span>
                <div>
                  <h3 className="font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                    {lang.name}
                  </h3>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400">
                    {lang.patterns} interference patterns
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </Section>

      <Section>
        <Container size="md">
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">The Science Behind L1 Interference</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
              L1 interference is one of the most studied phenomena in second language acquisition (SLA). Research shows that approximately 30-50% of errors made by ESL students can be attributed to L1 transfer. The effect is strongest in:
            </p>
            <ul className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4 list-disc pl-6 space-y-2">
              <li><strong>Grammar:</strong> Word order, verb tense, articles, prepositions</li>
              <li><strong>Phonology:</strong> Pronunciation, stress patterns, intonation</li>
              <li><strong>Vocabulary:</strong> False friends, cognates, collocations</li>
              <li><strong>Pragmatics:</strong> Politeness strategies, discourse patterns</li>
            </ul>

            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4 mt-10">How CogniESL Uses L1 Intelligence</h2>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">
              When you tell CogniESL that your students speak Spanish, our AI:
            </p>
            <ol className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4 list-decimal pl-6 space-y-2">
              <li>Identifies the 142 most common Spanish-to-English interference patterns</li>
              <li>Highlights which patterns are relevant to your specific lesson topic</li>
              <li>Generates materials with L1-specific callouts and error warnings</li>
              <li>Creates targeted exercises that address the most likely mistakes</li>
            </ol>
            <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
              The result? Materials that don&apos;t just teach English — they teach English <em>to Spanish speakers</em>. That&apos;s the difference between generic and L1-intelligent.
            </p>

            <div className="bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800 rounded-2xl p-6 mt-8">
              <h3 className="font-heading text-lg font-semibold text-primary-800 dark:text-primary-200 mb-2">
                Ready to see L1 intelligence in action?
              </h3>
              <p className="text-primary-700 dark:text-primary-300 text-sm mb-4">
                Join the waitlist and be first to know when CogniESL launches.
              </p>
              <Link
                href="/#waitlist"
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 px-6 py-3 text-sm"
              >
                Join the Waitlist
              </Link>
            </div>
          </div>
        </Container>
      </Section>
    </>
  );
}
