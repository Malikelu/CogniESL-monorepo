import { createLanguagePage } from "../_template";

const lang = {
  code: "french",
  name: "French",
  flag: "🇫🇷",
  patterns: 71,
  speakers: "1.3 million French speakers in the US",
  overview: "French and English share many cognates due to Norman influence, but differ significantly in verb tense usage, article usage, and word order. French has grammatical gender, which doesn't exist in English.",
  errors: [
    { error: "She is doctor", correction: "She is a doctor", explanation: "French omits indefinite articles before professions, similar to Spanish.", category: "Articles" },
    { error: "I go to home", correction: "I go home", explanation: "French uses 'à la maison' (to the home) where English drops the preposition.", category: "Prepositions" },
    { error: "He don't like it", correction: "He doesn't like it", explanation: "French negation structure differs from English.", category: "Verb Tense" },
    { error: "I have 20 years", correction: "I am 20 years old", explanation: "French uses 'avoir' (to have) for age, not 'être' (to be).", category: "Grammar" },
    { error: "She is more taller", correction: "She is taller", explanation: "French double-marking of comparatives transfers to English.", category: "Grammar" },
    { error: "I learn since 3 years", correction: "I have been learning for 3 years", explanation: "French uses present tense with 'depuis' where English requires present perfect.", category: "Verb Tense" },
  ],
  tips: [
    "Leverage cognates — French and English share thousands of words",
    "Watch for false friends — 'library' (bibliothèque ≠ librairie), 'actually' (actuellement ≠ currently)",
    "Teach article usage — French articles are used differently than English",
    "Practice pronunciation — French has nasal vowels and silent letters",
  ],
};

export const metadata = {
  title: "French L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by French-speaking ESL students. 71 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
