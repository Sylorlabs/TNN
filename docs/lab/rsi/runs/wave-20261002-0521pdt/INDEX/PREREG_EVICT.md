# PREREG_EVICT.md - INDEX-EVICT lane, wave-20261002-0521pdt

Frozen: 2026-10-02 (commit alone, before any implementation file).
Status at freeze: PROPOSED (unexecuted). No sealed results below were
observed before freezing. Exploratory probes (clearly labeled, in
`work/probe/`) informed the design and the bar; the sealed eval below
is a fresh build plus fresh runs.

Governing context: wave-20261002-0221pdt INDEX lane. Part A CONFIRMED
the 1393x indexed scan reduction (canonical output hash
`eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d`).
Part B FIX-VERIFIED the index-cycle crash fix plus the validation gate
(`idx_validate` / `fidx_validate`; gate REJECT routes to the linear
fallback, preserving availability). Explicitly out of scope there and
recorded as follow-up: the eviction path that CREATES stale bucket
entries. That is this wave.

## The defect (two coherence violations, one operation)

`evict_node` (base) kills a node (field 36 = 0) and removes its edges
but never touches the MAP plen-bucket index (tag-40 index node, fields
20/24/28/32, intrusive field-12 lists) or the FACT subject index
(24 buckets over 4 chained tag-40 nodes). Exploratory probes in this
wave established that eviction breaks index coherence in TWO ways:

(V1) Stale membership. The victim IS a bucket member (MAP tag 20 or
FACT tag 1). Its id stays in the bucket, dead. The gate rejects
(dead member); the index degrades to the linear fallback.

(V2) Chain invalidation (found 2026-10-02, diag2 probe). The victim is
a chain member (tags 902/101/102: literals, frames, procedure steps).
`rb_chain_plen` walks MAP chains as 102 -f12-> 101 -seq-> 102...; the
victim's death (plus evict_node's edge cleanup) breaks the walk, so a
LIVE indexed MAP's current chain plen no longer equals its bucket
(diag2: `VIOL B5 m=31 kind=4 ... gotplen=-1` after evicting node 18,
tag 101, from MAP 31's chain with root 17). The bucket list has no
stale entry, yet the gate correctly rejects (plen mismatch) and the
index again degrades to linear.

Both are production-path: `alloc_node` calls `evict_node` under memory
pressure, and direct `evict_node` calls are the same function. V2 fires
within ~4 natural evictions in the probe storm.

## Mechanism: index-coherent eviction (frozen design)

One hook, `idx_on_evict(W,n)`, called from `evict_node` after the
victim is chosen and BEFORE it is marked dead (tag still intact).
Coherence invariant maintained: (A) every bucket member is a live,
correctly-tagged node; (B) every MAP bucket member's current chain
plen equals its bucket. Dispatch on the victim's tag:

- t == 20 (MAP): unlink the victim id from all 4 MAP plen buckets
  (intrusive field-12 splice, new head written back); clear the MTF
  winner cache (`ix` field 12) if it names the victim.
- t == 1 (FACT): unlink the victim id from all 24 FACT bucket chains.
- t in {902,101,102} (possible chain member): unlink every indexed MAP
  whose chain contains the victim (chain walk mirrors `rb_chain_plen`
  exactly, seq edges via a per-eviction table built from one edge scan);
  clear the MTF cache if it names an unlinked MAP. The MAP stays live
  for the linear path; it is just no longer indexed under a plen that
  no longer describes it. Refiling under a new plen is rejected as
  dishonest: the chain is broken, not shortened.
- Other tags: MTF-cache check only.

All walks are cycle-safe and OOB-safe (step caps, range guards, the
`idx_bnext` discipline from Part B), so the hook can never panic even
on an already-corrupt list. Counters (node-0 fields 4/8/12: MAP
membership unlinks, FACT membership unlinks, chain-break unlinks) are
never read by the Part A driver, so the hook is output-silent there.

Source delta (frozen): exactly 1 line in the lane's base copy
(`idx_on_evict(W,best);` inside `evict_node`) plus the hook functions
in the lane's patch copy. New modes: 0. New bridges: 0. New handlers:
0. New semantic cases: 0. The index maintains its own membership
invariant at its existing mutation point (one-system compliant).

Metric moved: post-eviction gate acceptance (V1+V2 storms): OLD 0%
(expected: every storm run shows REJECT) to NEW 100%; post-storm
indexed query cost stays at indexed levels instead of degrading to the
linear fallback; query answers identical.

Cost (frozen expectation, measured in the sealed runs): per eviction,
O(indexed MAPs x chain length) for chain victims (one 16384-edge scan
for the seq table plus short walks; negligible next to evict_node's
own ~1e9-op selection scan), O(bucket lengths) for member victims.
Wall-time delta OLD vs NEW on the identical storm driver, reported
honestly. New cognition lines: about 90 (4 functions). No new modes,
bridges, handlers, or semantic cases.

## Sealed eval protocol (frozen)

Binaries (same pinned znc, sha256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`):
- OLD: unmodified base + 0221pdt `sc_patch_fixed.zag` verbatim
  (gate + hardened walk, NO evict hook) + `evict_driver.zag`.
- NEW: base + 1 hook line + `sc_patch_fixed.zag` + hook functions +
  the SAME `evict_driver.zag` (frozen sha256
  `b421402707b429bad88b89640b11956720ce6fcd53c4e5e4364732052ad6b450`,
  recorded 2026-10-02 before the freeze commit).

Assembly (frozen, same as the 0221pdt A4 recipe): base lines 1-296,
315-418, 427-441, 473-532, 544-812, 836-1356, 1358-1591; then patch;
then driver.

`evict_driver.zag` (frozen instrument):
- W1 MAP storm (mode 3 = MAP index + MTF): 30 plen-5 + 8 plen-3 MAPs,
  2 query chains; HEALTH gate check; QPRE (2 queries, ans/scan/ok);
  Phase A: 8 natural `evict_node` bursts, emitting victim id/tag and
  both gates after each, plus first-flip violator cause (1=dead member,
  2=wrong tag, 3=plen mismatch, 4=FACT-side); REFRESH query (resets MTF
  winner); Phase B: targeted victims (MTF winner, plen-5
  head/mid/tail, plen-3 head/tail for MAPs; 8 FACTs spread across
  buckets; adversarial positions), all other live nodes protected via
  the codebase's own type-9 self-edge idiom, `evict_node` loop until
  all targeted victims die, emitting victim/tag/gates/cache after
  each. The kill loop protects live tag-3 record nodes each iteration
  (records outrank MAP victims at bid 0 vs 2; without this the loop
  starves on reused record slots). W2 victims' guard edges are removed
  first (simulating full decay) so they are evictable; W2 lookups use
  step 6 to stay on taught subjects. Phase D churn: 6 new plen-5 MAPs
  + 12 FACTs + 2 fresh query chains (slot reuse of dead victim slots),
  CHURN gate check; QPOST (old subjects) + QPOST2 (fresh subjects,
  MTF cache cleared first so the query must walk the bucket, testing
  the index itself rather than the MTF fast path); COUNTERS (node-0
  fields 4/8/12) and cache state.
- W2 FACT storm (mode 4): 300 FACTs + gather chain; HEALTH; GPRE
  (gather np/factvisits; lu50 hits/factvisits); Phase A: 10 natural
  evictions; Phase B: 8 targeted FACT victims spread across buckets
  (guard edges removed first, simulating full decay), protect-others,
  kill loop; Phase D churn: 40 new FACTs (slot reuse); CHURN gates;
  GPOST; COUNTERS.
- Each binary runs the driver 3x; stdout captured; sha256 recorded.

## Kill bar (frozen, will not be weakened)

EVICT-PASS iff ALL of the following hold:

(i) Vacuity / bug demonstrated (OLD binary): in W1, at least one
eviction with victim tag 20 is followed at the next gate check by
`idx_validate==0`; in W2, at least one eviction with victim tag 1 is
followed by `fidx_validate==0`. If the storm never exercises the stale
path, it is vacuous and the verdict is FAIL (redesign), not PASS.

(ii) Coherence invariant (NEW binary): `idx_validate==1` after EVERY
eviction in W1 and W2, and `fidx_validate==1` after EVERY eviction in
W1 and W2, in all 3 runs. Any 0 is FAIL. (Covers V1 and V2.)

(iii) No performance collapse (storm worlds): NEW W1 QPOST2 q0 scan is
strictly less than OLD W1 QPOST2 q0 scan (index serving, not fallback)
and at most 4x NEW W1 QPRE q0 scan; NEW W2 GPOST gather factvisits is
strictly less than OLD W2 GPOST gather factvisits and at most 4x NEW
W2 GPRE gather factvisits.

(iv) Answers preserved: every emitted ans/ok/np/hits value in NEW
equals the corresponding OLD value, run for run (r1 vs r1, etc.).
Eviction must not change what the system knows.

(v) Determinism: 3/3 byte-identical runs per binary; hashes recorded.

(vi) Healthy-state no-op: NEW binary on the Part A driver
(`sc_driver.zag`): 3/3 runs byte-identical to the canonical hash
`eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d`.
(Exploratory probe showed 1/1; sealed runs confirm 3/3.)

(vii) Mechanism accounting (NEW): node-0 field 4 equals the number of
tag-20 victims across the run; field 8 equals the number of tag-1
victims; field 12 >= 1 (chain-break unlinks happened); every Phase-B
targeted victim died (k20==nv in W1, k10==nv in W2). OLD: all three
counters 0.

(viii) MTF coherence: in W1 Phase B the MTF winner is a targeted
victim; NEW shows cache == -1 on the eviction line that killed it;
query answers still equal OLD (iv).

EVICT-FAIL iff any of (i)-(viii) fails, with the failing condition and
first-divergent evidence recorded in SEALED_EVAL.md. A hook that
changes healthy-state output fails (vi) even if the storm passes.
PARTIAL may be recorded only with per-condition HOLD/FAIL and no bar
weakening.

## Red-team self-review (frozen requirement)

SEALED_EVAL.md and REDTEAM_SELF.md each end with a red-team
self-review attacking the work: ways coherence could hold usually but
not always (missed victim tags, chain shapes the mirror walk
mishandles, slot-reuse races, gate bypass paths), what would falsify
the verdict, and the adjacent non-eviction chain-killer
(`t2_revise_graph` tombstones tag-101 chain nodes without firing the
hook; flagged, out of scope). The verdict lines name this prereg as
the governing frozen bar.

## Governance

This prereg is committed ALONE before any implementation file.
Prereg commit strictly precedes implementation commits. No kill bar
above may be weakened after seeing results; amendment requires a new
frozen prereg and re-execution. Pure Zag only; no Python anywhere.
Zero em-dashes in all lane documentation (check_no_dash.sh before
every commit).
