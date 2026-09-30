# Threshold Red Team: Result

Date: 2026-09-30. Attack prereg: REDTEAM-THRESHOLD-PREREG-FROZEN,
committed 15982381c before any attack implementation (K1 satisfied).

## Verdict

REDTEAM-THRESHOLD-BREAK.

Family A (Tier-2 condition) BREAKS the mechanism's tiered
characterization cleanly. Family B (crowding) survives this round
(64/64), but via a behaviorally-equivalent distractor, not via the
true library term. Per the frozen overall bar, a single broken
structural claim refutes the mechanism as characterized.

## Target (recap)

d0d296650 (THRESHOLD-PASS), reproduced byte-identical at 07785ac78.
COND primitive (op==4) + tiered combiner. Tier-1: terminal/library
conditions, min slice min(4, en/8), no persistence. Tier-2:
round-built conditions, min slice max(4, en/8), persistence gate
(condition and both arms in pbeam). T1 tax: B=2 Tier-1, B=4 Tier-2.

## Family A: Tier-2 condition (A1-FAIR)

Fam 9: E9 = (C AND Y4) OR ((NOT C) AND Y5), C = (x1 AND x2).
C is composite and must be round-built (kind 1). Frozen 16-row
evidence gives C=1 on 4 rows, C=0 on 12 rows, meeting the Tier-2
min slice max(4, 16/8)=4 on both sides. Exact slice agreement
holds for arms Y4/Y5. This is the Tier-2 pass's best fair chance.

### Observed (3/3 byte-identical)

- Evidence self-check: ok (16/16 rows match sealed(9,x)).
- Round 0: C built by the pairwise AND phase (C_beam=1). Not in
  pbeam (pbeam = terminals), so the Tier-2 pass cannot use it yet.
  Expected.
- Round 1: C culled from the beam (C_beam=0). pbeam gate blocks
  (pbeam = S_0, no C). Expected.
- Round 2: pbeam = B_0 CONTAINS C (C_pbeam=1). This is the moment
  the Tier-2 pass could fire. Current beam B_1 does NOT contain C.
  condhit stays -1.
- Rounds 3-23: C never reappears (C_beam=0, C_pbeam=0). condhit=-1.
- Final: best_true=56/64 (< 61/64 phase2 hit bar). Best node
  contains NO COND node at all (A1 COND none). HAS_T2_COND=0.

### Failure signature (D1 diagnostic)

The Tier-2 pass is unreachable because its persistence precondition
contradicts the beam selection pressure. C=(x1&x2) predicts the
target at 50% (score 4800 = 5000 - 200*opc). Beam selection keeps
the top 32 by (score desc, opc asc, node asc); C is culled after a
single round. The Tier-2 pass requires the condition in BOTH the
current beam and pbeam (two consecutive survivals), but a
discriminative condition is a poor target-predictor, so selection
culls exactly the nodes the Tier-2 pass needs. The combiner logic
itself was never reached; the failure is in the selection/persistence
interaction, not in the slice math.

This is structural, not regime-specific: a condition's value is
discriminative (P(target|C) vs P(target|~C)), but beam selection
rewards predictive accuracy (P(node == target)). Any Tier-2
condition that is not itself a good target-predictor will be culled
before the persistence gate can ever see it.

### Family A verdict: BREAK

BIAS-FITTING predictions hold: CONDHIT=-1, best 56/64 < 61/64,
no Tier-2 COND anywhere. The mechanism's conditional handling is
effectively Tier-1-only. The "tiered" design does not deliver
Tier-2 conditional discovery.

## Family B: crowding (B1)

Frozen fam 8 world (E = (D AND Y4) OR ((NOT D) AND Y5)). True D
library term (t=8) plus three distractors added BEFORE it
(adversarial tie-break): D1 = D xor (x1&x2&x3) (t=9), D2 = D xor
x6 (t=10), D3 = NOT D (t=11). 12 rounds (tight time), seed 710202
(same evidence regime as frozen A2).

### Observed (3/3 byte-identical)

- hit_iv=5, final_true=64/64, CONDHIT=0.
- Installed COND uses t=11 (D3 = NOT D), kind=0. HAS_D=0.
- 64/64 proves the installed node is behaviorally correct:
  COND(NOT D, Y5, Y4) = E (arms swapped). Correct-via-equivalent,
  as anticipated in the prereg.

### Family B verdict: SURVIVE-THIS-ROUND

D7 = 64/64 >= 61/64 within 12 rounds. The mechanism resolves under
crowding with 3 distractor conditions and halved time. The unusable
near-miss distractors (D1, D2) were correctly avoided.

Caveat (diagnostic, not verdict-changing): it survived via D3, not
via the true D. HAS_D=0. The A2-PASS reuse criterion (true library
term as subexpression) does NOT hold under crowding; the mechanism
finds A correct conditional structure, but not reliably the
intended reuse. D3 was a "lucky" distractor (its negation supports
an equivalent solution). A follow-up with only non-equivalent
distractors (D1, D2) would test whether the mechanism breaks when
no distractor supports a correct solution.

## Overall

REDTEAM-THRESHOLD-BREAK. Family A refutes the tiered
characterization: the Tier-2 pass is decorative. The threshold
calibration (THRESHOLD-PASS) stands for what it was: a Tier-1
recalibration on Tier-1 batteries. It does not generalize to
Tier-2 conditional structure.

## Kill bars

- K1 (prereg strictly precedes implementation): PASS. Prereg at
  15982381c; attack implementation and runs after. Merge-base
  verified.
- K2 (both families 3/3 with verdicts vs frozen predictions): PASS.
  A1: BREAK (CONDHIT -1, 56/64, no Tier-2 COND). B1:
  SURVIVE-THIS-ROUND (64/64 in 5 IVs, via D3-equivalent).
- K3 (pure Zag, determinism, no dash): PASS. Zero Python at every
  step (implementation, build, runs; analysis via shell cmp/md5).
  3/3 byte-identical (md5 da3cb61643074f45c2d18b4998c58f63),
  exit 0, zero stderr. Shell-only dash check clean. Committed
  mechanism functions byte-identical to d0d296650 (diff shows
  additions only: fam 9, drivers, diagnostics, main).

## Files

- PREREG_THRESHOLD_REDTEAM.md (frozen, 15982381c)
- redteam_attack.zag (attack implementation; mechanism copied
  verbatim from d0d296650, diff = additions only)
- redteam_attack_bin (znc-built, not committed)
- RT_1/2/3.txt, RT_1/2/3.err (raw outputs; .err all zero bytes)
- RESULT_THRESHOLD_REDTEAM.md (this file)
- build.err (znc warnings; pre-existing, in committed functions)

REDTEAM-THRESHOLD-BREAK.
