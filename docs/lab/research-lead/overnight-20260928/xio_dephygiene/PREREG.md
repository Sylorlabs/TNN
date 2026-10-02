# PREREG: XIO DEP-Hygiene Repair (fresh, 2026-10-02)

Worker: TNN research revival worker (watchdog-assigned)
Date: 2026-10-02
Lane: docs/lab/research-lead/overnight-20260928/xio_dephygiene/
Verdict target: XIO-DEPHYGIENE-COMPLETE

Status: FRESH PREREGISTRATION. This file plus NAMECHECK.md (Step 0) are
committed ALONE before any implementation source, driver, assembly,
binary, or run output for THIS prereg exists. An earlier exploratory
pass of this work (2026-10-02, never committed, retained under
exploratory_uncommitted_20261002/ for provenance) informed the design
but counts for nothing as evidence. Pre-prereg design spikes were run
in /tmp only (exploratory, uncommitted, not deliverables); they are
disclosed in section 10 and are not evidence.

## 1. Objective

Repair the two A4c residuals that canonical XIO-IDFIX (commit
e4b25c110, verdict XIO-IDFIX-COMPLETE) explicitly left unrepaired
(its REPORT.md, "Residual bounds (not repaired, per prereg)"):

(a) Stale DEP edges shadowing xio_dep_rel. When a MAP is deleted, its
type-1 DEP edges stay in the edge table. When the allocator reuses
the freed node id for a new MAP, the stale edges can shadow the new
occupant's edges: xio_dep_rel scans edges in id order and returns the
first live-fact target, so a stale edge at a low id wins over the new
occupant's edges. Committed control behavior (xio_idfix/idfix_run1.txt,
T1): post-recycle live-deprel(ad.m1)=81 (stale chain relation) instead
of 82 (the recycled count MAP's relation).

(b) Masked-trial poisoning of the query relation. A masked trial
teaches a fact that contradicts adapter-verified knowledge, and the
fact stands as permanent knowledge: later unmasked queries activate
it. Committed control behavior (idfix_run1.txt, T1):
A4c masked-via-adapter=70 (the masked trial teaches (31,93,70)),
A4c unmasked-true=70 (the poisoned fact was installed; true answer 3).

No new modes, bridges, handlers, protected-core operations, edge
types, or node types. Pure Zag under safebin.

## 2. Repair design (unfrozen xio core only; frozen base byte-untouched)

Base core: the XIO-IDFIX repaired core (xio_idfix/idfix_full.zag lines
1678-1960, contains the XIO-INVALID token check). All changes below
are additive except xio_dep_rel's filter strengthening and xio_query's
masked-trial audit; no signature changes to frozen functions.

L_TOMB (tombstone): new unfrozen fn xio_tomb_edges(W,m) marks every
type-1 DEP edge with from==m as tombstoned (edge field 0 set to -2).
Frozen link_edge seeks from==-1 for free slots, so tombstones are
never recycled; every from==m reader skips them. New unfrozen fn
xio_del_map_rh(W,r) is the hygiene-aware delete: for each live MAP
with field4==r it calls xio_tomb_edges then deactivates (tag -1,
field36=0).

L_LIVE (liveness-validate): xio_dep_rel returns -1 unless m is a live
MAP (field36==1, tag==20). Catches stale edges whose slot was NOT
reused (tombstone and graph filter cannot see these, and the old code
would serve them).

L_GRAPH (graph-target filter): xio_dep_rel follows a type-1 DEP edge
from m only if the edge's target fact is referenced by m's own
executable graph (type-1 edges from the graph's cells, collected by
walking the graph with the xio_oty traversal pattern: guard
true-branch at slot 12, else SEQ link, max 64 steps). Rationale: a
stale edge from a deleted previous occupant points at the OLD
occupant's licensing facts, which the NEW occupant's graph never
references, so id recycling cannot shadow the new occupant no matter
where edge ids landed after frees and reallocations. This replaces an
earlier edge-id-ordering sketch, which the pre-prereg probe showed to
be unsound in general (frozen decay frees type-9 edges and frozen
eviction frees incident edges, so allocation is not append-only; see
section 10). Graphs that reference no facts (pure INC chains, e.g.
t2_asm_sum) keep the original first-live-fact behavior.

Masked-trial protection (unfrozen xio_query): on masked==1 queries,
xio_query snapshots (before the trial section) the verified answers
for the query relation (answers recorded by adapters: tag 40,
field32==qr, any liveness; adapter answers were verified against
expected at XIO-BUILD time) and the live (s,r) fact ids. After every
trial path (rebind_try, mp_run, bootstrap_miss, and the fallthrough),
xio_masked_audit supersedes (type-3 self-edge, which frozen activate
respects) each newly taught live non-superseded (s,r) fact whose
answer contradicts the snapshot (verified knowledge exists and the
taught answer matches none of it), emitting XIO-MASKED-REFUSED
s= r= ans= fact=. The trial's answer is still returned for the current
query; it is never installed as standing knowledge. The snapshot is
taken before the trials because an invalidated adapter's node id can
be recycled by the trial itself (observed in the pre-prereg probe:
adapter 380's tag-40 record was gone after the masked query),
destroying the record the audit needs. Unmasked queries are
unaffected. Masked trials teaching novel or corroborating answers are
unaffected (no contradiction).

prov/masked/audit state are data and control flow, not modes: no new
mode selectors, no bridges, no handlers, no new core semantic cases.

## 3. Fixture constants (frozen for this prereg)

The H-cases replicate the committed A4c fixture (xio_redteam
rt_driver.zag rt_a4c, and xio_idfix idfix_driver.zag t1_a4c):

- Train X (chain MAPs, r=91), train Y (count MAPs, r=92), 30-fact gap,
  Z facts for b=31, query (31,93) builds adapter 380 with
  m1=27 (chain MAP), m2=115 (count MAP), o1=0, o2=1, rel1=81, rel2=82,
  qr=93, ans=2.
- World revision: ev_teach(36,82,39); replacement count facts
  (31,82,41..47) and (7,82,70),(70,82,71); driver-built count graph
  via t2_asm_count promoted over the same fact ids.
- Delete variants: raw rt_del_map_r(W,91) (missed hygiene) and
  hygiene-aware xio_del_map_rh(W,91). First-fit node allocation
  recycles id 27 for the replacement MAP (verified in the probe:
  nm=27, reused=1).
- Masked query: xio_query(W,31,93,-2,1,1). Unmasked: xio_query(W,31,93,3,0,1).
- Table sizes: 1024 node slots, 4096 edge slots (frozen). No RNG.

## 4. H-cases and exact predictions

All H-cases run in a fresh workspace (z_alloc(110656) + tnn2_init).
Predictions below were validated by pre-prereg exploratory spikes
(/tmp only); the frozen bars in section 5 restate the essential ones.

- H0 (liveness unit): setup, raw delete r=91, probe xio_dep_rel(m1)
  BEFORE recycle. Predict -1. (Committed idfix core returns 81 here;
  the old code serves the dead MAP's edges.)
- H1 (hygiene delete): setup, teach replacement, xio_del_map_rh(W,91).
  Predict: type-1 edges from==m1 go 3 -> 0; tombstoned type-1 edges
  (from==-2) become 6 (both r=91 MAPs' edges); recycle promotes nm=27
  (reused=1); xio_dep_rel(ad.m1)=82.
- H2 (raw delete, missed hygiene): setup, teach replacement,
  rt_del_map_r(W,91). Predict: stale type-1 edges from==m1 stay 3
  (NOT tombstoned, proving the graph filter did the work, not the
  tombstone); recycle nm=27; xio_dep_rel(ad.m1)=82 via L_GRAPH.
- H3 (masked audit): setup, raw delete, recycle, then masked query
  xio_query(W,31,93,-2,1,1). Predict: XIO-INVALID id=380 stage=1
  (idfix behavior, unchanged); XIO-MASKED-REFUSED s=31 r=93 ans=70
  fact=<id> emitted; the taught (31,93,70) fact has
  is_superseded==1; qm==70 (trial answer still returned now).
- H4 (unmasked follow-up + poison census): same world as H3, then
  unmasked xio_query(W,31,93,3,0,1). Predict qu==3 (not the poisoned
  70); census of live non-superseded (31,93,70) facts == 0.
  (Committed idfix: qu==70, poison installed.)
- H5a (legitimate learning, unmasked): fresh world; teach
  (11,81,12),(12,81,13),(13,81,14); xio_query(W,11,91,14,0,1) twice.
  Predict 14, 14 (trial promotes; second query activates).
- H5b (contradiction predicate): setup through adapter build; snapshot
  verified answers for r=93 (predict vc==1); xio_contra_snap(va,1,2)
  ==0 (corroborating answer: no contradiction);
  xio_contra_snap(va,1,70)==1 (contradiction); snapshot for r=97
  gives vc==0 and contra==0 (no verified knowledge: no refusal).

## 5. Kill bars (frozen)

- K1 LIVENESS: H0 xio_dep_rel(dead m1)==-1.
- K2 TOMBSTONE: H1 post-hygiene type-1 from==m1 == 0;
  tombstoned type-1 count >= 1; post-recycle xio_dep_rel==82;
  nm==m1.
- K3 GRAPH-FILTER: H2 stale type-1 from==m1 >= 1 after raw delete;
  post-recycle xio_dep_rel==82.
- K4 MASKED-AUDIT: H3 emits XIO-MASKED-REFUSED with s=31 r=93
  ans=70; taught fact superseded==1; qm==70.
- K5 NO-POISON: H4 qu==3; live non-superseded (31,93,70) count==0.
- K6 LEGITIMATE-LEARNING: H5a 14,14; H5b vc==1 and contra
  outcomes 0,1,0 as predicted.
- K7 C229-REGRESSION: dephy_c229 stdout 3/3 byte-identical to
  committed xio_adapters/xio_run1.txt (sha256
  3b10e33ebdbb99d6826b945cd6ffbcb35c99ed17a6f4da3a84fb26d0325c9e98).
- K8 C235-REGRESSION: dephy_c235 stdout 3/3 byte-identical to
  committed xio_harder/xhio_run1.txt (sha256
  6909ba0c576b3204c110e259411cbb71970f3caa39912f812a2d7761188ab51a).
- K9 DETERMINISM: dephy_full 3/3 byte-identical (sha256 recorded);
  K7/K8 runs included (each binary 3/3).
- K10 ARCHITECTURE: frozen base (xio_full.zag lines 1-1677)
  byte-identical before/after (cmp against the committed source);
  0 new modes/bridges/handlers (grep audit of delivered source for
  _MODE, mode_, bridge, handler: no hits except comments documenting
  absence); 0 new protected-core operations, 0 new edge/node types;
  pure Zag under safebin PATH (guard recorded in NAMECHECK.md
  Step 0); pinned compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1.

## 6. Assemblies (all under this lane)

- src/dephygiene_core.zag: idfix core (idfix_full.zag lines 1678-1960)
  plus the section-2 changes (unfrozen). Audited by diff against the
  pristine extract: additive except xio_dep_rel and xio_query.
- dephy_full.zag = frozen base (xio_adapters/xio_full.zag lines
  1-1677, cmp-verified) + src/dephygiene_core.zag +
  src/dephy_driver.zag (new H0-H5 driver, unfrozen).
- dephy_c229.zag = frozen base + src/dephygiene_core.zag +
  original C229 driver verbatim (xio_adapters/xio_full.zag lines
  1925-2109, byte-verified at assembly).
- dephy_c235.zag = frozen base + src/dephygiene_core.zag +
  original C235 driver verbatim (xio_harder/xhio_full.zag lines
  1925-2130, byte-verified at assembly; xhio base lines 1-1677 and
  xhio core lines 1678-1924 are byte-identical to the xio ones).
- Drivers define the ev_query shim the frozen base's internal battery
  references; the battery is never invoked.

## 7. Verdict rule

XIO-DEPHYGIENE-COMPLETE iff K1-K10 all PASS, each 3/3 where runs
apply. Any kill-bar failure, any crash/panic, or any
forbidden-executable invocation yields XIO-DEPHYGIENE-FAIL naming the
failed bar. No bar weakening; amend transparently and re-freeze
instead. VOID-on-sight applies to any prereg edit after the freeze
commit.

## 8. Control baseline (committed, not rebuilt)

The control is the committed XIO-IDFIX T1 run
(xio_idfix/idfix_run1.txt, commit e4b25c110): post-recycle
live-deprel(ad.m1)=81 (stale), A4c masked-via-adapter=70 (poison
taught), A4c unmasked-true=70 (poison installed). The treatment must
show 82, REFUSED+superseded, and 3 respectively.

## 9. Standing constraints

Pure Zag. Unfrozen xio core only; frozen base read-only and
byte-verified. Paper untouched. Nothing pushed (commits local only).
No em or en dashes in deliverable documentation (audited by
worker_snippets/check_no_dash.sh). Do not touch
composition_integration/ (owned by another worker).

## 10. Pre-prereg exploration (disclosed, not evidence)

- Probe 1 (/tmp, unmodified idfix core): mapped the A4c edge-id layout
  (m1=27; stale marker@13/clk=4, stale t1@16-18; new marker@255/clk=63,
  new t1@258-264; first free edge slot 255). Established the fixture
  facts used in section 3.
- Probe 2 (/tmp): falsified the edge-id-ordering generation sketch.
  Frozen decay frees type-9 edges and frozen eviction frees incident
  edges, so allocation is not append-only; id-ordering cannot soundly
  discriminate stale from current edges under first-fit reuse. The
  graph-target filter (L_GRAPH) was designed to replace it.
- Probe 3 (/tmp): falsified live-adapter scanning for the audit. An
  invalidated adapter's node id can be recycled by the masked trial
  itself (adapter 380's tag-40 record was gone after the masked
  query), so the audit snapshots verified answers BEFORE the trials.
- Spike builds (/tmp): the full repaired core plus H-driver and both
  regression assemblies compiled and ran; all section-4 predictions
  held and both regressions were byte-identical 3/3. These spikes
  validated the design; the confirmatory experiment below re-builds
  and re-runs everything from the frozen sources.
- The pre-existing exploratory pass (exploratory_uncommitted_20261002/,
  never committed) informed the design; its binaries and runs were
  not trusted and are not evidence.

## 11. Known boundaries (stated before results)

- L_GRAPH falls back to the original first-live-fact behavior for
  graphs that reference no facts (pure INC chains, e.g. t2_asm_sum);
  the filter only constrains graphs that witness their licensing
  facts. No sum MAPs appear in the H-cases or the regression worlds.
- The masked-audit snapshot covers adapters present (any liveness) at
  query time; an adapter invalidated AND recycled by an earlier query
  leaves no record (pre-existing idfix node-recycling behavior).
- The repair targets the XIO-IDFIX core lineage (xio_adapters
  pipeline). The separately committed XIO-GENERAL core
  (xio_general/xio_core2.zag) is a different fork and is out of scope;
  unifying the forks is an architecture decision for the parent, not
  this experiment.
