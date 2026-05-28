import { Container } from "@/components/ui/Container";

const pains = [
  {
    before: "Sunday night. Class tomorrow. Two hours of slide-making ahead.",
    after: "Request submitted in 2 minutes. Materials in your inbox.",
    icon: "⏰",
    label: "5–10 hrs/week saved",
  },
  {
    before: "Generic worksheet that treats \"he walk\" the same for every student.",
    after: "Slide that says: Spanish speakers — this is why you do this.",
    icon: "🎯",
    label: "L1-specific every time",
  },
  {
    before: "You correct the same error 40 times and wonder why it doesn't stick.",
    after: "Materials that explain the linguistic reason — so errors stop recurring.",
    icon: "🧠",
    label: "Rooted in real linguistics",
  },
  {
    before: "Three different L1s in one class. One generic lesson for all of them.",
    after: "Run the same topic for Spanish AND Korean — get genuinely different materials.",
    icon: "🌍",
    label: "Multi-L1 in one request",
  },
];

export function Problem() {
  return (
    <section id="problem" className="py-20 lg:py-28 bg-white dark:bg-neutral-900">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            You already know your students&apos; mistakes.
            <br />
            <span className="gradient-text-warm">Your slides don&apos;t.</span>
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed max-w-2xl mx-auto">
            You&apos;ve been correcting &ldquo;He walk to school&rdquo; for three years. You know it&apos;s a Spanish speaker problem.
            But every worksheet you grab from Google was written for a student who doesn&apos;t exist — someone with no native language at all.
          </p>
        </div>

        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-4">
          {pains.map((item) => (
            <div
              key={item.before}
              className="group bg-neutral-50 dark:bg-neutral-800/50 rounded-2xl p-6 border border-neutral-200/80 dark:border-neutral-700/60 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-card-hover transition-all duration-300"
            >
              <div className="flex items-start gap-4">
                <div className="text-2xl flex-shrink-0 mt-0.5">{item.icon}</div>
                <div className="flex-1">
                  {/* Before */}
                  <p className="text-sm text-neutral-500 dark:text-neutral-400 leading-relaxed mb-3 line-through decoration-secondary-300 dark:decoration-secondary-600">
                    {item.before}
                  </p>
                  {/* After */}
                  <p className="text-sm font-medium text-neutral-800 dark:text-neutral-200 leading-relaxed mb-3">
                    {item.after}
                  </p>
                  <span className="inline-block text-xs font-bold text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/30 px-2.5 py-1 rounded-full">
                    {item.label}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stat strip */}
        <div className="mt-14 max-w-3xl mx-auto grid grid-cols-3 gap-6 text-center border-t border-neutral-200 dark:border-neutral-800 pt-12">
          {[
            { value: "302", label: "Grammar topics in the database" },
            { value: "36", label: "L1 native languages covered" },
            { value: "220", label: "Activity templates included" },
          ].map((s) => (
            <div key={s.label}>
              <div className="font-heading text-3xl md:text-4xl font-bold gradient-text mb-1">{s.value}</div>
              <div className="text-xs text-neutral-500 dark:text-neutral-400 leading-snug">{s.label}</div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
