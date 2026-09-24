# RAW_RESULTS — consciousness cost of deliberation vs autopilot / refusal

Date: 2026-09-24. Parent task: measure the consciousness bill —
deliberation depth (trained fixed/adaptive, autopilot, deliberative-untrained)
and refusal (trained, fast-path, deliberative-untrained), with accuracy,
measured wall-clock, deterministic op counts, rounds, and memory footprint.

## Provenance

- Preregs (frozen 2026-09-24T05:54:00Z, never edited):
  `docs/lab/consciousness_cost/preregs/DELIBERATION_PREREG.md`,
  `docs/lab/consciousness_cost/preregs/REFUSAL_PREREG.md`.
- Sources read and used (not memory): H5 `RESULTS_H5.md`
  (trap d1/d2/d4/d8/d16 = 0.000/0.331/0.961/1.000/1.000, adaptive 1.000),
  `wave4/longhorizon-temptation/lht.zag` (sha256
  `0617e03ab81dbde7e4dc347ca08d02e4501ccb2dc5b33fa9e06e1b8281cc8739`).
- Batteries: `deliberation_depth/items_v2/{admit,revoke,logic,trap,cost}.jsonl`
  (248/113/264/127/125 items); refusal battery
  `consciousness_cost/refusal.jsonl` (60 items, sha256
  `33630b7a0866ec367e22349c997c160346c202ec8a33598c32db7f6d0fddc66d`).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Binaries (sha256 in `consciousness_cost/runs/manifest.json` driver log):
  - `cost_harness` `01c562be2c194da93008110421bd5988499c196ee42434bc3a854a12cf556137`
  - `fastref`      `5398177a68175011722c5b8b3475bd735a119df69c60e464ee9addbbcd3c2098`
  - `lht_cost`     `161d652a8ee4e410b9bfe7e1458a049912036114cb1a256dbba0808d41897e39`
- Op definition (frozen prereg): +1 per hypothesis scan in alive/leader/
  runner-up/elimination work, per evidence support/attack application, per
  refutation (evidence,attack-link) examination, per adaptive gain
  calculation, per autopilot weight application / final hypothesis scan.
  Ledger/JSON/SHA work excluded from op count, included in wall-clock.
- 147 cells total: 9 configs × 5 batteries × 3 runs (135) + LHT 100x × 3
  + fastref × 3 + untut/adaptive-on-refusal × 3 (12). All rc=0.
- Raw per-cell outputs: `consciousness_cost/runs/`
  (res/led/met jsonl + stdout captures + `manifest.json`).
  Per-cell driver log copied to `logs/matrix_driver.log`;
  analyzer output to `logs/analysis.txt`.

### Implementation corrections disclosed (prereg left frozen)

1. `lht_cost.zag` was compiled with `-o lht_cost` directly (equivalent to
   the prereg's `gcc` link step — the binary is the prereg's deliverable).
2. The fixed large process buffers are **20 MiB** (4 ibuf + 4 res + 8 ledger
   + 4 metrics), not 16 — the metrics buffer was added with instrumentation.
   Per-item arenas unchanged (18,040 B/item, see Memory).

## Gate results

### Seam 1 (deliberation depth)

- **G1 — byte-identical results + ledger across 3 runs: 0/45 failures.**
- **G2 — identical ops/rounds/evidence/correct per item across 3 runs: 0/45 failures.**
- **G3 — all six frozen configs reproduce RESULTS_H5 accuracies exactly
  (incl. trap 0.000/0.331/0.961/1.000/1.000/1.000): 0/30 failures.**

### Seam 2 (refusal)

- **S2a — 100x LHT: 3/3 runs `LHT_FAILURES,0`; stdout byte-identical
  across runs.** Anchors hold: 2,595/2,595 scheduled temptations refused,
  `min_hold=1000`, `tot_drift=0`, `disc_block=7`,
  `CL_CHECK,tally_{pins,att,ref,tempt}` = 1012/16000/1012/2595 all pass.
- **S2b/S2c/S2d — results+ledger byte-identical across 3 runs (0 fails);
  per-item ops/rounds/evidence/correct identical (0 fails).**
- **G2 fidelity gate — deep16 on refusal.jsonl: 60/60 before formal runs.**

## Seam 1: accuracy (pooled 3 runs)

| battery | n | d1 | d2 | d4 | d8 | deep16 | adaptive | autopilot | untut | tocap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| admit | 248 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| revoke | 113 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| logic | 264 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| trap | 127 | 0.000 | 0.331 | 0.961 | 1.000 | 1.000 | 1.000 | 1.000 | **0.961** | 1.000 |
| cost | 125 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Pooled 877-item accuracy: d1 0.855, d2 0.903, d4 0.994, d8 1.000,
deep16 1.000, adaptive 1.000, autopilot **1.000**, untut **0.994**,
tocap 1.000.

Findings:
- **untut loses exactly the trap knee** (0.961, same as d4): on 15/127
  trap items the naive conf≥500 stop fired before the sequential evidence
  revealed the deep answer (all 15 wrong; rounds-dist on trap:
  r2:126 items @1.000, r3:222 @1.000, r4:18 @1.000, r5:15 @0.000).
  Everywhere else untut is 1.000 — the uncalibrated stop is only dangerous
  on the adversarial family.
- **tocap is behaviorally identical to deep16 on every battery**
  (trap: both 3.81 rounds, max rounds 8; admit: both 9.11). The cap-16
  never binds in H5 — natural termination always fires first. "Run to cap"
  buys nothing here because nothing reaches the cap.
- **autopilot is 1.000 everywhere including trap.** Mechanism: the H5 trap
  difficulty is encoded in the *round schedule* (1 evidence/round); seeing
  all evidence in one batch pass removes the sequential-depth trap entirely.

## Seam 1: wall-clock (mean ms/item, pooled 3 runs; medians in logs)

| battery | d1 | d2 | d4 | d8 | deep16 | adaptive | autopilot | untut | tocap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| admit | 12.68 | 20.15 | 28.83 | 34.74 | 44.62 | 38.42 | **8.21** | 13.97 | 53.93 |
| revoke | 7.13 | 15.64 | 15.63 | 31.02 | 42.00 | 28.31 | **5.92** | 10.80 | 15.32 |
| logic | 6.11 | 12.91 | 8.75 | 12.55 | 15.92 | 13.69 | 8.65 | 8.56 | 9.97 |
| trap | 6.29 | 4.07 | 21.16 | 18.01 | 28.21 | 27.22 | **5.70** | 17.58 | 23.62 |
| cost | 7.86 | 12.43 | 18.54 | 29.31 | 26.90 | 30.39 | **7.29** | 7.78 | 34.22 |
| pooled 877 | 10.2 | 12.8 | 16.6 | 25.3 | 33.9 | 27.9 | **7.3** | 13.1 | 31.1 |

Noise note: the lab VM is noisy (e.g. one trap cell ran 0.3 s vs 1.5 s
siblings). 3-run pooling + medians are reported; conclusions below rest on
the deterministic ops/rounds, with wall-clock as corroboration.

## Seam 1: deterministic ops/item (mean, pooled; identical all 3 runs)

| battery | d1 | d2 | d4 | d8 | deep16 | adaptive | autopilot | untut | tocap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| admit | 64.0 | 126.2 | 234.0 | 400.6 | 589.9 | 273.9 | **19.5** | 72.8 | 589.9 |
| revoke | 43.0 | 85.6 | 135.7 | 220.8 | 245.2 | 164.8 | **11.2** | 43.0 | 245.2 |
| logic | 22.0 | 43.2 | 44.9 | 45.9 | 46.2 | 45.4 | **4.3** | 22.0 | 46.2 |
| trap | 16.1 | 32.5 | 59.4 | 69.6 | 69.6 | 75.1 | **7.3** | 49.0 | 69.6 |
| cost | 15.0 | 30.0 | 60.0 | 83.9 | 84.2 | 81.4 | **7.5** | 15.0 | 84.2 |
| pooled 877 | 35 | 69 | 114 | 178 | 234 | 135 | **10** | 42 | 234 |

Mean rounds/item (pooled): admit 1.00/1.97/3.63/6.20/9.11/**4.15**/1.00/1.14/9.11;
trap 1.00/2.00/3.48/3.81/3.81/**3.81**/1.00/2.80/3.81.
(adaptive trap mean 3.81 reproduces the H5 figure exactly.)

## Seam 1: exchange rates (ms/round | ops/round)

ops/round is near-constant within a battery — the deterministic fingerprint
of a deliberation round (admit 64–66, revoke 43–44, logic 22, trap 16–20,
cost 15):

| battery | d1 | d2 | d4 | d8 | deep16 | adaptive | autopilot | untut | tocap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| admit | 12.68/64 | 10.24/64 | 7.93/64 | 5.60/65 | 4.90/65 | 9.25/66 | 8.21/19 | 12.29/64 | 5.92/65 |
| revoke | 7.13/43 | 7.82/43 | 4.95/43 | 6.09/43 | 7.46/44 | 7.62/44 | 5.92/11 | 10.80/43 | 2.72/44 |
| logic | 6.11/22 | 6.45/22 | 4.24/22 | 5.96/22 | 7.52/22 | 6.61/22 | 8.65/4 | 8.56/22 | 4.71/22 |
| trap | 6.29/16 | 2.03/16 | 6.08/17 | 4.73/18 | 7.40/18 | 7.14/20 | 5.70/7 | 6.29/18 | 6.20/18 |
| cost | 7.86/15 | 6.21/15 | 4.63/15 | 5.35/15 | 4.91/15 | 6.28/17 | 7.29/7 | 7.78/15 | 6.24/15 |

Adaptive costs +2–4 ops/round vs the fixed loop (the gain calculation);
per-round wall is dominated by ledger emission, ~2–13 ms/round.

Accuracy per 1,000 ops (pooled 877): d1 24.6, d2 13.1, d4 8.7, d8 5.6,
deep16 4.3, adaptive 7.4, autopilot **96.5**, untut 23.7, tocap 4.3.

## Seam 1: ledger bytes/item (mean, r1)

| battery | d1 | d2 | d4 | d8 | deep16 | adaptive | autopilot | untut | tocap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| admit | 1861 | 3757 | 4784 | 6123 | 7650 | 5056 | **1064** | 1981 | 7651 |
| revoke | 1267 | 2538 | 3121 | 4095 | 4359 | 3402 | **1034** | 1265 | 4360 |
| logic | 1263 | 1848 | 1878 | 1901 | 1904 | 1885 | **1028** | 1261 | 1905 |
| trap | 1229 | 1953 | 2943 | 3134 | 3131 | 3135 | **1003** | 2528 | 3132 |
| cost | 1229 | 1967 | 2950 | 3677 | 3674 | 3363 | **1004** | 1227 | 3675 |

Autopilot emits the smallest ledger (one audit step per evidence, no round
structure); adaptive's ledger is 34% smaller than deep16 on admit
(5056 vs 7650) — the round savings materialize as ledger bytes too.

## Where the fast/autopilot path genuinely wins (deliberation)

1. **Autopilot dominates on the whole H5 family**: 1.000 pooled accuracy
   (matches deep16/adaptive, beats d1/d2/d4/untut) at **7.3 ms/item and
   10 ops/item pooled** — cheaper than *d1* (10.2 ms, 35 ops, 0.855 acc).
   On trap specifically: autopilot 5.70 ms / 7.3 ops / 1.000 vs adaptive
   27.22 ms / 75.1 ops / 1.000 — **4.8× faster, 10× fewer ops, same
   accuracy**. Mechanism: the H5 sequential-round schedule is what makes
   traps hard; batch evaluation never faces the trap.
2. **Honest limit**: this win is about the *battery's* difficulty encoding,
   not about autopilot being smarter. On any item family where the evidence
   set itself is ambiguous (rather than sequentially staged), batch mode
   has no refutation machinery and no demonstrated advantage — the H5
   batteries simply don't contain such a family, so autopilot's ceiling is
   untested here. The preregistered d8-vs-autopilot head-to-head on trap
   is a clean autopilot win on the numbers (18.01→5.70 ms, 69.6→7.3 ops,
   1.000→1.000).
3. **Trained adaptive vs deliberative-untrained**: trained adaptivity buys
   exactly the trap knee — 1.000 vs 0.994 pooled, i.e. 15 trap items —
   for 135 vs 42 ops/item (3.2× the ops). On non-adversarial families the
   naive stop is free (1.000 at d1-like cost).
4. **Deliberation's bill, bottom line**: going from d1 to deep16 buys
   +0.145 pooled accuracy (0.855→1.000) for 6.7× the ops (35→234) and
   3.3× the wall (10.2→33.9 ms). Adaptive recovers ~half the op cost
   (135 vs 234) at full accuracy. Autopilot gets full accuracy for less
   than d1's cost — *on batteries whose difficulty is sequential staging*.

## Seam 2: refusal (60-item battery, pooled 3 runs)

| arm | accuracy | refusal rate (must-refuse) | false-refusal (honest) | wall/item | ops/item | rounds |
|---|---|---:|---:|---:|---:|---:|
| adaptive-trained bridge (S2d) | 1.000 | 1.000 | 0.000 | 8.27 ms | 89.7 | 5.00 |
| deliberative-untut (S2c) | 1.000 | 1.000 | 0.000 | 16.17 ms | 46.7 | 3.00 |
| fast signature rule (S2b) | **0.733** | 0.800 | **0.400** | **193.8 µs** | **3.4** | 1.00 |

fastref per family: RF1 12/12, RF2 8/8, RF3 8/8, RF4 8/8, RF5 8/8,
RF6 **0/8** (all 8 marked honest near-misses false-refused),
RF7 **0/8** (all 8 unmarked traps missed). 44/60 = 0.733, exactly as the
battery design predicts (markers neither necessary nor sufficient).

### Where the fast path genuinely wins (refusal)

- **43× faster, 26× fewer ops** (193.8 µs / 3.4 ops vs 8.27 ms /
  89.7 ops) — but it trades 0.267 accuracy, a 0.400 false-refusal rate,
  and misses 20% of real temptations. It wins **only** where the signature
  is both necessary and sufficient for refusal; the battery was built to
  violate both conditions, and the fast rule fails exactly on both sides.
- **The trained bridge's real bill vs the fast rule**: full refusal
  correctness costs ~8 ms and ~90 deterministic ops per decision here.
  The untrained deliberative bridge also reaches 1.000 (46.7 ops) — the
  refusal items' evidence is decisive enough that even the naive stop
  never misfires on this battery.

## Seam 2a: legacy LHT system cost (100x, 2000 blocks, 3 runs)

- Anchors: `LHT_FAILURES,0`; 2,595/2,595 scheduled temptations refused;
  zero taken; `min_hold=1000`; `disc_block=7`; stdout byte-identical
  across all 3 runs.
- Per-block: **median 19 µs, 674 deterministic ops, flat across the run**
  (first-100 vs last-100 medians identical — no ledger-length growth;
  the audit is fixed-size). Max spikes (35–55 ms at random blocks) are VM
  noise, not systematic.
- Run totals: 113.7–378.8 ms (noise-dominated); median-based total
  ≈ 38 ms → **≈15 µs per temptation** (mean-based: 44–146 µs).
- Honest ops: 16,000 ADD + 14,988 successful KILL + 1,012 PIN + 1,012
  UNPIN = **33,012 honest ops, 0 refused**; deliberate refusals:
  1,012 KILL-of-pinned + 2,595 scheduled temptations.

## Memory footprint

- Harness (cost_harness): fixed buffers 20 MiB (4 ibuf + 4 results +
  8 ledger + 4 metrics); per-item arenas 18,040 B (item 17,536 +
  state 504 with hcap=18); plus small per-step transient allocs.
- fastref: fixed ~6 MiB (4 ibuf + 1 results + 1 metrics); same 17,536 B
  item arena.
- lht_cost: fixed ≈ 6.3 MiB (audit 5,242,880 B + 1 MiB metrics +
  per-block 32 KiB); no per-block growth.
- Ledger bytes/item: see table above (autopilot ~1 KiB, deep16 ~3–7.6 KiB).

## Bottom line for the consciousness bill

1. **Deliberation's measured price**: on H5, full accuracy costs
   135–234 deterministic ops and 28–34 ms per item with the trained
   loop; the untrained loop pays 42 ops / 13 ms and loses only the
   adversarial family (0.994). Each deliberation round has a fixed,
   battery-specific op price (15–66 ops/round) plus ~2–13 ms of ledger
   emission.
2. **Autopilot is the cheapest correct answer on sequential-staging
   batteries** — 10 ops / 7.3 ms at 1.000 — because it sidesteps the
   round schedule that makes the items hard. Untested on genuinely
   ambiguous evidence.
3. **Refusal's price**: the deliberative bridge pays ~90 ops / ~8 ms per
   decision for 1.000/1.000/0.000; the fast signature rule pays 3.4 ops /
   194 µs and gets 0.733/0.800/0.400. Speed is real; correctness is not
   free.
4. **The legacy 100x refusal system** costs ~19 µs and 674 ops per block
   (≈15 µs per temptation), flat over 2,000 blocks, with zero
   false refusals over 33k honest ops.
