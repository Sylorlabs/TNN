# C2 K4 Amendment (Transparent)

Date: 2026-09-30.
Result commit amended: f313372d7 (v1 and v2 result files, implementation, run logs).
K4 assessment: b933d553 (verdict C2-K4-FLAGGED).

This document is a transparent amendment to the C2 result files. The
original files are NOT edited. This amendment is the sole correction
mechanism, per the loop rule that inaccuracies are corrected by
transparent amendment, never by silent edit.

## The disclosed violation

The C2 implementer self-disclosed, in the final handoff report, that
during byte-checking for em dashes the implementer invoked:

    python3 -c "pass"

exactly once. Under the literal zero-Python rule this is a K4 violation
regardless of disclosure or harmlessness: any Python invocation at any
stage counts.

## Assessment findings (b933d553)

1. The disclosure appears only in the implementer's handoff report to the
   parent. It is NOT recorded in any committed file.
2. No corroborating artifact exists: no shell history on this machine,
   no Python file in /tmp attributable to the C2 wave, and activity
   monitoring captured no Python activity attributable to the C2 worker.
3. The invocation is provably a no-op: `python3 -c "pass"` cannot read,
   write, or modify any file and cannot alter run outputs or measurements.
4. Runs are genuinely deterministic and byte-identical: v1 run1/run2/run3
   all md5 569c61a1...; v2 run_v2_1/2/3 all md5 d6fc84c0... (verified
   directly). The mechanism source hyp_c2.zag is pure Zag text with no
   Python references; the run logs contain none.
5. The wave verdict is a falsification (C2-F5 FIRES: T1/T3/T4/T5 exceed
   the 1M budget on v2). Nothing is being promoted, so no purity claim
   props up an adoption decision.

## Claims revoked

The following purity claims in the committed files are factually
inaccurate after the disclosure and are hereby REVOKED:

- HYP_C2_RESULT_V2.md line 5: "Implementation:
  hyp_c2_impl/hyp_c2.zag (pure Zag, no Python)."
- HYP_C2_RESULT_V2.md line 143: "K4: PASS. Pure Zag, zero Python,
  zero em/en-dash bytes, 3/3 deterministic."
- PREREG_HYPC2.md line 41: "File: hyp_c2_impl/hyp_c2.zag (pure Zag,
  no Python)."
- PREREG_HYPC2.md line 109: "K4: Pure Zag, zero Python invocations,
  zero em/en-dash bytes, 3/3"
- PREREG_HYPC2.md line 135: "Pure Zag only. No Python anywhere
  (implementation, execution, analysis,"
- PREREG_HYPC2_AMENDMENT_V2.md line 107: "K4: Pure Zag, zero Python,
  zero em/en-dash bytes, 3/3 deterministic."
- PREREG_HYPC2_AMENDMENT_V2.md line 138: "Pure Zag only. No Python
  anywhere. No em dashes (byte-verified). Commits"

The line numbers above refer to the committed text as of f313372d7
(and the earlier prereg commits). The prereg claims were protocol
requirements; the result file's K4 PASS was a purity certification.
Both are revoked as stated: one Python invocation occurred in the wave.

## Wave status

C2 wave status: K4-VIOLATION. The purity certification is revoked.

Measurements stand as evidence, flagged K4-VIOLATION:
- v1: T0 SOLVE, T1 SOLVE (via MOD trick), T2 SOLVE, T3/T4/T5 BUDGET.
- v2: T0 SOLVE, T1/T3/T4/T5 BUDGET, T2 SOLVE, F-SMUG PASS, C2-F5 FIRES.
The hypothesis remains falsified as a bounded discovery mechanism.
The falsification verdict (C2-F5 FIRES) is unaffected because the
violation was a provably no-op disclosure, self-reported, and the
verdict is negative.

## Conditions going forward

1. A clean K4 rerun is required before C2 is promoted, adopted, or any
   canonical claim rests on the wave's purity.
2. The valley-depth battery may still freeze the mechanism files
   (hyp_c2.zag and its compiled binaries); only the wave's purity
   certification is flagged, not the mechanism code.
3. Original files remain unmodified; this amendment is the correction.

## Authorship

This amendment was authored without Python (text authoring only) and
verified byte-free of em and en dashes via shell grep before commit.
