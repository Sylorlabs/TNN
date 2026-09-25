# Strength re-trial — verification re-run (2026-09-25)

**Prereg:** `PREREG_STRENGTH_V2.md` (frozen 2026-09-20). **Order:** Micah's
"run it" (2026-09-25). **Method:** fresh rebuild from the frozen trial
sources with the pinned toolchain
(`znc_linux_x86_64_abed8aa1`), full re-execution of the S1 matrix and the
S10/S100 scale legs, byte-compare of every log against the committed
2026-09-20 evidence. Pure Zag, zero RNG.

## Build determinism

- Rebuilt `strength_trial.zag` → binary **byte-identical** to the committed
  2026-09-20 chunked binary (`trial_bin_s100`). Toolchain output is stable
  across the 5-day gap.

## Re-run scope

- S1: all 3 arms (B, C, C-P3) × 3 curricula (VUP, WBS, JI) × 3 variants × 2 runs.
- S10/S100: arm B (sole S1 survivor) × 3 curricula × 3 variants × 2 runs.
- Every cell: exit 0, `ST_DONE`, `ST_INVALID 0`, r1/r2 byte-identical.

## Result

**100/100 evidence logs byte-identical to the 2026-09-20 committed evidence.
0 differences. 0 run failures.**

The 2026-09-20 verdicts reproduce exactly:

| Arm | S1 | S10 | S100 | Standing |
|---|---|---|---|---|
| B (uniform) | survives | survives | survives | sole survivor; control per §8–§9; not promoted (capacity-bound ~21% vs the 95% graded bar) |
| C (hybrid) | KILLED (P2: 470 drops > 64; JI junk 100%) | — | — | killed at S1, does not advance |
| C-P3 (hybrid+expiry) | KILLED (identical: 470 drops; P3 zero effect) | — | — | killed at S1, does not advance |

Cross-leg stability (arm B) re-confirmed: VUP retention 19.3% → 21.1% →
21.3% (capacity ceiling at every leg), WBS revision 100% with median
latency 25, JI implant rejection 100%, junk 0.3% → 0.03% → 0.003%, drops 0.

## What this re-run does not change

Nothing about the verdicts. It is a verification execution: same sources,
same binary (bit-for-bit), same numbers. Its value is that the "run it"
order of 2026-09-25 has now been executed end-to-end against the frozen
prereg, and the evidence still reproduces exactly.
