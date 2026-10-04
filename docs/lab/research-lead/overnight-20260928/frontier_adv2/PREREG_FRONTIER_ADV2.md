# Preregistration: Frontier Adversary 2 (Simpler-Explanation Attack)

**Date:** 2026-09-29 17:45 PDT
**Status:** FROZEN (before any baseline code, build, or run)
**Role:** Independent Frontier Adversary 2 (simpler-explanation angle)
**Branch:** tnn-native-lab

## Mission

For each frontier BUILD-PASS claim (A. representational expansion,
B. procedure-language invention, C. causal/experimental invention), assume the
"invention" is memorization, search, or researcher cuing until proven otherwise.
Construct the strongest SIMPLEST baseline that could plausibly explain the
builder's results. If it does, the L3 claim is KILLED (or DOWNGRADED to L2+).

This prereg freezes methodology and decision rules. Per-claim baseline specs
are frozen in claim-specific amendments (committed alone, before building).

## Relation to Adversary 1

Adversary 1 attacks the L3 mechanism directly (mechanism bugs, trace honesty,
prereg violations). I attack via baselines and OOD generalization only.
No duplication: I do not re-attack mechanism internals.

## Baseline classes (pure Zag)

### B-MEM: Memorizer / nearest-neighbor
Store all training (input, output) pairs. On a test input, emit the output of
the nearest stored input (exact match preferred; else smallest Hamming/edit
distance; WITHHOLD if all distances exceed a pinned threshold). This is the
deliberately SIMPLE but non-crippled baseline: a real memorizer, not a
straw man.

### B-ENUM: Enumerator over the frozen OLD language
Brute-force the builder's frozen old DSL up to the builder's own size bound.
Success means the old language was NOT provably insufficient, and the
expansion premise fails. The enumerator must use the same size bound the
builder claims was insufficient.

### B-CUE: Researcher-cue audit
Inspect the "generic substrate" for researcher-enumerated solution components.
Test: ablate the suspicious substrate component. If learning succeeds with it
and fails without it, and the component is a researcher-authored enumeration
of the solution family, the claim is researcher-cued.

### B-TEMP: Template-fitter
Fit parameters of a supplied template (e.g., affine index maps with free
constants). For claims that reduce to parameter fitting of a given form.

### B-OOD: OOD generalization attack
My own held-out distribution, constructed so memorization and enumeration
cannot succeed but a genuine invention could (e.g., longer inputs, new alphabet,
new arity, permuted surface features). If the builder's "invention" degrades
to memorizer rates on B-OOD, the claim is overfitted, not an invention.

## Evidence demanded from each claim

Before attacking, the builder must have published in its result commit:
1. Raw training set (inputs, outputs).
2. Raw hidden test set and per-case builder outputs.
3. The frozen old DSL grammar (for B-ENUM).
4. White-box creation trace (for B-CUE audit).

If any is missing: verdict EVIDENCE-GAP, attack marked INCONCLUSIVE
(never a pass).

## Frozen kill bars

**K-A2-1 (Memorization suffices):** If B-MEM scores within the builder's
reported hidden-test band (equal or better accuracy), the builder's
performance needs no invention. L3 KILLED.

**K-A2-2 (Old language suffices):** If B-ENUM finds any program in the frozen
old DSL (within builder's size bound) reproducing builder hidden accuracy,
the "provably insufficient" premise is false. L3 KILLED.

**K-A2-3 (Researcher-cued):** If ablating one researcher-authored substrate
component destroys learning while the builder succeeds with it, and that
component enumerates the solution family, the claim is DOWNGRADED to L2+
(researcher supplied the language; learner searched it).

**K-A2-4 (OOD collapse):** If builder accuracy on B-OOD falls to within the
B-MEM band, the invention does not generalize beyond the training
distribution. L3 claim unsupported: DOWNGRADED (overfitted invention).

## Verdict labels

- **SIMPLER-EXPLANATION-SUFFICES:** any K-A2 bar fires. L3 KILLED (K-A2-1,
  K-A2-2) or DOWNGRADED to L2+ (K-A2-3, K-A2-4).
- **SIMPLER-EXPLANATION-FAILS:** no baseline matches; builder exceeds all
  baselines by a clear margin on builder tests AND B-OOD. Supports L3
  (supports, does not certify; other gates still apply).
- **INCONCLUSIVE:** mixed results or EVIDENCE-GAP.

## Procedure per claim

1. Claim-specific amendment freezes: claim result commit, training/hidden sets,
   old DSL grammar, exact baseline algorithm, B-OOD distribution, kill
   thresholds. Committed ALONE before any baseline build.
2. Build baselines in pure Zag. No Python anywhere (implementation, harness,
   analysis, scratch). Analysis via shell grep/cmp/md5/diff/awk only.
3. Run 3/3 byte-identical. Record raw md5.
4. Commit raw evidence + report under frontier_adv2/ only.
5. No em dashes in any authored documentation (byte-verified).
6. Adversary does not promote or demote claims canonically; verdicts are
   adversary findings for governance adjudication.

## Scope

This prereg covers frontier claims A, B, C as they land. It does NOT cover
the old treadmill lanes (ROUTER, INTENT, SEG, REVISE, UNIFIED, MEM, FDCR,
CAUSAL vN series), which Adversary 1 and lane red teams handle.

## FROZEN

No baseline code, build, or run existed before this commit. No thresholds
adjusted post-hoc. Amendments are transparent and re-frozen.
