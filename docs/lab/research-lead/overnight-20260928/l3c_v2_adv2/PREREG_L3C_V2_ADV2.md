# PREREG: L3C v2 Round-2 Independent Adversary Attack (pipeline step 10)

Date: 2026-09-30. Status: FROZEN. Committed alone before any attack
implementation exists. The families below are designed AFTER this prereg's
freeze in the sense required by the attack protocol: no family vector,
prediction, or bar in sections 4-6 may be altered after results are observed.
Any slip found after the run is disclosed, never edited into a pass.

## 0. Step-0 name check

See NAMECHECK.md in this directory (standing-rules name check written
before this prereg was frozen).

## 1. Lineage

L3C-V2-PARTIAL (prereg 9e595301a, implementation in 20705ab5a): recursive
build_chain, compositional disc2 over full history, deferred construction
(EVID_MIN=2), ambiguity representation, principled observation memory.
Honest ceiling: bounded L2 at most; no L3 claim; no Criterion-0 claim.

L3C-V2-ADV-SURVIVES-THIS-ROUND (prereg 2c0e52739, results 8b82a836a):
round-1 adversary. F1 depth-3 successive refinement composes (D1->D2->D3,
4/4). F2 disjunction blind spot: 3x HONEST_FAIL, declare-and-withhold works;
OR is a permanent by-design blind spot of disc2. F3 default-edge refine
works (5/5). All frozen predictions matched 3/3.

This round attacks the two fronts round-1 named: (a) simultaneous
competing refinements on different edges of the same DISP node (two live
nested-clash records racing on sibling edges); (b) a mixed-output check
after a refine chain is built, plus a depth-4 extension.

## 2. Static audit findings (analyzed and closed; not empirical families)

I read the committed l3c_v2.zag (sha256
4a039420c7830de103fd38585ddf74207c0fbb2ce200a5fc1af5adf02cfe1c50,
identical to the 20705ab5a blob) in full. Three candidate holes were
analyzed and CLOSED by the code; they are recorded here so the empirical
families are not wasted on them:

- (S1) Race-induced record loss: try_refine extracts only the target
  edge's records into SCR_C and compacts all other edges' records forward
  (the w/r compaction loop), then sets nclash_n to the survivor count.
  A refine at one sibling edge cannot drop another edge's live records.
  CLOSED by code reading; the RACE family verifies it empirically.
- (S2) Simultaneous firing: observe() appends exactly one ncl record and
  fires at most one try_refine per call. "Simultaneous" races always
  serialize by arrival order of the second record. There is no concurrent
  path. CLOSED by code reading; the RACE family verifies the serialization
  is coherent (arrival order, no double-build, no misroute).
- (S3) Mixed-output guard coverage: try_construct_root withholds on mixed
  clash outputs (AMBIGUOUS_MIXED); try_refine withholds on mixed edge
  records (REFINE_MIXED). Both guards compare every recorded output
  against the first. CLOSED by code reading; the MIXED family verifies the
  nested guard fires at depth 3 and that the records are consumed.

The empirical families therefore target the untested dynamics in
section 1: cross-edge race serialization and post-chain mixed handling.

## 3. Attack method

Copy the committed l3c_v2.zag mechanism functions VERBATIM (all functions
before fn main at line 701; diff of the copied prefix against the
20705ab5a blob must be empty), append an attack main with two new families
(sigs 704-705) plus structure checks in the builder's style. The committed
mechanism file is never modified; the attack compiles its own copy. Pure
Zag, pinned znc, mode 1, 3 runs byte-identical. The attack main runs ONLY
sigs 704-705 in a fresh binary so node/edge ids are deterministic.

Notation: observe(W,sig,out,f0,f1,f2,f3,mode). All vectors exact.

## 4. Frozen families

### Family RACE (sig 704): competing refines on sibling edges

Purpose: two live nested-clash records race on the two sibling edges of
one DISP node. Does the serialization stay coherent?

Vectors (mode 1):
- Root: (3,0,0,7)->2 twice; (3,1,0,7)->0 twice.
  disc2: unique (f1==1). Builds D1 (node 2): default edge 0 -> TERM(2)
  (node 0), labeled edge 1 (f1==1) -> TERM(0) (node 1). BUILT natoms=1.
- (3,0,0,9)->0: walks edge 0 -> TERM(2), contradicts. ncl(edge0)=1.
- (3,1,0,9)->7: walks edge 1 -> TERM(0), contradicts. ncl(edge1)=1.
- (3,0,5,9)->0: walks edge 0, contradicts. ncl(edge0)=2 -> try_refine
  fires for edge 0. Sub-train: (3,0,0,7)->2 twice (walk edge 0, correctly
  served). disc2: unique (f3==9). Builds D2 (node 4): default edge 2 ->
  TERM(2), labeled edge 3 (f3==9) -> TERM(0) (node 3). Edge 0 re-pointed
  at D2. The compaction preserves edge 1's live record (nclash_n back
  to 1, holding edge 1's record).
- (3,1,5,9)->7: walks edge 1 -> TERM(0), contradicts. ncl(edge1)=2 ->
  try_refine fires for edge 1. Sub-train: (3,1,0,7)->0 twice (walk edge 1,
  correctly served; edge 0's re-pointing does not affect edge 1's walks
  because sibling edges are selected by disjoint predicates at the same
  node). disc2: unique (f3==9). Builds D3 (node 6): default edge 4 ->
  TERM(0), labeled edge 5 (f3==9) -> TERM(7) (node 5). Edge 1 re-pointed
  at D3.

Frozen predictions:
- Exactly two REFINE trace lines, in arrival order:
  "REFINE sig=704 edge=0 natoms=1 a0=(3,0,9)" FIRST,
  "REFINE sig=704 edge=1 natoms=1 a0=(3,0,9)" SECOND.
- Edge 1's pre-refine record survives edge 0's refine: edge 1's refine
  fires on its 2nd record (no 3rd record needed). Observable: exactly two
  REFINE lines total for sig 704, no extra contradiction needed.
- built delta for sig 704 = 3 (1 root + 2 refines); unresolved delta = 0;
  ambig_events delta = 0.
- Eval 6/6: (3,0,0,7)->2, (3,1,0,7)->0, (3,0,0,9)->0, (3,0,5,9)->0,
  (3,1,0,9)->7, (3,1,5,9)->7.
- Structure: D1's default edge target has kind==2 (DISP); D1's labeled
  edge target has kind==2 (DISP); D2's labeled edge atom is (3,0,9);
  D3's labeled edge atom is (3,0,9); no edge re-pointed twice
  (no double-build).

Honest bar: match -> the race serializes coherently; the design's
sequential firing plus record-preserving compaction handles sibling
competition. Any dropped record (edge 1 needing a 3rd contradiction),
double-build, misrouted eval, or wrong-order incoherence ->
L3C-V2-ADV2-BREAK.

### Family MIXED (sig 705): mixed-output check after a refine chain

Purpose: after a depth-3 refine chain is built, (M1) contradict the
deepest leaf with MIXED outputs (withhold expected), then (M2) contradict
it with consistent outputs differing in a fresh feature (depth-4
extension expected).

Vectors (mode 1), chain phase (replicates round-1 F1):
- Root: (3,0,0,7)->2 twice; (3,1,0,7)->0 twice. Builds D1 (node 9):
  default edge 6 -> TERM(2) (node 7), labeled edge 7 (f1==1) -> TERM(0)
  (node 8).
- Refine 1: (3,1,0,9)->7, (3,1,5,9)->7. Sub-train (3,1,0,7)->0 twice.
  disc2 unique (f3==9). "REFINE sig=705 edge=7 natoms=1 a0=(3,0,9)".
  D2 (node 11): default edge 8 -> TERM(0), labeled edge 9 (f3==9) ->
  TERM(7) (node 10). Edge 7 re-pointed at D2.
- Refine 2: (3,1,2,9)->3 twice. Sub-train (3,1,0,9)->7, (3,1,5,9)->7
  (walk edge 9, correctly served). disc2 unique (f2==2).
  "REFINE sig=705 edge=9 natoms=1 a0=(2,0,2)". D3 (node 13): default
  edge 10 -> TERM(7), labeled edge 11 (f2==2) -> TERM(3) (node 12).
  Edge 9 re-pointed at D3.

M1 (mixed withhold at deepest leaf edge 11):
- (3,1,2,9)->5: walks edge 11 -> TERM(3), contradicts. ncl(edge11)=1.
- (3,1,2,9)->6: walks edge 11, contradicts. ncl(edge11)=2 -> try_refine
  fires; the two records have outputs 5 and 6 -> mixed -> REFINE_MIXED,
  unresolved++, no re-pointing, records consumed.

M2 (depth-4 extension at edge 11):
- (8,1,2,9)->5: walks edge 11 (f1==1, f3==9, f2==2) -> TERM(3),
  contradicts. ncl(edge11)=1.
- (9,1,2,9)->5: walks edge 11, contradicts. ncl(edge11)=2 -> try_refine
  fires. Records consistent (both out 5). Sub-train: (3,1,2,9)->3 twice
  (walk edge 11, correctly served). disc2: level 1 finds no single
  equality (f0 8/9 split, rest tie); level 2 finds no conjunction;
  level 3: cmin(f0)=8 > tmax(f0)=3 -> unique (f0 GE 8).
  "REFINE sig=705 edge=11 natoms=1 a0=(0,1,8)". D4 (node 15): default
  edge 12 -> TERM(3), labeled edge 13 (f0>=8) -> TERM(5) (node 14).
  Edge 11 re-pointed at D4. Chain depth 4.

Frozen predictions:
- Trace lines in order: "REFINE sig=705 edge=7 natoms=1 a0=(3,0,9)",
  "REFINE sig=705 edge=9 natoms=1 a0=(2,0,2)",
  exactly one "REFINE_MIXED sig=705",
  "REFINE sig=705 edge=11 natoms=1 a0=(0,1,8)".
- built delta for sig 705 = 4 (1 root + 3 refines); unresolved delta = 1
  (the mixed); ambig_events delta = 0.
- Eval 6/6: (3,0,0,7)->2, (3,1,0,7)->0, (3,1,0,9)->7, (3,1,2,9)->3,
  (8,1,2,9)->5, (9,1,2,9)->5.
- Structure: edge 11's target has kind==2 (DISP, D4); D4's labeled edge
  atom is (0,1,8); D4's default edge target is the old TERM(3).

Honest bar: match -> mixed outputs withhold at depth 3 exactly as
designed, and consistent contradictions extend the chain to depth 4;
recursion composes one level deeper. Any re-pointing during M1, any
withhold during M2, any misroute, or any silent misresolution ->
L3C-V2-ADV2-BREAK.

## 5. Kill bars

- K1: this prereg is committed ALONE before any attack file exists;
  precedence verified with git merge-base --is-ancestor before the result
  commit. No frozen bar in section 4 may be weakened after results. A
  pre-implementation arithmetic slip, if found, is corrected by a dated
  prereg amendment committed before the attack file, never after results.
- K2: Families RACE and MIXED run against the frozen predictions of
  section 4 with the committed mechanism unmodified (verbatim copy,
  diff-verified); all runs 3/3 byte-identical. Verdict mapping: both
  families match frozen predictions with no break bar tripped ->
  L3C-V2-ADV2-SURVIVES-THIS-ROUND; any break bar tripped (dropped record,
  double-build, misrouted dispatch, re-point on mixed outputs, withhold
  on consistent contradictions, silent misresolution) ->
  L3C-V2-ADV2-BREAK, reported with the exact family and mechanism.
- K3: pure Zag at every step (attack copy, build, runs, analysis, byte
  checks); zero Python; no em dashes or en dashes (shell-only
  check_no_dash.sh on every committed document); the committed
  l3c_v2.zag unmodified; the prohibited paper untouched (verified empty
  diff).

## 6. Anti-widening note

This is an attack, not a builder: no mechanism change is proposed or made.
If a family breaks, the recommendation will be a redesign direction or
retirement, never a per-family patch. The v1 emergence claim stays retired
regardless of outcome; no L3 or Criterion-0 claim is in scope.
