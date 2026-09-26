# Pricing Forks — Deliverable Manifest

Built 2026-09-26 from the fixed F6 test build
(`~/workspace/strength-f6-wedgefix/`, base commits `de7f59c91`, `20497b8f0`).
Toolchain: pinned znc `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Pure Zag, zero RNG. Every measurement run twice, byte-identical.

## Blind red-team deliverables (the four arms)

| Dir | Binary | Brief | Price law |
|-----|--------|-------|-----------|
| `blind/arm_A/` | `price_rt_a_bin` (212,841 B) | `brief_A.md` | high-water: ceil(HW/25) — control |
| `blind/arm_B/` | `price_rt_b_bin` (212,841 B) | `brief_B.md` | flat: 2 cites, strength-blind |
| `blind/arm_C/` | `price_rt_c_bin` (213,263 B) | `brief_C.md` | variable, dual-scheme (`SCHEME<1\|2>`): JUSTIFY-code brackets / memory age |
| `blind/arm_D/` | `price_rt_d_bin` (212,841 B) | `brief_D.md` | zero-cost: 0 cites |

Each blind dir contains ONLY the binary + its brief. No source.
All four blind binaries verified deterministic (same args → byte-identical
output, 2/2 runs).

Binary SHAs (sha256):
- arm_A/price_rt_a_bin: 8a9576591844d679f43adff9ac09a5934ada8c657431a6365ef15bd800b2b433
- arm_B/price_rt_b_bin: 1a32b9c4347ad9bc219386490488d0f8058e8ef36a09e672a5f9eb2733f0827a
- arm_C/price_rt_c_bin: db088b2c2f68e81106b22330e2e77f35f99d25ebf01cd1809ec690fc31959162
- arm_D/price_rt_d_bin: 6b27a221560083f77770878196e534a7e3e976107f1f496623d73597871ad09e
- price_trial_bin (instrument, not blind): 0c895a3bd7e378679a8a3791d201b1f08bc5b196b330fdef7f817ad90dbb5feb

## Measurement instrument (not blind)

- `price_trial_bin` — unified trial driver: 5 price cells (A/B/C1/C2/D) ×
  ATTACK / HONEST / HONESTF / STRESS. `HONESTF` is the bitset-optimized
  honest driver (identical freshest-citation policy, proven byte-identical
  to `HONEST` on all five 400-episode arms). My instrument, not for the red
  team.

## Source (committed to tnn-native-lab, never main)

- `strength_core.zag` — adds `price_mode`, `st_price`, `st_set_price_mode`
- `strength_checker.zag` — checker recomputes the expected price
- `price_trial.zag` — trial driver
- `price_rt_template.zag` + `gen_drivers.py` — blind driver generation
- `price_rt_<a|b|c|d>.zag` — generated blind drivers
- `DESIGN.md`, `MEASUREMENTS.md`, `MANIFEST.md` (this file)
- `evidence/` — all run logs (attack/honest/stress × arms × 2 runs)

## Evidence index

- `evidence/attack_<ARM>_run{1,2}.txt` — attack battery per arm (2/2)
- `evidence/honest_<ARM>_run{1,2}.txt` — honest 400-episode per arm (2/2)
- `evidence/honest_C2_x10_run1.txt`, `evidence/honest_D_x10_run{1,2}.txt` —
  honest 4000-episode (C2 run1, D 2/2 byte-identical; A/B/C1 X10 attempted
  but not completed — see MEASUREMENTS.md scalability note)
- `evidence/stress_<ARM>_<S8|S16|S32>_run{1,2}.txt` — finite-pool stress (2/2)

## Key results

- Arm A reproduces the F6 G baseline byte-identically (attack + honest-400).
- Attack battery: fail=0 on all arms (no resurrection/double-spend/discount).
- Honest-400 destroys: A 99, B 199, C1 199, C2 386, D 386 (abandons make up
  the rest; c121=0, ckfail=0 everywhere).
- Finite-pool wedge: destroys-before-wedge = pool/price (D never wedges).
- See MEASUREMENTS.md for the full tables and the head-to-head verdict.
