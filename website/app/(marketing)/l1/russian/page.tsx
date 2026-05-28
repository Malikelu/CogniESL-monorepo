import { createLanguagePage } from "../_template";

const lang = {
  code: "russian",
  name: "Russian",
  flag: "🇷🇺",
  patterns: 94,
  speakers: "1.5 million Russian speakers in the US",
  overview: "Russian has a complex case system, no articles, and different verb aspects. These create systematic interference patterns in English grammar. Russian uses the Cyrillic alphabet, which affects reading and writing transfer.",
  errors: [
    { error: "She is more taller", correction: "She is taller", explanation: "Russian double-marking of comparatives transfers to English.", category: "Grammar" },
    { error: "I have 30 years", correction: "I am 30 years old", explanation: "Russian uses 'have' for age, similar to Romance languages.", category: "Grammar" },
    { error: "I went to store yesterday", correction: "I went to the store yesterday", explanation: "Russian has no article system. Articles must be explicitly taught.", category: "Articles" },
    { error: "He don't like it", correction: "He doesn't like it", explanation: "Russian doesn't conjugate verbs for person in the same way as English.", category: "Verb Tense" },
    { error: "I go to home", correction: "I go home", explanation: "Russian uses 'to' with 'home' where English drops the preposition.", category: "Prepositions" },
    { error: "I learn since 3 years", correction: "I have been learning for 3 years", explanation: "Russian uses present tense with 'since' where English requires present perfect.", category: "Verb Tense" },
  ],
  tips: [
    "Start with articles — Russian has no article system",
    "Teach verb conjugation — Russian has different person/number patterns",
    "Practice English word order — Russian is more flexible",
    "Use contrastive analysis — show Russian vs English grammar side by side",
  ],
};

export const metadata = {
  title: "Russian L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Russian-speaking ESL students. 94 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
