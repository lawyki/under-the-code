// Pass 31 gate prompts (tests/pass31/gate.mjs). The full text is reproduced in docs/pass-31-calibration.md, with its
// hash. The author never reads this file (brief section 6: the author learns only pass or fail and the criterion name).
// Every tester is a fresh Sonnet 5.5 session with no tools: it sees only what its message holds.

export const SYSTEM = `You help test the figures of a book about how computers work. You only look and report what you see and understand. You never suggest changes, never advise, never vote on anything but the question asked. Answer with exactly one JSON object and nothing else.`;

const BOOK = packet => `THE BOOK SO FAR (everything you have read before the figure; figures that came earlier are left out):
<<<
${packet}
>>>`;

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
 "result": "where it ends up: the result the figure arrives at",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "text_pieces": 0,
 "read_only": "any part of the idea you could get only by reading words, a table or a list in the picture, because the picture never shows it happening or drawn; \\"none\\" if none",
 "repeated": "anything the figure shows twice in different forms, for example a scene and also a step-by-step replay of the same steps, or the same rules written out again as a table. A label naming a drawn thing, or a short result line saying what the scene arrives at, is not a repeat; \\"none\\" if none",
 "unexplained": ["each word, label, symbol, number or mark in the picture whose meaning here you had to guess: neither the picture nor the text you read says what it means or what it refers to. Leave out anything the picture or the text makes plain; leave the list empty if there is none"],
 "unsure": ["each doubt you still have, after looking at every frame, about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (the exact timing of the animation, the loop starting again, layout, colours, where something rests at the end). Leave the list empty if you have none"]
}
("text_pieces" is the number of separate pieces of text you read in the picture.)`;

// (d) the t=0-only judge: the reduced-motion still
export const STILL = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure as a reader who has turned animation off sees it: one still picture that does not move. The figure has no caption and no explanation: you have only this picture and the text you have read.

Describe what the figure shows and teaches, from the still and the text before it only. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The still follows. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn, in plain words",
 "panels": ["one entry per separate picture inside the figure (a key, rule card, label or result line belongs to its scene)"],
 "changes": "what the still shows changing, happening or having happened: the process it depicts",
 "cause": "what makes it happen, as the picture shows it",
 "result": "the result the figure shows or states",
 "teaches": "the idea the figure teaches, in one or two sentences",
 "unexplained": ["each word, label, symbol, number or mark in the picture whose meaning here you had to guess: neither the picture nor the text you read says what it means or what it refers to. Leave out anything the picture or the text makes plain; leave the list empty if there is none"],
 "unsure": ["each doubt you still have about the figure's main idea: what changes, what makes it change, or what the result is. Leave out doubts you resolved, and doubts about side details (layout, colours, where something rests). Leave the list empty if you have none"]
}`;

// (e) the text-stripped judge: the same 12 frames with every <text> removed
export const STRIPPED = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. After it you see the figure as 12 frames captured at equal steps through one loop of its animation (frame 1 is the start; after frame 12 it starts again). Every word, letter and number has been removed from the picture: only shapes, marks, colours and their motion are left. There is no caption.

Say what the picture shows by its shapes and motion alone, using the text you have read only to name things. Do not fill gaps with knowledge from outside the book. State what you see as fact. If you are not sure about something, put it in "unsure", and only there.

${BOOK(packet)}

The 12 frames follow. Then answer with one JSON object, nothing else:
{
 "scene": "what is drawn: the shapes and what they seem to stand for",
 "moves": "what moves or changes, frame by frame",
 "cause": "what causes what: which thing acts, and what happens to which other thing as a result",
 "result": "where it ends up",
 "unsure": ["each doubt you still have about what moves, what causes what, or the result after looking at every frame. Leave out doubts you resolved; leave the list empty if you have none"]
}`;

// (b) the scorer: the judge's description against the intent sentence, for the figure's job
const JOBS = {
  'function': `The figure's job is "function": it shows how something works. The bar for this job (the book owner's approved reference) is one calm scene, the core function, few labels, motion that is the mechanism, and the result stated.`,
  'real thing': `The figure's job is "real thing": it shows a real object or machine as it really is, so the reader sees the real thing and what happens inside it. For this job the description must recognise the object the intent names and see in it what the intent says happens.`,
  'two-part': `The figure's job is "two-part": one panel shows the real thing and the other shows its function, in one figure. Two panels are expected; each must do its job.`,
};
const RUBRIC = {
  judge: job => `Score the description against the intent. PASS only if every test below passes; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: the same thing changes, for the same cause, with the same result. Paraphrase is fine and extra correct detail is fine. It fails if what changes, why, or the result is missing, vague or wrong, or if the description gives a different mechanism, a different representation or a different example than the intent names.
2. unexplained: nothing listed in "unexplained" shows that the reader could not get what changes, why, or the result. An item the description itself resolves elsewhere (in "changes", "cause" or "result"), or one about decoration or a side detail, does not count.
${job === 'real thing' ? `3. object: the description recognises the real object or scene the intent names, drawn as itself (not as boxes and labels standing for it).` : `3. carried by the picture: the mechanism is shown happening or drawn, not only written. It fails if "read_only" names a part of the mechanism (what changes, why, or the result) that the picture never shows. A short result line that states what the drawn change amounts to (for example a sum) is part of this bar ("the result stated") and does not fail the test, as long as the change it sums up is shown happening.
5. few words: the picture uses few words. It fails if "text_pieces" is more than 8 for one panel, or if the words, not the picture, carry the mechanism.
4. one scene, shown once: ${job === 'two-part' ? 'at most two panels, and' : 'one panel only (the scene, with its own rule cards, keys and result line), and'} "repeated" is "none". It fails if the figure adds a separate table, list of steps, replay or block of text beside the scene, or shows the same steps twice. A short result line that states what the scene arrives at is not a repeat, even when "repeated" names it.`}`,
  still: () => `This description comes from the still alone, the frame a reader with animation turned off sees. A still cannot move, so the change may be shown by drawn states, arrows, a before and after, drawn rules, or a stated result, and the reader may have to work the motion out. Score it against the intent: a reader who works out, from what is drawn, the same change, cause and result as the intent passes, even when the reader says the change is implied rather than seen. PASS only if both tests pass; otherwise FAIL.
1. mechanism: the description gives the intent's mechanism: what changes, why, and the result, as the intent says. Paraphrase is fine. It fails if any of the three is missing, vague or wrong, or a different mechanism is given.
2. unexplained: nothing listed in "unexplained" shows that the reader could not get what changes, why, or the result. An item the description itself resolves elsewhere, or one about a side detail, does not count.`,
  stripped: () => `This description comes from the 12 frames with every word, letter and number removed: only shapes and motion were left. Score whether the picture still shows what moves and what causes what, as the intent says. Words and numbers are not expected. PASS only if both tests pass; otherwise FAIL.
1. what moves: the description names the thing that moves or changes and how, consistent with the intent.
2. what causes what: the description says which thing acts and what happens because of it, consistent with the intent's cause. It fails if the description can say only that things move, appear or light up, without what causes what, or if it gives a different mechanism.`,
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

// (c) the hedge check: the judge's description, read for hedges on what changes, why, or the result
export const HEDGE = description => `Below is a blind reader's description of an animated figure. Decide whether the reader hedges on the figure's main idea: what changes, what makes it change, or the result.

Work in two steps.
Step 1. Write down what the description states as plain fact about each of the three: "changes", "cause" and "result". If one of them is missing, vague, or itself hedged, that is a hedge.
Step 2. List every candidate hedge: each entry in "unsure"; each word such as "seems", "appears", "apparently", "probably", "presumably", "possibly", "perhaps", "might", "may", "likely", "suggests", "I think", "I assume", "unclear", "not sure", "could be"; each pair of alternatives ("either ... or", "whether ... or"); each question. For each candidate decide whether it counts:
- It COUNTS when it leaves open which thing changes, what makes it change, or what the result is, or when it offers an alternative that contradicts what step 1 found.
- It does NOT count when step 1 already states that point plainly and the candidate does not contradict it: a doubt about how the figure shows something (shown or only implied, drawn or written), about what a number or a line in the picture stands for beyond the stated result, or about what else the figure might mean.
- It does NOT count when it is about a side detail: colours, decoration, layout, the exact timing of the animation, the loop starting again, where something rests at the end.

THE DESCRIPTION (JSON):
${JSON.stringify(description, null, 1)}

Answer with one JSON object, nothing else:
{"stated": {"changes": "...", "cause": "...", "result": "..."}, "candidates": [{"quote": "the hedged words", "about": "what changes | why | result | side detail", "counts": true, "why": "one sentence"}], "hedges": [{"quote": "each candidate that counts", "about": "what changes | why | result"}], "hedged": true}
("hedges" holds only the candidates that count; "hedged" is true when "hedges" is not empty.)`;

// (f) the pairwise comparison: two versions for the same place, order given by the caller
export const PAIRWISE = packet => `You are a newcomer reading a book about how computers work. Below is all of the book you have read so far, up to the point where a figure appears. Two different versions of that figure were made for this place, A and B. Each is shown as 12 frames captured at equal steps through one loop of its animation (frame 1 is the start). Neither has a caption.

Which version would a newcomer who has read only this text understand faster and more surely? Judge by the book's rules for figures: the picture carries the idea (it shows the mechanism, it does not hold a column of text); as few words as the idea allows; motion where motion is the mechanism; nothing a newcomer cannot yet read; everything shown once. Answer "SAME" if the differences would not change how quickly or surely a newcomer gets the idea.

${BOOK(packet)}

Version A's 12 frames come first, then version B's 12 frames. Then answer with one JSON object, nothing else:
{"better": "A or B or SAME", "why": "two sentences at most, naming the concrete difference"}`;
