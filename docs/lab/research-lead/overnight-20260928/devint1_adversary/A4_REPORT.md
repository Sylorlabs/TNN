# A4 Report: causal attribution (ablation of upstream structures)

Worker: DEVINT1 Adversary Worker B. Date: 2026-09-30.
Target: DEVINT1 builder commit `476c24b3d`, prereg `4b50ff7d4`.
Frozen criteria: `PREREG_ADVERSARY.md` (commit `60701a55f`), Attack A4.
Builder baseline (intact): S6 treat=4 ctrl=5; S10 probe treat=8/12 ctrl=0/12;
S11 recog 17/17, proc-reuse 3/3.

## Constructions (one structure removed each, everything else identical)

- `adv_noSeg.zag`: `segment()` replaced by fixed-width-3 chunking (remainder
  chunk for lengths not divisible by 3); lexicon still fed, ignored by the
  chunker. Concepts/rules/procedures learn from chunks.
- `adv_noConcepts.zag`: `conc_touch()` no longer counts recurrence (count
  frozen at 1); the table becomes pure content interning, so downstream
  learning keys on raw segmented strings. No segment is ever promoted to a
  concept; S3 inventory, boundary-violation detection (count>=2 gate), and
  split refinement are definitionally empty.
- `adv_noRules.zag`: no ACTIVE promotion in `rule_touch()`; `rule_predict()`
  is the raw bigram argmax; `apply_revision()` is a no-op (no demote/rollback);
  S8 competing-rule selection uses raw bigram counts. Twin stores and both
  eviction policies retained.

Pure Zag. Each variant 3/3 runs byte-identical. Raw output: `A4_RAW.txt`
(all three variants, 3 runs each, with headers).

## Results

| variant | S6 treat/ctrl | S10 probe treat/ctrl | S11 recog / reuse |
|---|---|---|---|
| baseline | 4 / 5 | 8/12 / 0/12 | 17/17, 3/3 |
| noSeg | 4 / 5 | 8/12 / 0/12 | 17/17, 3/3 |
| noConcepts | 4 / 5 | 8/12 / 0/12 | 17/17, 3/3 |
| noRules | 4 / 5 | 3/12 / 0/12 | 17/17, 3/3 |

Builder treat-minus-ctrl gaps: S6 = 1 example; S10 = 8 correct. (S11 has no
builder treat/ctrl gap, so the 50% threshold is undefined there; raw
comparison is reported.)

## Per-pair verdicts (frozen: degradation >= 50% of gap, or sign flip)

- (noSeg, S6): degradation 0 examples (4 vs 4; threshold 0.5). Sign intact
  (4<5). **ATTACK-FAILS.** Note: the S1/S2 corpora are entirely 3-aligned, so
  fixed-width-3 chunking reproduces the true segmentation on the stages that
  feed S6; this ablation cannot separate the DP segmenter from the corpus
  alignment (the same confound the builder disclosed for S4). Secondary: the
  variant still BUILD-PASSes, and its S4 metric reaches coverage at k=5 with 0
  spurious under fw3, confirming the alignment confound rather than refuting
  segmentation.
- (noConcepts, S6): degradation 0 (4 vs 4). **ATTACK-FAILS.**
  (noConcepts, S11): 17/17 and 3/3 unchanged; no builder gap exists, raw
  degradation is zero. **ATTACK-FAILS (descriptive).** Interpretation: the
  learned concept inventory beyond string interning carries none of the
  measured S6/S10/S11 synergy. The S6 gap survives because it is carried by
  1-substitution recognition over interned strings, and the S10 gap by rule
  support/eviction, neither of which needs recurrence counts.
- (noRules, S10): degradation 5 correct (8 -> 3; threshold 4). Sign intact
  (3>0). **ATTACK-SUCCEEDS (causal).** Removing ACTIVE/rollback while keeping
  raw bigram counts destroys 5 of the 8 probe points: the probe advantage is
  causally carried by the revision machinery (rollback of bik->gup lets
  bik->zol win), not by bigram frequency. Corroborating: S9 revision
  changed=0 (vs 1), survivor reverts to bik->gup, and S7 logs 5 contradictions
  (vs 4) because the raw argmax predicts where no ACTIVE rule existed.
  (noRules, S11): 17/17 and 3/3 unchanged. **ATTACK-FAILS (descriptive).**

## Overall verdict

1 of 3 ablations shows causal degradation on its primary metric. Per the
frozen criterion (>=2 of 3 required), overall **ATTACK-FAILS**: the synergy is
not shown to be correlational in general, but one clean causal link is
established (rules -> S10 probe) and two non-links are established
(segmentation and the learned concept inventory are causally inert for S6 on
this corpus; the concept inventory is inert for S10/S11 as well).
