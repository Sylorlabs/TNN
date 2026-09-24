# FS-E4b scores vs frozen joint bars

Tasks run: colordisc, colorconst, timbredisc, motiondir

Battery per task: 2,000 F-fooled adversarial + 1,000 TRUE controls.

## Per-task

| task | n_adv | FI_base k | FI_base rate | FI_boost k | FI_boost rate | FI_boost 95% UCB | n_ctrl | rec_base | rec_boost | wrong_on_TRUE_boost | n_cor | rec_corrupt_boost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| colordisc | 2000 | 0 | 0.0000 | 0 | 0.0000 | 0.0019 | 1000 | 0.9130 | 0.9040 | 0 | 1000 | 0.0000 |
| colorconst | 2000 | 1 | 0.0005 | 1 | 0.0005 | 0.0028 | 1000 | 0.5330 | 0.4420 | 1 | 1000 | 0.0000 |
  BAR2-FAIL: colorconst booster recall 0.4420 < 0.85
| timbredisc | 2000 | 527 | 0.2635 | 304 | 0.1520 | 0.1684 | 1000 | 0.2040 | 0.1600 | 36 | 1000 | 0.0000 |
  BAR1-FAIL: timbredisc FI booster UCB 0.1684 > 0.01
  BAR2-FAIL: timbredisc booster recall 0.1600 < 0.85
| motiondir | 2000 | 0 | 0.0000 | 0 | 0.0000 | 0.0019 | 1000 | 0.0000 | 0.0000 | 0 | 1000 | 0.0000 |
  BAR2-FAIL: motiondir booster recall 0.0000 < 0.85

## Pooled

- n_adv=8000 FI_base=528 (0.0660) FI_booster=305 (0.0381) 95% UCB=0.0425 (bar <=0.01)
- n_ctrl=4000 rec_base=0.4125 rec_booster=0.3765 (bar >=0.85); wrong_on_TRUE_booster=37
- n_corrupt=4000 rec_corrupt_booster=0.0000; availability cost = 0.3765 (clean rec 0.3765 - corrupt rec 0.0000)
  BAR1-FAIL (pooled): FI booster UCB 0.0425 > 0.01
  BAR2-FAIL (pooled): booster recall 0.3765 < 0.85

## Ablation (bar 3)

- pooled FI_base/FI_booster = 1.731 (bar >= 2)
  BAR3-FAIL: ablation ratio 1.731 < 2

## Determinism (bar 4)

- run_battery.py: full battery run twice; stdout logs + ledgers byte-identical (see run log).
- verify_chain.py: every hash-chain line of every run ledger verified (see run log).

## Verdict

- ALIVE iff bars 1-4 all pass; DEAD on recall/FI/ablation/determinism failure.
- JOINT BARS: FAIL
- HYPOTHESIS (cross-span concurrence scales to R2A): DEAD
