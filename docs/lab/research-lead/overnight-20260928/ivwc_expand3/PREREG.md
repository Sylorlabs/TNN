# PREREG.md -- IVWC-EXPAND3: corrected K6/K8 re-run

Frozen: 2026-10-03. This document fixes the experimental design and
the kill bars K1..K9. It must be committed ALONE (with NAMECHECK.md,
no implementation) before any implementation work. The prereg
commit must strictly precede the implementation commit. Amending a
bar after results invalidates the verdict.

## 1. What this wave is

A corrected re-run of IVWC-EXPAND2 (BUILD-FAIL on K6 and K8; see
ivwc_expand2/REPORT.md for the root-cause analysis). The expand2
mechanisms are intact; the two failures were defective
constructions:

- K6's shuffled-consequence ablation was vacuous: the joint
  rotation-by-7 of (bucket, eff) pairs is a position permutation,
  and verifier_train groups by bucket value, which is invariant
  under position permutation -- so the "shuffled" table was
  bit-identical to the true table and the bar could never pass.
- K8 measured degradation as absolute sealed accuracy, which
  conflates environment predictability with verifier quality:
  expand2 accuracy went 9->8->10 across wp 15/30/45 while the
  verifier's edge over the trivial baseline went +2 -> 0 -> -1.

Corrections (the ONLY design changes vs expand2):

C1. The shuffled arm rotates ONLY the eff array: sbkt[t]=tbkt[t],
    seff[t]=teff[(t+7)%24]. Marginals preserved (T unchanged,
    bucket counts unchanged); the bucket->eff mapping genuinely
    broken. The shuffled table will differ from the true table.
C2. K8 bars the EDGE degradation: (acc_45 - maj_45) <
    (acc_15 - maj_15), strict integer comparison. Absolute
    accuracies per shift remain reported as secondary.

Everything else -- world/beliefs/composition/consequences/
revision/verifier/shift levels (wp=15/30/45)/case identities/
train and sealed phases/bars K1-K5/K7/K9 -- is identical to the
frozen expand2 design (see ivwc_expand2/PREREG.md sections 2-4,
incorporated by reference). The wp=15 sealed worlds are
bit-identical to the IVWC-EXPAND sealed worlds, so K7 remains an
exact replication probe (expected 235 > 223).

## 2. Frozen kill bars

- K1 (commit before signal, all phases): PASS iff all 7 in-program
  checks hold (world-call counter == 0 after TRAIN COMMIT;
  unchanged across each shift's SELFCHECK COMMIT and REVISION
  COMMIT1) AND the section-4 audits confirm code ordering and the
  learner section contains no world-truth tokens.
- K2 (no disguised oracle): PASS iff the section-4 audits hold
  (no expected|answer|key|target tokens; no
  correct|reference_plan|gold tokens; == only physics/action/local;
  no reference plan; verifier inputs are consequence-derived
  (bucket, eff) pairs; T learner-computed).
- K3 (self-check discriminates, wp=15): PASS iff sealed n_pass > 0
  and n_fail > 0 and sum_eff_pass * n_fail > sum_eff_fail * n_pass
  (strict).
- K4 (verifier beats trivial baseline, wp=15): PASS iff sealed
  acc > acc_maj (strict), actual class = (eff >= T).
- K5 (determinism): PASS iff 3 runs byte-identical (equal sha256).
- K6 (ablation, CORRECTED): PASS iff sealed acc_shuf < acc
  (strict) at wp=15, where the shuffled verifier is trained on
  (tbkt[t], teff[(t+7)%24]) pairs -- buckets fixed, effs rotated,
  mapping broken, marginals preserved.
- K7 (revision replicates, wp=15): PASS iff sealed
  sum(actual_eff_P2) > sum(actual_eff_P1) (strict; expected
  235 > 223).
- K8 (carried verification degrades, CORRECTED): PASS iff
  (acc_45 - maj_45) < (acc_15 - maj_15) (strict). The verifier's
  edge over the trivial baseline must shrink under strong law
  change.
- K9 (break found): PASS iff acc_45 <= maj_45 (the frozen
  verifier no longer beats the trivial rule at wp=45).

Verdict: BUILD-PASS iff K1..K9 all PASS. Any FAIL yields
BUILD-FAIL naming the failed bar. VOID conditions: any
forbidden-interpreter invocation (PROCESS-FAIL), or any amendment
to this prereg after implementation begins.

## 3. What is NOT claimed

Same as expand2 PREREG section 4 (mechanism test of self-checking
and verification limits, not composition-novelty, not L3; the
verifier is a fixed bucket table; one wall-density law-change
axis). Incorporated by reference.

## 4. Frozen audit commands (run at report time, shell only)

Identical to expand2 PREREG section 5 (A1 phase-pair ordering on
learner_compose/learner_revise vs world_execute call sites; A2
zero world_buf/world_off in LEARNER section; A3 zero
expected|answer|key|target; A4 zero correct|reference_plan|gold
with physics-only ==; A5 sha256 equality across the three runs).
Incorporated by reference; the source is the expand2 source with
exactly the two corrections C1/C2, so A1 line numbers will shift
but the phase-pair ordering property is preserved by construction
(the edits do not move any call site across a phase boundary).

## 5. Why the corrected bars discriminate

- K6 now discriminates: the independent eff rotation changes
  bucket means (verifiable in the VB vs VBsh printout), so the
  shuffled verifier's verdicts genuinely differ; if consequence
  content did not matter, acc_shuf would match acc and the bar
  would fail.
- K8 now discriminates: it bars the quantity expand2 showed
  actually degrades (the edge +2 -> 0 -> -1). It fails if law
  change does not erode the verifier's value over the trivial
  rule (edge tie or improvement at wp=45).
