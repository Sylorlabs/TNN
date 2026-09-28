# PREDICTIONS_LOCKED.md — H7 exp2c Stage-2 predictions

Locked **before** any Stage-2 (vol/de) run. Stage-1 legs (ab-a, ab-b, abc-a,
abc-b, ab-a-rev) already ran; their outcomes are recorded below as OBSERVED
(post-hoc), not predictions. Only the Stage-2 section is a genuine a priori
prediction.

## Stage-1 OBSERVED (post-hoc, not predicted)

| leg | design | corpus | order | 2c_sinc_lk_3 | other 2c bars |
|---|---|---|---|---|---|
| base (control) | — | — | — | 3/10 FAIL | all pass |
| ab-a | α | A+B | E→W | 9/10 PASS | all pass |
| ab-b | β | A+B | E→W | 9/10 PASS | all pass |
| abc-a | α | A+B+C | E→W | 0/10 FAIL | SINC-DP fail t1,2,4,5; SINC-LK fail t2,4 |
| abc-b | β | A+B+C | E→W | 10/10 PASS | all pass |
| ab-a-rev | α | A+B | W→E | 9/10 PASS | all pass |

Mechanism (from MDUMP diffs, post-hoc): abc-a's family-C joke W-items install
promiscuous JOKE markers (`says evenly`, `evenly`, `is a`, `it is a` — CTX and
generic UTT ngrams from the absurd utterances). The family-C E-items run BEFORE
the W-items, so their eliminative revocation cannot remove them; design α's
final calibrate (original 40-item pool) does not match them either. They survive
and fire on every SINC probe with a "says evenly/plainly" context → mass
WITHHOLD (SINC-LK 0/10 on types 2,3,4,5; SINC-DP 4–5/10). Design β appends the
24 E-items to the endorse pool, so the final calibrate revokes exactly those
promiscuous markers → abc-b is pristine (all bars pass, LK 10/10 on types 2,3,4).

## Stage-2 A PRIORI predictions

### vol-a — design α, 96 volume items (16E+16W × families A,B,C), E→W

Family C runs under α with 16E+16W (vs 8+8 in abc-a): the same structural
hazard, more installs. PREDICT:
- `2c_sinc_dp_*` FAILS for ≥3 types (SINC-DP ≤5/10 on types 2,3,4,5).
- `2c_sinc_lk_3` FAILS (≤5/10); `2c_sinc_lk_2` and `2c_sinc_lk_4` also FAIL.
- TR/PA/NO per type stay ≥16/20 (typed learning itself is intact).
- MDUMP: live (status 1) joke field-1 markers `says evenly` / `says plainly`
  present; they are absent-or-revoked in vol-b.
- Falsification: if vol-a passes all 2c bars, the abc-a catastrophe was an
  8+8-sample artifact, not structural.

### vol-b — design β, 96 volume items, E→W

β's pool-append (now 48 E-items in pool) drives the final calibrate to revoke
promiscuous markers. PREDICT:
- ALL `2c_*` checks PASS; `2c_sinc_lk_3` ≥9/10.
- MDUMP: joke `says evenly` / `says plainly` CTX markers status 3 (revoked).
- Falsification: any 2c SINC-DP/LK failure here means volume alone (not just
  family C) breaks the bars under β.

### de-a — design α, 32 new-family items (D `what if` 8E+8W, E `where do` 8E+8W)

Structural analog of ab-a: W-items teach toward hypothetical (ti=2), no joke
re-keying, E-items run first and revoke promiscuous hypothetical markers.
PREDICT:
- ALL `2c_*` checks PASS; `2c_sinc_lk_3` ≥9/10.
- MDUMP: hypothetical `what if` / `where do` UTT markers live (status 1);
  hypothetical CTX `says evenly`/`says plainly` revoked (status 3), as in ab-a.
- Falsification: failure here means the mechanism does NOT generalize beyond
  the original A/B bigrams.

### de-b — design β, 32 new-family items

Same as de-a plus pool-append. PREDICT: ALL `2c_*` PASS, `2c_sinc_lk_3` ≥9/10.
MDUMP like de-a. Falsification: any failure means β's pool-append harms novel
families.

## Cross-leg predictions

- Determinism: every leg 3/3 byte-identical reps (SHA-256 recorded).
- Frozen `H7_CHECK` lines (pre-2c state) unchanged in every leg except the
  self-adjusting `nofilter_guards` (tn+1) and the expected `2c_*` additions.
- `2CITEMS|`: vol legs 96, de legs 32, pool 40 (α) / 88 (β: 40+48) for vol,
  40/72 for de.
- No new HARD0 scanner hits beyond the frozen filename-prefix false positives
  (to be verified by audit before the final report).

Locked: 2026-09-27, before any vol/de run.
