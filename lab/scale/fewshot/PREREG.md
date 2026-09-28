# FEW-SHOT / SCALE-DOWN preregistration — frozen 2026-09-21/22

Micah's question: the TNN learns shockingly fast (1.0 mastery at 240 facts and
at 6.58M). What happens BELOW 240? Find the floor. Does one-shot learning work?

## Instrument

`fewshot_learner.zag` = `scale_learner.zag` (frozen scale driver, validated
N=240 vs `run240_r0.log`) with exactly three harness-side changes (build
notes, behavior-identical at off=0, C=24):

1. **Config gate relaxed**: `c==24` → `1<=c<=24`, still requiring `n==c*m`.
   Lets N<24 run (N=C, M=1). No learner-code path changes.
2. **Fact-id offset** (new argv 8, default 0): store keys stay dense `0..n-1`;
   the FACTSPEC id used for truth/supplied/is_false becomes `fid=off+id`.
   Lets us place the taught window over a planted falsehood
   (e.g. N=1 off=6 teaches only id 6, a frozen plant; N=2 off=5 teaches
   ids 5,6 = one clean + one plant). The frozen `is_false` draw is untouched.
3. **Recall-timing microbenchmark** after SCALE_DIGEST, before SCALE_DONE:
   2000 iterations × n `sc_recall` calls timed with `clock_gettime`
   (CLOCK_MONOTONIC) via `_zag_raw_syscall`; prints one
   `SCALE_RECALL_TIMING` line. Read-only w.r.t. the store; excluded from
   byte-identity hashing (stripped before md5), timing is wall-clock.

Validation gate: N=240,C=24,M=10,P=3,off=0 must reproduce the frozen
`run240_r0.log` byte-identically (timing line stripped) before any few-shot
run counts.

## Run matrix (all P=1, single teaching pass; eval mode)

| N | C | M | off | plants in window | purpose |
|---|---|---|---|---|---|
| 192 | 24 | 8 | 0 | 13 | curve |
| 128 | 16 | 8 | 0 | 9 | curve |
| 96 | 24 | 4 | 0 | 5 | curve |
| 64 | 16 | 4 | 0 | 4 | curve |
| 48 | 24 | 2 | 0 | 3 | curve |
| 32 | 16 | 2 | 0 | 3 | curve |
| 24 | 24 | 1 | 0 | 2 | curve |
| 16 | 16 | 1 | 0 | 2 | curve |
| 8 | 8 | 1 | 0 | 1 (id 6) | minimal mixed (true+false) |
| 4 | 4 | 1 | 0 | 0 | curve (absorption N/A) |
| 2 | 2 | 1 | 0 | 0 | curve (absorption N/A) |
| 1 | 1 | 1 | 0 | 0 | one-shot clean (id 0) |
| 1 | 1 | 1 | 6 | 1 (id 6) | one-shot PLANT (absorption 1/1?) |
| 2 | 2 | 1 | 5 | 1 (id 6) | one-shot mixed: id5 clean + id6 plant |

Plant windows computed from the frozen draw, replica verified 114/114 against
`corpus_m100.json` false_ids. Under the frozen `is_false` rule, dense windows
at N=4,2,1 (off=0) contain no plants — absorption is N/A there, reported
honestly, not forced.

## Measures per config

- clean mastery (num/den), all-fact mastery, absorption (num/den or N/A),
  SCALE_FLAW families, ops/fact (x1000), bytes/fact, deciles, digest.
- Flaw battery: meaningful (24 distinct probe ids) at N>=96; below that probe
  ids collide — families reported with distinct-id count and a degeneracy
  caveat, not presented as a 96-probe result.
- Determinism: 5 reps per config, md5 of log minus SCALE_RECALL_TIMING line
  must collapse to 1 hash.
- Recall latency: ns_per_recall from the microbenchmark at N=240 (and the
  ladder for shape). Wall-clock, reported as measured, not byte-identical.

## Decision rules (measurement, not kill bars)

- Report the smallest N with clean mastery 1.0, and the N where it first
  breaks (if any). If mastery holds at N=1, that is the headline.
- One-shot verdicts: N=1/off=0 (clean held?), N=1/off=6 (plant absorbed as
  supplied?), N=2/off=5 (clean recalled as truth AND plant recalled as
  supplied in the same 2-fact store?).
- No kill bars: this is a floor-finding measurement. Nothing here changes
  frozen championship rules.

## Constraints

Pure Zag, zero RNG in decision paths, learner code untouched. Corpus texts
read at runtime as in the scale driver (fixed ~1.4s init per run).
