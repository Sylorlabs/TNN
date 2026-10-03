# SPEC-COLD-START: PREREG (frozen kill bars)

**Lane:** docs/lab/research-lead/overnight-20260928/spec_cold_start/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Prereg committed strictly
before any implementation file exists.

## Parent result this builds on

SPEC-ABSTENTION-TRAP (BUILD-FAIL on K5b, 2026-10-03) mapped the
abstention trap and disclosed, but did not test, a design-phase
quirk, quoted verbatim from its REPORT: "with (dh,ed) = (0,0) the
inherited margin test's price interval degenerates to {0}, making
any L >= 1 eager-decisive: a zero-data eager commit at e = 32. The
probe's D32 >= 1 selection rule kept this out of the sealed cells;
the quirk itself is untested and belongs in a cold-start lane, not
a patch here." This lane is that cold-start lane. It builds on
SPEC-ABSTENTION-TRAP without redesigning it: same cost model
J = rb + rf*L, same EWMA estimator, same nr_decide margin test,
same flip rule, same arrival mechanics and seed formulas, same
reused sources byte-unmodified (the 9 grandparent sources plus the
trap lane's at_spec.zag, which is superseded by copy-plus-delta,
not edited; da_learn.zag explicitly untouched). The deltas are:
(1) regime cells engineered for D32 == 0 (zero drifts in ticks
0..31), selected by the pre-prereg seed probe, so the quirk fires
by construction; (2) one experimental arm (pol 4, "guard") that
adds a minimum-data rule to the inherited commit logic; (3) no new
instrumentation fields (the guard's effect is fully visible in the
inherited tc/cm/Dc/sel/rs fields).

## The cold-start quirk (mechanism)

In the inherited checkpoint logic, the first checkpoint runs at
e = 32. If no drift has been observed by then, the EWMA state is
exactly (dh,ed) = (0,0): dh starts at 0 and df = 0 every tick keeps
it at 0; devd = 1024*df - dh = 0 keeps ed at 0. Then
sed = isqrt(ed/31) = 0, so dlo = dhi = 0, and nr_decide computes
phin = max0(dhi - qlo) = 0 with phid = maxi(qlo,1) >= 1:
eager-decisive iff L*phid > 0, i.e. every L >= 1. Lazy-decisive
needs L*plod < plon = max0(dlo - qhi) = 0, impossible. So any
L >= 1 commits eager at e = 32 with zero drift observations: the
{0} price interval is treated as decisive evidence that rebuilds
are free. At L = 0 neither direction can fire (0 > phin is false),
so L = 0 stays undecided. Note the degenerate condition is on the
estimator state (dh,ed), not the raw counter: (dh,ed) = (0,0)
holds iff no drift has been observed within the estimator's
effective memory (~129 drift-free ticks for ed to decay to zero).
On the preregistered cells the pre-shift window is 128 ticks, so
the guard binds exactly in the pure cold-start case here; a
stale-data facet (ancient drifts fully decayed, interval
re-collapsing to {0}) is a design observation that cannot trigger
on these cells and is not preregistered.

## Questions (frozen)

1. Characterize the quirk: does the zero-data eager commit fire
   exactly as disclosed (tc = 32, cm = 2, sel = 1, Dc = 0,
   phin = 0, pnum = 0, dhi = 0) for L >= 1 on D32 == 0 cells,
   regardless of query data (Q32 > 0 on all three)?
2. Is it a real problem: does the zero-data eager commit cause
   measurable harm where the world is lazy-optimal (wrong-direction
   commit, rescued or not by the flip rule)?
3. Should the margin test require minimum data before committing:
   does the permanent guard (block eager commits while
   (dh,ed) = (0,0)) strictly reduce harm, and does it change
   behavior anywhere data exists?
4. Or is zero-data eager actually correct: where the world is
   eager-optimal, or genuinely sparse, does the unguarded quirk
   beat the guard (making the guard a tradeoff, not a fix)?

## Design (frozen)

**Regime cells (frozen).** T = 256, shift at t = 128, mechanics
identical to the parent (burst/quiet Markov persists, LCG
continues unreseeded, seeds frozen and reset per episode,
identical across arms). Four cells, all with sparse (16,16)
pre-shift so D32 == 0 is realizable:

- CS0: R = 21, (16,16) -> (16,16). Sparse stationary control.
  D32 = 0, Q32 = 5, Dpre = 8, Qpre = 8.
- CS1: R = 60, (16,16) -> (1,16). Sparse -> drift-dense
  (lazy-optimal post). HARM CELL. D32 = 0, Q32 = 1, Dpre = 5,
  Qpre = 14.
- CS2: R = 82, (16,16) -> (16,1). Sparse -> query-dense
  (eager-optimal post). BENEFIT CELL. D32 = 0, Q32 = 2,
  Dpre = 6, Qpre = 5.
- CS3: R = 120, (16,16) -> (1,16). Same regime as CS1 but
  D32 = 1 (quirk absent). GUARD-PURITY CONTROL. Q32 = 3,
  Dpre = 12, Qpre = 10.

R values selected by the seed probe (probe.zag, committed before
this prereg; see below). Ranges were disjoint per cell so the four
R values are distinct (CELL lines are keyed by R).

**Arms (frozen).** 10 per cell, 40 episodes total: pol 0 fixed
lazy, pol 1 fixed eager (parent dynamics unchanged), pol 2 adapt
with L in {0,1,3,7} (parent semantics unchanged, quirk included),
pol 4 "guard" with L in {0,1,3,7}.

**Guard semantics (frozen).** Pol 4 runs the identical discipline
as pol 2: same checkpoints e in {32..128}, same EWMA, same
nr_decide margin test, same commit actions, same flip rule, same
terminal budget-default. The ONLY delta: in the com == 0 branch, a
dec == 2 (eager-decisive) outcome is NOT committed while
dh == 0 && ed == 0 (the degenerate {0} price interval); the
episode stays undecided at that checkpoint. At e = 128 a still
degenerate dec == 2 therefore falls through to budget-default
(com = 2, cm = 0) instead of committing eager. The guard never
blocks lazy commits (dec == 1 requires dlo > 0, hence ed > 0)
and never affects the flip rule or any pol-2 path once data
exists. Pol-3 code is inherited dormant (not swept in this lane).

**Seed probe disclosure.** probe.zag (committed before this
prereg) replicates ONLY the pre-shift arrival process and prints
arrival counts, identical in structure to the parent probe with
the selection rule inverted. Rationale: D32 == 0 guarantees
(dh,ed) = (0,0) at e = 32, so the quirk fires by construction.
Selection rule (frozen in probe.zag): CS0 lowest R in 20..49 with
D32 == 0 on (R,16,16,16,16); CS1 lowest R in 50..79 with
D32 == 0 on (R,16,16,1,16); CS2 lowest R in 80..109 with
D32 == 0 on (R,16,16,16,1); CS3 lowest R in 120..149 with
D32 >= 1 on (R,16,16,1,16). Result: CS0 = 21 (D32 = 0, Q32 = 5),
CS1 = 60 (D32 = 0, Q32 = 1), CS2 = 82 (D32 = 0, Q32 = 2),
CS3 = 120 (D32 = 1, Q32 = 3). The probe examined arrival counts
only: no EWMA, no margin test, no commits, no flips, no costs.

**Cost model (frozen, unchanged).** J = rb + rf*L per line, C = 1.

## Frozen predictions (not bars; recorded before running)

Quirk mechanics: on CS0/CS1/CS2, adapt L in {1,3,7} commits eager
at tc = 32 with Dc = 0, dh = dlo = dhi = pnum = phin = 0,
sel = 1, cm = 2, regardless of Q32. Adapt L = 0 never eager
(sel = 0, cm != 2) on all four cells.

Guard mechanics: on CS0/CS1/CS2, no guard episode commits eager
with Dc = 0; every guard eager commit has Dc >= 1 (drift data
seen). Guard lines are field-identical to adapt at L = 0 on every
cell, and field-identical to adapt at every L on CS3.

Harm: on CS1, adapt's zero-data eager commit is wrong-direction:
episodes flip to lazy post-shift (flips >= 1, final sel = 0) and
at L = 1 the guard is strictly cheaper (J_guard < J_adapt).

Benefit: on CS2 at L = 1, adapt's zero-data eager commit is
right-direction and strictly cheaper than the guard's abstention
(J_adapt < J_guard).

Default-correctness: on CS0 (genuine sparsity) at L in {3,7},
adapt's zero-data eager commit beats the guard's abstention
(J_adapt < J_guard); at L = 1 the two are within noise (finding).

## Kill bars (frozen)

- **K1.** Prereg commit strictly precedes the implementation
  commit (verified git log order on this lane directory). No
  implementation file (cs_spec.zag, cs_main.zag, cs_build.sh,
  cs_full.zag, cs_bin, cs_run*.txt/err) may exist in the prereg
  commit. The probe commit (probe.zag, probe_full.zag, probe_bin,
  probe_compile.txt, probe_out.txt, probe_err.txt) precedes the
  prereg and contains design tooling only.
- **K2.** Safebin mandatory: `which python3` and `which python`
  return nothing; pinned znc sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified in-script).
- **K3.** znc builds the assembly clean (no `: error`, exit 0);
  cs_bin exits 0 on all 3 runs; stderr empty on all 3 runs; stdout
  3/3 byte-identical (cmp + sha256). Exactly 40 CELL lines per run
  (4 cells x 10 arms).
- **K4 (anchoring).** (a) Per cell R in {21,60,82,120}: all 10
  arms see identical (D, Q); lazy lines: answered = Q, kb = 2Q,
  refusals = rebuilds, rebuilds <= min(D, Q); eager lines:
  rebuilds = D, answered = Q, refusals = 0, kb = 2Q.
  (b) Arrival splits show the shift (lazy arm): R = 60 and
  R = 120: Dpost = 128 exactly, Qpost < 32, Dpre < 32, Qpre < 32;
  R = 82: Qpost = 128 exactly, Dpost < 32, Dpre < 32, Qpre < 32;
  R = 21: D < 48, Q < 48.
  (c) Structural accounting on all 32 adapt + guard lines:
  D = Dpre + Dpost, Q = Qpre + Qpost, answered = Q, kb = 2Q,
  rebuilds = od + rs, refusals = od; (pflips = 0) iff (tf1 = 0)
  iff (fdir = 0); pflips > 0 implies 128 < tf1 <= 256;
  flips >= pflips; lines with flips = 0 and cm in {0,1}:
  od/rf/rs field-equal to the lazy twin; lines with flips = 0
  and cm = 2: rs = 1 + (D - Dc) and od <= min(Dc, Qc).
- **K5 (quirk characterization).** On R in {21,60,82}, for
  L in {1,3,7}: adapt tc = 32, cm = 2, sel = 1, Dc = 0,
  dh = 0, dlo = 0, dhi = 0, pnum = 0, phin = 0, phid >= 1.
  On all four cells: adapt L = 0 has sel = 0 and cm != 2.
- **K6 (guard mechanics).** (a) On R in {21,60,82}, for
  L in {1,3,7}: no guard line has (cm = 2 and tc = 32); every
  guard line with cm = 2 has Dc >= 1. (b) On all four cells:
  guard L = 0 is field-equal to adapt L = 0 on all numeric
  fields (the guard never binds at L = 0). (c) On R = 120:
  guard is field-equal to adapt on all numeric fields for each
  L in {0,1,3,7} (the guard never binds when drift data exists
  at e = 32).
- **K7 (harm / benefit / default).** J = rb + rf*L per line.
  (a) R = 60 adapt L in {1,3,7}: flips >= 1 and final sel = 0
  (the zero-data eager commit was wrong-direction; the flip rule
  rescued it). (b) R = 60 L = 1: J_guard < J_adapt strictly
  (measured harm of the quirk). (c) R = 82 L = 1:
  J_adapt < J_guard strictly (the quirk's early eager commit is
  right-direction where the world is eager-optimal). (d) R = 21
  L in {3,7}: J_adapt < J_guard strictly (zero-data eager is the
  cheaper default under genuine sparsity).
- **K8 (hygiene / governance).** ASCII-only lane sources; no world
  literals (901/902) in cs_spec.zag, cs_main.zag, probe.zag;
  exactly one `fn main` in cs_full.zag and probe_full.zag; reused
  sources byte-unmodified (`git diff --quiet` on da_base.zag,
  da_module.zag, da_learn.zag, rb_world.zag, rb_fix.zag,
  et_world.zag, et_spec.zag, rr_spec.zag, ld_spec.zag, and the
  trap lane's at_spec.zag); da_learn.zag in particular NOT
  modified (separate lane only); commits local with explicit
  pathspecs, never pushed.

## What would falsify the lane

- CS0/CS1/CS2 adapt L >= 1 not committing eager at tc = 32 with
  Dc = 0 (K5): the quirk does not fire as disclosed. The lane
  FAILs as designed and the report becomes a negative finding
  (plus the realized reason).
- Any guard eager commit with Dc = 0 (K6a): the minimum-data rule
  does not block the degenerate commit; the guard is not the
  intervention it claims to be.
- R = 120 guard not field-equal to adapt (K6c): the guard changes
  behavior where drift data exists; the "pure degenerate-case
  intervention" claim dies.
- R = 60 adapt L in {1,3,7} with flips = 0 or final sel = 1
  (K7a): the zero-data commit was not wrong-direction; the harm
  mechanism is absent.
- R = 60 L = 1 with J_guard >= J_adapt (K7b): no measured harm;
  the quirk's cost is fully absorbed by the flip rule.
- R = 82 L = 1 with J_adapt >= J_guard (K7c): no measured
  benefit; abstention costs nothing where eager is optimal.
- R = 21 L in {3,7} with J_adapt >= J_guard (K7d): zero-data
  eager is not the cheaper default under genuine sparsity.
