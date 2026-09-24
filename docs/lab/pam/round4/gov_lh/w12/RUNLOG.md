# RUNLOG — PAM GOV-LH CREW 1 (W12 K1 premise, long horizon)

Prereg: `PREREG_GOVLH_W12.md` (frozen; committed alone as
`1b26ca8ab1742e3f1cc147aa134c350e41cb9e3a` on tnn-native-lab).
All work 2026-09-24. Pure Zag instrument, zero RNG, zero wall clock.
Pinned znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Import `R33_NATIVE_IO_V1.zag` byte-identical to the frozen w12 copy
(sha256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).

## Build

`w12_glh.zag` = frozen `w12_budget.zag` with ONLY three capacity
constants changed (fmax 4MB→8MB, ob 2MB→8MB, cap_rows 2048→131072;
verified by diff). Binary `w12_glh` sha256
`4026e73bb4d4c6c6ec33befbaf38ae6b8cbec226b1b33b25fbaab4a2c853e0eb`.

## G1 gate (prereg §2) — PASS

Scaled instrument stdout byte-identical to frozen evidence on frozen fixtures:
- `w12_stream.txt` → `a892f4d97324a08a814ee8737053c9d40f8e8af16c95d5f377cf4db9c3090856` ✓
- `w12_attack.txt` → `389d557327e2d9f5bd109b864f5c1eaa9508908c4a874051473c4e24bc2cd9c1` ✓

## Fixtures (gen_govlh.py, deterministic; SHAs)

| stream | rows | sha256 |
|---|---|---|
| glh_honest_10x.txt | 11320 | c1ef8e068ff10d551129ac73c4e49e73ae660cff48b0aaba662022faf9e60ce8 |
| glh_honest_100x.txt | 113200 | 6295a6d7d1e6064f322feeb1f2fbfab16b4b0beccaef1b58077f2333602a6733 |
| glh_attack_10x.txt | 6271 | b280285d746a2dba967355ccf00a10a2530a07eefce3fbf15fa044d9653fce98 |
| glh_attack_100x.txt | 62701 | 7d04d508802d534999f71e3c2dde52f2ff3a6aad4dd8c1e9b3e119740d1030c4 |
| glh_adv_10x.txt | 12620 | 6a1425f438b3aa401b8928b2390677a784acea5f6825ccc9bb8148acb00d6cd1 |
| glh_adv_100x.txt | 126200 | 3e3364672789769db1cb8f5c9a58baea22abe8553389a810e6d134af4e7336c8 |

Attack target: tape C idx 70 (conf=927, mrgF=19123) — same row as the
frozen attack stream's target (stream row `500|927|19123|1|1|0|0` verified).

DEVIATION (documented, prereg §4): the prereg text said "first 1270/12700
tape C rows with tape-index ≠ target's" for attack trues, but only 1101
non-target C rows exist. The generator cycles the 1101 deterministically
in tape order. Row counts (6271/62701) and every prediction are unaffected.

## Leg 1 — item-level wrong-admit rate at scale (bar only)

Generator arithmetic pre-check (not a run): 20/300 (6.67%), 200/3000 (6.67%).

| battery | wrongs | bar admits | rate | admitted cells |
|---|---|---|---|---|
| frozen (ref) | 30 | 2 | 6.67% | (718,6600)×2 |
| 10x (W 0/120, P 20/180) | 300 | 20 | 6.67% | (718,6600)×20 |
| 100x (W 0/1200, P 200/1800) | 3000 | 200 | 6.67% | (718,6600)×200 |

P-canon rate 2/18 = 20/180 = 200/1800 = 11.11% at all scales. W-dense 0%
at all scales (structural: mrgF ≤ 2373 < 3588). Prediction held exactly.

## Leg 2 — W12 no-backdoor at scale (2× byte-identical each; G2/G3 pass all)

| stream | output sha256 (r1=r2) | ncand | admit | bar_reject | max_defer | quar | W12==bar | re-admitted |
|---|---|---|---|---|---|---|---|---|
| honest_10x | f58480f21e40d15773dd09a20d5e743c7e651a9a362acde4479e0e4cd3c3286d | 9120 | 9120 | 2200 | 0 | 0 | yes | 0 |
| honest_100x | 78e8a9a8d35556cd2a6c6137920687e836b0d28c46834bacd08f2314bdf3fb9e | 91200 | 91200 | 22000 | 0 | 0 | yes | 0 |
| attack_10x | ac4b7477f4f15ef0fae04fc7ebf1495b483c5587d29ccb5e50c3d3c93afa145c | 5521 | 5521 | 750 | 0 | 0 | yes | 0 |
| attack_100x | 133dd6408565769b5ede2854873c34777c1edfbd2a7a693abced558407bc17a9 | 55612 | 55612 | 7089 | 0 | 0 | yes | 0 |

Attack detail: target ADMIT, defer_count 0, price 81 at both scales
(idx 5000 / 50000); B2-analogous kill condition False both scales.
Junk bar-pass: 4508/5000 (10x), 45095/50000 (100x) — junk is not wrongs;
all bar-passed junk admitted (W12 == bar list).

## Leg 3 — adversarial flood (2× byte-identical each; G2/G3 pass)

| stream | output sha256 (r1=r2) | ADV bar/W12 | BND bar/W12 | wrongs end-to-end | W12==bar | re-admitted |
|---|---|---|---|---|---|---|
| adv_10x | 921ff57781cae0673416c5d47594963dcc2ab1eedc9d48c110f4c0a837cc6427 | 1040/1040 | 0/260 | 1060 (1040 ADV + 20 P) | yes | 0 |
| adv_100x | 5b23bfe3645a94557d9b35ebc5700a46342ce4256638c2527b47af656f582acd | 10400/10400 | 0/2600 | 10600 | yes | 0 |

Admitted-wrong (conf,mrgF) distribution (100x): 105 distinct cells —
the 104 ADV cells (100 each) + (718,6600) (200). EVERY admitted wrong
(10600/10600) has conf ≥ 705 and mrgF ≥ 3588. BND (conf 706–730,
mrgF 358/382): 0 admitted — the margin threshold is the operative gate.

## Bar characterization (measured, frozen implementation)

The frozen bar consults only (conf, mrgF): in honest_10x, 2760 C rows
have strong=0 or agree=0; 2390 of them pass on (conf,mrgF) alone and are
admitted end-to-end. strong/agree play no role in the implemented bar.

## Scorer notes

`score_glh.py` had two bugs found during scoring (both fixed before any
number was recorded; instrument and fixtures untouched):
1. ZeroDivisionError on wrong-free streams (attack) — guarded.
2. Wrong tuple index for the cat field in the B2-analogous check — fixed.
G3 (row-for-row mirror match) passed on all 6 streams after the fixes.

## Verdict

`VERDICT_GOVLH_W12.md` — decision-grade evidence summary for Micah's word.
The governance question is NOT resolved by this crew.
