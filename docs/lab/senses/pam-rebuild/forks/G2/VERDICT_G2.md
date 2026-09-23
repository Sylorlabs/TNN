# Fork G2 — Predictive Residual Percept (PRP): VERDICT

**Date:** 2026-09-22
**Status:** ☠️ **DEAD — killed by its own frozen kill bar**
**Kill trigger:** B5 false-install rate 23.9% > 8% ceiling (50 false installs / 209 installs, adversarial)

## What G2 was

A pure-Zag percept pipeline built on the stationarity prior: "the world
continues as it is." Every fixture is reduced to invariants; a forward
prediction is generated from them; the percept is a 256-byte vector of
signed residuals (prediction vs observation). The executable memory
contract: **INSTALL iff `residual_norm < 24` AND `pred_hash == obs_hash`;
else WITHHOLD**. Retrieval ranks installed memories by
coarse-predicted-byte agreement with the query and modulates confidence
±100 on top-ranked agreement. All judgment rules and thresholds are
Approach A's validated constants (ports, not inventions); G2's innovation
is the invariant→prediction→residual→contract layer.

## Verdict table

| Bar | Requirement | Result | Pass? |
|---|---|---|---|
| B1 viability | mean primary accuracy ≥ 60% | **75.4%** | ✅ |
| B2 head-to-head | vs Approach A, identical 925 fixtures | **G2 75.4% vs A 72.6%** (+2.8 pp) | ✅ G2 wins |
| B3 efficiency | ops & bytes/percept vs A | G2: 8k–9.2M ops, **533 bytes**/percept; A: 8k–4.5M ops, ~31 bytes variable | 📊 reported |
| B4 ablation | contract changes ≥10% of attack decisions AND fewer false installs than no-contract | **50.8%** changed (216/425); **50 vs 132** false installs | ✅ |
| B5 false-install | ≤8% on 425 attacks (per install) | **23.9%** (50/209) | ❌ **KILL** |
| B6 determinism | 60 fixtures × 3 byte-identical; 2×425-record batch × 3 byte-identical; ledger independently re-verified | **PASS** — single-mode 60×3 all byte-identical (180/180 runs); contract batch 3× sha256 `dc0315056d709f0ab5c8a87985d1990fd57d8e0c536bc5522ef4a7deae0070f9`; ablated batch 3× sha256 `fa38a2d9a7d150b0d0d0a6e82c3c758fe9dd79a59bdb0422b0783bcd7018901c`; independent Python FNV-1a-64 recompute 425/425 per-record on both streams (contract `cf4ab3fd62a17a71`, ablated `3582ea7ee3b45ff9`) | ✅ |
| B7 beauty | elegance / artifact check | N/A — G2 emits invariant-space residual vectors, no audio/visual artifacts | ➖ stated |
| Kill: false-install | ≤8% adversarial per install | **23.9%** (50/209) | ❌ **KILL** |
| Kill: integration | ≥85% complete percept+disposition+ledger records | **99.9%** (924/925) | ✅ |

## What died, and why

**The contract is load-bearing. The gate measures the wrong thing.**

G2's memory contract is not decoration: removing it (always-install)
flips 50.8% of adversarial dispositions and causes 132 false installs
instead of 50. The pipeline is viable (75.4% primary, beats Approach A
head-to-head) and deterministic. But the kill bar measures **safety, not
accuracy** — and G2 installed 50 wrong memories under attack (23.9% of
installs):

1. **27× motiondir (51% of motion installs wrong):** the constant-velocity
   prediction is satisfied even when the direction judgment is wrong.
   Reversed videos and dropped frames produce small residuals against the
   "world continues as it is" prior while the 8-way octant readout is
   wrong (adversarial motion judgment accuracy: 37.1%, yet 53 installs).
2. **11× colordisc:** SAME judgments installed on DIFFERENT truth —
   swaps and noise keep invariant-space residuals small while the
   RGB-distance judgment flips wrong.
3. **10× timbredisc:** RICH installed on BRIGHT truth — harmonic attacks
   fool the front-end estimator; the residuals stay small.
4. **2× shapetrans** (on only 4 installs).

Root cause: the contract gates on **predictive consistency** (small
residuals + exact coarse-hash match), but consistency is orthogonal to
correctness. When the front end is fooled, the world still "continues as
it is" in invariant space — residuals stay small, hashes match, and the
contract certifies the mistake with a clean ledger entry. The EPS=24 norm
gate is nearly non-binding (false installs: mean norm 4.6, max 22); the
hash-equality gate does all the work, and it is uneven across tasks:
colorconst withholds 55/60 adversarial (installs 5, 0 false — brutally
strict, discarding correct judgments too: 81.7% judgment accuracy but 5
installs), while motion installs 53/70 with 27 false. The same gate that
starves colorconst of memories poisons motion's.

## What survives

- The **judgment layer is viable**: 75.4% mean primary accuracy clears the
  60% bar and beats Approach A head-to-head (+2.8 pp, entirely on
  pitchdisc: G2 60/60 vs A 50/60 — the ported f0 estimator behaves
  slightly differently from A's, a deviation worth noting).
- The **residual layer is nearly free on images**: +12 ops/fixture on
  colordisc/colorconst/motiondir; the costs sit in pitchdisc (2.0×) and
  shapetrans (3.3×), where the 90°-rotation re-profile and fine residuals
  dominate.
- The **contract mechanism** gates installs mechanically; integration is
  99.9% (1 of 925 harness fixtures produced no record in the first crew's
  sweep — the fixture was never identified, "_TBD which"; an independent
  re-scan with the current binary (2026-09-23) found **0** bad fixtures
  across all 925, and the later `sweeps.json` cache from the frozen
  `eval_g2.py` also shows bad=0. The 924/925 figure is retained as the
  first crew's mechanical record; both figures pass the ≥85% bar and the
  kill outcome is unchanged. For reference, Approach A's one bad fixture
  is identified: `t3_shapetrans/adversarial/p042.img`, rc=1.)

## Honest caveats

- The contract's hash-equality gate is brutally strict: on primaries it
  installs only 29/60 (colordisc), 2/40 (colorconst), 7/90 (shapetrans),
  20/60 (pitchdisc), 49/60 (motiondir), 60/60 (timbredisc) — correct
  judgments are routinely withheld from memory (e.g. colorconst: 35/40
  correct judgments, 2 installs).
- The pitchdisc front-end is not a byte-faithful port of A (60/60 vs
  50/60) — the residual layer's fine-grid or octave handling diverges
  somewhere; not investigated further.
- 1 adversarial harness fixture yields no complete record (bad=1/185,
  same count for A) — counted against integration, ledger-chained as a
  non-install.
- During evaluation (2026-09-23 ~02:00 UTC) an unknown second process in
  this working directory edited `src/g2_sense.zag` (+11 lines/+362 bytes)
  and rebuilt the binary; the rebuild is byte-deterministic from the
  current source (re-verified 2026-09-23: rebuild sha256
  `ae2145f0445588e79be6eb6e5848c1cb6bef39900b5df2d1784e7a7bbdb66b6c`,
  byte-identical to the working binary), and every frozen constant (EPS=24,
  dist thresholds 40 / 150, prototypes 1000/637/414, |dppm|≥5000, timbre
  boundaries 1075/1400/3000, 90°-rotation prediction, the two-condition
  contract rule) was re-audited and is intact. A second `eval_g2.py`
  instance also ran concurrently against the same scratch directory
  (byte-identical inputs → byte-identical outputs; no corruption).
  Independent re-audit (2026-09-23, finalization crew) confirms each
  constant in the current source: `norm < 24` hard-coded in `g2_finalize`
  (`g2_sense.zag`), `dist > 40` (colordisc) / `dist > 150` (colorconst)
  judgment gates, `iabs(ratio-1000/637/414)` prototype comparison
  (shapetrans), `ad >= 5000` pitch boundary, `1075/1400/3000` timbre
  boundaries, `shape_rot_profile` 90°-clockwise mask rotation as the
  shapetrans forward prediction, and the contract disposition
  `disp = (pok==1 && norm<24 && ph==oh)` with the pok flag firing 0 times
  on the eval set (gate behaves exactly as the frozen two-condition rule).
