# FROZEN ENGINEERING PREREG: trial-garbage reclamation (ARENA-ENG)

Status: FROZEN. Written before any implementation of the approach.
Date: 2026-10-02 PDT. Lane: ARENA-ENG, wave-20261002-0521pdt.
Lane dir: docs/lab/rsi/runs/wave-20261002-0521pdt/ARENA/
Scope: ENGINEERING ONLY. This lane produces no capability verdicts and no
transfer scores. It produces an engineering design or a falsified approach.

## 1. Diagnosis (measured, see TRIALWALL_DIAGNOSIS.md)

- Sealed transfer refreeze (real frozen TNN-2): T_A steps 0-14 at 28-390ms
  each; step 15 at 72.6s; step 16 at 124.1s; 17+ never completed.
- Instrumented verbatim prototype reproduces it: step-15 marginal ~84s.
- The sum branch NEVER runs in the transfer scenario (d_sumv=0 all steps;
  comb_present<0, no type-8 node exists outside a unit test). The chain
  branch runs zero verifies (no length 3-5 paths). All trial work is in the
  small count/hop branches (~10 tiny graphs per query, all rejected fast;
  d_exec=32 at step 15).
- The wall is trial-garbage accumulation into the fixed 1024-node
  workspace: ~65 nodes/query, never freed; table fills at step ~15
  (nodes=1022); every later alloc_node falls into evict_node; measured
  ~3s per eviction, 28 evictions on step 15. Cost tracks workspace
  fullness, not term values. No branching-factor explosion exists.

## 2. The ONE approach: eager reclamation of dead trial graphs

Modify only the trial subsystem's memory hygiene (no ISA change, no new
opcodes, no new modes, no search-order change):

(a) In `t2_try_verify`: on candidate REJECT (v2==-2), walk the candidate
    graph from its root (SEQ edges + BRANCHEQ field-12 targets + field-8
    literal nodes, the same walk `t2_sig` uses) and free every cell
    (mark node dead). On VERIFY (v2!=-2) free nothing; the success path is
    untouched and promotion proceeds exactly as before.
(b) After each reject, one O(4096) edge sweep kills edges with a dead
    endpoint. This must run per-reject (not per-query): freed indices are
    reused by the next candidate's assembly, and a stale SEQ edge would
    otherwise corrupt its execution (seq_nx scans from slot 0).
(c) In `t2_exec`: free the scratch frame after the result integer is
    computed. The frame is dead after return by construction.
(d) Two new helpers only: the graph walk-free and the edge sweep. No
    other function changes.

Exactness argument (why trial semantics are preserved, not just
"admissible"): a rejected candidate's graph is unreachable from every
live structure by construction (only t2_trial holds `root`; on reject it
is dropped; DEP edges point from trial cells to facts, never the reverse;
no MAP node exists for a rejected candidate). The scratch frame is held
only by t2_exec. The sweep kills only edges with a dead endpoint, and at
sweep time the only dead nodes are freed trial cells/frames, so no live
structure loses an edge. Enumeration order, verify outcomes, promoted
graphs, taught facts, and tried/rejected stats are therefore identical by
construction; the differential test below checks this empirically.

## 3. Falsifiable success criteria (all must hold)

- S1 (wall broken): RECLAIM mode completes transfer T_A steps 0-20 with
  every step under 5s wall and the full 0-20 run under 60s wall. (ORIG:
  step 15 alone ~84s and growing; 0-20 infeasible.)
- S2 (no evictions): d_evict == 0 on every step 0-20 in RECLAIM mode;
  live nodes stay well under 1024 (expected ~10/step: observes + inquire).
- S3 (outcome identity, feasible prefix): on steps 0-14, per-query
  (answer, tried, rejected) byte-identical between ORIG and RECLAIM; the
  SET of taught fact triples (s,r,o) identical; the SET of promoted MAPs
  identical (empty in this scenario). Node/edge COUNTS will differ (less
  garbage in RECLAIM); that is the intended effect, not a divergence.
- S4 (success path preserved): on two success scenarios, RECLAIM matches
  ORIG exactly: (i) sum-branch success, t_p2 pattern (type-8 node planted,
  query (110,41,60) must return 60); (ii) chain-branch success (2-hop
  fact chain, masked query must return the chained value). Compared:
  answer, promoted MAP (s, r, ans, licensing facts, t2_sig graph
  signature), taught fact, tried/rejected stats.
- S5 (purity): prototype remains pure Zag under safebin; zero new
  opcodes, zero new modes/bridges/handlers; diff confined to
  t2_try_verify, t2_exec, plus the two new helpers.

## 4. Verdict mapping

- All of S1-S5 hold: APPROACH-VIABLE. Queue the integration design
  (porting the reclaim helpers into the TNN-3 trial subsystem) for the
  next wave. NOTE: integration into frozen TNN-2 is forbidden (frozen);
  this validates the approach for TNN-3, it does not patch TNN-2.
- Any of S1-S5 fails: APPROACH-FALSIFIED. Record the killing evidence in
  PROTOTYPE_EVAL.md and propose the next approach (candidate: per-query
  edge-sweep with trial-local free-list, or scratch-workspace trial
  assembly with winner-copy promotion).

## 5. Frozen boundaries

- No transfer scoring runs in this lane. No simulated scores as evidence.
- No changes to the frozen TNN-2 binary, the frozen shim, or the protected
  core ISA. The prototype is standalone and never wired into TNN-2.
- Commit discipline: pathspec-only, local only, never pushed. This prereg
  is committed alone; implementation follows in later commits.

FROZEN 2026-10-02 PDT. Implementation begins only after this file is
committed.
