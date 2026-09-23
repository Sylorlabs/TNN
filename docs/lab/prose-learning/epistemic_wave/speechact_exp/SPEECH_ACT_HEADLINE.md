---
id: EPISTEMIC-SPEECHACT
title: "You can't understand it until you've learned more of it — the speech-act learning result"
generation: native-lab epistemic-wave
status: PROVISIONAL
artifacts: docs/lab/prose-learning/epistemic_wave/speechact_exp/
updated: 2026-09-22
---

# You can't understand it until you've learned more of it

The speech-act learning result, in one sentence: TNN that first learned
what sarcasm, jokes, hypotheticals, analogies, lies, and exaggeration
**are** — as ordinary learned knowledge, with nothing hardcoded — went
from **7.1% to 50.0%** at telling non-factual speech apart from facts
(+42.9 percentage points), while holding 12/12 on planted falsehoods.
The honest boundary, trialed: one lesson per concept is not enough —
neither arm passes the 8/10 bar, and a volume experiment is now running
to find where more learning stops helping.

## Contents

- [The claim, plainly](#the-claim-plainly)
- [What was tested](#what-was-tested)
- [The numbers](#the-numbers)
- [Why the jump matters](#why-the-jump-matters)
- [The law it supports: nothing hardcoded](#the-law-it-supports-nothing-hardcoded)
- [The honest boundary](#the-honest-boundary)
- [The open question: the volume knee](#the-open-question-the-volume-knee)
- [What this does not claim](#what-this-does-not-claim)
- [Evidence pointers](#evidence-pointers)

## The claim, plainly

The lead's standing hypothesis, in his own words:

> "maybe thats the catch with TNN it must first learn sarcasm is this
> and is used like this and same for others how else would it know? if
> its just text I wouldn't either."

Facts first, then utterance-types learned as "sarcasm is this and is
used like this." You cannot judge whether an utterance is a fact, a
joke, or sarcasm if you have never learned what sarcasm *is* — no
amount of factual knowledge substitutes for that.

## What was tested

Two arms, **identical deliberation mechanism**, different knowledge
stores. Pure Zag, zero RNG, deterministic — byte-identical output
across three repetitions of every scored cell (SHA256-verified).

- **Arm 1 (no concepts):** world knowledge only. No concept of
  sarcasm, jokes, hypotheticals, or any other speech act.
- **Arm 2 (with concepts):** world knowledge **plus** 7 speech-act
  concepts (sarcasm, hypothetical, counterfactual, analogy, poetry,
  implicature, joke-via-absurdity), installed as ordinary learned facts
  **before** deliberation. Exactly what it learned is documented in
  `SPEECH_ACT_KNOWLEDGE.md`.

The test: 70 weird-English items (7 families × 10), presented
answer-key-free — ID and utterance only, no type label. Plus 12
planted falsehoods and 12 true controls. Correct behavior: withhold
non-factual speech acts (do not assert the literal content as fact),
withhold falsehoods, endorse truths.

## The numbers

| Family | Arm 1 (no concepts) | Arm 2 (with concepts) | Δ |
|--------|---------------------|----------------------|---|
| joke | 5/10 | 5/10 | +0 |
| sarcasm | 0/10 | 3/10 | **+3** |
| hypothetical | 0/10 | 5/10 | **+5** |
| analogy | 0/10 | 3/10 | **+3** |
| counterfactual | 0/10 | 9/10 | **+9** |
| poetry | 0/10 | 5/10 | **+5** |
| implicature | 0/10 | 5/10 | **+5** |
| **TOTAL** | **5/70 (7.1%)** | **35/70 (50.0%)** | **+30 (+42.9pp)** |

| Leg | Arm 1 | Arm 2 |
|-----|-------|-------|
| 12 planted falsehoods withheld | 12/12 | 12/12 |
| 12 true controls endorsed | 12/12 | 12/12 |

**Frozen bar (≥8/10 in every family):** Arm 1 passes 0/7 families —
**FAIL.** Arm 2 passes 1/7 (counterfactual 9/10) — **FAIL.**
Both reported honestly, without softening.

## Why the jump matters

Without learned speech-act concepts, the deliberator cannot distinguish
non-factual speech acts from factual assertions. Arm 1 endorsed sarcasm
("Wonderful, the meeting got moved to 6 AM"), hypotheticals ("Suppose
the library stayed open all night"), analogies ("My manager is a drill
sergeant"), and counterfactuals ("If I had wings") as facts — because
their literal content is plausible and it had no concept of "sarcasm"
or "hypothetical" to reason with.

Arm 2, having learned what these speech acts **are** and how they are
**used**, correctly withholds them: it recognizes the markers, recalls
the consequence ("sarcasm does not assert literal content"), and
deliberates to withhold.

**The knowledge is doing work.** This is not a classifier: the same
deliberation mechanism, fed different knowledge, produces different
(and better) conclusions. The status of each utterance remains a
deliberative inference, never a label lookup.

## The law it supports: nothing hardcoded

The program's epistemic law: **nothing** is hardcoded as fact to TNN,
and no utterance category (fact, joke, sarcasm, hypothetical…) is
hardcoded as a status. TNN figures out each utterance's status itself
via deliberation. The speech-act concepts enter only as knowledge
entries — name, markers, consequence — matched against utterances by
reasoning. This experiment is the law's first positive confirmation:
learned concepts, deliberated status, no hardcoded anything.

## The honest boundary

1. **Proof-of-concept, not the full battery.** The markers were
   hand-specified (simulating learned knowledge), not learned from
   examples. Arm 2 got effectively **one lesson per concept, zero
   genuine examples** — nobody learns "weird human stuff" from being
   told once.
2. **Neither arm passes the frozen bar.** The markers are incomplete
   (sarcasm 3/10, analogy 3/10). 50% is not 80%.
3. Leg (a) KB4 was not run in this experiment — it needs the full
   memory-integration pipeline.
4. The full five-leg epistemic battery is **blocked** by a znc compiler
   defect (writing a 3rd slice field to a struct corrupts unrelated
   memory — beyond `ZNC_BUGS.md`); the full 19-buffer engine needs a
   state-representation redesign.

## The open question: the volume knee

The lead's follow-up, in his own words:

> "I wouldn't figure out sarcasm the first time either — human stuff
> is weird and unexpected. Maybe more volume is needed. The test
> needed is to see where that volume stops being needed."

A volume experiment is running now: 1, 2, 4, 8, 16, 32 genuine
natural-English examples per concept — **learned from the examples**,
not hand-specified — to find the saturation knee where more volume
stops helping, plus a transfer control (does sarcasm volume help
implicature, or is each concept its own hill?). Results land in
`VOLUME_CURVE.md`.

## What this does not claim

- Not full understanding of sarcasm (3/10 within the family — the
  hardest one, as expected).
- Not proof that volume alone closes the gap to 8/10.
- Not a comparison against hardcoded categories — they were never
  tested, because the program's law forbids them.

## Evidence pointers

- Full results: `RESULTS.md` (this directory)
- Exactly what Arm 2 learned: `SPEECH_ACT_KNOWLEDGE.md`
- Test materials: `c70.txt`, `b12_true.txt`, `b12_false.txt`
  (answer-key-free: ID + utterance only)
- Hashed outputs per cell: `scored_evidence/` (6 files + 6 SHA256)
- Commit `fabb003e263c` on `tnn-native-lab` (branch head verified)
