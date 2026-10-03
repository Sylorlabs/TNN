# PREREG_SI_A1X — SI Arm 1 extended tests (FROZEN 2026-09-22)

Frozen before any extended-test run. Authorized by Micah 2026-09-22
("Run more tests here" on the SI Arm 1 epistemic plateau).

## Background (committed, verified)

- Frozen Arm 1 epistemic battery (94 items): 29 → 59 → 59 → 59 for
  1×/2×/4×/8×. Fresh disjoint 94-item battery (work_a1r): identical
  29 → 59 → 59 → 59. Resolution verdict: PLATEAU-CONFIRMED
  (ADDENDUM_SI_A1.md, commit `96d2a3c358d15c3da56cea9b212df839cf4d8aa2`).
- Frozen verdict remains PARTIAL per PREREG §3e strict clause (a):
  gain(4×→8×) < gain(2×→4×) fails as 0 < 0.
- Engine: `work_a1/delib_si.zag` — 1× world-knowledge checks;
  2× +6 speech-act matchers; 4× +one reconsideration round on
  non-unanimous items (nmatch≥1 AND kt+cm2≥1; majority wins; ties keep
  the 2× verdict); 8× +independent ledger re-derivation (disagreement
  → WITHHOLD, counted as verification-flip).

## 1. Extended battery B-188 (≥2× scale)

188 fresh items, same construction discipline as
work_a1r/gen_battery_a1r.py (delib trigger inventory FIXED — freshness
is at item level, not trigger level):

- 24 falsehoods, IDs F301–F324: declarative false world claims, each
  firing exactly one `is_known_false` trigger group. Correct: WITHHOLD.
- 24 true controls, IDs BC25–BC48: true verifiable claims, firing NO
  predicate. Correct: ENDORSE.
- 140 weird-English, IDs W211–W350: 7 families × 20, per-family
  matcher-fire balance mirroring the frozen/a1r batteries
  (joke 10, sarcasm 6, hypothetical 10, analogy 6, poetry 10,
  counterfactual 18, implicature 10 of 20 fire their family's matcher;
  the rest fire nothing). Each firing item fires exactly its intended
  predicates; non-firing items fire nothing. Correct: WITHHOLD.

ID disjointness: asserted programmatically against the frozen 94
(F003–F231, BC01–BC12, W001–W140) and the a1r 94 (F901–F912,
BC13–BC24, W141–W210). Zero overlap required.

Construction audit (Python mirror of the delib trigger lists, same as
the a1r audit): every item must fire exactly its intended predicates.
Additionally the INERTNESS AUDIT: for every item,
kt + cm2 ≤ kf + ab + nmatch must hold (this is the battery-side
condition under which the 4× reconsideration majority can never flip
a verdict — see §5). Battery is rejected if any audit fails.

Construction script + item list committed. Zero RNG.

## 2. Engine: delib_si2.zag

`delib_si2.zag` = `work_a1/delib_si.zag` with EXACTLY ONE change: the
budget argument parser reads a full non-negative integer
(1, 2, 4, 8, 16, 32) instead of matching only the first character.
All deliberation logic, trigger lists, staged verdict rule,
reconsideration rule, verification path, and predicate-evaluation
counting are byte-identical.

VERDICT-IDENTITY GATE (must pass before any extended-battery result
is trusted): delib_si2 at budgets 1/2/4/8 produces byte-identical
canonical verdict digests to the frozen delib_si build on ALL THREE
batteries (frozen-94, a1r-94, B-188): 12 cells × 3 reruns.
Canonical digest = sha256 over sorted "ID|verdict" lines.
If any cell differs: STOP, diagnose, do not proceed.

Rationale for the single change: the frozen parser only accepts the
first character ('1','2','4','8'); "16"/"32" must parse as integers
to test whether raw budget increases above 8× move anything.

## 3. Sweep design

PRIMARY: B-188 × budgets {1, 2, 4, 8, 16, 32} × 3 reruns.
SECONDARY: frozen-94 × {16, 32} × 3; a1r-94 × {16, 32} × 3
(ladder-saturation check on the earlier batteries).
32× runs iff the 16× cells complete cleanly (cheapness gate).

Zero RNG. Raw per-budget outputs saved
(`epi/out_b{B}_{false,true,c70}.txt` convention).
Determinism: 3 reruns byte-identical canonical digests per cell.
Gate battery 6/6 re-confirmed on the untouched learner (as in A1R).

## 4. Strict vs relaxed — test-both (amendment PROPOSED, NOT signed)

The relaxed amendment below is a TEST CANDIDATE ONLY. Micah has not
signed it. Both verdicts are computed from the same measured data;
no rule is rewritten.

- STRICT (frozen PREREG §3e): clause (a) gain(4×→8×) < gain(2×→4×);
  clause (b) gain(4×→8×) ≤ 1pp. Epistemic PASS requires both.
- RELAXED (a′): clause (a) gain(4×→8×) ≤ gain(2×→4×); clause (b)
  unchanged. Epistemic PASS requires both.

Report: verdict under STRICT and under RELAXED on B-188 (plus the
two 94s for reference), and whether the verdict CHANGES.
Interpretation note (preregistered): under RELAXED, a hard plateau
(0pp/0pp) satisfies (a′); the knee-location question (2× vs the
hypothesized 2×–4× window) is NOT re-litigated here — it stays with
Micah's amendment decision.

## 5. Higher-budget question (preregistered prediction)

Q: does any budget above 8× change any verdict on any item?
Prediction: NO — LADDER-SATURATED. Analytic basis (to be verified
empirically):

- Reconsideration fires only when nmatch≥1 (already-WITHHOLD items)
  and can flip WITHHOLD→ENDORSE only if kt+cm2 > kf+ab+nmatch; the
  §1 inertness audit excludes this on the battery side.
- Verification re-derives the staged verdict from the same ledger
  through the same rule; disagreement is impossible absent a
  derivation fault (pv vs v_pre are the same predicate by
  construction), so vflip=0 always.
- Hence 16×/32× (which engage no new gates beyond ≥8) are
  verdict-identical to 8× on every item.

Empirical check: canonical digests at 16×/32× must equal the 8×
digest on all three batteries; recon/vflip counters must stay 0
(or outcome-inert, as in A1R's single tie).

## 6. Mechanism probes (preregistered)

6a. Per-item trajectories: verdict at 1/2/4/8/16/32 for every B-188
    item. Classify: SOLVED-1X (correct at 1×), SOLVED-2X (wrong at
    1×, correct at ≥2×), NEVER (wrong at every budget).
6b. Ledger audit: Python mirror (kf/ab/6 matchers/kt/cm2) predicts
    the verdict for every item×budget; require 100% agreement with
    the Zag binary before ledgers are used for classification.
    (Binary verdicts are authoritative; the mirror is the probe
    instrument.)
6c. Cheap-property test: candidate predictor of NEVER =
    "item fires zero predicates in the 2× ledger" (i.e. its
    non-factual status is unmarked in the delib's fixed trigger
    inventory). Report precision/recall vs the trajectory
    classification, per-family NEVER rates, and NEVER proportion
    across all three batteries (predicted stable ≈35–37%).
6d. Inertness confirmation: report per-battery recon-fire count and
    outcome, vflip count; confirm the §5 prediction.

## 7. Resolution rules

- SCALE: PLATEAU-REPLICATES-AT-2X-SCALE iff on B-188:
  gain(1×→2×) > 10pp AND gain(2×→4×) ≤ 1pp AND gain(4×→8×) ≤ 1pp.
  Else PLATEAU-NOT-REPLICATED (report the measured curve).
- HIGHER BUDGETS: LADDER-SATURATED iff 16×/32× digests equal 8× on
  all three batteries with no verdict changes on any item.
- STRICT-vs-RELAXED: report both verdicts + CHANGE/NO-CHANGE.
- MECHANISM: classification table (§6a), predictor precision/recall
  (§6c), inertness status (§6d).
- NEXT BOUNDARY: if the plateau is confirmed at all budgets and
  scales, PROPOSE (do not run) the next boundary experiment —
  candidates: new-knowledge injection (extend the trigger inventory),
  different deliberation shape (cross-item consistency). The proposal
  is written after results, not preregistered.

## 8. Standards

Frozen prereg before results (this file). Zero RNG. Byte-identical
reruns (3×). Pure Zag for deliberation; Python glue only.
Commit to sylorlabs/TNN branch tnn-native-lab under
docs/lab/coding/reflection/speed_intel/ (prereg) and
.../work_a1x/ (battery, engine, logs, results). No binaries, no
.zagd, no .zag-cache in commits.
