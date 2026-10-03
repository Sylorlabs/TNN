# SPEC-DRIFTRATE-SWEEP: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_driftrate_sweep/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (11/11 frozen kill bars)**

## Summary

Swept drift rate against query rate to quantify the eager-recovery
break-even left as reasoned-but-unmeasured analysis in
SPEC-REFUSAL-RECOVERY. 75 episodes (25 drift/query cells x 3 policies),
one binary, pure Zag, safebin-built, 3/3 byte-identical
(sha256 ccfc1d9902a1fcf2b6061d5b0b370e836f3fe3da83650553c2dcf68493e03c42).

Each episode is 256 ticks: a drift every M ticks, one RET query every N
ticks (M, N in {1,2,4,8,16}), drift before query at coincident ticks.
Three policy arms per cell, all built on the byte-unmodified
SPEC-REFUSAL-RECOVERY wrappers and the et_* epoch machinery:
EAGER (re-specialize immediately after every drift), LAZY (the rr wrapper
rebuilding only when a query actually refuses: on-demand recovery), and
REFUSE (plain epoch-gated spec, never rebuilds). Drift is the repeatable
content-idempotent unrelated drift (epoch bump only), isolating the rate
economics from answer-change confounds; gen is constant, so every
answered query has identical value.

Measured: eager pays exactly D rebuilds per episode at every rate and
answers every query; lazy answers every query while paying only
min(D, Q) rebuilds, never more than eager; refuse-only answers nothing
post-drift at any rate. The sweep brackets the unit-economics crossover:
at k = 1/16 eager pays 256 rebuilds for 16 answers (16 rebuilds per
answer); at k = 16 it pays 16 rebuilds for 256 answers. The eager-vs-lazy
waste ratio is exactly max(1, 1/k): 16x waste at the highest churn, zero
waste at saturation.

## What was tested

Assembly: `ds_full.zag` = da_base + rb_world + et_world + da_module +
da_learn + rb_fix + et_spec + rr_spec + ds_spec + ds_main, all reused
sources byte-unmodified; only ds_spec.zag (policy steps) and ds_main.zag
(harness) are new. Repro: `./ds_build.sh`. Per-episode fresh world
(rb_setup + explicit epoch reset, ret family specialized at epoch 0).

Per-cell results (D = drifts, Q = queries, k = Q/D queries per drift;
E/L = eager/lazy rebuilds; W = eager/lazy waste ratio):

| M | N | D | Q | k | EAGER rb | LAZY rb | W |
|---|---|---|---|---|----------|---------|---|
| 1 | 1 | 256 | 256 | 1 | 256 | 256 | 1 |
| 1 | 2 | 256 | 128 | 1/2 | 256 | 128 | 2 |
| 1 | 4 | 256 | 64 | 1/4 | 256 | 64 | 4 |
| 1 | 8 | 256 | 32 | 1/8 | 256 | 32 | 8 |
| 1 | 16 | 256 | 16 | 1/16 | 256 | 16 | 16 |
| 2 | 1 | 128 | 256 | 2 | 128 | 128 | 1 |
| 2 | 2 | 128 | 128 | 1 | 128 | 128 | 1 |
| 2 | 4 | 128 | 64 | 1/2 | 128 | 64 | 2 |
| 2 | 8 | 128 | 32 | 1/4 | 128 | 32 | 4 |
| 2 | 16 | 128 | 16 | 1/8 | 128 | 16 | 8 |
| 4 | 1 | 64 | 256 | 4 | 64 | 64 | 1 |
| 4 | 2 | 64 | 128 | 2 | 64 | 64 | 1 |
| 4 | 4 | 64 | 64 | 1 | 64 | 64 | 1 |
| 4 | 8 | 64 | 32 | 1/2 | 64 | 32 | 2 |
| 4 | 16 | 64 | 16 | 1/4 | 64 | 16 | 4 |
| 8 | 1 | 32 | 256 | 8 | 32 | 32 | 1 |
| 8 | 2 | 32 | 128 | 4 | 32 | 32 | 1 |
| 8 | 4 | 32 | 64 | 2 | 32 | 32 | 1 |
| 8 | 8 | 32 | 32 | 1 | 32 | 32 | 1 |
| 8 | 16 | 32 | 16 | 1/2 | 32 | 16 | 2 |
| 16 | 1 | 16 | 256 | 16 | 16 | 16 | 1 |
| 16 | 2 | 16 | 128 | 8 | 16 | 16 | 1 |
| 16 | 4 | 16 | 64 | 4 | 16 | 16 | 1 |
| 16 | 8 | 16 | 32 | 2 | 16 | 16 | 1 |
| 16 | 16 | 16 | 16 | 1 | 16 | 16 | 1 |

Uniform across all 25 cells: EAGER answered = Q with refusals = 0;
LAZY answered = Q with refusals = rebuilds; REFUSE answered = 0 with
refusals = Q, rebuilds = 0, kb = 0. Measured per-query scan cost: 2
slots per hit query (eager and lazy kb = 2Q in every cell), 0 slots per
refused query.

Kill-bar adjudication: K1 prereg commit 350ea74b7 strictly precedes the
implementation commit (verified git log order). K2 safebin, no
python3/python, pinned znc znc_linux_x86_64_abed8aa1. K3 builds clean,
exit 0, empty stderr on all 3 runs. K4 all 25 refuse lines:
rebuilds=0, answered=0, refusals=Q, kb=0. K5 all 25 eager lines:
answered=Q, refusals=0. K6 all 25 lazy lines: answered=Q,
refusals=rebuilds. K7 lazy rebuilds <= eager rebuilds in all 25 cells
(strictly less in the 10 cells with M<N). K8 (1,16) eager 256 rebuilds >
16 answered; (16,1) eager 16 rebuilds < 256 answered. K9 (1,16) eager
256 >= 2x lazy 16; (16,1) eager 16 == lazy 16. K10 eager rebuilds == D
on all 25 eager lines; 75 CELL lines emitted. K11 ASCII-only, no world
literals in ds_spec.zag/ds_main.zag, one fn main, reused sources
unmodified (git diff clean). **11/11 PASS.**

## Tested findings

1. **Eager recovery is rate-independent in correctness, rate-blind in
   cost.** answered = Q in all 25 eager cells (H1): recovery works at
   every drift rate, including 256 drifts per episode. But rebuilds = D
   in all 25 cells regardless of Q: eager pays one rebuild per drift even
   when no query ever sees the drifted world.
2. **Lazy on-demand recovery serves the same answers for fewer
   rebuilds.** answered = Q in all 25 lazy cells with rebuilds =
   min(D, Q) exactly as preregistered (H2): one rebuild per drift that a
   query actually follows, zero for the rest. refusals = rebuilds in
   every cell confirms the single-refusal-then-restamp mechanism (no
   double refusals anywhere in 75 episodes).
3. **Refuse-only is a pure-loss baseline at every rate.** answered = 0,
   kb = 0 in all 25 refuse cells (H3): refusal yields no answer and costs
   no scan. This prices what eager's rebuilds buy: Q answers that the
   refuse-only policy cannot serve at all.
4. **The unit-economics crossover is bracketed at k = 1.** Eager pays
   rebuilds/answered = 1/k rebuilds per answered query: 16 rebuilds per
   answer at k = 1/16, 1/16 rebuild per answer at k = 16 (H4). The sweep
   spans both sides of the line where eager starts paying more than one
   rebuild per answer served.
5. **The eager-vs-lazy waste crossover is exact: W = max(1, 1/k).**
   At high churn eager wastes rebuilds on drifts no query ever sees
   (16x at k = 1/16); at saturation (k >= 1 on this grid) eager and lazy
   pay identically, rebuild for rebuild (H5).

## Reasoned analysis: the break-even, quantified

Let C = cost of one rebuild, V = value of one answered query, same
units. Per drift interval with k queries per drift: eager net = kV - C,
refuse-only net = 0. **Eager beats refuse-only iff k > C/V.** Measuring
cost in rebuilds (C = 1), the break-even is **k* = 1/V**:

| Answer value V (rebuilds) | Break-even k* = 1/V | Swept cells justifying eager |
|---|---|---|
| 0.1 (answers nearly worthless) | 10 | only (M=16,N=1), k=16 |
| 1 (an answer worth one rebuild) | 1 | the 15 cells with k >= 1 (M >= N) |
| 10 (answers precious) | 0.1 | 24 of 25 cells; only (M=1,N=16), k=1/16, still does not justify eager |

The V column is an explicit policy assumption, not a measurement; the
measured, assumption-free quantities are the cost curve (1/k rebuilds
per answer) and the waste ratio W(k). The headline the data supports
without any value assumption: **when the world churns faster than
queries arrive (k < 1), eager recovery pays more than one full rebuild
per answer it serves, and the excess is pure waste that lazy on-demand
recovery avoids entirely.**

Eager vs lazy has no value-V crossover on rebuild cost: lazy weakly
dominates eager in every cell (K7) with identical answer service. Eager
can only be justified by latency, not cost: eager is the only arm with
refusals = 0, meaning no query ever waits for a rebuild. The price of
that latency is exactly W(k) - 1 wasted rebuilds per useful one. A
latency-sensitive learner should therefore compare its deadline cost
against (W(k)-1) rebuilds, not against the full D.

Measured work units grounding the cost side: a hit query scans exactly
2 bucket slots (kb = 2Q on every eager/lazy line), a refused query
scans 0 (kb = 0 on every refuse line), and a rebuild is one full
ret-family re-specialize (one world scan by source inspection, counted
as one resp-style event). So in slot-scan terms one rebuild dominates
one query by roughly the world-size-to-bucket-size ratio; the event
counts above are the conservative accounting.

## Bug or design limitation

Design limitation, inherited and now priced. The epoch tag is
per-world, so every drift refuses every family (the conservative
refusal the parent lanes documented); eager recovery therefore rebuilds
for answers that were already correct on unrelated drift. The sweep
shows this is not a corner case but the dominant cost at high churn:
at k = 1/16, 15 of every 16 eager rebuilds serve no query at all. The
per-relation epoch follow-up (SPEC-PERRELATION-EPOCH, BUILD-PASS 12/12)
attacks exactly this: finer refusal granularity shrinks the set of
drifts that force a rebuild. This lane quantifies the prize: at k=1/16
a perfect per-relation epoch would cut eager rebuilds up to 16x.

## Honest scope limits

- One drift type (unrelated, repeatable) and one query family (RET).
  The rate economics are structural (refusal is per-epoch, rebuild is
  per-family), but answer-changing drifts and CNT/VFY families were not
  swept; the parent lane proved recovery correctness there, not the
  rate curve.
- Deterministic periodic schedules, not bursty or stochastic arrivals.
  The crossover k* = C/V is schedule-independent (it depends only on
  queries per drift), but the exact lazy rebuild count min(D,Q) used
  the power-of-2 grid structure; irregular schedules would give a
  messier lazy curve bounded above by the same min(D,Q).
- The value V is a policy input, not measured. The lane measures cost;
  break-even needs a value assumption, stated explicitly.
- Latency is counted in refusals (0 for eager), not wall-clock time.

## Battery cost

None. `da_learn.zag` byte-unmodified (verified via git diff in
ds_build.sh), the DA battery untouched, the SPEC-EPOCHTAG and
SPEC-REFUSAL-RECOVERY sources reused unmodified. All new code lives in
ds_spec.zag / ds_main.zag in this lane.

## Recommendations

1. Adopt lazy on-demand recovery (rebuild on refusal, at query time) as
   the default over eager rebuild-on-drift: identical answers, never
   more rebuilds, exactly fewer whenever k < 1. Eager should require an
   explicit latency justification priced against the measured W(k).
2. The per-relation epoch follow-up is now quantitatively motivated:
   the sweep prices the conservative-refusal waste it would eliminate
   (up to 16x fewer rebuilds at k = 1/16).
3. Any future recovery-policy proposal should be evaluated on the
   (k, W) plane measured here: report rebuilds per answered query
   against 1/k, and waste against max(1, 1/k), before claiming an
   improvement.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3`/`which python`
  empty, recorded in NAMECHECK.md Step 0); pinned znc
  znc_linux_x86_64_abed8aa1; no Python invoked at any point.
- Git via `/usr/bin/git` directly (safebin git symlink breaks writes
  with EPERM per AGENTS.md); explicit pathspecs; commits local, never
  pushed.
- Commit order: 350ea74b7 (frozen prereg K1-K11 + NAMECHECK, alone) ->
  implementation + outputs + this report. One tooling iteration during
  commit (misordered `-m`/`--` args rejected by git; recommitted
  correctly); no implementation iterations needed, all bars passed on
  the first full run.
- No amendments: the frozen bars adjudicated as written.
- Repro: `./ds_build.sh` assembles `ds_full.zag`, builds with the pinned
  znc, runs 3x, checks byte-identity and all kill bars. All sources and
  logs are in this lane directory.
