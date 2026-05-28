import { Badge } from "@/components/ui/Badge";
import { Container } from "@/components/ui/Container";
import { Section } from "@/components/ui/Section";
import { l1Languages } from "@/lib/l1-data";
import Link from "next/link";

export const metadata = {
  title: "L1 Interference Explorer — CogniESL",
  description: "Explore L1 interference patterns for 31 languages. Understand why your ESL students make specific mistakes based on their native language.",
};

export default function L1ExplorerPage() {
  return (
    <>
      <Section className="pt-28 lg:pt-32 pb-12 " background="neutral">
        <Container size="md">
          <div className="text-center">
            <Badge variant="accent" className="mb-4">L1 Intelligence</Badge>
            <h1 className="text-4xl sm:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-4">
              L1 Interference Explorer
            </h1>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl mx-auto">
              Select a language to see common interference patterns, typical errors,
              and how CogniESL addresses them in your teaching materials.
            </p>
          </div>
        </Container>
      </Section>

      <Section>
        <Container>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
            {l1Languages.map((lang) => (
              <Link
                key={lang.code}
                href={`/l1/${lang.code}`}
                className="group bg-white dark:bg-neutral-900 rounded-2xl p-5 border border-neutral-200/80 dark:border-neutral-800 hover:shadow-card-hover hover:border-primary-300 dark:hover:border-primary-700 transition-all duration-300"
              >
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl">{lang.flag}</span>
                  <div>
                    <h3 className="font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                      {lang.name}
                    </h3>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">{lang.speakers}</p>
                  </div>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {lang.interferencePatterns.map((p) => (
                    <span key={p.category} className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400">
                      {p.category}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>

          <div className="text-center">
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
              Want to dive deeper? Visit our <Link href="/l1-interference-guide" className="text-primary-600 dark:text-primary-400 font-medium hover:underline">complete L1 interference guide</Link> with detailed patterns for each language.
            </p>
          </div>
        </Container>
      </Section>

      {l1Languages.map((lang, idx) => (
        <Section key={lang.code} id={`detail-${lang.code}`} background={idx % 2 === 0 ? "white" : "neutral"}>
          <Container size="md">
            <div className="flex items-center gap-4 mb-8">
              <span className="text-4xl">{lang.flag}</span>
              <div>
                <h2 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100">
                  {lang.name} L1 Interference Patterns
                </h2>
                <p className="text-sm text-neutral-500 dark:text-neutral-400">{lang.speakers}</p>
              </div>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
                Common Errors in English
              </h3>
              <div className="bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800">
                <ul className="space-y-2.5">
                  {lang.commonErrors.map((error) => (
                    <li key={error} className="flex items-start gap-2.5 text-sm text-neutral-700 dark:text-neutral-300">
                      <span className="text-secondary-500 mt-0.5 flex-shrink-0">⚠️</span>
                      <span>{error}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
                Interference Patterns & How CogniESL Addresses Them
              </h3>
              <div className="space-y-4">
                {lang.interferencePatterns.map((pattern) => (
                  <div key={pattern.category + pattern.example} className="bg-white dark:bg-neutral-900 rounded-xl p-5 border border-neutral-200/80 dark:border-neutral-800">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 mb-3">
                      {pattern.category}
                    </span>
                    <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-4">{pattern.description}</p>
                    <div className="grid sm:grid-cols-2 gap-3">
                      <div className="bg-red-50 dark:bg-red-900/20 rounded-xl p-3 border border-red-200/60 dark:border-red-800/40">
                        <p className="text-xs font-medium text-red-600 dark:text-red-400 mb-1">❌ Common Error</p>
                        <p className="text-sm text-red-800 dark:text-red-200">{pattern.example}</p>
                      </div>
                      <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-3 border border-green-200/60 dark:border-green-800/40">
                        <p className="text-xs font-medium text-green-600 dark:text-green-400 mb-1">✅ Correction</p>
                        <p className="text-sm text-green-800 dark:text-green-200">{pattern.correction}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-8 text-center">
              <Link
                href={`/l1/${lang.code}`}
                className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-primary-500 text-white hover:bg-primary-600 px-6 py-3 text-sm"
              >
                View Full {lang.name} Guide →
              </Link>
            </div>
          </Container>
        </Section>
      ))}
    </>
  );
}
