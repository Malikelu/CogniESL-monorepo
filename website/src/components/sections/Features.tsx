import { Container } from "@/components/ui/Container";

const features = [
  {
    icon: "🎯",
    title: "L1 Intelligence — the feature no one else has",
    description: "36 native languages. Each one a dedicated database of interference patterns, linguistic explanations, example errors, and teacher tips. This isn't translation — it's the science of why your students make the mistakes they make.",
    highlight: true,
    tag: "Core differentiator",
  },
  {
    icon: "📊",
    title: "Slide decks that teach themselves",
    description: "15–18 PPTX slides with CCQs before formulas, L1-specific callout slides in red/green, visual grammar anchors, and speaker notes for every slide. Download. Open. Teach.",
  },
  {
    icon: "📝",
    title: "Worksheets with answer keys that explain why",
    description: "5 sections (A–E) of graded exercises targeting your students' specific error patterns. The answer key doesn't just give answers — it explains the L1 reason. That's the part students actually learn from.",
  },
  {
    icon: "🎮",
    title: "Activity guides with teacher scripts",
    description: "Step-by-step classroom activities with exact words to say, timing guides, and differentiation notes for lower/higher levels. Walk in and run it.",
  },
  {
    icon: "🔬",
    title: "Zero AI-generated grammar",
    description: "Every grammar rule, every CCQ, every error pattern comes from a 302-file validated academic database. CogniESL reads from research. It doesn't invent linguistics.",
  },
  {
    icon: "📬",
    title: "Request and walk away",
    description: "Describe your lesson, hit send. Materials generate in the background and land in your inbox. No waiting at a loading screen.",
  },
];

export function Features() {
  return (
    <section id="features" className="py-20 lg:py-28 bg-white dark:bg-neutral-900">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-16">
          <span className="inline-block px-4 py-1.5 rounded-full bg-accent-100 dark:bg-accent-900/30 text-accent-700 dark:text-accent-300 text-sm font-semibold mb-4">
            What you get
          </span>
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            Not just another AI tool.
            <br />
            <span className="gradient-text">A tool built for your students.</span>
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed">
            CogniESL was designed around one insight: great ESL materials aren&apos;t just about English.
            They&apos;re about the bridge between your students&apos; language and English.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 max-w-6xl mx-auto">
          {features.map((feature) => (
            <div
              key={feature.title}
              className={`rounded-2xl p-6 border transition-all duration-300 hover:-translate-y-0.5 ${
                feature.highlight
                  ? "bg-gradient-to-br from-primary-600 to-primary-700 border-primary-500 shadow-glow lg:col-span-3 md:col-span-2"
                  : "bg-neutral-50 dark:bg-neutral-800/50 border-neutral-200/80 dark:border-neutral-700/60 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-card-hover"
              }`}
            >
              {feature.highlight ? (
                <div className="flex flex-col md:flex-row md:items-start gap-6">
                  <div className="text-4xl flex-shrink-0">{feature.icon}</div>
                  <div>
                    <div className="inline-block text-xs font-bold text-primary-200 bg-white/10 px-3 py-1 rounded-full mb-3">
                      {(feature as { icon: string; title: string; description: string; highlight: boolean; tag: string }).tag}
                    </div>
                    <h3 className="font-heading text-2xl font-bold text-white mb-3 leading-snug">
                      {feature.title}
                    </h3>
                    <p className="text-primary-100 leading-relaxed max-w-3xl">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="flex items-start gap-4">
                  <div className="text-2xl flex-shrink-0 mt-0.5">{feature.icon}</div>
                  <div>
                    <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-1.5">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Comparison strip */}
        <div className="max-w-4xl mx-auto mt-16">
          <h3 className="font-heading text-xl font-bold text-center text-neutral-900 dark:text-neutral-100 mb-8">
            CogniESL vs. doing it yourself
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-neutral-50 dark:bg-neutral-800/50 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-6 h-6 rounded-full bg-neutral-300 dark:bg-neutral-600 flex items-center justify-center">
                  <span className="text-xs font-bold text-neutral-600 dark:text-neutral-300">✕</span>
                </div>
                <span className="font-semibold text-neutral-700 dark:text-neutral-300">Manual prep</span>
              </div>
              <ul className="space-y-2.5 text-sm text-neutral-500 dark:text-neutral-400">
                {[
                  "5–10 hours per lesson set",
                  "Generic content that misses L1-specific errors",
                  "No answer key explanations",
                  "Google for activities, format manually",
                  "Hope it works in class",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <span className="text-secondary-400 flex-shrink-0 mt-0.5">✕</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-primary-50 dark:bg-primary-900/20 rounded-2xl p-6 border border-primary-200 dark:border-primary-800">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-6 h-6 rounded-full bg-primary-500 flex items-center justify-center">
                  <span className="text-xs font-bold text-white">✓</span>
                </div>
                <span className="font-semibold text-primary-800 dark:text-primary-200">CogniESL</span>
              </div>
              <ul className="space-y-2.5 text-sm text-neutral-700 dark:text-neutral-300">
                {[
                  "2-minute request, materials in your inbox",
                  "L1-specific error slides built in for every language",
                  "Answer key explains the linguistic why",
                  "220 research-backed activities, pre-formatted",
                  "Teacher-tested structure, ready to open and use",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <span className="text-success-600 dark:text-success-400 flex-shrink-0 mt-0.5">✓</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
