# PREREG: Red Team vs XIO-DEPHYGIENE (fresh, 2026-10-02)

Worker: TNN red-team worker (watchdog-assigned)
Date: 2026-10-02
Lane: docs/lab/research-lead/overnight-20260928/xio_dephygiene_redteam/
Target: XIO-DEPHYGIENE PASS (ledger C308, results commit 5318cbfc9,
prereg c8c811a73, verdict XIO-DEPHYGIENE-COMPLETE)

Status: FRESH PREREGISTRATION. This file plus NAMECHECK.md (Step 0)
are committed ALONE before any attack source, driver, assembly,
binary, or run output for THIS prereg exists. No attack code has been
written; no attack binary has been built or run.

Per Micah's standing rule, every PASS triggers a red team. This
prereg attacks the graph-target filter repair (L_GRAPH: a DEP edge is
followed only if its target fact is referenced by the MAP's own
executable graph) plus the tombstone/masked-audit machinery, exactly
as committed in C308. Fork caveat: the repair targets the XIO-IDFIX
lineage; fork unification is an architecture decision above this
worker's pay grade and is NOT attempted; the repair is attacked as
committed.

## 1. Objective

Determine, per preregistered attack, whether the committed repair can
be broken by adversarial worlds. Verdict is PER ATTACK
(ATTACK-SUCCEEDED or ATTACK-FAILED); there is no global claim. For
each SUCCEEDED attack, propose a minimal guard, implement it, and show
the attack then fails while the C308 K1-K10 arms still pass (no
overreach).

## 2. Background facts (frozen, from the committed C308 source)

All facts below are read from the committed dephygiene sources
(verified by reading, not assumed):

- xio_dep_rel(W,m): L_LIVE (m must be live MAP, field36==1, tag==20);
  then L_GRAPH: follows a type-1 DEP edge from==m only if its target
  fact is referenced by m's own executable graph (walk from
  ng(W,m,20) with the xio_oty pattern, collecting type-1 edge targets
  from graph cells). Graphs referencing no facts (pure INC chains,
  e.g. t2_asm_sum, which writes NO type-1 cell edges) keep the
  original first-live-fact behavior (gn==0 fallback). Edges are
  scanned in id order; the first edge whose target is live (tag 1,
  field36==1) and passes the filter wins; its relation ng(W,to,24) is
  returned.
- xio_tomb_edges(W,m): marks type-1 edges with from==m as from==-2;
  frozen link_edge seeks from==-1 for free slots, so tombstones are
  never recycled and never match from==m.
- xio_del_map_rh: hygiene-aware delete (tombstone, then deactivate).
- promote_graph (frozen): alloc_node (first-fit, zeroes fields on
  recycle), tag 20, field4=r, field20=root, field24=hg(W,24),
  provenance link_edge(W,m,1,fact,0) per licensing fact (clk=0),
  plus type-13/2/6 self edges, plus ev_teach_in(s,r,ans).
- t2_trial (frozen) promotes SUM graphs with their licensing facts:
  promote_graph(W,root,s,r,v2,ff,c) where ff are the summand fact ids
  (t2_gather_sum collects facts with subject s, ANY relation). A sum
  MAP therefore has MAP-level type-1 provenance edges AND a fact-less
  graph (gn==0), so the fallback path is reachable in real operation.
- alloc_node zeroes all fields on recycle; link_edge is first-fit over
  from==-1 slots; decay frees only type-9 edges; evict_node frees
  incident edges of evicted nodes. Allocation is NOT append-only
  (established by the C308 prereg's probe 2).
- Node 0/1 are header nodes; node ids 2..1023; edge ids 0..4095.
- Fact nodes: tag 1, field20=s, field24=r, field28=answer,
  field32=hg(W,0) teach clock. MAP nodes: tag 20, field4=relation,
  field20=graph root, field24=promotion edge count, field36=liveness.

## 3. Attack constructions (frozen)

All attacks run in a fresh workspace (z_alloc(110656) + tnn2_init).
Table sizes 1024 nodes / 4096 edges (frozen). No RNG. The A4c fixture
functions (rt_gap, rt_trainX, rt_trainY, rt_zfacts, rt_del_map_r,
find_fact, setup_a4c, teach_new) are COPIED verbatim from the
committed C308 driver into the attack driver (hashes verified, see
section 8).

A shared tracer, rt_trace_dep(W,m), replicates xio_dep_rel's scan
predicate line for line (same graph-fact collection via
xio_graph_facts, same id-order scan, same liveness checks) and emits
the followed edge's id, from, to, and target relation. Its predicted
return MUST equal the real xio_dep_rel(W,m) return; on any mismatch
the run is VOID for that attack (tracer unfaithful, diagnose, do not
score).

Edge classification: STALE(m) = the set of type-1 edge ids with
from==m recorded AFTER the old occupant's promotion and BEFORE its
deletion. CUR(m) = type-1 edge ids with from==m recorded AFTER the
recycle promotion, minus STALE(m). Classification is by recorded id
sets, never by guessed layout.

### A1: LATE-PROMOTION + DECAY + LOW-RECYCLE (recommended variant)

1. Fresh world. Filler: 200 ev_teach(7000+i, 60+(i%10), 8000+i) for
   i in 0..199 (pushes the edge allocator high).
2. setup_a4c(W) copied verbatim (trains X chain MAPs, Y count MAPs,
   gap, Z facts, builds adapter; ad.m1 = M, the r=91 chain MAP id; 27
   in the no-filler fixture, shifted higher by the 200 filler nodes;
   the actual id is recorded and used for STALE/CUR classification
   throughout; the verdict bar is id-set based and does not depend on
   the specific value). The old MAP's provenance edges land at HIGH
   ids because the filler's type-9 edges have not yet expired when it
   is promoted. Record STALE(M); record F1=find_fact(11,81,12),
   F2=find_fact(12,81,13), F3=find_fact(13,81,14).
3. rt_del_map_r(W,91) (raw delete: missed hygiene).
4. Deactivate F1,F2,F3 (ns field36=0): aggressive id recycling of
   the old licensing facts.
5. Decay pressure: 20 direct decay(W) calls (frees expired type-9
   edge slots at low ids; allocates nothing).
6. ev_teach(W,36,82,39); then 7 count facts (31,82,41)..(46,82,47).
   Verify via find_fact that (36,82,39) recycled F1's id, (31,82,41)
   recycled F2's id, (41,82,42) recycled F3's id; on mismatch the run
   is VOID for A1 (layout assumption broken, diagnose).
7. Build count graph via t2_asm_count over cv=[31,41,42,43,44,45,46,47],
   cf=[c1..c7] (the 7 new count fact ids).
8. nm=promote_graph(W,croot,31,82,7,cf,7); require nm==27 (else VOID).
   Record CUR(27). Emit min/max id of STALE(27) and CUR(27) to show
   the recommended layout (stale high, current low).
9. Call rt_trace_dep(W,27) and the real xio_dep_rel(W,27);
   cross-check equality (else VOID).

Rationale: the stale edges' targets (F1,F2,F3) are now LIVE new
facts (r=82) referenced by the new graph, so the graph filter's
premise is violated for them; only edge-id order (new edges low,
stale high) can save the filter. This tests the repair's claim that
"id recycling cannot shadow the new occupant no matter where edge
ids landed".

ATTACK-SUCCEEDS iff the traced followed edge is in STALE(27) or the
returned relation != 82. ATTACK-FAILS iff the traced followed edge
is in CUR(27) and the returned relation == 82.

### A2: FACT-LESS FALLBACK BOUNDARY

1. Fresh world. Teach (11,81,12),(12,81,13),(13,81,14) -> F1,F2,F3.
2. Build chain graph: t2_asm_chain over values [11,12,13,14] with
   facts [F1,F2,F3]; X=promote_graph(W,root,11,91,14,f,3). X is a
   live chain MAP with provenance X->F1,F2,F3 (type-1, low ids).
3. Build sum graph: t2_asm_sum over vals=[30,40] (total 70, in
   1..900). The assembler writes NO type-1 cell edges (verified by
   reading the frozen source).
4. Teach summand facts (50,82,30),(50,82,40) -> G1,G2. This MUST
   precede the deletion: teaching after the delete would recycle X's
   own id for a fact node.
5. Raw delete X (deactivate tag/field36; stale provenance remains).
   promote_graph(W,sumroot,50,82,70,[G1,G2],2); require the returned
   id == X (first-fit recycle; else VOID). The new occupant is a sum
   MAP: field4=82, MAP-level provenance X->G1,G2 (high ids), fact-less
   graph (gn==0).
6. dr=xio_dep_rel(W,X); emit dr and the from==X type-1 edge id set.

Rationale: t2_trial promotes sum MAPs WITH licensing facts, so this
configuration is reachable in real operation, not just constructible.
The gn==0 fallback keeps the original first-live-fact behavior, so
the stale low-id edges shadow the new occupant's provenance: the A4c
shadowing reintroduced through the fallback.

ATTACK-SUCCEEDS iff dr==81 (the stale occupant's relation).
ATTACK-FAILS iff dr==82, or the construction proves unreachable, in
which case the unreachability argument is frozen here as a bar (it
must name the exact mechanism that prevents the configuration).

### A3: ADVERSARIAL ID REUSE (live-but-wrong target)

1. Fresh world. setup_a4c(W) copied verbatim (m1=27 chain MAP,
   provenance 27->F1,F2,F3 at LOW edge ids 16-18, r=81 facts).
   Record STALE(27); F1=find_fact(11,81,12).
2. rt_del_map_r(W,91) (raw delete).
3. Deactivate F1 (ns field36=0).
4. ev_teach(W,99,94,100); require find_fact(99,94,100)==F1 (node id
   recycled for a live-but-wrong fact, r=94 != 82; else VOID). Node
   F1 now holds a LIVE fact whose relation is wrong for the incoming
   occupant, and it is NOT the original target fact.
5. Teach 6 count facts (31,82,41)..(45,82,46) -> c1..c6.
6. Build count graph via t2_asm_count over cv=[31,41,42,43,44,45,46,99],
   cf=[c1,c2,c3,c4,c5,c6,F1] (F1 last). The new graph references F1.
7. nm=promote_graph(W,croot,31,82,7,cf,7); require nm==27 (else
   VOID). New provenance 27->c1..c6,27->F1 at HIGH ids. Record
   CUR(27).
8. Call rt_trace_dep(W,27) and the real xio_dep_rel(W,27);
   cross-check equality (else VOID).
9. CONTROL (same world): xio_tomb_edges(W,27) applied right after
   step 2 (perfect hygiene), then steps 3-8; require dep_rel==82.
   This proves the stale edge is NECESSARY for any wrong answer.

Rationale: the stale edge 27->F1 (id 16) now points at a live fact
(r=94) referenced by the new occupant's graph, so the graph filter
follows it and returns 94 instead of 82. The K2 pattern is preserved
(id 27 recycled, raw delete) but the target is live-but-wrong, not
the original target fact.

ATTACK-SUCCEEDS iff the traced followed edge is in STALE(27) AND its
target's relation != 82. ATTACK-FAILS iff the traced followed edge
is NOT in STALE(27) (correct refusal of the stale edge).

## 4. Guard-test bars (frozen)

For each SUCCEEDED attack, a minimal guard is proposed, implemented
in this lane, and tested:

- G1: the attack's world is rebuilt with the guard in place; the
  attack must then FAIL per its section-3 bar (same construction,
  same measurements).
- G2: the C308 K1-K10 arms are rerun against the guarded core:
  dephy_full H-cases must reproduce the K1-K6 predictions exactly;
  dephy_c229 and dephy_c235 must be 3/3 byte-identical to the
  committed baselines (sha256 3b10e33e... and 6909ba0c...); every
  binary 3/3 byte-identical across runs (K9); frozen base
  byte-identical, 0 new modes/bridges/handlers, pure Zag (K10).
- G3 (no overreach): the guard must not change behavior on any
  honest world; the K7/K8 byte-identity is the empirical check, plus
  a principled soundness argument in REPORT.md.

Candidate guard directions (not frozen; the prereg freezes only the
bars above): A2, constrain the gn==0 fallback against the MAP's own
promotion relation (field4, which alloc_node zeroes on recycle and
promote_graph writes fresh, so it cannot be stale); A3, the stale
and current edges are content-identical (from,type,to,clk all equal),
so no content-based unfrozen guard can discriminate them and no
id-ordering rule is sound (allocation is not append-only per C308
probe 2); the guard is therefore source-side (tombstone-on-recycle or
generation-tagged provenance), implemented and demonstrated in this
lane, with deployment flagged as a parent architecture decision
because frozen t2_trial calls promote_graph directly.

## 5. Assemblies (this lane)

- src/rt_core.zag: byte-copy of the committed C308
  src/dephygiene_core.zag (hash-verified, never edited in place;
  guard variants are separate files).
- src/rt_attack.zag: the A1/A2/A3 drivers + rt_trace_dep + copied
  A4c fixture functions.
- rt_a123.zag = frozen base (xio_adapters/xio_full.zag lines 1-1677,
  sha-verified dc0e86d4...) + src/rt_core.zag + src/rt_attack.zag.
- Guard variants: src/rt_core_g2.zag (A2 guard), src/rt_core_g3.zag
  (A3 guard) or scratch copies; assembled analogously; the guarded
  K1-K10 reruns reuse the C308 drivers verbatim (boundary-checked).
- Drivers define the ev_query shim the frozen base references; the
  internal battery is never invoked.

## 6. Verdict rule

Per attack: ATTACK-SUCCEEDED or ATTACK-FAILED against the frozen
section-3 bar, each on 3/3 byte-identical runs (sha256 recorded). Any
tracer/real mismatch, any crash/panic, or any forbidden-executable
invocation makes the affected attack VOID (not FAILED): diagnose,
do not score. Never weaken a frozen bar; amend transparently and
re-freeze instead. VOID-on-sight applies to any prereg edit after the
freeze commit.

## 7. Deliverables

NAMECHECK.md, PREREG.md (this file), attack drivers, 3/3
byte-identical runs with sha256 digests, REPORT.md with per-attack
verdicts against frozen bars, guard proposals with control results
(G1/G2/G3), cognition lines touched. Work stays in
docs/lab/research-lead/overnight-20260928/xio_dephygiene_redteam/.

## 8. Standing constraints

Pure Zag under safebin (Step 0). Frozen base read-only and
byte-verified (sha256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6).
C308 files never modified (copies hash-verified before use). Paper
untouched. composition_integration/ untouched. Nothing pushed
(commits local only). No em or en dashes in deliverable docs
(audited by worker_snippets/check_no_dash.sh). Explicit pathspecs.
Never amend shared history. No Python at any step.

## 9. Amendment log (transparent, post-freeze)

- Amendment 1 (2026-10-02, before any attack implementation was
  committed): A2 construction steps 4-5 reordered. Teaching the
  summand facts must precede the raw delete; teaching after the
  delete would recycle X's own node id for a fact, breaking the
  first-fit recycle the attack requires. The ATTACK-SUCCEEDS /
  ATTACK-FAILS bar is unchanged (dr==81 succeeds, dr==82 fails).
  No bar was weakened.
- Amendment 2 (2026-10-02, before any attack implementation was
  committed): A1 step 2 clarified. The 200-node filler shifts ad.m1
  above the fixture's 27; the actual id M is recorded and used for
  STALE/CUR classification. The verdict bar was and remains id-set
  based, so no specific id value is required. No bar was weakened.
