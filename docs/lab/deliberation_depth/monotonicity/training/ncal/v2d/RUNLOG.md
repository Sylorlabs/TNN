# RUNLOG — NEC v2 development (m15 / m20 full workup)

- **Date:** 2026-09-25 (PDT)
- **Crew:** NEC v2d coordinator (subagent)
- **Protocol:** `PREREG_NCAL_V2D_FROZEN.md` (frozen BEFORE any run; this commit)
- **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- **Branch:** `tnn-native-lab`, sylorlabs/TNN
- **Scratch:** `~/workspace/nec_v2d/` (binaries, temp TSVs, SHA logs — outside the repo)

## Freeze (this commit)

- `PREREG_NCAL_V2D_FROZEN.md` — full bar set B1–B9 (B8 computed, reported, non-gating), s1/s10/s100 legs, T1–T4 per direction, T4 on m15, m20 redteam characterization, frozen adoption rule.
- `src/nec_v2d.zag` — variant×scale driver (11/15/20 adoption candidates; 21/22 m_g diagnostic controls; 23 m20_ind light-T4).
- `v2d/sim_v2d.py`, `v2d/bars_full.py`, `v2d/gen_scale.py`, `v2d/t2_v2d.py`, `v2d/t13_v2d.py` — analysis scripts.

## Pipeline checks (§1 — MUST pass before scoring)

1. `nec_q1` ids 15/20 on `necc_input.tsv` vs committed `q1/results_q1/` legs (mechs 15/20): 37/37 byte-identical.
2. `nec_v2d` variant 11 vs committed `results_m11/` (s1), `results_scale_10x/`, `results_scale_100x/`: 111/111 byte-identical (validates driver + regenerated scale inputs).

## Runs

(pending)

## Analysis

(pending)
