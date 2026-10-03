# SPEC-LAZY-DEFAULT: PREREG (frozen)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_lazy_default/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Parent result:** SPEC-DRIFTRATE-SWEEP BUILD-PASS (11/11), 2026-10-03.
**Task:** adopt SPEC-DRIFTRATE-SWEEP recommendation #1: make lazy on-demand
recovery the DEFAULT recovery policy; eager rebuild-on-drift requires an
explicit latency justification priced against the measured W(k).

## Question

SPEC-DRIFTRATE-SWEEP measured eager vs lazy across the drift/query grid and
found lazy weakly dominates eager on rebuild cost (identical answers, never
more rebuilds, exactly fewer when k < 1), with eager's only advantage being
refusals = 0 (no query ever waits). This lane turns that finding into the
standing policy: the default recovery path is lazy on-demand; eager is
reachable only through an explicit-justification entry point. It measures
the default's rebuild savings against eager (expected to reproduce the
1/k waste curve) and prices the explicit latency justification eager
requires.

## Hypotheses

H1 (default correctness): the default (lazy) policy answers every query at
every drift rate: answered = Q and refusals = rebuilds on all 25 default
lines (single-refusal-then-restamp, no double refusals).

H2 (default rebuild curve): the default's rebuilds equal min(D, Q) exactly
on this grid: the lazy curve is now the default curve, reproducing the
parent lane's LAZY arm line for line.

H3 (justified eager unchanged): eager invoked WITH an explicit latency
justification answers every query with refusals = 0 and rebuilds = D,
reproducing the parent lane's EAGER arm line for line.

H4 (unjustified eager is unreachable): an eager request with just = 0 is
refused by the policy layer and falls back to the default path (fb = 1,
numbers identical to the default line of the same cell). Lazy is the
effective default in code, not merely in comparison.

H5 (waste curve reproduced): the eager/default waste ratio W equals
max(1, 1/k): 16 at (M = 1, N = 16), 1 at (M = 16, N = 1).

H6 (eager tax priced): the eager rebuild tax D - min(D, Q) is exact in
every cell; the per-avoided-refusal price is W(k) - 1 rebuilds: 15 wasted
rebuilds per useful one at k = 1/16, 0 at k >= 1. This is the price the
explicit latency justification must beat.

## Frozen design

One binary, 75 episodes. Assembly: `ld_full.zag` = da_base + rb_world +
et_world + da_module + da_learn + rb_fix + et_spec + rr_spec + ld_spec +
ld_main, all reused sources byte-unmodified; only ld_spec.zag (policy
layer) and ld_main.zag (harness) are new. Repro: `./ld_build.sh`.

Each episode is T = 256 ticks on a fresh world (world_new + rb_setup +
explicit epoch reset to 0 at offset 772, which rb_setup predates;
ret_log_rel for the query relation; et_specialize_ret stamping epoch 0).
The query family is RET only (rel via rb_rel_a(), obj via rb_obj_a1()).
Drift schedule: a drift every M ticks (tick 0 included; drift runs before
the query at coincident ticks). Query schedule: one query every N ticks.
M, N in {1, 2, 4, 8, 16} (countdown counters, no modulo operator). 25
cells. Per cell, three policy arms:

- DEFAULT (pol 0): the standing default. No justification needed or
  accepted. Queries go through the byte-unmodified rr_ret_spec wrapper:
  lazy on-demand recovery only.
- EAGER (pol 1): eager rebuild-on-drift, invoked through the explicit
  justification entry with just = 1 recorded ("zero-refusal deadline
  required"). After every drift, et_specialize_ret immediately; queries
  go through rr_ret_spec (the restamp always precedes the next query).
- EAGER0 (pol 2): eager requested with just = 0 (no justification). The
  policy layer refuses the eager request, flags fb = 1, and routes the
  query through the default path. No eager restamp ever fires on this arm.

Drift type: et_drift_unrelated only, applied repeatedly (content-idempotent
epoch bump, as in the parent lane), isolating the rate economics from
answer-change confounds; gen is constant, every answered query has
identical value, agree = 1 is unambiguous.

Per-episode counters (reset per episode): D (drifts executed), Q (queries
issued), rebuilds (re-specialize events), answered (queries with agree = 1
against ret_gen), refusals (refusal-counter deltas), kb (kb-counter deltas
on the learner path only), just (justification token recorded), fb
(fallback flag: 1 iff the policy layer refused an unjustified eager
request).

Emitted line per episode:
CELL M=<m> N=<n> P=<default|eager|eager0> just=<j> fb=<f> D=<d> Q=<q>
rebuilds=<r> answered=<a> refusals=<f> kb=<k>

## Frozen expected values

D = 256/M, Q = 256/N, k = Q/D = M/N. Predictions (eager0 = default numbers
with fb = 1):

| M | D | N | Q | k | DEFAULT rebuilds | EAGER rebuilds |
|---|---|---|---|---|------------------|----------------|
| 1 | 256 | 1 | 256 | 1 | 256 | 256 |
| 1 | 256 | 2 | 128 | 1/2 | 128 | 256 |
| 1 | 256 | 4 | 64 | 1/4 | 64 | 256 |
| 1 | 256 | 8 | 32 | 1/8 | 32 | 256 |
| 1 | 256 | 16 | 16 | 1/16 | 16 | 256 |
| 2 | 128 | 1 | 256 | 2 | 128 | 128 |
| 2 | 128 | 2 | 128 | 1 | 128 | 128 |
| 2 | 128 | 4 | 64 | 1/2 | 64 | 128 |
| 2 | 128 | 8 | 32 | 1/4 | 32 | 128 |
| 2 | 128 | 16 | 16 | 1/8 | 16 | 128 |
| 4 | 64 | 1 | 256 | 4 | 64 | 64 |
| 4 | 64 | 2 | 128 | 2 | 64 | 64 |
| 4 | 64 | 4 | 64 | 1 | 64 | 64 |
| 4 | 64 | 8 | 32 | 1/2 | 32 | 64 |
| 4 | 64 | 16 | 16 | 1/4 | 16 | 64 |
| 8 | 32 | 1 | 256 | 8 | 32 | 32 |
| 8 | 32 | 2 | 128 | 4 | 32 | 32 |
| 8 | 32 | 4 | 64 | 2 | 32 | 32 |
| 8 | 32 | 8 | 32 | 1 | 32 | 32 |
| 8 | 32 | 16 | 16 | 1/2 | 16 | 32 |
| 16 | 16 | 1 | 256 | 16 | 16 | 16 |
| 16 | 16 | 2 | 128 | 8 | 16 | 16 |
| 16 | 16 | 4 | 64 | 4 | 16 | 16 |
| 16 | 16 | 8 | 32 | 2 | 16 | 16 |
| 16 | 16 | 16 | 16 | 1 | 16 | 16 |

DEFAULT rebuilds = min(D, Q); EAGER rebuilds = D. Answered: Q on every
default/eager/eager0 line. Refusals: equal to rebuilds on every default
and eager0 line; 0 on every eager line. kb = 2Q on every line (2 slots per
hit query, as measured in the parent lane). just = 1 on every eager line,
0 elsewhere. fb = 1 on every eager0 line, 0 elsewhere.

## Latency-justification pricing (frozen method, numbers filled in REPORT)

The default policy pays refusals = rebuilds: each on-demand rebuild is
bought by exactly one refused-then-retried query (the latency tax of
lazy). Eager with justification pays refusals = 0 at an extra rebuild
cost of tax = D - min(D, Q) per cell. The price per avoided refusal is
tax / min(D, Q) = W(k) - 1 rebuilds (0 at k >= 1). Frozen decision rule:
eager is justified iff the deadline value L of avoiding one
refused-then-retried query exceeds (W(k) - 1) * C, where C is one rebuild
cost. The justification token records the assumed L regime; the REPORT
tabulates measured W(k) - 1 across the swept k values so any claimed L
can be checked against the measured price. At k = 1/16 the measured price
is 15 rebuilds per avoided refusal: a zero-refusal deadline must be worth
more than 15 rebuilds per useful answer to justify eager there.

## Frozen kill bars

- K1: This prereg (plus NAMECHECK) is committed strictly before any
  implementation file (ld_spec.zag, ld_main.zag, ld_build.sh, outputs).
  Verified by git log order: the prereg commit's hash precedes the
  implementation commit.
- K2: safebin PATH mandatory; `which python3` and `which python` return
  nothing; pinned znc znc_linux_x86_64_abed8aa1 builds the binary.
- K3: znc builds clean; binary exits 0 on all 3 runs; stderr empty on all 3.
- K4 (default correctness): every P=default line has answered = Q,
  refusals = rebuilds, kb = 2Q. Fails if the default policy ever misses a
  query, double-refuses, or scans a different number of slots.
- K5 (justified-eager correctness): every P=eager line has answered = Q,
  refusals = 0, just = 1, kb = 2Q. Fails if justified eager ever misses or
  lets a query wait.
- K6 (default is the lazy curve): every P=default line has
  rebuilds = min(D, Q) computed from that line's own D and Q. Fails if the
  default ever rebuilds for a drift no query sees.
- K7 (unjustified eager falls back): every P=eager0 line has fb = 1 and
  just = 0, and its rebuilds/answered/refusals are identical to the
  P=default line of the same (M, N) cell. Fails if eager fires without a
  recorded justification.
- K8 (waste curve = max(1, 1/k)): the (M = 1, N = 16) cell has
  rebuilds(eager) = 16 * rebuilds(default) (predicted 256 = 16 * 16); the
  (M = 16, N = 1) cell has rebuilds(eager) = rebuilds(default) (predicted
  16 = 16). Fails if the 1/k curve does not reproduce.
- K9 (eager tax priced): every cell has rebuilds(eager) - rebuilds(default)
  = D - min(D, Q); at (M = 1, N = 16) the tax = 240 = 15 * rebuilds(default).
  Fails if the per-avoided-refusal price W(k) - 1 is not exact.
- K10 (schedule fidelity): exactly 75 CELL lines are emitted (25 cells x 3
  arms); every P=eager line has rebuilds = D (exactly one justified eager
  rebuild per executed drift).
- K11: ASCII-only lane sources; no world literals (901/902) in ld_spec.zag
  / ld_main.zag (relation ids arrive only via the rb_* accessors); exactly
  one fn main in ld_full.zag; da_learn.zag byte-unmodified (verified: no
  changes outside this lane directory in git status).

Verdict rule: BUILD-PASS requires 11/11. Any single bar failure is
BUILD-FAIL with the failing bar named.
