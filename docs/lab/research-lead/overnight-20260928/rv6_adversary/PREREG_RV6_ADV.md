# PREREG H-REVISE6 RED TEAM (X-RV6) FROZEN

**Date:** 2026-09-29
**Branch:** tnn-native-lab
**Target:** H-REVISE6 SURVIVES (66/66), commit 400463112
**Status:** FROZEN before any attack code written or executed.

## Mission

Independently attack the H-REVISE6 repair claim. Assume it is false.
H-REVISE6 claims: (R1) new condition (b) verifies the FULL proposed
revision ((p,v),P1) predicts fail2 correctly via a direct evaluator;
(R2) the gate is honestly three-condition with independent failure
paths; (R3) P1 discovered before corroborate at all call sites is
safe; (R4) X-RV5-1 residual documented as fundamental limit.

## Method

Adversary harness `rv6_adv.zag` = lines 1..507 of committed
`revise6.zag` (mechanism region, byte-verified by cmp) with `main()`
replaced by attack drivers. The real, unmodified
`diagnose_corroborate_v6`, `peval_prog`, `prog_apply_direct`,
`diagnose_propose`, `discover`, `vs3_*` are called. Each empirical
attack runs 3 times; all runs must be byte-identical. Pure Zag.
No Python at any stage.

## Attacks and kill criteria

**X-RV6-1 (correlated fail2 boundary):** Replay the exact X-RV5-1
fixture against the NEW gate: P0=broadcast-last,
fail1=("zqy"->"zzz"), propose must yield (0,122), P1=broadcast-first
discovered from fail1 only, fail2=("zab"->"zzz").
Attack SUCCEEDS iff the gate returns 1 and the caller appends the
wrong revision (0,122). Per the frozen builder prereg this is a
DOCUMENTED FUNDAMENTAL LIMIT, so success here = CONFIRMED RESIDUAL
(boundary verified as documented), NOT a new kill or downgrade.
If the gate instead withholds (returns 0), that contradicts the
builder's underdetermination argument and triggers a full
investigation before any verdict.

**X-RV6-2 (protocol reorder safety):** R3 moved P1 discovery before
corroborate at all call sites. Attack SUCCEEDS (DOWNGRADE or KILL)
iff any call site passes a failed discovery (nn<0) or a P1
discovered from data other than the phase's fail1 into
`diagnose_corroborate_v6`, or the reorder changes which P1 is
discovered relative to revise5's order. Method: enumerate every
`diagnose_corroborate_v6` call site by grep, verify the nn<0 FATAL
guard precedes each call, and verify by code reading that
`discover` has no VS side effects (so early discovery cannot alter
gate inputs). If every site is guarded and discovery is side-effect
free, X-RV6-2 FAILS (defense holds).

**X-RV6-3 ((b) false withhold on genuine revision):** The new (b)
adds a check revise5 lacked; it must not withhold genuine revisions.
Attack SUCCEEDS (DOWNGRADE) iff I construct a genuine revision case
(P1 correctly discovered from fail1 for its condition class, (a)
fires on fail2, P0 mispredicts fail2) where the new (b) returns 0.
Constructions: (i) deep/recursive binop P1 stressing `peval_prog`
recursion; (ii) fail2 of different length than fail1. If (b)
passes on all genuine constructions, X-RV6-3 FAILS (defense holds).

**X-RV6-4 (regression and source audit):** Attack SUCCEEDS
(DOWNGRADE or KILL) iff rebuilding committed `revise6.zag`
unmodified does not reproduce 66/66 byte-identical to committed
`REVISE6_RAW.txt` across 3 runs, or the revise5.zag-to-revise6.zag
diff contains changes outside the preregistered set (corroborate
replacement, peval_prog/prog_apply_direct helpers, call-site
reorderings, Phase M, header), or any fixture byte literal appears
in the new gate/evaluator functions. Otherwise X-RV6-4 FAILS
(defense holds).

**X-RV6-5 (independent (c) failure path):** The "honestly
three-condition" claim needs (c) to fail independently: a fail2
that (a) fires on and (b) is predicted by P1, but VS already
predicts (e.g. via an earlier appended revision). Fixture: VS with
R1 revision (0,120)->broadcast-first already appended;
fail2=("xqw"->"xxx"). (a) fires ('x'==120); (b) P1("xqw")="xxx"
passes; (c) VS("xqw")="xxx" via the revision, so the gate must
return 0 ("already predicts"). Attack SUCCEEDS (DOWNGRADE or KILL)
iff the gate returns 1 (a duplicate revision would be appended).
If it returns 0, X-RV6-5 FAILS (defense holds).

## Verdict rules

- X-RV6-1 succeeding = CONFIRMED RESIDUAL (pre-disclosed limit).
  Not a kill or downgrade.
- Any of X-RV6-2, X-RV6-3, X-RV6-4, X-RV6-5 succeeding =
  DOWNGRADED at minimum; KILLED if the gate appends a wrong
  revision in a non-adversarial setting or the 66/66 is
  unreproducible.
- All five failing = H-REVISE6 SURVIVES this red team.

## Commit lineage plan

1. This prereg committed alone (frozen).
2. Attack harness + raw evidence + result committed after.
3. Verify prereg is strict ancestor of the result commit.
4. Stage only adversary-owned paths.
