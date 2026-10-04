# PREREG-3: P5-META-LEARNING -- THE PRIOR PREREG IS DECLARED VOID AS A TEST

Lane `p5meta2`. Committed **alone**, after the unmodified prereg run and before
any change to the implementation. Claim block **C7xx**.

## 0. WHAT THE UNMODIFIED RUN MEASURED (recorded, not reinterpreted)

Apparatus repaired (`p5b.zag`, commit `fbaff2f93`), prereg `24c133b42` executed
**unmodified**. Payload byte-identical 3/3, `BOUNDS_VIOLATIONS = 0` over the
whole run, determinism PASS.

| bar | result | measured quantity |
|---|---|---|
| K4 FLOOR | **FAIL** | REACH = 2/6 RELATED, 3/6 MISLEADING, 2/6 PARTIAL, 3/6 DOMAIN2 |
| K5 RELATED SPEEDUP | **FAIL** | `EX(COLD)/EX(PRIOR) = 1.00` (1032/1032) |
| K6 IRRELEVANT NEUTRAL | PASS | EX equal, per-family maxdiff 0, SA delta 18 <= 25% |
| K7 MISLEADING | **FAIL** | `RR = 0 < 6`; reuse never rejected |
| K8 PARTIAL SELECTIVE | **FAIL** | `EX(PARTIAL) == EX(RELATED)` |
| K9 DOMAIN2 TRANSFER | **FAIL** | ratio 1.00 (780/780) |
| K10 ABL-L1 DISCRIMINATION | **FAIL** | `D2_PRIOR/ABL_L2 = 1.00 < 1.4` |
| K11 ABL-L1 NECESSARY | **FAIL** | `EX(L1,RELATED)/EX(PRIOR,RELATED) = 1.00` |
| K12 ABL-L1 HARMFUL | PASS | vacuously, `EX(L1)==EX(PRIOR)` |
| K13 NOT-MORE-DATA | PASS | DATA/COLD >= 100 on all five |
| K14 DECOMPOSITION | PASS | vacuously, all channels equal |

**Negative transfer** `EX(PRIOR) - EX(COLD)` = **0 on all five conditions**;
`COST(PRIOR) - COST(COLD)` = +262 RELATED, +201 MISLEADING, +262 PARTIAL,
+18 IRRELEVANT, **-9 DOMAIN2**.

**Ablation verdict on causality: the meta-structure is NOT causal, because
there is no advantage to attribute.** `EX(PRIOR) == EX(COLD)` in every
condition and ablating L1 changes EX by 0%. Speedup did **not** appear on
IRRELEVANT (ratio 1.00 there too) -- but not because the instrument is
discriminating; it appears *nowhere*, which is the "just more data" signature
with the volume effect also absent.

**Recorded verdict: NO META-LEARNING (this design).**

## 1. WHY THE DESIGN IS VOID AS A TEST (two independent defects)

### D-A. `derive_ar` does not implement prereg 1.4. CODE BUG.

Prereg 1.4 specifies `AR[0..3]` as a **permutation** of the arity ladder
obtained by sorting arities by `STRATT[arity].wins` descending, ties by arity
ascending. The inherited `derive_ar` never masks an already-selected arity, so
it selects the argmax four times. Measured: `prior_AR = 1,1,1,1`.

Consequence: the L2-arity channel carries **no information at all**, arities
2,3,4 are never searched, and K9/K10/K14 cannot test what they claim to test.
Their PASS/FAIL is uninformative. **The measured K9 FAIL and K10 FAIL are
therefore not evidence about meta-learning.** This is a spec-conformance repair,
not a design change, but it changes results, so it is preregistered here.

### D-B. THE HYPOTHESIS GRAMMAR ADMITS CONSTANT PREDICTORS. DESIGN FLAW.

Any arity-1 hypothesis on a slot that is **inactive** in the family, with
`op = NOR` (`op3`: output 1 iff the sum of the active bits is 0), is a
**constant function** of the input. The prereg's search admits it, and it fits
any in-sample buffer whose labels happen to be constant so far. Measured
consequences:

- probe on a **fresh empty-PLAN** learner reaches criterion at **`EX = 4`**;
- `SLOT_REL` is **4 for slot 0 and 0 for all eleven other slots**;
- `STRATT` records **all 4 wins at arity 1**, arities 2-3 unused;
- `IRRELEVANT` (label noise) reaches criterion **6/6** at `EX = 24`.

So the "acquired meta-structure" measured by this design is the single
hypothesis *"arity 1, slot 0, NOR"* -- a constant. Every arm finds it in the
same few rounds, which is why `EX(PRIOR) == EX(COLD)` exactly. **The design
cannot detect meta-learning even if meta-learning were present**, because the
task it poses is solved by a constant.

Per the standing rule, this prereg is **VOID** and is re-registered below.
The measured result of section 0 stands as measured and is not withdrawn; it
is re-labelled as *not a test of the hypothesis*, because the instrument was
degenerate.

### D-C. `res[6]` (RA) is aliased. METRIC BUG.

`RA` is incremented in the reuse phase (correct) **and again** in the
plan-creation branch of the search phase. So `RA` counts reuse attempts *plus*
plan creations, which makes prereg K7's companion reading and my own K15
`fresh_RA = 0` clause unsatisfiable by construction. Measured `fresh_RA = 1`
on a genuinely empty PLAN table, which is how this was found.

**VOID clauses, explicitly and by name:** K15's `RA = 0 on an empty starting
PLAN` clause, and any reading of `RA` as "structural reuse attempts".
`RR` was never aliased and K7's `RR >= 6` clause stands unamended.

## 2. THE FIXES (all three, preregistered before implementation)

- **F1 (repairs D-A).** `derive_ar` must return a permutation: maintain a
  `used` bitmask over arities 1..4 and skip any already-selected arity.
  Ties broken by arity ascending, as prereg 1.4 already specifies.
- **F2 (repairs D-B). NON-DEGENERACY RULE.** A hypothesis is **admissible**
  iff, in addition to zero in-sample mismatches, it predicts **both** classes
  on the in-sample buffer. A constant predictor is inadmissible at every round,
  in the search phase and in the reuse phase alike. This is a property of the
  hypothesis and the presented stream; it uses no knowledge of the family, so
  it leaks nothing. It is the minimal rule that removes the degeneracy: it
  excludes exactly the hypotheses whose prediction does not vary with the input.
- **F3 (repairs D-C).** Split the counter: `RA` counts reuse-phase proposals
  only; a new field `PC` counts PLAN writes. `NS` is unchanged.
- **F4 (defect found by the probe).** `V` is floored at 1: an uninitialised
  learner state must not yield a verification batch of 0. Measured `SA = 16`
  on the fresh probe was a consequence of `V = 0`.

## 3. WHAT IS **NOT** CHANGED

Everything scientific is inherited verbatim and **no kill bar is moved**:
`RMAX 64`, `SB 24`, `AUDN 16`, `MAXE 256`, `VAUD 32`, the five conditions and
their fids 16..45, the seven arms and their channel assignments, `TrainA` and
`COLD`, the metric definitions in prereg 4.2, and **all of K1..K14 exactly as
frozen in `24c133b42`**. K4's `REACH = 6` requirement is *not* relaxed.

## 4. NEW BARS FOR THE DEFECTS (additive; they gate, they do not relax)

- **K16 PERMUTATION**: `AR[0..3]` is a permutation of 1..4 in both trained
  states, and `STRUCT a1..a3 uses` sums to > 0 after training.
- **K17 NON-DEGENERACY**: `SLOT_REL` is nonzero on **at least 3** distinct
  slots and `AR` is not constant; `IRRELEVANT` has `REACH = 0` and
  `EX = 256` on 6/6 for every arm.
- **K18 COUNTER SEPARATION**: `RA = 0` and `RR = 0` on every episode whose
  starting PLAN table is empty; `PC >= 1` on every episode that reached
  criterion; `BOUNDS_VIOLATIONS = 0`.

K16/K17/K18 FAIL -> `APPARATUS-FAIL`; K4..K14 are then not evaluated.

## 5. FALSIFIABLE PREDICTIONS, REGISTERED IN ADVANCE

- **P1.** The degeneracy was located at one slot. Under F2 the absorbed
  structure must spread: `SLOT_REL` nonzero on >= 3 slots, all of them in
  `TrainA`, and **zero on every `COLD` slot**. If relevance still concentrates
  on a single slot, F2 did not remove the degeneracy and the design is still
  broken.
- **P2.** Under F2, `IRRELEVANT` becomes `EX = 256, REACH = 0` on 6/6 for
  every arm, because no hypothesis can fit label noise without being constant.
  If `IRRELEVANT` still reaches criterion, some other degenerate hypothesis
  survives and the non-degeneracy rule is insufficient.
- **P3.** The frozen cost model of prereg section 5 predicts
  `EX(PRIOR)/EX(COLD)` of roughly 1/12 on RELATED, 1/1.9 on MISLEADING,
  1/3.5 on PARTIAL, 1/1 on IRRELEVANT and 1/1.7 on DOMAIN2. The bars, not this
  table, decide the verdict.
- **P4 (the bar that must not be softened).** If K5 or K9 or K10 or K11 or
  K13 fails **again** after F1-F4, the finding is
  **NO META-LEARNING for this architecture, with a working instrument**, and
  that is a citable negative result rather than an apparatus failure. It is
  **not** grounds for a third re-preregistration of the same design.

## 6. ATTESTATION

Committed alone, after the unmodified run, before any of F1-F4 exists in
source. Predictions P1, P2 and P4 are falsifiable and were registered before
the fixed run, so a pass cannot be attributed to having tuned the design until
it passed. Section 9 of prereg `24c133b42` -- researcher-authored hypothesis
grammar, researcher-supplied form of the meta-structure, arity matched to the
training-dominant arity, six families per condition, single frozen seed set --
is inherited unchanged and is restated here as still binding on any claim this
lane could make.
