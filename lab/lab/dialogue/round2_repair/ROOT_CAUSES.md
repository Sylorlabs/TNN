# Round-2 dialogue failures — root-cause report (Phase 1)

Date: 2026-09-23. Investigator: TNN dialogue crew (parent task).
Source: `~/workspace/tnn-lab/dialogue/REAL_CONVERSATION_2026-09-23.md` (18 turns, 5/18 good).
Mechanism: `dialogue/dialogue.zag` (1917 lines, pure Zag), read in full; every trace below
was verified by running `dialogue_bin` on probe batteries (byte-identical reruns).

## How the machine works (one paragraph)

Each user turn goes through `do_turn`, which tries, in order: (1) correction handling
("no,", "i meant", "the other one"), (2) topic resume ("back to X"), (3) composition
templates (`do_compose`: four hard-coded string-prefix branches — "was the author of…before…"
→ yes/no, "which is taller" → "X is taller.", "did…write" → yes/no, "birth year" → emit fact),
(4) user-assertion/contradiction (only when the input has no "?"), and (5) the default:
gazetteer entity scan + pronoun resolution → Jaccard similarity between the query's key set
and each KB fact's key set → `retrieve()` picks the best fact (ties → lowest fid) →
`emit_fact()` prints the fact text verbatim. **There is exactly one response strategy:
retrieve the best-matching fact and emit it.** Every failure below is an input that needs
a different strategy.

## F1 — Comparison-as-answer (turns 3, 4, 7): the machinery exists but is padlocked

The comparison machinery EXISTS in `do_compose` — but each capability is gated behind an
exact string prefix. Turn 5 ("which is taller…") worked because it literally starts with
"which is taller". Turn 3 ("was he born before the eiffel tower was built?") does not start
with "was the author of", so it falls through to step-5 Jaccard, which retrieves one date
fact and emits it — the machinery to compare the two dates never fires. Turns 4 ("who was
born first, darwin or melville?") and 7 ("which of those two was built first?") have no
template at all: both candidate facts tie on Jaccard (2/6 each for turn 4), the lower fid
wins, and one date is emitted with no comparison. "Those two" is additionally never
resolved to the two towers (pronoun binder only handles he/him/his/she/her/it/its/they/them).

**Root cause:** comparison is implemented as a handful of frozen string-prefix templates,
not as a general capability. Anything outside the exact phrasings collapses to single-fact
retrieval, which cannot express a comparison.

## F2 — Withholding (turns 8, 9, 13, 17): there is no "I don't know" — verified absent

`retrieve()` always returns a fact: with 38 facts installed and no exclusions, the
first-fact-wins initialization means the best score starts at fact 0 and only a strictly
better Jaccard score displaces it. `emit_fact()` always emits the fact text. The string
"UNCERTAIN." exists in `emit_fact` but is unreachable — it only fires when the fid matches
no fact, which `retrieve()` can never return. Verified by probe: two zero-overlap questions
("which author lived the longest?", "who is the current president…") both emit fact 0,
"Herman Melville wrote the novel Moby Dick."

The transcript's template-fill diagnosis is CONFIRMED mechanistically. Turn 9 ("who wrote
hamlet?"): query keys are {wrote, hamlet}. Facts containing "wrote" score 1/(union); fact 15
("Andy Weir wrote The Martian.", 4 keys) scores 1/5 and beats fact 4 ("Jane Austen wrote
the novel Pride and Prejudice.", 6 keys) at 1/7. **The tie-break systematically favors the
SHORTEST fact** — the one with the fewest extra words — so a relation-word match
("wrote", "capital") plus shortest-fact tie-break emits a confidently-shaped falsehood
with zero check that the requested entity ("hamlet", "italy") appears in the emitted fact.
Unmatched query terms are not penalized anywhere. Turn 8 ("capital of italy"): facts 33/34
tie 1/4 → lower fid → "Paris is the capital of France."

**Root cause:** relation-word matching with no entity-presence check, no score floor, and
no decline path. The confabulation is not a bug in the matcher — it is the matcher working
as designed on a question type it was never given a way to refuse.

## F3 — Arithmetic follow-up (turn 6): no subtraction exists, plus a morphology gap

No subtraction (or any arithmetic) exists anywhere in the 1917 lines — only `<`/`>` value
comparisons inside `do_compose`. "How much taller is it?" matches no compose branch and
falls to Jaccard. Worse, "taller" does not stem to "tall" (there is no "-er" rule, and the
morphology crew explicitly left tall/taller unbridged as a documented boundary), so the
height facts ("is 330 meters tall") don't even match well: "The Eiffel Tower is in Paris."
(2/4) outscores "The Eiffel Tower is 330 meters tall." (2/5). The answer needs 330−210=120
carried from turn 5's comparison; the machine has no arithmetic, no cross-turn value
passing, and a morphology gap on the exact word in the question.

**Root cause:** missing arithmetic machinery + tall/taller morphology gap + Jaccard fallback
emitting a related fact instead of declining.

## F4 — Challenge defense (turn 11): noisy keys + no defense path; "resistance" is accidental

Two stacked causes. First, the stopword list is missing "a", "i", "you" — they become
content keys. Verified by probe: "are you sure? i read 1818 in a biography." emits fact 25
("The Louvre opened as a museum in 1793.") because the bare article **"a"** in "a biography"
matches the **"a"** in "as a museum" (intersection of 1 on pure noise). Second, there is no
challenge/defense machinery: "are you sure?" matches no correction pattern, isn't an
assertion (it contains "?"), matches no compose branch — so it falls to retrieval. Turn 10's
"resistance" is equally accidental: the digit 1818 is extracted into the value field and
then never read — step 5 ignores it entirely. The machine retrieved the true fact; it never
engaged with the false premise at all.

**Root cause:** function words ("a", "i", "you") polluting the key sets + no notion of
defending a fact under challenge. What looked like conviction was retrieval luck.

## F5 — Joke (14), history (15), provenance (16), forget-instruction (18): one strategy for all inputs

Shared root, verified in code:

- **Joke (14):** no utterance-type routing exists. "Tell me a joke about darwin." is tokenized
  like any question; Jaccard finds the Darwin birth fact. There is no joke machinery and no
  decline machinery, so a related fact is emitted instead.
- **History (15):** the history store (`hist`/`histb`) is **write-only**. Every user turn and
  every response is recorded (for the novelty check), but nothing ever reads it for recall.
  "Do you remember the first thing I asked?" falls to Jaccard → zero overlap → fact 0.
  (The first question IS in the store — the machinery to read it back was never built.)
- **Provenance (16):** the fact rows have no source field
  (fid/key_off/key_len/value/text_off/text_len/ent_off/ent_n). "How do you know…?" retrieves
  the fact about Weir and restates it — restating is structurally the only option.
- **Forget (18):** no instruction/command recognition. `extract_assert` handles 7 declarative
  templates ("X wrote Y", "was born in…", etc.); "forget everything I just told you."
  matches none, so it falls through to step-5 retrieval → fact 0.

**Root cause:** a single retrieve-and-emit pipeline with no input-type dispatch. Jokes,
commands, meta-questions, and factual questions all take the same path; the path can only
emit a KB fact.

## What is NOT broken

Turns 1, 2 (retrieval + pronoun binding), 5 ("which is taller" template), 10 (accidental
true-fact retrieval), and 12 ("did X write Y" → wrote_rel → "no.", a genuine composition)
work as designed. The binary, KB, and gazetteer are byte-identical to round 1 — the
failures are in the system's design, not the probes.

## The load-bearing gap (for the repair crews)

The machine has no way to say "I don't know", no way to check that its answer is ABOUT the
thing asked, no comparison outside four frozen phrasings, no arithmetic, no utterance-type
dispatch, and a write-only history. The F2 confabulation (answer-shaped falsehoods) is the
most dangerous: it is the matcher working as designed, so it will keep happening on every
new relation until an entity-presence check and a decline path exist.
