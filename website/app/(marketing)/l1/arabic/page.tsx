import { createLanguagePage } from "../_template";

const lang = {
  code: "arabic",
  name: "Arabic",
  flag: "🇸🇦",
  patterns: 115,
  speakers: "1.2 million Arabic speakers in the US",
  overview: "Arabic has a rich morphological system that differs significantly from English. Key interference areas include definite articles, verb conjugation, and the absence of certain English sounds. Arabic is written right-to-left, which affects reading patterns.",
  errors: [
    { error: "The life is beautiful", correction: "Life is beautiful", explanation: "Arabic uses the definite article 'al-' more broadly than English 'the'.", category: "Articles" },
    { error: "I want that you come", correction: "I want you to come", explanation: "Arabic uses conjunction 'that' where English uses infinitive 'to'.", category: "Grammar" },
    { error: "He didn't went", correction: "He didn't go", explanation: "Arabic past tense negation doesn't require the main verb to change form.", category: "Verb Tense" },
    { error: "I have 30 years", correction: "I am 30 years old", explanation: "Arabic uses 'have' for age, similar to Romance languages.", category: "Grammar" },
    { error: "She is more taller", correction: "She is taller", explanation: "Arabic double-marking of comparatives transfers to English.", category: "Grammar" },
    { error: "I go to home", correction: "I go home", explanation: "Arabic uses 'to' with 'home' where English drops the preposition.", category: "Prepositions" },
  ],
  tips: [
    "Focus on article usage — Arabic 'al-' is used more broadly than English 'the'",
    "Teach verb negation patterns — Arabic doesn't change the main verb after 'didn't'",
    "Practice English sounds that don't exist in Arabic (p, v, g)",
    "Use contrastive analysis — show Arabic vs English side by side",
  ],
};

export const metadata = {
  title: "Arabic L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Arabic-speaking ESL students. 115 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
