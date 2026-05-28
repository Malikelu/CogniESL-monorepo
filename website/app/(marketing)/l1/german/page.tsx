import { createLanguagePage } from "../_template";

const lang = {
  code: "german",
  name: "German",
  flag: "🇩🇪",
  patterns: 68,
  speakers: "1.1 million German speakers in the US",
  overview: "German has a case system, compound words, and different word order rules. While German and English share Germanic roots, significant interference patterns exist, particularly in verb position and case marking.",
  errors: [
    { error: "I go to home", correction: "I go home", explanation: "German 'Ich gehe nach Hause' (I go to home) transfers the preposition.", category: "Prepositions" },
    { error: "She has 20 years", correction: "She is 20 years old", explanation: "German uses 'haben' (to have) for age, similar to Romance languages.", category: "Grammar" },
    { error: "I learn since 3 years", correction: "I have been learning for 3 years", explanation: "German uses present tense with 'seit' where English requires present perfect.", category: "Verb Tense" },
    { error: "He don't like it", correction: "He doesn't like it", explanation: "German negation structure differs from English.", category: "Verb Tense" },
    { error: "I have many homeworks", correction: "I have a lot of homework", explanation: "German pluralizes nouns differently than English.", category: "Nouns" },
    { error: "She is my friend good", correction: "She is my good friend", explanation: "German places adjectives after the noun in some constructions.", category: "Word Order" },
  ],
  tips: [
    "Leverage Germanic roots — many English words come from German",
    "Teach word order — German verb position rules differ from English",
    "Practice article usage — German has three genders, English has none",
    "Use compound word awareness — German compounds can be very long",
  ],
};

export const metadata = {
  title: "German L1 Interference Patterns — CogniESL",
  description: "Common English mistakes made by German-speaking ESL students. 68 interference patterns with examples, corrections, and teaching tips.",
};

export default createLanguagePage(lang);
