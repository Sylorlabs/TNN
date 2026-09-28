# D1 BATTERY VERDICT — build crew B-D1 (2026-09-24)

Battery: `d1battery.zag` (pure Zag, zero RNG). 3× byte-identical runs,
stdout SHA `0ed3de64a4a1e3fab8e0228d4397682d5aff59d5bd3e6994ab5086e890f4f920`
(run1.out = run2.out = run3.out, byte-identical).
Fixtures: 360 honest (committed F5 `fixtures_ledger.txt`,
SHA-256 `0c5e2c0d…3a0` VERIFIED) + 300 adversarial
(`d1_adv_fixtures.txt`, SHA-256 `a18f807b…`, generator `gen_d1_adv.py`,
deterministic parameter sweeps, zero RNG).
Design frozen before code: `D1B_DESIGN.md`. Specs extracted BY SCRIPT from
frozen commit `bfab522a` (see `frozen/`).

## Per-class numbers (hybrid D1: P7 + P10-specialist + independence audit)

| class | n | P7 install | hybrid committed | hybrid provisional | hybrid withhold |
|---|---|---|---|---|---|
| Honest | 360 | 252 (70%) | 252 (70%) | 108 (30%) | 0 (0%) |
| A static injection | 120 | 0 (0%) | 0 (0%) | 24 (20%) | 96 (80%) |
| B driver-level | 120 | 120 (100%) | 81 (68%) | 39 (32%) | 0 |
| C fusion-layer | 60 | 60 (100%) | 40 (67%) | 20 (33%) | 0 |

In-repertoire (TMB-5, P10-covered) committed false installs:
A 0/40, B 1/40 (single 5-bit slip), C 0/20 → **1/100 = 1%**.
Out-of-repertoire (COL-4/PTC-4, named blind spots): B 80/80, C 40/40
committed (UNCOVERED flag) — the R1 residual, all of it.

P10 specialist (measured, not modeled): 310 invocations; Class B 39/40 caught
(measured 4 bits; slip 1/40 = 2.5% ≈ predicted 1/32); Class C 20/20 caught;
honest 250/250 pass. The probe's "5 bits" MODEL is confirmed as a measurement.

Independence audit: 660/660 path agreement, premium_bp=0, effective-n=1.0,
verdict=SHARED_SOURCE; F8c 3/3 hidden common causes detected
(shared record, fusion-layer lie, shared perturbation faker) → the
independence CLAIM for this deployment is correctly killed (it was never
independent). P8w (measurement only): 0 installs on every class.

Delay: 310/660 = 47% delayed >50 cycles (all P10 invocations; P7-alone 0%).

## K1–K7 (D1 prereg bars, on prototypes)

- **K1 (P7)**: Class-B install 120/120 = 100% ≥ 50% → **FIRED**.
  P7 KILLED as a general mechanism (confirms the D-1 debate probe).
- **K2 (P8)**: premium_bp = 0 → ≤ 0 → **FIRED**. P8 warrant killed
  (re-confirms probe; warrant excluded from hybrid by design).
- **K3 (P8)**: P8w honest retention 0/360 = 0% < 90% → **FAILS**
  (constructional: paths are shared-source by design; warrant not in hybrid).
- **K4(a)**: hybrid Class-C committed 40/60 = 67%. Strict-0 → **FAILS overall**;
  in-repertoire 0/20 = 0% → **PASSES**. The failure is entirely R1 (coverage).
- **K4(b)**: F8c 3/3 detected → audit kills the independence claim correctly
  → **PASSES**.
- **K5**: 3× byte-identical, SHA `0ed3de64…` → **PASSES**.
- **K6**: P7 prototype agreement 252/360 = 70% < 90% → FAIL;
  P7 honest-loss 108/360 = 30% > 15% → FAIL (a withholding P7 fails K6,
  as the debate predicted). **Hybrid honest committed-loss 0/360 = 0% ≤ 15%
  → PASSES** — the abstention-to-provisional routing is load-bearing.
  Hybrid honest retention: 252 committed + 108 provisional = 360/360 (0% lost).
- **K7 (P7)**: P7-alone 0% delayed → **PASSES**. Hybrid 47% delayed is a
  reported cost of the P10 fallback (R4), not a P7 bar failure.

## Commit rule: HOLDS

The built hybrid exhibits the predicted complementary, non-overlapping
failures: P7 owns Class A (0/120, perfect) and honest-via-provisional;
P10 owns Class B/C in-repertoire (59/60 → provisional, 1 slip);
the audit owns C-detection (3/3, kills the independence claim).
The hybrid beats P7 alone on committed false installs (121 vs 180)
and on honest loss (0% vs 30%). **The D1 hybrid is JUSTIFIED as the
architecture.**

Blocking residual (R1, predicted before runs): the P10 repertoire covers
1/3 scene classes (TMB-5). The 120 out-of-repertoire B/C spoofs committed-install
(UNCOVERED flag). The hybrid is a **TMB-5-scene trust locus, not a general one**.
General deployment needs the repertoire expanded (F10b blind spots named:
COL-4, PTC-4) or a second specialist. K4(a) strict-0 and any "0 false installs"
claim are blocked on R1.

Secondary findings:
- Class A meas≥6000 (24/120) → PROVISIONAL (tier pollution, R3; not committed).
- P10 5-bit slip is real (1/40); K4(a) strict-0 in-repertoire held this run
  (0/20 C) but the slip predicts occasional breaches; 0 needs ≥8 bits/dual-check.
- K7 fires on hybrid cost (47% delayed); a sparser P10 invocation policy is
  future work (D4 K5 action-budget also implicated: 310 actions/660 percepts).

## Hypothesis backlog updates
- H-PAM-7 → TESTED-survived (narrowed): static-injection defense perfect
  (0/120); general claim killed by K1 (100% Class-B installs).
- H-PAM-8 → TESTED-survived (audit-only): warrant killed by K2 (premium 0);
  audit component detects 3/3 hidden common causes, correctly reports
  SHARED_SOURCE.
- H-PAM-10 → TESTED-survived (specialist): 4-bit measured discrimination on
  the driver-level class (only non-zero); general claim killed by coverage
  (1/3 < 50%).

## Artifacts (this commit)
- `d1battery.zag`, `R33_NATIVE_IO_V1.zag`, `gen_d1_adv.py`,
  `d1_adv_fixtures.txt`, `D1B_DESIGN.md`, `frozen/` (3 frozen docs, git-SHA
  verified), `extract_*.py`, `verify_fixtures.py`, `verify_battery.py`
  (independent Python reimplementation — output byte-identical to Zag on all
  8 lines), `run1.out`, `run2.out`, `run3.out`, `SHASUMS.txt`.
- NOT committed: `d1battery` binary, `.zagd`/`.zag-cache`.
