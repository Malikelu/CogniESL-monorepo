export interface L1Language {
  code: string;
  name: string;
  flag: string;
  speakers: string;
  commonErrors: string[];
  interferencePatterns: {
    category: string;
    description: string;
    example: string;
    correction: string;
  }[];
}

export const l1Languages: L1Language[] = [
  {
    code: "es",
    name: "Spanish",
    flag: "🇪🇸",
    speakers: "42M+ ESL students",
    commonErrors: [
      "Subject pronoun dropping (\"I went\" → \"Went\")",
      "Adjective after noun (\"car red\")",
      "False cognates (\"embarrassed\" → \"embarazada\")",
      "Double negatives (\"I don't know nothing\")",
      "Present perfect vs. simple past confusion",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Spanish often omits subject pronouns because verb conjugation indicates the subject.",
        example: '"Went to the store yesterday."',
        correction: '"I went to the store yesterday."',
      },
      {
        category: "Vocabulary",
        description: "False friends between Spanish and English cause confusion.",
        example: '"I am embarazada" (meaning "embarrassed")',
        correction: '"I am embarrassed." (embarazada = pregnant in Spanish)',
      },
      {
        category: "Pronunciation",
        description: "Spanish speakers often add a vowel before English words starting with 's'.",
        example: '"I go to eschool"',
        correction: '"I go to school."',
      },
    ],
  },
  {
    code: "zh",
    name: "Mandarin Chinese",
    flag: "🇨🇳",
    speakers: "35M+ ESL students",
    commonErrors: [
      "Article omission (\"I have book\")",
      "Tense marking (\"Yesterday I go\")",
      "Plural marking (\"two book\")",
      "Subject-verb agreement (\"He go\")",
      "Preposition errors (\"on the picture\")",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Mandarin has no articles (a, an, the), leading to omission.",
        example: '"I need book from library."',
        correction: '"I need a book from the library."',
      },
      {
        category: "Grammar",
        description: "Mandarin doesn't conjugate verbs for tense.",
        example: '"Yesterday I go to school."',
        correction: '"Yesterday I went to school."',
      },
      {
        category: "Pronunciation",
        description: "Mandarin speakers may confuse /l/ and /r/ sounds.",
        example: '"I have a rabbit" → "I have a labbit"',
        correction: 'Practice: "red, right, rice" vs. "led, light, lice"',
      },
    ],
  },
  {
    code: "ar",
    name: "Arabic",
    flag: "🇸🇦",
    speakers: "15M+ ESL students",
    commonErrors: [
      "Vowel omission in writing",
      "Definite article overuse (\"the life is beautiful\")",
      "Word order (VSO vs SVO)",
      "Preposition substitution",
      "Capitalization confusion",
    ],
    interferencePatterns: [
      {
        category: "Writing",
        description: "Arabic script often omits short vowels, carrying over to English writing.",
        example: '"I wnt to the str."',
        correction: '"I went to the store."',
      },
      {
        category: "Grammar",
        description: "Arabic uses 'al-' (the) more broadly than English.",
        example: '"The life is beautiful."',
        correction: '"Life is beautiful."',
      },
      {
        category: "Pronunciation",
        description: "Arabic lacks /p/ and /v/ phonemes in many dialects.",
        example: '"I bery much enjoy it"',
        correction: '"I very much enjoy it."',
      },
    ],
  },
  {
    code: "ko",
    name: "Korean",
    flag: "🇰🇷",
    speakers: "10M+ ESL students",
    commonErrors: [
      "Subject omission",
      "Plural marking",
      "Article usage",
      "Word order (SOV vs SVO)",
      "Final consonant clusters",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Korean is SOV (Subject-Object-Verb) while English is SVO.",
        example: '"I the book read."',
        correction: '"I read the book."',
      },
      {
        category: "Grammar",
        description: "Korean doesn't require plural markers in the same way.",
        example: '"I have two cat."',
        correction: '"I have two cats."',
      },
      {
        category: "Pronunciation",
        description: "Korean has fewer final consonant sounds.",
        example: '"I lik it" (dropping final consonants)',
        correction: '"I like it."',
      },
    ],
  },
  {
    code: "vi",
    name: "Vietnamese",
    flag: "🇻🇳",
    speakers: "8M+ ESL students",
    commonErrors: [
      "Tense marking",
      "Article usage",
      "Plural forms",
      "Preposition errors",
      "Tone transfer to English",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Vietnamese doesn't use verb conjugation for tense.",
        example: '"Yesterday I go market."',
        correction: '"Yesterday I went to the market."',
      },
      {
        category: "Pronunciation",
        description: "Vietnamese is tonal; speakers may apply tones to English.",
        example: "Rising intonation on statements",
        correction: "Practice falling intonation for statements.",
      },
    ],
  },
  {
    code: "pt",
    name: "Portuguese",
    flag: "🇧🇷",
    speakers: "6M+ ESL students",
    commonErrors: [
      "False cognates",
      "Pronoun placement",
      "Gerund overuse",
      "Article usage",
      "Subjunctive mood transfer",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Portuguese uses gerunds more frequently than English.",
        example: '"I am study English."',
        correction: '"I am studying English."',
      },
      {
        category: "Vocabulary",
        description: "False friends between Portuguese and English.",
        example: '"I am constipated" (meaning "congested")',
        correction: '"I have a stuffy nose."',
      },
    ],
  },
  {
    code: "ru",
    name: "Russian",
    flag: "🇷🇺",
    speakers: "5M+ ESL students",
    commonErrors: [
      "Article omission",
      "Verb aspect confusion",
      "Case system transfer",
      "Word order flexibility",
      "Preposition errors",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Russian has no articles, leading to omission in English.",
        example: '"I saw cat in garden."',
        correction: '"I saw a cat in the garden."',
      },
      {
        category: "Grammar",
        description: "Russian has perfective/imperfective verb aspects.",
        example: '"I was reading the book (but didn\'t finish)"',
        correction: '"I read the book" (completed) vs. "I was reading" (in progress)',
      },
    ],
  },
  {
    code: "ja",
    name: "Japanese",
    flag: "🇯🇵",
    speakers: "5M+ ESL students",
    commonErrors: [
      "Subject omission",
      "Article usage",
      "Plural marking",
      "Word order (SOV)",
      "L/R confusion",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Japanese is SOV and often omits subjects.",
        example: '"Went to store."',
        correction: '"I went to the store."',
      },
      {
        category: "Pronunciation",
        description: "Japanese doesn't distinguish /l/ and /r/.",
        example: '"I have a lice" (meaning "rice")',
        correction: 'Practice minimal pairs: light/right, lead/read',
      },
    ],
  },
  {
    code: "hi",
    name: "Hindi",
    flag: "🇮🇳",
    speakers: "4M+ ESL students",
    commonErrors: [
      "Article usage",
      "Word order",
      "Preposition errors",
      "Tense marking",
      "Retroflex consonants",
    ],
    interferencePatterns: [
      {
        category: "Grammar",
        description: "Hindi uses postpositions instead of prepositions.",
        example: '"I went store to."',
        correction: '"I went to the store."',
      },
      {
        category: "Pronunciation",
        description: "Hindi has retroflex consonants that transfer to English.",
        example: '"I tink so" (retroflex t)',
        correction: '"I think so."',
      },
    ],
  },
  {
    code: "tl",
    name: "Tagalog",
    flag: "🇵🇭",
    speakers: "3M+ ESL students",
    commonErrors: [
      "Article usage",
      "Verb focus system transfer",
      "Plural marking",
      "Preposition errors",
      "F/V and P/F confusion",
    ],
    interferencePatterns: [
      {
        category: "Pronunciation",
        description: "Tagalog speakers may interchange /f/ and /p/.",
        example: '"I am punny" (meaning "funny")',
        correction: '"I am funny."',
      },
      {
        category: "Grammar",
        description: "Tagalog has a focus system different from English.",
        example: '"The book was read by me" (overuse of passive)',
        correction: '"I read the book."',
      },
    ],
  },
];

export function getL1ByCode(code: string): L1Language | undefined {
  return l1Languages.find((l) => l.code === code);
}

export function getAllL1Codes(): string[] {
  return l1Languages.map((l) => l.code);
}
