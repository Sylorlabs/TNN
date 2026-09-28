# FORMAL VERDICT — R-4 (B-T3 dose curve)

Crew 4 (marathon) · Track R0 · 2026-09-21 · branch `tnn-native-lab`
Prereg: `units/PREREG_FREEZE.md` FROZEN (Micah signed 2026-09-21).

## Formal bar (extracted programmatically from the frozen prereg — verbatim)

§0 I, **R-4**: "Dose-curve bar: flatness/degradation tolerance across 250 →
8000. Approve."

§2 R0.2, **B-T3 Dose curve**: "flat or non-decreasing across 250 → 8000; no
degradation (tolerance, R-4)."

Run rules (R0.1): 1x only (R-9). Pure Zag, zero RNG in AI decision paths,
N=5 + adversarial perturbations hard gate.

## Formal-leg measurement (fresh rerun, 2026-09-21)

Rebuilt `units/r0/impl/ablation/b_t3.zag` from frozen source with
`znc_linux_x86_64_abed8aa1` (same toolchain as the descriptive pass).
Ran the formal M8 matrix: perturbations 0–4 + repeated perturbation-0,
both legs (recovered parameters leg 0, re-derived leg 1), doses
250 → 500 → 1000 → 2000 → 4000 → 8000.

- Formal gate: **PASS** — 6/6 runs byte-identical (stdout+stderr) per leg;
  expected-value readback probe 0 fails; leg-0 and leg-1 canonical outputs
  byte-identical to the descriptive-pass canonical captures.
- Pure Zag; zero RNG in AI decision paths; env seed 20260921 (environment
  inputs only, never an AI decision).
- Note: one background worker was killed mid-run (leg-0 repeated-p0 at
  dose 4000, file incomplete); the run was re-executed from scratch and
  completed rc=0 with `BT3_DONE`. No partial outputs were used.

## Measured values (formal leg — identical to descriptive pass)

Dual hard-grounding score (/1000) by dose:

| leg | 250 | 500 | 1000 | 2000 | 4000 | 8000 | strictly non-decreasing | max adjacent drop (/1000) |
|---|---|---|---|---|---|---|---|---|
| 0 (recovered) | 950 | 950 | 950 | 950 | 950 | 950 | yes | **0** |
| 1 (re-derived) | 950 | 950 | 950 | 950 | 950 | 950 | yes | **0** |

Compression ratio grows with dose (leg 0: 1234→1898; leg 1: 1184→1219);
ledger saturates at 2048 entries from dose 500 (leg 0) — disclosed in the
descriptive verdict.

## Formal verdict: **UNDECIDED — BLOCKED on Micah's numeric amendment**

The frozen prereg sets **no numeric degradation tolerance**; §0 I R-4 is a
sign-off item ("Approve") whose number Micah has not signed. The descriptive
pass measured max adjacent drop 0/1000 in both legs, and this formal leg
reproduces those measurements exactly — but **nothing in this verdict
asserts a formal PASS against R-4**, because the tolerance does not exist
yet. This is not a silent upgrade of the descriptive pass.

Counterfactual for Micah's ruling (NOT a verdict): under the *proposed,
unsigned* tolerance from the descriptive crew (≤ 25/1000), the measured
battery would pass with full margin (0 ≤ 25).

## Files

- `units/r0/evidence/ablation/verdict_bt2_bt3.md` — descriptive verdict
- `units/r0/evidence/ablation/MANIFEST_BT2_BT3.md` — frozen manifest
- Spec extract: `units/r0/evidence/FORMAL_SPEC_R3_R4_R5.md`
