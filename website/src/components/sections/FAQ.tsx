"use client";
import { Container } from "@/components/ui/Container";
import { useState } from "react";
import { cn } from "@/lib/utils";

const faqs = [
  {
    question: "Is it really tailored to my students' native language?",
    answer: "Yes — this is the whole product. CogniESL doesn't generate generic grammar exercises. For every request, it reads from a dedicated L1 interference database for that specific language. Spanish speakers get slides that call out the preterite transfer error. Korean speakers get exercises designed around a language with no article system. Arabic speakers get materials that address tense backshifting in conditionals. The L1 specificity is not a feature. It's the foundation.",
  },
  {
    question: "What formats do I actually get?",
    answer: "Three formats, every time: (1) A PowerPoint slide deck (15–18 slides) with CCQs, formation rules, L1-specific error slides, practice activities, and full speaker notes. (2) A printable worksheet with 5 graded sections (A–E) and a complete answer key that explains why each answer is correct — including the L1 reason. (3) A step-by-step activity guide with teacher script, timing, and differentiation tips for different levels. All delivered to your email.",
  },
  {
    question: "How long does it take?",
    answer: "Your request takes 2–3 minutes to set up — just describe your class in plain language. Generation happens in the background. You'll get your materials in your inbox, typically within a few minutes. You don't wait at a loading screen. You go make coffee.",
  },
  {
    question: "How is this different from using ChatGPT?",
    answer: "ChatGPT doesn't know that Korean has no article system. It doesn't have a 36-language database of validated L1 interference patterns. It doesn't produce PPTX files, printable worksheets, or activity guides. And it invents grammar — CogniESL reads from a 302-file academic database, so nothing is made up. The output of CogniESL is a complete, formatted, classroom-ready lesson set. Not a block of text you have to format yourself.",
  },
  {
    question: "Do I need to know my students' native language?",
    answer: "Not at all. You tell CogniESL what language your students speak — CogniESL handles the rest. You don't need to know any linguistics. In fact, most teachers say using CogniESL teaches them more about their students' language backgrounds over time. Think of it as a linguistics expert working alongside you.",
  },
  {
    question: "Can I use the materials as-is in class?",
    answer: "Yes. Materials are designed to be classroom-ready without editing. That said, you know your students best — we recommend a quick review before use, not because quality is a concern, but because you may want to personalise a detail or two. Most teachers use them as-is, or with minor tweaks.",
  },
  {
    question: "What L1 languages are covered?",
    answer: "36 languages including Spanish, Korean, Mandarin, Arabic, Japanese, Portuguese, Russian, Vietnamese, Hindi, French, German, Tagalog, and more. Each language has a dedicated database covering grammar, vocabulary, pronunciation, and pragmatics interference. New languages are added based on teacher demand.",
  },
  {
    question: "Is student data protected?",
    answer: "Completely. CogniESL never collects, stores, or processes student information. You describe your lesson needs in general terms (e.g., 'Spanish-speaking B1 adults, present perfect'). No student names, no student work, no student data of any kind. Fully FERPA compliant.",
  },
];

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section id="faq" className="py-20 lg:py-28 bg-white dark:bg-neutral-900">
      <Container>
        <div className="max-w-3xl mx-auto text-center mb-14">
          <span className="inline-block px-4 py-1.5 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-semibold mb-4">
            FAQ
          </span>
          <h2 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 dark:text-neutral-50 mb-6 leading-tight">
            Questions teachers{" "}
            <span className="gradient-text">actually ask.</span>
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400">
            Honest answers. No marketing fluff.
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-2">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className="border border-neutral-200/80 dark:border-neutral-800 rounded-xl overflow-hidden"
            >
              <button
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-neutral-50 dark:hover:bg-neutral-800/50 transition-colors"
              >
                <span className="font-semibold text-neutral-900 dark:text-neutral-100 pr-4 text-sm md:text-base">
                  {faq.question}
                </span>
                <svg
                  className={cn(
                    "w-5 h-5 text-neutral-400 flex-shrink-0 transition-transform duration-200",
                    openIndex === i && "rotate-180"
                  )}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {openIndex === i && (
                <div className="px-5 pb-5 animate-fade-in border-t border-neutral-100 dark:border-neutral-800/60 pt-4">
                  <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed text-sm md:text-base">
                    {faq.answer}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="text-center mt-10">
          <p className="text-neutral-500 dark:text-neutral-400 text-sm">
            Still have questions?{" "}
            <a href="/contact" className="text-primary-600 dark:text-primary-400 font-medium hover:underline">
              Write to us
            </a>
            {" "}— we actually reply.
          </p>
        </div>
      </Container>
    </section>
  );
}
