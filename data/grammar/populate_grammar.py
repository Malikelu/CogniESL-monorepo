#!/usr/bin/env python3
"""
Populate empty grammar files with content.
Run this script to fill all 83 empty grammar YAML files.
"""

import os
import yaml

grammar_dir = '/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/grammar/'

# ============================================================
# GRAMMAR CONTENT DATA
# ============================================================

GRAMMAR_DATA = {
    # === PRONOUNS ===
    "subject_pronouns": {
        "title": "Subject Pronouns",
        "description": "Pronouns that replace the subject of a sentence: I, you, he, she, it, we, they.",
        "level": "A1",
        "core_meaning": "Subject pronouns replace nouns to avoid repetition. They refer to the person or thing performing the action.",
        "timeline": "Timeless — applies to all tenses.",
        "contrast": "'Subject pronoun' = 'She reads.' (replaces a name) vs 'Noun' = 'Maria reads.' (specific name)",
        "ccqs": [
            {"question": "Is the pronoun doing the action?", "answer": "Yes — it's a subject pronoun."},
            {"question": "Can you replace it with a name?", "answer": "Yes — then it's a subject pronoun."}
        ],
        "contexts": ["introductions", "describing people", "daily activities", "family"],
        "form_affirmative": "Subject + verb: 'I walk.', 'She reads.'",
        "form_negative": "Subject + don't/doesn't + verb: 'I don't walk.', 'She doesn't read.'",
        "form_questions": "Do/Does + subject + verb?: 'Do I walk?', 'Does she read?'",
        "sub_rules": [
            {"rule": "'I' is always capitalized", "type": "spelling", "examples": ["I am happy. ✅ / i am happy. ❌"]},
            {"rule": "'You' is the same for singular and plural", "type": "grammatical", "examples": ["You are my friend. (singular)", "You are my friends. (plural)"]}
        ],
        "uses": [
            {"context": "Introducing yourself", "description": "Using 'I' to talk about yourself", "examples": ["I am a student.", "I live in Brazil."]},
            {"context": "Talking about others", "description": "Using he/she/they to refer to people", "examples": ["She is a teacher.", "They are my friends."]}
        ],
        "phonetics": [{"note": "Weak form of 'he' /hiː/ → /hɪ/ in connected speech", "contexts": ["connected speech"], "l1_issue": "Some L1 speakers over-pronounce subject pronouns"}],
        "methodology": "PPP",
        "tips": ["Use substitution drills (name → pronoun)", "Use visual aids showing who each pronoun refers to"],
        "activities": [{"name": "Pronoun Substitution", "duration": 10, "adaptation_notes": "Replace nouns with pronouns in simple sentences."}]
    },
    "object_pronouns": {
        "title": "Object Pronouns",
        "description": "Pronouns that replace the object of a sentence: me, you, him, her, it, us, them.",
        "level": "A1",
        "core_meaning": "Object pronouns receive the action of the verb. They come after the verb or preposition.",
        "timeline": "Timeless — applies to all tenses.",
        "contrast": "'Subject pronoun' = 'I see her.' (I do the action) vs 'Object pronoun' = 'She sees me.' (I receive the action)",
        "ccqs": [
            {"question": "Is the pronoun receiving the action?", "answer": "Yes — it's an object pronoun."},
            {"question": "Does it come after the verb?", "answer": "Yes — object pronouns follow the verb."}
        ],
        "contexts": ["daily activities", "interactions", "requests", "describing relationships"],
        "form_affirmative": "Verb + object pronoun: 'She sees me.', 'I like him.'",
        "form_negative": "Verb + not + object pronoun or auxiliary + not: 'She doesn't see me.'",
        "form_questions": "Auxiliary + subject + verb + object pronoun?: 'Does she see me?'",
        "sub_rules": [
            {"rule": "'You' and 'it' are the same for subject and object", "type": "grammatical", "examples": ["I like you. / You like me.", "I see it. It is here."]},
            {"rule": "Object pronouns after prepositions", "type": "grammatical", "examples": ["Give it to me.", "She's talking to him."]}
        ],
        "uses": [
            {"context": "Daily interactions", "description": "Using object pronouns in conversation", "examples": ["Can you help me?", "I don't know him.", "She called us."]},
            {"context": "After prepositions", "description": "Object pronouns always follow prepositions", "examples": ["This is for you.", "Come with me."]}
        ],
        "phonetics": [{"note": "Weak forms: /hiːm/ → /ɪm/ (him), /hɜːr/ → /ər/ (her)", "contexts": ["connected speech"], "l1_issue": "Some L1 speakers use subject pronouns in object position"}],
        "methodology": "PPP",
        "tips": ["Contrast subject vs object pronouns explicitly", "Use physical actions to show who receives the action"],
        "activities": [{"name": "Object Pronoun Bingo", "duration": 10, "adaptation_notes": "Students match sentences with correct object pronouns."}]
    },
    "possessive_adjectives": {
        "title": "Possessive Adjectives",
        "description": "Words that show ownership or relationship: my, your, his, her, its, our, their.",
        "level": "A1",
        "core_meaning": "Possessive adjectives show who owns or is related to something. They come BEFORE the noun.",
        "timeline": "Timeless — shows a permanent or ongoing relationship.",
        "contrast": "'Possessive adjective' = 'my book' (before noun) vs 'Possessive pronoun' = 'mine' (replaces noun)",
        "ccqs": [
            {"question": "Does this word come before a noun?", "answer": "Yes — it's a possessive adjective."},
            {"question": "Does it show who owns something?", "answer": "Yes — that's its purpose."}
        ],
        "contexts": ["family and relationships", "personal belongings", "daily routines", "describing people"],
        "form_affirmative": "Possessive adjective + noun: 'my book', 'her house'",
        "form_negative": "Subject + be + not + possessive + noun: 'This is not my book.'",
        "form_questions": "Whose + noun?: 'Whose book is this?' → 'It's mine.'",
        "sub_rules": [
            {"rule": "'Its' (possessive) vs 'it's' (it is)", "type": "spelling", "examples": ["The dog wagged its tail. (possessive)", "It's raining. (it is)"]},
            {"rule": "Possessive adjectives don't change for plural nouns", "type": "grammatical", "examples": ["my book / my books", "her car / her cars"]}
        ],
        "uses": [
            {"context": "Family and relationships", "description": "Describing family members", "examples": ["My mother is a teacher.", "His brother lives in London."]},
            {"context": "Personal belongings", "description": "Talking about possessions", "examples": ["This is my phone.", "Where is your bag?"]}
        ],
        "phonetics": [{"note": "Weak form of 'your' /jɔːr/ → /jər/ in connected speech", "contexts": ["connected speech"], "l1_issue": "Some L1 speakers confuse 'his' and 'her'"}],
        "methodology": "PPP",
        "tips": ["Use real objects to demonstrate possession", "Contrast with possessive 's"],
        "activities": [{"name": "Whose Is It?", "duration": 10, "adaptation_notes": "Students guess ownership of classroom objects."}]
    },

    # === DETERMINERS ===
    "demonstratives": {
        "title": "Demonstratives (This, That, These, Those)",
        "description": "Words that point to specific things based on distance: this (near), that (far), these (near plural), those (far plural).",
        "level": "A1",
        "core_meaning": "Demonstratives point to specific things. This/these = near the speaker. That/those = far from the speaker.",
        "timeline": "Present — refers to things visible or known in the current context.",
        "contrast": "'This' = near (this book here) vs 'That' = far (that book there)",
        "ccqs": [
            {"question": "Is the thing near or far?", "answer": "Near = this/these, Far = that/those"},
            {"question": "Is it one thing or more than one?", "answer": "One = this/that, More = these/those"}
        ],
        "contexts": ["classroom objects", "shopping", "pointing at things", "describing locations"],
        "form_affirmative": "This/That + singular noun: 'This book is mine.' / These/Those + plural noun: 'These books are mine.'",
        "form_negative": "This/That + be + not: 'This is not my book.'",
        "form_questions": "Is this/that...?: 'Is this your bag?' / Are these/those...?: 'Are those your shoes?'",
        "sub_rules": [
            {"rule": "This/That for singular, These/Those for plural", "type": "grammatical", "examples": ["this book / these books", "that car / those cars"]},
            {"rule": "Can be used alone as pronouns", "type": "grammatical", "examples": ["This is nice. (no noun)", "I want that. (no noun)"]}
        ],
        "uses": [
            {"context": "Pointing at objects", "description": "Identifying things near or far", "examples": ["This is my pen.", "That is a beautiful painting."]},
            {"context": "Shopping", "description": "Referring to items", "examples": ["I'd like this one.", "How much are those?"]}
        ],
        "phonetics": [{"note": "Strong /ðiːs/ when emphasizing vs weak /ðɪs/ in connected speech", "contexts": ["emphasis"], "l1_issue": "Some L1 speakers use 'this' for both singular and plural"}],
        "methodology": "PPP",
        "tips": ["Use real objects at different distances", "Gesture to reinforce near/far concept"],
        "activities": [{"name": "Point and Say", "duration": 10, "adaptation_notes": "Students point to objects and describe them with demonstratives."}]
    },
    "indefinite_pronouns": {
        "title": "Indefinite Pronouns",
        "description": "Pronouns that refer to non-specific people or things: someone, anyone, everyone, no one, something, anything, everything, nothing.",
        "level": "A2",
        "core_meaning": "Indefinite pronouns refer to people or things without specifying who or what exactly.",
        "timeline": "Timeless — the reference is general, not specific.",
        "contrast": "'Indefinite pronoun' = 'Someone called.' (I don't know who) vs 'Definite' = 'Maria called.' (specific person)",
        "ccqs": [
            {"question": "Do we know exactly who/what?", "answer": "No — that's why it's indefinite."},
            {"question": "Is it about people or things?", "answer": "Someone/somebody = people, Something = things"}
        ],
        "contexts": ["describing unknown people", "talking about things", "making general statements", "questions and negatives"],
        "form_affirmative": "Indefinite pronoun + verb: 'Someone is here.', 'Everything is ready.'",
        "form_negative": "Use 'any-' forms: 'Nobody came.', 'Nothing happened.' / 'Not...any-': 'I didn't see anyone.'",
        "form_questions": "Use 'any-' forms: 'Did anyone call?', 'Is anything wrong?'",
        "sub_rules": [
            {"rule": "Some- for positive, Any- for questions and negatives", "type": "grammatical", "examples": ["Someone called. (positive)", "Did anyone call? (question)", "Nobody called. (negative)"]},
            {"rule": "Indefinite pronouns take singular verbs", "type": "grammatical", "examples": ["Everyone is here. ✅ / Everyone are here. ❌"]},
            {"rule": "Someone = positive, Anyone = question/negative, No one = negative", "type": "grammatical", "examples": ["I saw someone.", "Did you see anyone?", "I saw no one."]}
        ],
        "uses": [
            {"context": "Describing unknown people", "description": "When you don't know or don't want to say who", "examples": ["Someone knocked on the door.", "Everybody loves chocolate."]},
            {"context": "Making general statements", "description": "Talking about things in general", "examples": ["Everything is fine.", "Nothing is impossible."]}
        ],
        "phonetics": [{"note": "Stress on first syllable: /ˈsʌmwʌn/, /ˈeniwʌn/", "contexts": ["pronunciation"], "l1_issue": "Some L1 speakers stress the wrong syllable"}],
        "methodology": "PPP",
        "tips": ["Contrast some- vs any- explicitly", "Use real situations (knocking on door, finding something)"],
        "activities": [{"name": "Mystery Person", "duration": 10, "adaptation_notes": "Students describe unknown people using indefinite pronouns."}]
    },

    # === ADVERBS ===
    "adverbs_frequency": {
        "title": "Adverbs of Frequency",
        "description": "Words that tell us how often something happens: always, usually, often, sometimes, rarely, never.",
        "level": "A1",
        "core_meaning": "Adverbs of frequency tell us how often something happens — from 100% (always) to 0% (never).",
        "timeline": "Timeless — describes habitual frequency.",
        "contrast": "'Always' = 100% of the time vs 'Never' = 0% of the time",
        "ccqs": [
            {"question": "Does this happen all the time?", "answer": "Yes = always, No = never"},
            {"question": "Is it more than 50% or less than 50%?", "answer": "More = usually/often, Less = sometimes/rarely"}
        ],
        "contexts": ["daily routines", "habits and preferences", "schedules and timetables", "lifestyle"],
        "form_affirmative": "Subject + adverb + verb: 'I always wake up early.' / Subject + be + adverb: 'He is never late.'",
        "form_negative": "Use 'never' for negative meaning: 'I never eat meat.' (not 'I don't never')",
        "form_questions": "How often + do/does + subject + verb?: 'How often do you exercise?'",
        "sub_rules": [
            {"rule": "Position: before main verb, after 'be'", "type": "word_order", "examples": ["I always eat breakfast. (before verb)", "She is always happy. (after be)"]},
            {"rule": "Scale: always (100%) > usually > often > sometimes > rarely > never (0%)", "type": "semantic", "examples": ["I always brush my teeth. (100%)", "I never eat insects. (0%)"]}
        ],
        "uses": [
            {"context": "Daily routines", "description": "Describing how often you do things", "examples": ["I always have breakfast.", "She never drinks coffee."]},
            {"context": "Habits and preferences", "description": "Talking about regular activities", "examples": ["We often go to the park on Sundays.", "He rarely watches TV."]}
        ],
        "phonetics": [{"note": "Stress on first syllable: /ˈɔːlweɪz/, /ˈjuːʒuəli/", "contexts": ["pronunciation"], "l1_issue": "Word order — some L1 speakers put the adverb at the end of the sentence"}],
        "methodology": "PPP",
        "tips": ["Use a frequency line (0%-100%) to visualize", "Have students survey classmates about habits"],
        "activities": [{"name": "Frequency Survey", "duration": 15, "adaptation_notes": "Students ask classmates 'How often do you...?' and report results."}]
    },
    "adverbs_manner": {
        "title": "Adverbs of Manner",
        "description": "Words that tell us how something is done: quickly, slowly, carefully, well, badly, quietly, loudly.",
        "level": "A1",
        "core_meaning": "Adverbs of manner describe HOW an action is performed. They usually go after the verb.",
        "timeline": "Timeless — describes the manner of an action in any tense.",
        "contrast": "'Adverb of manner' = 'She sings beautifully.' (how?) vs 'Adverb of frequency' = 'She always sings.' (how often?)",
        "ccqs": [
            {"question": "Does this word tell us HOW something is done?", "answer": "Yes — it's an adverb of manner."},
            {"question": "Does it go after the verb?", "answer": "Usually yes."}
        ],
        "contexts": ["describing actions", "giving instructions", "telling stories", "describing people's behavior"],
        "form_affirmative": "Subject + verb + adverb: 'She sings beautifully.', 'He drives carefully.'",
        "form_negative": "Subject + verb + adverb (same position): 'She doesn't sing beautifully.'",
        "form_questions": "How + do/does + subject + verb?: 'How does she sing?' → 'Beautifully.'",
        "sub_rules": [
            {"rule": "Most adverbs of manner: adjective + -ly", "type": "spelling", "examples": ["quick → quickly", "careful → carefully", "quiet → quietly"]},
            {"rule": "Irregular: good → well, fast → fast, hard → hard", "type": "irregular", "examples": ["She sings well. (not goodly)", "He runs fast. (not fastly)"]},
            {"rule": "Position: after the verb or at the end of the sentence", "type": "word_order", "examples": ["She speaks English fluently.", "He drove carefully."]}
        ],
        "uses": [
            {"context": "Describing how people do things", "description": "Talking about the quality of actions", "examples": ["She speaks English very well.", "He drives too fast."]},
            {"context": "Giving instructions", "description": "Telling someone how to do something", "examples": ["Listen carefully.", "Speak slowly and clearly."]}
        ],
        "phonetics": [{"note": "-ly ending pronounced as /li/", "contexts": ["pronunciation"], "l1_issue": "Some L1 speakers omit the -ly ending"}],
        "methodology": "PPP",
        "tips": ["Use actions and demonstrations", "Contrast adjective vs adverb (quick vs quickly)"],
        "activities": [{"name": "Act and Describe", "duration": 10, "adaptation_notes": "Students act out actions, others describe using adverbs."}]
    },
    "place_adverbs": {
        "title": "Common Place Adverbs",
        "description": "Words that tell us where: here, there, everywhere, somewhere, nowhere, upstairs, downstairs, inside, outside.",
        "level": "A1",
        "core_meaning": "Place adverbs tell us WHERE something happens or where something/someone is.",
        "timeline": "Timeless — describes location, not time.",
        "contrast": "'Here' = near the speaker vs 'There' = far from the speaker",
        "ccqs": [
            {"question": "Does this word tell us WHERE?", "answer": "Yes — it's a place adverb."},
            {"question": "Is it near or far from the speaker?", "answer": "Here = near, There = far"}
        ],
        "contexts": ["giving directions", "describing locations", "talking about where things are", "daily routines"],
        "form_affirmative": "Subject + verb + place adverb: 'I live here.', 'She is upstairs.'",
        "form_negative": "Subject + verb + no-/nowhere: 'I found it nowhere.' / 'There's nothing here.'",
        "form_questions": "Where + be/auxiliary + subject?: 'Where is the bathroom?', 'Where do you live?'",
        "sub_rules": [
            {"rule": "Here = near speaker, There = far from speaker", "type": "semantic", "examples": ["Come here. (near me)", "Put it there. (over there)"]},
            {"rule": "No- words for negative meaning", "type": "grammatical", "examples": ["nowhere = not anywhere", "nothing = not anything"]}
        ],
        "uses": [
            {"context": "Giving directions", "description": "Telling someone where to go", "examples": ["Turn left here.", "The bathroom is upstairs."]},
            {"context": "Describing where things are", "description": "Talking about location", "examples": ["My keys are here somewhere.", "She lives nearby."]}
        ],
        "phonetics": [{"note": "Stress on 'here' and 'there' for emphasis", "contexts": ["emphasis"], "l1_issue": "Some L1 speakers confuse 'here' and 'there'"}],
        "methodology": "PPP",
        "tips": ["Use classroom locations to demonstrate", "Use gestures to reinforce here/there"],
        "activities": [{"name": "Hide and Seek", "duration": 10, "adaptation_notes": "Hide objects, students describe where they are using place adverbs."}]
    },

    # === PREPOSITIONS ===
    "prepositions_time": {
        "title": "Prepositions of Time (At, In, On)",
        "description": "Prepositions used to talk about when something happens: at (specific time), in (months/years/seasons), on (days/dates).",
        "level": "A1",
        "core_meaning": "Prepositions of time tell us WHEN something happens. Each preposition is used with different time expressions.",
        "timeline": "Specific to the time expression used with each preposition.",
        "contrast": "'At' = specific time (at 3pm) vs 'In' = longer periods (in July) vs 'On' = days/dates (on Monday)",
        "ccqs": [
            {"question": "Is it a specific clock time?", "answer": "Use 'at' (at 3pm)"},
            {"question": "Is it a day or date?", "answer": "Use 'on' (on Monday)"},
            {"question": "Is it a month, year, or season?", "answer": "Use 'in' (in July)"}
        ],
        "contexts": ["schedules and appointments", "daily routines", "holidays and special dates", "telling time"],
        "form_affirmative": "at + specific time: 'at 3pm', 'at noon' / in + month/year/season: 'in July', 'in 2024' / on + day/date: 'on Monday', 'on July 4th'",
        "form_negative": "Same preposition, negated verb: 'The class doesn't start at 9am.'",
        "form_questions": "When + be/auxiliary?: 'When is the meeting?' → 'At 3pm.'",
        "sub_rules": [
            {"rule": "at: at 3pm, at noon, at night, at the weekend", "type": "grammatical", "examples": ["I wake up at 7am.", "We rest at night."]},
            {"rule": "in: in the morning, in July, in 2024, in summer", "type": "grammatical", "examples": ["I was born in 1990.", "We swim in summer."]},
            {"rule": "on: on Monday, on July 4th, on my birthday", "type": "grammatical", "examples": ["The class is on Monday.", "We celebrate on Christmas Day."]},
            {"rule": "No preposition with: today, tomorrow, yesterday, last, next, this, every", "type": "grammatical", "examples": ["I study every day. (not 'on every day')", "See you tomorrow. (not 'on tomorrow')"]}
        ],
        "uses": [
            {"context": "Making appointments", "description": "Scheduling meetings and events", "examples": ["Let's meet at 3pm.", "The party is on Saturday."]},
            {"context": "Talking about routines", "description": "Describing when things happen regularly", "examples": ["I exercise in the morning.", "We have class on Mondays."]}
        ],
        "phonetics": [{"note": "Weak forms: /æt/ → /ət/, /ɪn/ → /ən/, /ɒn/ → /ən/", "contexts": ["connected speech"], "l1_issue": "Prepositions are often omitted or confused by L1 speakers"}],
        "methodology": "PPP",
        "tips": ["Use a timeline to visualize at/in/on", "Create a chart with time expressions"],
        "activities": [{"name": "Time Preposition Sort", "duration": 10, "adaptation_notes": "Students sort time expressions into at/in/on columns."}]
    },
    "prepositions_place": {
        "title": "Prepositions of Place (At, In, On)",
        "description": "Prepositions used to talk about where something is: at (specific point), in (enclosed space), on (surface).",
        "level": "A1",
        "core_meaning": "Prepositions of place tell us WHERE something is located. Each preposition describes a different spatial relationship.",
        "timeline": "Timeless — describes location, not time.",
        "contrast": "'At' = specific point (at the door) vs 'In' = enclosed space (in the box) vs 'On' = surface (on the table)",
        "ccqs": [
            {"question": "Is it a specific point or address?", "answer": "Use 'at' (at the bus stop)"},
            {"question": "Is it inside an enclosed space?", "answer": "Use 'in' (in the room)"},
            {"question": "Is it on a surface?", "answer": "Use 'on' (on the wall)"}
        ],
        "contexts": ["giving directions", "describing locations", "talking about where things are", "addresses"],
        "form_affirmative": "at + specific point: 'at the door', 'at the bus stop' / in + enclosed space: 'in the room', 'in London' / on + surface: 'on the table', 'on the wall'",
        "form_negative": "Same preposition, negated verb: 'The book isn't on the table.'",
        "form_questions": "Where + be?: 'Where is the cat?' → 'On the table.'",
        "sub_rules": [
            {"rule": "at: at the door, at home, at school, at work, at the bus stop", "type": "grammatical", "examples": ["I'm at home.", "Wait at the traffic lights."]},
            {"rule": "in: in the box, in the room, in London, in the park, in the car", "type": "grammatical", "examples": ["The keys are in my pocket.", "I live in Brazil."]},
            {"rule": "on: on the table, on the wall, on the floor, on the bus, on Main Street", "type": "grammatical", "examples": ["The book is on the desk.", "I'm on the bus."]}
        ],
        "uses": [
            {"context": "Giving directions", "description": "Telling someone where to go or where something is", "examples": ["Turn left at the bank.", "The pharmacy is on Main Street."]},
            {"context": "Describing locations", "description": "Talking about where things are", "examples": ["My phone is in my bag.", "There's a picture on the wall."]}
        ],
        "phonetics": [{"note": "Weak forms: /æt/ → /ət/, /ɪn/ → /ən/, /ɒn/ → /ən/", "contexts": ["connected speech"], "l1_issue": "Some L1 speakers use 'in' for all locations"}],
        "methodology": "PPP",
        "tips": ["Use real objects to demonstrate spatial relationships", "Draw diagrams to show at/in/on"],
        "activities": [{"name": "Where Is It?", "duration": 10, "adaptation_notes": "Hide objects and describe their location using prepositions."}]
    },

    # === VERBS ===
    "stative_dynamic_verbs": {
        "title": "Stative vs. Dynamic Verbs",
        "description": "The distinction between verbs that describe states (stative) and verbs that describe actions (dynamic). Stative verbs are not normally used in continuous tenses.",
        "level": "B1",
        "core_meaning": "Stative verbs describe states, feelings, or conditions (know, believe, love, want). Dynamic verbs describe actions (run, eat, write). Stative verbs are NOT normally used in continuous tenses.",
        "timeline": "Stative = unchanging state. Dynamic = action in progress.",
        "contrast": "'Stative' = 'I know the answer.' (not 'I am knowing') vs 'Dynamic' = 'I am running.' (action in progress)",
        "ccqs": [
            {"question": "Is this verb describing an action or a state?", "answer": "Action = dynamic, State = stative"},
            {"question": "Can I use this verb in continuous form?", "answer": "If yes, it's dynamic. If no, it's stative."}
        ],
        "contexts": ["describing feelings and opinions", "talking about possession", "mental states", "senses"],
        "form_affirmative": "Stative: Subject + stative verb: 'I know her.', 'She loves chocolate.' / Dynamic: Subject + be + verb-ing: 'I am running.'",
        "form_negative": "Stative: Subject + don't/doesn't + stative verb: 'I don't know.' / Dynamic: Subject + be + not + verb-ing: 'I am not running.'",
        "form_questions": "Stative: Do/Does + subject + stative verb?: 'Do you know her?' / Dynamic: Am/Is/Are + subject + verb-ing?: 'Are you running?'",
        "sub_rules": [
            {"rule": "Common stative verbs: know, believe, understand, love, hate, want, need, prefer, own, belong, seem, appear", "type": "grammatical", "examples": ["I understand. (not 'I am understanding')", "She loves music. (not 'She is loving music')"]},
            {"rule": "Some verbs can be both stative and dynamic with different meanings", "type": "semantic", "examples": ["I think it's great. (opinion = stative) / I'm thinking about it. (process = dynamic)", "I have a car. (possession = stative) / I'm having lunch. (action = dynamic)"]},
            {"rule": "Sense verbs are usually stative: see, hear, smell, taste, feel", "type": "grammatical", "examples": ["I see a bird. (not 'I am seeing')", "This tastes good. (not 'This is tasting')"]}
        ],
        "uses": [
            {"context": "Describing feelings and opinions", "description": "Using stative verbs for emotions and thoughts", "examples": ["I love this song.", "She believes in God.", "I don't understand."]},
            {"context": "Describing actions in progress", "description": "Using dynamic verbs in continuous tenses", "examples": ["I am reading a book.", "She is cooking dinner."]}
        ],
        "phonetics": [{"note": "No specific phonetic pattern — focus on correct tense usage", "contexts": ["tense usage"], "l1_issue": "Many L1 speakers overuse continuous tenses with stative verbs"}],
        "methodology": "PPP",
        "tips": ["Create a list of common stative verbs", "Use the 'Can I see someone doing this?' test (if no, it's stative)"],
        "activities": [{"name": "Stative or Dynamic?", "duration": 10, "adaptation_notes": "Students classify verbs and create sentences."}]
    },
    "verbs_two_objects": {
        "title": "Verbs with Two Objects (Ditransitive)",
        "description": "Verbs that can take two objects: a direct object and an indirect object. Common verbs: give, send, tell, show, buy, make, bring, offer.",
        "level": "A2",
        "core_meaning": "Ditransitive verbs transfer something (direct object) to someone (indirect object). The indirect object can come before or after the direct object.",
        "timeline": "Depends on the tense used.",
        "contrast": "'Two objects' = 'She gave me a book.' (indirect + direct) vs 'One object' = 'She read a book.' (direct only)",
        "ccqs": [
            {"question": "Is something being transferred to someone?", "answer": "Yes — it's a ditransitive verb."},
            {"question": "Can you identify who receives something?", "answer": "That's the indirect object."}
        ],
        "contexts": ["giving and receiving", "telling stories", "buying and making things", "offering help"],
        "form_affirmative": "Subject + verb + indirect object + direct object: 'She gave me a book.' / Subject + verb + direct object + to/for + indirect object: 'She gave a book to me.'",
        "form_negative": "Subject + don't/doesn't + verb + objects: 'She didn't give me a book.'",
        "form_questions": "Who + verb + indirect object?: 'Who did she give the book to?' / What + verb + direct object?: 'What did she give you?'",
        "sub_rules": [
            {"rule": "Some verbs use 'to' (give, send, show, tell, bring, offer)", "type": "grammatical", "examples": ["Give it to me.", "Send the email to John."]},
            {"rule": "Some verbs use 'for' (buy, make, cook, get, find)", "type": "grammatical", "examples": ["Buy a gift for her.", "Make a cake for the party."]},
            {"rule": "Word order: indirect object comes BEFORE direct object (no preposition)", "type": "word_order", "examples": ["She gave me a book. ✅ / She gave a book to me. ✅ / She gave to me a book. ❌"]}
        ],
        "uses": [
            {"context": "Giving and receiving", "description": "Describing transfers of things or information", "examples": ["Can you lend me your pen?", "She told me a secret.", "I bought my mom flowers."]},
            {"context": "Offering and requesting", "description": "Making offers or asking for things", "examples": ["Could you show me the way?", "I'll make you a sandwich."]}
        ],
        "phonetics": [{"note": "Stress on the verb, not the objects", "contexts": ["sentence stress"], "l1_issue": "Word order — some L1 speakers put the direct object first"}],
        "methodology": "PPP",
        "tips": ["Use real objects to demonstrate giving/receiving", "Practice both word orders (indirect+direct vs direct+to/for)"],
        "activities": [{"name": "Give and Tell", "duration": 15, "adaptation_notes": "Students practice ditransitive verbs in a gift-giving role play."}]
    },
}

# Write all files
written = []
for slug, data in GRAMMAR_DATA.items():
    filepath = os.path.join(grammar_dir, f"{slug}.yaml")
    
    output = {
        'grammar_point': slug,
        'title': data['title'],
        'description': data['description'],
        'level': data['level'],
        'meaning': {
            'core_meaning': data['core_meaning'],
            'timeline': data.get('timeline', ''),
            'contrast': data.get('contrast', ''),
            'ccqs': data.get('ccqs', []),
            'example_generator': {
                'contexts': data.get('contexts', []),
                'cultural_notes': [],
                'min_examples': data.get('min_examples', 5)
            }
        },
        'form': {
            'affirmative': {
                'structure': data.get('form_affirmative', ''),
                'example_generator': {
                    'contexts': data.get('contexts', [])[:3],
                    'min_examples': 4
                }
            },
            'negative': {
                'structure': data.get('form_negative', ''),
                'example_generator': {
                    'contexts': data.get('contexts', [])[:3],
                    'min_examples': 4
                }
            },
            'questions': {
                'structure': data.get('form_questions', ''),
                'example_generator': {
                    'contexts': data.get('contexts', [])[:3],
                    'min_examples': 4
                }
            }
        },
        'sub_rules': data.get('sub_rules', []),
        'use': data.get('uses', []),
        'phonetics': data.get('phonetics', []),
        'teaching': {
            'methodology': data.get('methodology', 'PPP'),
            'tips': data.get('tips', []),
            'recommended_activities': data.get('activities', [])
        }
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    written.append(slug)

print(f"Written {len(written)} files")
