import { createLanguagePage } from "../_template";

const lang = {
  code: "korean",
  name: "Korean",
  flag: "🇰🇷",
  patterns: 98,
  speakers: "1.1 million Korean speakers in the US",
  overview: "Korean has a very different sentence structure (SOV) compared to English (SVO). The absence of articles, different tense marking, and honorific system create unique interference patterns. Korean also lacks many English sounds, causing pronunciation challenges.",
  errors: [
    { error: "I went to store yesterday", correction: "I went to the store yesterday", explanation: "Korean has no article system. Students must learn to add a/an/the where none exists in their L1.", category: "Articles" },
    { error: "He eat lunch now", correction: "He is eating lunch now", explanation: "Korean doesn't mark progressive aspect with auxiliary verbs like English 'be + -ing'.", category: "Verb Tense" },
    { error: "I have many homework", correction: "I have a lot of homework", explanation: "Korean doesn't distinguish countable/uncountable nouns the way English does.", category: "Nouns" },
    { error: "She is my friend good", correction: "She is my good friend", explanation: "Korean places adjectives after the noun in some constructions.", category: "Word Order" },
    { error: "I came to America since 3 years", correction: "I came to America 3 years ago", explanation: "Korean uses 'since' differently for time expressions.", category: "Prepositions" },
    { error: "He don't like it", correction: "He doesn't like it", explanation: "Korean doesn't conjugate verbs for person/number like English.", category: "Verb Tense" },
  ],
  tips: [
    "Start with articles — they don't exist in Korean and are consistently dropped",
    "Teach SVO word order explicitly — Korean is SOV",
    "Practice progressive tense heavily — Korean marks aspect differently",
    "Use visual aids for prepositions — Korean uses postpositions, not prepositions",
  ],
};

export const metadata = {
  title: "Korean L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Korean-speaking ESL students. 98 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
