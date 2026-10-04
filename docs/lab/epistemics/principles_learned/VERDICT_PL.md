# VERDICT — PL-1 Principles-Not-Triggers (2026-09-22)

**Verdict: NOT-DERIVED** (per frozen PREREG_PL §7: K1 fails).

Micah's order: *"give it the basic principles and knowledge and see if the
logic figures it out."* We did exactly that. The logic figures it out
**wherever the taught knowledge covers the vocabulary** — and nowhere
else. The failure is a knowledge-coverage failure, not an inference
failure. Details below.

## §1 Kill-bar outcomes (frozen)

| Bar | Requirement | Result |
|---|---|---|
| K1 (logic claim) | (a) NOVEL-W ≥ 70% AND > (c) | **FAIL**: (a)=8.6% (6/70), (c)=0% (0/70). (a)>(c) holds; 70% does not. |
| K2 (logic vs memorization) | (a) NOVEL-W > (b) NOVEL-W | **HOLDS**: 8.6% (6/70) > 0% (0/70). |
| K3 (no regression) | F=100%, BC=100% every arm, every battery | **HOLDS**: 100% in all 15 arm×battery cells. |

Determinism: all 15 cells byte-identical across 3 reruns (sha256-checked).
Zero RNG. Pure Zag reasoning/learning in all arms.

## §2 Full results (accuracy; W/F/BC slices)

| Battery | (a) principles-learned | (b) hand-injected | (c) baseline |
|---|---|---|---|
| frozen94 | 92.5% (W 63/70, F 12/12, BC 12/12) | 100% (70/70, 12/12, 12/12) | 62.8% (35/70, 12/12, 12/12) |
| a1r94 | 93.6% (W 64/70, F 12/12, BC 12/12) | 100% | 62.8% |
| B-188 | 86.7% (W 115/140, F 24/24, BC 24/24) | 100% | 62.8% |
| FRESH-94 | 43.6% (W 17/70, F 12/12, BC 12/12) | 25.5% (W 0/70) | 25.5% (W 0/70) |
| NOVEL-94 | 31.9% (W 6/70, F 12/12, BC 12/12) | 25.5% (W 0/70) | 25.5% (W 0/70) |

(b) aces the old batteries (it memorized their 145 verbatim phrases) and
scores exactly zero on both new batteries — memorization does not
generalize at all. (c) is at 0/70 W on the new batteries by construction
(the battery author verified every new W item is baseline-unmarked).

## §3 The boundary the trial found

Arm (a)'s 23 novel+battery hits (17 FRESH + 6 NOVEL) are **all genuine
rule applications** — deadpan markers ("what a surprise", "said no one"),
hypothetical openers ("imagine", "pretend", "perhaps", "might", "could",
"they say"), counterfactual frames ("meant missing/losing"), lyric
verb+subject ("thunder"+"drums"), fixable states ("piling up", "getting
cold"). Zero accidental hits.

Per-family on the new batteries, arm (a):

| Family | FRESH-94 | NOVEL-94 | Why |
|---|---|---|---|
| hypothetical | 10/10 | 5/10 | closed-class markers ("imagine", "might") generalize; novel frames ("chances are", "odds are", "there is talk") are unlisted |
| sarcasm | 3/10 | 0/10 | listed deadpan markers hit; new ones ("what a treat", "how refreshing", "nothing beats" as new shape) miss |
| counterfactual | 2/10 | 0/10 | "meant missing/losing" hit; "cost them", "meant a grumpy morning" unlisted |
| poetry | 1/10 | 0/10 | new image nouns ("beehive"→n/a, "well", "wind chime") and lyric verbs ("freckles", "pins", "salt") unlisted |
| analogy | 0/10 | 0/10 | new image nouns ("beehive", "parking lot", "laser beam", "tug of war") all unlisted |
| joke | 0/10 | 0/10 | new human-act phrases ("filed a union grievance", "staged a protest") unlisted |
| implicature | 1/10 | 1/10 | listed fixable states hit; new ones miss |

**The pattern is total:** the compositional logic (category conjunctions
like `pos_eval & neg_sit`, `absurd_subj & human_act`) derives the right
verdict in 100% of cases where the novel item's vocabulary intersects
the taught categories, and 0% where it doesn't. A byte-substring
mechanism cannot recognize an unlisted category member ("beehive" is an
image-noun; "freckles" is a vivid verb; "chances are" is speculative) —
that recognition IS world knowledge, and 295 taught phrases don't cover
English.

## §4 What this means for the hypothesis

Micah's hypothesis — teach the principles, let the logic derive — is
**not falsified, but underspecified**: "the basic principles and
knowledge" has to mean *genuinely broad* category knowledge, not a
phrase list. The trial separates the two components cleanly:

- **Inference: SOUND.** The rule engine applies taught principles
  correctly to every covered case, including novel combinations
  (e.g. "they say the night train might return" — a novel sentence the
  lessons never saw, derived WITHHOLD by rule).
- **Knowledge: INSUFFICIENT.** Open semantic classes cannot be taught
  as finite substring lists. The learner needs to KNOW what a beehive
  is, what "freckles" means as a verb, that "chances are" speculates —
  the knowledge organ, not the inference organ, is the gap.

K2 holding (6–0) points in the direction of Micah's bet: principles+logic
beat verbatim memorization on novel shapes, even with impoverished
knowledge. The honest next step is not "more phrases" (that converges to
arm (b)) but genuine category knowledge — the thing real TNN is supposed
to have and this byte-substring learner does not.

## §5 Learning-path audit (frozen §2 criteria)

1. No lesson content in source: **PASS** — 295 lesson members grepped
   against `delib_plearn.zag`; zero hits beyond baseline literals
   already in `delib_si2.zag` (e.g. "suppose", "if i had", "love").
2. Runtime installation: **PASS** — installed state built at runtime
   from the 8 lesson files before any scoring.
3. Learner judges: **PASS** — all 7 good lessons installed only after
   deriving 4/4 calibration verdicts each (log: `LEARN|INSTALLED|<fam>|
   cals=4` × 7).
4. Negative control: **PASS** — `lesson_bad.txt` REJECTED
   (`LEARN|REJECTED|bad|cal-mismatch`); a bad install would have aborted
   the run VOID.

## §6 Method notes / disclosures

- Timeline: lessons were authored from the principles + old misses,
  scored on the old batteries, then committed frozen (577c577f) BEFORE
  the author saw FRESH-94/NOVEL-94 items. The deciding probe is clean;
  no lesson was ever tuned to any battery item (the 25 B-188 residual
  misses were left standing as honest coverage gaps).
- FRESH/NOVEL batteries were authored by an independent subagent from
  the principles + blocklist only (no access to lessons/arm sources),
  verified baseline-unmarked at budget 2, blocklist-clean (0
  violations), ID- and utterance-disjoint.
- Battery semantics: all W items correct=WITHHOLD (established 59/94
  construction), F→WITHHOLD, BC→ENDORSE.
- Scores: `batteries/work/scores_all/scores.json`. Raw outputs are
  regenerable byte-identically (deterministic binaries + frozen
  inputs); the scorer asserts 3× sha256 equality per cell.

## §7 Commits

- `91e963ce` — frozen prereg + principles + arm-b triggers
- `fb9fd055` — FRESH-94 + NOVEL-94 batteries (battery author)
- `577c577f` — frozen lessons + three arm implementations + scorer
- (this verdict + scores — next)
