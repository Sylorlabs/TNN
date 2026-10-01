# Shared Consequence Substrate: Design and Build

## 1. Problem

Micah Q4 (increased priority): test whether ONE substrate can drive
action-policy learning, withholding, abandonment, retention, search
strategy, and revision strategy. Avoid separate subsystem
implementations where one general mechanism explains them.

Status quo ante:
- Node2-v2 (0988839a2): K-H3 PASS, but policy lives in a PRIVATE
  tag-40 node (history slots f8/f12/f16, default f20). Narrow
  counter, does not compose.
- Decline gate: RETIRED as architecture mechanism (Micah ruling).
  Its signal was a proxy for duplicate allocation. Keep DEDUP.
- Substrate consolidation (1ed3f5a6b): decline gate migrated onto
  shared substrate (tag-61 records). EMERGES. But only ONE consumer
  demonstrated; spec 9.4 (S2 falsification) remains open.

This wave: migrate Node2-v2 policy learning onto the SAME substrate
store, and test withholding as a second consumer. If both work from
one store with no private tallies, the S2 falsification test moves:
two consumers, one mechanism, zero new storage machinery for the
second.

## 2. The substrate store (reused, not rebuilt)

The consolidation built generic machinery (sc_substrate.zag). This
wave reuses it verbatim:

- `sub_find(W,kt,ka,kb)`: keyed lookup over tag-61 records.
- `sub_get(W,kt,ka,kb)`: get or create.
- `sub_note(W,kt,ka,kb,success,mode,src,cost,create)`: one write
  path for all consumers (spec 4.2).
- `sub_consec(W,kt,ka,kb)`: read consec_fail, 0 when no record.

Record layout (tag 61), unchanged:
- f4: key_type (1 PURSUIT, 2 STRATEGY)
- f8: key_a (s for PURSUIT; action id for STRATEGY)
- f12: key_b (r for PURSUIT; 0 for STRATEGY)
- f16: consec_fail (reset to 0 on success)
- f20: attempts
- f24: successes
- f28: src packed (taught/observed/self, saturating)
- f32: life packed (state, last_mode F1-F7, cost_nodes saturating)

New in this wave: `sub_best_action(W)`  -  argmax over STRATEGY
records by successes, tie broken by smaller action id, default 30
when no records exist. This is the policy READ path. It is generic:
it reads the shared store, knows nothing about Node2-v2.

## 3. Behavior 1: action-policy learning via STRATEGY records

Node2-v2 convergence: the private policy node is deleted. In its
place:

Write path (`ev_observe_aw`, adapted from n2v2):
- When the world reveals action a_w >= 0 with an observation for
  (s,r) that has an open uncertainty:
  - Supersede the uncertainty and its guide (as n2v2).
  - `sub_note(W, STRATEGY, a_w, 0, success=1, mode=0,
    src=OBSERVED, cost=0, create=1)`.
- Each revelation is one success write for the revealed action.
- Source tag is OBSERVED (world-sourced), never self.

Read path (`miss_inquire`):
- `act = sub_best_action(W)` (default 30).
- Guide created with this action, as n2v2.

Why argmax-successes instead of "3 consistent":
- Node2-v2 required exactly 3 consistent revelations differing from
  default. The threshold is researcher-set.
- Argmax eliminates the threshold: the policy is whichever action
  has the most world-revealed successes. One revelation of 45 when
  30 has zero successes flips the policy; this is faster but also
  more revisable.
- Revision without a reversal case: if the world later reveals 30
  repeatedly, record(30).successes overtakes record(45), and the
  policy returns to 30. No dedicated logic.
- Noisy evidence: a single 46 among 45s gives record(46).successes=1
  vs record(45).successes=3; argmax stays at 45. Graceful.
- This directly addresses Micah Q1 (threshold plasticity, revision,
  noisy evidence) as emergent properties, not special cases.

Honest difference from n2v2: the flip timing changes (argmax flips
earlier than 3-consistent). The qualitative behavior (world evidence
changes the policy) is preserved and generalized.

## 4. Behavior 2: withholding via PURSUIT records

The retired decline gate is NOT rebuilt. What is built is a
substrate consumer that reads PURSUIT records:

Write path (`ev_query`, adapted from consolidation):
- Activate hit: `sub_note(PURSUIT, s, r, success=1, ..., create=0)`
  (no record on answers from memory, spec 4.1).
- Trial or bootstrap success: `sub_note(PURSUIT, s, r, success=1,
  cost=verifies_spent, create=1)`.
- Trial and bootstrap both fail: `sub_note(PURSUIT, s, r,
  success=0, mode=F6, cost=verifies_spent, create=1)`.
- Withheld queries do NOT write (the gate's caution must not
  inflate the count it reads, spec 5.1).

Read path (`ev_query`, before trial):
- `cf = sub_consec(PURSUIT, s, r)`.
- If `cf >= WITHHOLD_N`, return WITHHOLD (-3) without running trial.
- WITHHOLD_N = 3, honestly labeled researcher-set scaffolding
  (carried over for comparability; learner-owned thresholds are
  future work per spec section 8).

Key architectural point: this is the SAME `sub_note` and
`sub_consec` as Behavior 1. No private tally. No separate engine.
The withholding decision and the policy decision read different
keys (PURSUIT vs STRATEGY) from one store.

## 5. The compute-vs-state experiment

Micah: "Test whether deliberate stopping provides COMPUTE savings
beyond dedup's STATE savings."

Dedup (296fd79cb) saves NODES by reusing duplicate UNCERTAINTY
nodes, but the trial still RUNS on every miss (dedup is in
miss_inquire, after trial). Dedup saves state, not compute.

Withholding via substrate skips the trial entirely. It should save
VERIFIES (compute), not just nodes.

Experiment (DYN-1-like battery, repeated misses on same keys, trial
always fails because r=99 is never taught):

- Arm A (baseline): frozen ev_query. No dedup, no substrate.
- Arm B (dedup): dedup gate in miss_inquire. Measures state
  savings; verifies should equal baseline.
- Arm C (substrate): substrate ev_query with withholding. Measures
  compute savings; verifies should drop after consec_fail hits 3.

Predictions:
- Nodes: B < A (dedup saves state). C < A (withholding saves state
  too, fewer trials means fewer allocations).
- Verifies: B = A (dedup does not save compute). C < A (withholding
  saves compute by skipping trials).
- If C.verifies < B.verifies: withholding provides compute savings
  beyond dedup's state savings. CONFIRMED.
- If C.verifies = B.verifies: withholding adds nothing over dedup.
  INFORMATIVE NEGATIVE.

## 6. Unification test

Both behaviors must work in ONE binary (Arm C):
- Experiment A (policy): Node2-v2 3-phase scenario via
  ev_observe_aw. Phase 1: a_w=30 revelations. Phase 2: a_w=45
  revelations. Phase 3: miss, check guide action = 45.
- Experiment B (withholding): DYN-1 battery. Check verifies drop.

If both pass in one binary with one substrate store, the
unification claim holds: one mechanism, two cognitive effects.

## 7. One-System Rule audit (design)

- New modes: 0.
- New bridges: 0.
- New handlers: 0.
- New semantic cases: 0.
- New node tag: 61 (storage only, reused from consolidation; no
  production function branches on tag 61 to alter cognition).
- New edge types: 0.
- The substrate is infrastructure (keyed store), not a cognitive
  subsystem. Consumers are read rules, not engines.

## 8. Standing metrics (design-time)

- RESEARCHER-OWNED: substrate record format (reused), WITHHOLD_N=3
  (scaffolding), sub_best_action tiebreak rule, argmax policy rule.
- LEARNER-OWNED: consec_fail values, successes per action, which
  action the policy selects, whether to withhold per key.
- The policy VALUE (45) is learner-owned (from world revelations).
  The policy RULE (argmax) is researcher-owned. This is the honest
  boundary.
