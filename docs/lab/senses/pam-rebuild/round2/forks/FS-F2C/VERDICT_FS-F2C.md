# VERDICT_FS-F2C.md — "Colorconst Formation Improvement" (FINAL)

**Crew:** FS-F2C. **Date:** 2026-09-24.
**Prereg:** `PREREG_FS-F2C.md`, frozen and committed alone at
`af5fc8cc` BEFORE any eval result existed (verified via GitHub API).
**FINAL: ALIVE** — colorconst EARNS FS-E2 install scope.

## Rule shipped

`f_colorconst_ratio` (pure Zag, integer math, zero RNG): per-pixel
per-channel linear-RGB ratio viewB/viewA dispersion test — "are the two views
related by a global per-channel gain?" LUT gamma inversion (exact inverse of
the generator's gamma), clip exclusion (>=250), dark gate (linear <100),
64-pixel channel minimum, d = sum of per-channel CV^2 x300, DIFFERENT iff
d >= 44. Overflow-proof (num*300 <= 7.96e18 < 2^63-1). Bit-exact: Zag `dstat`
matches the Python reference on **720/720** fixtures.

## Bar results (all PASS)

| # | Bar | Result | Verdict |
|---|---|---|---|
| (a) | colorconst formation accuracy >= 85% on FRESH deterministic draw (n=1200) | **1183/1200 = 98.58%** | PASS (+13.58pp over bar) |
| (b) | no regression: colordisc >= 91.96% | 1004/1080 = 92.96% (= FS-E2 reference exactly) | PASS |
| (b) | no regression: pitchdisc >= 96.92% | 705/720 = 97.92% (= FS-E2 reference exactly) | PASS |
| (b) | no regression: motiondir >= 95.63% | 545/564 = 96.63% (= FS-E2 reference exactly) | PASS |
| (c) | determinism: both eval runs byte-identical | r1/r2 SHA-256 equal on all 4 TSVs | PASS |

Diagnostic reference: the frozen rule re-scored on the same fresh 1200 draw
gives 654/1200 = 54.50% — the improvement delta is **+44.08pp** (98.58 vs
54.50), consistent with the calibration-set delta (98.75 vs 56.81).

## Fresh draw

`fixtures_fresh/`: 1200 fixtures, MASTER_F2C=20260924, stream 401, family 0,
indices 0..1199, frozen R2-7 generator unchanged. 601 SAME_SURFACE / 599
DIFFERENT. MANIFEST.sha256 verified (1200/1200 OK). Drawn AFTER the prereg
commit; the prereg named the seed, so no re-rolling was possible.

## Residual errors (honest accounting)

17/1200 fresh errors. Same understood classes as calibration: dark/low-data
crops (ratio test abstains toward SAME) and heavily clipped crops (clip
exclusion removes the informative pixels). No new error mode appeared on the
fresh draw (98.58% vs 98.75% calibration — no overfit).

## Build provenance

- Source: `src/f2c_form.zag` (+ `src/lut_frag.zag`, `src/R33_NATIVE_IO_V1.zag`);
  only the colorconst formation function differs from FS-E2's independent
  implementation; all other formation functions byte-identical logic.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned). Binary SHA-256:
  `7b3b0255944946a175b3a19b93b985df844bf21daefd05e36b81ec78dd8a8f48`
  (binary NOT committed, per rule).
- Eval: `src/run_eval.py` glue only; `evidence/eval/` holds the 8 scored TSVs
  (r1/r2 x 4 lists), the fixture lists, and the frozen-rule reference TSV.

## Decision

**FINAL: ALIVE.** All three frozen bars pass with wide margins. The
colorconst formation rule (98.58% on a fresh deterministic 1200-draw,
byte-identical reruns, zero regression on the three in-scope tasks) earns
FS-E2 install scope. Micah's standing rule holds: the tests decided.
