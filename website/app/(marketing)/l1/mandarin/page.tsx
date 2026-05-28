import { createLanguagePage } from "../_template";

const lang = {
  code: "mandarin",
  name: "Mandarin Chinese",
  flag: "🇨🇳",
  patterns: 127,
  speakers: "3.4 million Chinese speakers in the US",
  overview: "Mandarin has no verb conjugation, no articles, and a tonal system. These fundamental differences create systematic interference patterns in grammar, pronunciation, and writing. Mandarin is the most spoken language in the world.",
  errors: [
    { error: "He go to school every day", correction: "He goes to school every day", explanation: "Chinese doesn't conjugate verbs for person/number. Third-person -s is consistently dropped.", category: "Verb Tense" },
    { error: "I very like it", correction: "I like it very much", explanation: "Chinese places 'very' before the verb; English places 'very much' after the object.", category: "Word Order" },
    { error: "There have many people", correction: "There are many people", explanation: "Chinese uses 'have' (有 yǒu) for existence; English uses 'there is/are'.", category: "Grammar" },
    { error: "She is my classmate in English", correction: "She is my English classmate", explanation: "Chinese places modifiers after the noun in some constructions.", category: "Word Order" },
    { error: "I learn English since 5 years", correction: "I have been learning English for 5 years", explanation: "Chinese uses simple present where English requires present perfect continuous.", category: "Verb Tense" },
    { error: "I have many homework", correction: "I have a lot of homework", explanation: "Chinese doesn't distinguish countable/uncountable nouns.", category: "Nouns" },
  ],
  tips: [
    "Drill third-person -s — it doesn't exist in Chinese and is the most common error",
    "Teach 'there is/are' vs 'have' — Chinese uses one word for both",
    "Practice English articles — Chinese has no article system",
    "Use tone awareness activities — Mandarin is tonal, English is stress-timed",
  ],
};

export const metadata = {
  title: "Mandarin L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Mandarin-speaking ESL students. 127 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
