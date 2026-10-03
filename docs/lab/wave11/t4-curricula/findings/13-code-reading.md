# Slice 13 — code curriculum: READING code (Track 4: teaching curricula)

## 1. Slice
TNN must READ the existing native codebase (five organs, Zag substrate) and genuinely
understand it — comprehension stages, a memory representation of understood code, a mastery
bar on invariant questions about unseen functions, and the self-application milestone: TNN
reads its own memory-substrate source and correctly describes what kill/pin do. Prerequisite
to RC2/RC3 self-change work (RC1: 40/40, `docs/lab/waveN/` per brief).

## 2. Falsifiable claim
A TNN trained through a five-stage comprehension curriculum (syntax -> control flow ->
data flow -> invariants -> design intent) with understood functions stored as deliberate
structured memories will answer invariant questions about previously unseen native
functions at >=80% correct (n=100 per trial, binary-scored questions), with byte-identical
reruns given the same full internal state (per Micah's variation rule); a control arm
trained only to emit function-level summaries will not exceed 55% on the same questions.

## 3. Design
`CodeRep` stored as a deliberate memory record per understood function:
```
struct CodeRep {
  name, src_hash: i32;            // identity of the source read
  sig: (ret, param types);        // stage 1 syntax: exact signature
  cfg: [BB];                      // stage 2 control flow: basic-block graph, branch targets
  defuse: (def_slot -> use_slots); // stage 3 data flow: where each value is born/killed
  guards: [invariant];            // stage 4 invariants: preconditions + refusal codes,
                                 //   e.g. (kill: "stage>=KILL", "live[slot]==1",
                                 //   "region!=CORE", "pinned!=1" else REFUSED_PINNED)
  intent: cite_episode;           // stage 5 design intent: WHY (episode citation, audit ref)
}
```
Curriculum: stages are gates, not labels. A function advances a stage only when TNN
produces, unprompted, the correct stage artifact (signature parse, branch trace on a
concrete input, def-use chain for one register, all refusal conditions of one op, and a
why-answer that survives an adversarial why-question). The audit ledger records each
advance (append-only, replayable — same discipline as MA1 58/58). Mastery test: unseen
functions from a held-out substrate file; questions are machine-generated from the actual
invariants (e.g. "what does ma_kill return if slot is pinned?" — answer MA_REFUSED_PINNED
before live becomes 0). All deterministic: expression of answers may vary, verdicts may not.

## 4. Kill bar
Run 200 questions on 100 unseen functions (2 per function). Falsify if EITHER: (a) the
full-curriculum arm scores <80% overall; or (b) the summary-only control scores >=55%,
shrinking the claimed gap to <25 points. Both legs run byte-identical reruns (same full
state -> identical scores). Firing either bar kills the claim that the five-stage
curriculum is what produces comprehension; it does not kill the milestone result itself
if that independently passes.

## 5. Honesty notes
Weakest link: stage-5 "design intent" grading is adversarial-question-based, and graders can
be gamed by plausible confabulation — this is where the design could silently become a
storytelling test rather than a comprehension test. Confabulation of intent is the failure
mode with the least automatic detection. NOT claimed: that understanding generalizes to
natural-language specs or to buggy code (trial uses committed, working native code only);
not claimed that TNN can *write* better code from comprehension (that's slice scope beyond
13); not claimed that self-application implies self-modification safety — reading one's own
substrate is prerequisite to, not sufficient for, RC-grade self-change. Truthful-but-sensor-
deceivable applies here too: comprehension is of the source as read; a spoofed source file
would be comprehended faithfully and wrongly.

## 6. Next build step
Build the smallest leg first: take the real `ma_kill`/`ma_pin`/`ma_unpin`/`ma_promote`
functions from the committed MA1 substrate (`wave2/memoryagency/trial/memory_core.zag`),
machine-generate 40 invariant questions (preconditions, refusal codes, post-state on
success, post-state on each refusal), and run a comprehension probe WITHOUT the curriculum:
can TNN already answer them from the source text alone? This baseline decides whether a
curriculum is even needed or comprehension is already present and only needs formalizing.
