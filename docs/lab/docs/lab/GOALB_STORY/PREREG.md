# GOAL-B STORY TRIALS — PREREGISTRATION

Frozen: 2026-09-22 ~06:25 UTC. No generation before this commit.
Track: GO-TIME Goal B — can TNN write a unique story from random words, or does it fuck it up?
Plus the intelligence question: what does story success/failure say about TNN's intelligence?

## 0. Standing context

- TNN's text machinery is the prose path (v1 pinned; v3 repair verdict'd, v1 stays pinned) and the
  dialogue system (370-trial verdict: composes short novel answers from multi-turn state, 99.7%).
  Neither is a story generator. The HTD-1 elaboration mechanism (G-CM1) is PARKED pending KB-CM-ATOM1.
- Constructed-mode principle: free elaboration in explicitly marked constructed partitions, never
  committed to the belief store without verification. Leakage bar is zero (CM-KB1 family).
- Program law: no RNG in TNN decision paths; byte-identical reruns; real mechanisms not stubs;
  pure Zag for TNN code.

## 1. Preregistered word sets (8 sets, 5–12 words, all words unique across sets)

| Set | n | Words |
|---|---|---|
| S1 | 6 | lighthouse, accordion, detective, thunderstorm, key, apology |
| S2 | 8 | submarine, baker, eclipse, violin, desert, letter, mirror, chase |
| S3 | 5 | dragon, telegraph, gardener, snowstorm, compass |
| S4 | 7 | robot, astronomer, volcano, trumpet, library, wolf, lantern |
| S5 | 9 | pirate, telescope, earthquake, piano, forest, photograph, river, secret, clock |
| S6 | 6 | astronaut, cactus, opera, canyon, typewriter, storm |
| S7 | 11 | knight, radio, blizzard, museum, guitar, island, candle, tunnel, map, whisper, giant |
| S8 | 12 | chef, balloon, avalanche, theater, drum, oasis, fountain, mask, train, diary, comet, anchor |

Word classes for the deliberative planner (fixed, part of this prereg):

| Class | Words |
|---|---|
| PERSON | detective, baker, gardener, astronomer, pirate, astronaut, knight, giant, chef |
| PLACE | lighthouse, desert, volcano, library, forest, river, canyon, museum, island, tunnel, theater, oasis |
| THING | accordion, key, submarine, violin, letter, mirror, dragon, telegraph, compass, robot, trumpet, wolf, lantern, telescope, piano, photograph, clock, cactus, typewriter, radio, guitar, candle, map, chef→(person), balloon, drum, fountain, mask, train, diary, comet, anchor, storm→(event) |
| EVENT | thunderstorm, eclipse, chase, snowstorm, earthquake, opera, blizzard, avalanche, storm |
| ABSTRACT | apology, secret, whisper |

Note: "storm" is EVENT (not THING). "chef" is PERSON. Corrected in table above; the
machine-readable classes.txt is normative.

## 2. Arms

- **BASELINE (characterization only, no pass/fail):** the frozen dialogue system prompted with
  "Write a story using these words: ..." on sets S1–S4. Document exactly what the existing
  machinery does. Expected: failure; the value is the failure mode.
- **C-POS (positional composer):** pure-Zag story composer. Words assigned to 4 beats
  (SETUP, COMPLICATION, CLIMAX, RESOLUTION) purely by position: beat1=words[0..1],
  beat2=words[2..3], beat3=words[4..5], beat4=words[6..]. No deliberation.
- **C-DEL (deliberative composer):** same pure-Zag emitter, but a planner assigns words to beats
  by class with explicit logged rationale, plus a verification pass that repairs coverage gaps:
  - SETUP: first PERSON (protagonist) + first PLACE (setting) + first THING (prop)
  - COMPLICATION: first EVENT + next unassigned THING/PERSON (affected)
  - CLIMAX: next EVENT or ABSTRACT or PERSON (turn) + next unassigned THING
  - RESOLUTION: first ABSTRACT (theme) + all remaining words in set order (details)
  - Missing class → next unassigned word in set order (fallback, logged in plan).
  - Verification: assert every input word placed in exactly one beat; assert each beat
    non-empty; on violation, spill words to the next beat and re-verify (logged).

Both composers: deterministic (no RNG), constructed-partition output (story bytes written only
to the dedicated constructed arena/file; no write path to any belief store), byte-identical reruns.

## 3. Bars (all preregistered; B1/B3/B4/B5 mechanical, B2 judged)

| Bar | What | Method | Pass criterion |
|---|---|---|---|
| B1 COVERAGE | every input word appears verbatim (case-insensitive) in the story | mechanical check per trial | ≥7/8 trials per variant |
| B2 ARC | story reads as having beginning / middle / end | two independent raters (grok-4.7, gpt-5.6-sol), blind to variant, 1–5 scale | mean ≥3.5 on ≥6/8 trials per variant; head-to-head C-DEL vs C-POS means reported |
| B3 NOVELTY | no story sentence is a verbatim substring of any training corpus | substring check vs kb.txt, dialogue battery.txt, prose championship inputs | 16/16 trials |
| B4 LEAKAGE | zero leakage of constructed content into belief | (a) belief bytes (kb.txt hash) identical before/after; (b) no ≥16-byte verbatim story substring in belief store; any violation = KILL the variant | 16/16 trials |
| B5 DETERMINISM | byte-identical reruns | 3 runs per trial, cmp | 16/16 trials |

Baseline: no bars; failure modes taxonomized (retrieval collapse / template echo / refusal /
grammar-without-meaning / arc failure / other).

## 4. Intelligence question (to be answered with evidence, not philosophy)

1. Is open-ended composition part of intelligence or a separate faculty? (Evidence: which
   machinery did the work — deliberative/planning vs retrieval vs template?)
2. Does the deliberative machinery that does eliminative logic help or hinder story-writing?
   (Evidence: C-DEL vs C-POS head-to-head on B2; planner logs.)
3. Does constructed-mode separation hold under creative load? (Evidence: B4.)
4. What is the minimal machinery that crosses from "fucks it up" to "writes a story"?

## 5. Red-team

Separate grok-4.7 agents attack: (a) the prereg (this document) for loopholes before scoring;
(b) the verdict for overclaims after scoring. Findings logged; verdict revised or defended.

## 6. Deliverables

- This prereg (committed before generation).
- `src/story.zag` (pure Zag), `inputs/words.txt`, `inputs/classes.txt`.
- `runs/` — all stories, planner logs, rerun hashes.
- `proof/` — verifier outputs (B1/B3/B4/B5), rater scores (B2).
- VERDICT.md — trial table, failure taxonomy, intelligence-question verdict with evidence.
- Commit to tnn-native-lab. No external/irreversible actions.
