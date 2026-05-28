import { createLanguagePage } from "../_template";

const lang = {
  code: "tagalog",
  name: "Tagalog",
  flag: "🇵🇭",
  patterns: 59,
  speakers: "1.7 million Filipino speakers in the US",
  overview: "Tagalog has a verb-initial sentence structure, no articles in the same sense as English, and a focus system that differs from English subject-prominence. Many Filipino speakers are bilingual in English and Tagalog.",
  errors: [
    { error: "I am already eat", correction: "I already ate", explanation: "Tagalog 'na' (already) is placed before the verb, causing word order confusion.", category: "Word Order" },
    { error: "She is my classmate in English", correction: "She is my English classmate", explanation: "Tagalog places modifiers after the noun.", category: "Word Order" },
    { error: "I will go to the market for buy vegetables", correction: "I will go to the market to buy vegetables", explanation: "Tagalog uses 'para for' where English uses 'to'.", category: "Grammar" },
    { error: "He go to school every day", correction: "He goes to school every day", explanation: "Tagalog doesn't conjugate verbs for person/number.", category: "Verb Tense" },
    { error: "I have many homework", correction: "I have a lot of homework", explanation: "Tagalog doesn't distinguish countable/uncountable nouns.", category: "Nouns" },
    { error: "I learn English since 5 years", correction: "I have been learning English for 5 years", explanation: "Tagalog uses simple present where English requires present perfect.", category: "Verb Tense" },
  ],
  tips: [
    "Teach SVO word order — Tagalog is often verb-initial",
    "Focus on articles — Tagalog doesn't have articles in the same way as English",
    "Practice verb conjugation — Tagalog doesn't conjugate for person/number",
    "Use contrastive analysis — show Tagalog vs English grammar side by side",
  ],
};

export const metadata = {
  title: "Tagalog L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Tagalog-speaking ESL students. 59 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
