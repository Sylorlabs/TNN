# REPORT: H-DECOMP-1 Fragment-Addressable MAP Storage

## Verdict: FRAG-STORAGE-COMPLETE

Date: 2026-10-02. Worker: Fragment-Addressable Storage (H-DECOMP-1, P0).
All 7 frozen kill bars pass. T4 (partial applicability) is resolved by
fragment addressing: the C208 all-FAIL becomes a PASS for both consumer
mechanisms through one shared type-15 LINK store.

## 1. What was built

`frag_store.zag` (pure Zag, 19.8 KB source): a fragment-addressable
storage substrate in learner state.

- A fragment mark is ONE type-15 LINK edge: from = MAP node m,
  to = entry guard cell of the sub-chain at position `start`,
  aux field = (start << 16) | len. No new tables, no new node types,
  no modes, bridges, or handlers. The marks are learner-state edges,
  written by `frag_store`, resolved by `frag_fetch`, enumerated by
  `frag_list`.
- Structural discipline inherited from Invention H2: chain walks read
  each SET cell's licensing fact via its DEP edge; MAP field 4 and
  field 8 are never consulted.
- The only type-15 edge write in the codebase is inside `frag_store`
  (line 254); the other `add_edge` calls write types 1 (DEP) and 12
  (SEQ) for MAP chain construction. Neither consumer mechanism stores
  fragment marks of its own.

## 2. T4 test (exact C208 replication)

X plen-4 r1 (facts 11..15), Y plen-2 r2 (facts 21..23), Z facts
101..106, query (101,70,106), expected=106. Six marks stored:
(mx,0,3) (mx,0,4) (mx,1,3) (mx,2,2) (my,0,2) (my,0,1).

Results (3/3 byte-identical, sha256
440f6d8419a07e3e6cf4a37e5f1b08f55b0907e211f0b4cc7a1bd93c2c191761):

- UNIT-1 bounds: frag_store rejects (-1,2), (0,0), (2,3) on plen-4 and
  dead node 999; no edge written. PASS
- UNIT-2 dedup: second frag_store(mx,0,3) returns the same edge id;
  type-15 count stays 6. PASS
- UNIT-3 unknown fetch: frag_fetch of unstored (mx,3,1) returns -1. PASS
- UNIT-4 list: frag_list(mx)=4 with exact pairs (0,3)(0,4)(1,3)(2,2);
  frag_list(my)=2 with (0,2)(0,1). PASS
- UNIT-5 fetch: frag_fetch(mx,0,3) from 11 walks relseq [1,1,1] and
  fills vals=[11,12,13,14]. PASS
- T4-CTRL whole-MAP DFS (no marks): ans=0, FAILS. Replicates the C208
  T4 FAIL and anchors the comparison. PASS
- T4-FRAG-C (Composition C lineage, depth-first over the store):
  ans=1, path=[(mx,0,3),(my,0,2)]. The PREFIX (mx,0,3) is used. PASS
- T4-FRAG-H2 (Invention H2 lineage, longest-first greedy over the
  same store): ans=1, pathlen=2. PASS
- SHARED: 6 type-15 edges total; C reads=5, H2 reads=6 (both nonzero,
  both resolved through frag_fetch against the identical edge set).
  PASS

## 3. Kill bar adjudication

- KB1 3/3 byte-identical stdout: PASS (sha256 match run1..run3).
- KB2 T4-CTRL FAILS: PASS (ans=0).
- KB3 T4-FRAG-C PASSES with (mx,0,3) then (my,0,2): PASS.
- KB4 T4-FRAG-H2 PASSES on the identical edge set, both read counters
  nonzero: PASS.
- KB5 UNIT-1..UNIT-5 all pass: PASS.
- KB6 pure Zag, toolchain guard recorded in NAMECHECK.md Step 0
  (`which python3 python` empty), zero new modes/bridges/handlers,
  marks are learner-state edges only: PASS.
- KB7 store written once via the single frag_store path; mechanism
  code holds no mark tables (verified by inspection of add_edge call
  sites): PASS.

## 4. Design notes and limits

- Marks in this prototype are researcher-seeded. Learner origination
  of marks (the learner deciding what to mark) is a follow-up
  hypothesis and is NOT claimed here.
- Output uses the single-buffer plus one raw write syscall pattern
  (2026-10-02 stdout miscompile workaround); stdout bytes verified
  with od, ending cleanly at VERDICT=FRAG-STORAGE-COMPLETE.
- Frozen TNN-2 core and all prior lanes were read but never modified.
- This is shared substrate, not a subsystem: the two mechanisms are
  consumers of one store, and the store adds one edge type to the
  existing learner-state edge table.

## 5. Artifacts

- PREREG.md (frozen, committed before implementation as b5b8fe190)
- NAMECHECK.md (toolchain guard Step 0 and checks)
- frag_store.zag (source, sha256 179fd7eede815594a3abd5049a0c4cebaa85586c26661378ca4ec32011e9bfe9)
- frag_bin (binary, sha256 bf609633679db2e12073ab2658660ecbe4a177e67614c000d9a0ad8bf422e323)
- compile.log, run1.txt, run2.txt, run3.txt

## 6. Recommended follow-ups

- Learner-originated marks: let the learner write its own (m,start,len)
  marks from experience, then test reuse (composition criteria).
- Adversarial red team on the store: overlapping marks, marks on
  revised MAPs, mark invalidation on contradiction.
- Integration: run the fragment store against the continuing learner
  rather than a fresh workspace per test.
