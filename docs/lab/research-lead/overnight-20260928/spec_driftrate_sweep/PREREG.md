# SPEC-DRIFTRATE-SWEEP: PREREG (frozen)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_driftrate_sweep/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent result:** SPEC-REFUSAL-RECOVERY BUILD-PASS (11/11), 2026-10-03.
**Task:** quantify the eager-recovery break-even: at what drift/query ratio
does eager recovery beat lazy refusal, and where does recovery stop being
worth it.

## Question

SPEC-REFUSAL-RECOVERY reasoned (not measured) that recovery dominates
repeated refusal whenever the learner expects at least one more query, and
is pure overhead when the world churns faster than queries arrive. This lane
measures that tradeoff: sweep drift rate against query rate, count rebuilds
vs answered queries per policy, and locate the crossover.

## Hypotheses

H1: Eager recovery answers every query at every drift rate (correctness is
rate-independent). Its cost is exactly one rebuild per drift per episode,
independent of the query rate: rebuilds = D in every cell.

H2: Lazy on-demand recovery (rebuild only when a query actually refuses)
answers every query too, and never rebuilds more than eager: on this
schedule its rebuilds equal the number of drifts followed by at least one
query before the next drift.

H3: Refuse-only answers nothing after the first drift at any rate
(rebuilds = 0, answered = 0): the baseline that prices what eager's
rebuilds buy.

H4 (unit-economics crossover): eager pays rebuilds/answered = D/Q = 1/k
rebuilds per answered query, where k = queries per drift. The sweep spans
k in [1/16, 16], bracketing k = 1, the point where eager starts paying
more than one rebuild per answer served.

H5 (eager-vs-lazy waste crossover): at high churn (k << 1) eager pays many
times lazy's rebuilds (wasted rebuilds on drifts no query ever sees); at
saturation (k >= 1 on this grid) eager and lazy pay identically.

## Frozen design

One binary, 75 episodes. Each episode is T = 256 ticks on a fresh world
(world_new + rb_setup + explicit epoch reset to 0 at offset 772, which
rb_setup predates; ret_log_rel for the query relation; et_specialize_ret
stamping epoch 0). The query family is RET only (rel via rb_rel_a(), obj
via rb_obj_a1()); the rate economics are per-family and identical in
structure for CNT/VFY, which the parent lane already proved correct.

Drift schedule: a drift every M ticks (tick 0 included; drift runs before
the query at coincident ticks). Query schedule: one query every N ticks.
M, N in {1, 2, 4, 8, 16} (countdown counters, no modulo operator). 25
cells. Per cell, three policy arms:

- EAGER: after every drift, et_specialize_ret immediately (eager rebuild),
  counted as one resp-style rebuild. Queries go through rr_ret_spec (the
  byte-unmodified SPEC-REFUSAL-RECOVERY wrapper).
- LAZY: no eager rebuild. Queries go through rr_ret_spec: the wrapper
  rebuilds only when the epoch gate actually refuses (on-demand recovery).
- REFUSE: queries go through et_ret_spec directly (refuse-only, never
  rebuild).

Drift type: et_drift_unrelated only, applied repeatedly. It is content-
idempotent (slot 2 obj set to the same alt value) and bumps the world
epoch every call, so it is repeatable indefinitely. This isolates the rate
economics from answer-change confounds: gen is constant (the queried fact
is untouched), every answered query has identical value, and agree=1 is
unambiguous. The parent lane already proved recovery correctness on
answer-changing drifts (9/9 agree=1); this lane prices the rate tradeoff,
it does not re-prove correctness. Using the unrelated drift is the
conservative choice: it is the case where eager recovery rebuilds for
answers that were already correct (the E1 cost the parent lane measured),
so the sweep quantifies exactly when that price is worth paying.

Per-episode counters (reset per episode): D (drifts executed), Q (queries
issued), rebuilds (re-specialize events), answered (queries with agree=1
against ret_gen), refusals (refusal-counter deltas), kb (kb-counter deltas
on the learner path only; the gen oracle's kb is reset and not counted).

Emitted line per episode:
CELL M=<m> N=<n> P=<eager|lazy|refuse> D=<d> Q=<q> rebuilds=<r>
answered=<a> refusals=<f> kb=<k>

## Frozen expected values

D = 256/M, Q = 256/N, k = Q/D = M/N. Predictions:

| M | D | N | Q | k | EAGER rebuilds | LAZY rebuilds | REFUSE rebuilds |
|---|---|---|---|---|----------------|---------------|-----------------|
| 1 | 256 | 1 | 256 | 1 | 256 | 256 | 0 |
| 1 | 256 | 2 | 128 | 1/2 | 256 | 128 | 0 |
| 1 | 256 | 4 | 64 | 1/4 | 256 | 64 | 0 |
| 1 | 256 | 8 | 32 | 1/8 | 256 | 32 | 0 |
| 1 | 256 | 16 | 16 | 1/16 | 256 | 16 | 0 |
| 2 | 128 | 1 | 256 | 2 | 128 | 128 | 0 |
| 2 | 128 | 2 | 128 | 1 | 128 | 128 | 0 |
| 2 | 128 | 4 | 64 | 1/2 | 128 | 64 | 0 |
| 2 | 128 | 8 | 32 | 1/4 | 128 | 32 | 0 |
| 2 | 128 | 16 | 16 | 1/8 | 128 | 16 | 0 |
| 4 | 64 | 1 | 256 | 4 | 64 | 64 | 0 |
| 4 | 64 | 2 | 128 | 2 | 64 | 64 | 0 |
| 4 | 64 | 4 | 64 | 1 | 64 | 64 | 0 |
| 4 | 64 | 8 | 32 | 1/2 | 64 | 32 | 0 |
| 4 | 64 | 16 | 16 | 1/4 | 64 | 16 | 0 |
| 8 | 32 | 1 | 256 | 8 | 32 | 32 | 0 |
| 8 | 32 | 2 | 128 | 4 | 32 | 32 | 0 |
| 8 | 32 | 4 | 64 | 2 | 32 | 32 | 0 |
| 8 | 32 | 8 | 32 | 1 | 32 | 32 | 0 |
| 8 | 32 | 16 | 16 | 1/2 | 32 | 16 | 0 |
| 16 | 16 | 1 | 256 | 16 | 16 | 16 | 0 |
| 16 | 16 | 2 | 128 | 8 | 16 | 16 | 0 |
| 16 | 16 | 4 | 64 | 4 | 16 | 16 | 0 |
| 16 | 16 | 8 | 32 | 2 | 16 | 16 | 0 |
| 16 | 16 | 16 | 16 | 1 | 16 | 16 | 0 |

LAZY rebuilds = min(D, Q) on this power-of-2 grid: when M >= N every drift
is followed by a query before the next drift (rebuilds = D); when M < N
every query follows at least one drift since the last rebuild
(rebuilds = Q, one per query). EAGER rebuilds = D always (one eager
rebuild per drift, even drifts no query ever sees).

Answered: Q on every EAGER and LAZY line (recovery correct at every rate);
0 on every REFUSE line (refusal yields no answer). Refusals: 0 on every
EAGER line (the eager restamp always precedes the next query); equal to
rebuilds on every LAZY line (one refusal triggers each on-demand rebuild,
and the single retry restamps, so no double refusals); equal to Q on every
REFUSE line (every query refuses exactly once). kb = 0 on every REFUSE
line (refusal never scans, at any rate).

## Break-even computation (frozen method, numbers filled in REPORT)

Let C = cost of one rebuild, V = value of one answered query, both in the
same units. Per drift interval with k queries: eager net = k*V - C,
refuse-only net = 0. Eager beats refuse-only iff k > C/V. Measuring cost
in rebuilds (C = 1): the break-even is k* = 1/V. The REPORT tabulates k*
for reference answer values V in {0.1, 1, 10} rebuilds and marks which
swept cells fall on each side. The measured, assumption-free quantities
are the cost curve (eager rebuilds per answered query = 1/k across the
swept k range) and the eager-vs-lazy waste ratio W = D/min(D,Q) =
max(1, 1/k) per cell. The V values are an explicit policy assumption, not
a measurement; the REPORT states this.

## Frozen kill bars

- K1: This prereg (plus NAMECHECK) is committed strictly before any
  implementation file (ds_spec.zag, ds_main.zag, ds_build.sh, outputs).
  Verified by git log order: the prereg commit's hash precedes the
  implementation commit.
- K2: safebin PATH mandatory; `which python3` and `which python` return
  nothing; pinned znc znc_linux_x86_64_abed8aa1 builds the binary.
- K3: znc builds clean; binary exits 0 on all 3 runs; stderr empty on all 3.
- K4 (refuse-only arm sanity): every P=refuse line has rebuilds=0,
  answered=0, refusals=Q, kb=0. Fails if the refuse arm ever rebuilds,
  answers, or scans.
- K5 (eager correctness at all rates): every P=eager line has answered=Q
  and refusals=0. Fails if recovery misses at any drift rate or the eager
  restamp ever lags a query.
- K6 (lazy correctness + single-refusal mechanism): every P=lazy line has
  answered=Q and refusals=rebuilds. Fails if on-demand recovery misses, or
  if the retry restamp breaks (a second refusal would make
  refusals > rebuilds).
- K7 (lazy never exceeds eager): for every (M,N) cell,
  rebuilds(lazy) <= rebuilds(eager). Fails if on-demand recovery ever
  rebuilds more than eager.
- K8 (unit-economics crossover bracketed): the (M=1,N=16) P=eager line has
  rebuilds > answered (256 rebuilds for 16 answers, k=1/16: more than one
  rebuild per answer); the (M=16,N=1) P=eager line has rebuilds < answered
  (16 rebuilds for 256 answers, k=16). Fails if the sweep does not span
  both sides of k=1.
- K9 (eager-vs-lazy waste crossover): the (M=1,N=16) cell has
  rebuilds(eager) >= 2 * rebuilds(lazy) (predicted 256 vs 16: high-churn
  waste demonstrated); the (M=16,N=1) cell has rebuilds(eager) ==
  rebuilds(lazy) (predicted 16 vs 16: no waste at saturation). Fails if
  the waste regime or the saturated regime is missing.
- K10 (schedule fidelity): every P=eager line has rebuilds == D (exactly
  one eager rebuild per executed drift); exactly 75 CELL lines are
  emitted (25 cells x 3 arms).
- K11: ASCII-only lane sources; no world literals (901/902) in ds_spec.zag
  / ds_main.zag (relation ids arrive only via the rb_* accessors);
  exactly one fn main in ds_full.zag; da_learn.zag byte-unmodified
  (verified: no changes outside this lane directory in git status).

Verdict rule: BUILD-PASS requires 11/11. Any single bar failure is
BUILD-FAIL with the failing bar named.
