import { createLanguagePage } from "../_template";

const lang = {
  code: "spanish",
  name: "Spanish",
  flag: "🇪🇸",
  patterns: 142,
  speakers: "41 million Spanish speakers in the US — the largest ESL population",
  overview: "Spanish is the most common L1 among ESL students in the US. Spanish and English share many cognates, which helps vocabulary acquisition but also creates false friends. Key interference areas include verb tense, articles, and word order. Spanish has two 'to be' verbs (ser/estar) which creates confusion with English's single 'to be'.",
  errors: [
    { error: "I am agree", correction: "I agree", explanation: "Spanish 'estar de acuerdo' literally translates to 'to be of agreement' — students transfer the 'ser/estar' structure.", category: "Grammar" },
    { error: "I have 25 years", correction: "I am 25 years old", explanation: "Spanish uses 'tener' (to have) for age, not 'ser/estar' (to be).", category: "Grammar" },
    { error: "She is doctor", correction: "She is a doctor", explanation: "Spanish omits indefinite articles before professions.", category: "Articles" },
    { error: "I go to the school yesterday", correction: "I went to school yesterday", explanation: "Spanish often uses present tense where English requires past tense for completed actions.", category: "Verb Tense" },
    { error: "The life is beautiful", correction: "Life is beautiful", explanation: "Spanish uses definite articles more broadly than English.", category: "Articles" },
    { error: "I want that you come", correction: "I want you to come", explanation: "Spanish uses 'que' (that) where English uses infinitive 'to'.", category: "Grammar" },
  ],
  tips: [
    "Focus on article usage early — Spanish has more articles than English",
    "Teach the difference between 'ser' and 'estar' as it maps to English 'to be'",
    "Use cognates strategically but warn about false friends (e.g., 'embarazada' ≠ 'embarrassed')",
    "Practice past tense heavily — Spanish speakers often default to present tense",
  ],
};

export const metadata = {
  title: "Spanish L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Spanish-speaking ESL students. 142 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
