# The speech-act volume curve: where more examples stop helping

**Date:** 2026-09-22 · **Branch:** `tnn-native-lab` · **Engine:** `delib_vol.zag` (pure Zag, zero RNG)

## The headline

Micah's hypothesis was: *"I wouldn't figure out sarcasm the first time either — human stuff is weird
and unexpected. Maybe more volume is needed. The test needed is to see where that volume stops
being needed."*

The answer, measured:

| Question | Answer |
|---|---|
| Where does volume stop helping? | **2 examples per concept.** Gains are significant from 0→1 and 1→2; after that, no significant gain at any step — and from 2→32 the score **declines significantly** (53/70 → 35/70, p < 0.0001). |
| Knee per concept | hypothetical: 1 · joke: 1 · sarcasm: 2 · counterfactual: 2 · poetry: 2 · implicature: 2 · analogy: 4 |
| Is ≥8/10 per family reachable by volume alone? | **No.** No single rung passes all 7 families. Best joint rung (r2) fails sarcasm (6/10) and implicature (3/10). |
| Does learning transfer across concepts? | **No genuine transfer.** The sarcasm-only control's apparent transfer is degenerate: with no competing concepts, the word **"the" alone** withholds poetry 10/10 *and* all 12 true controls. Distinctiveness is meaningless without contrast. |
| What accumulated at every rung | Per-concept feature profiles (counts only): 150 features at r1 → 3,666 at r32. Details in §5. |

The surprise is the shape: this is not a saturation curve, it is a **peak-and-decline**. More examples
past ~2 per concept make this learner *worse*, significantly. The mechanism is understood (§6) and it
is a property of the fixed deliberative bar interacting with volume — disclosed as the experiment's
main limitation (§9).

## 1. What was built

`delib_vol.zag` replaces the PoC's hand-specified marker lists with a learner that builds each
concept's profile **from genuine examples only**. Per concept it stores nothing but
`(feature → document count)` pairs. No word lists, no frames, no markers appear in the source.

- **Learned (varies by rung):** per-concept feature counts from the first N example utterances.
- **Fixed (identical at every rung and mode):** feature *types* (word unigrams ≥3 letters, adjacent
  bigrams, first-word marker, `?`/`!` flags — the perceptual front-end, like tokenization);
  world knowledge (known-false / known-true / absurdity checks — see limitation §9);
  deliberative standards (SCORE_BAR = 500, DISC_BAR = 750); deliberation order
  (false → absurd → learned concepts → true → default endorse).
- **Decision rule:** a test utterance is withheld iff some concept's profile matches it with
  cumulative weight ≥ 500 *and* at least one feature with distinctiveness ≥ 750/1000.
  Weight per feature = prevalence × distinctiveness / 1000, where
  prevalence = 1000·df_concept/N_concept and distinctiveness = 1000·df_concept/(df_concept+df_others).
  All integer math. Status is always a deliberative conclusion, never a label lookup.

Volume ladder per concept: **0, 1, 2, 4, 8, 16, 32** genuine natural-English examples (nested: rung N
uses the first N lines of each 32-line file).

## 2. Materials audit (independent)

Four crews authored 224 utterances (32 × 7 concepts). I audited every file:

| Check | Result |
|---|---|
| 32 non-empty lines each | ✅ 7/7 files |
| No line > 140 chars, no blanks | ✅ |
| No shared 3-word sequence with any test item (c70 + b12) | ✅ after 1 fix |
| No duplicate lines within/across files | ✅ |
| Natural English, on-concept (spot-checked) | ✅ |

One fix: `ex_implicature.txt` line 18 shared the trigram "the wi fi" with W006; my first
replacement ("The trash is starting to smell up the whole garage.") turned out to paraphrase W132's
scenario, so I replaced it again with "The printer has been out of paper since Tuesday." —
zero test trigrams. Both replacements are single-line, same-concept, same-register.

## 3. The learning curve (all concepts trained jointly)

Correct verdict on all 70 c70 items is WITHHOLD. Score = items correctly withheld.

| rung | joke | sarcasm | hypoth. | analogy | counterf. | poetry | implic. | **total** |
|---|---|---|---|---|---|---|---|---|
| 0 | 5/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | **5/70 (7%)** |
| 1 | 9/10 | 4/10 | 10/10 | 5/10 | 6/10 | 8/10 | 1/10 | **43/70 (61%)** |
| 2 | 9/10 | 6/10 | 10/10 | 6/10 | 10/10 | 9/10 | 3/10 | **53/70 (76%)** |
| 4 | 7/10 | 3/10 | 10/10 | 9/10 | 10/10 | 5/10 | 3/10 | **47/70 (67%)** |
| 8 | 6/10 | 4/10 | 10/10 | 5/10 | 10/10 | 6/10 | 1/10 | **42/70 (60%)** |
| 16 | 6/10 | 0/10 | 10/10 | 5/10 | 10/10 | 4/10 | 1/10 | **36/70 (51%)** |
| 32 | 5/10 | 1/10 | 10/10 | 5/10 | 10/10 | 3/10 | 1/10 | **35/70 (50%)** |

Rung 0 reproduces the PoC's no-concept arm **byte-identically** (sha256
`49c77be1…c36`, the committed Arm 1 hash). One example per concept jumps 7% → 61%.
Two examples reach the peak, 76%. Then it slides all the way back to 50% — exactly the
PoC's hand-specified 50%, but arrived at through genuine learning followed by genuine
over-accumulation.

**Frozen bar (≥8/10 in every family): FAIL at every rung.** The best joint rung (r2) clears 5 of 7
families but sarcasm (6/10) and implicature (3/10) never reach 8 at any rung. Per-family peaks at
their individual best rungs clear the bar for joke (9), hypothetical (10), analogy (9),
counterfactual (10), poetry (9) — but never simultaneously.

## 4. Knees, with uncertainty

Knee = earliest rung attaining the family's observed maximum. Each family has only 10 items, so
adjacent rungs are usually statistically indistinguishable — the Wilson 95% intervals below are
wide, and the knee should be read as "≈1–4 examples", not a precise point.

| concept | knee | family max | 95% CI at max | note |
|---|---|---|---|---|
| hypothetical | **1** | 10/10 | [72%, 100%] | saturated immediately; formulaic frames ("what if", "suppose") |
| joke | **1** | 9/10 | [60%, 98%] | r2 ties 9/10 |
| sarcasm | **2** | 6/10 | [31%, 83%] | collapses to 0–1/10 by r16 — the profile dissolves |
| counterfactual | **2** | 10/10 | [72%, 100%] | stays at ceiling once reached |
| poetry | **2** | 9/10 | [60%, 98%] | declines to 3/10 by r32 |
| implicature | **2** | 3/10 | [11%, 60%] | never learns it — indirect requests share surface form with plain statements |
| analogy | **4** | 9/10 | [60%, 98%] | latest knee; the "X is a Y" frame needs a few sightings |

Statistical basis for the total curve (McNemar paired test on the same 70 items):

| transition | gained | lost | p | reading |
|---|---|---|---|---|
| r0 → r1 | 38 | 0 | < 0.0001 | first example per concept is transformative |
| r1 → r2 | 10 | 0 | 0.0044 | second example still helps, significantly |
| r2 → r4 | 6 | 12 | 0.24 | no significant change — the knee region |
| r4 → r8 | 3 | 8 | 0.23 | noise |
| r8 → r16 | 0 | 6 | 0.041 | significant loss begins |
| r2 → r32 (overall) | 0 | 18 | **0.000061** | the decline is real, not sampling noise |

Total at r2: 75.7%, 95% CI [64.5%, 84.2%]. Total at r32: 50.0%, 95% CI [38.6%, 61.4%]
(non-overlapping — the decline survives even unpaired comparison).

## 5. What accumulated at every rung

Unique features stored per concept profile (counts only — this is the entirety of what each
concept "knows"):

| rung | sarcasm | hypoth. | counterf. | analogy | poetry | implic. | joke | total |
|---|---|---|---|---|---|---|---|---|
| 1 | 20 | 27 | 24 | 19 | 18 | 19 | 23 | 150 |
| 2 | 41 | 51 | 43 | 36 | 33 | 38 | 47 | 289 |
| 4 | 81 | 98 | 85 | 69 | 63 | 70 | 88 | 554 |
| 8 | 177 | 180 | 154 | 135 | 118 | 136 | 159 | 1,059 |
| 16 | 339 | 316 | 284 | 245 | 230 | 255 | 305 | 1,974 |
| 32 | 648 | 563 | 513 | 442 | 444 | 474 | 582 | 3,666 |

Knowledge keeps accumulating (3,666 features at r32) while performance falls. More stored ≠ more
useful — the extra features are mostly low-prevalence, low-weight, and they dilute the
distinctiveness of the good ones.

## 6. Why more hurts: the mechanism

The decline is not mysterious; it falls out of the weight formula against the **fixed** bar:

- A feature seen in 1 of 2 examples has prevalence 500/1000. With distinctiveness 1000/1000 its
  weight is 500 — **a single feature alone** crosses SCORE_BAR. At rung 2 the bar is easy.
- The same feature at rung 32 has prevalence 31/1000 → weight 31. Crossing the unchanged bar of
  500 now needs ~16 such features on one utterance.
- Median best-concept score per test item: 1000 (r1) → 722 (r2) → 548 (r4) → 458 (r32).
  Items clearing the bar: 54 → 52 → 45 → 40 → 32 → 30 of 70.

So the fixed absolute bar gets *relatively stricter* as volume grows, because prevalence is
normalized by N. The learner genuinely learns more (smoking-gun features with distinctiveness
≥750 grow from ~20 to ~500 per concept), but each counts for less against a bar that never moves.
**The knee at 2 is conditional on this fixed bar** — a volume-relative bar (e.g., "k distinctive
features" instead of "weight ≥ 500") could show a different curve. That variant is the obvious
follow-up; it was not run here because changing the bar after seeing results would be tuning.

## 7. Transfer control: sarcasm-only training

Sarcasm examples only, all other concepts empty. If sarcasm knowledge transferred, implicature and
friends should rise with sarcasm volume.

| rung | joke | sarcasm | hypoth. | analogy | counterf. | poetry | implic. | **total** | true-endorsed |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 5/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 5/70 | 12/12 |
| 1 | 7/10 | 6/10 | 6/10 | 4/10 | 7/10 | 10/10 | 5/10 | 45/70 | **0/12** |
| 2 | 7/10 | 8/10 | 6/10 | 4/10 | 7/10 | 10/10 | 5/10 | 47/70 | **0/12** |
| 32 | 7/10 | 6/10 | 6/10 | 4/10 | 7/10 | 10/10 | 5/10 | 45/70 | **0/12** |

(r4–r16 identical to r32 within ±1; full table in evidence.)

This looks like transfer — until you look at *why*. Poetry goes 10/10 on **the single feature
"the"** (weight 500 at r2, 875 at r32). With no competing concepts, every feature has
distinctiveness 1000/1000 — there is nothing to be distinct *against* — so the most common word
in English becomes a smoking gun. The same "the" withholds **all 12 true controls** (0/12
endorsed at every rung ≥ 1), including "The letter count of a is 1."

Two consequences:

1. **There is no genuine transfer.** The cross-family scores are degenerate over-generalization,
   exposed only by the true-control leg: on c70 alone, the broken single-concept learner (45/70
   at r1) *outscores* the joint learner (43/70 at r1). Without the 12 true controls we would have
   concluded transfer exists. The control leg earned its place.
2. **Learning is concept-specific *and* contrast-dependent.** A concept profile only discriminates
   when trained against the others. Distinctiveness without competitors is vacuous — which is
   arguably how human concepts work too: you can't know what sarcasm *isn't* without the contrast
   set. In the joint arm the b12 legs hold: falsehoods withheld 12/12 at every rung, trues
   endorsed 12/12 at every rung except one transient (r4: BC10 "The count of members of the Beatles
   is 4." withheld on the bigram "of_the", distinctiveness noise at low volume — 1 false positive
   in 84 true-control trials).

## 8. Controls

| Control | Result |
|---|---|
| Zero examples (rung 0) | 5/70 (7.1%) — reproduces PoC Arm 1 **byte-identically** (sha256 `49c77be1a5506dfd59c817940f2897bb724b765ff258d58feb90451840062c36`) |
| Determinism | **60/60 cells byte-identical across 3/3 reruns** (sha256 per cell) |
| Reversed example order | **18/18 checks byte-identical** to forward order — accumulation is order-independent, as designed |
| Falsehood leg (12 planted) | Withheld 12/12 at every rung, both modes |
| True leg (12 controls) | Endorsed 12/12 at every rung in joint mode, except r4 11/12 (one transient, §7) |
| Independent verification | A from-scratch Python twin of the learner agrees with the Zag binary on **1,339/1,339** non-absurdity-gate decisions across all rungs and modes (the 61 diffs are all W001–W005, which the binary withholds via the absurdity gate the twin omits) |

## 9. Limitations (read before citing the knee)

1. **The knee is bar-conditional.** SCORE_BAR=500 / DISC_BAR=750 were set after a smoke test on
   hand-written toy examples, before the real examples were scored — frozen since, never tuned
   against c70. But the fixed-absolute-bar × normalized-prevalence interaction (§6) is very likely
   the *cause* of the decline. A volume-relative bar might move the knee or remove the decline.
2. **World knowledge is test-derived.** `is_known_false` / `is_absurd` / `is_known_true` contain
   strings authored against leg-b/c70 items in the PoC. They are byte-identical at every rung and
   mode, so they cannot bias the *curve*, but they are prior knowledge the learner didn't earn.
   Only 5 c70 items (W001–W005, absurdity) and 0 decisions elsewhere depend on them.
3. **Ten items per family.** Knee rungs are ±1 rung uncertain at best; several families'
   adjacent-rung differences are inside the Wilson intervals. The total-curve knee at 2 is the
   well-supported claim (paired p = 0.0044 up, p = 6.2e-5 down).
4. **Implicature never learns** (peak 3/10). Indirect requests ("The printer has been out of paper
   since Tuesday") share surface form with plain statements; unigram/bigram features may be the
   wrong front-end for it. Volume is not the bottleneck there — representation is.
5. **One transient false positive** in 84 true-control trials (r4 BC10). Low-volume
   distinctiveness noise; worth watching in follow-ups.

## 10. Evidence inventory

- Engine: `delib_vol.zag` (this directory)
- Examples: `examples/ex_{sarcasm,hypothetical,counterfactual,analogy,poetry,implicature,joke}.txt`
- Independent twin: `analysis_twin.py` (verification only; not part of the mechanism)
- Scored outputs: `scored_evidence/vol_r{R}_{all,sarconly,orderswap}_{c70,b12_false,b12_true}_rep{1,2,3}.txt`
  plus `.sha256` per file (90 runs; binaries, `.zagd` caches excluded from the commit)
- This report: `VOLUME_CURVE.md`

## 11. Bottom line for Micah

You were right that one lesson isn't how humans get sarcasm — one genuine example per concept took
TNN from 7% to 61%, and two took it to 76%. But the "keep going" half of the intuition didn't
survive contact with the data: for this learner, **the third example is where it starts getting
worse, not better**, and 32 examples land back at 50% — the same score the hand-specified PoC got,
reached the honest way and then overshot. The knee is ≈2 examples per concept (1–4 by family),
with hypothetical learned in a single shot and implicature unlearned at any volume tried.

Two deeper findings came free with the controls: (a) a concept learned alone is not a concept —
without competing concepts, "the" becomes a sarcasm marker and every true statement gets
withheld; distinctiveness *requires* the contrast set; (b) on the weird-English set alone, the
degenerate single-concept learner looks *better* than the joint learner — only the true-control
leg catches it. Keep the true controls in every future epistemic battery.
