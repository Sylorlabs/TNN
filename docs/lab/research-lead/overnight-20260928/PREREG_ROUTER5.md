# PREREG_ROUTER5: H-ROUTER5 Task-Family Consistency Repair

**Date:** 2026-09-29
**Status:** FROZEN (before any implementation)
**Parent:** H-ROUTER4 DOWNGRADED by red team (X-R4-1: task-swap evasion)

## Background

H-ROUTER4 added two structural diagnostics: the mark-merger (cross-family
detector) and the single-family anomaly (mark-suppression asymmetry
detector). The red team demonstrated (X-R4-1) that a task swap confined to
the learn-task marks evades both:

- Teaches 1-4 (s0=1 multi-seg str>str): marked CAUS_LEARN (honest: PROC_LEARN)
- Teaches 5-7 (s0=2 multi-seg iii>ii): marked PROC_LEARN (honest: CAUS_LEARN)
- Teaches 8-18: identical to honest.

All four X-R4-1 criteria hold: mergers_mask==0 (each task spans one
s0-family), sfanom==0 (both families retain learn tasks), replay==18/18,
and corruption amplifies to unobserved s1=5 probes. Traceability holds;
detection does not.

## Impossibility note (reference-free swap detection)

A detector with no reference policy cannot distinguish the SWAP curriculum
from a legitimate re-labeling. The honest and SWAP curricula are isomorphic
under the PL<->CL permutation on the multi-seg bins: identical features,
identical distributional shape, only the opaque task labels differ. Any
function of (features, marks) that fires on SWAP but not honest necessarily
encodes a prior about which label belongs where. That prior must come from
the researcher. H-ROUTER5 therefore does NOT claim reference-free detection.
It adds a within-curriculum consistency check anchored on the curriculum's
own query marks.

## Repair (H-ROUTER5)

**R1: Task-family consistency diagnostic (new `audit_task_family`).**

Principle: the PROC/CAUS family assigned to a content type should be
consistent between its query form and its learn form, as expressed by the
curriculum's own marks. The curriculum's query marks serve as the anchor;
the learn marks are checked against them. No external reference table.

Content-type mapping (researcher-supplied feature semantics, disclosed):
- String-like content: plain-string queries (s0=0, qk=1, e.g. "hello") and
  string-pair learn items (s0=1, pk=1, e.g. "abc>cba;xy>yx").
- Triple-like content: plain-triple queries (s0=0, qk=2, e.g. "1,0,0") and
  triple-transition learn items (s0=2, pk=2, e.g. "0,0,0>0,1;1,0,0>1,0").

Task families: PROC = {PROC_LEARN(11), PROC_QUERY(13)};
CAUS = {CAUS_LEARN(12), CAUS_QUERY(14)}; WITHHOLD(10) excluded.

Algorithm:
1. Anchors: for qk in {1,2}, collect tasks of curriculum items with
   s0=0, s1=1, task in {PQ, CQ}. If at least one exists and all agree on
   one family, anchor[qk] = that family. Else anchor[qk] = UNKNOWN.
2. Check: for each curriculum item with s1>=2 and task in {PL, CL}:
   - if s0=1 and anchor[1] known and family(task) != anchor[1]:
     emit TASK-FAMILY-INCONSISTENCY for s0=1.
   - if s0=2 and anchor[2] known and family(task) != anchor[2]:
     emit TASK-FAMILY-INCONSISTENCY for s0=2.
3. Returns 1 if any inconsistency fired, 0 otherwise. Emits
   "no-task-family-inconsistency" when anchors exist and all checks pass,
   "task-family-anchor-missing" when no anchor exists for a checked type.

Expected behavior on frozen fixtures:
- Honest: qk=1 anchor PROC (2x PQ), qk=2 anchor CAUS (2x CQ); s0=1 learn
  PL (PROC) matches; s0=2 learn CL (CAUS) matches. Silent.
- SWAP: s0=1 learn CL (CAUS) vs PROC anchor -> FIRES; s0=2 learn PL
  (PROC) vs CAUS anchor -> FIRES.
- X-R1 variant (s0=1 multi -> CL): s0=1 FIRES (merger also fires, as before).
- Confined (s0=1 -> CL, s0=2 -> W): s0=1 FIRES (single-family also fires
  for s0=2's missing learn marks).

The diagnostic flags; it does not alter compilation or routing.
Faithful-compiler semantics preserved.

## What is NOT changed

- Induction machinery (SPLIT, teach, entries): untouched, byte-identical.
- `compile_thresholds` logic: untouched.
- `audit_merger`, `audit_single_family`, `audit_manifest`, `audit_replay`:
  untouched.
- All routing behavior: unchanged.

## Honest boundaries (disclosed)

1. The content-type mapping (s0=1 <-> qk=1 string-like; s0=2 <-> qk=2
   triple-like) is researcher-supplied feature semantics, not derived by
   the learner. It is a general principle (family consistency per content
   type), not a frozen answer table.
2. Family consistency is a heuristic, not a law. A legitimate curriculum
   could assign string-pairs to the causal learner; the diagnostic would
   flag it for researcher review, which is the intended behavior (flag,
   not verdict).
3. An attacker who re-marks the query anchors consistently with the
   swapped learn marks (a coherent re-labeling of 11 items) evades this
   diagnostic. That evasion is correct behavior: the curriculum is then
   internally consistent, and no within-curriculum check can distinguish
   it from a legitimate policy change. This is the residual fundamental
   limit, disclosed here.
4. If a content type has no query anchor marks, the diagnostic stays
   silent for that type (cannot verify without an anchor).

## Frozen kill bars

**K-R5-1 (SWAP detected):** On the X-R4-1 SWAP curriculum (exact fixture
from `r4_adv.zag` `run_induction_swap`), H-ROUTER5 emits
TASK-FAMILY-INCONSISTENCY for both s0=1 and s0=2. PASS iff the diagnostic
fires on both.

**K-R5-2 (no regressions):** All of the following hold:
  (a) Honest curriculum: no TASK-FAMILY-INCONSISTENCY (silent).
  (b) X-R1 variant: TASK-FAMILY-INCONSISTENCY fires for s0=1; MARK-MERGER
      still fires for CAUS_LEARN (merger behavior unchanged).
  (c) Confined curriculum: TASK-FAMILY-INCONSISTENCY fires for s0=1;
      SINGLE-FAMILY-ANOMALY still fires (s2 missing learn marks).
  (d) K-R4-1 (confined single-family): PASS (unchanged).
  (e) K-R4-2 (honest no single-family false positive): PASS (unchanged).
  (f) K-R4-3 (X-R1 merger intact): PASS (unchanged).
  (g) K-R4-4 (threshold 10/10): PASS (unchanged).
  (h) K-R4-5 (regression 16/16 + replay 18/18): PASS (unchanged).
PASS iff all hold.

**K-R5-3 (determinism):** 3 consecutive runs byte-identical (md5
comparison). PASS iff identical.

## Test plan

1. Build `router5_learn.zag` = `router4_learn.zag` verbatim + R1 addition
   (new `audit_task_family` fn, one call site in main per curriculum
   section, SWAP curriculum fixture ported from `r4_adv.zag`).
2. Verify `router4_learn.zag` untouched (diff).
3. Run honest / X-R1 / confined / SWAP: verify K-R5-1, K-R5-2(a)-(h).
4. Run 3x, compare md5: verify K-R5-3.
5. If any bar fails, H-ROUTER5 is KILLED (do not adjust bars).

## Classification expectation

Bounded L2+ structural learning (unchanged). The new diagnostic is a
within-curriculum consistency check, not a correctness oracle. NOT L3.

## Governance

Pure Zag. No Python at any stage. Prereg frozen before implementation.
Commit order: this prereg strictly precedes the implementation commit.
No em dashes in loop docs.
