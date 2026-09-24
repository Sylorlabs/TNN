# WS1-A PRELIM — smoke-test leg (2 cells, before full battery)

Date: 2026-09-24 ~15:30 PDT. Prereg: `403906826516f3c76c0a26ff1b60e94a094370d9` (frozen before any run).

## What ran
Fresh Zag binaries built from new deterministic sources (generator S=7, new truth
functions, not the old R27 fixtures). Smoke cells: cap32a0r1 (benign, 384 eps)
and cap128a35r3 (adversarial, 4608 eps). Each binary ran twice in-process;
in-driver determinism digest matched both times (match=1) on every arm.

## Numbers (smoke, preliminary — full battery in flight)

| cell | arm | correct/nt | W/ep | wall ns/ep | notes |
|---|---|---|---|---|---|
| cap32a0r1 | trained | 16/16 | 10.3 | 596 | suppress=0 |
| cap32a0r1 | naive | 16/16 | 10.2 | 432 | collateral=0 |
| cap32a0r1 | auto | 16/16 | 28.4 | 6133 | scan_steps=7264 total |
| cap128a35r3 | trained | 64/64 | 42.3 | 4600 | suppress=540, kill=0 |
| cap128a35r3 | naive | 64/64 | 46.4 | 10021 | collateral=177, spurious=16, kill=752 |
| cap128a35r3 | auto | 64/64 | 110.8 | 55679 | scans 329280, consol=64, dropped=540 |

W = find_steps + scan_steps + mutops + suppressions (prereg metric).

## Early readings (NOT verdicts — battery still running)
1. **The anomaly replicates on fresh fixtures.** Auto is 2.8x W-costlier than
   trained on the benign cell and 2.62x on the adversarial cell. The direction
   (deliberate-trained cheaper than autopilot) appears on the NEW generator too.
2. **The benign-small regime also flips against autopilot.** Prereg guessed auto
   might be cheaper on benign cells; smoke says otherwise. Auto's every-10-ep
   full-tier scans (16 age + 16 pass + slow scans) cost ~19 scan steps/ep
   regardless of content; trained spends ~10 find steps/ep and 0 scans.
3. **Mechanism visible already.** On the adversarial cell, auto's gap driver is
   scan_steps=329280 of W=510430 total (~65%): per-episode age scans
   (64x4608=294912) plus periodic full passes. Trained's gap-avoidance comes
   from suppressing 540 adversarial observations instead of installing and
   later repairing them (add=64, kill=0 for trained; auto dropped=540 of its
   own observations).
4. **Substrate confound to decompose in final analysis.** Wall ratio (12.1x on
   adversarial cell) >> W ratio (2.62x). Auto's psm substrate does multiple
   byte-accessor field reads/writes per counted step (age/ver/unv/ctx/prom
   bookkeeping); the kb arms do ~2 accessor calls per find step. Final report
   will separate algorithmic gap (W) from per-step accessor overhead (wall/W).
5. **Untrained deliberation damage replicates.** Naive: 177 collateral
   true-kills on cap128a35r3 (prior: 28 on old fixtures — same phenomenon,
   different generator), 752 kills total, 16 spurious entries left in store.
   WS1-B assumption note: untrained deliberation is NOT a safe default; the
   training is load-bearing.

## Next
- Full 162-run battery (`run_all.sh`, background, ~minutes).
- Rerun byte-identity check via manifest sha256; in-driver digest gates already
  green on smoke cells.
- Analyzer: per-cell ratios, accuracy gates, scan/churn attribution, conditions
  map, wall-vs-W decomposition.
