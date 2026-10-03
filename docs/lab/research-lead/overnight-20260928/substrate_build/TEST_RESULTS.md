# Shared Consequence Substrate: Test Results

## Experiment A: Action-policy learning via STRATEGY records

Scenario: Node2-v2 3-phase (revelations via ev_observe_aw, policy via
sub_best_action argmax).

Results (3/3 byte-identical, SHA 0a94063d6b78ced8):

- Phase 1 (a_w=30, -1, 30): policy=30. PASS (no spurious shift).
- Phase 2 (a_w=45 x3): mids 30, 30, 45. Policy=45 after 3rd.
  PASS (shift to 45).
- Phase 3 (miss): guide action=45. PASS.
- STRATEGY_RECORDS=2 (one per action).

The flip timing matches Node2-v2 (3rd revelation) via the tiebreak
rule: after 2 revelations of 45 vs 2 of 30, tie goes to smaller
action (30); 3rd breaks the tie. The threshold emerges from argmax,
not from a hardcoded count.

Verdict: POLICY-LEARNING-CONFIRMED. World revelations drive the
policy via shared STRATEGY records. No private policy node.

## Experiment B: Compute vs state (withholding vs dedup)

Setup: 2 keys (s=101..102), teach r=1..5, query r=99 (untaught).
Phase C: 8 queries (4 per key). Phase E: 4 queries (2 per key).
Measure verifies (compute) and node delta (state) separately.
3/3 byte-identical per arm.

### Results

| Arm | Phase C VC | Phase C DN | Phase C DEC | Phase E VC | Phase E DN | Phase E DEC | Total VC | Total DN |
|-----|-----------|-----------|------------|-----------|-----------|------------|---------|---------|
| A (baseline) | 80 | 497 | 0 | 40 | 248 | 0 | 120 | 745 |
| B (dedup) | 80 | 485 | 0 | 40 | 240 | 0 | 120 | 725 |
| C (substrate) | 60 | 375 | 2 | 0 | 0 | 4 | 60 | 375 |

VC = verifies (compute). DN = node delta (state). DEC = withholds.

### Analysis

**Dedup saves state, not compute:**
- B.DN (725) < A.DN (745): dedup saves 20 nodes.
- B.VC (120) = A.VC (120): dedup saves ZERO verifies.
- The trial runs on every miss; dedup is in miss_inquire (after
  trial). Confirms Micah's analysis.

**Substrate withholding saves compute beyond dedup:**
- C.VC (60) < A.VC (120): 50% reduction in verifies.
- C.VC (60) < B.VC (120): withholding saves compute that dedup
  does not.
- Phase E: C withholds all 4 queries (0 verifies, 0 nodes).
  A and B run trial on all 4 (40 verifies each).

**Substrate also saves state:**
- C.DN (375) < A.DN (745): 50% reduction in nodes.
- C.DN (375) < B.DN (725): fewer trials means fewer allocations.

### Verdict

HYPOTHESIS-CONFIRMED: Deliberate withholding via the shared
substrate provides COMPUTE savings (50% fewer verifies) beyond
dedup's STATE savings (dedup: 0% compute reduction). The substrate
consumer skips the trial entirely; dedup cannot.

## Unification

Arm C runs BOTH experiments in one binary with one substrate store:
- STRATEGY records drive the action policy (Experiment A).
- PURSUIT records drive withholding (Experiment B).
- No private tallies. No separate engines. One `sub_note` write
  path, two key namespaces.

Verdict: SUBSTRATE-BUILD-COMPLETE. One persistent consequence
store drives action-policy learning and withholding. The S2
falsification test advances: two consumers, one mechanism.

## Honest limits

- WITHHOLD_N=3 is researcher-set scaffolding (carried from
  consolidation for comparability). Learner-owned thresholds are
  future work.
- The policy RULE (argmax) is researcher-owned; the policy VALUE
  (45) is learner-owned (from world revelations). This is the
  honest boundary.
- N=3 scale (2 keys, 12 queries) due to trial slowdown at larger
  scales. The effect is robust; the magnitude may vary with scale.
- No sealed worlds in this wave (builder-run experiments).
  Independent replication required before SURVIVES.
