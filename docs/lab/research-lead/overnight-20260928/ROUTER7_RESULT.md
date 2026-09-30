# ROUTER7_RESULT: H-ROUTER7 Total-Table + Single-Segment Family Audit

**Verdict: H-ROUTER7 SURVIVES.** All frozen kill bars pass.
**Frozen prereg:** `PREREG_ROUTER7.md` (commit `34347580c`), strictly before
implementation. No amendments.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER7_RAW_OUTPUT.txt` (sha256
`aa88b563868188530e003b8419ee30069d8fcd5d161bde83adccb7044195bd67`,
3 runs byte-identical via cmp)
**Implementation:** `router7_learn.zag` (`router6_learn.zag` copied
verbatim, cmp-verified, plus exactly the frozen R1/R2 changes, the F-FB/F-S1
fixture sections, and K-R7-1/K-R7-2 verdict lines). `router6_learn.zag`
unmodified.
**Pure Zag. No Python.**

## Kill bar results

**K-R7-1 (fallback preserved): PASS.** F-FB fixture (exact X-R6-3d CAND1
attack: honest curriculum + `ab>1,0`->CL, features (3,1,0)):
- `CONFLICTED action 7 [any] at seq 19 (no single-var split resolves)`
  confirms the test exercises the intended path (the induced [any] entry
  is CONFLICTED, as in X-R6-3d).
- `TABLE-RULE [any]->WITHHOLD (explicit fallback: no induced [any] rule;
  total-table invariant)` is compiled as the terminal rule; TABLE-SIZE 7.
- `FALLBACK-PROBE (3,1,0) -> 10` (WITHHOLD, not silent -1).
- `FALLBACK-ANY-RULE present=1`.
- Under R6 this exact fixture yields zero all-ANY rules and route3
  returns -1 (pilot-verified against the unmodified router6 mechanism).
  The latent table-shape change is now closed: the table is total by
  design.

**K-R7-2 (single-segment family check): PASS.** F-S1 fixture (honest
curriculum + `ab>cd`->CL, features (1,1,0), a single-segment string-pair
learn mark with swapped family):
- `TASK-FAMILY-INCONSISTENCY: s0=1 learn mark #19 CAUS_LEARN (CAUS) vs
  qk=1 query anchor PROC; string-like learn/query families disagree.`
- `single-segment tfam=1` (bit0). Under R6 this fixture emits
  `no-task-family-inconsistency` with tfam=0 (pilot-verified). The
  carried s1>=2 scope boundary is now closed for s0=1/s0=2 learn marks.

**K-R7-3 (no regressions): PASS.**
- K-R6-1: pollution-swap tfam=76 (bits 2,3 contested + partial). PASS.
- K-R6-2: single-side tfam=68 (bit2 contested + partial). PASS.
- K-R5-1: swap tfam=3. K-R5-2a: honest tfam=0. K-R5-2b: gamed tfam=1,
  CL merger intact. K-R5-2c: confined tfam=1, sfanom=1. All PASS.
- K-R4-1 through K-R4-5: all PASS (16/16 regression, 10/10 threshold,
  18/18 replay, no honest false positives, merger intact).
- Frozen-section diff: the six frozen sections (honest, X-R1 gamed,
  confined, SWAP, F-P1 pollution-swap, F-P2 single-side) are
  byte-identical to the committed `ROUTER6_RAW_OUTPUT.txt` EXCEPT for:
  (a) the program banner line (router6 to router7 identifier);
  (b) the `audit_single_family` scope label `learn-marks s1>=2:` to
  `learn-marks s1>=1:` (counts unchanged on all sections: 4/3, 4/3,
  4/0, 4/3, 4/3, 4/3); (c) the SINGLE-FAMILY-ANOMALY message text
  `s1>=2` to `s1>=1` (confined section only, counts unchanged).
  Verified by full diff: no other differences. This confirms R1 never
  fires on the frozen fixtures (every one compiles an induced [any]
  rule) and R2 changes no verdict on them (zero s1==1 learn marks in
  any frozen fixture).

**K-R7-4 (determinism): PASS.** 3 consecutive runs byte-identical
(cmp-confirmed; sha256
`aa88b563868188530e003b8419ee30069d8fcd5d161bde83adccb7044195bd67` x3).

## What was repaired

**Latent table-shape observation (X-R6-3d):** `build_table_rest` now
enforces a total-table invariant. After compiling ACTIVE equality
entries, it scans for an all-ANY rule; if absent, it appends an explicit
terminal `[any]->WITHHOLD` fallback with a loud emit. The router no
longer degrades to a silent -1 when the induced `[any]` entry goes
CONFLICTED. The fallback is a default-deny safety invariant, not an
induced rule; it is appended only when no induced all-ANY rule exists,
so honest-curriculum output is unchanged.

**Single-segment scope boundary:** the learn-mark predicates in
`audit_single_family` and `audit_task_family` (checks and summary) now
use `s1>=1` instead of `s1>=2`. Single-segment learn marks of a content
type are family-checked like multi-segment ones. The s0 in {1,2}
content-type scoping is unchanged; s0=3 (mixed) marks remain out of
scope.

## Honest boundaries (carried, unchanged)

1. Coherent re-labeling of query anchors (disclosed honest boundary #3)
   still evades every within-curriculum check, correctly.
2. Contested anchors are not checked against a plurality family; the
   finding is the contest itself.
3. Reference-free swap detection remains impossible.
4. The explicit fallback does not restore the lost induced rule's
   mark provenance; the manifest shows the fallback with no supporting
   marks, which is honest (it is a safety default, not learned policy).

## Classification

Bounded L2+ structural learning with provenance diagnostics (unchanged).
The total-table invariant is a safety property; the s1>=1 extension is a
diagnostic scope repair. NOT L3.

## Governance

- Prereg `34347580c` strictly precedes implementation (verify with
  `git merge-base --is-ancestor` before commit).
- Pure Zag. No Python at any stage (implementation, fixtures, builds,
  greps, hashes, diffs).
- `router6_learn.zag` unmodified. Only new files: `PREREG_ROUTER7.md`,
  `router7_learn.zag`, `ROUTER7_RESULT.md`, `ROUTER7_RAW_OUTPUT.txt`.
- No binaries committed (builds in /tmp/r7 and /tmp/r7pilot only).
- No em dashes in new docs.
- Fixture dynamics for F-FB and F-S1 were pilot-verified against the
  UNMODIFIED router6 mechanism before the prereg was frozen
  (exploration only; no mechanism code written before the freeze).

## Lineage

- H-ROUTER6 (SURVIVES; red team SURVIVES with two suggested follow-ups):
  contested-anchor finding, honest summary, induction, threshold
  compilation, merger, single-family, and family-consistency diagnostics
  retained; total-table fallback and s1>=1 family audit added.
- H-ROUTER7 supersedes H-ROUTER6 as the routing layer for unified-learner
  work.
- The F-FB (fallback-loss) and F-S1 (single-segment) fixtures are
  retained as regression tests for future red teams.
