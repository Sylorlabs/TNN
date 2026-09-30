# Integration Step A: Retirement of Stale Discovery Copies

Date: 2026-09-30.
Worker: Integration Step A Worker.
Source: Integration Scout INVENTORY.md (e6f140b64), gap G9.

## Action taken

Verified retirement of the five stale single-pass discovery copies.
No file moves performed. No deletions performed.

## The five copies

All under docs/lab/research-lead/overnight-20260928/:

1. sem_l3/proc_learn.zag
   Frozen historical H-PROC v1 experiment (8/8 hidden tests, bounded L2+,
   11/12 L3 criteria). Carries the old single-pass discovery search;
   reproduces the 3-K overfit on uniform-length training.

2. bridge_learn.zag
   Standalone H-BRIDGE experiment (7/7, bounded L2+ binary conditional
   revision). Bridge mechanism now lives in the canonical unified learner.
   Carries the old single-pass discovery search.

3. route_learn.zag
   Standalone H-ROUTER experiment (5/5, bounded L2 structure-inferred
   routing). Router now lives in the canonical unified learner.
   Carries the old single-pass discovery search.

4. integ_learn.zag
   H-INTEG experiment (5/5, bounded L2 integration). Superseded by H-UNIFIED
   (9/9) in the canonical unified learner.

5. sem_l3/proc_cond.zag
   Frozen historical H-CC v1 content-conditional experiment. H-CC is VOID
   as a preregistered claim (K-CC2 voided). Carries the old single-pass
   discovery search.

## Why they are stale

Each carries the single-pass discovery search without the H-GENBIAS N-first
two-pass generality fix. On uniform-length training they inherit the 3-K
overfit (documented as NQ5, unrepaired). The N-first generality bias
(H-GENBIAS, 4/4) exists only in the canonical implementations.

## Retirement mechanism

Each file already carries a SUPERSEDED header (dated 2026-09-29, NQ5),
committed and clean in git. Each header states DO NOT BUILD NEW WORK ON
THIS FILE and points to the canonical implementation. The headers were
verified present and committed on 2026-09-30.

Files were NOT moved to an archive directory. Reason: historical documents
(preregs, result reports, adversary preregs and reports, CANONICAL_STATE.md)
reference these files by path. Moving them would break the historical
record. The SUPERSEDED headers achieve the retirement goal (no new work
built on stale copies) without breaking provenance.

## Canonical replacements (verified)

- docs/lab/research-lead/overnight-20260928/unified_learn.zag
  Contains the H-GENBIAS N-first generality bias (3 markers verified).
  Single canonical discovery + bridge + router in one process.
- docs/lab/research-lead/overnight-20260928/stress_learn.zag
  Contains the H-GENBIAS fix (3 markers verified). Frontier stress copy.

## Verification performed

1. Located all five files by name.
2. Read headers: all five carry SUPERSEDED (NQ5, 2026-09-29) with
   DO NOT BUILD NEW WORK and canonical pointer.
3. Confirmed absence of H-GENBIAS implementation in stale copies
   (only the header comment referencing it).
4. Confirmed presence of H-GENBIAS in both canonical copies.
5. Confirmed git status clean (headers committed).
6. Confirmed historical references exist by path (moving would break them).

## Gap G9 status

CLOSED. The five stale copies are retired via committed SUPERSEDED
headers. The single canonical N-first discovery lives in
unified_learn.zag (and the frontier stress_learn.zag). No new work can
accidentally build on the stale copies without ignoring an explicit
in-file directive.

## Style compliance

No em dashes in this document. No Python used in this task.
