# FORMAL VERDICT — R-5 (B-T4 support-gap recruitment)

Crew 4 (marathon) · Track R0 · 2026-09-21 · branch `tnn-native-lab`
Prereg: `units/PREREG_FREEZE.md` FROZEN (Micah signed 2026-09-21).

## Formal bar (extracted programmatically from the frozen prereg — verbatim)

§0 I, **R-5**: "Support-gap floor: minimum hard-battery score across 1–16
exposures. Approve."

§2 R0.2, **B-T4 Support-gap**: "hard-battery score at or above floor (R-5)
across 1–16 exposures; no collapse at 1 exposure."

Run rules (R0.1): 1x only (R-9). Pure Zag, zero RNG in AI decision paths,
N=5 + adversarial perturbations hard gate.

## Formal-leg measurement (fresh rerun, 2026-09-21)

Rebuilt `units/r0/impl/support_gap/sg_b4.zag` from frozen source with
`znc_linux_x86_64_abed8aa1` (same toolchain as the descriptive pass).
Ran the formal M8 matrix: perturbations 0–4 + repeated perturbation-0,
both legs (recovered thresholds leg 0: support_min 3 / margin 2;
re-derived leg 1: support_min 4 / margin 3).

- Formal gate: **PASS** — all 6 runs per leg exit 0 with `SG_DONE`;
  battery rows (256 clean + 128 contested), `SG_FAILS_TOTAL,0`, and M8
  captures (`M8_STORE_IMAGE`, `M8_LEDGER`, `M8_ALLOC_TRACE`) byte-identical
  across all perturbation modes. (The single differing line across modes is
  `M8_PERTURB,<n>`, the perturbation label itself, which differs by
  construction; gate compares battery+capture lines, matching the
  descriptive M8 gate semantics.)
- Canonical outputs byte-identical to the descriptive-pass captures
  (`sg_leg0.log`, `sg_leg1.log`); store images and ledger hashes reproduce
  exactly (leg 0: `d3af4111…4525a` / `563518471`; leg 1: `491af1c4…dbed8` /
  `1232367883`).
- STORESEQ readback probe 0 fails; battery expected-value self-checks 0;
  pure Zag; zero RNG in AI decision paths.

## Measured values (formal leg — identical to descriptive pass)

Clean sub-battery correct-decision rate, per exposure 1–16: **8/8 at every
exposure, both legs.** Recruitment onset exactly on the recovered bars
(leg 0 at e=3, leg 1 at e=4); every recruited chunk verified byte-exact.
Contested sub-battery: **0 recruitments at all 16 exposures, both legs**
(4/4 correct-abstain everywhere; `d2=1` for e<minsup, `d2=2` once support
passes). Controls: covered → `-1`/`d2=4`; archived → `-1`/`d2=5`.

## Formal verdict: **UNDECIDED — BLOCKED on Micah's numeric amendment**

The frozen prereg states **no R-5 floor**; §0 I R-5 is a sign-off item
("Approve") whose number Micah has not signed. The descriptive pass measured
8/8 everywhere, and this formal leg reproduces those measurements exactly —
but **nothing in this verdict asserts a formal PASS against R-5**, because
the floor does not exist yet. This is not a silent upgrade of the
descriptive pass.

Counterfactual for Micah's ruling (NOT a verdict): under the *proposed,
unsigned* floor from the descriptive crew (minimum correct-decision rate
≥ 7/8 per exposure across 1–16 both legs, contested abstention exactly 8/8),
the measured battery would exceed it everywhere.

## Files

- `units/r0/evidence/support_gap/VERDICT_B4_SUPPORTGAP.md` — descriptive verdict
- `units/r0/evidence/support_gap/sg_table.csv` — 384-row per-case table
- `units/r0/evidence/support_gap/b4_m8.json` — gate verdicts
- Spec extract: `units/r0/evidence/FORMAL_SPEC_R3_R4_R5.md` (programmatic
  verbatim extract of the R-3/R-4/R-5 bars from the frozen prereg)
