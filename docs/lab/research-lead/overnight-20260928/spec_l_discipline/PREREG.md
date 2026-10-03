# SPEC-L-DISCIPLINE: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_l_discipline/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-FLIP-THRESHOLD (BUILD-PASS K1-K10, 2026-10-03) answered the
threshold-redesign question: the flip threshold should NOT scale with
L. fix2 (`2*qhi < dlo`) dominates the L-scaled bar on the harm cell
(J 102 < 142 at L = 7, J 132 < 133 = J_eager at L = 10 with the rescue
timing L-independent at tf1 = 144). Its recommendation 4, the frozen
next question this lane takes: "The next question is whether L should
enter at all. The fixed bar still takes L as an argument (for J
accounting and the unchanged eager direction). A follow-up could test
whether the eager-decisive direction or the cost model needs the
caller-stated L, or whether the whole discipline can run L-free."

## Where L enters after fix2 (frozen mechanism analysis)

1. Flip lazy bar: NO. fix2's `2*qhi < dlo` has no L.
2. Flip eager direction: YES. `nr_decide_ft` keeps the eager-decisive
   test identical to `nr_decide` in every arm: `if(L*phid>phin){ eg=1; }`.
3. Pre-shift commit rule: YES. `nr_decide` uses L in both directions
   (`L*phid>phin`, `L*plod<plon`). OUT OF SCOPE for the variants
   (quirk territory; the commit rule stays frozen). Its L-dependence is
   observably load-bearing on R = 120 in the frozen parent data
   (commit outcome differs by L: cm = 0 / tc = 128 at L = 1/3 vs
   cm = 2 / tc = 112 at L = 7/10): a bound on the "L is purely
   cost-accounting" claim, reported as a finding, not a variant.
4. J accounting: YES. J = rb + rf*L per line (frozen, unchanged).

Observability note (frozen): in the flip branch the eager direction is
observable only when lazy-selected (cur == 0) and dec == 2 fires. In
the parent's frozen 84 episodes no eager-direction flip ever occurs
(every recorded flip has fdir = -1; tf2 = 0 everywhere). On R = 60 the
eager direction may fire unobservably while eager-committed
pre-rescue, but post-rescue (cur == 0) it never fires at any
L in {1,3,7,10}.

## The L-discipline question (frozen)

Four conditions on the fix2 base, implemented as three new policy arms
plus the fix2 replication control. L is caller-stated, not measured
(inherited).

- **pol 7 "fix2" (neither):** unchanged. L stays in the flip-path
  eager direction and in J accounting. Replication control.
- **pol 10 "noeg" (eager-direction L-free):** the flip-path
  eager-decisive test becomes `phid > phin` (equivalently the direction
  evaluated at L = 1); the lazy bar stays `2*qhi < dlo`; the commit
  rule is unchanged; J uses the caller L. Tests: is L load-bearing in
  the flip-path eager direction?
- **pol 11 "noj" (J L-free):** dynamics byte-identical to fix2 BY
  CONSTRUCTION (pure alias: same code path, differs only in the P=
  name); scored post-hoc with J' = rb + rf, i.e. J with the
  caller-stated L replaced by the identity multiplier 1. Tests: does
  L-free scoring change the fix2-vs-adapt-vs-eager conclusions?
- **pol 12 "nol" (both L-free):** dynamics byte-identical to noeg BY
  CONSTRUCTION (pure alias); scored with J'. Tests: the full L-free
  flip discipline.

The commit rule (`nr_decide`, com == 0 branch) is UNCHANGED in all
arms, so quirk fields must replicate identically (K5b) and any tf1
spread between noeg and fix2 would be an eager-direction property by
construction.

## Questions (frozen)

1. Does removing L from the flip-path eager direction change behavior?
   (K6/K8: noeg vs fix2 line identity modulo P=.)
2. Does removing L from J accounting change the conclusions?
   (K7: alias correctness as bars; J' rankings as findings.)
3. Can the whole flip discipline run L-free? (Synthesis: if noeg is
   identical to fix2, both flip directions are observably L-free and L
   survives only in J accounting, where it belongs by definition as
   the caller-stated cost ratio, plus the untouched commit rule.)

## Design (frozen)

**Regime cells (frozen, inherited).** T = 256, shift at t = 128,
mechanics identical to the parent. Four cells: CS0 R = 21
(16,16)->(16,16) sparse stationary; CS1 R = 60 (16,16)->(1,16)
sparse -> drift-dense, THE HARM CELL; CS2 R = 82 (16,16)->(16,1)
sparse -> query-dense; CS3 R = 120 (16,16)->(1,16) D32 = 1 control.
No new probe.

**Arms (frozen).** 22 per cell, 88 episodes total: pol 0 fixed lazy,
pol 1 fixed eager (parent dynamics unchanged), pol 2 adapt L in
{1,3,7,10} (L-scaled control; replication), pol 7 fix2 L in {1,3,7,10}
(replication control), pol 10 noeg L in {1,3,7,10}, pol 11 noj L in
{1,3,7,10}, pol 12 nol L in {1,3,7,10}.

**Implementation (frozen, copy-plus-delta).** ld_spec.zag is a minimal
documented delta on the parent's ft_spec.zag ([LD-DELTA] markers,
[LD-RENAME] ft_ -> ld_): nr_decide_ft gains the hoisted egl flag
(eager-direction L multiplier: egl = 1 for pol 10/12, else egl = L;
`if(egl*phid>phin){ eg=1; }`) and lzmult = 1 for pol 10/11/12 (the
fix2 lazy bar for all three new arms); pol 8/9 branches kept dormant
(not swept); nr_polname gains noeg/noj/nol; ld_episode wires pol
10/11/12 through the adapt initialization, EWMA updates, and
checkpoint call. nr_decide (commit rule), the EWMA, the grid, the
arrival mechanics are the parent's, unchanged. The parent's
ft_spec.zag is byte-unmodified in its own lane (K9). The 9 grandparent
sources are reused byte-unmodified. da_learn.zag untouched.

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.
J' = rb + rf scored post-hoc for pols 7/10/11/12 (dynamics-identical
pairs: 7/11 and 10/12).

## Frozen predictions (not bars; recorded before running)

- K5a replication: 32 lines (adapt {1,3,7,10} + fix2 {1,3,7,10} x 4
  cells) byte-identical to the parent's frozen ft_run1.txt (sha256
  99d52d2b3aac843ad8ddc2225c742c95bf6cc977d9ee6570af8970defaf957a8).
- K5d L = 1 identity: noeg L = 1 line equals fix2 L = 1 modulo P=, and
  nol L = 1 equals noj L = 1 modulo P=, on all four cells (egl = 1 = L
  at L = 1, so the eager direction is identical by construction).
- K6: noeg lines equal fix2 lines modulo P= on R = 60 at every L: the
  flip-path eager direction never fires observably (no fdir = 1 flip
  and no tf2 > 0 in the parent's 84 episodes; post-rescue the stricter
  bar fires even less).
- J' findings calibrated from the frozen parent data (J' = rebuilds +
  refusals): on R = 60, fix2 has od = 10, rs = 22, rebuilds = 32 at
  every L, so J'_fix2 = 42 at every L; adapt L = 7 has od = 3,
  rs = 118, rebuilds = 121, so J'_adapt(7) = 124; eager has
  rebuilds = 133, refusals = 0, so J'_eager = 133. Predicted:
  J'_fix2(7) = 42 < 124 = J'_adapt(7) and J'_fix2(10) = 42 < 133 =
  J'_eager: the fix2 advantage survives L-free scoring.
- Control cells: noeg/noj/nol show zero flips on R = 21/82 (finding;
  inherits fix2's clean controls).

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation commit
  (verified git log order on this lane directory). No implementation
  file (ld_spec.zag, ld_main.zag, ld_build.sh, ld_posthoc.sh,
  ld_full.zag, ld_bin, ld_run*.txt/err) may exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python` return
  nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified in-script).
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  ld_bin exits 0 on all 3 runs; stderr empty on all 3 runs; stdout 3/3
  byte-identical (cmp + sha256). Exactly 88 CELL lines per run
  (4 cells x 22 arms).
- **K4 (anchoring).** (a) Per cell R in {21,60,82,120}: all 22 arms see
  identical (D, Q); lazy lines: answered = Q, kb = 2Q, refusals =
  rebuilds, rebuilds <= min(D, Q); eager lines: rebuilds = D,
  answered = Q, refusals = 0, kb = 2Q. (b) Arrival splits show the shift
  (lazy arm): R = 60 and R = 120: Dpost = 128 exactly, Qpost < 32,
  Dpre < 32, Qpre < 32; R = 82: Qpost = 128 exactly, Dpost < 32,
  Dpre < 32, Qpre < 32; R = 21: D < 48, Q < 48. (c) Structural
  accounting on all 80 adaptive lines (per cell: 4 adapt + 4 fix2 +
  4 noeg + 4 noj + 4 nol): D = Dpre + Dpost, Q = Qpre + Qpost,
  answered = Q, kb = 2Q, rebuilds = od + rs, refusals = od;
  (pflips = 0) iff (tf1 = 0) iff (fdir = 0); pflips > 0 implies
  128 < tf1 <= 256; flips >= pflips; lines with flips = 0 and cm in
  {0,1}: od/rf/rs field-equal to the lazy twin; lines with flips = 0
  and cm = 2: rs = 1 + (D - Dc) and od <= min(Dc, Qc); lc = 0
  everywhere (pol 3 dormant in this lane).
- **K5 (replication / quirk / monotonicity / identity).** (a) Exact
  replication: on all four cells, adapt L in {1,3,7,10} and fix2 L in
  {1,3,7,10} CELL lines are byte-identical to the parent's frozen
  ft_run1.txt (32 lines). (b) Quirk fires identically in the new arms:
  on R in {21,60,82}, pol in {noeg,noj,nol} at L in {1,3,7,10}:
  tc = 32, cm = 2, Dc = 0. (c) Monotone latency (theorem): on R = 60,
  for each arm pol in {adapt,fix2,noeg,noj,nol} and each consecutive
  pair (La,Lb) in its L sweep with La < Lb: flips(Lb) >= 1 implies
  flips(La) >= 1 and tf1(La) <= tf1(Lb). (d) L = 1 identity: on all four
  cells, the noeg L = 1 CELL line equals the fix2 L = 1 CELL line
  modulo the P= field, and the nol L = 1 line equals the noj L = 1
  line modulo the P= field.
- **K6 (eager-direction question, harm cell).** On R = 60, L in
  {1,3,7,10}: the noeg CELL line equals the fix2 CELL line modulo the
  P= field. Prediction: removing L from the flip-path eager direction
  changes nothing observable: L is not load-bearing there.
- **K7 (J-accounting question).** (a) Alias correctness: on all four
  cells, L in {1,3,7,10}: the noj line equals the fix2 line modulo P=,
  and the nol line equals the noeg line modulo P= (scoring must not
  touch dynamics). (b) Findings (reported, not barred): J' = rb + rf
  for pols 7/10/11/12 vs J for adapt/eager on R = 60 (J'_fix2(7) vs
  J'_adapt(7), J'_fix2(10) vs J'_eager); J/J' tables on all cells.
- **K8 (both L-free / control integrity).** On R in {21,82,120}, L in
  {1,3,7,10}: the noeg CELL line equals the fix2 CELL line modulo the
  P= field (no spurious divergence where the discipline is quiet).
  Findings (reported, not barred): flips and J of the new arms on the
  control cells; the commit-side L-dependence on R = 120 (cm = 0 at
  L = 1/3 vs cm = 2 at L = 7/10) as the bound on the L-free claim.
- **K9 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in ld_spec.zag, ld_main.zag; exactly one `fn main`
  in ld_full.zag; reused sources byte-unmodified (`git diff --quiet` on
  da_base.zag, da_module.zag, da_learn.zag, rb_world.zag, rb_fix.zag,
  et_world.zag, et_spec.zag, rr_spec.zag, ld_spec.zag); da_learn.zag in
  particular NOT modified (separate lane only); the parent lane's
  ft_spec.zag / ft_main.zag superseded by copy-plus-delta (ld_spec.zag
  carries [LD-DELTA]/[LD-RENAME] markers), never edited; commits local
  with explicit pathspecs, never pushed.

## What would falsify the lane

- K5a fails (replication lines differ): the copy-plus-delta changed
  inherited dynamics (or a znc name-dependent miscompile); the delta is
  not surgical. BUILD-FAIL, fix the delta, do not weaken the bar.
- K6 fails with quirk/commit fields differing between noeg and fix2:
  the egl delta leaked into the commit path. BUILD-FAIL, fix the
  delta.
- K6 fails with tf1/fdir/flips differing (fdir = 1 or tf2 > 0 in
  noeg): L IS load-bearing in the flip-path eager direction somewhere
  on the harm cell. The lane's headline hypothesis dies; report the
  cell/L/tick where the eager direction fires as the answer to
  question 1 (positive), do not weaken the bar.
- K8 fails on a control cell: same diagnosis; a divergence where the
  discipline is quiet is the more surprising result and must be
  reported as such.
- K7a fails (noj != fix2 or nol != noeg beyond P=): the "pure alias"
  construction is broken; scoring touched dynamics. BUILD-FAIL, fix
  the delta.
- J' findings overturn the ranking (J'_fix2(7) >= J'_adapt(7)): the
  fix2 advantage is partly a scoring artifact of L-weighting refusals.
  Report as the answer to question 2 (negative); not a build failure.
- Any K4 failure: arrival anchoring broken; the cells are not the
  parent's cells.

## Non-goals (frozen)

- No change to the commit rule, the EWMA estimator, the checkpoint
  grid, or the arrival mechanics.
- No guard / pol-3 / pol-5 / pol-6 / pol-8 / pol-9 sweeps (dormant code
  kept, not swept).
- No new instrumentation fields: the CELL line format is frozen so the
  K5a replication is byte-exact.
- No verdict on which threshold is "best overall" beyond this lane's
  L-discipline question: one seed per cell, one shift per episode
  (inherited limits).
