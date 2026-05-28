import { createLanguagePage } from "../_template";

const lang = {
  code: "portuguese",
  name: "Portuguese",
  flag: "🇧🇷",
  patterns: 89,
  speakers: "1.3 million Portuguese speakers in the US",
  overview: "Portuguese shares many features with Spanish but has unique interference patterns, particularly in pronunciation, false friends, and the use of personal infinitives. Brazilian and European Portuguese have notable differences.",
  errors: [
    { error: "I am 20 years", correction: "I am 20 years old", explanation: "Portuguese uses 'tenho' (I have) for age, similar to Spanish.", category: "Grammar" },
    { error: "I go to the beach in the weekend", correction: "I go to the beach on the weekend", explanation: "Portuguese uses 'no' (in the) where English uses 'on'.", category: "Prepositions" },
    { error: "She is my sister of heart", correction: "She is my best friend", explanation: "Portuguese 'irmã de coração' doesn't translate directly.", category: "Vocabulary" },
    { error: "He is more taller", correction: "He is taller", explanation: "Portuguese double-marking of comparatives transfers to English.", category: "Grammar" },
    { error: "I want that you come", correction: "I want you to come", explanation: "Portuguese uses 'que' (that) where English uses infinitive 'to'.", category: "Grammar" },
    { error: "I go to home", correction: "I go home", explanation: "Portuguese uses 'para casa' (to home) where English drops the preposition.", category: "Prepositions" },
  ],
  tips: [
    "Watch for false friends — Portuguese and English share many look-alikes with different meanings",
    "Focus on preposition usage — Portuguese prepositions don't map 1:1 to English",
    "Teach the difference between 'ser' and 'estar' as it maps to English 'to be'",
    "Practice pronunciation — Portuguese has nasal vowels that don't exist in English",
  ],
};

export const metadata = {
  title: "Portuguese L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Portuguese-speaking ESL students. 89 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
