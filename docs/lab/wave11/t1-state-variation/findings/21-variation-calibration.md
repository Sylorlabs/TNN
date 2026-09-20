# 21 — Variation calibration: how much is enough, how much is too much

## 1. Slice
Track 1, slice 21: define the lower and upper bounds of lawful state-dependent expression
variation, and the calibration trial that measures a mechanism against both.

## 2. Falsifiable claim
A lawful state-variation mechanism exists whose expression-diversity D (defined below)
sits strictly between a cosmetic-jitter floor L=0.15 and an arbitrariness ceiling
U=0.6·D_cross, with variation monotonically tracking logged state-distance
(Spearman ρ ≥ 0.4), while every (input, state) pair replays byte-identically and all
MUST-NOT-vary anchors (verdicts, memory ops, refusals, ledger) hold fixed. If no
mechanism can sit between the bounds, state-dependent variation as specified is falsified.

## 3. Design
Calibration trial: an I×S matrix. I=24 inputs (8 explanation requests, 8 "walk me through
your reasoning", 8 elaboration requests — all with preregistered verdict anchors pinned).
S=16 lawful states, each produced by a logged, replayable episode history, differing in
the prereg-enumerated state variables only (memory recency contents, active context
partition, deliberation-depth budget, episode clock, emphasis weights from prior feedback).
No synthesized states. Every (i,s) cell runs twice; replay distance must be exactly 0
or the trial is void (determinism bug, not a bound reading).

Expression-diversity metric, exact: `norm(t)` lowercases, strips punctuation, collapses
whitespace. `ned(a,b)` = byte-Levenshtein(`norm(a)`,`norm(b)`) / max length, in [0,1].
D_same[i] = mean pairwise ned over the S outputs for input i. D_cross[i] = mean pairwise
ned between outputs for input i and outputs for all j≠i at matched states.
D_var = median_i D_same[i]; D_cross = median_i D_cross[i].
State-distance: normalized Hamming distance over the logged state vector for the pair.
Lawfulness curve: Spearman ρ between state-distance and ned across all (i, s1<s2) pairs.

Upper-bound operationalization (the arbitrariness detector, Track 3 interface): a
deterministic classifier on (n-gram Jaccard, ned, length ratio, template-slot overlap)
labels pairs as Arm-C-style (same input, different lawful states) vs Arm-B-style
(fenced seeded-RNG variation, per AMENDMENT_2026-09-20_RNG_ARM_B.md). AUC < 0.65 means
the variation is indistinguishable from arbitrary output.

Numeric bands: PASS iff 0.15 ≤ D_var < 0.6·D_cross, ρ ≥ 0.4, detector AUC ≥ 0.65, and
zero verdict-anchor drift. L=0.15: below it, outputs differ by <1 word in 7 on average —
inside a single template's cosmetic slot-fill range, i.e. hardcoded vibes. U=0.6·D_cross:
at 60% of between-question distance, source attribution collapses and the detector can
no longer tell "state variation" from "arbitrary generation".

## 4. Kill bar
1. MUST-NOT-vary breach (any verdict, memory decision, refusal, or ledger entry drifts
   across states) → KILL immediately. This outranks all bounds.
2. Upper-bound failure: D_var ≥ 0.6·D_cross, or detector AUC < 0.65, or ρ < 0.4
   → KILL. Variation indistinguishable from arbitrary is RNG-equivalent in every
   property Micah's law cares about (unexplainable from logged state, unjudgeable);
   keeping it would smuggle RNG past the no-RNG law under a determinism label.
3. Lower-bound failure: D_var < 0.15 → FAIL but not kill: the mechanism is a null
   (hardcoded vibes unsolved), returned for gain repair per law 6 (deliberate repair).
   A second calibrated build that still cannot clear 0.15 → KILL as falsified (two-strike).
4. Replay ≠ byte-identical on any cell → trial void; bounds unread until determinism
   is restored (standing law 2).

## 5. Honesty notes
The 0.15/0.60/0.65/0.4 constants are judgment calls, not theorems; the pilot must re-fit
them against the three reference points (null mechanism, Arm B, deliberately-arbitrary
control) before scoring any real mechanism. ned penalizes long elaborations and is blind
to semantic vacuity — a mechanism could score high via synonym shuffling with no lawful
state story; the ρ ≥ 0.4 lawfulness curve is the guard, and it is the weakest link
(small S=16, noisy rank statistic). The detector's feature family is crude; a clever
arbitrary generator could beat it, which is Track 3's problem to keep honest, not mine.
I am NOT claiming these bands transfer across input genres — they are calibrated for
explanation/reasoning/elaboration only.

## 6. Next build step
Build the I×S harness with the verdict-anchor checker and run the metric-validation
pilot first: score the null mechanism (zero variation), Arm B (fenced RNG), and a
deliberately-arbitrary control. If the bounds do not cleanly separate those three
reference points, the calibration is broken — fix the calibrator before any real
mechanism is judged by it.
