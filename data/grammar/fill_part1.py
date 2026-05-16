#!/usr/bin/env python3
"""Fill empty fields in grammar YAML files — Part 1 (files 1-10)."""

import yaml
import os

GRAMMAR_DIR = "/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/grammar"


def load_file(name):
    with open(os.path.join(GRAMMAR_DIR, name)) as f:
        return yaml.safe_load(f)


def save_file(name, data):
    with open(os.path.join(GRAMMAR_DIR, name), 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ─── degree_adverbs.yaml ───────────────────────────────────────────────────────
d = load_file("degree_adverbs.yaml")
d["meaning"]["ccqs"] = [
    {"question": "Is 'very hot' comfortable to touch?", "answer": "No — 'very hot' means it has a high temperature, probably too hot to touch."},
    {"question": "Does 'too heavy' mean the weight is acceptable?", "answer": "No — 'too' means more than wanted or needed, with a negative meaning."},
    {"question": "If she is 'tall enough to reach the shelf,' can she reach it?", "answer": "Yes — 'enough' means sufficient."},
]
d["sub_rules"] = [
    {"type": "Very", "rule": "Very goes before adjectives and adverbs to make them stronger. It is neutral.", "examples": ["very tall", "very quickly"]},
    {"type": "Too", "rule": "Too means 'more than necessary/wanted' and has a negative meaning.", "examples": ["too loud", "too expensive"]},
    {"type": "Enough", "rule": "Enough means 'as much as needed.' It goes AFTER adjectives and adverbs but BEFORE nouns.", "examples": ["old enough", "enough money"]},
    {"type": "Quite", "rule": "Quite means 'fairly' or 'rather.' In British English it can mean 'very' with extreme adjectives.", "examples": ["quite good", "quite amazing"]},
    {"type": "Too + Infinitive", "rule": "Too + adjective + to + verb shows that something prevents an action.", "examples": ["too tired to go out", "too young to drive"]},
]
d["phonetics"] = [
    {"feature": "Stress on degree adverbs", "description": "Degree adverbs are often stressed to emphasise the degree. 'Enough' has stress on the second syllable /ɪˈnʌf/.", "l1_issues": ["Spanish speakers may place 'enough' before the adjective (e.g. 'enough big' instead of 'big enough').", "Chinese speakers may omit degree adverbs entirely, relying on context."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Temperature Scale", "duration": "10 min", "description": "Draw a thermometer on the board. Students place degree adverbs at different temperature points and create sentences.", "adaptation": "Limit to very, too, and enough for lower levels."},
    {"name": "Real Object Comparison", "duration": "15 min", "description": "Bring objects of different sizes or weights. Students describe them using degree adverbs.", "adaptation": "Provide sentence frames for weaker students."},
    {"name": "Problem-Solving Scenarios", "duration": "15 min", "description": "Give students scenarios with problems (too expensive, not big enough) and have them suggest solutions.", "adaptation": "Pair work for lower levels."},
]
save_file("degree_adverbs.yaml", d)
print("OK: degree_adverbs.yaml")

# ─── dependent_prepositions.yaml ───────────────────────────────────────────────
d = load_file("dependent_prepositions.yaml")
d["meaning"]["ccqs"] = [
    {"question": "Is 'I listen music' correct?", "answer": "No — you need 'to.' The correct form is 'I listen to music.'"},
    {"question": "Is 'good in maths' the correct preposition?", "answer": "No — the correct collocation is 'good at maths.'"},
    {"question": "Can you say 'depend of' or 'depend from'?", "answer": "No — the only correct form is 'depend on.'"},
]
d["sub_rules"] = [
    {"type": "Verb + Preposition", "rule": "Some verbs require a specific preposition. These must be learned as chunks.", "examples": ["listen to", "look at", "wait for", "depend on"]},
    {"type": "Adjective + Preposition", "rule": "Adjectives are followed by fixed prepositions.", "examples": ["afraid of", "good at", "interested in", "different from"]},
    {"type": "Noun + Preposition", "rule": "Nouns often take the same preposition as their related verb.", "examples": ["reason for", "solution to", "need for"]},
    {"type": "Preposition Not Translated", "rule": "Many languages use different prepositions or none at all. Learners must memorise English collocations.", "examples": ["dream about (not 'dream with')", "married to (not 'married with')"]},
    {"type": "Question Form", "rule": "In questions, the preposition often moves to the end in informal English.", "examples": ["Who did you listen to?", "What are you looking at?"]},
]
d["phonetics"] = [
    {"feature": "Weak forms of prepositions", "description": "Prepositions are usually unstressed. 'To' reduces to /tə/, 'for' to /fə/, and 'of' to /əv/.", "l1_issues": ["Spanish speakers may use 'in' as a default preposition since 'en' covers both 'in' and 'on'.", "Arabic speakers may omit prepositions entirely."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Collocation Matching", "duration": "10 min", "description": "Students match verbs/adjectives to their correct prepositions and create sentences.", "adaptation": "Reduce the number of items for lower levels."},
    {"name": "Preposition Bingo", "duration": "15 min", "description": "Students fill bingo grids with prepositions. Teacher says verbs/adjectives and students mark the correct preposition.", "adaptation": "Allow lower levels to have a reference sheet."},
    {"name": "Error Correction Race", "duration": "10 min", "description": "Display sentences with wrong prepositions. Teams race to identify and correct the errors.", "adaptation": "Provide multiple choice options for weaker students."},
]
save_file("dependent_prepositions.yaml", d)
print("OK: dependent_prepositions.yaml")

# ─── ed_clauses.yaml ───────────────────────────────────────────────────────────
d = load_file("ed_clauses.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'Built in 1900, the house is old.' Who built the house?", "answer": "We don't know — the house was built (passive) in 1900. The -ed clause describes the house."},
    {"question": "'Exhausted by the race, he collapsed.' Was he tired or energetic?", "answer": "Exhausted (very tired). The -ed clause tells us why he collapsed."},
    {"question": "'I am interested in art.' Am I causing interest or feeling it?", "answer": "Feeling it — 'interested' describes your feeling."},
]
d["sub_rules"] = [
    {"type": "Reduced Passive", "rule": "An -ed clause can replace 'which/who + be + past participle.'", "examples": ["The car driven by Tom was red.", "The letter written by my grandmother was beautiful."]},
    {"type": "Fronted -ed Clauses", "rule": "An -ed clause at the start of a sentence gives the reason for the main clause.", "examples": ["Exhausted by the race, he collapsed.", "Built in 1900, the house has a lot of history."]},
    {"type": "Subject Consistency", "rule": "The subject of the -ed clause must be the same as the subject of the main clause.", "examples": ["Confused by the instructions, she asked for help. (correct)", "Confused by the instructions, the task was hard. (incorrect)"]},
    {"type": "-ed as Adjective", "rule": "Many -ed forms function as adjectives describing a state or feeling.", "examples": ["I'm interested.", "He's bored.", "We're tired."]},
    {"type": "Active vs Passive Participle", "rule": "-ed = passive (done TO the subject). -ing = active (done BY the subject).", "examples": ["The bored student (feels boredom) vs the boring student (causes boredom)."]},
]
d["phonetics"] = [
    {"feature": "-ed pronunciation", "description": "The -ed ending has three pronunciations: /t/ (walked), /d/ (played), /ɪd/ (wanted). The /ɪd/ form adds a syllable.", "l1_issues": ["Spanish speakers may pronounce -ed as a separate syllable in all cases.", "Chinese speakers may omit the -ed ending entirely."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Clause Reduction", "duration": "15 min", "description": "Students reduce full relative clauses to -ed clauses.", "adaptation": "Provide the first few as examples."},
    {"name": "Picture Description", "duration": "10 min", "description": "Show pictures and students describe them using -ed clauses.", "adaptation": "Give sentence starters for lower levels."},
    {"name": "Error Hunt", "duration": "10 min", "description": "Display sentences with dangling participles. Students identify and correct the errors.", "adaptation": "Provide hints about which subject is wrong."},
]
save_file("ed_clauses.yaml", d)
print("OK: ed_clauses.yaml")

# ─── ed_vs_ing_adjectives.yaml ─────────────────────────────────────────────────
d = load_file("ed_vs_ing_adjectives.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'I am boring.' Am I feeling boredom or causing it?", "answer": "Causing it — 'I am boring' means I make other people feel bored."},
    {"question": "Is 'The film was excited' correct?", "answer": "No — films don't feel emotions. It should be 'The film was exciting.'"},
    {"question": "'She is interested in music.' Does she feel interest or cause it?", "answer": "She feels interest — 'interested' describes her feeling."},
]
d["sub_rules"] = [
    {"type": "-ed = Person's Feeling", "rule": "-ed adjectives describe how a person feels. The subject is the experiencer.", "examples": ["I'm bored.", "He's tired.", "We're surprised."]},
    {"type": "-ing = Cause of Feeling", "rule": "-ing adjectives describe the thing or person that causes the feeling.", "examples": ["The lesson is boring.", "The news was exciting."]},
    {"type": "Same Root, Different Forms", "rule": "Most emotion verbs have three forms: the verb, the -ed adjective, and the -ing adjective.", "examples": ["bore → bored/boring", "excite → excited/exciting", "interest → interested/interesting"]},
    {"type": "People as -ing", "rule": "People can be described with -ing adjectives when they cause that feeling in others.", "examples": ["He's a boring teacher.", "She's an exciting speaker."]},
    {"type": "Common Mistake", "rule": "Using -ing for a person's feeling is a very common error.", "examples": ["I am bored. (correct — I feel boredom)", "I am boring. (this means I am a boring person)"]},
]
d["phonetics"] = [
    {"feature": "Stress patterns", "description": "Both -ed and -ing adjectives have stress on the same syllable as the base verb.", "l1_issues": ["Spanish speakers may confuse 'I'm boring' and 'I'm bored' in speech.", "Japanese speakers may struggle with the /ɪŋ/ ending."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Emotion Charades", "duration": "15 min", "description": "A student acts out an emotion. The class says 'You're bored!' and 'The class is boring!'", "adaptation": "Write target adjectives on the board as prompts."},
    {"name": "Survey — What Interests You?", "duration": "15 min", "description": "Students survey classmates about what they find interesting and boring.", "adaptation": "Provide question templates and sentence frames."},
    {"name": "Minimal Pair Drilling", "duration": "10 min", "description": "Teacher says a situation. Students respond with the correct form.", "adaptation": "Use visual aids to reinforce the distinction."},
]
save_file("ed_vs_ing_adjectives.yaml", d)
print("OK: ed_vs_ing_adjectives.yaml")

# ─── even_if.yaml ──────────────────────────────────────────────────────────────
d = load_file("even_if.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'Even if it rains, we will go.' Will the rain change the plan?", "answer": "No — 'even if' means the rain will not change the plan."},
    {"question": "'Even if you study, you might fail.' Does studying help?", "answer": "No — 'even if' suggests studying will not change the result."},
    {"question": "Are 'even if' and 'even though' the same?", "answer": "No. 'Even if' is about a possible condition. 'Even though' is about a known fact."},
]
d["sub_rules"] = [
    {"type": "No Future After Even If", "rule": "Even if is followed by present simple, not will, even for future reference.", "examples": ["Even if it rains tomorrow, we will go. (correct)", "Even if it will rain tomorrow, we will go. (incorrect)"]},
    {"type": "First Conditional Pattern", "rule": "Even if + present simple, will + base verb.", "examples": ["Even if you call, I won't answer.", "I will go even if it snows."]},
    {"type": "Zero Conditional Pattern", "rule": "Even if + present simple, present simple for general truths.", "examples": ["Even if you water it every day, this plant dies."]},
    {"type": "Even If vs Even Though", "rule": "Even if = hypothetical condition. Even though = known fact.", "examples": ["Even if he apologises, I won't forgive him. (hypothetical)", "Even though he apologised, I didn't forgive him. (fact)"]},
    {"type": "Emphasis Position", "rule": "Even if can come at the start or middle of a sentence.", "examples": ["Even if you try hard, you might fail.", "You might fail even if you try hard."]},
]
d["phonetics"] = [
    {"feature": "Contraction and stress", "description": "'Even if' is often reduced in speech. 'Even' may be pronounced /iːn/ in fast speech.", "l1_issues": ["Spanish speakers may use 'will' after 'even if.'", "Arabic speakers may confuse 'even if' and 'even though.'"]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Stubborn Speaker", "duration": "10 min", "description": "One student makes plans using 'even if' and the other tries to change their mind.", "adaptation": "Provide scenario cards for lower levels."},
    {"name": "Even If vs Even Though Sorting", "duration": "10 min", "description": "Students sort sentences into groups and explain their choices.", "adaptation": "Provide the rule as a reference."},
    {"name": "Debate with Even If", "duration": "15 min", "description": "Students debate a topic, using 'even if' to dismiss counter-arguments.", "adaptation": "Provide useful phrases and sentence starters."},
]
save_file("even_if.yaml", d)
print("OK: even_if.yaml")

# ─── few.yaml ──────────────────────────────────────────────────────────────────
d = load_file("few.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'Few people came to the party.' Are you happy or disappointed?", "answer": "Disappointed — 'few' has a negative meaning. Almost no one came."},
    {"question": "'A few people came to the party.' Are you happy or disappointed?", "answer": "Relieved — 'a few' has a positive meaning. Some people came."},
    {"question": "Can you say 'few water'?", "answer": "No — 'few' is only for countable nouns. Use 'little' for uncountable."},
]
d["sub_rules"] = [
    {"type": "Few (Negative)", "rule": "Few means 'almost none' and emphasises the lack.", "examples": ["Few students passed the exam.", "Few people know about this."]},
    {"type": "A Few (Positive)", "rule": "A few means 'some' and emphasises that there is a small but sufficient number.", "examples": ["A few students passed the exam.", "I have a few friends in London."]},
    {"type": "Countable Only", "rule": "Few and a few are only used with countable plural nouns.", "examples": ["Few books (correct)", "Few water (wrong — use 'little water')"]},
    {"type": "Very Few / Quite a Few", "rule": "Very few emphasises the negative. Quite a few means 'more than expected.'", "examples": ["Very few people understood.", "Quite a few people came."]},
    {"type": "Position", "rule": "Few and a few go directly before the noun they modify.", "examples": ["Few cars were parked outside.", "A few options remain."]},
]
d["phonetics"] = [
    {"feature": "Vowel sounds", "description": "'Few' is pronounced /fjuː/ with a /j/ glide. 'A few' has the schwa sound /ə/ for the article.", "l1_issues": ["Spanish speakers may pronounce 'few' without the /j/ glide.", "Japanese speakers may struggle with the /f/ sound before /j/."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Traffic Light Analogy", "duration": "10 min", "description": "Red = few (negative). Green = a few (positive). Students create sentences for each.", "adaptation": "Use real classroom objects to practise."},
    {"name": "Countable vs Uncountable Sorting", "duration": "10 min", "description": "Students sort nouns and choose the correct quantifier.", "adaptation": "Provide a reference list of common uncountable nouns."},
    {"name": "Story Completion", "duration": "15 min", "description": "Students complete a story using few, a few, little, and a little.", "adaptation": "Provide multiple choice options for lower levels."},
]
save_file("few.yaml", d)
print("OK: few.yaml")

# ─── first_conditional.yaml ────────────────────────────────────────────────────
d = load_file("first_conditional.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'If it rains, I will stay home.' Is it possible that it will rain?", "answer": "Yes — the first conditional is for real, possible future situations."},
    {"question": "Is 'If I will rain, I stay home' correct?", "answer": "No — we never use 'will' in the if-clause."},
    {"question": "'If you study, you will pass.' Is this a promise, warning, or general truth?", "answer": "It could be a promise or encouragement."},
]
d["sub_rules"] = [
    {"type": "No Will in If-Clause", "rule": "The if-clause always uses present simple, never will.", "examples": ["If it rains, I will stay. (correct)", "If it will rain, I will stay. (incorrect)"]},
    {"type": "Comma Rule", "rule": "When the if-clause comes first, it is followed by a comma. When it comes second, no comma.", "examples": ["If it rains, I will stay home.", "I will stay home if it rains."]},
    {"type": "Unless = If Not", "rule": "Unless can replace 'if...not' in first conditional sentences.", "examples": ["If you don't study, you will fail. = Unless you study, you will fail."]},
    {"type": "Variations in Main Clause", "rule": "The main clause can use other modals (can, may, might, should) instead of will.", "examples": ["If it rains, we can stay inside.", "If you study, you should pass."]},
    {"type": "Imperative in Main Clause", "rule": "The main clause can be an imperative for instructions or warnings.", "examples": ["If the alarm goes off, press the red button.", "If you get lost, call me."]},
]
d["phonetics"] = [
    {"feature": "Weak forms in connected speech", "description": "'If' is often reduced to /ə/ in fast speech. 'Will' reduces to /l/ — 'I'll.'", "l1_issues": ["Spanish speakers may use 'will' in the if-clause.", "Chinese speakers may omit 'if' entirely."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Chain Conditionals", "duration": "10 min", "description": "Students build a chain: 'If I study, I will pass.' Next: 'If I pass, I will celebrate.'", "adaptation": "Provide the first half of each sentence."},
    {"name": "Promise and Warning Cards", "duration": "15 min", "description": "Students draw scenario cards and create promises or warnings.", "adaptation": "Provide sentence frames for weaker students."},
    {"name": "Real-Life First Conditional", "duration": "10 min", "description": "Students write 5 first conditional sentences about their own plans.", "adaptation": "Pair work for lower levels."},
]
save_file("first_conditional.yaml", d)
print("OK: first_conditional.yaml")

# ─── frequency_adverbs.yaml ────────────────────────────────────────────────────
d = load_file("frequency_adverbs.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'I always go to the gym.' Does this mean every single time?", "answer": "Yes — 'always' means 100% of the time."},
    {"question": "'I never eat meat.' Does this mean I eat meat sometimes?", "answer": "No — 'never' means 0% of the time."},
    {"question": "'She is always late.' Where does 'always' go?", "answer": "After the verb 'be' — 'She is always late.' Before other verbs — 'She always arrives late.'"},
]
d["sub_rules"] = [
    {"type": "Position with Main Verbs", "rule": "Frequency adverbs go BEFORE the main verb (except with 'be').", "examples": ["I always brush my teeth.", "She often forgets her keys."]},
    {"type": "Position with Be", "rule": "Frequency adverbs go AFTER the verb 'be.'", "examples": ["I am always late.", "She is usually happy."]},
    {"type": "Position with Auxiliaries", "rule": "Frequency adverbs go AFTER the auxiliary and BEFORE the main verb.", "examples": ["I have always wanted to travel.", "She can never remember names."]},
    {"type": "Scale of Frequency", "rule": "Always (100%) > Usually (80%) > Often (60%) > Sometimes (40%) > Rarely (20%) > Never (0%).", "examples": ["I always drink coffee.", "I rarely drink coffee."]},
    {"type": "Negative Adverbs", "rule": "Never, rarely, and seldom are negative. Do not use 'not' with them.", "examples": ["I never go there. (correct)", "I don't never go there. (incorrect)"]},
]
d["phonetics"] = [
    {"feature": "Stress and rhythm", "description": "Frequency adverbs are usually stressed to emphasise how often something happens.", "l1_issues": ["Spanish speakers may place frequency adverbs after the main verb.", "Arabic speakers may omit frequency adverbs."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Frequency Line", "duration": "10 min", "description": "Draw a line from 0% to 100%. Students place frequency adverbs and create sentences.", "adaptation": "Use visual icons for lower levels."},
    {"name": "Class Survey", "duration": "15 min", "description": "Students survey classmates using 'How often do you...?' and report findings.", "adaptation": "Provide survey question templates."},
    {"name": "Daily Routine Description", "duration": "10 min", "description": "Students describe their daily routines using at least 5 frequency adverbs.", "adaptation": "Provide a model paragraph for lower levels."},
]
save_file("frequency_adverbs.yaml", d)
print("OK: frequency_adverbs.yaml")

# ─── future_continuous.yaml ─────────────────────────────────────────────────────
d = load_file("future_continuous.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'I will be eating at 7pm.' Will I start eating at 7pm?", "answer": "No — you will already be in the middle of eating at 7pm."},
    {"question": "'Will you be using the car tomorrow?' Is this polite or direct?", "answer": "Polite — the future continuous is used for less direct questions about plans."},
    {"question": "'This time tomorrow, I will be flying to Paris.' Where am I now?", "answer": "Not flying yet. At this time tomorrow, you will be in the middle of your flight."},
]
d["sub_rules"] = [
    {"type": "Action in Progress", "rule": "Describes an action that will be in progress at a specific future time.", "examples": ["At 8pm, I will be watching TV.", "This time next week, we will be lying on a beach."]},
    {"type": "Polite Enquiries", "rule": "Used to ask about someone's plans politely.", "examples": ["Will you be using the car tonight?"]},
    {"type": "Parallel Actions", "rule": "Two future continuous actions show both will be in progress at the same time.", "examples": ["While I will be cooking, my husband will be setting the table."]},
    {"type": "Stative Verbs", "rule": "Stative verbs are not normally used in the continuous form.", "examples": ["I will know the answer tomorrow. (not 'will be knowing')"]},
    {"type": "Time Expressions", "rule": "Common expressions: at + time, this time + future period, while, all day/night.", "examples": ["At 6pm, I will be working.", "I will be studying all evening."]},
]
d["phonetics"] = [
    {"feature": "Contraction of will", "description": "'Will be' is almost always contracted — 'I'll be,' 'she'll be.' The /biː/ sound in 'be' is often reduced to /bi/.", "l1_issues": ["Spanish speakers may use the simple future instead of the future continuous.", "Chinese speakers may find the continuous aspect difficult."]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Future Snapshot", "duration": "15 min", "description": "Give a specific future time. Students write 5 things they will be doing at that moment.", "adaptation": "Provide sentence starters for lower levels."},
    {"name": "Polite Request Role-Play", "duration": "10 min", "description": "Students practise making polite enquiries using the future continuous.", "adaptation": "Provide dialogue templates for weaker students."},
    {"name": "Parallel Actions Timeline", "duration": "15 min", "description": "Students draw a timeline and describe what people will be doing simultaneously.", "adaptation": "Use visual timelines for support."},
]
save_file("future_continuous.yaml", d)
print("OK: future_continuous.yaml")

# ─── future_going_to.yaml ───────────────────────────────────────────────────────
d = load_file("future_going_to.yaml")
d["meaning"]["ccqs"] = [
    {"question": "'I am going to travel next month.' Did I decide just now or before now?", "answer": "Before now — 'going to' is for plans made before speaking."},
    {"question": "'Look at those clouds! It is going to rain.' What evidence do I have?", "answer": "The dark clouds — 'going to' is for predictions based on visible evidence."},
    {"question": "'I am going to eat pizza tonight.' Is this a spontaneous decision?", "answer": "No — it is a plan. For spontaneous decisions, use 'will.'"},
]
d["sub_rules"] = [
    {"type": "Plan (Intention)", "rule": "Going to expresses a plan or intention made before speaking.", "examples": ["I am going to study medicine.", "They are going to get married in June."]},
    {"type": "Prediction with Evidence", "rule": "Going to is used for predictions when there is visible evidence now.", "examples": ["Look at the sky — it's going to rain.", "He's going to fail — he never studies."]},
    {"type": "Form", "rule": "The verb 'be' changes to match the subject. 'Going to' does not change.", "examples": ["I am going to leave.", "She is going to leave.", "They are going to leave."]},
    {"type": "Gonna (Informal)", "rule": "In informal speech, 'going to' is often pronounced 'gonna.' Not used in formal writing.", "examples": ["I'm gonna call you later. (informal)", "I am going to call you later. (formal)"]},
    {"type": "Negative and Questions", "rule": "Negate with 'not' after 'be.' Invert 'be' and subject for questions.", "examples": ["I am not going to travel.", "Are you going to travel?"]},
]
d["phonetics"] = [
    {"feature": "Gonna vs going to", "description": "In natural speech, 'going to' is almost always reduced to 'gonna.' Learners who always say the full form can sound overly formal.", "l1_issues": ["Spanish speakers may pronounce 'going to' too clearly, missing the natural reduction.", "Japanese speakers may struggle with the nasal /ŋ/ sound in 'going.'"]}
]
d["teaching"]["recommended_activities"] = [
    {"name": "Weekend Plans Interview", "duration": "15 min", "description": "Students interview each other about weekend plans using 'going to.'", "adaptation": "Provide question templates for lower levels."},
    {"name": "Evidence Predictions", "duration": "10 min", "description": "Show pictures with clear evidence. Students make predictions using 'going to.'", "adaptation": "Provide sentence frames for weaker students."},
    {"name": "Plan vs Spontaneous Decision", "duration": "15 min", "description": "Students sort scenarios into plans (going to) and spontaneous decisions (will).", "adaptation": "Provide the scenarios as cards for sorting."},
]
save_file("future_going_to.yaml", d)
print("OK: future_going_to.yaml")

print("\nPart 1 complete: 10 files processed.")
