# PREREG H-UNIFIED3: Compositional Repair for H-UNIFIED2 Red-Team Downgrades

**Date:** 2026-09-29
**Status:** FROZEN. No implementation exists yet. Any implementation commit must strictly descend from this commit.
**Base:** `unified2_learn.zag` (H-UNIFIED2, commit 0eb7677fe), copied verbatim then repaired. `clearn` revision semantics preserved; only its return type changes (void -> i32 status code). No logic change to the learning path.
**Target:** `unified3_learn.zag` (new file; `unified2_learn.zag` untouched).
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED2 SURVIVES (12/12) but was DOWNGRADED by independent red team
(ADVERSARY_REPORT_H_UNIFIED2.md, prereg 4d9b05302, report 9f451fa42).
Two downgrades, no kill. The frozen 12/12 bars still pass; the downgrades
bound the GENERALIZATION of the repair.

- **X-U2-2a (poison-first ordering):** The coherence gate protects ACTIVE
  rules with no provenance. Poison arriving first becomes the "verified"
  knowledge; truth arriving later through the unlabeled stream is
  quarantined permanently. Order-dependent first-writer-wins, not
  veracity-dependent protection.
- **X-U2-2b (capacity flood):** The 16-slot causal store fills with
  coherent junk; later legitimate novel learning is silently dropped by
  `clearn`'s full-store early return while the handler reports success
  (counts episodes handed to `clearn`, not rules stored).

X-U2-1 (quarantine bypass) and X-U2-3 (AMBIGUOUS gaming) PASSED: no
bypass exists in truth-first order; the gate is sound for its frozen
threat model.

## Repair design (frozen)

### Repair A: explicit authoritative revision channel (X-U2-2a)

Trust distinction, enforced structurally:

- The unlabeled stream stays UNTRUSTED: coherence-gated,
  append/corroborate-only, exactly as in H-UNIFIED2. Truth arriving late
  through the stream is still quarantined. This is documented, not
  hidden.
- A new explicit channel carries AUTHORITATIVE revisions: input lines
  prefixed with `!` (byte 33) route to new code 6 = CAUS_REVISE when the
  remainder parses as iii>ii episodes (nseg>=2, all_ep==1).
  `handle_caus_revise` bypasses the coherence gate and calls `clearn`
  directly, whose native revision semantics (contradicting episode marks
  the old rule CONFLICTED; a repeated episode learns the corrected rule)
  then apply.
- `!` on a non-causal line routes WITHHOLD (0) with an explicit reason;
  the marker never changes procedure/bridge routing.
- This answers "whoever reaches the stream first wins forever": the
  stream is first-writer-wins by design (untrusted), but the explicit
  channel is the operator/researcher asserting authority and CAN correct
  poison. Veracity now has a path; it is just not the unlabeled path.

### Repair B: honest capacity accounting + explicit capacity policy (X-U2-2b)

- `clearn` returns an i32 status code (logic unchanged):
  - 1 = new rule stored
  - 0 = corroborated (matched ACTIVE rule, no conflict, no state change)
  - 2 = conflict marked (old rule set CONFLICTED; revision step)
  - -1 = dropped (store full, no slot)
- `handle_caus_learn` reports stored / corroborated / quarantined /
  dropped separately, returns the STORED count (episodes that changed
  store state), and emits an explicit `STORE FULL` warning per dropped
  episode. A cumulative dropped-episode counter is kept at W[DCOUNT()]
  (new address 65008), mirroring QCOUNT().
- `handle_caus_revise` uses the same accounting (minus quarantine).
- Explicit capacity policy (frozen): REFUSE-WITH-WARNING. On a full
  store, novel rules are refused with an explicit warning; verified
  knowledge is never evicted; queries on dropped states withhold. Silent
  eviction would be a U-A2-class integrity violation. A real eviction /
  consolidation policy for the continuing learner is future work
  (H-MEM lane owns memory strategy).

### What is NOT changed

- The coherence gate (`caus_coherent`), the router (except the `!`
  prefix branch), the procedure/bridge stores, the AMBIGUOUS code 5,
  subset direct discovery, and the query path are byte-identical in
  behavior to H-UNIFIED2.
- All 12 original frozen tests must pass unchanged (K-U3-3).

## Frozen kill bars

### K-U3-1: poison-first recovery via the explicit channel (X-U2-2a)

Fresh workspace W3 (truth rules from the main tests must not interfere):

1. Route check: `route_line("!1,0,0>1,0;1,0,0>1,0")` returns 6
   (CAUS_REVISE).
2. Stream poison: `handle_caus_learn(W3,"1,0,0>9,9;1,0,0>9,9")` ->
   stored=1 (first episode stores, second corroborates),
   `cpredict(W3,1,0,0)` yields s1=9 (poison is ACTIVE).
3. Stream truth (late): `handle_caus_learn(W3,"1,0,0>1,0;1,0,0>1,0")` ->
   stored=0, quarantined=2 (gate unchanged; documents the stream's
   order-dependence honestly).
4. Explicit revise: `handle_caus_revise(W3,"!1,0,0>1,0;1,0,0>1,0")` ->
   stored=2 (first marks poison CONFLICTED, second learns corrected
   rule); `cpredict(W3,1,0,0)` yields s1=0; active rule count is 1
   (poison CONFLICTED, corrected ACTIVE).
5. Stream truth now corroborates:
   `handle_caus_learn(W3,"1,0,0>1,0;1,0,0>1,0")` -> stored=0,
   quarantined=0 (coherent with the corrected rule).

PASS iff all five hold. KILL (of the repair claim) iff the explicit
channel cannot correct poison-first state, or the route code is wrong.

### K-U3-2: capacity honest accounting (X-U2-2b)

Fresh workspace W4:

1. Fill: 16 distinct coherent novel states
   ("10,0,0>0,1;11,0,0>0,1" ... "25,0,0>0,1" as 2-seg lines, 8 lines)
   via `handle_caus_learn` -> active rule count is 16 (CR_MAX).
2. Legitimate novel: `handle_caus_learn(W4,"99,0,0>0,1;99,0,0>0,1")` ->
   returns 0 (stored), dropped delta is 2 (DCOUNT), active stays 16,
   `cpredict(W4,99,0,0)` withholds (returns 0).
3. The handler emission contains an explicit store-full warning
   (checked by the dropped counter, which only increments on -1).

PASS iff all hold. KILL iff the handler reports stored>0 for dropped
episodes, or the dropped counter does not move, or a confident wrong
answer is returned for the dropped state.

### K-U3-3: no regression

All 12 original H-UNIFIED2 frozen checks pass unchanged on the main
workspace: K-U1, K-U2a, K-U2b, K-U2c, K-U3, K-U4a, K-U4b, K-U5, K-A,
K-U2-1, K-U2-3a, K-U2-3b. The main() body keeps these blocks verbatim;
the new tests run on separate workspaces (W3, W4) and new assertions.

Note on K-U2-1 under the new accounting: the interference replay
expects `ncommitted==0`; the handler now returns the STORED count, and
quarantined episodes never reach `clearn`, so stored=0 still holds.

### K-U3-4: determinism

Three full runs of the final binary are byte-identical (cmp). The md5
of the three runs is recorded in the result doc.

## Honest limitations (frozen, carried forward)

1. The unlabeled stream remains first-writer-wins. The explicit channel
   is the only correction path; there is no autonomous veracity
   judgment. A genuinely-correct stream revision is still quarantined.
2. Capacity policy is refuse-with-warning, not eviction. A continuing
   learner will eventually refuse all novel causal learning once the
   16 slots fill. This is honest but not a solution.
3. The `!` marker is a researcher/operator affordance, not a learned
   trust signal. The learner does not infer authority.
4. Procedure/bridge stores have no analogous explicit revision channel
   in this change (causal only).

## Commit plan

1. This prereg (frozen).
2. Implementation: `unified3_learn.zag` + `UNIFIED3_RAW_OUTPUT.txt`
   (raw evidence) + `UNIFIED3_RESULT.md`.
3. No amendment unless a harness bug is found; any amendment will be
   transparent and will not change kill criteria.

## Classification sought

Bounded L2 integration repair, not L3. Closes the two H-UNIFIED2
downgrades at the composition layer with explicit, tested mechanisms.
