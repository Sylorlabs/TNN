# PREREG AMENDMENT 1: R4b/R4c World Size 3-wide to 2-wide

Date: 2026-10-02. Worker: H-FALLBACKFIX-1.
Amends: PREREG.md (commit 9d1adc2f6), sections 4 and 5 (K2, K4, K5).

## Change

R4b and R4c worlds change from 3-wide to 2-wide layered graphs:

- R4b: 2 nodes per layer, 7 layers (L0..L6), 28 facts, 28 single link
  MAPs trained via direct t2_trial on the layered facts. Unreachable
  goal 99999.
- R4c: same 28, correct path (a=1,b=1) MAPs trained last, plus final
  hop 9601 -> 9008 on rel 400 (1 MAP). Reachable goal 9008 via
  8 segments.
- K2 timeout: 600s per test (unchanged). K4/K5 timeout: 300s
  (unchanged).

## Rationale

The 3-wide design (63 facts + 63 MAPs) does not fit the 1024 node
workspace. Measured: one fact plus one 1-link MAP costs 15 nodes;
63 facts + 63 MAPs = 945 nodes, leaving 79 nodes margin. Training
the 3-wide world hit the eviction latency cliff (AGENTS.md base
capacity lesson: at capacity allocs trigger full arena evict scans,
~0.8s each) and stalled; the 63rd MAP failed with ans=-2.

The 2-wide world (28 facts + 28 MAPs = 420 nodes) fits comfortably
and preserves the exponential blowup that K2/K4/K5 discriminate:

- UNFIXED: every 1-link MAP is fallback admitted at every node
  (plen 2 matches any 1-link path), so branching = 28 per node,
  28^8 paths: non terminating.
- REPAIRED: only walk compatible MAPs admitted, branching = 2
  per node, 2^8 = 256 paths: terminates in seconds.

The kill (non termination vs termination) and the repair
(relation relevant branching) are identical; only the absolute
width changes. No kill bar is weakened: K2 still requires
non termination within 600s, K4/K5 still require termination
within 300s with correct answers.

## Commit order

This amendment is committed before any R4b/R4c test is executed.
No 3-wide R4b/R4c result is reported (the 3-wide probe never
completed training; no verdict was drawn from it).
