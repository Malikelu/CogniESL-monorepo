#!/usr/bin/env python3
"""Populate remaining grammar files - Part 1"""
import os, yaml

grammar_dir = '/Users/marcos/Documents/Marcos-Brain/00_ACTIVE/ESL with AI/forge/data/grammar/'

def write_file(slug, title, desc, level, core_meaning, timeline, contrast, ccqs, contexts, form_aff, form_neg, form_q, sub_rules, uses, phonetics, methodology, tips, activities):
    lines = []
    lines.append(f'grammar_point: {slug}')
    lines.append(f'title: "{title}"')
    lines.append(f'description: "{desc}"')
    lines.append(f'level: {level}')
    lines.append('')
    lines.append('meaning:')
    lines.append(f'  core_meaning: "{core_meaning}"')
    if timeline: lines.append(f'  timeline: "{timeline}"')
    if contrast: lines.append(f'  contrast: "{contrast}"')
    lines.append('  ccqs:')
    for c in ccqs: lines.append(f'    - question: {c[0]}'); lines.append(f'      answer: {c[1]}')
    lines.append('  example_generator:')
    lines.append('    contexts:')
    for ctx in contexts: lines.append(f'      - {ctx}')
    lines.append('    cultural_notes: []')
    lines.append(f'    min_examples: 5')
    lines.append('')
    lines.append('form:')
    for block, struct, ctxs in [('affirmative', form_aff, contexts[:3]), ('negative', form_neg, contexts[:3]), ('questions', form_q, contexts[:3])]:
        lines.append(f'  {block}:')
        lines.append(f'    structure: "{struct}"')
        lines.append('    example_generator:')
        lines.append('      contexts:')
        for c in ctxs: lines.append(f'        - {c}')
        lines.append('      min_examples: 4')
    lines.append('')
    if sub_rules:
        lines.append('sub_rules:')
        for sr in sub_rules:
            lines.append(f'  - rule: {sr[0]}')
            lines.append(f'    type: {sr[1]}')
            lines.append('    examples:')
            for e in sr[2]: lines.append(f'      - {e}')
        lines.append('')
    if uses:
        lines.append('use:')
        for u in uses:
            lines.append(f'  - context: {u[0]}')
            lines.append(f'    description: {u[1]}')
            lines.append('    examples:')
            for e in u[2]: lines.append(f'      - {e}')
        lines.append('')
    if phonetics:
        lines.append('phonetics:')
        for p in phonetics:
            lines.append(f'  - note: {p[0]}')
            if p[1]: lines.append('    example_generator:'); lines.append('      contexts:'); lines.append(f'        - {p[1]}')
            if p[2]: lines.append(f'    l1_issue: {p[2]}')
        lines.append('')
    lines.append('teaching:')
    lines.append(f'  methodology: {methodology}')
    lines.append('  tips:')
    for t in tips: lines.append(f'    - {t}')
    lines.append('  recommended_activities:')
    for a in activities: lines.append(f'    - name: {a[0]}'); lines.append(f'      duration: {a[1]}'); lines.append(f'      adaptation_notes: {a[2]}')
    
    with open(os.path.join(grammar_dir, f'{slug}.yaml'), 'w') as f:
        f.write('\n'.join(lines))

# === FILES ===

write_file('expanded_prepositions', 'Expanded Prepositions', 'Multi-word prepositions: in addition to, with regard to, on behalf of.', 'C1',
    'Fixed multi-word units that function as single prepositions with idiomatic meanings.',
    'Timeless — used across all tenses.',
    'Simple preposition = on the table vs Expanded = in front of the television.',
    [('Does this function as a single preposition?', 'Yes, the words together act as one unit.'), ('Can you change words in the middle?', 'No, the expression is fixed.')],
    ['formal writing', 'academic essays', 'business correspondence', 'legal documents'],
    'Expanded preposition + noun phrase: In addition to his salary, he receives bonuses.',
    'Expanded preposition + negative phrase: Without regard for safety, they continued.',
    'Can appear in questions: In terms of cost, is this feasible?',
    [('Two-word expanded prepositions', 'grammatical', ['according to the report', 'because of the delay', 'instead of waiting']),
     ('Three-word expanded prepositions', 'grammatical', ['in addition to the main course', 'with regard to your complaint', 'on behalf of the team'])],
    [('Formal writing', 'Preferred in formal registers for precision and tone.', ['In accordance with the regulations, all participants must register.', 'With respect to your proposal, we have several concerns.'])],
    [('Stress on content word', 'formal speech', 'Speakers of syllable-timed languages may give equal stress to all words.')],
    'Guided discovery', ['Teach as fixed chunks', 'Contrast with simple prepositions', 'Provide a reference list by function'],
    [('Register transformation', 15, 'Students rewrite informal sentences using expanded prepositions.')])

write_file('right_dislocation', 'Right-Dislocation', 'Moving a pronoun to the end of a sentence for emphasis: "She is really smart, my sister."', 'C1',
    'A structure where a noun phrase is moved to the end of a sentence and replaced by a pronoun. Used for emphasis or clarification in spoken English.',
    'Present — the dislocated element refers to the present.',
    'Standard = My sister is really smart. vs Right-dislocation = She is really smart, my sister.',
    [('Is there a pronoun at the beginning and a noun at the end?', 'Yes, that is right-dislocation.'), ('Is this formal or informal?', 'Informal — used in spoken English.')],
    ['spoken English', 'informal conversation', 'emphasis', 'clarification'],
    'Pronoun + verb + complement + comma + noun phrase: She is really smart, my sister.',
    'Same pattern: He did not show up, John.',
    'Not typically used in questions.',
    [('The dislocated noun clarifies the pronoun', 'pragmatic', ['She is really smart, my sister.', 'He did not show up, John.', 'They are very kind, my neighbors.'])],
    [('Clarification', 'Used when the listener might not know who the pronoun refers to', ['She is really smart, my sister.', 'They are very kind, my neighbors.'])],
    [('Stress on the dislocated noun', 'emphasis', 'Some L1 speakers are not familiar with this structure.')],
    'Guided discovery', ['Use authentic spoken examples', 'Explain the clarifying function', 'Practice with real names and relationships'],
    [('Dislocation Practice', 10, 'Students transform standard sentences into right-dislocation.')])

write_file('present_perfect_recent', 'Present Perfect of Recent Past', 'Using present perfect with just to talk about actions that have just been completed.', 'B1',
    'Actions that have just finished — very recent past with present relevance. Usually with just.',
    'Just now — moments before speaking.',
    'Recent past = I have just arrived. (moments ago) vs Past simple = I arrived an hour ago. (specific time)',
    [('Did this happen moments ago?', 'Yes, it is very recent.'), ('Is just used?', 'Usually yes.')],
    ['arrivals and departures', 'completed actions', 'news and announcements'],
    'Subject + have/has + just + past participle: I have just arrived. / She has just finished.',
    'Subject + have/has + not + yet: I have not finished yet.',
    'Have/Has + subject + just + past participle?: Have you just arrived?',
    [('Just goes between have/has and the past participle', 'word_order', ['I have just eaten.', 'She has just left.']),
     ('Also used with already and yet', 'grammatical', ['I have already done it.', 'Have you finished yet?'])],
    [('Arrivals and departures', 'Talking about very recent events', ['I have just arrived at the airport.', 'She has just left the office.']),
     ('Completed actions', 'Reporting something that just finished', ['I have just finished my homework.', 'We have just heard the news.'])],
    [('Stress on just for emphasis', 'emphasis', 'Many L1 speakers use present simple when present perfect is needed.')],
    'PPP', ['Use real classroom events', 'Practice with just, already, yet', 'Contrast with past simple using timelines'],
    [('News Reporter', 10, 'Students report recent events using have just.')])

write_file('disapproval', 'Disapproval (If you will)', 'Using if you will to express mild disapproval or distance from a statement.', 'C2',
    'A polite way to express mild disapproval or to distance yourself from what you are saying. Suggests if you are willing to call it that.',
    'Present — the disapproval is about now.',
    'Direct = He is not really a genius. vs Disapproval = He is a genius, if you will. (mild irony)',
    [('Does the speaker fully agree?', 'Not entirely — there is mild disapproval.'), ('Is this formal?', 'Formal and somewhat literary.')],
    ['formal writing', 'literary English', 'mild criticism', 'ironic statements'],
    'Statement + if you will: It is a solution, if you will. / He is an expert, if you will.',
    'Same structure: It is not ideal, if you will.',
    'Not used in questions.',
    [('Usually comes at the end of a statement', 'word_order', ['It was a disaster, if you will.', 'She is a bit eccentric, if you will.'])],
    [('Mild criticism', 'Expressing disapproval politely', ['It is a solution, if you will.', 'He is generous, if you will.'])],
    [('Stress on will for ironic effect', 'emphasis', 'Very advanced structure — most L1 speakers will not use this.')],
    'Guided discovery', ['Use literary examples', 'Explain the ironic/distance function', 'Contrast with direct statements'],
    [('Ironic Statements', 10, 'Students create ironic statements using if you will.')])

write_file('sentential_aspect', 'Sentential Aspect', 'The relationship between action and time: perfective (completed) vs progressive (ongoing) vs habitual (repeated).', 'C1',
    'Sentential aspect describes how an action relates to time. Perfective = completed action. Progressive = ongoing action. Habitual = repeated action.',
    'Varies by aspect — perfective = completed, progressive = ongoing, habitual = repeated.',
    'Perfective = I wrote a letter. (completed) vs Progressive = I was writing a letter. (ongoing)',
    [('Is the action completed or ongoing?', 'Completed = perfective, ongoing = progressive'), ('Does this happen regularly?', 'Yes = habitual aspect.')],
    ['academic writing', 'linguistic analysis', 'advanced grammar', 'formal descriptions'],
    'Perfective: Subject + past simple: I wrote a letter. / Progressive: Subject + be + verb-ing: I was writing a letter.',
    'Same patterns with negation: I did not write a letter. / I was not writing a letter.',
    'Did + subject + verb?: Did you write a letter?',
    [('Perfective aspect — completed actions', 'grammatical', ['I wrote a letter.', 'She finished the project.']),
     ('Progressive aspect — ongoing actions', 'grammatical', ['I was writing a letter.', 'She was working on the project.']),
     ('Habitual aspect — repeated actions', 'grammatical', ['I write letters every day.', 'She always arrives early.'])],
    [('Academic analysis', 'Describing how actions relate to time', ['The perfective aspect presents the action as completed.', 'The progressive aspect focuses on the internal structure of the event.'])],
    [('No specific phonetic pattern', 'written English', 'This is a metalinguistic concept — most L1 speakers do not analyze aspect explicitly.')],
    'Guided discovery', ['Use timelines to visualize aspects', 'Contrast perfective vs progressive explicitly', 'Use authentic texts for analysis'],
    [('Aspect Identification', 15, 'Students identify and classify aspect in authentic texts.')])

write_file('continuous_perfect_infinitive', 'Continuous and Perfect Infinitive', 'Infinitive forms showing aspect: continuous (to be doing), perfect (to have done), perfect continuous (to have been doing).', 'C1',
    'Infinitives can show aspect. Continuous infinitive = ongoing action. Perfect infinitive = completed action. Perfect continuous = ongoing action completed before another point.',
    'Continuous = ongoing. Perfect = completed before reference point. Perfect continuous = ongoing and completed.',
    'Simple infinitive = I want to go. vs Continuous = I want to be going. (ongoing)',
    [('Is the action ongoing or completed?', 'Ongoing = continuous, completed = perfect'), ('Does the infinitive show aspect?', 'Yes — continuous or perfect infinitive.')],
    ['after certain verbs', 'expressing regret', 'reporting', 'formal writing'],
    'Continuous: to be + -ing: I want to be studying. / Perfect: to have + past participle: I want to have finished.',
    'Not + infinitive: I want not to be studying.',
    'Not typically used in questions.',
    [('Continuous infinitive — ongoing action', 'grammatical', ['She seems to be working hard.', 'I want to be traveling the world.']),
     ('Perfect infinitive — completed action', 'grammatical', ['I am glad to have met you.', 'She claims to have seen a UFO.']),
     ('Perfect continuous — ongoing and completed', 'grammatical', ['He seems to have been waiting for hours.', 'I would like to have been working on that project.'])],
    [('Expressing regret', 'Using perfect infinitive for things you wish had happened', ['I would like to have studied harder.', 'She regrets not to have traveled more.']),
     ('Reporting', 'Using infinitives in reported speech', ['He claimed to have seen the accident.', 'She seems to be working on something important.'])],
    [('Weak form of to /tuː/ → /tə/', 'connected speech', 'Very advanced structure — most L1 speakers will not use this.')],
    'Guided discovery', ['Start with simple infinitives, then add aspect', 'Use real examples from news and literature'],
    [('Infinitive Transformation', 10, 'Students transform simple infinitives into continuous/perfect forms.')])

write_file('existential', 'Existential Constructions (There is/are)', 'Using there is/are to say that something exists or is present.', 'A2',
    'There is/are introduces the existence of something. There is not a place — it is a grammatical subject. The real subject comes after the verb.',
    'Present (there is/are) or past (there was/were).',
    'There is = There is a book on the table. (existence) vs A book is on the table. (location)',
    [('Are we saying something exists?', 'Yes — use there is/are.'), ('Is this new information?', 'Yes — there is/are introduces new information.')],
    ['describing places', 'talking about what exists', 'introducing new information', 'describing scenes'],
    'There is + singular noun: There is a book on the table. / There are + plural noun: There are many people in the room.',
    'There is/are + not + noun: There is not a solution. / There are not any tickets left.',
    'Is/Are + there + noun?: Is there a problem? / Are there any questions?',
    [('Use is with singular nouns and non-count nouns', 'grammatical', ['There is a book.', 'There is some water.']),
     ('Use are with plural nouns', 'grammatical', ['There are many people.', 'There are three books.']),
     ('There is not a place in this structure', 'semantic', ['There is a book. (existence)', 'The book is there. (location)'])],
    [('Describing places', 'Saying what exists in a location', ['There is a park near my house.', 'There are many restaurants in this area.']),
     ('Introducing new information', 'Presenting something for the first time', ['There is a new student in our class.', 'There are some things I need to tell you.'])],
    [('Weak form of there /ðeər/ → /ðər/', 'connected speech', 'Some L1 speakers omit there or it as dummy subjects.')],
    'PPP', ['Use real situations to demonstrate existence', 'Contrast with location (the book is there)', 'Practice with classroom objects and people'],
    [('What is in the Room?', 10, 'Students describe what exists in different locations using there is/are.')])

write_file('it_cleft', 'It-Cleft Sentences', 'Using it + be + focused element + who/that for emphasis: It was John who broke the window.', 'B2',
    'It-cleft sentences divide a single clause into two parts for emphasis. The focused element comes after it was/who/that.',
    'Depends on the tense used.',
    'Simple = John broke the window. vs It-cleft = It was John who broke the window.',
    [('Is this sentence dividing information into two parts?', 'Yes, it is an it-cleft.'), ('What element is being emphasized?', 'The element after it was.')],
    ['emphasis', 'contrast', 'correcting misunderstandings', 'formal writing'],
    'It + be + focused element + who/that + clause: It was John who broke the window. / It was yesterday that she arrived.',
    'It + be + not + focused element: It was not John who broke the window.',
    'Was/Were + it + focused element?: Was it John who broke the window?',
    [('It-cleft emphasizes one element of the sentence', 'grammatical', ['It was Mary who called. (not John)', 'It was yesterday that she arrived. (not today)', 'It is the price that matters most. (not the quality)'])],
    [('Emphasis', 'Highlighting specific information', ['It was the teacher who explained it best.', 'It was yesterday that she arrived.']),
     ('Correcting misunderstandings', 'Clarifying what actually happened', ['It was not me who broke the window — it was John.', 'It was an accident, not intentional.'])],
    [('Stress on the focused element', 'emphasis', 'Many L1 speakers do not use cleft sentences, missing opportunities for natural emphasis.')],
    'Guided discovery', ['Use contrastive contexts (I thought it was X, but it was actually Y)', 'Practice identifying the focused element', 'Contrast with simple sentences'],
    [('Emphasis Practice', 15, 'Students rewrite simple sentences using it-cleft for emphasis.')])

write_file('complex_reporting', 'Complex Reporting Structures', 'Advanced reporting structures: passive reporting verbs, reporting with that-clauses, and reporting questions.', 'C1',
    'Reporting what others said or thought using complex structures. Includes passive reporting (It is said that...), reporting verbs with that-clauses, and reported questions.',
    'Depends on the tense of the reporting verb.',
    'Simple reporting = He said that he was tired. vs Passive reporting = It is said that he is rich.',
    ('Is the speaker reporting their own words or someone else\'s?', 'Someone else\'s — that is reporting.'),
    ['news reporting', 'academic writing', 'formal communication', 'indirect speech'],
    'Passive: It is said/reported/believed + that + clause: It is said that he is rich. / Active: Subject + reporting verb + that + clause: Experts claim that climate change is accelerating.',
    'It is not believed that... / Experts deny that...',
    'Not typically used in questions.',
    [('Passive reporting verbs: It is said/reported/believed/thought/known/expected that...', 'grammatical', ['It is believed that the economy will improve.', 'It is known that smoking causes cancer.']),
     ('Active reporting verbs: say, claim, suggest, argue, deny, admit, explain, warn', 'grammatical', ['Scientists claim that the study is flawed.', 'The government denied that there was a problem.']),
     ('Reported questions use whether or if, not question word order', 'grammatical', ['She asked whether I was coming.', 'They wanted to know if I had finished.'])],
    [('News reporting', 'Reporting information from sources', ['It is reported that the president will resign.', 'Sources claim that negotiations are ongoing.']),
     ('Academic writing', 'Reporting research findings', ['Studies suggest that exercise improves mental health.', 'It has been argued that technology is harmful.'])],
    [('Stress on the reporting verb in passive structures', 'emphasis', 'Word order in reported questions — some L1 speakers keep question order.')],
    'Guided discovery', ['Use real news headlines as examples', 'Practice transforming direct speech to reported speech', 'Contrast active and passive reporting'],
    [('News Reporter', 15, 'Students rewrite news headlines using passive reporting structures.')])

write_file('relative_clause_reductors', 'Relative Clause Reductors', 'Reducing relative clauses by omitting the relative pronoun or using participle clauses.', 'C1',
    'Making sentences more concise by reducing relative clauses. Instead of the man who is standing there, we say the man standing there.',
    'Timeless — applies to all tenses.',
    'Full relative clause = The man who is standing there vs Reduced = The man standing there.',
    ('Can we make this sentence shorter?', 'Yes — by reducing the relative clause.'), ('Is the relative pronoun necessary?', 'No — it can be omitted in some cases.'),
    ['academic writing', 'formal communication', 'concise expression', 'advanced grammar'],
    'Omit relative pronoun + be: The man (who is) standing there is my brother. / Use participle: The book (which was) written by Shakespeare is famous.',
    'Same reduction: The people (who were) invited to the party had fun.',
    'Not typically used in questions.',
    [('Can omit relative pronoun when it is the subject of a passive clause', 'grammatical', ['The car (which was) parked outside is mine.', 'The letter (that was) sent yesterday arrived today.']),
     ('Can use present participle for active meaning', 'grammatical', ['The woman (who is) sitting next to me is my sister.', 'People (who are) living in cities face more pollution.']),
     ('Can use past participle for passive meaning', 'grammatical', ['The cake (that was) made by my mom was delicious.', 'The problems (that were) discussed were serious.'])],
    [('Academic writing', 'Making writing more concise', ['The data collected shows a clear trend.', 'The participants interviewed reported positive results.']),
     ('Formal communication', 'Expressing ideas efficiently', ['The man standing by the door is the manager.', 'The book recommended by the teacher is excellent.'])],
    [('No specific phonetic pattern — focus on correct structure', 'written English', 'Many L1 speakers do not reduce relative clauses, making speech sound overly formal.')],
    'Guided discovery', ['Start with full relative clauses, then show reductions', 'Use authentic academic texts as examples', 'Practice identifying what can be reduced'],
    [('Sentence Reduction', 10, 'Students transform full relative clauses into reduced forms.')])

print('Part 1 complete!')
