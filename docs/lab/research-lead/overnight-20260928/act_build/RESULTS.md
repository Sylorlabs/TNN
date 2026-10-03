# ACT Build Results

Date: 2026-09-30. Worker: ACT Builder (resumed with amended specs).
Status: ACT-BUILD-COMPLETE.

## Governing specs

- PREREG_ACT.md (51a818141): the five-step generic ACT operation.
- Integration amendments A1-A12 (62e5ebb9f), APPROVED:
  A3 (evidence-bid selection), A4 (POLICY_ROOT + context ring),
  A8 (utility remap to evidence edges), A11 (signed bid),
  A12 (reserved node addresses 0/1, WRITE to set).
- ISA boundary ruling (0525377f3): {EQ,ADD} approved as ISA
  primitives; no regularity detectors in core.

## Implementation

`act.zag` (pure Zag, ~700 lines). Components:

- Node store: (type_tag, ref[4], payload[4]) per CLA-2, u8-backed.
- Edge store: (from, to, etype), CLA-2 vocabulary.
- A12: POLICY_ROOT = node 0 payload[0], set via ordinary WRITE.
- A4: 4-slot event-context ring (core bookkeeping).
- A3/A11: signed bid = SUPPORTS/USE/CONFIRMS (+1),
  CONTRADICTS (-1).
- `act_event`: the five-step read protocol. Zero branches on
  world, task, or relation identity (verifiable: the function
  takes only stores + context, no world/task parameters).
- Learner-side scaffolding: mk_goal, mk_guide, mk_uncert,
  derive_d1 (backward-chain reference derivation), learn_confirm
  / learn_contra (A8 evidence-edge remap), evict_to_cap
  (capacity-pressure stand-in for the CLA-2 retention lane).

Built with pinned `znc_linux_x86_64_abed8aa1`. Warnings only
(A0102 ignored-return-value notes); zero errors.

## Test results (./act_bin all): 24/24 PASS

- P-ACT3 (null policy): POLICY_ROOT null -> CHOICE 0. PASS.
- P-ACT1 (planning): W7-class s1->s2->s3; D1 derived 3 guides;
  ACT emits 10/11/10 by state. The constant-0 baseline would
  score 0/4 here. PASS.
- P-ACT2 (inquiry): uncertainty-anchored guide fires 20 when
  the uncertainty record is live; decoy context fires 21;
  unrelated context fires 0. act_event takes no positional
  input, so the swap test is satisfied structurally. PASS.
- P-ACT4 (ablation): deleting ACTION-GUIDEs -> constant 0;
  deleting the GOAL (policy root dead) -> 0, no hallucination;
  fact nodes remain readable (recall intact). The capability
  is in the structures, not the handler. PASS.
- P-ACT5 (generality): W7-class and W6-class scenarios run
  through the identical act_event. PASS.
- P-ACT6 (memory prerequisite): under capacity pressure,
  unevidenced guides (bid 0) are evicted -> ACT degrades to 0;
  guides with USE/CONFIRMS evidence (bid 2) survive the same
  pressure -> ACT holds at 10. The retention mechanism, not
  the handler, decides. PASS.

## Falsification status

- F-ACT1: not triggered (correct policies produce correct actions).
- F-ACT2: not triggered (no positional input exists to correlate with).
- F-ACT3: not triggered (zero per-world branches; verified by inspection).
- F-ACT4: not triggered (no guides -> no action; core smuggles nothing).

## One-System Rule accounting (measured)

- Cognition source lines added: ~700 (act.zag, incl. test scaffolding;
  the act_event core is ~60 lines).
- New hardcoded semantic cases: 0.
- New modes: 0. New bridges: 0. New task-specific handlers: 0.
- New edge types: 0. New state formats: 0.
- Learner-state structures: GOAL, ACTION-GUIDE, UNCERTAINTY node
  conventions (workspace content, learner-owned).

## Notes

- The eviction used in P-ACT6 is a test stand-in (lowest signed
  bid), not the CLA-2 three-step routine; that is the CLA-2
  builder's lane.
- derive_d1 is a reference derivation (per the prereg, D1/D2 are
  examples, not frozen algorithms).
- No sealed FW1-FW9 files accessed at any step.
