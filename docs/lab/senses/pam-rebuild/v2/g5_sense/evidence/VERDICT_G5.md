# VERDICT G5 — KILL

**Hypothesis:** G5 "heavy second-pass sense aimed at the 278" (champion C)
**Date:** 2026-09-24
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_G5_SENSE.md` (commit b1bb14d290ebe30a4629b5e20a53363433a0fdb2)

## Verdict

**KILL** — killed by the steel bar (d). The second sense re-emits PASS on
6/6 timbredisc wrongs. Per the frozen prereg and Micah's order ("If G5 is
killed, say so plainly and stop. No rescue missions."), the hypothesis is
dead. No tuning, no rescue.

## Measured values

| Leg | Result | Kill bar | Status |
|-----|--------|----------|--------|
| (1) Conversion (278) | 153/278 truth-agreeing PASS; 0 wrong-label | KILL iff <100 | PASS (moot) |
| (2) Mint (sealed 288) | G5 new false-PASS: 0; system rate 67/288=23.26% (unchanged) | KILL iff G_new>=6 | PASS (moot) |
| (3) Regression (V2-D replay) | NOT COMPLETED — stopped after steel kill | KILL iff RK-3'<88.48% | MOOT |
| (4) Steel (6 timbredisc wrongs) | 6/6 re-PASS | KILL iff >=2 | **KILL** |

## What the steel failure means

The six timbredisc wrongs (seqs 10983, 10992, 11024, 11049, 11126, 11192;
sense said RICH, truth BRIGHT, conf 701-718) are spoofed trials where the
wrong label is sustained in the raw audio. G5's heavier measurement (4-window
averaged spectral centroid) sees RICH with very large margin (centroid ~2630,
threshold 900) on all six — it measures the same spoofed features more
confidently, not the truth. This is exactly the correlated-wrongs failure
mode champion C's steel bar was designed to catch: the second sense learned
the spoof features.

## Conversion detail (leg 1, for the record)

153/278 conversions, all pitchdisc (153/155 convertible pitchdisc; 2
deliberation-blocked abstained per trigger). Zero conversions on colordisc
(0/2), colorconst (0/6), timbredisc (0/0 convertible). The 115 harness trials
correctly abstained (no G span). The denser G measurement works where the
underlying signal is genuine (pitchdisc harmonic energy) and correctly
abstains where it is not — but it cannot discriminate sustained spoof, which
is what the steel bar tests.

## Evidence

- `evidence/leg1_results.txt` — 278 per-trial g5sense outputs (run 1)
- `evidence/leg2_results.txt` — 288 sealed per-trial outputs (run 1)
- `evidence/leg4_run1.log` — 6 steel forced runs
- `evidence/leg1_run1.log`, `evidence/leg2_run1.log` — run logs
- Source: `src/g5sense.zag` (+ helpers), `src/leg1_driver.py`, `src/leg2_driver.py`
- Prereg: `../preregs/PREREG_G5_SENSE.md`

## Note on determinism

Only one run of each leg completed before the steel kill stopped the battery.
The prereg required three byte-identical runs; these were not performed because
the hypothesis was killed. The single-run outputs are committed as evidence
of the kill, not as a surviving result.
