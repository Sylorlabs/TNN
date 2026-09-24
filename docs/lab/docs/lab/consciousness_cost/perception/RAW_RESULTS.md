# PERCEPTION THREE-ARM COST MEASUREMENT — raw results

Prereg: `docs/lab/consciousness_cost/preregs/PERCEPTION_PREREG.md`
(frozen 2026-09-24T05:52:53Z, before the F3 build and before any three-arm run).
Parent law: `tnn-lab/senses/conscious-perception/preregs/FAIR_FIGHT.md`.

## Run provenance

| item | value |
|---|---|
| F1 binary | `tnn-lab/senses/rebuild/a_raw/sense` (frozen, pre-existing) |
| F1 SHA-256 | `68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1` |
| F2 binary | `tnn-lab/senses/conscious-perception/forks/deliberative/f2_bin` (rebuilt from `f2.zag` this session, pinned toolchain) |
| F2 SHA-256 | `a4ad7c49333e04dfdad17b0827a0063f8b1a5b3f1da0107b49f39e8572931444` |
| F3 binary | `docs/lab/consciousness_cost/perception/f3/f3_bin` (built from `f3.zag` this session, pinned toolchain) |
| F3 SHA-256 | `05e5cb791e4db008d95ab9a2908269bc722514f0e194a53be2c4ec94784b554f` |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` |
| Decision battery | 14 frozen fixtures `senses/conscious-perception/fixtures/test/`, 3 reruns/(arm,fixture) = 126 episodes, run 2026-09-24 ~06:15–06:25 UTC |
| Speed legs | 370 primary fixtures `senses/rebuild/harness/fixtures/*/primary/` (F1: 370, F2/F3: 280 — see router note), run 2026-09-24 ~06:30–06:50 UTC |
| Fixture SHAs | re-verified against `fixtures/MANIFEST.sha256`: 42/42 OK |
| Byte-identical reruns | 42/42 decision rows (3 reruns each); speed legs: 37/37 rechecked (every 10th) |
| Contract errors | 0 (all rows validate: approach tag, task, vocab, conf 0..1000, ops ≥ 0, resense/rs_kind rules) |
| Harness | `run_three_arm.py`, `run_speed.py`, `aggregate.py` (this dir) |
| Run artifacts | `runs/main/` (ledger.jsonl, rows.jsonl, RUNLOG.md, per-episode .verdict/.ledger), `runs/speed/` (speed_rows.jsonl, per-episode .verdict/.ledger) |

## Load-bearing determination: is the F2 fork REAL or a stub?

**REAL.** Verified from `forks/deliberative/f2.zag` source (994 lines) and
observed behavior:

- Pass 1 = bit-exact F1 port (`f1.zag`), with the sampling policy and loss
  bounds declared in the ledger (P1_PLAN) before sampling.
- Interrupt-only background scan (`bg_scan`) per task — cannot install.
- Six trigger types (`f2_trigger`): TR_UNCERTAIN (conf<250), TR_COVERAGE
  (stake-HIGH at acq 0), TR_GOAL (motion untracked), TR_DIVERSITY
  (colorconst), TR_BG (background interrupt), TR_NONE.
- Per-task selector priority lists (`f2_choose`), hint-driven reordering,
  used-selector bitmask (same-evidence reruns structurally impossible),
  every acquisition's evidence bytes SHA-256-hashed into the ledger.
- Hard budget: MAX_ACQ=6 + op-count deadline + verification depth ≤ 2.
- Majority adjudication (newest-wins ties), provisional-flagged fallback,
  install-time verification with fresh evidence on high-stake installs.

Observed: F2 resensed on 13/14 decision fixtures (26/28 speed fixtures with
router support), recovered all 6 catch opportunities, and its ledger shows
TRIGGER → P2_ACQ → INSTALL phase chains with per-acquisition evidence SHAs.
The selftest's 0-catch/0-resense "deliberative"
(`evidence/fairfight_runs/selftest/`, mean ops ratio 1.0) was an intentionally
disguised-autopilot binary built to prove the harness fires KB-D1 — it is not
this mechanism. **Score F2 as trained-policy, not as stub.**

## Decision battery — per-fixture (3-rerun means; wall = mean of 3)

| arm | fixture | leg | judgment | conf | truth | ok | ops | F1_ops | wall_ms | rs | rss_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | om_p1.pcm | omission | SAME | 285 | HIGHER | ✗ | 5583041 | 5583041 | 1830 | 0 | 16332 |
| F1 | om_p2.pcm | omission | SAME | 285 | LOWER | ✗ | 5583041 | 5583041 | 2223 | 0 | 16332 |
| F1 | om_p3.pcm | omission | SAME | 285 | SAME | ✓ | 5583041 | 5583041 | 3010 | 0 | 16332 |
| F1 | om_p4.pcm | omission | HIGHER | 951 | HIGHER | ✓ | 5583041 | 5583041 | 2465 | 0 | 16332 |
| F1 | om_t1.pcm | omission | PURE | 272 | BRIGHT | ✗ | 2824296 | 2824296 | 1307 | 0 | 16332 |
| F1 | om_t2.pcm | omission | BRIGHT | 491 | BRIGHT | ✓ | 2824296 | 2824296 | 2245 | 0 | 16332 |
| F1 | ib_m1.vid | inattentional | E | 500 | W | ✗ | 28674 | 28674 | 209 | 0 | 16332 |
| F1 | ib_m2.vid | inattentional | W | 789 | W | ✓ | 28674 | 28674 | 384 | 0 | 16332 |
| F1 | am_p1.pcm | ambiguity | HIGHER | 19 | HIGHER | ✓ | 5583041 | 5583041 | 3439 | 0 | 16332 |
| F1 | am_c1.img | ambiguity | DIFFERENT | 16 | DIFFERENT | ✓ | 4097 | 4097 | 403 | 0 | 16332 |
| F1 | il_c1.img | illusion | DIFFERENT | 90 | SAME_SURFACE | ✗ | 4097 | 4097 | 500 | 0 | 16332 |
| F1 | il_c2.img | illusion | SAME_SURFACE | 555 | DIFFERENT | ✗ | 4097 | 4097 | 440 | 0 | 16332 |
| F1 | rt_p1.pcm | redteam | SAME | 2 | HIGHER | ✗ | 5583041 | 5583041 | 4498 | 0 | 16332 |
| F1 | rt_c1.img | redteam | SAME | 16 | DIFFERENT | ✗ | 4097 | 4097 | 308 | 0 | 16332 |
| F2 | om_p1.pcm | omission | HIGHER | 1000 | HIGHER | ✓ | 8188 | 5583041 | 80 | 1 | 16332 |
| F2 | om_p2.pcm | omission | LOWER | 1000 | LOWER | ✓ | 8188 | 5583041 | 77 | 1 | 16332 |
| F2 | om_p3.pcm | omission | SAME | 886 | SAME | ✓ | 10236 | 5583041 | 88 | 1 | 16332 |
| F2 | om_p4.pcm | omission | HIGHER | 1000 | HIGHER | ✓ | 10236 | 5583041 | 149 | 1 | 16332 |
| F2 | om_t1.pcm | omission | BRIGHT | 1000 | BRIGHT | ✓ | 8956 | 2824296 | 57 | 1 | 16332 |
| F2 | om_t2.pcm | omission | BRIGHT | 1000 | BRIGHT | ✓ | 4861 | 2824296 | 100 | 0 | 16332 |
| F2 | ib_m1.vid | inattentional | W | 1000 | W | ✓ | 43008 | 28674 | 338 | 1 | 16332 |
| F2 | ib_m2.vid | inattentional | W | 1000 | W | ✓ | 67584 | 28674 | 422 | 1 | 16332 |
| F2 | am_p1.pcm | ambiguity | HIGHER | 22 | HIGHER | ✓ | 20476 | 5583041 | 88 | 1 | 16332 |
| F2 | am_c1.img | ambiguity | DIFFERENT | 25 | DIFFERENT | ✓ | 19456 | 4097 | 42 | 1 | 16332 |
| F2 | il_c1.img | illusion | SAME_SURFACE | 1000 | SAME_SURFACE | ✓ | 16384 | 4097 | 50 | 1 | 16332 |
| F2 | il_c2.img | illusion | DIFFERENT | 1000 | DIFFERENT | ✓ | 16384 | 4097 | 20 | 1 | 16332 |
| F2 | rt_p1.pcm | redteam | SAME | 886 | HIGHER | ✗ | 20476 | 5583041 | 92 | 1 | 16332 |
| F2 | rt_c1.img | redteam | SAME | 300 | DIFFERENT | ✗ | 19456 | 4097 | 41 | 1 | 16332 |
| F3 | om_p1.pcm | omission | HIGHER | 1000 | HIGHER | ✓ | 10236 | 5583041 | 63 | 1 | 16332 |
| F3 | om_p2.pcm | omission | LOWER | 1000 | LOWER | ✓ | 10236 | 5583041 | 72 | 1 | 16332 |
| F3 | om_p3.pcm | omission | SAME | 1000 | SAME | ✓ | 10236 | 5583041 | 52 | 1 | 16332 |
| F3 | om_p4.pcm | omission | HIGHER | 1000 | HIGHER | ✓ | 10236 | 5583041 | 127 | 1 | 16332 |
| F3 | om_t1.pcm | omission | BRIGHT | 1000 | BRIGHT | ✓ | 17147 | 2824296 | 13 | 1 | 16332 |
| F3 | om_t2.pcm | omission | BRIGHT | 1000 | BRIGHT | ✓ | 4861 | 2824296 | 17 | 0 | 16332 |
| F3 | ib_m1.vid | inattentional | W | 1000 | W | ✓ | 67584 | 28674 | 290 | 1 | 16332 |
| F3 | ib_m2.vid | inattentional | W | 1000 | W | ✓ | 67584 | 28674 | 339 | 1 | 16332 |
| F3 | am_p1.pcm | ambiguity | HIGHER | 22 | HIGHER | ✓ | 10236 | 5583041 | 80 | 1 | 16332 |
| F3 | am_c1.img | ambiguity | DIFFERENT | 25 | DIFFERENT | ✓ | 13312 | 4097 | 34 | 1 | 16332 |
| F3 | il_c1.img | illusion | SAME_SURFACE | 1000 | SAME_SURFACE | ✓ | 24576 | 4097 | 130 | 1 | 16332 |
| F3 | il_c2.img | illusion | SAME_SURFACE | 875 | DIFFERENT | ✗ | 24576 | 4097 | 53 | 1 | 16332 |
| F3 | rt_p1.pcm | redteam | SAME | 90 | HIGHER | ✗ | 10236 | 5583041 | 26 | 1 | 16332 |
| F3 | rt_c1.img | redteam | SAME | 25 | DIFFERENT | ✗ | 13312 | 4097 | 72 | 1 | 16332 |

rss_kb = peak RSS of the fork process (os.wait4 rusage), mean of 3 runs.
Measured 16332 KB on all 42 decision rows; independent probe shows ±several-MB
run-to-run variance on identical invocations (11–17 MB range) — see §Memory.
No arm-distinguishable difference.

## Decision battery — per arm × fixture class

| arm | class | acc | n | mean wall ms | mean ops | resense % |
|---|---|---|---|---|---|---|
| F1 | omission | 50.0% (3/6) | 6 | 2073.5 | 4663459 | 0.0 |
| F1 | inattentional | 50.0% (1/2) | 2 | 357.2 | 28674 | 0.0 |
| F1 | ambiguity | 100.0% (2/2) | 2 | 1627.8 | 2793569 | 0.0 |
| F1 | illusion | 0.0% (0/2) | 2 | 409.2 | 4097 | 0.0 |
| F1 | redteam | 0.0% (0/2) | 2 | 2137.8 | 2793569 | 0.0 |
| F1 | ALL | 42.9% (6/14) | 14 | 1536.1 | 2801469 | 0.0 |
| F2 | omission | 100.0% (6/6) | 6 | 108.0 | 8444 | 83.3 |
| F2 | inattentional | 100.0% (2/2) | 2 | 291.7 | 55296 | 100.0 |
| F2 | ambiguity | 100.0% (2/2) | 2 | 86.9 | 19966 | 100.0 |
| F2 | illusion | 100.0% (2/2) | 2 | 37.6 | 16384 | 100.0 |
| F2 | redteam | 0.0% (0/2) | 2 | 55.8 | 19966 | 100.0 |
| F2 | ALL | 85.7% (12/14) | 14 | 113.7 | 19563 | 92.9 |
| F3 | omission | 100.0% (6/6) | 6 | 49.7 | 10492 | 83.3 |
| F3 | inattentional | 100.0% (2/2) | 2 | 315.5 | 67584 | 100.0 |
| F3 | ambiguity | 100.0% (2/2) | 2 | 51.1 | 11774 | 100.0 |
| F3 | illusion | 50.0% (1/2) | 2 | 90.1 | 24576 | 100.0 |
| F3 | redteam | 0.0% (0/2) | 2 | 58.3 | 11774 | 100.0 |
| F3 | ALL | 78.6% (11/14) | 14 | 94.9 | 21026 | 92.9 |

## Catches, false-install deltas, kill bars

- F2 catches (correct ∧ F1 wrong, 12 scored): **6/6** —
  om_p1, om_p2, om_t1, ib_m1, il_c1, il_c2 (all 6 frozen opportunities).
- F3 catches: **5/6** — om_p1, om_p2, om_t1, ib_m1, il_c1 (missed il_c2).
- False-install delta (deliberative wrong ∧ F1 right): F2 = 0, F3 = 0.
- KB-D1 (zero catches → kill): F2 alive (6), F3 alive (5).
- KB-D2 (mean ops ratio > 2.0 AND catches < 3 → kill): F2 alive (1.385, 6
  catches), F3 alive (1.665, 5 catches).
- KB-D3 (redteam: ops ratio > 10 or wall ratio > 10 → kill): F2 alive
  (max ops ratio 4.749 on rt_c1, max wall ratio 0.132), F3 alive
  (3.249, 0.235).

**Cost-ratio interpretation warning (load-bearing):** the ops ratios vs F1
are dominated by a first-pass pipeline difference, not by deliberation. F1's
audio pipeline is integer-DFT-based (~5.6M/2.8M ops/episode); F2/F3's pass-1
is zero-crossing-based (~4k ops). The honest marginal cost of deliberation is
`ops_total / p1ops` (from each deliberative verdict):

| fixture | F2 marginal | F3 marginal |
|---|---|---|
| om_p1, om_p2 | 2.00× | 2.50× |
| om_p3, om_p4 | 2.50× (incl. verify round) | 2.50× |
| om_t1 | 2.19× | 4.19× |
| om_t2 | 1.19× (no resense) | 1.19× (no resense) |
| ib_m1 | 5.25× | 8.25× |
| ib_m2 | 8.25× | 8.25× |
| am_p1 | 5.00× | 2.50× |
| am_c1 | 2.38× | 1.62× |
| il_c1, il_c2 | 2.00× | 3.00× |
| rt_p1 | 5.00× | 2.50× |
| rt_c1 | 2.38× | 1.62× |

Deliberation costs 1.2–8.3× its own first pass. The trained policy is cheaper
than the naive policy on 8/14 fixtures, equal on 4 (om_p3/om_p4/ib_m2/om_t2),
more expensive on 2 (am_c1: 2.38× vs 1.62×; rt_c1: 2.38× vs 1.62× — the
trained policy keeps acquiring on the redteam images while the naive policy
stops after its fixed 2).

## Speed legs (S1–S4 analogues) — per arm × task

F1 ran all 370 primaries; F2/F3 ran 280 (shapetrans excluded — the F2 router
has no shapetrans path; pitch/timbre primaries are 16 kHz/14080/12800-sample
and the router only accepts 44.1 kHz 16384/8192-sample — both documented
mechanism limitations, recorded as N/A, not failures).

| arm | task | n | acc | eps/sec | wall p50 (s) | wall p95 (s) | ops med | ops min | ops max | rs% | bi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | colordisc | 60 | 48.3% | 2.698 | 0.385 | 0.740 | 8193 | 8193 | 8193 | 0.0 | 6/6 |
| F1 | colorconst | 40 | 87.5% | 2.887 | 0.343 | 0.728 | 8193 | 8193 | 8193 | 0.0 | 4/4 |
| F1 | shapetrans | 90 | 100.0% | 2.856 | 0.385 | 0.657 | 27651 | 27651 | 27651 | 0.0 | 9/9 |
| F1 | pitchdisc | 60 | 83.3% | 0.329 | 3.166 | 4.246 | 4521065 | 4521065 | 4521065 | 0.0 | 6/6 |
| F1 | timbredisc | 60 | 75.0% | 0.492 | 2.104 | 2.962 | 2293308 | 2293308 | 2293308 | 0.0 | 6/6 |
| F1 | motiondir | 60 | 41.7% | 2.299 | 0.463 | 0.759 | 28674 | 28674 | 28674 | 0.0 | 6/6 |
| F2 | colordisc | 60 | 50.0% | 17.155 | 0.056 | 0.120 | 18432 | 18432 | 28672 | 11.7 | 6/6 |
| F2 | colorconst | 40 | 50.0% | 13.633 | 0.064 | 0.162 | 32768 | 32768 | 32768 | 100.0 | 4/4 |
| F2 | motiondir | 60 | 50.0% | 3.826 | 0.268 | 0.484 | 67584 | 43008 | 67584 | 100.0 | 6/6 |
| F2 | pitchdisc | 60 | — | 20.395 | 0.049 | 0.105 | N/A | N/A | N/A | 0.0 | 6/6 |
| F2 | timbredisc | 60 | — | 15.484 | 0.053 | 0.153 | N/A | N/A | N/A | 0.0 | 6/6 |
| F3 | colordisc | 60 | 50.0% | 11.887 | 0.079 | 0.176 | 26624 | 18432 | 26624 | 68.3 | 6/6 |
| F3 | colorconst | 40 | 55.0% | 10.910 | 0.083 | 0.205 | 49152 | 49152 | 49152 | 100.0 | 4/4 |
| F3 | motiondir | 60 | 46.7% | 3.133 | 0.333 | 0.530 | 67584 | 67584 | 67584 | 100.0 | 6/6 |
| F3 | pitchdisc | 60 | — | 24.759 | 0.030 | 0.096 | N/A | N/A | N/A | 0.0 | 6/6 |
| F3 | timbredisc | 60 | — | 16.743 | 0.052 | 0.143 | N/A | N/A | N/A | 0.0 | 6/6 |

bi = byte-identity rechecks passed (every 10th fixture re-run; stdout/verdict
SHA256-identical).

### S1–S4 verification (F1 vs frozen)

| task | n | acc (frozen) | eps/s (frozen) | ops med (frozen) |
|---|---|---|---|---|
| shapetrans | 90 | 100.0% (100.0%) | 2.856 (3.666) | 27651 (27651) ✓ |
| motiondir | 60 | 41.7% (41.7%) | 2.299 (2.453) | 28674 (28674) ✓ |
| colorconst | 40 | 87.5% (87.5%) | 2.887 (1.266) | 8193 (8193) ✓ |
| colordisc | 60 | 48.3% (48.3%) | 2.698 (1.268) | 8193 (8193) ✓ |
| timbredisc | 60 | 75.0% (75.0%) | 0.492 (0.384) | 2293308 (2293308) ✓ |
| pitchdisc | 60 | 83.3% (83.3%) | 0.329 (0.355) | 4521065 (4521065) ✓ |

Accuracy and instrumented ops reproduce the frozen numbers EXACTLY (all six
tasks). Wall-clock eps/sec differs (environment-dependent VM timing; the
deterministic quantities are byte-exact). S3 no-uncertainty: conf ≥ 950 AND
correct = 0.0% on all six tasks over the 370 primaries (frozen: 0.0%; the
frozen 1.5% pitchdisc figure came from including the 14 new fixtures —
om_p4's conf 951).

### First-pass decoder analysis (speed legs — disentangles pipeline from deliberation)

F2/F3's pass-1 (the fair-fight F1 fork) vs F1 (a_raw) judgment agreement:

| task | p1 == F1 judgment | F2 flips (final≠p1) | F3 flips | p1 acc → F2 final | p1 acc → F3 final | F1 acc |
|---|---|---|---|---|---|---|
| colordisc | 98.3% (59/60) | 0 | 0 | 50.0% → 50.0% | 50.0% → 50.0% | 48.3% |
| colorconst | 57.5% (23/40) | 2 | 0 | 55.0% → 50.0% | 55.0% → 55.0% | 87.5% |
| motiondir | 43.3% (26/60) | 29 | 27 | 23.3% → 50.0% | 23.3% → 46.7% | 41.7% |

Mechanism reasons for the first-pass divergence (verified in source):
- **colorconst:** a_raw = von Kries discount (mean×1000/max), EUCLIDEAN
  distance of discounted means, threshold 150 per-mille. Fair-fight f1 =
  discounted channel mean×255/max, MAX channel absolute difference,
  threshold 8. Different decision rules: they agree on the illusion fixtures
  but diverge on textured primaries (F1 87.5% vs p1 55%).
- **motiondir:** a_raw = frame-differencing centroid displacement
  (|disp|<3px → STILL). Fair-fight f1 = brightness-weighted global centroid
  (bv>16) on frames 0 and nf−1, STILL if max<128 Q6 subpixels. Different
  decoders: 43% agreement; deliberation's bright-tracker then repairs
  23.3% → 50.0% (F2) / 46.7% (F3).
- **colordisc:** same rule both sides (98% agreement); deliberation flips
  nothing on primaries.

## Memory footprint

- Peak RSS of the fork process per episode (os.wait4 rusage): 11–17 MB
  across all runs with several-MB run-to-run variance on IDENTICAL
  invocations (environmental noise on this shared VM) — no
  arm-distinguishable difference. Reported as measured; not a basis for
  arm comparison.
- Fixed arena sizes from source (the reliable numbers): F2/F3 — 64 KiB
  hash-chained ledger buffer, fixture buffer = fixture byte size (largest:
  motiondir primaries, ≤ ~1.2 MB), small scratch (bg scan, vote arrays);
  F1 — per-task buffers in `sense.zag` (DFT twiddle/scratch for audio).
  All arms' working sets are fixture-sized; no arm has an asymptotic
  memory advantage.

## Where autopilot genuinely wins (same verdict, lower cost)

1. **Ambiguity class (am_p1, am_c1): all three arms correct.**
   F1: 5,583,041 / 4,097 ops, 0 resenses. F2: 5.00×/2.38× marginal
   (20,476 / 19,456 ops), 4 and 3 acquisitions. F3: 2.50×/1.62× marginal.
   Same verdicts, strictly more compute — the uncertainty triggers fire on
   low-confidence-but-correct judgments and the fresh evidence agrees, so
   every resense was pure overhead. Mechanism: triggers key on confidence,
   not on correctness; nothing distinguishes "uncertain and right" from
   "uncertain and wrong" before resensing.
2. **Controls om_p3 (SAME✓) and om_t2 (BRIGHT✓): F1 correct at base cost.**
   F2 resenses om_p3 anyway (TR_COVERAGE fires on stake-HIGH at acq=0 even
   at conf 1000 → 2.50× marginal, verified install). Same verdict, higher
   cost. om_t2 is the honest exception: no trigger fires, 1.19× — the
   no-uncertainty path stays cheap.
3. **Redteam (rt_p1, rt_c1): cost-only leg.** F1's cost is a pure function of
   fixture size — no input can make it burn more (DoS-immune, KB-A2). F2/F3
   burn their full acquisition pattern on maximally ambiguous inputs
   (F2: 5.00×/2.38× marginal; F3: 2.50×/1.62×). Absolute cost still favors
   F2/F3 on audio (cheap first pass), but the STRUCTURAL gap is real:
   deliberative cost is adversary-drivable, autopilot cost is not.
4. **Speed legs, colordisc primaries:** F1 48.3% at 8,193 ops, 0 resenses;
   F2 50.0% at 18,432 median ops (2.25×) with 11.7% resense; F3 50.0% at
   26,624 (3.25×) with 68.3% resense. No accuracy gain for 2–3× the ops.
   Mechanism: on the bulk distribution most episodes are unambiguous, so
   the trained policy's triggers mostly stay quiet (11.7%) while the naive
   policy's conf<900 threshold fires on 68.3% — pure overhead both ways.
5. **KB-A3 no-op boundary:** on the provable-no-gain fraction (= per-task
   accuracy: 100/87.5/83.3/75/48.3/41.7%), same-decoder re-sensing cannot
   flip a correct judgment (deterministic no-op); every deliberative op
   spent there is overhead by construction.

## Where deliberation wins (for the bill's other side)

- Omission: F2/F3 6/6 vs F1 3/6 (late-onset events beyond the 2048-sample
  first-pass window; new-window selectors recover them).
- Inattentional: F2/F3 2/2 vs F1 1/2 (bright-tracker defeats the
  distractor-dominated centroid).
- Illusion: F2 2/2 vs F1 0/2 (absolute/robust decoders defeat the
  spike-corrupted illuminant and discount collision); F3 1/2 — the naive
  fixed order [ROBUST, ABSOLUTE] lets the spike-immune-but-still-discounted
  ROBUST vote agree with the wrong pass-1, outvoting ABSOLUTE 2–1.
- Motiondir primaries: deliberation repairs a weak first pass
  (23.3% → 50.0%).

## Trained (F2) vs naive (F3) policy — the load-bearing contrast

Same machinery, different policy. F2: 12/12 scored, 6/6 catches, mean
marginal cost lower on 8/14 fixtures. F3: 11/12, 5/6 catches. The il_c2
divergence is the clean mechanism story: F2's diversity trigger +
hint-aware selection picks the ABSOLUTE (no-discount) decoder first →
DIFFERENT ✓ (1 round, 2.00×); F3's fixed order tries ROBUST first, which
agrees with the wrong pass-1 → majority SAME_SURFACE ✗ (2 rounds, 3.00×).
Trained attention selection beats fixed-order selection exactly where the
evidence sources disagree.

## Open / caveats

- F2's "trained" status: parameters (CONF_BAR=250, trigger structure,
  selector orders) were set by the F2 builder crew against the train pool;
  whether the full FAIR_FIGHT §6 protocol (3 zero-improvement search
  rounds, held-out check, anti-shopping) was satisfied was NOT verified
  here. F2 is "trained" relative to F3's deliberately naive policy.
- F2/F3 router limitations (documented, not run failures): no shapetrans
  path; audio only at 44.1 kHz 16384/8192-sample (fair-fight format), so no
  F2/F3 pitch/timbre speed-leg data on the 16 kHz primaries.
- Wall-clock is environment-dependent (this VM); the deterministic
  quantities (judgments, confidences, ops, byte-identity) are exact.
- The F2 builder's RUNLOG reports 3.26× overall vs ITS OWN fair-fight F1
  fork; vs a_raw/sense the ratio is dominated by the first-pass pipeline
  difference (report both, never mix).
