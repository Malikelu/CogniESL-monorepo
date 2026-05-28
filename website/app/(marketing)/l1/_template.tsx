import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { Badge } from "@/components/ui/Badge";
import Link from "next/link";

interface ErrorPattern {
  error: string;
  correction: string;
  explanation: string;
  category: string;
}

interface LanguageData {
  code: string;
  name: string;
  flag: string;
  patterns: number;
  speakers: string;
  overview: string;
  errors: ErrorPattern[];
  tips: string[];
}

export function createLanguagePage(lang: LanguageData) {
  return function LanguagePage() {
    return (
      <>
        <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
          <Container size="md">
            <div className="text-center">
              <Badge variant="primary" className="mb-4">L1 Interference Guide</Badge>
              <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
                {lang.flag} {lang.name} L1 Interference Patterns
              </h1>
              <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
                {lang.patterns} common interference patterns. Why {lang.name}-speaking students make specific mistakes — and how to help them.
              </p>
            </div>
          </Container>
        </Section>

        <Section>
          <Container size="md">
            <div className="prose prose-lg dark:prose-invert max-w-none">
              <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">Overview</h2>
              <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-4">{lang.overview}</p>
              <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed mb-6">
                <strong>US Speaker Population:</strong> {lang.speakers}
              </p>
            </div>
          </Container>
        </Section>

        <Section background="neutral">
          <Container>
            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-8 text-center">
              Common Error Patterns
            </h2>
            <div className="space-y-4 max-w-3xl mx-auto">
              {lang.errors.map((ex, i) => (
                <div key={i} className="bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800">
                  <div className="flex items-start gap-3">
                    <span className="text-base mt-0.5 flex-shrink-0">❌</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-medium text-neutral-400 bg-neutral-100 dark:bg-neutral-800 px-2 py-0.5 rounded-full">{ex.category}</span>
                      </div>
                      <p className="text-neutral-400 dark:text-neutral-500 line-through text-sm">{ex.error}</p>
                      <p className="text-success-600 dark:text-success-400 font-medium text-sm mt-0.5">✅ {ex.correction}</p>
                      <p className="text-neutral-600 dark:text-neutral-300 text-sm mt-1.5 leading-relaxed">💡 {ex.explanation}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Container>
        </Section>

        <Section>
          <Container size="md">
            <h2 className="font-heading text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-6">
              Teaching Tips for {lang.name} Speakers
            </h2>
            <div className="space-y-3">
              {lang.tips.map((tip, i) => (
                <div key={i} className="flex items-start gap-3 bg-primary-50 dark:bg-primary-900/20 rounded-xl p-4 border border-primary-200/60 dark:border-primary-800/40">
                  <span className="text-primary-500 font-bold text-sm mt-0.5">{i + 1}.</span>
                  <p className="text-neutral-700 dark:text-neutral-300 text-sm leading-relaxed">{tip}</p>
                </div>
              ))}
            </div>

            <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl p-6 mt-10 text-center">
              <h3 className="font-heading text-lg font-semibold text-white mb-2">
                Generate L1-Intelligent Materials
              </h3>
              <p className="text-primary-100 text-sm mb-4">
                CogniESL automatically creates materials tailored to your students&apos; {lang.name} L1 background.
              </p>
              <Link
                href="/#waitlist"
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-white text-primary-700 hover:bg-primary-50 px-6 py-3 text-sm"
              >
                Join the Waitlist
              </Link>
            </div>
          </Container>
        </Section>
      </>
    );
  };
}
