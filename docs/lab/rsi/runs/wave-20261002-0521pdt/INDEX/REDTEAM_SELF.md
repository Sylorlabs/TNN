# REDTEAM_SELF.md - INDEX-EVICT lane, wave-20261002-0521pdt

Self red team, written before the verdict. The job is to kill the
claim "eviction maintains index coherence" or bound it honestly.

## Claim under attack

`idx_on_evict` (1 hook line in `evict_node` + ~90 lines of pure Zag)
maintains the index coherence invariant (every bucket member live and
correctly tagged; every MAP member's current chain plen equals its
bucket) across eviction storms, with no answer changes and no
performance collapse.

## Attack 1: Does coherence hold, or just usually hold?

The hook dispatches on victim tag: 20 (MAP member unlink), 1 (FACT
member unlink), 902/101/102 (chain-break unlink), else MTF-cache check
only. Shapes that could escape:

(a) A chain member with a tag outside {902,101,102}. `rb_chain_plen`
only traverses 102 and 101 nodes (returns -1 otherwise), and the
mirror walk (`idx_chain_hits`) enforces the same tags. A non-102/101
node cannot be ON a chain that `rb_chain_plen` would walk, so its
death cannot change a valid plen. Tag 902 (literal) is included
because literals anchor chain roots in the probe worlds. If a future
chain shape uses a new tag, the hook must be extended. BOUND: the
hook covers exactly the tags `rb_chain_plen` understands.

(b) The seq-table first-wins fix. The initial sealed build used
last-wins for the per-eviction seq table while `seq_nx` (used by
`rb_chain_plen`) returns the first type-12 edge. A 101 node with two
type-12 out-edges would make the mirror walk diverge from
`rb_chain_plen`, potentially missing a victim (under-unlink, fatal
for the invariant). Self-caught during the sealed runs; fixed to
first-wins (matching `seq_nx` exactly) and the governing run set
re-executed. In the storm worlds each 101 node has exactly one
type-12 out-edge (chains are built once by `t2_asm_chain`), so the
two builds are behaviorally identical there; the fix is a soundness
hardening for production shapes, not a bar change.

(c) The index node itself (tag 40) or the counter node (tag 900) as
victim. The hook does not handle t=40/900. If `evict_node` ever
selects infrastructure, the index is destroyed, not just incoherent.
MITIGATION: infrastructure nodes carry protection in practice; the
driver protects them. But there is no structural guarantee. FLAGGED
as a production hardening gap, not a storm-world issue.

(d) `t2_revise_graph` (base) tombstones tag-101 chain nodes WITHOUT
going through `evict_node`, so the hook never fires. This is a REAL,
known chain-invalidation path outside the hook's reach. The gate
catches the resulting incoherence (REJECT to linear fallback;
availability preserved), but it is a performance cliff the hook does
not close. Explicitly out of scope for this wave; queued for the
adjacent-path work. Any production claim of "index-coherent memory
management" must cover it.

## Attack 2: Is the storm adversarial enough?

The storm uses natural `evict_node` bursts (8-10), targeted victims at
adversarial bucket positions (head/mid/tail, MTF winner, cross-bucket
FACT spread), slot reuse via churn, and guard-edge removal (simulated
decay). What it does NOT do:

(a) It does not evict the index node or counter node (see 1c).
(b) It does not interleave `t2_revise_graph` (see 1d).
(c) Burst sizes are small (8-10 natural + 6-8 targeted). A longer
soak (hundreds of evictions) could expose accumulation bugs the
counters would miss. The per-eviction gate checks bound this: any
single missed unlink flips a gate to 0 immediately, and the logs
show gate=1 after EVERY eviction, not just at the end.
(d) The W1 storm's MAP victims are all plen-5/plen-3 (the only plens
indexed). Plen-4/plen-2 buckets are empty; a victim in those buckets
is untested. The unlink loop covers all four buckets identically, but
the adversarial-position coverage is incomplete. WEAKNESS admitted.

## Attack 3: Could the gate be fooled (false ACCEPT)?

The gate walks every bucket and checks liveness, tag, and plen. A
false ACCEPT requires a stale entry the walk does not detect: a cycle
the hardened walk does not terminate on, or an OOB id the walk
skips silently. The walk was FIX-VERIFIED in the 0221pdt wave (8/8
validation matrix, cycle-safe by construction with step caps and
range guards). The hook's own walks reuse the same discipline. No
false ACCEPT was observed in 6 storm runs (3 NEW + 3 OLD, where OLD
correctly REJECTs). Residual risk is in the Part B walk, not new
here.

## Attack 4: Cost

Per chain-victim eviction the hook scans 16384 edges (one pass) plus
short MAP-chain walks. `evict_node`'s own selection scan is ~1e9 ops
in these worlds, so the hook is noise by comparison. Wall-time
OLD vs NEW on the identical driver is reported in SEALED_EVAL.md. If
the edge store grows, the 16384 scan grows with it; it is bounded by
the store, not by the world size. No per-query cost: the hook runs
only on eviction.

## Attack 5: What would falsify the verdict?

- Any `idx=0` or `fidx=0` in a NEW storm run (kills (ii)).
- Any NEW answer differing from OLD run-for-run (kills (iv)).
- Any Part A run not matching the canonical hash (kills (vi)).
- A production-shaped world (revise_graph, infrastructure eviction,
  101 node with two seq edges) breaking the invariant. The first two
  are queued; the third is covered by the first-wins fix.

## Verdict on the red team

The mechanism holds in the storm worlds with the first-wins fix. The
known gaps (1c, 1d, 2d) are bounded, flagged, and queued; none fires
in the sealed eval. The claim is "index-coherent eviction for the
evict_node path", not "all memory mutation is index-safe". The
verdict names this bound.
