# ROUTER6_RESULT: H-ROUTER6 Contested-Anchor Repair

**Verdict: H-ROUTER6 SURVIVES.** All frozen kill bars pass.
**Frozen prereg:** `PREREG_ROUTER6.md` (commit `b87eae2a3`), strictly before
implementation. No amendments.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER6_RAW_OUTPUT.txt` (sha256
`4ce8a69eff2dec1fa09fd072f056670fcea7c630cc2caf98332511524eb0abf4`,
3 runs byte-identical via cmp)
**Implementation:** `router6_learn.zag` (`router5_learn.zag` copied
verbatim, cmp-verified, plus exactly the frozen R1/R2 changes, the F-P1/F-P2
fixture sections, and K-R6-1/K-R6-2 verdict lines). `router5_learn.zag`
unmodified.
**Pure Zag. No Python.**

## Kill bar results

**K-R6-1 (pollution caught): PASS.** F-P1 fixture (exact X-R5-2b attack:
SWAP learns + honest queries + "zzz"->CQ + "9,9,9"->PQ):
- `query anchors: qk=1 family=UNKNOWN (n=3) qk=2 family=UNKNOWN (n=3)`
- `ANCHOR-CONTESTED: qk=1 ...` and `ANCHOR-CONTESTED: qk=2 ...` both emitted
- `task-family-check-partial: anchor contested; learn marks for the
  contested type unchecked`
- tfam=76 (bits 2+3 contested, bit6 partial); `(tfam & 3)==0` (no learn
  check fabricated against a nonexistent anchor)
- Corruption probes confirm the attack is real: `zz>yy;xx>ww -> CAUS_LEARN`
  (honest: PROC_LEARN), `3,3,3>3,2;4,4,4>4,3 -> PROC_LEARN` (honest:
  CAUS_LEARN). The router5 silence signature (tfam=0, anchor-missing only)
  is gone.

**K-R6-2 (summary honesty): PASS.** F-P2 fixture (exact X-R5-2c attack:
s0=1-only swap + honest queries + "zzz"->CQ):
- `query anchors: qk=1 family=UNKNOWN (n=3) qk=2 family=CAUS (n=2)`
- `ANCHOR-CONTESTED: qk=1 ...` emitted
- `task-family-check-partial: anchor contested; learn marks for the
  contested type unchecked`
- tfam=68 (bit2 contested, bit6 partial); `(tfam & 3)==0`
- The F-P2 diagnostic block contains zero "no-task-family-inconsistency"
  lines (verified by grep over the committed raw output). The X-R5-2c
  overstatement is fixed.
- System-level state documented: mergers_mask=4096 (the mark-merger still
  fires on the X-R1 shape, as the red team observed).

**K-R6-3 (no regressions): PASS.** All prior bars hold with the modified
`audit_task_family`:
- K-R5-1: swap tfam=3. K-R5-2a: honest tfam=0. K-R5-2b: gamed tfam=1,
  CL merger intact. K-R5-2c: confined tfam=1, sfanom=1.
- K-R4-1..K-R4-5: all PASS (16/16 regression, 10/10 threshold,
  replay 18/18, no honest false positives).
- The four frozen sections' TASK-FAMILY DIAGNOSTIC blocks are byte-
  identical to the committed `ROUTER5_RAW_OUTPUT.txt` (verified by
  section-wise cmp): the repair adds lines only in contested/partial
  situations, which do not occur in the frozen fixtures.

**K-R6-4 (determinism): PASS.** 3 consecutive runs byte-identical
(cmp-confirmed; sha256
`4ce8a69eff2dec1fa09fd072f056670fcea7c630cc2caf98332511524eb0abf4` x3).

## What was repaired

**X-R5-2b (anchor pollution):** `audit_task_family` now tracks a contested
flag per content type. Disagreeing query marks keep the anchor UNKNOWN
(there is no honest anchor to check learn marks against, and checking
against an arbitrary family would manufacture verdicts), but the
disagreement is emitted LOUD as `ANCHOR-CONTESTED` and recorded in the
return value (bit2/bit3). The 2-item pollution is now a tripwire, not a
silencer.

**X-R5-2c (summary honesty):** `no-task-family-inconsistency` is emitted
only when every learn-bearing content type has a known, uncontested anchor
and all checks pass. Contested anchors produce
`task-family-check-partial: anchor contested; ...`; a missing anchor for a
type with learn marks produces `task-family-check-partial: anchor missing
for a content type with learn marks; ...`. The all-clear line can no
longer appear while marks sit unchecked. `task-family-anchor-missing` is
retained for the both-anchors-missing case.

## Honest boundaries (carried, unchanged)

1. Coherent re-labeling of query anchors (disclosed honest boundary #3)
   still evades every within-curriculum check, correctly: the curriculum
   is then internally consistent.
2. Contested anchors are not checked against a plurality family; the
   finding is the contest itself. A curriculum with contested anchors and
   genuinely consistent learn marks will still trip ANCHOR-CONTESTED for
   researcher review (flag, not verdict).
3. Reference-free swap detection remains impossible (carried from
   H-ROUTER5).

## Classification

Bounded L2+ structural learning with provenance diagnostics (unchanged).
The contested-anchor finding is a within-curriculum anomaly signal, not a
correctness oracle. NOT L3.

## Governance

- Prereg `b87eae2a3` strictly precedes implementation (verify with
  `git merge-base --is-ancestor` before commit).
- Pure Zag. No Python at any stage (implementation, fixtures, builds,
  greps, hashes).
- `router5_learn.zag` unmodified. Only new files: `PREREG_ROUTER6.md`,
  `router6_learn.zag`, `ROUTER6_RESULT.md`, `ROUTER6_RAW_OUTPUT.txt`.
- No binaries committed (builds in /tmp/r6 only).
- No em dashes in new docs.
- Toolchain quirk disclosed: `md5sum` in this environment returns the
  empty-file hash for the full 35209-byte output while hashing prefixes
  correctly and agreeing with sha256sum on other files; determinism was
  therefore verified with `cmp` (byte-identical) and sha256. Not a
  research finding; recorded so future waves do not misread it.

## Lineage

- H-ROUTER5 (DOWNGRADED by red team X-R5-2b/X-R5-2c): induction, threshold
  compilation, merger, single-family, and family-consistency diagnostics
  retained; contested-anchor finding and honest summary added.
- H-ROUTER6 supersedes H-ROUTER5 as the routing layer for unified-learner
  work.
- The F-P1 (pollution-swap) and F-P2 (single-side) fixtures are retained
  as regression tests for future red teams.
