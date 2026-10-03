# SPEC-FLIP-LATENCY: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_flip_latency/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-COLD-START (BUILD-FAIL on K5, 2026-10-03) confirmed the
cold-start quirk 9/9 (zero-data eager commit at e = 32, tc = 32,
cm = 2, Dc = 0, degenerate {0} price interval) and measured the
flip-rule rescue latency on the harm cell CS1 (R = 60,
(16,16) -> (1,16), sparse -> drift-dense): tf1 = 144/160/240 for
adapt L in {1,3,7}, with J_adapt = 42/74/142. Its recommendation,
quoted verbatim: "Open a flip-latency lane (tf1 grows with L; L=7
rescue was too late)". This lane is that flip-latency lane. It
builds on SPEC-COLD-START without redesigning it: same cost model
J = rb + rf*L, same EWMA estimator, same nr_decide margin test,
same flip rule, same arrival mechanics and seed formulas, same
regime cells (R = 21/60/82/120 inherited; D32 = 0 established by
the parent's frozen data, no new probe needed), same reused
sources byte-unmodified (the 9 grandparent sources; the cold-start
lane's cs_spec.zag is superseded by copy-plus-delta, not edited;
da_learn.zag explicitly untouched). The deltas are: (1) an
extended adapt L sweep {1,3,7,10,15,20,30} to trace the latency
curve past the too-late boundary; (2) two latency-reduction
variant arms, pol 5 "fastchk" (post-shift checkpoint cadence 8
instead of 16) and pol 6 "fastewma" (EWMA weight 7/8 instead of
15/16); (3) no new instrumentation fields (latency is fully
visible in the inherited tf1/flips/fdir/rs/od fields).

## The flip-latency mechanism (frozen analysis)

The flip rule (inherited, com == 1 branch) reuses nr_decide at
each checkpoint: an eager-committed episode flips to lazy iff the
margin test is lazy-decisive, L*plod < plon, where
plon = max0(dlo - qhi) and plod = maxi(qhi, 1). With dlo > qhi
this is (L+1)*qhi < dlo: the rescue fires when the LOWER drift
bound clears L times the UPPER query bound. Three consequences,
all frozen before running:

1. **Latency grows with L by the evidence bar, not the grid.**
   dec == 1 is pointwise monotone-decreasing in L at fixed
   estimator state (larger L makes L*plod < plon strictly
   harder). The EWMA trajectory is L-independent (updates never
   see L) and the checkpoint grid is L-independent, so the first
   post-shift checkpoint with dec == 1 is non-decreasing in L.
   The (L+1) multiplier falls on qhi, the query-side uncertainty:
   eq spikes on every bursty query arrival (devq^2 ~ 891k at
   qh ~ 80), so the rescue is gated by query-gap troughs deep
   enough that (L+1)*qhi < dlo. Larger L needs deeper/longer
   troughs, hence later tf1.

2. **Steady-state feasibility boundary.** Post-shift on R = 60,
   df = 1 every tick (Dpost = 128 over 128 ticks), so dh -> 1024,
   ed -> 0, dlo -> 1024; qh -> 1024*Qpost/128 ~ 80. A
   steady-state lazy-decisive verdict needs (L+1)*80 < 1024,
   i.e. L <= 11. For L >= 12 no steady-state flip is possible;
   flips there can only occur in early transients or deep
   query-gap troughs.

3. **The quirk does not cause the latency.** Guard (pol 4) runs
   the identical per-tick EWMA as adapt (pol 2); the EWMA block
   is pol-independent. Both are eager-committed before the
   post-shift checkpoints (guard commits eager on real data at
   tc <= 96 for L >= 3 by dec == 2 monotonicity in L from the
   parent's tc = 96 at L = 7). Identical EWMA + identical flip
   rule + identical grid => identical flip ticks. The parent's
   frozen data already shows tf1_guard = tf1_adapt = 160/240 at
   L = 3/7; this lane bars the equality at L = 10.

## Questions (frozen)

1. Characterize the latency curve: tf1(L) on the harm cell for
   adapt L in {1,3,7,10,15,20,30}. Is it non-decreasing (the
   monotone-evidence-bar theorem)? Where does the flip stop
   coming at all?
2. Why does latency grow with L? Is it the L-scaled evidence
   requirement ((L+1)*qhi < dlo), the checkpoint grid, or the
   estimator speed? Discriminate via: guard (quirk exonerated if
   tf1_guard == tf1_adapt), fastchk (grid contributes at most one
   8-tick step if tf1_fastchk in {tf1_adapt, tf1_adapt - 8}),
   fastewma (estimator-speed contribution, direction unknown a
   priori: faster mean-tracking vs wider transient intervals).
3. Can latency be reduced? fastchk halves the post-shift
   checkpoint grid (never later than adapt, by the superset-grid
   theorem); fastewma doubles the EWMA speed (effect measured,
   not barred directionally).
4. Is there an L where the flip comes too late to matter?
   L = 7 already lost to fixed eager (142 > 133). Bar the
   extension: J_adapt(10) > J_eager = 133 in every flip scenario
   (theorem: J >= 134). Report J_adapt at L in {15,20,30} and
   whether the flip fires there at all.

## Design (frozen)

**Regime cells (frozen, inherited).** T = 256, shift at t = 128,
mechanics identical to the parent. Four cells: CS0 R = 21
(16,16)->(16,16) sparse stationary; CS1 R = 60 (16,16)->(1,16)
sparse -> drift-dense, THE LATENCY CELL (D32 = 0, quirk fires by
construction); CS2 R = 82 (16,16)->(16,1) sparse -> query-dense;
CS3 R = 120 (16,16)->(1,16) D32 = 1 control. No new probe: the
R values and their D32/Q32 properties are established by the
parent's frozen 3/3-byte-identical data.

**Arms (frozen).** 18 per cell, 72 episodes total: pol 0 fixed
lazy, pol 1 fixed eager (parent dynamics unchanged), pol 2 adapt
with L in {1,3,7,10,15,20,30}, pol 4 guard with L in {3,7,10},
pol 5 "fastchk" with L in {1,7,10}, pol 6 "fastewma" with L in
{1,7,10}.

**New-arm semantics (frozen).** Pol 5 runs the identical
discipline as pol 2 (same EWMA, same nr_decide, same commit
rule including the quirk, same flip rule) with ONE delta: the
checkpoint countdown resets to 8 instead of 16 for intervals
starting at e >= 128, so post-shift checkpoints fall at
136,144,152,...,256 (a superset of adapt's 144,160,...,256).
Pre-shift checkpoints are unchanged (32,48,...,128), so the
quirk fires at e = 32 identically. Pol 6 runs the identical
discipline as pol 2 with ONE delta: the EWMA uses weight 7/8
instead of 15/16 (dh = (7*dh+1024*df)/8,
ed = (7*ed+devd*devd)/8, and likewise qh, eq). The quirk still
fires at e = 32: with D32 = 0, df = 0 for 32 ticks keeps
(dh,ed) = (0,0) under any (k*dh+1024*df)/(k+1) update, so
dec == 2 for every L >= 1 exactly as in adapt. Neither variant
touches the flip rule, the commit rule, or pol-3 code (dormant).

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.

## Frozen predictions (not bars; recorded before running)

- Exact replication: adapt L in {1,3,7} and guard L in {3,7}
  CELL lines are byte-identical to the parent's frozen
  cs_run1.txt on all four cells (the delta is rename-only on
  those paths; this also guards against znc name-dependent
  miscompiles).
- tf1_adapt = 144/160/240 at L = 1/3/7 (replication); tf1(10)
  in {240, 256} or never (monotone from 240; only checkpoints
  240/256 remain).
- tf1_guard(L) == tf1_adapt(L), flips and fdir equal, for
  L in {3,7,10} on R = 60 (theorem).
- tf1_fastchk(L) <= tf1_adapt(L) for L in {1,7,10} (theorem);
  expected in {tf1_adapt, tf1_adapt - 8} absent trough flicker
  (finding).
- tf1_fastewma direction unknown (finding): faster dh rise vs
  wider transient eq spikes; flips >= 1 certain only at L = 1
  (2*qhi < dlo needs qhi < ~512; eq <= max devq^2 = 1024^2
  gives qhi <= ~448 at convergence).
- J_adapt(10) > 133 (theorem: every flip scenario gives
  J >= 134); J_adapt(7) = 142 (replication).
- L in {15,20,30}: steady-state flip infeasible (L > 11);
  flips, if any, are transient/trough events (finding).

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation
  commit (verified git log order on this lane directory). No
  implementation file (fl_spec.zag, fl_main.zag, fl_build.sh,
  fl_posthoc.sh, fl_full.zag, fl_bin, fl_run*.txt/err) may
  exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python`
  return nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified in-script).
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  fl_bin exits 0 on all 3 runs; stderr empty on all 3 runs;
  stdout 3/3 byte-identical (cmp + sha256). Exactly 72 CELL
  lines per run (4 cells x 18 arms).
- **K4 (anchoring).** (a) Per cell R in {21,60,82,120}: all 18
  arms see identical (D, Q); lazy lines: answered = Q, kb = 2Q,
  refusals = rebuilds, rebuilds <= min(D, Q); eager lines:
  rebuilds = D, answered = Q, refusals = 0, kb = 2Q.
  (b) Arrival splits show the shift (lazy arm): R = 60 and
  R = 120: Dpost = 128 exactly, Qpost < 32, Dpre < 32, Qpre < 32;
  R = 82: Qpost = 128 exactly, Dpost < 32, Dpre < 32, Qpre < 32;
  R = 21: D < 48, Q < 48.
  (c) Structural accounting on all 64 adaptive lines (per cell:
  7 adapt + 3 guard + 3 fastchk + 3 fastewma): D = Dpre + Dpost,
  Q = Qpre + Qpost, answered = Q, kb = 2Q, rebuilds = od + rs,
  refusals = od; (pflips = 0) iff (tf1 = 0) iff (fdir = 0);
  pflips > 0 implies 128 < tf1 <= 256; flips >= pflips;
  lines with flips = 0 and cm in {0,1}: od/rf/rs field-equal to
  the lazy twin; lines with flips = 0 and cm = 2:
  rs = 1 + (D - Dc) and od <= min(Dc, Qc); lc = 0 everywhere
  (pol 3 dormant in this lane).
- **K5 (latency curve).** (a) Exact replication: on all four
  cells, adapt L in {1,3,7} and guard L in {3,7} CELL lines are
  byte-identical to the parent's frozen cs_run1.txt
  (sha256 59e04ecd5e0a33fddc1a8daed2f879098150b74b1683aabea98f1af6fdd01c6d).
  In particular R = 60 adapt: tf1 = 144/160/240, flips = 1,
  fdir = -1, sel = 0 at L = 1/3/7.
  (b) Quirk replication in the new arms: on R in {21,60,82},
  pol 5 and pol 6 at L in {1,7,10}: tc = 32, cm = 2, Dc = 0
  (the degenerate commit fires identically; the deltas did not
  move the pre-shift commit path).
  (c) Monotone latency (theorem): on R = 60, for each adaptive
  arm pol in {2,4,5,6} and each consecutive pair (La,Lb) in its
  L sweep with La < Lb: flips(Lb) >= 1 implies flips(La) >= 1
  and tf1(La) <= tf1(Lb).
- **K6 (too late).** J = rb + rf*L per line, on R = 60.
  (a) J_adapt(7) = 142 > 133 = J_eager (replication of the
  too-late finding).
  (b) J_adapt(10) > J_eager = 133 (theorem: flips>=1 with
  tf1 in {240,256} gives J in {151, >=134}; flips = 0 gives
  rs = 1 + (D - Dc) = 134, hence J >= 134; all > 133).
- **K7 (quirk exonerated).** On R = 60, L in {3,7,10}:
  tf1_guard == tf1_adapt, flips_guard == flips_adapt,
  fdir_guard == fdir_adapt (theorem: identical post-shift EWMA,
  identical flip rule, identical grid, both eager-committed
  pre-shift). The rescue latency is a flip-rule property, not a
  quirk property.
- **K8 (cadence).** On R = 60, L in {1,7,10}:
  (a) tf1_fastchk <= tf1_adapt (theorem: post-shift 8-grid is a
  superset of the 16-grid; EWMA identical).
  (b) flips_adapt >= 1 implies flips_fastchk >= 1 (theorem:
  fires at latest at tf1_adapt, which lies on the 8-grid).
  (c) flips_fastchk >= 1 implies tf1_fastchk >= 136 (theorem:
  first post-shift 8-checkpoint; flips are recorded only for
  e > 128).
- **K9 (EWMA).** On R = 60, pol 6:
  (a) L = 1: flips >= 1 (theorem: at convergence dlo ~ 1023
  and qhi <= ~448 < dlo/2, so 2*qhi < dlo holds).
  (b) Monotone latency within the arm per K5c (already barred
  there; the tf1_fastewma values and J_fastewma are findings:
  faster dh rise vs wider transient eq spikes, direction not
  predicted).
- **K10 (hygiene / governance).** ASCII-only lane sources; no
  world literals (901/902) in fl_spec.zag, fl_main.zag; exactly
  one `fn main` in fl_full.zag; reused sources byte-unmodified
  (`git diff --quiet` on da_base.zag, da_module.zag,
  da_learn.zag, rb_world.zag, rb_fix.zag, et_world.zag,
  et_spec.zag, rr_spec.zag, ld_spec.zag); da_learn.zag in
  particular NOT modified (separate lane only); the cold-start
  lane's cs_spec.zag superseded by copy-plus-delta (fl_spec.zag
  carries [FL-DELTA]/[FL-RENAME] markers), never edited;
  commits local with explicit pathspecs, never pushed.

## What would falsify the lane

- K5a fails (replication lines differ): the copy-plus-delta
  changed inherited dynamics (or a znc name-dependent
  miscompile); the delta is not surgical. BUILD-FAIL, fix the
  delta, do not weaken the bar.
- K5b fails: the quirk does not fire identically in a new arm;
  the cadence/EWMA delta broke the pre-shift commit path.
- K5c fails: tf1 not monotone in L within an arm; the margin
  test is not the L-scaled rule analyzed (implementation bug).
- K6b fails (J_adapt(10) <= 133): the too-late boundary does
  not extend to L = 10; the rescue still beats naive eager.
- K7 fails (guard tf1 != adapt tf1): commit history affects
  rescue latency (e.g. via et_specialize_ret state); the
  flip-rule-property claim dies and the mechanism analysis is
  wrong.
- K8a fails (fastchk later than adapt): the superset-grid
  argument is broken; implementation bug in the cadence delta.
- Any K4 failure: arrival anchoring broken; the cells are not
  the parent's cells.

## Non-goals (frozen)

- No change to the flip rule itself (whether the threshold
  should scale with L is for a follow-up lane; this lane
  characterizes the inherited rule).
- No guard re-litigation (the guard tradeoff was settled in
  SPEC-COLD-START; guard appears here only as the
  quirk-exoneration control).
- No new instrumentation fields; no pol-3 work; no stale-data
  facet (noted in the parent, still untested).
