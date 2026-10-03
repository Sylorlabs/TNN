# Deduplication as a DYN-1 Bending Mechanism: Investigation Report

## Verdict

**DEDUP-COMPLETE: BENT.** A content-addressed dedup gate at the miss
allocation site bends the DYN-1 cost curve. Per-miss node cost now declines
with experience for repeated keys: first miss +2, repeats +0.

## 1. Analysis: why 70 duplicate UNCERTAINTY nodes are created

Allocation site: `miss_inquire(W,s,r)` (line 795 of the variant; sole
production caller is `ev_query`'s true-miss path, line 833).

On every true miss it unconditionally allocates:

1. An UNCERTAINTY node: tag 30, field 4 = -4,
   `write_node(W,u,s,r,2,0)` so fields 20=s, 24=r, 28=2, 32=0.
2. A guide: tag 1, field 4 = s, `write_node(W,g,30,-999,0,0)`.
3. Edges: guide->UNCERTAINTY (type 1), POLICY_ROOT->guide (type 10).

The DYN-1 sequence misses 10 keys (s=101..110, r=99) exactly 7 times each,
so 70 misses x (1 UNCERTAINTY + 1 guide) = 70 duplicate UNCERTAINTY nodes
and 70 duplicate guides.

Duplicate identity: a miss-created UNCERTAINTY node is fully determined by
(tag=30, field4=-4, field20=s, field24=r). Every other field is constant
(field 28=2, rest 0) by construction in `miss_inquire`, which is the only
production writer of tag-30/field4=-4 nodes (other tag-30 writers at lines
1047, 1182, 1378 are inert test functions the DYN-1 driver never calls).
The guide is likewise fully determined per (s,r): tag 1, field 4=s,
fields (20,24,28,32)=(30,-999,0,0). Two UNCERTAINTY nodes with the same
(s,r) key are byte-identical in every field. They are duplicates by
content, not just by key.

Why no dedup existed: `miss_inquire` performs no existence check before
`alloc_node`. The miss path is write-first.

## 2. Design: content-addressed reuse gate

Before allocating, scan the 1024-cell node table for a live
(field 36=1) tag-30/field4=-4 node with (field20,field24)==(s,r). If found,
return early: the reification would be an exact duplicate, so cost is +0
nodes and +0 edges. Because the guide is created in the same call and is
likewise fixed per (s,r), skipping both preserves the ev_act option set:
the distinct candidate actions are unchanged; only exact-duplicate options
are removed.

Lookup cost: one 1024-cell scan per true miss, comparing 4 fields. The
existing `ev_query` already performs a 1024-cell scan per query and
`activate` another; the dedup scan is the same order, so it is no worse
than the current full-scan architecture. (A production version needs a
sublinear index; see section 6.)

Correctness argument:

- Query answers unchanged: all 70 misses still return -2 (verified in
  run output). UNCERTAINTY nodes are invisible to `activate` (tag-1 scan
  only); guides carry field20=30 so they cannot match (s,r) queries.
- Eviction-safe: if the earlier UNCERTAINTY was evicted, no live key
  matches and a fresh node is allocated, identical to baseline behavior.
- The guide pool under POLICY_ROOT keeps one guide per distinct missed
  key; the DYN-1 driver never calls ev_act, so no behavioral claim is
  made beyond option-set preservation.

What dedup does NOT cover in this sequence: Phase A teaches carry a fresh
value per event (v=100+i), so no two teaches are identical. Phase D
contradictions write HIST nodes stamped with the event clock, so repeats
are not byte-identical. The miss path is the complete dedup story for the
DYN-1 sequence.

## 3. Implementation

Unfrozen variant only. `dedup_full.zag` = `dyn1_full.zag` (the DYN-1
measurement variant from `003767553`: verbatim frozen cognition with base
test main removed and the DYN-1 driver appended) plus a 15-line dedup
pre-scan at the top of `miss_inquire`. `dedup_diff.txt` records the exact
diff: nothing else in cognition changed, and the driver is verbatim.
Frozen source was never opened for edit.

## 4. Results: DYN-1 bends

3/3 byte-identical runs, SHA-256
`7bfa828aa982307825d5ada42b018e60a81204aeb517df89983159cb8c965fe4`.

Per-phase node deltas (dedup vs frozen baseline from `003767553`):

| Phase | Events | Baseline totdn (min/max) | Dedup totdn (min/max) | Delta |
|-------|--------|--------------------------|-----------------------|-------|
| A teach | 80 | 80 (1/1) | 80 (1/1) | 0 |
| B qhit | 50 | 0 (0/0) | 0 (0/0) | 0 |
| C miss | 50 | 101 (2/3) | 21 (0/3) | -80 |
| D observe | 50 | 100 (2/2) | 100 (2/2) | 0 |
| E miss2 | 20 | 40 (2/2) | 0 (0/0) | -40 |

Final state: 201 live nodes (baseline 321, -120), 369 live edges
(baseline 489, -120), clock=250.

Per-event Phase C pattern (event:dn):
130:3 (first miss ever: policy anchor + UNCERTAINTY + guide),
131-139:2 (first miss per remaining key),
140-179:0 (all repeats).
Phase E: all 20 events dn=0.

UNCERTAINTY census: 10 total, exactly 1 per miss key (baseline 70, 7 per
key). All 70 misses still return -2.

Edge deltas also fall (C: 70 vs 150; E: 8 vs 48) because no duplicate
guide edges are created.

## 5. Interpretation

This is the first mechanism in the program that bends DYN-1. The discount
pilot (`8ad158352`) and Node 1 (`67b700d3f`) both left the curve flat
because they changed decisions without touching allocation sites. The
dedup gate touches the allocation site directly: repeated experience now
costs less than novel experience, which is the operational definition of
amortization the TNN-3 gate requires.

Honest classification: the mechanism is researcher-authored (a fixed
identity rule at a researcher-chosen site), so this is bounded L2-class
architecture, not learner-invented structure. It proves dedup is a valid
DYN-1 bending mechanism and quantifies the available headroom in this
sequence (120 nodes, 37% of final state). It does not prove the learner
can build such a mechanism itself; learner-authored amortization remains
the open frontier.

The mechanism generalizes: the same pre-allocation existence check can be
applied at any allocation site where the written structure is a function
of its key. It is one candidate for the shared consequence substrate's
retention side (decline/forget as "do not reify what is already known").

## 6. Limitations and follow-ups

- Lookup is O(1024) per miss. Sublinear retrieval (hash index on
  (tag, key fields)) is required before this scales; the scan cost is
  bounded and matches current architecture but does not improve it.
- Identity is byte-exact. Semantically equivalent but
  representationally distinct structures are not deduped; that needs
  canonicalization, which is harder.
- Phase A and D are untouched: distinct values and clock-stamped
  histories are genuinely novel content, not duplicates. Bending those
  needs decline or revision-aware reuse, not dedup.
- ev_act behavioral equivalence under dedup was not measured (driver
  never calls ev_act); argued at the option-set level only.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 1 (the dedup existence gate in
  miss_inquire; identity rule fixed by researcher)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 1 (the dedup pre-scan pattern)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 60 (misses that reused an existing UNCERTAINTY instead
  of allocating: 40 in Phase C, 20 in Phase E)
- REVISION EVENTS: 0
- COGNITION LINES: 15 (dedup pre-scan plus comment)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints honored

UNFROZEN variant only. Frozen source read-only, hash re-verified
(`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`).
Pure Zag via pinned znc. Safebin active, `which python3 python` empty.
Zero em dashes (byte-verified). Paper untouched. No sealed worlds.
Nothing pushed. Explicit pathspecs on git add and git commit.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/dedup/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, constraints)
- `DEDUP.md` (this report)
- `dedup_full.zag` (unfrozen variant: DYN-1 measurement build + dedup gate)
- `dedup_diff.txt` (exact cognition diff vs `dyn1_full.zag`)
- `dedup_bin` (compiled binary)
- `run1.txt`, `run2.txt`, `run3.txt` (3/3 byte-identical)
