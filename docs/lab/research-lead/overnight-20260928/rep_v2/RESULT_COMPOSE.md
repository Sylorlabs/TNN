# COMPOSE Result Report (H-COMPOSE)

**Date:** 2026-09-29
**Prereg:** `rep_v2/PREREG_COMPOSE.md` (commit 271ec362b, frozen before implementation)
**Implementation:** `rep_v2/fdcr_learn.zag` (COMPOSE operator, reason=6)
**Verdict:** H-COMPOSE KILLED on utility. K-C1 PASS, K-C2 FAIL, K-C3 N/A (confirmed no effect), K-C4 PASS.

## What was implemented

Deliberate union-intent COMPOSE operator in the learning fixpoint, per frozen
spec. For pairs (C1,C2) of active ctx-free concepts with non-subsuming
intents, if the intent union U satisfies |U|<=6, at least one entity has all
features of U, and no active concept has intent exactly U, recruit C3 with
intent=U, members={entities covering U}, reason=6, with subset/superset
linking. Gated by COMPOSE_ON (1/0) for ablation. Pure Zag, no Python.

## Kill bar verdicts

### K-C1 (operator fires): PASS

On `compose_fixtures/disambig.txt`, the dump contains 3 active reason=6
concepts:
- C10: {color=red, kind=block}, members {e2}
- C11: {shape=round, kind=block}, members {e3}
- C28: {shape=square, color=blue}, members {e4}

Each is the union of two pre-existing concepts' intents. White-box verified.

### K-C2 (utility): FAIL

`Q e5 | kind` (expected roller): WITHHOLD with COMPOSE_ON=1 (0/1).
The composed concepts do not enable the held-out inference. The probe
fails identically to baseline.

### K-C3 (ablation): N/A per prereg (K-C2 failed); confirmed no effect

COMPOSE_ON=0 (all else identical): 0/1 WITHHOLD.
COMPOSE_ON=1: 0/1 WITHHOLD.
Removing the operator changes nothing. The composed concepts are not
load-bearing for this probe.

### K-C4 (precision, no harm): PASS

All six committed fixtures unchanged (k5 4/4, k2 5/5, k4 2/2, k3_merge 5/5,
mini_world 8/8, ctx_test 3/3). Zero reason=6 concepts fired on any of them.
On disambig.txt, 3 reason=6 concepts (< 12 bound). No score degradation
anywhere. Determinism: 3x byte-identical outputs.

## Interpretation

H-COMPOSE is KILLED as a utility claim. The operator works mechanically
(K-C1) but provides no inference capability beyond the existing machinery
(K-C2, K-C3).

This matches the redundancy argument recorded in the prereg:

1. The composed concepts that fired ({red,block}, {round,block},
   {square,blue}) are unions the existing SPLIT/FORM machinery also
   produces (as reason=2 children). COMPOSE merely created them earlier
   (as reason=6) in the fixpoint. They carry no novel evidence.
2. For the disambiguation probe, the needed conjunction concept {red,round}
   already exists (as e5's leaf artifact). COMPOSE correctly declined to
   duplicate it (exact-match non-redundancy). The failure is inference-side:
   sibling evidence accumulates globally across candidates, so the correct
   specific evidence (via {red,round}) is vetoed by conflicting less-specific
   evidence (via {red} and {round}).
3. In general, a crisp union-intent concept cannot enable a novel held-out
   Step-1 inference (target-in-intent would imply the fact was taught), and
   for Step-2 (sibling) any union with 2+ evidence-carrying members is
   already covered by FORM/MERGE/subset-linking over the members' leaves.

## What this means

Deliberate union-intent composition is not the missing operator in FDCR.
The architecture already recruits every useful union via FORM (intersection
parents), MERGE (identical intents), leaf artifacts, and subset linking.
The genuine gap exposed by the disambiguation probe is in the inference
procedure (most-specific evidence should not be vetoed by less-specific
conflicting evidence), not in concept formation.

This is an informative negative result: it rules out a natural hypothesis
about what FDCR lacks, with a mechanism-level explanation, rather than
merely reporting a failed test.

## Scope

- Claim is bounded to union-intent COMPOSE in FDCR's feature-based
  architecture. Other composition semantics (invented features, relational,
  graded) were not tested.
- NOT L3 evidence. The operator enumerates unions; it does not invent
  representations.
- The inference-side gap (most-specific preference) is noted as future
  work, not claimed here.

## Raw outputs

- `rep_v2/compose_fixtures/disambig.txt` (frozen fixture)
- `rep_v2/raw_outputs/COMPOSE_DISAMBIG_RAW.txt` (with COMPOSE_ON=1)
- `rep_v2/raw_outputs/COMPOSE_ABLATED_RAW.txt` (COMPOSE_ON=0)
- `rep_v2/raw_outputs/COMPOSE_KC4_RAW.txt` (six fixtures, both binaries)

## Commits

- 271ec362b: prereg FROZEN (this result's bar)
- (this commit): implementation + result + raw outputs
