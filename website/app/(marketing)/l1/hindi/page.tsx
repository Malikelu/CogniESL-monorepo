import { createLanguagePage } from "../_template";

const lang = {
  code: "hindi",
  name: "Hindi",
  flag: "🇮🇳",
  patterns: 82,
  speakers: "1.4 million Hindi speakers in the US",
  overview: "Hindi has an SOV structure, no articles, and a complex honorific system. Postpositions (instead of prepositions) and different tense marking create systematic interference. Hindi uses the Devanagari script.",
  errors: [
    { error: "He is having a car", correction: "He has a car", explanation: "Hindi uses progressive tense for possession where English uses simple present.", category: "Verb Tense" },
    { error: "I am knowing the answer", correction: "I know the answer", explanation: "Hindi uses progressive for stative verbs where English doesn't.", category: "Verb Tense" },
    { error: "She is my cousin sister", correction: "She is my cousin", explanation: "Hindi specifies gender for all family relations.", category: "Vocabulary" },
    { error: "I go to home", correction: "I go home", explanation: "Hindi uses 'to' with 'home' where English drops the preposition.", category: "Prepositions" },
    { error: "He don't like it", correction: "He doesn't like it", explanation: "Hindi doesn't conjugate verbs for person in the same way as English.", category: "Verb Tense" },
    { error: "I have 25 years", correction: "I am 25 years old", explanation: "Hindi uses 'have' for age, similar to other South Asian languages.", category: "Grammar" },
  ],
  tips: [
    "Teach stative vs dynamic verbs — Hindi uses progressive for both",
    "Focus on articles — Hindi has no article system",
    "Practice SVO word order — Hindi is SOV",
    "Use contrastive analysis — show Hindi vs English grammar side by side",
  ],
};

export const metadata = {
  title: "Hindi L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by Hindi-speaking ESL students. 82 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
