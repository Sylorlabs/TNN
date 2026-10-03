# PREREG: H-FALLBACKFIX-1 Repair of R7/R4b/R4c Fallback Kills in Collapsed Composition (UNFROZEN)

Status: FROZEN. This file is committed ALONE before any implementation.
Worker: Composition Fallback Repair Worker (H-FALLBACKFIX-1, RETRY-2).
Date: 2026-10-02. Branch: tnn-native-lab. Local only, never pushed.
Pure Zag. Frozen read only.

## 1. Hypothesis

H-FALLBACKFIX-1: the three unified red-team findings (R7 KILL, R4b/R4c
KILL, R6a BOUND; red-team commit 797d63f2f) transfer to the collapsed
mechanism C234, because the collapse ported the fallback verbatim
(cl_satisfy = cl_fetch OR plen gather) and kept link_edge without
dedup. All three are repairable without new modes, bridges, handlers,
or semantic cases:

(a) R7: gate the plen fallback on EXTRACTION failure
(cl_extract == -1: dead licensing fact), not on walk failure. This
restores the unified mechanism's own documented design intent
(composition_unified/REPORT.md: fallback "when relseq extraction
fails"), which the implementation violated by gating on
cc_satisfy == -1 (extraction OR walk failure).

(b) R4b/R4c: bound branching. After (a), admission is relation
relevant (walk compatible). Defense in depth: walk admitted
candidates order before fallback admitted candidates at each DFS
node (kind ordering), and fallback admissions are capped at 4 per
node (the unsound plen match cannot inflate branching).

(c) R6a: deduplicate type-15 co-use edges at write time in
cb_couse_link (check existing (from,15,to,aux=0) before link_edge).

## 2. Base and inputs (all frozen, read only)

- composition_C/cc_base.zag (1677 lines): world, trial, rebind,
  t2_gather, t2_lu_first, link_edge, promote_graph.
- composition_collapse/cl_patch.zag (382 lines): the kill carrying
  collapsed mechanism. Copied to ff_cl_patch_orig.zag in this
  directory as a frozen reference; never modified, never compiled
  directly.
- composition_collapse/cl_driver.zag: C234 battery protocol
  (T1/T2A/T2B/T3/T4/T5/T4B) reused verbatim for regression.
- composition_unified_redteam/rt_driver_main.zag: R7, R4b, R4c, R6a
  world constructions ported for kill verification.

## 3. Design (frozen)

### 3.1 Repair (a): split cl_fetch, gate the fallback

cl_fetch conflates two failure kinds, both returning -1:

- EXTRACTION failure (cur independent): mark unresolvable, entry
  cell not a guard (102), set cell not a set (101), DEP licensing
  fact missing or dead (tag != 1 or not live).
- WALK failure (cur dependent): t2_lu_first finds no fact from the
  current value along a live extracted relation.

New functions:

- cl_extract(W,m,start,len,rels): resolve the mark entry, walk len
  steps through the fragment chain structure, read each step's DEP
  licensing fact, store relation ng(W,f,24) into rels[i]. Returns
  len, or -1 on any extraction failure. Cur independent.
- cl_walk(W,cur,rels,len,vals,fids): walk the extracted relations
  from cur via t2_lu_first. Returns len or -1. Walk failure is
  rejection, never fallback.
- cl_satisfy(W,m,start,len,cur,vals,fids,kind): cl_extract first.
  If extraction fails (ex < 1), A's plen contract via t2_gather
  (plen len+1, unchanged code), kind=2 on success. If extraction
  succeeds, cl_walk only, kind=1 on success, kind=0 and -1 on any
  failure with NO fallback.

Call sites updated: cl_candidates (collects kind for ordering),
cl_dfs (revalidation; kind buffer discarded).

### 3.2 Repair (b): bound branching

- Primary: (a) makes admission relation relevant. On the R4b
  layered graph this cuts per node candidates from 12 (10 via
  relation agnostic fallback) to 3 (walk compatible only).
- Ordering: cl_candidates orders by (co-use desc, kind asc with
  walk=1 before fallback=2, len desc, edge id asc). The unsound
  plen match is explored only after sound candidates fail.
- Cap: at most 4 fallback admitted (kind=2) candidates per node;
  walk admitted candidates keep the existing 32 total cap. The
  unsound branch cannot inflate search.

### 3.3 Repair (c): type-15 dedup

cb_couse_link checks for an existing type-15 edge with aux == 0
from newM to prevM before calling link_edge; returns 0 without
writing if present. FRAG marks were already deduplicated in
cl_mark; co-use edges were not. LINK14 untouched (R7 false
provenance is fixed by (a), not by dedup).

### 3.4 What is NOT changed

- compose_try pipeline, cl_dfs depth bound (8), auto marking,
  assembly, verification, promotion, ev_query, ev_cq: unchanged.
- No new edge types, node tags, relation literals, modes,
  bridges, handlers, semantic cases. One compose_try definition,
  one call site. No COMPOSE_MODE.
- The fallback still exists and still fires for genuinely
  unextractable fragments (dead licensing facts); it is gated,
  ordered last, and capped, not deleted.

## 4. Drivers and tests

Build: cat cc_base.zag ff_patch.zag ff_driver.zag > ff_full.zag;
compile with pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.

ff_driver.zag contains, each in a fresh workspace:

- V-R7 (kill verification, UNFIXED build = base + ff_cl_patch_orig.zag
  + driver): port of r7_world/r7_test. Expect on unfixed: Z ans=105
  via [M,N] (misattributed), false LINK14 MAP_Z -> M, false
  type-15 N -> M. This confirms the kill transfers to C234.
- R7 (repaired build): same world. Expect: Z ans=105 via [N,P],
  LINK14 only to N and P, type-15 co-use only P -> N, no
  duplicate type-15 triples.
- V-R4B/V-R4C (kill verification, UNFIXED build): layered graph
  worlds ported from r4b_test/r4c_test, MAPs taught via direct
  t2_trial calls (per AGENTS.md worker driver lesson: avoids
  ev_query workspace stall; identical MAP inventory). Run with
  600s timeout. Expect: non termination (timeout), confirming
  the kill transfers.
- R4B (repaired): 3-wide depth-8 layered graph, 63 single link
  MAPs via direct t2_trial, unreachable goal 99999. Expect:
  terminates, ans=-2 (clean decline).
- R4C (repaired): same plus L8 reachable (9008), correct path
  MAPs trained last. Expect: terminates, ans=9008.
- R6A-DEDUP (repaired): A1/B1 1-link MAPs, Z query, then count
  type-15 (from,to,aux) triples for duplicates. Also direct
  double cb_couse_link probe. Expect: zero duplicates.
- R3 (repaired, regression): port of r3_test (A Suite-A). Expect:
  ans=306 (fallback still load bearing where extraction truly
  fails, or walk carries it; either way the capability holds).
- C234 battery (repaired): T1/T2A/T2B/T3/T4/T5/T4B verbatim
  protocol from cl_driver.zag. Expect: byte identical answers
  and segment MAPs to C234 (107/109/111/105, -2, -2, 106;
  segments 13 26 39 / 13 26 39 52 / 13 26 39 52 65 / 27 42 /
  45 58).

The unfixed verification build (V) and the repaired build are
separate binaries from separate full files; the V driver runs
only V-R7/V-R4B/V-R4C.

## 5. Kill bars (all must pass for COMPOSITION-FALLBACKFIX-COMPLETE)

- K1: V-R7 on UNFIXED collapsed mechanism reproduces the kill:
  Z ans=105 via [M,N], LINK14 MAP_Z -> M present, type-15 N -> M
  present. (Kill transfer confirmed.)
- K2: V-R4B and V-R4C on UNFIXED mechanism do not terminate
  within 600s each (timeout kill; output shows training
  completed and Z query started). (Kill transfer confirmed.)
- K3: R7 on REPAIRED mechanism: ans=105, COMP-SEGS n=2 with
  segments [N,P] (the N and P MAP ids from R7-IDS), no LINK14
  from MAP_Z to M, no type-15 N -> M, zero duplicate type-15
  (from,to,aux) triples.
- K4: R4B on REPAIRED mechanism terminates within 300s,
  ans=-2 (clean decline, no hang).
- K5: R4C on REPAIRED mechanism terminates within 300s,
  ans=9008.
- K6: R6A-DEDUP: zero duplicate type-15 triples after Z
  composition; double cb_couse_link writes exactly one edge.
- K7: R3 still PASS (ans=306).
- K8: C234 battery on REPAIRED mechanism: T1 ans=107 segs
  (13 26 39); T2A ans=109; T2B ans=111; T3 ans=105 segs
  (27 42); T4 ans=-2 terminates; T5 ans=-2 terminates;
  T4B ans=106 segs (45 58). All match C234.
- K9: 3/3 runs byte identical stdout per binary (SHA-256 recorded).
- K10: architecture audit: exactly one compose_try definition
  and one call site; 0 COMPOSE_MODE; 0 modes/bridges/handlers/
  new semantic cases; no whole MAP DFS remnants; candidate
  enumeration still consults only type-15 FRAG marks
  (aux != 0) plus co-use discrimination on aux == 0.
- K11: process: pure Zag only; safebin toolchain guard in
  NAMECHECK.md Step 0; `which python3 python` empty; no
  forbidden executable invoked.

## 6. Verdict names

- All bars pass: COMPOSITION-FALLBACKFIX-COMPLETE.
- Any bar missed: BUILD-FAIL (report which bar and the exact
  mechanism: which candidate was admitted, which edge was
  written, which bound failed to hold).

## 7. Method

- Toolchain guard recorded in NAMECHECK.md Step 0 before any work.
- This PREREG.md committed ALONE; commit order self check:
  prereg commit strictly precedes any implementation file.
- Implementation: ff_patch.zag (drop in replacement for
  cl_patch.zag; same public function names), ff_driver.zag,
  verification driver ff_verify_driver.zag for the unfixed build.
- Frozen inputs never modified (read only copies; cmp verified).
- Zero em/en dashes in all documents (byte verified before commit).
- Local commits only with explicit pathspecs. Nothing pushed.
  Paper untouched.
