"use client";
import { Container } from "@/components/ui/Container";

import { useState } from "react";

const l1Languages = [
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

const interferenceExamples: Record<string, { error: string; correction: string; explanation: string }[]> = {
  es: [
    { error: "I am agree", correction: "I agree", explanation: "Spanish 'estar de acuerdo' literally translates to 'to be of agreement' — students transfer the 'ser/estar' structure." },
    { error: "I have 25 years", correction: "I am 25 years old", explanation: "Spanish uses 'tener' (to have) for age, not 'ser/estar' (to be)." },
    { error: "She is doctor", correction: "She is a doctor", explanation: "Spanish omits indefinite articles before professions." },
  ],
  ko: [
    { error: "I went to store yesterday", correction: "I went to the store yesterday", explanation: "Korean has no article system. Students must learn to add a/an/the where none exists in their L1." },
    { error: "He eat lunch now", correction: "He is eating lunch now", explanation: "Korean doesn't mark progressive aspect with auxiliary verbs like English 'be + -ing'." },
    { error: "I have many homework", correction: "I have a lot of homework", explanation: "Korean doesn't distinguish countable/uncountable nouns the way English does." },
  ],
  ar: [
    { error: "The life is beautiful", correction: "Life is beautiful", explanation: "Arabic uses the definite article 'al-' more broadly than English 'the'." },
    { error: "I want that you come", correction: "I want you to come", explanation: "Arabic uses conjunction 'that' where English uses infinitive 'to'." },
    { error: "He didn't went", correction: "He didn't go", explanation: "Arabic past tense negation doesn't require the main verb to change form." },
  ],
  zh: [
    { error: "He go to school every day", correction: "He goes to school every day", explanation: "Chinese doesn't conjugate verbs for person/number. Third-person -s is consistently dropped." },
    { error: "I very like it", correction: "I like it very much", explanation: "Chinese places 'very' before the verb; English places 'very much' after the object." },
    { error: "There have many people", correction: "There are many people", explanation: "Chinese uses 'have' (有 yǒu) for existence; English uses 'there is/are'." },
  ],
  ja: [
    { error: "I am agree", correction: "I agree", explanation: "Japanese 'soudesu' (that's right) structure transfers to English as 'I am agree'." },
    { error: "She is my friend good", correction: "She is my good friend", explanation: "Japanese places adjectives after the noun in some constructions." },
    { error: "I came to America since 3 years", correction: "I came to America 3 years ago", explanation: "Japanese uses 'since' differently for time expressions." },
  ],
  pt: [
    { error: "I am 20 years", correction: "I am 20 years old", explanation: "Portuguese uses 'tenho' (I have) for age, similar to Spanish." },
    { error: "She is my sister of heart", correction: "She is my best friend", explanation: "Portuguese 'irmã de coração' (sister of heart) is a common expression that doesn't translate directly." },
    { error: "I go to the beach in the weekend", correction: "I go to the beach on the weekend", explanation: "Portuguese uses 'no' (in the) where English uses 'on'." },
  ],
  ru: [
    { error: "I am agree", correction: "I agree", explanation: "Russian 'ya soglasen' (I am in agreement) transfers the 'to be' structure to English." },
    { error: "She is more taller", correction: "She is taller", explanation: "Russian double-marking of comparatives transfers to English." },
    { error: "I have 30 years", correction: "I am 30 years old", explanation: "Russian uses 'have' for age, similar to Romance languages." },
  ],
  vi: [
    { error: "I very like it", correction: "I like it very much", explanation: "Vietnamese places 'very' before the verb, similar to Chinese." },
    { error: "She is more beautiful than all", correction: "She is the most beautiful", explanation: "Vietnamese comparative structure differs from English superlative." },
    { error: "I go to school by foot", correction: "I go to school on foot", explanation: "Vietnamese uses 'by' for all transportation modes." },
  ],
  hi: [
    { error: "He is having a car", correction: "He has a car", explanation: "Hindi uses progressive tense for possession where English uses simple present." },
    { error: "I am knowing the answer", correction: "I know the answer", explanation: "Hindi uses progressive for stative verbs where English doesn't." },
    { error: "She is my cousin sister", correction: "She is my cousin", explanation: "Hindi specifies gender for all family relations." },
  ],
  fr: [
    { error: "I am 20 years old", correction: "I am 20 years old", explanation: "French uses the same structure, but 'J'ai 20 ans' (I have 20 years) causes confusion." },
    { error: "She is doctor", correction: "She is a doctor", explanation: "French omits indefinite articles before professions, similar to Spanish." },
    { error: "I go to home", correction: "I go home", explanation: "French uses 'à la maison' (to the home) where English drops the preposition." },
  ],
  de: [
    { error: "I go to home", correction: "I go home", explanation: "German 'Ich gehe nach Hause' (I go to home) transfers the preposition." },
    { error: "She has 20 years", correction: "She is 20 years old", explanation: "German uses 'haben' (to have) for age, similar to Romance languages." },
    { error: "I learn since 3 years", correction: "I have been learning for 3 years", explanation: "German uses present tense with 'seit' where English requires present perfect." },
  ],
  tl: [
    { error: "I am already eat", correction: "I already ate", explanation: "Tagalog 'na' (already) is placed before the verb, causing word order confusion." },
    { error: "She is my classmate in English", correction: "She is my English classmate", explanation: "Tagalog places modifiers after the noun." },
    { error: "I will go to the market for buy vegetables", correction: "I will go to the market to buy vegetables", explanation: "Tagalog uses 'para for' where English uses 'to'." },
  ],
};

export function L1Explorer() {
  const [selected, setSelected] = useState("es");
  const examples = interferenceExamples[selected] || interferenceExamples.es;
  const lang = l1Languages.find((l) => l.code === selected);

  return (
    <section id="l1-explorer" className="py-20 lg:py-28 bg-neutral-50 dark:bg-neutral-950">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-14">
          <span className="inline-block px-4 py-1.5 rounded-full bg-secondary-100 dark:bg-secondary-900/30 text-secondary-700 dark:text-secondary-300 text-sm font-semibold mb-4">
            Live preview — the L1 database
          </span>
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            Pick a language. See what{" "}
            <span className="gradient-text-warm">your students get wrong</span> — and why.
          </h2>
          <p className="text-lg text-neutral-600 dark:text-neutral-400 leading-relaxed">
            These aren&apos;t guesses. Every pattern comes from peer-reviewed linguistic research.
            CogniESL uses this database to build your materials — so your lessons target the right errors.
          </p>
        </div>

        {/* Language selector */}
        <div className="flex flex-wrap justify-center gap-2 mb-10 max-w-4xl mx-auto">
          {l1Languages.map((l) => (
            <button
              key={l.code}
              onClick={() => setSelected(l.code)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                selected === l.code
                  ? "bg-primary-500 text-white shadow-glow"
                  : "bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-300 hover:bg-primary-100 dark:hover:bg-primary-900/30"
              }`}
            >
              {l.flag} {l.name}
            </button>
          ))}
        </div>

        {/* Examples */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-gradient-to-br from-neutral-50 to-primary-50/30 dark:from-neutral-800 dark:to-neutral-800 rounded-2xl p-6 lg:p-8 border border-neutral-200/80 dark:border-neutral-700/60">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-neutral-200/60 dark:border-neutral-700/60">
              <span className="text-3xl">{lang?.flag}</span>
              <div>
                <h3 className="font-heading text-xl font-semibold text-neutral-900 dark:text-neutral-100">
                  {lang?.name} → English
                </h3>
                <p className="text-sm text-neutral-500 dark:text-neutral-400">
                  {lang?.patterns} interference patterns identified
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {examples.map((ex, i) => (
                <div
                  key={i}
                  className="bg-white dark:bg-neutral-900 rounded-xl p-4 border border-neutral-200/80 dark:border-neutral-700/60"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-base mt-0.5 flex-shrink-0">❌</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-neutral-400 dark:text-neutral-500 line-through text-sm">{ex.error}</p>
                      <p className="text-success-600 dark:text-success-400 font-medium text-sm mt-0.5">✅ {ex.correction}</p>
                      <p className="text-neutral-600 dark:text-neutral-300 text-sm mt-1.5 leading-relaxed">
                        💡 {ex.explanation}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* CTA after explorer */}
        <div className="text-center mt-10">
          <p className="text-neutral-500 dark:text-neutral-400 text-sm mb-4">
            These patterns are built into every material CogniESL generates for {l1Languages.find(l => l.code === "es")?.name} speakers — and 35 other L1s.
          </p>
          <a
            href="#waitlist"
            className="inline-flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-bold px-6 py-3 rounded-xl transition-colors shadow-sm"
          >
            Generate materials for my students
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>
      </Container>
    </section>
  );
}
