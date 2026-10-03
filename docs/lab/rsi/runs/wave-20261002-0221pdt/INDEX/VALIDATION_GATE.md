# VALIDATION_GATE.md - INDEX lane, wave-20261002-0221pdt (Part B, gate)

Governing bar: PREREG_INDEX_REPRO.md B3 (frozen).

## The gate

Two pure-read validators in `work/sc_patch_fixed.zag`. "Pure read"
means: no `hs` writes, no counter touches, no state mutation of any
kind. The gate observes; it never changes what it validates.

`idx_validate(W)` -> 1 (ACCEPT) / 0 (REJECT). The MAP plen-bucket
index is healthy iff, for each plen bucket 2..5 (index node fields
20/24/28/32), every member of the intrusive field-12 list:
  - is a node id in [0, NN),
  - is live (field 36 == 1),
  - has tag 20 (MAP node),
  - has a chain root in [0, NN) whose `rb_chain_plen` equals the
    bucket plen,
and every next pointer is -1 or a node id in [0, NN), and no list
contains a cycle (Floyd tortoise-and-hare; a step cap of NN as
backstop).

`fidx_validate(W)` -> 1 / 0. The FACT subject index is healthy iff
the 4 chained tag-40 FACT index nodes exist exactly (live, tag 40,
chain of length 4 ending in -1) and every one of the 24 bucket
chains is acyclic with members in range, live, tag 1, and clean
next pointers. The node chain is validated BEFORE any bucket head
is read through it, so the head lookup itself cannot panic on
corrupt node state.

Production wiring (mandatory before use):
  - `rebind_try_idx` calls `idx_validate` as its first statement;
    on REJECT it returns `rebind_try_lin(...)`.
  - `t2_gather` / `t2_lu_first` consult `fidx_validate` at the bit2
    dispatch; on REJECT they use the linear variants.
There is no production path that touches the MAP or FACT index
without its gate passing first.

## Test matrix (real structures)

`work/gate_driver.zag` assembled with the base ranges and the fixed
patch (`work/gate_full.zag`, 2255 lines), compiled with the pinned
znc (exit 0), run 3x. Each case builds a fresh 8192-node workspace,
promotes real MAPs, applies one corruption shape, and checks the
gate verdict.

  G1-healthy      idx_validate -> 1  PASS   (3 plen-5 MAPs, intact)
  G1-factempty    fidx_validate -> 1 PASS   (no FACTs filed: empty is healthy)
  G2-cycle        idx_validate -> 0  PASS   (self-loop on bucket head)
  G3-nonmap       idx_validate -> 0  PASS   (live FACT node prepended)
  G4-oobnext      idx_validate -> 0  PASS   (head next -> 9999, out of range)
  G5-plenmismatch idx_validate -> 0  PASS   (plen-3 MAP spliced into plen-5 bucket)
  G6-facthealthy  fidx_validate -> 1 PASS   (60 FACTs filed, intact)
  G7-factcycle    fidx_validate -> 0 PASS   (self-loop on a FACT bucket head)

3/3 runs byte-identical (sha256
f0ccd99c5f1ff334f168aaa8d9fa7d7a682b85743e005f763127faa8d0cdf96e),
exit 0, no panics on any corrupt shape: the gate rejects without
ever indexing out of bounds itself.

B3 HOLD: G1 ACCEPT; G2-G6 REJECT (G7 is the FACT-side analogue of
G2); all 3/3 deterministic.

## Design notes

- Strict gate, lenient walker: the gate rejects any deviation
  (including an OOB next pointer, which the walker would merely
  treat as list end). Trust decisions are strict; safety floors are
  lenient. See FIX.md for the rationale.
- The plen-match check makes the gate sensitive to the filing
  invariant, not just pointer hygiene: a structurally valid MAP in
  the wrong bucket is REJECT. This is the check that catches the
  "silent wrong-bucket" corruption class the red team did not test.
- Empty buckets and empty FACT chains are healthy (return 1): the
  gate must not reject a freshly initialized or fully evicted index.
- The gate does not repair: repair policy (rebuild vs evict vs
  ref file) is a separate decision. Fail-closed (fall back to
  linear) is the safe default.

## Red-team self-review (gate)

- Could the gate false-REJECT a healthy index at scale (eviction
  staleness)? Possibly: if eviction reuses a MAP node's slot, the
  bucket holds a stale id and the gate rejects. That is the CORRECT
  behavior (the index IS corrupt then), and the fallback keeps
  answers right. But it means at sustained scale with eviction, the
  index could be rejected often, degrading to linear. The honest
  fix is index-coherent eviction (recorded as follow-up, not built
  here). The B4 byte-identical result shows no such staleness in
  the current benchmark worlds.
- Could a corrupt shape pass the gate? The gate checks id range,
  liveness, tag, chain-plen match, pointer range, and acyclicity.
  A shape passing all six yet steering a wrong answer would need a
  live tag-20 MAP with a valid plen-q chain that is nonetheless the
  "wrong" MAP for the bucket: but bucket membership has no
  correctness semantics beyond plen (candidates are verified
  structurally downstream), so no wrong answer can result. The
  residual risk is performance (duplicate members), not correctness.
- The gate itself walks attacker-influenced pointers; every read is
  range-checked before use (the `raw`/`fraw` strict steps, the node
  pre-validation in `fidx_validate`). The G4 case is the direct
  test that an OOB pointer is rejected, not followed.
- `z_alloc(16)` in `fidx_validate` allocates per call; negligible
  (16 bytes), but a per-query allocator call is the kind of thing
  the epoch-cache refinement would also remove.
- What would falsify the gate: any corrupt shape from the matrix
  (or a new one) that returns ACCEPT, or any healthy state that
  returns REJECT. The matrix covers the red-team shapes plus
  plen-mismatch and FACT-side corruption; B4 covers healthy-state
  acceptance at full scale.
