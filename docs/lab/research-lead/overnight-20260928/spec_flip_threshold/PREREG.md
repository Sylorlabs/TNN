# SPEC-FLIP-THRESHOLD: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_flip_threshold/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-FLIP-LATENCY (BUILD-PASS K1-K10, 2026-10-03) characterized the
flip-rule rescue latency on the harm cell CS1 (R = 60): tf1 = 144/160/240
at L = 1/3/7, then the flip never comes at L >= 10. Its mechanism
analysis (frozen): the flip rule reuses nr_decide, eager -> lazy needs
lazy-decisive, L*plod < plon, i.e. (L+1)*qhi < dlo. The (L+1) multiplier
falls on qhi, the upper query bound: L scales the evidence bar against
query-side uncertainty, and the rescue is gated by query-gap troughs.
Steady-state on R = 60: dlo -> 1024, qh -> ~80, so steady-state flips
need L <= 11. The quirk was exonerated (K7: guard tick-identical to
adapt). Latency proved reducible via cadence (fastchk) and estimator
speed (fastewma), both of which leave the (L+1)*qhi < dlo bar itself
untouched. The parent's recommendation 1: "Any future flip-threshold
work should target the query-side uncertainty term (qhi), which gates
the rescue, not the drift estimate." Its explicit non-goal: "Whether
the flip threshold should scale with L (a threshold redesign) was
explicitly a non-goal; this lane characterizes the inherited rule."
This lane is that threshold-redesign lane. It is the well-posed question
the parent's evidence-bar analysis produced.

## The redesign question (frozen)

Current rule: flip eager -> lazy iff (L+1)*qhi < dlo. L is caller-stated,
not measured (inherited). Three candidate answers, tested as three new
policy arms on the parent's discipline (same EWMA, same commit rule
including the quirk, same grid, same eager-decisive direction, same
arrival mechanics; ONLY the flip-path lazy bar changes):

- **pol 7 "fix2" (fixed threshold):** flip iff 2*qhi < dlo. No L in the
  bar. Tests: should the threshold scale with L at all? At L = 1 this is
  arithmetically identical to the inherited rule (both need 2*qhi < dlo),
  which yields a built-in identity check (K5d).
- **pol 8 "qmean" (qhi estimated differently):** flip iff (L+1)*qh < dlo.
  The point estimate qh replaces the interval upper bound qhi; L-scaling
  is kept. Tests: is the interval-upper conservatism (eq spikes on
  bursty arrivals) what gates the rescue? Scope note: this is the one
  qhi-estimation variant tried here (interval-vs-point); other
  re-estimations (e.g. narrower intervals) are not in scope.
- **pol 9 "adaptd" (adaptive threshold):** flip iff M*qhi < dlo with
  M = max(2, (L+1)-(n-1)), where n = number of post-shift (e > 128)
  com == 1 checkpoints evaluated so far (n = 1 at the first post-shift
  checkpoint, so M starts at the inherited L+1 and relaxes by 1 per
  fruitless checkpoint, floored at 2 = the fix2 bar). Pre-shift
  (n = 0): M = L, the inherited bar. Tests: should the bar relax as
  evidence accumulates without a flip? Rationale: each additional eager
  rebuild observed is itself evidence the eager stint is costly; the
  bar adapts to patience, not to a new measurement.

The eager-decisive direction (L*phid > phin) is UNCHANGED in all arms:
the redesign targets the rescue (eager -> lazy) bar only. The commit
rule (com == 0 branch, including the quirk) is UNCHANGED in all arms,
so quirk fields must replicate identically (K5b) and any tf1 spread
across the four threshold arms is a flip-rule property by construction
(K8b).

## Questions (frozen)

1. Does L-scaling improve J? (K7: J_fix2 vs J_adapt on the harm cell;
   J_qmean / J_adaptd as scored findings.)
2. Does the redesign reduce tf1? (K6: bar-ease orderings, all
   theorem-safe; K6e: the fixed bar's rescue timing is L-independent.)
3. Is the quirk exoneration preserved? (K8: guard/adapt tick-identity
   replicated; tf1 spread across threshold arms with identical quirk
   fields.)
4. Does the aggressive fixed bar flip where it should not? (K9: control
   cells; mechanism ordering barred, spurious flips reported as
   findings with J impact.)

## Design (frozen)

**Regime cells (frozen, inherited).** T = 256, shift at t = 128,
mechanics identical to the parent. Four cells: CS0 R = 21
(16,16)->(16,16) sparse stationary; CS1 R = 60 (16,16)->(1,16)
sparse -> drift-dense, THE HARM CELL (D32 = 0, quirk fires by
construction); CS2 R = 82 (16,16)->(16,1) sparse -> query-dense;
CS3 R = 120 (16,16)->(1,16) D32 = 1 control. No new probe.

**Arms (frozen).** 21 per cell, 84 episodes total: pol 0 fixed lazy,
pol 1 fixed eager (parent dynamics unchanged), pol 2 adapt L in
{1,3,7,10} (L-scaled control; replication), pol 4 guard L in {3,7,10}
(quirk-exoneration control), pol 7 fix2 L in {1,3,7,10}, pol 8 qmean
L in {1,3,7,10}, pol 9 adaptd L in {1,3,7,10}.

**Implementation (frozen, copy-plus-delta).** ft_spec.zag is a minimal
documented delta on the parent's fl_spec.zag ([FT-DELTA] markers,
[FT-RENAME] fl_ -> ft_): nr_decide UNCHANGED (commit path, pol-3
branch); new nr_decide_ft(dh,qh,dlo,dhi,qlo,qhi,L,pol,nchk) used ONLY
in the com == 1 (flip) branch, with the eager direction identical to
nr_decide and the lazy bar per the three variants above (hoisted
flags, znc workaround: shallow if-nesting); CS+120 holds the pol-9
post-shift checkpoint counter nchk (init 0; incremented only for
pol == 9 at com == 1 checkpoints with e > 128; never emitted, so the
CELL line format is unchanged and K5a byte-replication is possible);
nr_polname gains fix2/qmean/adaptd; ft_episode wires pol 7/8/9 through
the adapt initialization, EWMA updates, and checkpoint call. The
parent's fl_spec.zag is byte-unmodified in its own lane (K10). The 9
grandparent sources are reused byte-unmodified. da_learn.zag untouched.

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.

## Frozen predictions (not bars; recorded before running)

- K5a replication: adapt L in {1,3,7}, guard L in {3,7} CELL lines
  byte-identical to the parent's frozen fl_run1.txt on all four cells
  (sha256 b81f6080d57a4bc7b29eb71a820fc3897a0b5bb68680f60c28bf509af629d9ac).
- fix2 rescue timing is L-independent on R = 60: tf1 = 144, flips = 1,
  fdir = -1 at L in {1,3,7,10} (same lazy bar, same EWMA, same grid as
  adapt L = 1; the eager-decisive direction cannot fire first while
  eager-committed).
- Implied J_fix2 on R = 60 (from the parent's frozen adapt L = 1 line:
  rs = 22, od = 10; J = rs + od*(L+1)): 42/62/102/132 at L = 1/3/7/10.
  Note J_fix2(7) = 102 equals fastewma's J = 102: the fixed bar matches
  the estimator-speed lever's rescue value on this cell.
- tf1_qmean(7) <= 240, tf1_adaptd(7) <= 240; both flip at L = 10 (bars
  easier than adapt's never-flip). qmean may flip at L = 10 in steady
  state (11*qh < dlo feasible: 11*80 = 880 < 1024).
- Control cells: no flips expected for any arm on R = 21/82 (finding;
  the aggressive bars still need dlo > 0, which sparse drift does not
  supply). R = 120: fix2 expected to flip (same regime as R = 60).

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation commit
  (verified git log order on this lane directory). No implementation
  file (ft_spec.zag, ft_main.zag, ft_build.sh, ft_posthoc.sh,
  ft_full.zag, ft_bin, ft_run*.txt/err) may exist in the prereg commit.
- **K2.** Safebin mandatory: `which python3` and `which python` return
  nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified in-script).
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  ft_bin exits 0 on all 3 runs; stderr empty on all 3 runs; stdout 3/3
  byte-identical (cmp + sha256). Exactly 84 CELL lines per run
  (4 cells x 21 arms).
- **K4 (anchoring).** (a) Per cell R in {21,60,82,120}: all 21 arms see
  identical (D, Q); lazy lines: answered = Q, kb = 2Q, refusals =
  rebuilds, rebuilds <= min(D, Q); eager lines: rebuilds = D,
  answered = Q, refusals = 0, kb = 2Q. (b) Arrival splits show the shift
  (lazy arm): R = 60 and R = 120: Dpost = 128 exactly, Qpost < 32,
  Dpre < 32, Qpre < 32; R = 82: Qpost = 128 exactly, Dpost < 32,
  Dpre < 32, Qpre < 32; R = 21: D < 48, Q < 48. (c) Structural
  accounting on all 76 adaptive lines (per cell: 4 adapt + 3 guard +
  4 fix2 + 4 qmean + 4 adaptd): D = Dpre + Dpost, Q = Qpre + Qpost,
  answered = Q, kb = 2Q, rebuilds = od + rs, refusals = od;
  (pflips = 0) iff (tf1 = 0) iff (fdir = 0); pflips > 0 implies
  128 < tf1 <= 256; flips >= pflips; lines with flips = 0 and cm in
  {0,1}: od/rf/rs field-equal to the lazy twin; lines with flips = 0
  and cm = 2: rs = 1 + (D - Dc) and od <= min(Dc, Qc); lc = 0
  everywhere (pol 3 dormant in this lane).
- **K5 (replication / quirk / monotonicity).** (a) Exact replication: on
  all four cells, adapt L in {1,3,7} and guard L in {3,7} CELL lines are
  byte-identical to the parent's frozen fl_run1.txt. (b) Quirk fires
  identically in the new arms: on R in {21,60,82}, pol in {7,8,9} at L
  in {1,3,7,10}: tc = 32, cm = 2, Dc = 0. (c) Monotone latency
  (theorem): on R = 60, for each arm pol in {2,4,7,8,9} and each
  consecutive pair (La,Lb) in its L sweep with La < Lb: flips(Lb) >= 1
  implies flips(La) >= 1 and tf1(La) <= tf1(Lb). (d) L = 1 identity: on
  all four cells, the fix2 L = 1 CELL line equals the adapt L = 1 CELL
  line modulo the P= field (same bar, same L, same everything).
- **K6 (threshold redesign moves tf1).** On R = 60, L in {1,3,7,10}:
  (a) tf1_fix2 <= tf1_adapt; flips_adapt >= 1 implies flips_fix2 >= 1.
  (b) tf1_qmean <= tf1_adapt; flips_adapt >= 1 implies flips_qmean >= 1.
  (c) tf1_adaptd <= tf1_adapt; flips_adapt >= 1 implies flips_adaptd >= 1.
  (d) tf1_fix2 <= tf1_adaptd; flips_adaptd >= 1 implies flips_fix2 >= 1.
  (e) fix2 tf1/flips/fdir equal adapt(L = 1) tf1/flips/fdir at each L
  (the fixed bar's rescue timing is L-independent). All are theorems:
  at fixed estimator state the easier bar fires whenever the harder
  bar fires; EWMA trajectory and grid are arm-independent; the eager
  direction cannot record a flip before the first lazy flip.
- **K7 (J: does the redesign improve J?).** On R = 60:
  (a) J_fix2(7) < J_adapt(7) = 142. (b) J_fix2(10) < J_eager = 133
  (positive rescue value restored where the L-scaled bar never flips;
  implied 132 from the frozen parent data). J_qmean and J_adaptd vs
  adapt are scored findings (reported, not barred).
- **K8 (quirk exoneration preserved).** (a) On R = 60, L in {3,7,10}:
  tf1_guard == tf1_adapt, flips_guard == flips_adapt,
  fdir_guard == fdir_adapt (parent K7 replicated). (b) The redesign
  moves tf1: at L = 7 on R = 60, tf1 takes at least two distinct values
  across pol in {2,7,8,9} while quirk fields (tc, cm, Dc) are identical
  across the four arms: the latency spread is a flip-rule property, not
  a quirk property.
- **K9 (control cells).** (a) Mechanism integrity on every cell: for
  every cell R in {21,60,82,120} and L in {1,3,7,10}:
  flips_adapt(L) >= 1 implies flips_fix2(L) >= 1, flips_qmean(L) >= 1,
  flips_adaptd(L) >= 1 (the bar-ease ordering is cell-independent).
  (b) Findings (reported, not barred): flips and J of the new arms on
  R = 21/82/120; whether the aggressive bars flip where adapt does not,
  and the J cost of any such spurious flip.
- **K10 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in ft_spec.zag, ft_main.zag; exactly one `fn main`
  in ft_full.zag; reused sources byte-unmodified (`git diff --quiet` on
  da_base.zag, da_module.zag, da_learn.zag, rb_world.zag, rb_fix.zag,
  et_world.zag, et_spec.zag, rr_spec.zag, ld_spec.zag); da_learn.zag in
  particular NOT modified (separate lane only); the parent lane's
  fl_spec.zag superseded by copy-plus-delta (ft_spec.zag carries
  [FT-DELTA]/[FT-RENAME] markers), never edited; commits local with
  explicit pathspecs, never pushed.

## What would falsify the lane

- K5a fails (replication lines differ): the copy-plus-delta changed
  inherited dynamics (or a znc name-dependent miscompile); the delta is
  not surgical. BUILD-FAIL, fix the delta, do not weaken the bar.
- K5d fails: the flip path diverges at L = 1 between fix2 and adapt;
  the "fixed" bar is not the claimed 2*qhi < dlo. BUILD-FAIL.
- K6a fails (fix2 later than adapt anywhere): the bar-ease theorem is
  broken; implementation bug in the variant bar. BUILD-FAIL.
- K6e fails: the fixed bar's rescue is not L-independent; the eager
  direction interferes (e.g. re-flips) or the bar sees L after all.
- K7a fails (J_fix2(7) >= 142): the fixed threshold does not improve J
  on the harm cell; the redesign's core claim dies. BUILD-FAIL (the
  lane's question is answered negatively; report it as such).
- K7b fails (J_fix2(10) >= 133): no positive rescue value at L = 10;
  the fixed bar does not beat naive eager where the L-scaled bar is
  absent.
- K8a fails (guard/adapt diverge): the exoneration breaks under the
  refactor; the mechanism analysis is wrong.
- Any K4 failure: arrival anchoring broken; the cells are not the
  parent's cells.

## Non-goals (frozen)

- No change to the commit rule, the EWMA estimator, the eager-decisive
  direction, the checkpoint grid, or the arrival mechanics.
- No guard re-litigation (guard is the exoneration control only).
- No pol-3 / pol-5 / pol-6 work (dormant in this lane).
- No new instrumentation fields: the CELL line format is frozen so the
  K5a replication is byte-exact (the pol-9 patience counter CS+120 is
  deliberately un-emitted).
- No verdict on which threshold is "best overall" beyond the barred J
  comparisons and the reported findings: one seed per cell, one shift
  per episode (inherited limits).
