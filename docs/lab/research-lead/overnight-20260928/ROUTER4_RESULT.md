# ROUTER4_RESULT: H-ROUTER4 Single-Family Gaming Repair

**Verdict: H-ROUTER4 SURVIVES.** All six frozen kill bars pass.
**Frozen prereg:** `PREREG_ROUTER4.md` (commit `caa884962`), strictly before
implementation. No amendments.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER4_RAW_OUTPUT.txt` (md5
`62c58c749100b7f572c34643fb978ca3`, 3 runs byte-identical)
**Implementation:** `router4_learn.zag` (induction machinery copied from
`router3_learn.zag` untouched; new sections: single-family anomaly diagnostic,
threshold generalization warning, confined-gaming curriculum; updated
`main()`). `router3_learn.zag` not modified.
**Pure Zag. No Python.**

## Kill bar results

**K-R4-1 (confined gaming detected): PASS.** On the X-R3-2 confined-gaming
curriculum (exact fixture ported from `r3_adv.zag`), the run emits:
`SINGLE-FAMILY-ANOMALY: s0=2 has no LEARN task at s1>=2 while s0=1 has 4;
asymmetric learn-task distribution suggests mark suppression.`
The diagnostic fires (sfanom=1).

**K-R4-2 (honest no false positive): PASS.** On the honest 18-item
curriculum, no SINGLE-FAMILY-ANOMALY fires (sfanom=0). Both families have
learn-task marks at s1>=2 (s0=1: 4 PL marks; s0=2: 3 CL marks).

**K-R4-3 (X-R1 merger intact): PASS.** On the X-R1 gamed variant (s0=1
multi-seg -> CL), MARK-MERGER still fires for CAUS_LEARN; honest run stays
silent. The merger diagnostic is unmodified and behaves identically to
H-ROUTER3. The single-family diagnostic does not fire on X-R1 (both families
retain learn tasks), confirming the two diagnostics are complementary.

**K-R4-4 (threshold 10/10): PASS.** nseg=5,6,7,8,9 str>str all route
PROC_LEARN; nseg=5,6,7,8,9 iii>ii all route CAUS_LEARN. Identical to
H-ROUTER3.

**K-R4-5 (regression + replay): PASS.** 16/16 original H-ROUTER2 suite
items route identically; honest replay 18/18. Identical to H-ROUTER3.

**K-R4-6 (determinism): PASS.** Three consecutive runs byte-identical
(md5 `62c58c749100b7f572c34643fb978ca3`).

## What was repaired

**X-R3-2 (merger evasion via single-family gaming):** Two additions.

1. **Single-family anomaly diagnostic** (`audit_single_family`): For each
   s0-family in {1,2}, counts curriculum marks with s1>=2 (multi-seg range)
   and task != WITHHOLD. If one family has learn-task marks and the other
   has zero, emits SINGLE-FAMILY-ANOMALY. This is a structural signal
   requiring no knowledge of "correct" marks. It specifically catches the
   X-R3-2 mark-suppression pattern (s0=2 CAUS_LEARN marks re-marked to
   WITHHOLD, leaving s0=2 with no learn task while s0=1 compiles
   CAUS_LEARN from gamed marks).

2. **Threshold generalization warning:** Every compiled threshold now emits
   `THRESHOLD-GENERALIZATION: [rule] generalizes marks to unobserved s1
   values; amplification not validated, verify marks.` This addresses the
   red team's "worse than silent acceptance" point by making the
   amplification explicit on every compilation (honest and gamed alike).
   Honest, not a false detection claim.

The diagnostic flags; it does not alter compilation or routing.
Faithful-compiler semantics are preserved. The threshold still compiles
from gamed marks (replay remains 18/18 on the confined curriculum), but
the anomaly is now surfaced.

## Honest boundaries (carried from prereg + red team)

1. The mark-merger diagnostic is a cross-family mark-merging detector only.
   The single-family diagnostic catches mark-suppression asymmetry, not all
   single-family gaming (e.g., re-marking within a family that preserves
   learn-task counts would not fire it).
2. Traceability is not detection. The provenance statement ("every routing
   decision is traceable to researcher-supplied marks") holds verbatim; the
   diagnostics report structure, and the researcher judges intent.
3. The threshold generalization warning fires on honest compilations too.
   It is an explicit statement of extrapolation, not a gaming signal.
4. Robustness to single-mark contradictions (X-R3-1, X-R3-1b) depends on the
   inherited contest mechanism from `causal_learn`, which is now documented
   here (was unmentioned in the H-ROUTER3 result doc).
5. Features remain authored; marks remain supplied; threshold preference
   remains a disclosed researcher bias.

## Classification

Bounded L2+ structural learning with threshold vocabulary enrichment and
provenance diagnostics (unchanged from H-ROUTER3). The new diagnostic is a
structural asymmetry detector, not a correctness oracle. NOT L3.

## Governance

- Prereg `caa884962` strictly precedes implementation (verified via
  `git merge-base --is-ancestor` before commit).
- Pure Zag. No Python at any stage.
- `router3_learn.zag` unmodified. Only new files: `PREREG_ROUTER4.md`,
  `router4_learn.zag`, `ROUTER4_RESULT.md`, `ROUTER4_RAW_OUTPUT.txt`.
- No em dashes in new docs.

## Lineage

- H-ROUTER3 (DOWNGRADED by red team X-R3-2): induction, threshold
  compilation, and merger diagnostic retained verbatim; single-family
  evasion repaired by new diagnostic.
- H-ROUTER4 supersedes H-ROUTER3 as the routing layer for unified-learner
  work.
- K-R3-1..K-R3-4 are preserved as K-R4-3..K-R4-6 (renumbered; K-R3-2
  threshold behavior unchanged).
