# SPEC-ADAPTIVE-SWITCH: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_adaptive_switch/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-LAZY-DEFAULT (BUILD-PASS 11/11) measured the eager tax exactly:
per-avoided-refusal price = W(k) - 1 rebuilds, where W(k) = max(1, 1/k)
and k = Q/D (queries per drift). Its recommendation: "if a future lane
measures wall-clock C and deadline value L in common units, the rule
L > (W(k)-1)*C becomes an executable adaptive policy switch." This lane
is that future lane.

## Design (frozen)

**Common unit.** One abstract work unit = one rebuild, so C = 1 by
definition of the unit. L (deadline value of avoiding one
refused-then-retried query) is stated by the caller in work units
(rebuilds). A separate calibration program (as_calib.zag) genuinely
measures wall-clock nanoseconds per `et_specialize_ret` via
clock_gettime (raw syscall 228, CLOCK_MONOTONIC); its output anchors
the work unit physically but is nondeterministic by nature, so it is
recorded to as_calib.txt and EXCLUDED from the byte-identical bars.
The executable switch itself runs on work units and is fully
deterministic.

**Adaptive arm (pol=2).** Each episode: T = 256 ticks, warmup W = 16
ticks (the least common multiple of the grid periods, so the observed
rate ratio is exact). Phase 1 [0, W) runs the lazy on-demand path and
observes Dw drifts and Qw queries (Dw = 16/M, Qw = 16/N on the grid).
At t = W the switch computes the measured per-avoided-refusal price
pnum/pden = max(0, Dw - Qw)/Qw rebuilds (this IS W(k) - 1 from observed
rates, as an exact rational, no floating point) and selects

    eager  iff  L * pden > pnum * C        (C = 1)

i.e. iff (Dw <= Qw and L > 0) or (Dw > Qw and L*Qw > Dw - Qw).
Phase 2 [W, T) runs the selected policy; eager means restamp-on-drift
exactly as the parent's justified-eager arm. No sync restamp is needed:
t = W is a multiple of every grid M, so a drift fires at t = W and the
eager restamp freshens the epoch before the t = W query.

**Fixed arms** (pol=0 lazy, pol=1 eager) run the parent's exact dynamics
for anchoring; they carry L = -1 (n/a), Dw = Qw = 0, pnum = 0, pden = 1.

**Grid.** M, N in {1, 2, 4, 8, 16} (25 cells) x (lazy + eager +
adapt x L in {0, 1, 3, 7}) = 150 episodes, one CELL line each:

    CELL M=<M> N=<N> P=<adapt|lazy|eager> L=<L> C=1 Dw=<Dw> Qw=<Qw>
         pnum=<pnum> pden=<pden> sel=<sel> D=<D> Q=<Q>
         rebuilds=<rb> answered=<an> refusals=<rf> kb=<kb>

**Cost model (frozen).** J = rebuilds * C + refusals * L, C = 1, so
J = rb + rf * L per line. The adaptive switch is worth having iff it
beats the fixed policies on total J.

## Frozen selection table (K5)

sel per (M, N) cell, rows M = 1, 2, 4, 8, 16 outer, N = 1, 2, 4, 8, 16
inner. E = eager (sel = 1), L = lazy (sel = 0). Derived from the rule
above with Dw = 16/M, Qw = 16/N:

- L=0: all 25 lazy. String: `LLLLLLLLLLLLLLLLLLLLLLLLL`
- L=1: `ELLLLEELLEEELLEEEELEEEEE`
  (eager iff k > 1/2; boundary k = 1/2 cells stay lazy)
- L=3: `EELLEEELLEEELEEEEEEEEEE`
  (eager iff k > 1/4; boundary k = 1/4 cells stay lazy)
- L=7: `EEELLEEELEEEEEEEEEEEEEEE`
  (eager iff k > 1/8; boundary k = 1/8 cells stay lazy)

In closed form the switch fires at k* = 1 / (L/C + 1): L = 1 -> k* = 1/2,
L = 3 -> k* = 1/4, L = 7 -> k* = 1/8, with strict > (equality stays
lazy). The 9 strict-boundary cells (L == price exactly, must be lazy):
(1,2),(2,4),(4,8),(8,16) at L=1; (1,4),(2,8),(4,16) at L=3;
(1,8),(2,16) at L=7.

## Frozen portfolio totals (K7)

Per-L totals of J = rb + rf*L over the 25 cells (mechanical consequence
of the selection table plus the structural accounting in K6;
hand-verified twice):

| L | adapt total | fixed-lazy total | fixed-eager total |
|---|-------------|------------------|-------------------|
| 0 | 1328        | 1328             | 2480              |
| 1 | 1801        | 2656             | 2480              |
| 3 | 2297        | 5312             | 2480              |
| 7 | 2869        | 10624            | 2480              |

Predicted verdicts: adaptive beats fixed lazy at every L > 0 (and ties
it exactly at L = 0, where the switch correctly never fires); adaptive
beats fixed eager at L = 1 and L = 3; at L = 7 adaptive is NOT expected
to beat fixed eager (2869 > 2480: eager is the right policy on 22/25
cells there, and adaptive pays the warmup observation cost) -- this is
a measured finding, not a bar.

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation commit
  (verified git log order on this lane directory). No implementation
  file may exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python` return
  nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- **K3.** znc builds both assemblies clean (no `: error`, exit 0),
  as_bin exits 0 on all 3 runs, stderr empty on all 3 runs, stdout
  3/3 byte-identical (cmp + sha256). Exactly 150 CELL lines per run.
- **K4 (parent anchoring).** All 25 lazy lines: rebuilds = min(D, Q),
  answered = Q, refusals = rebuilds, kb = 2Q. All 25 eager lines:
  rebuilds = D, answered = Q, refusals = 0, kb = 2Q. (Reproduces
  SPEC-LAZY-DEFAULT's measured economics exactly; the adaptive layer
  changes nothing about the fixed arms.)
- **K5 (the switch).** All 100 adapt lines: sel equals the frozen
  selection-table entry for (M, N, L); equivalently sel = 1 iff
  (Dw <= Qw and L > 0) or (Dw > Qw and L*Qw > Dw - Qw) computed from
  the line's own Dw, Qw, L fields. In particular all 9
  strict-boundary cells have sel = 0, and all 25 L = 0 cells have
  sel = 0.
- **K6 (structural accounting).** All 100 adapt lines: answered = Q,
  kb = 2Q. sel = 0 implies rebuilds/answered/refusals field-equal to
  the lazy line of the same (M, N) cell. sel = 1 implies
  rebuilds = min(Dw, Qw) + (D - Dw) and refusals = min(Dw, Qw)
  (warmup ran lazy: min(Dw,Qw) rebuilds/refusals; post-switch eager:
  one restamp per drift, zero refusals).
- **K7 (portfolio).** Per-L totals of J = rb + rf*L equal the frozen
  table exactly: L=0: adapt 1328 = lazy 1328; L=1: adapt 1801 <
  lazy 2656 and < eager 2480; L=3: adapt 2297 < lazy 5312 and <
  eager 2480; L=7: adapt 2869 < lazy 10624. (L=7 vs eager 2480 is
  reported as a finding, not barred.)
- **K8 (calibration).** as_calib.zag builds and runs; as_calib.txt
  contains a `CALIB rebuild_ns_min=<positive integer> iters=200`
  line: a genuine wall-clock measurement of one rebuild, anchoring
  the work unit. Excluded from K3 (timing is nondeterministic).
- **K9 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in as_spec.zag, as_main.zag, as_calib.zag;
  exactly one `fn main` per assembled binary; reused sources
  byte-unmodified (`git diff --quiet` on da_base.zag, da_module.zag,
  da_learn.zag, rb_world.zag, rb_fix.zag, et_world.zag, et_spec.zag,
  rr_spec.zag, and ../spec_lazy_default/ld_spec.zag); da_learn.zag in
  particular NOT modified; commits local with explicit pathspecs,
  never pushed.

## What would falsify the lane

- The switch selecting eager where the rule says lazy (or vice versa)
  on any of the 100 adapt cells (K5).
- Adaptive totals not beating fixed lazy at any L > 0 (K7): the switch
  would be pure overhead.
- Any adapt-lazy line differing from its fixed-lazy twin (K6): the
  warmup would not be honest lazy.
- A zero or missing wall-clock measurement (K8): C would have no
  physical anchor.
