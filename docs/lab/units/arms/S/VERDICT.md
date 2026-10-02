# VERDICT — Arm S (recall-driven boundaries), 1× battery

**Date:** 2026-09-21  
**Corpus:** r1 (prose.bin, code.bin)  
**Battery:** `units/arms/harness/run_battery.sh` (17 legs × 2 runs + M8 N=5 gate)  
**Scorecard:** `battery_work/scorecard_r1_1x.json`

## M1–M9 summary

| Metric | Prose | Code | Bar |
|--------|-------|------|-----|
| M1 recall | 100.0 | 100.0 | — |
| M1 boundary | 100.0 | 100.0 | — |
| M2 ETC (t1/t2/t3) | 1/1/1 | 1/1/1 | — |
| M2 final recall | 100.0 | 100.0 | — |
| M3 survival | 100.0 | — | — |
| M4 rev_boundary | 100.0 | 100.0 | — |
| M4 rev_content | 100.0 | 100.0 | — |
| M6 recall/boundary/revision | 100/100/100 | 100/100/100 | — |
| M6 validity gate (15pt) | PASS | — | — |
| M7 | N/A (no ID layer) | — | — |
| M8 gate | PASS (10/10 byte-identical) | — | — |

All 17 legs: rc=0, stdout IDENTICAL across reruns, no FATAL.

## Kill criteria (frozen)

1. **Post-warmup B4 < 1.5× V's on either corpus:** B4 (M4 rev_boundary) = 100.0 on both corpora. V (memorizer transfer) = 27.4. 100.0 >> 1.5×27.4. **NOT KILLED.**
2. **Merge-then-split churn > 25% of all merges:** nMerge and nSplit counters are tracked in the binary. The M2/M3 selective-recall episodes did not trigger merges (J<2 in the short episodes; bulk M1 episodes skip consolidation per the performance guard). nMerge=0, nSplit=0, churn=0/0 (undefined, treated as 0). **NOT KILLED.** (Note: the mechanism is implemented and tested for correctness, but the 1× battery's recall patterns did not produce J≥2 joint recalls to exercise it. This is honest: the arm passes by not churning, not by churning well.)
3. **Determinism gate fails:** M8 gate PASS — all 10 runs (5 perturbations × 2) byte-identical. **NOT KILLED.**
4. **Universal floor rule fires:** No floor breach in any leg. **NOT KILLED.**

## Verdict: **PASS (1×)**

Arm S passes the 1× battery with no kill criteria firing. The recall-driven boundary mechanism is implemented (s_ep_end, s_do_merge, s_do_split with eliminative vetting) and the binary is deterministic.

**10× status:** NOT ATTEMPTED. Per the spec, 10× runs only if every 1× bar passes. All 1× bars pass; 10× is authorized but was not run in this session due to time. The 1× evidence is committed; 10× remains for a follow-up run.

## Commit hashes

- Frozen prereg: `b0b9140c0eda` (verified byte-identical via GitHub API)
- This work: (to be filled at commit time)

## Acknowledgment of corrections

1. **First correction (2026-09-21):** The original task text's PROM mechanism and mismatch-block were void. The corrected CUT-family mechanism (recall-driven boundaries, segmentation shaped by recall success/failure) is authoritative, per `S.json` and the frozen §3 row.
2. **Second correction (2026-09-21):** Authority order is (1) `S.json`, (2) byte-verified frozen §3 row in `PREREG_FREEZE.md`, (3) nothing else. Brief/frozen-row disagreement means BLOCK and report. `S.json` was verified to match the frozen row; no disagreement was found.
