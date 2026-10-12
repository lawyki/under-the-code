# Law 4 · Teach at the right depth (owner, 2026-10-12)

Binding on every paragraph and figure, and on the language pass embedded in Pass 29 (Parts I to V; Part I re-checked under it). Written down on the owner's instruction; **not yet run**: it runs only when the owner writes "continue", after its samples are approved.

> "It doesn't need to be childish or naive, it just needs to be good. … Just don't overfit around that opinion. That you never explain anything because you cannot explain: that isn't the solution either. It's something from the middle." (owner, 2026-10-12)

## The standard

Each passage gives the reader its idea **at the depth the book needs**, reached **from what the reader already knows**, with **nothing to carry that the next idea does not use**. The reader is a curious, intelligent adult who does not know the field and who reads every word.

## The two failures, both forbidden

- **Too deep (the expert's curse).** Steps only an expert needs; mechanism detail the next idea never uses; a term leaned on before it is given. Example: Pass 29's first version of ch1-context-p8 closed a gap by adding the Bombe's plugboard chain ("if A's partner is Q and the rotors there turn Q into X…"). The owner could not explain the paragraph.
- **Too shallow (the overcorrection).** Replacing a mechanism with a slogan, a vaguer word or silence because it is hard to explain; cutting the cause and keeping only the claim. Example of what must not happen: "The Bombe helped break Enigma." True, and teaches nothing.

The middle, as now in ch1-context-p8 (commit 6092c0c): the settings were too many to try; Turing designed a machine to find the day's setting; a guessed phrase and Enigma's one flaw let it throw out impossible rotor positions; a handful were left for people to check. The how is there, at the depth the chapter needs.

## Rules

1. **One job per passage.** Say it in one sentence first. Everything in the passage serves it; detail that serves another job goes to its own place (the How it works strip, a Go deeper link) or out.
2. **Depth stays where it carries the job.** Mechanism, cause and effect, real numbers and names stay. Never trade a mechanism for a vaguer word.
3. **Enter from the known: concrete, then general, then concrete again** (the ladder of abstraction). A familiar thing or a real example first, the general idea second, back to the example to check it. Petzold's *Code* builds every layer this way, from flashlights, Morse code and relays up to a processor.
4. **Every step a newcomer needs, once; no step only an expert needs.** Test each sentence: would the next sentence, paragraph or figure fail without it? If not, it goes.
5. **Close a gap by making the passage clearer, never by adding expert detail.** If the right explanation is long, it is long; if it is detail, it goes.
6. **Read it as the reader.** Not childish: no talking down, no forced analogy, no cheerleading, precision kept. One idea per sentence where it helps; a term is named before it is used, and jargon is kept only where the book uses it again.
7. **Figures follow the same law.** Fig 1.1 (commit 2a9ece9) is the reference: one calm scene, the core function, about five labels; history and detail in the caption and How it works.

## Procedure (when it runs)

Per section: (1) the editor writes each passage's job in one sentence and marks every sentence *serves the job / detail beyond the job / missing step*; (2) the edit; (3) **two blind readers**: a newcomer retells the passage and names what stopped them, an expert checks that nothing true was lost or blurred. Both must pass; one revision, then an owner call. **Samples first:** three edited paragraphs from different chapters go to the owner before the pass scales. Cost is bounded per section; no long agent chains.

## Grounding

The brief's research (Ausubel; McNamara et al.; Kalyuga et al. on the expertise reversal effect; Clark and Haviland; Sweller; Mayer and Harp and Mayer on coherence; Gentner), plus: Steven Pinker on the curse of knowledge (the expert cannot imagine not knowing), the ladder of abstraction (concrete to abstract and back), and reviews of Petzold's *Code* (built from familiar systems with analogy, diagram and example; faulted only where it lists detail no reader needs).
