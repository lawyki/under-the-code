// Pass 31 gate prompts (tests/pass31/gate.mjs). The full text is reproduced in docs/pass-31-calibration.md, with the
// hash of every prompt (npm run fig:hash). The author never reads this file (brief section 6: the author learns only
// pass or fail and the criterion name). Every tester is a fresh Sonnet 5.5 session with no tools, run in an empty
// temporary directory outside the repo: it sees only what its message holds.

export const SYSTEM = `You help test the figures of a book about how computers work. You only look and report what you see and understand. You never suggest changes, never advise, never vote on anything but the question asked. Answer with exactly one JSON object and nothing else.`;

const BOOK = packet => `THE BOOK SO FAR (everything you have read before the figure; figures that came earlier are left out):
<<<
${packet}
>>>`;

// the fields every describer fills the same way
const CAUSE_DRAWN = `"cause_drawn": "what in the picture shows the cause: name the drawn thing (a shape, a card, a symbol, an arrow, a light) that you see act, light up, match or point when each change happens, and say what it shows. Write \\"none\\" if the picture shows things changing but nothing drawn shows why, if the cause is only written out in words, or if you know the cause only from the text you read before the figure"`;
const CAUSE_DRAWN_STILL = `"cause_drawn": "what in the picture shows the cause: name the drawn thing (a rule card, an arrow, a drawn state, a symbol, a shape) that shows why the change happens, and say what it shows. Write \\"none\\" if nothing drawn shows why, if the cause is only written out in words, or if you know the cause only from the text you read before the figure"`;
const UNEXPLAINED = `"unexplained_words": ["one entry per word or label written in letters in the picture whose meaning here you had to guess, written as the word, a colon, and why you could not place it: a word the text you read never uses, or a word used as the name of a state, a mode, a step or a setting that neither the picture nor the text says what it is, even if you could guess it from the rest of the picture. This includes a word tagged onto a part to say what it is doing or what condition it is in (for example "head · ready"), unless the picture or the text says what that condition is. Leave out a word naming a drawn part or object the text has described, and a plain everyday word for an action, even where the picture puts it somewhere you did not expect. Leave the list empty if every word is plain"],
 "unexplained_marks": ["each symbol, number, sign or mark in the picture whose meaning here you had to guess: neither the picture nor the text you read says what it means or what it refers to. Leave the list empty if there is none"]`;

// (a) the judge: 12 frames, the prose up to the figure
export const JUDGE = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure: an animated picture, shown as 12 frames captured at equal steps through one loop of its animation. Frame 1 is the start of the loop; after frame 12 the loop starts again at frame 1. The figure has no caption and no explanation: you have only the picture and the text you have read.

Describe what the figure shows and teaches, from the frames and the text before it only. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The 12 frames follow. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn, in plain words: the things in the picture and where they are",
 "panels": ["one entry per separate picture inside the figure, saying what it is. A key, a rule card, a label or a result line that belongs to a scene is part of that scene. A separate panel is its own picture: a second scene, a table, a list of steps, a replay of steps, a timeline, a block of text"],
 "changes": "what changes from frame to frame, in order",
 "cause": "what makes each change happen, as the picture shows it",
 ${CAUSE_DRAWN},
 "result": "where it ends up: the result the figure arrives at",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "text_pieces": 0,
 "read_only": "any part of the idea you could get only by reading words, a table or a list in the picture, because the picture never shows it happening or drawn; \\"none\\" if none",
 "repeated": "anything the figure shows twice in different forms, for example a scene and also a step-by-step replay of the same steps, or the same rules written out again as a table. A label naming a drawn thing, or a short result line saying what the scene arrives at, is not a repeat; \\"none\\" if none",
 ${UNEXPLAINED},
 "unsure": ["each doubt you still have, after looking at every frame, about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (the exact timing of the animation, the loop starting again, layout, colours). Leave the list empty if you have none"]
}
("text_pieces" is the number of separate pieces of text you read in the picture.)`;

// (d) the t=0-only judge: the reduced-motion still (also the whole test of a figure that does not animate)
export const STILL = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure as a reader who has turned animation off sees it: one still picture that does not move. The figure has no caption and no explanation: you have only this picture and the text you have read.

Describe what the figure shows and teaches, from the still and the text before it only. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The still follows. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn, in plain words",
 "panels": ["one entry per separate picture inside the figure (a key, rule card, label or result line belongs to its scene)"],
 "changes": "what the still shows changing, happening or having happened: the process it depicts, as you work it out from what is drawn",
 "cause": "what makes it happen, as the picture shows it",
 ${CAUSE_DRAWN_STILL},
 "result": "the result the figure shows or states",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "text_pieces": 0,
 "read_only": "any part of the idea you could get only by reading words, a table or a list in the picture, because the picture never draws it; \\"none\\" if none",
 ${UNEXPLAINED},
 "unsure": ["each doubt you still have about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (layout, colours). Leave the list empty if you have none"]
}
("text_pieces" is the number of separate pieces of text you read in the picture.)`;

// (e) the text-stripped judge: the same frames with every <text> removed (one frame for a figure that does not animate)
export const STRIPPED = (packet, n = 12) => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure ${n > 1 ? `as ${n} frames captured at equal steps through one loop of its animation (frame 1 is the start; after frame ${n} it starts again)` : 'as one still picture (the figure does not animate)'}. Every word, letter and number has been removed from the picture: only shapes, marks, colours${n > 1 ? ' and their motion' : ''} are left. There is no caption.

Say what the picture shows by its shapes${n > 1 ? ' and motion' : ''} alone, using the text you have read only to name things. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The ${n > 1 ? `${n} frames follow` : 'picture follows'}. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn: the shapes and what they seem to stand for",
 "moves": "${n > 1 ? 'what moves or changes, frame by frame' : 'what the shapes show moving, changing or happening (arrows, drawn states, before and after)'}",
 "cause": "what causes what: which thing acts, and what happens to which other thing as a result",
 ${CAUSE_DRAWN},
 "result": "where it ends up",
 "unsure": ["each doubt you still have about what moves, what causes what, or the result${n > 1 ? ' after looking at every frame' : ''}. Leave out doubts you resolved; leave the list empty if you have none"]
}`;

// (b) the scorer: a describer's description against the intent sentence, for the figure's job
const JOBS = {
  'function': `The figure's job is "function": it shows how something works. The bar for this job (the book owner's approved reference) is one calm scene, the core function, few labels, motion that is the mechanism, and the result stated.`,
  'real thing': `The figure's job is "real thing": it draws a real physical object, machine or place as it looks, its parts drawn with their own physical features (a wheel's contacts and wiring, round keys and lamps, a cabinet's front), even when the drawing is simplified or flattened; and the reader sees in it what the intent says happens. This job is judged on showing the real object as it looks and what visibly happens in it, not on explaining how or why it works: a reader who cannot say what the object is for, why it is built or wired as it is, or why it gives these particular values does not fail for that. Plain labelled boxes joined by arrows or lines standing for the parts, a table, a timeline or text in a frame is never a real thing.`,
  'two-part': `The figure's job is "two-part": one panel shows the real thing and the other shows its function, in one figure. Two panels are expected; each must do its job.`,
};
const DRAWN = `A thing that holds still while its matching rule card stays lit is shown stopping, even though the card's word names the stop. The cause counts only when the picture draws it: "cause_drawn" must name a drawn thing (a shape, card, symbol, arrow or light) that shows the intent's cause. It fails if "cause_drawn" is "none", empty, or names only written words; if "read_only", "unsure" or "cause_drawn" says the rules, the cause or the result is not drawn or not shown; or if the cause given comes only from the book's text before the figure or from the reader's own guess.`;
const DRAWN_STILL = `The cause counts only when the picture draws it: "cause_drawn" must name a drawn thing (a rule card, an arrow, a drawn state, a symbol) that shows the intent's cause. It fails if "cause_drawn" is "none", empty, or names only written words; if "read_only", "unsure" or "cause_drawn" says the rules or the cause are not drawn; or if the cause given comes only from the book's text before the figure or from the reader's own guess. A still cannot show the change happening, so the result may be worked out from the drawn rules and states or stated by a short result line.`;
const UNEXPLAINED_BASE = `unexplained: it fails if "unexplained_words" lists any word or label (a word the reader had to guess, or one naming something the text never introduced, fails even when the reader got the mechanism anyway; an entry that is only a number or a sign is judged as a mark). The one exception: an entry whose own reason says the text describes the thing the word names and the reader was unsure only where or how the picture places it does not count. It also fails if an entry in "unexplained_marks" shows that the reader could not get what changes, why, or the result. Judge only these two lists here (doubts in "unsure" are scored elsewhere). A mark the description itself uses in the intent's way in "changes", "cause" or "result" is resolved; so is a mark the description itself resolves elsewhere (for example strokes the reader took as counting marks and then used that way in "result"), one about decoration, or a doubt only about how a short result line refers to the drawn marks (whether it states the task or the answer, which mark is the "+ 1") when "result" matches the intent, does not count.`;
// a real thing is judged on showing the object as it looks: its parts' names, the letters on them, a legend and a short
// note on a part are part of that job (taught-yet still checks every token mechanically)
// (from revision 1 of the follow-up, try26: a rule of its own, not the base rule with exceptions, which the scorer
// sometimes applied over them)
const UNEXPLAINED_REAL = `unexplained (real thing): this job draws the object as it looks, so the words, letters and numbers that are part of drawing it are expected: a part's name, or one label naming parts (a key, a wheel, a lamp, a reflector, a cabinet, or two part names on one label), the letters or numbers written on a part (a key's letter, a wheel's position letter), a legend for the drawing's colours or lines, and a short note on the drawing saying what a part does or how the drawing simplifies the object, with every word in that note. None of these counts, in either list, even when the reader had to guess it or the text never used it (a separate mechanical check makes sure every such word is an everyday word or taught before the figure). The test fails only if "unexplained_words" lists a word tagged onto a part to name a state, mode or condition it is in that neither the picture nor the text explains (for example a part tagged "· ready"), or if an entry in "unexplained_marks" shows that the reader could not tell what object is drawn. Judge only these two lists here (doubts in "unsure" are scored elsewhere).`;
const UNEXPLAINED_TEST = job => job !== 'real thing' ? UNEXPLAINED_BASE : UNEXPLAINED_REAL;
const OBJECT = `object: the description recognises the real object or scene the intent names, its parts drawn with their own physical features (for example wheels with their rows of contacts and the wiring inside them, round keys and lamps). It fails only when the parts are plain boxes or labels with nothing of the part drawn in them (at most a name, a letter or a number), joined by arrows or lines, or when the figure is a table, a timeline or text in a frame. Parts drawn with their own detail pass even when the reader calls them boxes or the drawing a diagram.`;
// the still of a real thing (author decision D1, 2026-10-24): it passes when it shows the real object as it looks, its
// parts identifiable; the mechanism is carried by the animation (the 12-frame judge) and is not tested on the still
const OBJECT_STILL = `${OBJECT} The parts must also be identifiable: the reader names them, or tells them apart by their own features.`;
// a real thing's cause is its part changing as drawn; how that change gives the result inside the object is function
const REAL_CAUSE = ` For this job (real thing), the cause is drawn when the part the intent names is drawn changing (it moves or steps, or its position letter or drawn state changes); how that change produces the result inside the object is not tested, so a reader who says nothing shows how it does so does not fail this test.`;
const RUBRIC = {
  judge: job => `Score the description against the intent. PASS only if every test below passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: the same thing changes, for the same cause, with the same result. Paraphrase is fine and extra correct detail is fine. It fails if what changes, why, or the result is missing, vague or wrong, or if the description gives a different mechanism, a different representation or a different example than the intent names. ${DRAWN}${job === 'real thing' ? REAL_CAUSE : ''}
2. ${UNEXPLAINED_TEST(job)}
${job === 'real thing' ? `3. ${OBJECT}` : `3. carried by the picture: the mechanism is shown happening or drawn, not only written. It fails if "read_only" names a part of the mechanism (what changes, why, or the result) that the picture never shows, or if the cause is not drawn (test 1). Things moving is not enough: the picture must show what makes them move. A short result line that states what the drawn change amounts to (for example a sum, which also says what the drawn marks count) is part of this bar ("the result stated") and does not fail the test, even when "read_only" names it, as long as the change it sums up is shown happening.
4. one scene, shown once: ${job === 'two-part' ? 'at most two panels, and' : 'one panel only (the scene, with its own rule cards, keys and result line), and'} "repeated" is "none". It fails if the figure adds a separate table, list of steps, replay or block of text beside the scene, or shows the same steps twice. A short result line that states what the scene arrives at is not a repeat, even when "repeated" names it.
5. few words: the picture uses few words. It fails if "text_pieces" is more than 8 for one panel, or if the words, not the picture, carry the mechanism.`}`,
  still: job => job === 'real thing' ? `This description comes from the still alone, the frame a reader with animation turned off sees (for a figure that does not animate, the whole figure). The figure's job is "real thing": its still passes when it shows the real object the intent names as it looks, its parts identifiable. The still does not have to show what changes, why, or the result: the animation carries that, and another test scores it on the frames. So do not score the intent's mechanism here: a reader who says the still shows no change, or who gets the change, its cause or the result wrong or not at all, does not fail for that. PASS only if both tests pass; otherwise FAIL.
1. ${OBJECT_STILL}
2. ${UNEXPLAINED_TEST(job)}` : `This description comes from the still alone, the frame a reader with animation turned off sees (for a figure that does not animate, the whole figure). A still cannot move, so the change may be shown by drawn states, arrows, a before and after, drawn rules, or a stated result, and the reader may have to work the motion out. Score it against the intent: a reader who works out, from what is drawn, the same change, cause and result as the intent passes, even when the reader says the change is implied rather than seen. PASS only if every test passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: what changes, why, and the result, as the intent says. Paraphrase is fine. It fails if any of the three is missing, vague or wrong, or a different mechanism is given. ${DRAWN_STILL}${job === 'real thing' ? ` For this job (real thing) the change may also be shown on the drawn object by its parts' drawn states, a row of results, or a short note on the part that changes together with that part's drawn state (a still cannot move); such a note counts as drawn.${REAL_CAUSE}` : ''}
2. ${UNEXPLAINED_TEST(job)}
3. ${job === 'real thing' ? OBJECT : `few words: it fails if "text_pieces" is more than 8 for one panel.`}`,
  stripped: job => job === 'real thing' ? `This description comes from the figure with every word, letter and number removed (the letters on keys, wheels or dials too): only shapes (and, for an animated figure, their motion) were left. The figure's job is "real thing", so score whether the picture without its words still shows the real object and what changes in it, as the intent says. Names are not expected, and why the object behaves as it does is not tested for this job. PASS only if both tests pass; otherwise FAIL.
1. the object: the shapes the description gives can be matched to the parts of the object the intent names, drawn with their own features (for example panels with rows of contacts and crossing wires for wheels, circles for keys and lamps, cabinets), even when the reader cannot name them or calls them boxes. It fails only if the reader saw plain empty boxes with nothing of the part drawn in them, joined by arrows or lines, or text-like blocks.
2. what changes: the description names a drawn part that moves or changes, or a drawn result that changes from one press or step to the next (a different light, a path that takes a different route), consistent with the intent. It fails if it names nothing that changes, or only a change the intent does not name.` : `This description comes from the figure with every word, letter and number removed: only shapes (and, for an animated figure, their motion) were left. Score whether the picture still shows what moves and what causes what, as the intent says. Words and numbers are not expected. PASS only if both tests pass; otherwise FAIL.
1. what moves: the description names the thing that moves or changes and how, consistent with the intent.
2. what causes what: the description says which thing acts and what happens because of it, consistent with the intent's cause, and "cause_drawn" names a drawn shape that shows that cause (it lights up, matches, points or acts when the change happens). It fails if "cause_drawn" is "none" or empty, if the description can say only that things move, appear or light up without what causes what, if the cause given is only the reader's guess or comes only from the book's text, or if it gives a different mechanism.`,
};
export const SCORER = ({ kind, job, intent, description }) => `You score one blind reader's description of a figure in a book about how computers work. The reader saw the figure (and the book's text before it) but never saw the figure's intended message, which only you see.

${JOBS[job]}

THE INTENT (what the figure must get across):
"${intent}"

THE READER'S DESCRIPTION (JSON):
${JSON.stringify(description, null, 1)}

${RUBRIC[kind](job)}

Answer with one JSON object, nothing else:
{"tests": {"<test name>": {"pass": true, "why": "one sentence"}}, "verdict": "PASS or FAIL"}`;

// (c) the hedge check, on each description (12 frames, still, text-stripped), each in its own scope. It guards the
// events the reader saw: what changes, what makes it change, whether it stops, where it ends up. What the end state
// means (that marks stand for a number, that a line states the sum) is scored by the scorer's mechanism test.
const HEDGE_SCOPE = {
  judge: { fields: ['changes', 'cause', 'cause_drawn', 'result', 'teaches', 'unsure'] },
  still: { fields: ['changes', 'cause', 'cause_drawn', 'result', 'teaches', 'unsure'] },
  stripped: { fields: ['moves', 'cause', 'cause_drawn', 'result', 'unsure'] },
};
// The text-stripped reader lost every word that named an action or a result, so its check is narrow and positive: it
// counts only a doubt about which thing moves, or a doubt that anything drawn causes the change (the stripped scorer
// tests the drawn cause itself).
const HEDGE_STRIPPED = (d, job = 'function') => job === 'real thing' ? `Below is part of a blind reader's description of a figure from which every word, letter and number was removed. The figure draws a real object, and it is judged on showing that object as it looks, not on how or why it works. Decide whether the reader hedges on whether anything in it changes.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only when it says that nothing in the picture moves or changes, or that the reader cannot tell what the drawing shows at all.
Every other candidate does NOT count: doubts about which of the drawn things moves, or whether a change the reader sees is real or meant; why things move or change, what causes it, what the shapes or their parts stand for or are called (the words that named them were removed), what the object is for; timing (a pause, a frame where nothing is lit, a frame caught between two positions, the order inside a step); the result (where it ends up, whether it stops or holds still); the loop starting again; colours and layout.

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "nothing changes | cannot tell what is drawn | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "nothing changes | cannot tell what is drawn"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)` : `Below is part of a blind reader's description of a figure from which every word, letter and number was removed. Decide whether the reader hedges on what moves, or on whether any drawn thing causes it.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these two cases:
- it leaves open WHICH thing moves or changes (the reader cannot tell what moved, or offers two different things);
- it says that nothing drawn shows why things move or change: the reader names no drawn thing as the cause at all. "cause_drawn" being "none" or empty also counts.
Every other candidate does NOT count: doubts about which action a drawn rule stands for, whether a particular step comes from the drawn cause the reader named, or whether that drawn thing causes the change or only goes with it (the words that named the actions were removed, and another test scores the drawn cause); timing (a pause, a frame where nothing is lit, a frame caught between two positions, the order inside a step); the result (where it ends up, whether it stops or holds still, whether a mark is new); the loop starting again; colours and layout.

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "which thing moves | no drawn cause | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "which thing moves | no drawn cause"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
// the still of a real thing (author decision D1): judged only on showing the object as it looks, its parts identifiable
const HEDGE_REAL_STILL = d => `Below is part of a blind reader's description of a figure seen as one still picture. The figure draws a real object (a machine, a device, a place), and its still is judged only on showing that object as it looks, its parts identifiable; what changes in the object is carried by the animation and tested elsewhere. Decide whether the reader hedges on what the drawing shows.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only when it leaves open what the drawing shows: the reader cannot tell what object is drawn, or what kind of parts it has (offers two different objects, or cannot say what the parts are).
Every other candidate does NOT count, however it is worded: whether anything changes, what changes, whether the still shows a change, which part moves, what the result is or whether it changes; why or how a part moves or gives its result; what a letter, mark or note on a part stands for; why the object is built or wired as it is, or what it is for; which moment the still shows; colours, layout and how the drawing is meant. (Another test scores whether the reader saw the object.)

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what is drawn | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what is drawn"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
// the function (and two-part) checks on the judge's and the still's descriptions (from revision 1 of the follow-up,
// try26: narrow positive checks, as the text-stripped check, instead of "counts unless an exclusion applies")
const HEDGE_FUNCTION = (kind, d) => kind === 'still' ? `Below is part of a blind reader's description of a figure seen as one still picture, which cannot move. Decide whether the reader hedges on what makes the change happen: which drawn thing is the cause, or whether the cause is drawn at all.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "I infer", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these cases:
- it says, or leaves open, that nothing drawn shows why the change happens: the reader names no drawn thing as the cause, or says the rules or the cause are not drawn, or are only written in words. "cause_drawn" being "none", empty or only words also counts;
- it offers two different drawn things as the cause, or cannot tell which drawn thing is the cause.
Every other candidate does NOT count, however it is worded: what happens over time; what a rule's action produces (for example what "write" writes); how the drawn rules are chosen step by step; whether the end state is reached; whether the still shows the start, the end or only the rules; whether the drawn cause the reader names truly causes the change, or only shows which rule applies or goes with it; what the end state, a mark, a number or a line means; whether there is more than is drawn; colours, decoration and layout. (The reader saw one still picture, and other tests score whether the reader worked out the change and the result.)

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "no drawn cause | which cause | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "no drawn cause | which cause"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)` : `Below is part of a blind reader's description of a figure shown as frames of its animation. Decide whether the reader hedges on what changes, what makes it change, or where it ends up.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "I infer", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these cases:
- what changes: it leaves open WHICH thing changes or moves, or whether anything changes (the reader cannot tell, or offers two different things);
- what makes it change: the reader names no drawn thing as the cause, says the rules or the cause are not drawn, or are only written in words, or offers two different drawn things as the cause. "cause_drawn" being "none", empty or only words also counts;
- where it ends up: the reader cannot say what the end state is, offers two different end states, or doubts that it stops while nothing drawn shows a stop (holding still while a rule card or light stays lit is a drawn stop);
- a field about these ("changes", "cause", "cause_drawn", "result") is missing, empty or vague.
Every other candidate does NOT count, however it is worded:
- a doubt that names the drawn thing that shows the point and asks only whether it is really meant that way, or whether it truly causes the change or only shows which rule applies or goes with it (for example "the head stays put with the stop card lit, but does the machine truly stop?");
- what the end state, a mark, a number or a line means (whether marks stand for a number, whether a written sum states the task or the answer, which mark is the "+ 1"): another test scores the meaning;
- how a drawn rule or card depicts its condition or its action (what it shows or leaves out), while the change itself is stated;
- whether there is more to the thing than is drawn (another part, a hidden state);
- timing: a pause, a frame where nothing is lit, a frame caught between two positions, the order of events inside one step; the loop starting again;
- colours, decoration and layout.

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what changes | why | end state | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what changes | why | end state"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
// a real thing is judged on showing the object as it looks, not on how or why it works (brief section 4)
const HEDGE_REAL_THING = (kind, d) => `Below is part of a blind reader's description of a figure${kind === 'still' ? ' seen as one still picture' : ''}. The figure draws a real object (a machine, a device, a place), and it is judged on showing that object as it looks and what visibly happens in it, not on explaining how or why it works. Decide whether the reader hedges on what the drawing shows, on whether anything in the object changes, or on the result it shows.

A candidate is each entry in "unsure", each hedging word ("seems", "appears", "probably", "perhaps", "might", "may", "likely", "I think", "I assume", "unclear", "not sure", "could be"), each pair of alternatives and each question, in any field. A candidate COUNTS only in these three cases:
- it leaves open what the drawing shows: the reader cannot tell what object, or which kind of parts, is drawn;
- it leaves open whether anything in the object changes at all${kind === 'still' ? ' (or, for this still, whether the picture shows a change: drawn states, a row of results, a note on a part)' : ''};
- it leaves open whether the result the reader names changes (for example whether a different lamp lights for the same key), or offers two different results.
Every other candidate does NOT count, however it is worded: which of several parts moves, how far, or why the others stay still; why or how a part moves or gives the result it gives, including whether the drawn part is really what makes the result change; what a letter, mark or note on a part stands for; why the object is built or wired as it is, or what it is for; the order or timing of the results shown, a pause, a frame caught between two positions, the loop starting again; colours, layout and how the drawing is meant. (Another test scores whether the reader saw what the figure is meant to show.)

THE DESCRIPTION (JSON):
${JSON.stringify(d, null, 1)}

Answer with one JSON object, nothing else:
{"candidates": [{"quote": "the hedged words", "about": "what is drawn | whether it changes | the result | other", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what is drawn | whether it changes | the result"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;
export const HEDGE = (kind, description, job = 'function') => {
  const S = HEDGE_SCOPE[kind];
  const d = Object.fromEntries(S.fields.filter(k => description[k] !== undefined).map(k => [k, description[k]]));
  if (kind === 'stripped') return HEDGE_STRIPPED(d, job);
  if (job === 'real thing') return kind === 'still' ? HEDGE_REAL_STILL(d) : HEDGE_REAL_THING(kind, d);
  return HEDGE_FUNCTION(kind, d);
};

// (f) the pairwise comparison: two versions for the same place, order given by the caller
const seen = n => n > 1 ? `${n} frames captured at equal steps through one loop of its animation (frame 1 is the start)` : 'one still picture (it does not animate)';
export const PAIRWISE = (packet, nA = 12, nB = 12) => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. Two different versions of that figure were made for this place, A and B. Version A is shown as ${seen(nA)}; version B as ${seen(nB)}. Neither has a caption.

Which version would a newcomer who has read only this text understand faster and more surely? Judge by the book's rules for figures: the picture carries the idea (it shows the mechanism, it does not hold a column of text); as few words as the idea allows; motion where motion is the mechanism; nothing a newcomer cannot yet read; everything shown once. Answer "SAME" if the differences would not change how quickly or surely a newcomer gets the idea.

${BOOK(packet)}

Version A comes first, then version B. Then answer with one JSON object, nothing else:
{"better": "A or B or SAME", "why": "two sentences at most, naming the concrete difference"}`;

// the prompts as frozen: each rendered with placeholder inputs, for the hashes in docs/pass-31-calibration.md
export function frozenTexts() {
  const pk = '{{PACKET}}', desc = { '{{DESCRIPTION}}': '' };
  const jobs = Object.keys(JOBS);
  return {
    system: SYSTEM,
    judge: JUDGE(pk),
    scorer: ['judge', 'still', 'stripped'].flatMap(kind => jobs.map(job => SCORER({ kind, job, intent: '{{INTENT}}', description: desc }))).join('\n\u0000\n'),
    hedge: ['judge', 'still', 'stripped'].flatMap(k => jobs.map(job => HEDGE(k, Object.fromEntries(HEDGE_SCOPE[k].fields.map(f => [f, `{{${f}}}`])), job))).join('\n\u0000\n'),
    still: STILL(pk),
    stripped: [STRIPPED(pk, 12), STRIPPED(pk, 1)].join('\n\u0000\n'),
    pairwise: [PAIRWISE(pk, 12, 12), PAIRWISE(pk, 12, 1), PAIRWISE(pk, 1, 12), PAIRWISE(pk, 1, 1)].join('\n\u0000\n'),
  };
}
