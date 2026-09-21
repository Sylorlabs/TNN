# FORMAL VERDICT — R-3 (B-T2 causal ablation)

Crew 4 (marathon) · Track R0 · 2026-09-21 · branch `tnn-native-lab`
Prereg: `units/PREREG_FREEZE.md` FROZEN (Micah signed 2026-09-21).

## Formal bar (extracted programmatically from the frozen prereg — verbatim)

§0 I, **R-3**: "Dual≈raw tolerance ε (B-T2) + minimum compression ratio the dual
route must add. Approve both."

§2 R0.2, **B-T2 Ablation**: "`dual_route ≈ raw_active` on hard grounding
(within tolerance ε, R-3) **while adding compression** (minimum ratio, R-3);
**chunk-only is rejected** (must lose to dual/raw on hard grounding)."

Run rules (R0.1): 1x only (R-9). Pure Zag, zero RNG in AI decision paths,
N=5 + adversarial perturbations hard gate.

## Formal-leg measurement (fresh rerun, 2026-09-21)

Rebuilt `units/r0/impl/ablation/b_t2.zag` from frozen source with
`znc_linux_x86_64_abed8aa1` (same toolchain as the descriptive pass).
Ran the formal M8 matrix: perturbations 0–4 + repeated perturbation-0,
both legs (recovered parameters leg 0, re-derived leg 1).

- Formal gate: **PASS** — 6/6 runs byte-identical (stdout+stderr) per leg;
  expected-value readback probe 0 fails; leg-0 and leg-1 canonical outputs
  byte-identical to the descriptive-pass canonical captures.
- Pure Zag; zero RNG in AI decision paths; env seed 20260921 (environment
  inputs only, never an AI decision).

## Measured values (formal leg — identical to descriptive pass)

| leg | raw (/1000) | chunk (/1000) | dual (/1000) | |dual−raw| (/1000) | compression ratio | chunk<dual | chunk<raw |
|---|---|---|---|---|---|---|---|
| 0 (recovered) | 950 | 550 | 950 | **0** | **1.417** | yes | yes |
| 1 (re-derived) | 950 | 250 | 950 | **0** | **1.195** | yes | yes |

## Formal verdict: **UNDECIDED — BLOCKED on Micah's numeric amendment**

The frozen prereg sets **no numeric ε and no minimum compression ratio**;
§0 I R-3 is a sign-off item ("Approve both") whose numbers Micah has not
signed. The descriptive pass measured |dual−raw| = 0/1000 in both legs and
ratios 1.417 / 1.195, and this formal leg reproduces those numbers exactly —
but **nothing in this verdict asserts a formal PASS against R-3**, because
the numeric bar does not exist yet. This is not a silent upgrade of the
descriptive pass.

Counterfactual for Micah's ruling (NOT a verdict): under the *proposed,
unsigned* numbers from the descriptive crew (|dual−raw| ≤ 25/1000,
ratio ≥ 1.2), leg 0 would pass and leg 1 would **fail the ratio bar**
(1.195 < 1.2). The legs disagree at the proposed floor — the number is
genuinely his.

## Files

- Formal rerun outputs: crew-4 scratch (not committed — binaries/logs are
  evidence-intermediate; canonical numbers reproduced byte-for-byte above)
- `units/r0/evidence/ablation/verdict_bt2_bt3.md` — descriptive verdict
- `units/r0/evidence/ablation/MANIFEST_BT2_BT3.md` — frozen manifest
- Spec extract: `units/r0/evidence/FORMAL_SPEC_R3_R4_R5.md` (programmatic
  verbatim extract of the R-3/R-4/R-5 bars from the frozen prereg)
