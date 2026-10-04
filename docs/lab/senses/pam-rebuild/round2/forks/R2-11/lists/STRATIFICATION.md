# R2-11 frozen list stratification (seed 20260923)

## scoring_10000.txt

Task-major order (colordisc, colorconst, shapetrans, pitchdisc,
timbredisc, motiondir); within a task: all adversarial first
(generated index order, then frozen name order), then the
stride-selected normal quota from [generated, frozen primary,
frozen noise]. Stride: index j -> (j*count)//quota.

| task | adv (gen+frozen) | normal quota (pool) |
|---|---|---|
| colordisc | 1180 | 822 (1200) |
| colorconst | 700 | 548 (800) |
| shapetrans | 1195 | 1011 (1476) |
| pitchdisc | 1180 | 575 (840) |
| timbredisc | 720 | 575 (840) |
| motiondir | 1025 | 469 (684) |

Total: 6000 adversarial + 4000 normal = 10000.

## human_200.txt

100 adversarial: 5 per each of 17 R2A families + 1 extra to the
15 largest families (stride-selected within family).
100 clean: stride-selected from the per-task normal pool; 17 each
for the 4 largest task pools, 16 each for the other two.
Blind order: Fisher-Yates with splitmix64(SEED=20260923).
Format: `HNNN task lab/relative/path KIND` (KIND = family or CLEAN).

### adversarial quotas

- colorconst CCN-1: 6 of 380
- colorconst CCN-2: 6 of 300
- colordisc COL-1: 6 of 400
- colordisc COL-2: 6 of 350
- colordisc COL-3: 6 of 400
- motiondir MOT-1: 6 of 345
- motiondir MOT-2: 6 of 330
- motiondir MOT-3: 6 of 320
- pitchdisc PTC-1: 6 of 400
- pitchdisc PTC-2: 6 of 350
- pitchdisc PTC-3: 6 of 400
- shapetrans SHP-1: 6 of 400
- shapetrans SHP-2: 6 of 350
- shapetrans SHP-3: 6 of 400
- timbredisc TMB-1: 6 of 250
- timbredisc TMB-2: 5 of 220
- timbredisc TMB-3: 5 of 220

### clean quotas

- colordisc: 17 of 1200
- colorconst: 16 of 800
- shapetrans: 17 of 1476
- pitchdisc: 17 of 840
- timbredisc: 17 of 840
- motiondir: 16 of 684
