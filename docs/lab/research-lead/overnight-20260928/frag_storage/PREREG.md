# PREREG: H-DECOMP-1 Fragment-Addressable Storage (UNFROZEN)

Status: FROZEN. Committed before any implementation.
Worker: Fragment-Addressable Storage (H-DECOMP-1, P0). Date: 2026-10-02.

## 1. Hypothesis

H-DECOMP-1: fragments of learned MAP structures can be made FIRST-CLASS
addressable in learner-state storage via type-15 LINK edges annotated with
(start, len) segment marks, so that any mechanism (composition DFS,
fragment recombination, rebinding) addresses (m, start, len) through one
shared store instead of ad hoc per-mechanism triples.

This supersedes the ad hoc addressing in Invention H2 (ir_full.zag), where
(map_id, start, length) triples exist only ephemerally during search and
are recomputed per mechanism.

## 2. Background (from C208)

The composition-compare battery (C208, composition_compare/REPORT.md) found
T4 (partial applicability) FAILED for all three mechanisms A, B, C.
Root cause: all mechanisms treat MAPs as atomic units; none can use a
PREFIX of a learned structure.

T4 world (exact, replicated here):
- X: plen-4 r1 chain, facts (11,1,12) (12,1,13) (13,1,14) (14,1,15).
  Query (11,71,15) promotes MAP mx.
- Y: plen-2 r2 chain, facts (21,2,22) (22,2,23).
  Query (21,72,23) promotes MAP my.
- Z facts: (101,1,102) (102,1,103) (103,1,104) (104,2,105) (105,2,106).
  Query (101,70,106), expected=106.
- Z needs the first 3 r1 steps of X (75% useful) plus all of Y.

## 3. Design (frozen)

### 3.1 Storage medium

Learner-state edge table, 16 bytes per edge: field0=from node,
field4=edge type, field8=to node, field12=aux. New edge type 15 (FRAG)
joins the existing type registry. No new tables, no new node types,
no new modes, bridges, or handlers. The marks are learner-created
persistent state, not researcher machinery.

### 3.2 Fragment mark layout

One type-15 edge per fragment mark:
- from = MAP node m
- to = entry guard cell of the sub-chain (the guard cell at position
  `start` in m's executable graph; for start=0 this is the graph root)
- aux (field12) = (start << 16) | len, packing both segment marks into
  the single existing aux field. Chains are short; 16 bits each is ample.

### 3.3 API (pure Zag, operates on learner workspace W)

- `frag_store(W,m,start,len)` -> edge id, or -1 on rejection.
  Validates: m is a live MAP node (type 20); extracts the relation
  sequence length L by structural walk (guard/set alternation, licensing
  facts read via DEP edges, same discipline as H2 ir_relseq; MAP field 4
  and field 8 are never consulted); rejects start<0, len<1,
  start+len>L, dead MAP. Walks to the entry guard cell for `start`.
  Deduplicates: an identical (m,start,len) mark returns the existing
  edge id without writing a duplicate.
- `frag_fetch(W,m,start,len,cur,vals,fids)` -> steps read, or -1.
  Finds the mark by scanning type-15 edges (from==m, unpacked marks
  match). From the entry cell, walks `len` steps structurally, reading
  each step's relation label from its licensing fact's DEP edge, and
  checks satisfiability from value `cur` by fact-store lookup.
  Fills vals[0..len] (value chain) and fids[0..len-1] (licensing fact
  ids). Returns len on success, -1 if the mark is absent or any step
  is unwalkable from cur.
- `frag_list(W,m,out)` -> count.
  Enumerates all type-15 marks with from==m into out[] as
  (start,len,entry) triples. Returns the count.

### 3.4 Consumers (two mechanisms, one store)

- Mechanism C-DFS: depth-first fragment chaining. Candidates are ALL
  marks in the store satisfiable from the current value (via
  frag_fetch), excluding reuse of the same mark in one path. Recurses
  until cur==expected. This is the Composition C lineage (constraint
  driven DFS), with whole MAPs replaced by fragment marks.
- Mechanism H2-greedy: longest-first greedy fragment assembly. Same
  store, same frag_fetch reads, different search order (longest
  satisfiable mark first, then verify full chain reaches expected).
  This is the Invention H2 lineage (fragment recombination).
- Neither mechanism stores fragment marks of its own; both resolve
  exclusively through frag_store/frag_fetch/frag_list. A per-mechanism
  read counter instruments which marks each mechanism resolved.

### 3.5 Marks written for the T4 world

frag_store(mx,0,3)  prefix needed by Z
frag_store(mx,0,4)  whole X (control mark)
frag_store(mx,1,3)  interior fragment (generality)
frag_store(mx,2,2)  suffix fragment (generality)
frag_store(my,0,2)  whole Y
frag_store(my,0,1)  Y prefix (generality)

Expected store size: 6 type-15 edges. frag_list(mx) returns 4,
frag_list(my) returns 2.

## 4. Test specification

### UNIT-1: bounds rejection
frag_store(mx,-1,2), frag_store(mx,0,0), frag_store(mx,2,3) with
plen(mx)=4, frag_store(deadnode,0,1) all return -1. No edge written.

### UNIT-2: dedup
frag_store(mx,0,3) twice returns the same edge id; type-15 edge count
does not grow.

### UNIT-3: unknown fetch
frag_fetch(W,mx,3,1,...) with no such mark returns -1.

### UNIT-4: list enumeration
frag_list(mx) returns 4 with the exact (start,len) pairs
{(0,3),(0,4),(1,3),(2,2)} in edge-id order; frag_list(my) returns 2.

### UNIT-5: fetch correctness
frag_fetch(W,mx,0,3,101,...) walks relseq [1,1,1] from value 101 and
fills vals=[101,102,103,104], fids=the three licensing fact ids.

### T4-CTRL: whole-MAP control
C-style DFS restricted to whole MAPs (no fragment marks consulted) on
the T4 world must FAIL to reach expected=106. This replicates the C208
T4 FAIL and anchors the comparison.

### T4-FRAG-C: C-DFS over the shared store
C-DFS over fragment marks on the T4 world must PASS: reach expected=106
with a solution path that includes mark (mx,0,3) followed by (my,0,2).

### T4-FRAG-H2: H2-greedy over the same store
H2-greedy over the same type-15 store must PASS: reach expected=106.
Its fragment reads must resolve through frag_fetch against the
identical edge set used by C-DFS (same 6 edges; per-mechanism read
counters show both mechanisms resolved marks from the shared store).

### SHARED: no duplication
The implementation contains exactly one fragment-mark storage path
(frag_store writes type-15 edges). Mechanism code contains no
fragment storage of its own. Verified by inspection and by the single
shared edge count both mechanisms read.

## 5. Kill bars (all must pass for FRAG-STORAGE-COMPLETE)

- KB1: 3/3 runs byte-identical stdout (sha256 match across run1..run3).
- KB2: T4-CTRL FAILS (whole-MAP DFS does not reach 106).
- KB3: T4-FRAG-C PASSES with (mx,0,3) then (my,0,2) in the solution path.
- KB4: T4-FRAG-H2 PASSES using the identical type-15 edge set
  (per-mechanism read counters both nonzero; shared edge count = 6).
- KB5: UNIT-1 through UNIT-5 all pass.
- KB6: pure Zag only (toolchain guard recorded in NAMECHECK.md Step 0;
  no forbidden executable invoked); zero new modes/bridges/handlers;
  marks are learner-state edges only.
- KB7: store written once, read by both mechanisms; no per-mechanism
  fragment storage (single frag_store path; mechanism code holds no
  mark tables).

## 6. Determinism plan

All output is formatted into ONE preallocated buffer with
cursor-returning emit helpers and flushed with a single
_zag_raw_syscall(1,1,ptr,len) write (per the 2026-10-02 stdout
miscompile workaround). No _zag_print for dynamic content. Fixed
iteration orders (node id ascending, edge id ascending). No randomness,
no timestamps, no addresses in output.

## 7. Out of scope

T5 (unsupervised composition), cross-world transfer, and learner-driven
mark creation (marks are researcher-seeded in this prototype; learner
origination of marks is a follow-up hypothesis, not claimed here).
