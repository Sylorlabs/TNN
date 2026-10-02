# Attack A2: segmentation control weakness

Target: DEVINT1 builder commit `476c24b3d`, prereg `4b50ff7d4`.
Adversary prereg: `PREREG_ADVERSARY.md` (commit `60701a55f`, frozen).
Date: 2026-09-30.

## Construction

`adv_segctrl.zag` derived from the committed builder source
(`devint1.zag` at `476c24b3d`, 1079 lines, extracted via `git show`).
Builder S1-S4 machinery verbatim (treat loop and fixed-width-3 control
in `s4_run` unchanged). Only additions: three new S4 metric controls
that replace fixed-width-3 in the control role:

- `s4_ctrl_width(W,2)`: fixed-width-2 chunking (trailing clamp).
- `s4_ctrl_width(W,4)`: fixed-width-4 chunking (trailing clamp).
- `s4_ctrl_rand(W)`: random-width chunking, widths 1..5 per position
  from a seeded LCG (seed 1234567, multiplier 1103515245, mod 2^31-1,
  i64 arithmetic), reseeded per k so each k corpus is a prefix of the
  k+1 corpus, same design as the fixed-width controls.

Each measures full-coverage k (first k in 1..12 at which all 4 true
morphemes have count>=2) and spurious count (non-morpheme concepts with
count>=2) on the same S1 corpus. Emitted as `S4METRIC-CTRLFW2`,
`S4METRIC-CTRLFW4`, `S4METRIC-CTRLRAND`.

Built with frozen toolchain `znc 2026.07.0-dev`. Pure Zag, no Python.

## Determinism

3 runs, all exit 0, zero stderr bytes, `cmp` byte-identical 3/3.
md5 `09b6140ecd69f9d63b71f351e252a557`. Canonical run: `A2_RAW.txt`.

## Results

| Metric | Full-coverage k | Spurious |
|---|---|---|
| Treat (SEG-core, verbatim) | 5 | 0 |
| Control fixed-width-3 (verbatim) | 5 | 0 |
| Control fixed-width-2 (new) | -1 (never, k=1..12) | 0 |
| Control fixed-width-4 (new) | -1 (never, k=1..12) | 0 |
| Control random-width (new) | -1 (never, k=1..12) | 0 |

The verbatim treat and fw3 numbers reproduce the builder exactly
(treat-k=5=ctrl-k=5, 0 spurious). All three new controls fail to reach
full coverage at any k<=12 (k=-1). Expected: fixed-width-2/4 chunks can
never equal the true 3-char morphemes, and random-width hits all four
morphemes twice too rarely.

Note: STATE-CONT checksums at stages 7+ differ from the builder raw
while all counts and emitted numbers are identical. Cause: the three new
control measurements call `tick(W)` (36 extra ticks, one per k), which
shifts `last_used` timestamps stored in the concept/rule tables that the
checksum hashes. Behavioural state (counts, emissions, BUILD-PASS) is
byte-identical to the builder through S11. Determinism 3/3 holds.

## Verdict: ATTACK-SUCCEEDS (control artifact confirmed)

Frozen criterion: ATTACK-SUCCEEDS if treat reaches full coverage at
k <= 5 with 0 spurious while ALL of fw2/fw4/randwidth need k > 8 or
produce >= 3 spurious. Observed: treat k=5 spur=0; fw2, fw4, and
random-width all never reach coverage (k=-1, i.e. k > 8 required).
Criterion met on all clauses.

The builder's S4 neutral tie (treat-k=5 = ctrl-k=5) is confirmed as an
artifact of the control choice: fixed-width-3 is the ONLY control width
that can produce 3-char morpheme concepts, so the tie was guaranteed by
the width match, exactly as the builder's disclosure admitted. Against
width-mismatched controls the learned SEG-core segmentation strictly
dominates (k=5/0 vs never-covered), so the S4 synergy claim is revived
as positive rather than neutral vs any control that does not encode the
true width. The engineering BUILD-PASS is not contested by this attack;
only the interpretation of the S4 metric.
