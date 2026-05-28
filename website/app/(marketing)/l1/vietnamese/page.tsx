import { createLanguagePage } from "../_template";

const lang = {
  code: "vietnamese",
  name: "Vietnamese",
  flag: "🇻🇳",
  patterns: 76,
  speakers: "1.1 million Vietnamese speakers in the US",
  overview: "Vietnamese is a tonal language with no verb conjugation, no articles, and a classifier system. These create unique interference patterns in English. Vietnamese uses a Latin-based script with diacritics, which is different from Chinese characters.",
  errors: [
    { error: "I very like it", correction: "I like it very much", explanation: "Vietnamese places 'very' before the verb, similar to Chinese.", category: "Word Order" },
    { error: "She is more beautiful than all", correction: "She is the most beautiful", explanation: "Vietnamese comparative structure differs from English superlative.", category: "Grammar" },
    { error: "I go to school by foot", correction: "I go to school on foot", explanation: "Vietnamese uses 'by' for all transportation modes.", category: "Prepositions" },
    { error: "He go to school every day", correction: "He goes to school every day", explanation: "Vietnamese doesn't conjugate verbs for person/number.", category: "Verb Tense" },
    { error: "I have many homework", correction: "I have a lot of homework", explanation: "Vietnamese doesn't distinguish countable/uncountable nouns.", category: "Nouns" },
    { error: "I learn English since 5 years", correction: "I have been learning English for 5 years", explanation: "Vietnamese uses simple present where English requires present perfect.", category: "Verb Tense" },
  ],
  tips: [
    "Drill third-person -s — it doesn't exist in Vietnamese",
    "Teach articles — Vietnamese has no article system",
    "Practice English stress patterns — Vietnamese is tonal",
    "Use visual aids for prepositions — Vietnamese prepositions differ significantly",
  ],
};

export const metadata = {
  title: "Vietnamese L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Vietnamese-speaking ESL students. 76 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
