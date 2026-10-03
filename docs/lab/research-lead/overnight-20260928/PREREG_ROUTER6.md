# PREREG_ROUTER6: H-ROUTER6 Contested-Anchor Repair

**Date:** 2026-09-29
**Status:** FROZEN (before any implementation)
**Parent:** H-ROUTER5 DOWNGRADED by red team (X-R5-2b anchor pollution,
X-R5-2c summary honesty)

## Background

H-ROUTER5 added `audit_task_family`, a within-curriculum consistency check
anchored on the curriculum's own query marks. The red team demonstrated:

- X-R5-2b: 2 injected disagreeing query marks ("zzz" marked CQ, "9,9,9"
  marked PQ) make both content-type anchors UNKNOWN via the all-agree rule.
  Both family checks are skipped; tfam=0, mergers_mask=0, sfanom=0. Full
  system silence on the exact SWAP curriculum the repair was built to
  catch, with corruption probes confirming genuinely swapped routing.
- X-R5-2c: single-sided pollution (s0=1-only swap + "zzz" CQ) yields tfam=0
  with "no-task-family-inconsistency" emitted while four swapped s0=1
  learn marks sit present-but-unchecked. The summary line overstates what
  was verified.

No frozen kill bar was broken (K-R5-1 still passes on the un-polluted
SWAP), so this is claim-narrowing (DOWNGRADE), not a kill.

## Repair (H-ROUTER6)

**R1: Contested anchors are findings, not silent UNKNOWN-skips.**

`audit_task_family` tracks a contested flag per content type (a1c, a2c).
When query marks for a content type disagree on family, the anchor stays
UNKNOWN (there is no honest anchor to check against, and checking against
an arbitrary family would manufacture verdicts), but the disagreement is
emitted LOUD as `ANCHOR-CONTESTED: qk=<k> ...` and recorded in the return
value: bit2 = qk=1 contested, bit3 = qk=2 contested. The learn-mark checks
for a contested type are skipped (no anchor exists), but the contested
state itself is a finding. This converts the 2-item pollution from a
silencer into a tripwire.

Return-bit semantics (extended, all prior bits unchanged):
- bit0: s0=1 learn inconsistency fired (unchanged)
- bit1: s0=2 learn inconsistency fired (unchanged)
- bit2 (NEW): qk=1 anchor contested
- bit3 (NEW): qk=2 anchor contested
- bit5 (NEW): summary "task-family-anchor-missing" emitted
- bit6 (NEW): summary "task-family-check-partial" emitted
- The all-clear summary "no-task-family-inconsistency" is NOT encoded in
  the return value (preserves K-R5-2a `tfam1==0`).

**R2: Honest summary line.**

`no-task-family-inconsistency` is emitted ONLY when every content type that
carries learn marks (s1>=2, PL/CL) has a known, uncontested anchor and all
checks pass. Otherwise:
- any contested anchor -> emit
  `task-family-check-partial: anchor contested; learn marks for the
  contested type unchecked` (bit6)
- anchor missing for a content type that carries learn marks -> emit
  `task-family-check-partial: anchor missing for a content type with learn
  marks; those marks unchecked` (bit6)
- both anchors missing (a1n==0 and a2n==0) -> keep
  `task-family-anchor-missing` (bit5, unchanged behavior)

This fixes the X-R5-2c overstatement and its missing-anchor sibling: the
all-clear line can no longer appear while marks sit unchecked.

## What is NOT changed

- Induction machinery, `compile_thresholds`, `audit_merger`,
  `audit_single_family`, `audit_manifest`, `audit_replay`: untouched.
- The anchor collection rule (all-agree), the check predicates
  (`s0==1 && a1!=0 && f!=a1`, `s0==2 && a2!=0 && f!=a2`), the per-mark
  TASK-FAMILY-INCONSISTENCY lines: unchanged.
- All routing behavior: unchanged.
- The coherent-relabeling boundary (disclosed honest boundary #3) stands:
  a curriculum whose query anchors consistently re-label families is
  internally consistent and remains undetectable by any within-curriculum
  check. H-ROUTER6 does not claim otherwise.

## Frozen kill bars

**K-R6-1 (pollution caught):** F-P1 fixture: X-R4-1 SWAP learns + honest
queries + "zzz" (features (0,1,1)) marked CQ + "9,9,9" (features (0,1,2))
marked PQ (exact X-R5-2b attack). PASS iff: ANCHOR-CONTESTED emitted for
qk=1 AND for qk=2; `(tfam5 & 12)==12` (both contested bits); `(tfam5 &
3)==0` (learn checks for contested types skipped, not fabricated);
`(tfam5 & 64)!=0` (partial summary, not the all-clear line). The router5
silence signature (tfam==0 with anchor-missing only) must be gone.

**K-R6-2 (summary honesty):** F-P2 fixture: s0=1-only swap (s0=1 learns ->
CL, s0=2 learns honest CL; i.e. run_induction gamed=1) + honest queries +
"zzz" marked CQ (exact X-R5-2c attack). PASS iff: ANCHOR-CONTESTED emitted
for qk=1; `(tfam6 & 4)!=0`; `(tfam6 & 3)==0`; `(tfam6 & 64)!=0`
(task-family-check-partial emitted); and the raw output for the F-P2
diagnostic block contains no "no-task-family-inconsistency" line
(verified by inspection of the committed raw output).

**K-R6-3 (no regressions):** All of the following hold on the four frozen
sections (honest / X-R1 / confined / SWAP) with the modified
`audit_task_family`: K-R5-1 (`(tfam4 & 3)==3`), K-R5-2a (`tfam1==0`),
K-R5-2b (`(tfam2 & 1)==1` and CL merger intact), K-R5-2c (`(tfam3 & 1)==1`
and sfanom3==1), K-R4-1, K-R4-2, K-R4-3, K-R4-4, K-R4-5. PASS iff all hold.
Additionally, the diagnostic output of the four frozen sections must be
byte-identical to the committed H-ROUTER5 output for those sections (the
repair adds lines only in contested/partial situations, which do not occur
in the frozen fixtures); verified by diff of the section blocks.

**K-R6-4 (determinism):** 3 consecutive runs of `router6_learn` byte-
identical (md5 comparison). PASS iff identical.

## Test plan

1. Copy `router5_learn.zag` to `router6_learn.zag` verbatim; verify with
   cmp before editing. `router5_learn.zag` must remain unmodified
   (verified by git status / diff at the end).
2. Apply exactly: (a) contested flags + ANCHOR-CONTESTED emissions +
   extended return bits in `audit_task_family`; (b) honest summary logic;
   (c) F-P1 and F-P2 curriculum sections + main() verdict lines for
   K-R6-1/K-R6-2; (d) extended final gate. No other changes.
3. Build with the pinned toolchain (`znc 2026.07.0-dev (edition 2026)`),
   run, verify K-R6-1, K-R6-2, K-R6-3 bars in-program, verify raw output
   contains no all-clear line in the F-P2 block, diff frozen-section
   diagnostic blocks against committed `ROUTER5_RAW_OUTPUT.txt`.
4. Run 3x, compare md5: verify K-R6-4.
5. If any bar fails, H-ROUTER6 is KILLED (do not adjust bars).

## Classification expectation

Bounded L2+ structural learning with provenance diagnostics (unchanged).
The contested-anchor finding is a within-curriculum anomaly signal, not a
correctness oracle. NOT L3.

## Governance

Pure Zag. No Python at any stage. Prereg frozen before implementation.
Commit order: this prereg strictly precedes the implementation commit
(verify with `git merge-base --is-ancestor`). Only owned files staged.
No em dashes in loop docs.
