# REPORT.md -- Scaling Continuation (Micah Section 6)

Worker: Scaling Continuation Worker. Base: scaling index commit 2bea4c73f
(unfrozen variant). Date: 2026-10-01. Pure Zag. 3/3 byte-identical runs
(sha256 eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d).

## What was built

Three mechanisms on an expanded workspace (8192 nodes / 16384 edges,
8x the frozen 1024-node base):

A. MAP plen-bucket index (from the scaling-index wave, adapted to 8192
   nodes). Learner-maintained via promote_graph. Mode bit0.

B. EMERGENT ORDERING (new). The retrieval priority key emerges from
   access/consequence history, not from a researcher taxonomy:
   - Fast path: the (MAP, path-length) of the last verified rebind hit
     is remembered in learner state (index node field 12, packed as
     mapid*8+plen). Next query tries it first across all paths of that
     length. Verification still arbitrates.
   - Move-to-front: on every verified hit the winning MAP moves to the
     front of its plen bucket. Bucket order reflects experienced
     success, not promotion order or id order.
   No researcher table of important MAPs exists; priority is written
   only by verified outcomes. Mode bit1 (requires bit0).

C. FACT subject index (new). 24 hash buckets (subject mod 24) over 4
   chained tag-40 index nodes; intrusive lists via FACT field 12
   (verified free on tag-1 nodes: zeroed at alloc, never otherwise
   read/written). Learner-maintained via ev_teach/ev_teach_in.
   t2_gather and t2_lu_first dispatch to indexed variants. Stale
   (evicted) entries skipped by live/tag checks. Mode bit2.

Mode bits in MAP index node field 4: 1=MAPidx, 2=MTF, 4=FACTidx.
Tested: 0 (linear), 1 (MAPidx id-ordered), 3 (MAPidx+MTF), 4 (FACTidx).

## Bug found at scale (pre-existing, frozen base)

res_op/execute used 1000 as the frame-slot vs node-id threshold. Any
node id >= 1000 was misread as a frame slot, so t2_exec returned
-999999 once the workspace passed 1000 nodes. At 100 MAPs this was
invisible (small ids); at 500 every verify rejected (tried=5,
rejected=5, ok=0). Fixed in the unfrozen expanded base only (threshold
1000 -> 10000); frozen base untouched. Scaling-blocker class: the
architecture could not have passed 1000 nodes without this fix.

## 1. Scale law: 100 / 500 / 1000 MAPs

World: D broken plen-2 decoys + 5 real plen-5 MAPs, 2 plen-5 queries.

| MAPs | mode | scan visits | walks | tried | ok |
|------|------|-------------|-------|-------|----|
| 100  | lin  | 699         | 96    | 1     | 1  |
| 100  | idx  | 5           | 1     | 1     | 1  |
| 500  | lin  | 3464        | 491   | 1     | 1  |
| 500  | idx  | 5           | 1     | 1     | 1  |
| 1000 | lin  | 6964        | 991   | 1     | 1  |
| 1000 | idx  | 5           | 1     | 1     | 1  |

Reduction: 140x at 100 (confirms prior wave), 693x at 500, 1393x at
1000. The indexed scan is flat (one bucket walk); the linear scan grows
with MAP count. The 140x was not a ceiling.

Honest limits:
- The index cuts scan visits, not verifies. When decoys structurally
  match (section 2), the tax is in verifies.
- t2_gather still scans all slots per expansion in linear mode
  (section 3 addresses this).
- Absolute ceiling: 8192 nodes / 16384 edges. 1000 MAPs used ~8043
  nodes. 10000 MAPs do not fit; further scale needs a bigger workspace
  or eviction that preserves index integrity (not attempted).
- alloc_node, link_edge, and decay remain O(N) free-slot / full scans;
  they are the next targets after gather.

## 2. Emergent ordering

World: 12 plen-3 decoy MAPs + 1 real plen-5 MAP (promoted 7th, so
oldest-first, id-ascending, and newest-first orders ALL pay the decoy
tax on Q0), 3 len-3 distractor paths + real-chain prefix per query
subject (4 len-3 paths), repeat queries on fresh subjects, then a stale
second len-5 chain with a new answer.

Verifies per query (tried):

| mode | Q0 | Q1 | Q2 | QSTALE |
|------|----|----|----|--------|
| 0 linear, oldest-first | 25 | 43 | 43 | 50 |
| 1 indexed, id-order, no MTF | 25 | 43 | 43 | 50 |
| 3 indexed + MTF emergent | 49 | 1 | 1 | 2 |

Findings:
- MTF learns from verified hits: 49 verifies on Q0 collapse to 1 on
  Q1/Q2 (fast path). Without MTF, repeat queries repay the full tax
  (43), which grows as successful rebinds promote new MAPs.
- Stale recovery: the fast path tries the remembered winner on all
  paths of its length. The stale path rejects (1 verify), the new path
  accepts (1 verify). Total 2 vs 50 for a full rescan. Verification
  arbitrates; a wrong memory costs exactly the rejected attempts, never
  a wrong answer (all ok=1).
- The priority key (which MAP, which length) was written only by the Q0
  verified hit. No researcher ranking exists. This is the requested
  alternative to fixed plen buckets: plen still selects candidates, but
  ORDER emerges from consequence history.

## 3. FACT subject index (attacking the O(1024) gather)

World: 1000 FACTs + a 3-link chain. Direct t2_gather from the chain
head; 50 t2_lu_first lookups. Metric: FACT visits.

| op | linear visits | indexed visits | reduction |
|----|---------------|----------------|-----------|
| t2_gather (4 paths) | 32760 | 167 | 196x |
| 50 x t2_lu_first | 24800 | 1092 | 22.7x |

The gather BFS now walks hash-bucket chains (~42 FACTs/bucket) instead
of all 8192 slots per expansion. Same paths returned (np=4 both modes;
50/50 lookups hit). Learner-maintained: every teach files the FACT, so
the index never goes stale except via eviction, which is skipped by
live checks.

## Architecture accounting

New cognition source: sc_patch.zag (~430 lines: index, MTF, FACT index,
replacements). New modes: 0 (mode bits are learner-state flags, not
cognitive modes; the query path is unchanged). New bridges/handlers: 0.
Hardcoded semantic cases added: 0. The plen-bucket key remains
researcher-chosen; section 2 shows ordering emerging from history
instead.

## Files

- sc_base_expanded.zag (with sc_base_expanded.zag.bak1000 pre-fix copy)
- sc_patch.zag, sc_driver.zag, sc_full.zag (2149 lines), sc_bin
- build.sh, expand.sh
- run1.txt, run2.txt, run3.txt (byte-identical), runN.time
- dbg*.zag: debug scaffolding, not part of the result

## Verdict

SCALING-CONT-COMPLETE. Scale law holds to 1000 MAPs (1393x). Emergent
ordering learns 49->1 on repeat queries and recovers from stale memory
in 2 verifies. FACT index cuts gather visits 196x. Pre-existing
1000-threshold bug fixed (unfrozen only).
