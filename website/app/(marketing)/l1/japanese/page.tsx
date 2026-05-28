import { createLanguagePage } from "../_template";

const lang = {
  code: "japanese",
  name: "Japanese",
  flag: "🇯🇵",
  patterns: 103,
  speakers: "1.5 million Japanese speakers in the US",
  overview: "Japanese has an SOV sentence structure, no articles, and a complex honorific system. These create unique interference patterns in English grammar and pragmatics. Japanese writing uses three scripts (hiragana, katakana, kanji).",
  errors: [
    { error: "I went to store yesterday", correction: "I went to the store yesterday", explanation: "Japanese has no article system. Articles must be explicitly taught.", category: "Articles" },
    { error: "He don't like it", correction: "He doesn't like it", explanation: "Japanese doesn't conjugate verbs for person, so third-person -s is dropped.", category: "Verb Tense" },
    { error: "I have many homeworks", correction: "I have a lot of homework", explanation: "Japanese doesn't distinguish countable/uncountable nouns.", category: "Nouns" },
    { error: "She is my friend good", correction: "She is my good friend", explanation: "Japanese places adjectives after the noun in some constructions.", category: "Word Order" },
    { error: "I came to America since 3 years", correction: "I came to America 3 years ago", explanation: "Japanese uses 'since' differently for time expressions.", category: "Prepositions" },
    { error: "I go to home", correction: "I go home", explanation: "Japanese uses 'to' with 'home' where English drops the preposition.", category: "Prepositions" },
  ],
  tips: [
    "Teach SVO word order explicitly — Japanese is SOV",
    "Focus on articles — they don't exist in Japanese",
    "Practice /l/ vs /r/ sounds — Japanese doesn't distinguish these",
    "Teach direct communication styles — Japanese is more indirect",
  ],
};

export const metadata = {
  title: "Japanese L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Japanese-speaking ESL students. 103 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
