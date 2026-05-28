import Link from "next/link";

interface AuthorBioProps {
  compact?: boolean;
}

export function AuthorBio({ compact = false }: AuthorBioProps) {
  if (compact) {
    return (
      <div className="flex items-center gap-3 mt-8 pt-6 border-t border-neutral-200 dark:border-neutral-800">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-bold text-sm">
          CM
        </div>
        <div>
          <p className="text-sm font-medium text-neutral-900 dark:text-neutral-100">Maria C.</p>
          <p className="text-xs text-neutral-500 dark:text-neutral-400">ESL Teacher · 20+ years in the classroom</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-primary-50 dark:bg-primary-900/20 border border-primary-200/60 dark:border-primary-800/40 rounded-2xl p-6 mt-10">
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary-400 to-accent-400 flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
          CM
        </div>
        <div>
          <h3 className="font-heading text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-1">
            Maria C.
          </h3>
          <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed mb-3">
            ESL teacher with over 20 years of experience teaching adult learners in community college and language school settings. Passionate about helping teachers spend less time prepping and more time teaching. Currently based in Texas, where she teaches a wonderfully mixed class of Spanish, Korean, and Arabic speakers.
          </p>
          <p className="text-xs text-neutral-500 dark:text-neutral-400">
            Follow along for practical tips, honest insights, and real talk about ESL teaching.
          </p>
        </div>
      </div>
    </div>
  );
}

interface BlogCTAProps {
  topic?: string;
}

export function BlogCTA({ topic }: BlogCTAProps) {
  return (
    <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl p-6 mt-8 text-center">
      <h3 className="font-heading text-lg font-semibold text-white mb-2">
        {topic ? `Ready to teach ${topic} with confidence?` : "Ready to get your weekends back?"}
      </h3>
      <p className="text-primary-100 text-sm mb-4">
        {topic
          ? `CogniESL creates materials specifically targeting ${topic} for your students' L1 background.`
            : "Join the waitlist and be first to know when CogniESL launches."}
      </p>
      <Link
        href="/#waitlist"
        className="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 bg-white text-primary-700 hover:bg-primary-50 px-6 py-3 text-sm"
      >
        Join the Waitlist — It&apos;s Free
      </Link>
    </div>
  );
}
