# J1 Death Certificate — Fixed-k Competing Tilings (STRUCT)

**Arm:** J1 (STRUCT) — Fixed-k competing tilings  
**Date of death:** 2026-09-21  
**Cause:** Kill criterion 1 (binding)  
**Scale:** 1x (r1)  

## Cause of Death

Kill criterion 1 fired on both M1 corpora:

> Best-of-k ≤ best single tiling + 2 points at equal total budget on
> adversarial-cut corpus.

The three-tiling arbitration (T0 word-runs, T1 phase-shifted, T2 64-byte grid
with α/β/γ scoring) achieved:
- **prose.bin:** 96.2% word coverage vs 94.4% for best single (T2) — **+1.8 pts**
- **code.bin:** 93.9% word coverage vs 92.2% for best single (T2) — **+1.7 pts**

Both are ≤ 2.0 points. The complexity is not justified.

## What Worked

- M1 recall/boundary: 100.0% on both corpora (2.0M and 2.6M units)
- A15 ID-remapping probe: PASS (PROVISIONAL-PENDING-FREEZE)
- Kill criterion 2: PASS (zero non-covering choices, zero suboptimal choices)
- Zero RNG, byte-identical reruns, pure Zag

## What Didn't

The fundamental hypothesis — that three competing fixed tilings with
deterministic arbitration would significantly outperform the best single
tiling — was falsified. The 64-byte fixed grid (T2) alone covers 92-94% of
words; adding two more tilings and arbitration only gains 1.7-1.8 points.

## Evidence

- `work/battery/r1_1x/m1-1x-prose/stdout.log`: `J1_ADV prose.bin ... kill_i=1`
- `work/battery/r1_1x/m1-1x-code/stdout.log`: `J1_ADV code.bin ... kill_i=1`
- `VERDICT.md`: Full kill-criteria evaluation
- `ARM_SPEC.md`: Mechanism specification
- `BUILD_LOG.md`: Implementation history

## Provisional Items (for the record)

- A15 schedule: PROVISIONAL-PENDING-FREEZE (probe PASS)
- α/β/γ=2/1/1, tiling values 20/16/8, recency=seq mod 64: judgment-set, not frozen
- Kill (i) "equal budget" reading: documented in VERDICT.md

---

*J1 was built and tested per the frozen prereg. It died by its own binding
kill criterion, as designed. The evidence is committed; the mechanism is
abandoned.*
