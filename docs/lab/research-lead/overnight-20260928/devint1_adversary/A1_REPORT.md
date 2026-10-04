# Attack A1: future-data leakage (online variant)

Target: DEVINT1 builder commit `476c24b3d`, prereg `4b50ff7d4`.
Adversary prereg: `PREREG_ADVERSARY.md` (commit `60701a55f`, frozen).
Date: 2026-09-30.

## Construction

`adv_online.zag` derived from the committed builder source
(`devint1.zag` at `476c24b3d`, 1079 lines, extracted via `git show`).
All learner machinery is verbatim. The only changes vs builder:

1. New `process_single` (derived from `process_nofeed`): concept/rule
   updates from single-char segments, used for episode t=0.
2. Main S1 schedule: episode t is segmented using ONLY the lexicon from
   episodes 0..t-1 (empty at t=0, single-char fallback), then the episode
   is fed to the lexicon. Concepts/rules update after each episode as in
   the builder. Builder phase A (lexicon from all 12 first) is removed.
3. Stages S2..S11 unchanged, run on the resulting state.

Built with frozen toolchain `znc 2026.07.0-dev`. Pure Zag, no Python.

## Determinism

3 runs, all exit 0, zero stderr bytes, `cmp` byte-identical 3/3.
md5 `36800372b4611ac50b1188c09317685b`. Canonical run: `A1_RAW.txt`.

## Results (builder baseline -> attack)

| Stage | Builder | A1 online |
|---|---|---|
| S2 correct segmentations | 6/6 | 6/6 (byte-identical lines) |
| S3 concepts | bik:11 gup:14 zol:10 tav:10 | gup:11 zol:10 bi:2 kgup:2 tav:10 bik:8 |
| S4 bigrams | 12 | 19 (12 real + junk from char concepts) |
| S5 ACTIVE rules | 4 | 4 (same set: bik->gup, gup->zol, gup->bik, zol->tav) |
| S6 treat/ctrl | 4/5, held 5/5 | 4/5, held 5/5 |
| S7 contradictions / boundary | 4 / 2 | 4 / 3 (bik bi tav) |
| S8 inquiry / acc | ctx=bik, 1/6 both | ctx=bik, 3/6 both |
| S9 revision / acc | 1, bik->zol, 3/6 | 1, bik->zol, 3/6 |
| S10 evict treat/ctrl | 17 / 18 | 21 / 21 |
| S10 probe treat/ctrl | 8/12 / 0/12 | 8/12 / 0/12 |
| S11 recognition / proc reuse | 17/17, 3/3 | 17/17, 3/3 |
| S4 metric treat-k/spur, ctrl-k/spur | 5/0, 5/0 | 5/0, 5/0 |
| Verdict | BUILD-PASS | BUILD-PASS |

## Verdict: PARTIAL

Frozen criteria applied without modification:

- KILL the "no leakage" reading? Requires S2 < 4/6, or < 3 true
  morphemes, or trajectory abort. Observed: S2 = 6/6, 4/4 true morphemes
  (bik, gup, zol, tav all count>=2), BUILD-PASS with non-decreasing
  STATE-CONT counts. No kill condition met.
- DOWNGRADE? Requires S2 = 4-5/6 (observed 6/6), or true morphemes
  recovered while segment/rule numbers degrade > 30% vs baseline.
  S2 = 6/6, S5 ACTIVE = 4, S7 contradictions = 4; nothing degraded > 30%.
  No downgrade condition met.
- ATTACK-FAILS? Requires S2 = 6/6 (yes), 4 concepts (yes), AND all B2
  stage numbers within 10% of builder values. FAILED: bik count 11->8
  (-27%), gup count 14->11 (-21%), S4 bigrams 12->19 (+58%),
  S7 boundary 2->3 (+50%), S8 acc 1/6->3/6, S10 evictions 17/18->21/21.

The attack failed to kill or downgrade the "no leakage" reading: the
qualitative trajectory (segmentations, morpheme inventory, all frozen
bars, final BUILD-PASS) survives strict online feeding. But the learned
inventory is measurably different: the t=0 empty-lexicon episode leaves
persistent single-char concepts (STATE-CONT shows 12 concepts at S1 vs
builder 4), two spurious concepts survive to S3 (`bi:2`, `kgup:2`), and
several B2 numbers fall outside the 10% tolerance. So the strict
ATTACK-FAILS bar is also not met. PARTIAL: qualitatively robust,
quantitatively sensitive to the feed schedule.
