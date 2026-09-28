# RUNLOG — M1 Bar Calibration (PAM Round 3, Crew 7)

**Prereg:** `prereg/PREREG_M1_BAR.md` — committed alone as
`e0d96b7f78de7d485f8ed2fb6134d3e011a89f2d` before any fixture/build/output.
**Branch:** `tnn-native-lab` (sylorlabs/TNN).

## Fixture generation (glue, never the instrument)

`gen_m1.py` derives `m1_cases.txt` deterministically (zero RNG) from the three
frozen sources pinned in the prereg:

| source | sha256 (verified at read) |
|---|---|
| `~/workspace/pam_round2/o1_delivery/sweep.jsonl` | `4163fffa65f18f552d48f7efec0e9800a7406547a27c6259d39a48ec7f0833f2` |
| `~/workspace/pam_round2/d1_stack/rec_install.records` | `c26ac9743b8c079e782cdf8511caf2350f653556ac11ac70dfda03720c17c4ad` |
| `~/workspace/pam_round2/cc1_guard/prereg/gen_guard.py` | `49eef7b169790207dd53b140a3586144fe34a8b99a134e18d2244702ae2c214b` |

`m1_cases.txt`: 2,241 rows (C=1102, W=12, P=18, B=1109), 9 pairs,
sha256 `5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611`.
Row counts match the prereg's frozen assertions (1102/12/18/1109); the 12
TMB-5 rows are rec_install.records seq 24–35 (RICH vs DARK/BRIGHT, conf
764–832); the 9 CC1 pairs are cells CC1, CC1-V1…V8 trials idx 2,3
(jcode=2 ≠ truth=3), byte-verified against the prereg's pair table
((718,382)+(704,358) ×6 [CC1,V1,V2,V3,V7,V8], (850,382)+(840,358) [V4],
(718,6600)+(704,6603) [V5], (718,6600)+(704,358) [V6]).

## Build

Toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
`m1_grid.zag` + byte-identical copy of `R33_NATIVE_IO_V1.zag`
(sha `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
Build warnings only (benign, same class as prior crews): A0101 off-by-one
advisory in `field` (guarded by `i < llen`), A0102 discarded `nio_close`.
Binary → `build/m1_grid` (NOT committed).

One source fix during build (pre-run, no results existed): the P-row
field-index block mis-mapped strong/agree columns; corrected before the first
run. No threshold, grid, or kill-bar logic changed — the prereg's §6
algorithm is implemented verbatim.

## Runs (3×, byte-identical)

```
./build/m1_grid m1_cases.txt > evidence/runN.txt   (N=1,2,3)
```

stdout sha256 ×3: `9c8df89a7e53b9831cc4b8107076c6c3731897c18dad6ea5274bf2d7dc9e980c`
(run1 = run2 = run3, byte-identical). Zero RNG. See `evidence/DIGESTS.txt`.

## Reported numbers (from run1.txt; scorer reproduced all 18)

| metric | baseline (700,0,1,1) | optimized (0,0,705,3588) |
|---|---|---|
| true-PASS | 826/1102 = 74.95% | **910/1102 = 82.58%** |
| C1 violations (12 TMB-5) | 12 | 0 |
| C2 violations (9 CC1 pairs) | 9 | 0 |
| broad-wrong false-PASS (1109) | 7 | 712 |
| trial 1145 | PASS | PASS |

Kill bar KB-M1 (RK-3 ≥ 82%, i.e. ≥904/1102): 910 ≥ 904 → **SURVIVE**.

## Independent scoring

`score_m1.py` (Python mirror of prereg §6, never the instrument): all 18
Zag-reported numbers reproduced exactly, including the independent exact
sweep agreeing on the optimum (ST,AT,CT,MT)=(0,0,705,3588). Exit 0.
