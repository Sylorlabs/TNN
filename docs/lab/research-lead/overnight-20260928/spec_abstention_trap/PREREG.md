# SPEC-ABSTENTION-TRAP: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_abstention_trap/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-REGIME-CHANGE (BUILD-PASS 8/8, 2026-10-03) put the adaptive policy
switch on nonstationary worlds (one mid-episode rate shift at tick
128). Findings: the opposite-decisive flip rule handled step regime
changes in both directions (6/6 correct-direction flips, zero
wrong-direction, zero oscillation); adaptation latency 16 ticks toward
eager, 32/48/80 toward lazy; burn-in is decision-irrelevant for the
flip rule. Its REPORT left one open follow-up, quoted verbatim: "Map
the abstention trap next. Budget-default (com = 2) is terminal: under
noisier pre-shift regimes the switch could abstain and then be unable
to flip when the regime changes. Either bound the trap (measure at
what noise level pre-shift commits fail) or give budget-default a
post-shift re-check -- but the latter changes the honest-abstention
semantics and needs its own preregistered lane, not a patch." This
lane is that preregistered lane. It builds on SPEC-REGIME-CHANGE
without redesigning it: same cost model J = rb + rf*L, same EWMA
estimator, same margin test, same flip rule, same reused sources
byte-unmodified (da_learn.zag explicitly untouched). The deltas are:
(1) regime cells with SPARSE pre-shift arrivals, chosen to trigger
pre-shift budget-defaults; (2) one experimental arm (pol 3, "rechk")
that makes budget-default deferred instead of terminal; (3) one
appended instrumentation field (lc = late-commit flag).

## The abstention trap (mechanism)

In the inherited checkpoint logic, an episode that is undecided at the
e = 128 budget checkpoint sets com = 2 (budget-default): it runs the
lazy path and the checkpoint function returns immediately on all
later checkpoints. The abstention is terminal. If the regime then
shifts post-128 in a way that would have justified a decisive commit
(e.g. sparse pre-shift data kept the price interval wide, then the
post-shift world is clearly eager-optimal), the episode cannot react:
it is stuck lazy for the rest of the episode. The trap has two
candidate readings, stated as competing hypotheses:

- H-trap-real: terminality is the defect. Abstention was honest
  pre-shift ("evidence too thin to decide"), but the regime change is
  new evidence; a non-terminal abstention (deferred re-check) commits
  correctly post-shift, does not thrash, and saves measurable cost.
- H-trap-correct: terminality is protective. Thin pre-shift evidence
  means the switch should stay conservative; a post-shift re-check
  would chase noise, thrash, or misfire, and staying lazy is the
  honest default.

This lane discriminates them experimentally.

## Questions (frozen)

1. When does the trap trigger? (Characterize the boundary: at what
   pre-shift noise/sparsity level do pre-shift commits fail?)
2. Is it a real problem? (Does it occur outside contrived seeds, and
   does it cost measurable J?)
3. Can it be avoided? (Does the deferred re-check arm commit
   correctly post-shift without thrash?)
4. Or is the trap correct behavior? (Does the recheck arm misfire,
   supporting H-trap-correct?)

## Design (frozen)

**Regime cells (frozen).** T = 256, shift at t = 128, mechanics
identical to the parent (burst/quiet Markov persists, LCG continues
unreseeded, seeds frozen and reset per episode, identical across
arms). Six cells, pre-shift sparsity decreasing down the table to map
the boundary:

- T0: R = 10, (16,16) -> (16,16). Sparse stationary control.
- T1: R = 12, (16,16) -> (16,1). Sparse -> eager world. MAIN TRAP.
- T2: R = 11, (16,16) -> (1,16). Sparse -> lazy world. MIRROR.
- T3: R = 1, (1,16) -> (16,1). Seed-identical to parent R1.
  IDENTITY CONTROL (validates the rebuild changed nothing).
- T4: R = 14, (8,8) -> (16,1). Medium-sparse -> eager. BOUNDARY.
- T5: R = 13, (4,4) -> (16,1). Dense -> eager. BOUNDARY.

R values 10/12/11/14/13 were selected by the seed probe (probe.zag,
committed before this prereg; see below). R values are distinct
because CELL lines are keyed by R. T3 is fixed at R = 1 so its
arrival streams are bit-identical to the parent's R1.

**Arms (frozen).** 10 per cell, 60 episodes total: pol 0 fixed lazy,
pol 1 fixed eager (parent dynamics unchanged), pol 2 adapt with
L in {0,1,3,7} (parent semantics unchanged, including terminal
budget-default), pol 3 "rechk" (recheck) with L in {0,1,3,7}.

**Recheck semantics (frozen).** Pol 3 runs the identical pre-shift
discipline as pol 2: same checkpoints e in {32..128}, same EWMA, same
nr_decide margin test, same commit actions. The ONLY delta: com = 2
at e = 128 is NOT terminal. At each post-shift checkpoint
e in {144..256}, if com = 2, re-run nr_decide on the current
intervals: dec = 2 commits eager (sel = 1, com = 1, tc = e, Dc/Qc
snapshotted, sync restamp rs + 1, lc = 1); dec = 1 commits lazy
(sel = 0, com = 1, tc = e, Dc/Qc snapshotted, lc = 1, no restamp);
dec = 0 stays deferred (com = 2). Once com = 1, the inherited
opposite-decisive flip rule applies unchanged. Pre-shift decisive
commits on pol 3 are byte-identical in behavior to pol 2.

**New instrumentation (one appended field).** lc (CS+116, zero on all
parent-semantics arms): 1 iff the episode committed post-shift from
com = 2 (late commit), else 0. Appended to the CELL line as `lc=`.

**Seed probe disclosure.** probe.zag (committed before this prereg)
replicates ONLY the pre-shift arrival process and prints arrival
counts. Rationale, derived from the inherited nr_decide: with
(dh,ed) = (0,0) the price interval degenerates to {0}, so any L >= 1
is eager-decisive (L*1 > 0): a zero-data eager commit at e = 32 that
would pre-empt the trap. D32 >= 1 (a drift in ticks 0..31)
guarantees (dh,ed) != (0,0) at e = 32, and since ed needs ~129
drift-free ticks to decay to zero, at every later pre-shift
checkpoint too. Selection rule (frozen in probe.zag): T0 lowest
R in 10..19 with D32 >= 1 on (R,16,16,16,16); T1 next such R on
(R,16,16,16,1); T2 next such R on (R,16,16,1,16); T4 lowest
available R with D32 >= 1 on (R,8,8,16,1); T5 lowest available R
with D32 >= 1 on (R,4,4,16,1). Result: T0 = 10 (D32 = 1),
T1 = 12 (D32 = 2), T2 = 11 (D32 = 1), T4 = 14 (D32 = 7),
T5 = 13 (D32 = 11). The probe examined arrival counts only: no
EWMA, no margin test, no commits, no flips, no costs.

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.

## Frozen predictions (not bars; recorded before running)

Pre-shift abstention (adapt, cm = 0 at tc = 128; cm: 0 = budget,
1 = lazy commit, 2 = eager commit): T0 4/4, T1 4/4, T2 4/4, T4 4/4
(symmetric sparse pre-shift keeps the price interval straddling all
L in {0,1,3,7}); T5: L in {0,1} abstain, L in {3,7} commit eager
pre-shift (parent R0 measured this pattern on (4,4)); T3: 0/4
(parent R1 measured lazy commits by tc = 32).

Recheck: T1 L in {1,3,7} late-commit eager (lc = 1, sel = 1, cm = 2,
tc = 144); T1 L = 0 stays com = 2 (eager impossible at L = 0).
T2 L in {0,1,3} late-commit lazy (lc = 1, sel = 0, cm = 1,
tc = 144); T2 L = 7 stays com = 2. T4 like T1. T5 L = 1 late
eager commit; L in {3,7} identical to adapt (pre-shift eager);
L = 0 stays com = 2. T0 recheck stays com = 2 on all L (no late
commits under stationary sparsity). T3 recheck field-equal to adapt
on all numeric fields.

Economics: on trapped-then-late-eager episodes (T1 L = 1),
J_rechk < J_adapt strictly: the trapped arm pays ~Dpost refused
queries at (1+L) each under lazy while the recheck arm pays one
sync restamp plus Dpost eager restamps.

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation commit
  (verified git log order on this lane directory). No implementation
  file (at_spec.zag, at_main.zag, at_build.sh, at_full.zag, at_bin,
  at_run*.txt/err) may exist in the prereg commit. The probe commit
  (probe.zag, probe_full.zag, probe_bin, probe_compile.txt,
  probe_out.txt, probe_err.txt) precedes the prereg and contains
  design tooling only.
- **K2.** Safebin mandatory: `which python3` and `which python`
  return nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified in-script).
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  at_bin exits 0 on all 3 runs; stderr empty on all 3 runs; stdout
  3/3 byte-identical (cmp + sha256). Exactly 60 CELL lines per run
  (6 cells x 10 arms).
- **K4 (anchoring).** (a) Per cell R in {10,12,11,1,14,13}: all 10
  arms see identical (D, Q); lazy lines: answered = Q, kb = 2Q,
  refusals = rebuilds, rebuilds <= min(D, Q); eager lines:
  rebuilds = D, answered = Q, refusals = 0, kb = 2Q. (b) Arrival
  splits show the shift (lazy arm): R = 12: Qpost = 128 exactly,
  Dpost < 32, Dpre < 32, Qpre < 32; R = 11: Dpost = 128 exactly,
  Qpost < 32, Dpre < 32, Qpre < 32; R = 14: Qpost = 128 exactly,
  Dpre < 64, Qpre < 64, Dpost < 32; R = 13: Qpost = 128 exactly,
  Dpre < 64, Qpre < 64, Dpost < 32; R = 10: D < 48, Q < 48.
  (c) T3 cross-lane identity: for pol in {lazy, eager} and adapt
  L in {0,1,3,7}, the R = 1 line with the trailing ` lc=0` stripped
  is byte-equal to the parent spec_regime_change/rc_run1.txt R = 1
  line for the same arm (seed-identical streams; validates the
  rebuild did not change inherited pol-2 behavior). (d) T3 recheck
  identical to adapt: all numeric fields equal between P = rechk
  and P = adapt on R = 1 for each L.
- **K5 (trap occurrence + boundary).** n_abstain(R) = #{L in
  {0,1,3,7}: adapt cm = 0} on cell R. (a) R = 12 adapt L = 0:
  cm = 0; R = 12 adapt L = 1: cm = 0 (the trap triggers on the
  robust core). (b) n_abstain(12) >= 3 and n_abstain(13) <= 3
  (trap strong at the sparse end, weaker at the dense end).
  (c) R = 13 adapt L = 7: cm = 2 (the dense end escapes via a
  pre-shift eager-decisive commit).
- **K6 (recheck behavior).** (a) R = 12 rechk L = 1: lc = 1,
  sel = 1, cm = 2, 128 < tc <= 176 (late eager commit, correct
  direction, prompt). (b) All 6 rechk L = 0 episodes: sel = 0 and
  cm != 2; R = 12 rechk L = 0: cm = 0, lc = 0 (never eager at
  L = 0). (c) Every rechk episode: flips <= 2; total rechk flips
  <= 4; R = 10 rechk flips = 0 on all L (no thrash). (d) R = 11
  rechk: zero episodes with sel = 1; per L, J_rechk == J_adapt and
  flips equal (recheck harmless where abstention was fine).
  (e) Late-commit consistency on all 60 lines: (lc = 1) iff
  (P = rechk and tc > 128); lc = 1 implies cm in {1,2}; rechk
  episodes with lc = 1 and cm = 2: rs = 1 + (D - Dc); with lc = 1
  and cm = 1: rs = 0 and od/rf field-equal to the lazy twin.
  (f) Structural accounting on all 40 adapt + rechk lines:
  D = Dpre + Dpost, Q = Qpre + Qpost, answered = Q, kb = 2Q,
  rebuilds = od + rs, refusals = od; (pflips = 0) iff (tf1 = 0)
  iff (fdir = 0); pflips > 0 implies 128 < tf1 <= 256;
  flips >= pflips; adapt episodes with flips = 0 and cm in {0,1}:
  od/rf/rs field-equal to the lazy twin; adapt episodes with
  flips = 0 and cm = 2: rs = 1 + (D - Dc) and od <= min(Dc, Qc);
  rechk episodes with lc = 0: same checks as adapt by cm value.
- **K7 (economics).** J = rb + rf*L per line. (a) R = 12: for each
  L in {1,3,7} with adapt cm = 0 and rechk lc = 1 and rechk
  sel = 1: J_rechk < J_adapt strictly (wherever the trap
  triggered and the recheck fired eager, the recheck wins).
  (b) R = 11 all L: J_rechk == J_adapt. (c) R = 10 all L:
  J_rechk <= J_adapt + 1. (d) R = 14 and R = 13: the same
  adaptive bar as (a).
- **K8 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in at_spec.zag, at_main.zag; exactly one
  `fn main` in at_full.zag; reused sources byte-unmodified
  (`git diff --quiet` on da_base.zag, da_module.zag, da_learn.zag,
  rb_world.zag, rb_fix.zag, et_world.zag, et_spec.zag, rr_spec.zag,
  ld_spec.zag); da_learn.zag in particular NOT modified (separate
  lane only); commits local with explicit pathspecs, never pushed.

## What would falsify the lane

- R = 12 adapt L in {0,1} not cm = 0 (K5a): the trap does not
  trigger on the robust core. The lane FAILs as designed and the
  report becomes a negative finding (plus the realized reason).
- R = 12 rechk L = 1 with lc = 0 (K6a): the deferred re-check does
  not fire post-shift; avoidance fails.
- R = 12 rechk L = 1 with sel = 0 or cm != 2 (K6a): the recheck
  fires in the wrong direction.
- Any rechk episode with flips >= 3, or total rechk flips > 4
  (K6c): the recheck thrashes under nonstationarity; H-trap-correct
  wins and terminality was protective.
- T3 cross-lane identity fails (K4c): the rebuild changed inherited
  pol-2 behavior; implementation defect, not a scientific result.
- R = 11 rechk with sel = 1 anywhere (K6d): the recheck invents
  eager commitments where the post-shift world is lazy-optimal.
