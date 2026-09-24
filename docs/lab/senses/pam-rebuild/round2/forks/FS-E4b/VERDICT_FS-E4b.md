# VERDICT_FS-E4b — Cross-Span Concurrence on R2A

## Prereg

`round2/preregs/PREREG_FS-E4b.md`, committed alone a9a48b3f before any
results. Frozen hypothesis: cross-span concurrence (R2-7's formation
judgment on the G-span as independent witness; INSTALL iff
formation(F)==formation(G)==claim AND the discriminative challenge passes)
scales the safe+live profile to R2A.

## Mechanism (as built)

- `src/r27fe.zag`: vendored frozen R2-7 front-ends (1-line diff: main
  renamed).
- `src/e4b.zag`: pure-Zag driver; base = R2-7 full mode; booster = base +
  G-agreement conjunct. Zero RNG; deterministic.
- Base parity: 5/5 dispositions match the rebuilt frozen r27 binary.

## Battery (fresh deterministic draw)

- Per eligible task (colordisc, colorconst, timbredisc, motiondir;
  shapetrans excluded a priori per prereg; pitchdisc did NOT qualify):
  8,000 adversarial candidates (indices 200000–207999) + 1,500 normal
  candidates (indices 100000–101499), MASTER=20260923, splitmix streams.
  Disjoint from R2-7's measured slices.
- F-fooled = formF != truth; TRUE = normal candidates.
- Qualification (≥2,000 F-fooled AND ≥1,000 TRUE):
  - colordisc: 6,563 F-fooled / 1,500 TRUE → QUALIFIES
  - colorconst: 5,293 F-fooled / 1,500 TRUE → QUALIFIES
  - pitchdisc: 1,042 F-fooled / 1,500 TRUE → DOES NOT QUALIFY
  - timbredisc: 5,879 F-fooled / 1,500 TRUE → QUALIFIES
  - motiondir: 4,293 F-fooled / 1,500 TRUE → QUALIFIES
- Final battery: 12,000 trials (4 tasks × 3,000: 2,000 adv + 1,000 ctrl).

## Results

(See `evidence/SCORES_E4B.md` for full numbers.)

Per-task (booster):
- colordisc: FI 0/2000 (UCB 0.0019) PASS; recall 0.9040 PASS
- colorconst: FI 1/2000 (UCB 0.0028) PASS; recall 0.4420 FAIL
- timbredisc: FI 304/2000 (UCB 0.1684) FAIL; recall 0.1600 FAIL
- motiondir: FI 0/2000 (UCB 0.0019) PASS; recall 0.0000 FAIL

Pooled (n_adv=8000, n_ctrl=4000):
- FI_booster 305/8000 = 0.0381, 95% UCB 0.0425 (bar ≤0.01): FAIL
- recall_booster 0.3765 (bar ≥0.85): FAIL
- wrong_on_TRUE_booster: 37

Ablation:
- pooled FI_base/FI_booster = 528/305 = 1.731 (bar ≥2): FAIL

## Joint bars

1. FI 95% Wilson UCB ≤ 1% (per task + pooled): FAIL (timbredisc 0.1684,
   pooled 0.0425)
2. Recall ≥ 85% (per task + pooled): FAIL (colorconst 0.442, timbredisc
   0.160, motiondir 0.000, pooled 0.3765)
3. Ablation pooled FI_base/FI_booster ≥ 2: FAIL (1.731)
4. Determinism byte-identical ×2, hash chains verify: PASS (16/16
   ledgers byte-identical; all 20 hash chains verify)

## Availability-cost diagnostic

Booster recall on corrupted-G TRUE set: 0.0000 (vs clean 0.3765).
Availability cost = 0.3765. Under adversarially corrupted G, the booster
never installs (formG never matches formF). Not gated; diagnostic only.

## Verdict

**DEAD** — Cross-span concurrence does not scale to R2A. The booster
fails three of the four joint bars: (1) FI 95% UCB exceeds 1% on
timbredisc (16.8%) and pooled (4.25%); (2) recall falls below 85% on
three of four tasks (colorconst 44%, timbredisc 16%, motiondir 0%) and
pooled (37.6%); (3) the ablation ratio is 1.73×, below the required 2×.
Only colordisc passes both bars individually. The mechanism is too
conservative on TRUE (motiondir recall 0.0 — the G-agreement conjunct
never fires) and too permissive on adversarial timbredisc (15.2% FI).
Determinism holds (byte-identical ×2, all hash chains verify), but the
hypothesis is falsified on the performance bars.

## Commits

- FS-E4 closeout: 7b24f0c5
- FS-E4b prereg (alone): a9a48b3f
- FS-E4b sources: 6d9942d7 (+ fix bda95a8f)
- FS-E4b evidence + verdict: [SHA]
