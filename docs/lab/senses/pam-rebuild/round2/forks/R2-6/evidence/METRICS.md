# R2-6 completion-crew metrics (2026-09-23)

Frozen build run on the fixtures it can consume: 925 round-1 harness fixtures
(`senses/rebuild/harness/fixtures`): 370 primary + 370 noise + 185 adversarial.
The frozen R2A 10,000-trial suite is NOT consumable by this build
(see R2FX_INCOMPAT.txt) — every R2A-calibrated bar below is marked
**UNEVALUABLE (frozen)**; the numbers shown are harness-set analogs, not the
prereg's bars.

Bar (frozen) | Measured (harness 925) | Result
---|---|---
B1 primary accuracy ≥ 60% | 69.2% (256/370) | PASS (harness set)
B2 vs Approach A (reported) | R26 69.2% vs A 74.1% → Δ −4.9pp | reported
B3 efficiency (measured) | R26 p95 ops 1,112,292 vs A 4,521,065 (24.6%) | reported; bytes/percept unmeasured
B4 contract ablation (HARD KILL, frozen: ≥10% of R2A adv + fewer false installs) | 63/185 adv = 34.1% changed; false installs 60 → 37 | PASS as analog; frozen bar UNEVALUABLE
B5 false installs ≤ 3% (frozen: /10,000 R2A) | 37/925 = 4.0% (adv 6/185 = 3.2%, normal 31/740 = 4.2%); permanent-only: 0 | FAIL as analog; frozen bar UNEVALUABLE
B6 ≥3 runs byte-identical + ledger (HARD KILL) | 3 runs sha256 `af5dc8321851…` identical; ledger 925/925 verified | PASS
B7 beauty | no sensory artifacts produced | PENDING-MICAH
RK-1 ≤ 0.03 false installs/10,000 (frozen) | analog 4.0% > 3% | FAIL as analog; frozen bar UNEVALUABLE
RK-2 ≤ 1% wrong-high-conf installed | 5/9 = 55.6% | FAIL (structural: timbredisc RICH→BRIGHT systematic; judgment vocab has no RICH/PURE)
RK-3 ≥ 85% correct-high-conf PASS-and-install | 0/141 = 0% | FAIL (structural: single provisional/permanent slot per task; correct PASSes stuck in CONFLICT_WITHHELD after first wrong provisional)
RK-4 ≥ 100 installs in contract-less ablation | 309 | PASS (analog)
RK-5 ≥ 90% wrong-high-conf → FAIL/UNRESOLVED | 3/9 = 33.3% | FAIL (structural: same timbredisc systematic PASSes)
RK-6 ≤ 5% escalations AND p95 ops ≤ 40% of A | 0 escalations; p95 ops 24.6% of A | PASS (analog)
RK-7 byte-identical | 3 runs identical, ledger verified | PASS

## Per-task primary accuracy (R26 vs DESIGN_R26.md claim)

Task | Measured (n=370 primary) | DESIGN claim | Match?
---|---|---|---
colordisc | 47/60 = 78.3% | 100% | NO — refuted
colorconst | 36/40 = 90.0% | 86.7% | close
shapetrans | 36/90 = 40.0% | 45.0% | close
pitchdisc | 60/60 = 100% | 100% | yes
timbredisc | 30/60 = 50.0% | 50.0% | yes
motiondir | 47/60 = 78.3% | 85.0% | NO — refuted
overall | 256/370 = 69.2% | 77.8% (280/360) | NO — refuted

DESIGN's headline numbers do not reproduce on the only fixture set the frozen
build can run; colordisc's claimed 100% and motiondir's 85% are refuted
(13-trial and 4-trial gaps, not explainable by the 370-vs-360 denominator).

## Head-to-head vs Approach A (frozen a_raw sense, identical fixtures)

- Primary accuracy: R26 69.2% vs A 74.1% (Δ −4.9pp, R26 worse).
- Per-task primary (A vs R26): colordisc 48.3% vs 78.3%; colorconst 87.5% vs
  90.0%; shapetrans 100% vs 40.0%; motiondir 41.7% vs 78.3%.
  (pitchdisc/timbredisc per-task A not measured — audio too slow for a
  synchronous per-task loop; included in the aggregate.)
- p95 ops: R26 1,112,292 vs A 4,521,065 (R26 = 24.6% of A).
- A had 1 trial error / 925.

## Disposition distribution (925 trials, contract)

NEGATIVE_EVIDENCE 465, CORROBORATED 151, SUPPRESSED 104, WITHHELD 88,
PROVISIONAL_INSTALL 65, CONFLICT_WITHHELD 48, PERMANENT_INSTALL 4.
prog: PASS 309 / FAIL 465 / UNRESOLVED 151. normcmp: EQUAL 635 / DIFFER 290.

## Files

- `sense_raw_run{1,2,3}.log` — full per-trial outputs, byte-identical ×3
  (sha256 `af5dc8321851c03e034c50c021cd5eac770307418acab6d082453f40a088146d`)
- `records.txt` — memgate input (925 lines, seq order)
- `dispositions.txt` — memgate dispositions; `ledger.txt` — hash-chained ledger
  (independently verified 925/925, see `ledger_verify.json`)
- `sweep.jsonl`, `metrics.json`, `byte_identity.json`, `approach_a.json`
- `eval_r26.py` — the harness (test equipment)
- `BUILD_INFO.txt`, `R2FX_INCOMPAT.txt` — provenance and the R2A incompatibility proof
