import { Container } from "@/components/ui/Container";

const testimonials = [
  {
    quote: "I've been teaching ESL for 11 years and have never seen a tool that actually understands L1 interference. The Spanish section alone is worth it — it catches errors I spent years figuring out myself.",
    name: "Raquel M.",
    role: "ESL Coordinator, Community College · Texas",
    initials: "RM",
    color: "bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300",
    stars: 5,
  },
  {
    quote: "I teach adult learners from 6 different countries in the same class. CogniESL is the only prep tool I've found that doesn't make me choose — I run the same topic for Spanish AND Korean speakers and get genuinely different, targeted materials for each.",
    name: "David K.",
    role: "ESOL Teacher, Adult Education Center · Illinois",
    initials: "DK",
    color: "bg-accent-100 dark:bg-accent-900/40 text-accent-700 dark:text-accent-300",
    stars: 5,
  },
  {
    quote: "The answer keys explain why the correct answer is correct. That's the part my students actually learn from. I've been writing that structure manually for years — now it just happens.",
    name: "Priya S.",
    role: "Private ESL Tutor · California",
    initials: "PS",
    color: "bg-secondary-100 dark:bg-secondary-900/40 text-secondary-700 dark:text-secondary-300",
    stars: 5,
  },
];

function Stars({ count }: { count: number }) {
  return (
    <div className="flex gap-0.5 mb-3">
      {Array.from({ length: count }).map((_, i) => (
        <svg key={i} className="w-4 h-4 text-accent-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </div>
  );
}

export function SocialProof() {
  return (
    <section className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-950">
      <Container>
        {/* Testimonials heading */}
        <div className="max-w-3xl mx-auto text-center mb-12">
          <span className="inline-block px-4 py-1.5 rounded-full bg-success-100 dark:bg-success-900/30 text-success-700 dark:text-success-300 text-sm font-semibold mb-4">
            From beta testers
          </span>
          <h2 className="font-heading text-3xl md:text-4xl font-bold text-neutral-900 dark:text-neutral-50 mb-4 leading-tight">
            Teachers who tried it{" "}
            <span className="gradient-text">won&apos;t go back.</span>
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400">
            CogniESL is in private beta. Here&apos;s what early testers are saying.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-5 max-w-5xl mx-auto mb-16">
          {testimonials.map((t) => (
            <div
              key={t.name}
              className="bg-white dark:bg-neutral-900 rounded-2xl p-6 border border-neutral-200/80 dark:border-neutral-800 flex flex-col hover:shadow-card-hover hover:-translate-y-0.5 transition-all duration-300"
            >
              <Stars count={t.stars} />
              <div className="text-2xl text-neutral-200 dark:text-neutral-700 font-serif leading-none mb-3">&ldquo;</div>
              <p className="text-neutral-700 dark:text-neutral-300 text-sm leading-relaxed flex-1 mb-5">
                {t.quote}
              </p>
              <div className="flex items-center gap-3 border-t border-neutral-100 dark:border-neutral-800 pt-4">
                <div className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${t.color}`}>
                  {t.initials}
                </div>
                <div>
                  <div className="text-sm font-semibold text-neutral-900 dark:text-neutral-100">{t.name}</div>
                  <div className="text-xs text-neutral-500 dark:text-neutral-400">{t.role}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats bar */}
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 lg:gap-8 text-center border-t border-neutral-200 dark:border-neutral-800 pt-12">
          {[
            { value: "36", label: "L1 Languages", sub: "Interference patterns" },
            { value: "302", label: "Grammar Files", sub: "Academic-validated" },
            { value: "220", label: "Activity Templates", sub: "Classroom-ready" },
            { value: "< 5 min", label: "To request materials", sub: "No forms, just chat" },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="font-heading text-3xl md:text-4xl font-bold gradient-text mb-1">
                {stat.value}
              </div>
              <div className="font-semibold text-neutral-900 dark:text-neutral-100 text-sm mb-0.5">
                {stat.label}
              </div>
              <div className="text-xs text-neutral-500 dark:text-neutral-400">
                {stat.sub}
              </div>
            </div>
          ))}
        </div>

        {/* Trust line */}
        <div className="max-w-3xl mx-auto text-center mt-10">
          <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-5">
            Used by ESL teachers across
          </p>
          <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-3 opacity-60">
            {["Public Schools", "Community Colleges", "Language Institutes", "Private Tutors", "Adult Education"].map((org) => (
              <div key={org} className="text-sm font-medium text-neutral-400 dark:text-neutral-500">
                {org}
              </div>
            ))}
          </div>
        </div>
      </Container>
    </section>
  );
}
