# SPEC-FLIP-LATENCY: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_flip_latency/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (K1-K10 all pass)**

## Summary

This lane traced the flip-rule rescue latency recommended by
SPEC-COLD-START ("tf1 grows with L; L=7 rescue was too late").
72 episodes (4 inherited regime cells x 18 arms: fixed lazy,
fixed eager, adapt L in {1,3,7,10,15,20,30}, guard L in {3,7,10},
fastchk L in {1,7,10}, fastewma L in {1,7,10}), one binary, pure
Zag, safebin-built, 3/3 byte-identical (sha256
b81f6080d57a4bc7b29eb71a820fc3897a0b5bb68680f60c28bf509af629d9ac).

The two new arms are the lane's experimental deltas on the
parent's policy layer, everything else inherited unchanged:
pol 5 "fastchk" halves the post-shift checkpoint cadence
(136,144,152,...,256; pre-shift grid unchanged so the quirk
fires at e = 32 identically), pol 6 "fastewma" doubles the EWMA
speed (7/8 weight instead of 15/16). The flip rule, margin test,
commit rule, guard, and arrival mechanics are the parent's,
byte-identical on the overlapping sweep (K5a: 20 adapt/guard
lines byte-identical to the parent's frozen run).

**Headline:** the latency curve is fully characterized and the
quirk is exonerated. On the harm cell (R = 60): tf1_adapt =
144/160/240 at L = 1/3/7, then the flip **never comes** at
L >= 10 (flips = 0; adapt degrades to eager-plus-one-commit-
restamp, J = 134 > 133 = J_eager). Guard shows tick-identical
flip behavior at every L (K7) -- rescue latency is a flip-rule
property, not a quirk property. Latency is reducible, and
substantially: halving the post-shift checkpoint cadence moved
the L = 7 rescue from tf1 = 240 to tf1 = 168 (J 142 -> 118,
now beating fixed eager); doubling EWMA speed moved it to
tf1 = 144 for L = 7 AND L = 10 (J 142 -> 102 at L = 7, beating
every other arm including fixed lazy; J 134 -> 132 at L = 10,
restoring a positive rescue value). The mechanism: the rescue
needs (L+1)*qhi < dlo, so L scales the evidence bar against
query-side uncertainty, and the rescue is gated by query-gap
troughs -- cadence matters as trough-sampling rate (72 ticks,
not the 8-tick quantization), estimator speed matters via
faster dh rise and faster qh decay.

## Answers to the four questions

1. **Characterize the latency curve.** On R = 60, adapt:
   tf1 = 144/160/240 at L = 1/3/7 (replication, K5a), then
   flips = 0 at L = 10/15/20/30 -- the rescue does not come
   late, it does not come at all. Latency is monotone
   non-decreasing in L within every adaptive arm (K5c, the
   monotone-evidence-bar theorem: dec == 1 is pointwise
   monotone-decreasing in L at fixed estimator state, and the
   EWMA trajectory is L-independent). tf2 = 0 everywhere: every
   rescue is a single clean flip, no re-flips. On the control
   cells: no flips anywhere on R = 21/82 (no harmful shift);
   on R = 120 (same regime as R = 60, different seed, D32 = 1)
   adapt flips at tf1 = 176/192/192/192/208 for L = 7/10/15/20/30
   -- high-L flip existence is trough-realization-dependent,
   not a hard architectural boundary.

2. **Why does latency grow with L?** The flip rule reuses
   nr_decide: eager -> lazy needs lazy-decisive,
   L*plod < plon, i.e. (L+1)*qhi < dlo. Three separable
   contributions, each isolated by an arm:
   (a) **Evidence bar (dominant):** the (L+1) multiplier falls
   on qhi, the upper query bound. eq spikes on every bursty
   query arrival, so the rescue waits for a query-gap trough
   deep enough that (L+1)*qhi < dlo; larger L needs deeper
   troughs, hence later (or never). Steady-state analysis on
   this cell: dlo -> 1024, qh -> ~80, so steady-state flips
   need L <= 11; beyond that only transient/trough flips.
   (b) **Checkpoint grid (trough sampling, not quantization):**
   fastchk (8-grid superset) flipped at 168 where adapt flipped
   at 240 -- 72 ticks earlier, far outside the 8-tick
   quantization bound in the frozen prediction. The 8-grid
   sampled a trough at 168 that the 16-grid missed (adapt's
   evaluations at 160/176 saw qhi too high). Cadence matters as
   trough-sampling rate. The prediction's qualifier ("absent
   trough flicker") was the operative one: flicker dominates.
   (c) **Estimator speed:** fastewma flips at tf1 = 144 for
   L = 1, 7, 10 alike. At e = 144 its dh = 905 (vs 675) and
   qh = 14 (vs 52): faster dh rise toward the true drift rate
   plus faster decay of pre-shift query mass. The a priori
   worry (wider transient eq intervals under faster EWMA) did
   not bind on this cell.
   The quirk contributes nothing: guard (data-driven eager
   commit at tc = 96, no quirk) shows tick-identical tf1/flips/
   fdir at L = 3/7/10, including the never-flip at L = 10 (K7).

3. **Can latency be reduced? Yes, substantially.**
   Scoreboard on R = 60 at L = 7 (J = rb + rf*L; fixed lazy =
   112, fixed eager = 133): adapt 142, guard 147, **fastchk
   118**, **fastewma 102**. Halving post-shift cadence restores
   a positive rescue value (118 < 133); doubling EWMA speed
   makes fastewma the best of all six arms (102 < 112). At
   L = 10: adapt/fastchk 134 (never flip), guard 142,
   **fastewma 132** < eager 133 -- the only arm with a positive
   rescue value there. At L = 1 all three adaptive variants
   tie at 42 (the flip already fires at the first post-shift
   checkpoint; nothing to gain).

4. **Is there an L where the flip comes too late to matter?**
   Yes, and past it the flip stops coming entirely (on this
   cell). L = 7: J_adapt = 142 > 133 = J_eager (replication,
   K6a). L = 10: J_adapt = 134 > 133 (theorem, K6b) with
   flips = 0 -- the rescue is absent, not late; adapt =
   eager + 1 commit restamp (rs = 1 + (D - Dc) = 134).
   L = 15/20/30: same 134. Rescue value V(L) = J_eager -
   J_adapt: 91/59/-9/-1/-1/-1/-1 at L = 1/3/7/10/15/20/30.
   (Caveat: R = 120 flips at L = 30, so the never-flip
   boundary is seed-dependent; the monotone theorem and the
   L <= 11 steady-state bound are the portable claims.)

## Kill-bar adjudication

| Bar | Status | Detail |
|-----|--------|--------|
| K1 prereg order | PASS | prereg d8d697a07 -> implementation aaee920e4; no implementation file in prereg commit |
| K2 toolchain | PASS | safebin PATH, no python3/python, znc sha256 verified in-script |
| K3 determinism | PASS | build clean, exit 0, stderr empty, 3/3 byte-identical (b81f6080...), 72 CELL lines |
| K4 anchoring | PASS | cross-arm (D,Q) identical (18 arms x 4 cells); fixed-arm identities; splits show the shift; structural accounting on all 64 adaptive lines; lc = 0 everywhere |
| K5a replication | PASS | 20 adapt/guard lines byte-identical to parent frozen run (delta is surgical; no znc rename miscompile) |
| K5b quirk in new arms | PASS | fastchk/fastewma tc = 32, cm = 2, Dc = 0 on all D32 = 0 cells at L = 1/7/10 |
| K5c monotone latency | PASS | flips(Lb)>=1 => flips(La)>=1 and tf1(La)<=tf1(Lb) for every consecutive L pair in every adaptive arm, R = 60 |
| K6a too-late repl. | PASS | R = 60: J_adapt(7) = 142 > 133 = J_eager |
| K6b too-late ext. | PASS | R = 60: J_adapt(10) = 134 > 133 = J_eager (flips = 0 case) |
| K7 quirk exonerated | PASS | R = 60, L = 3/7/10: tf1/flips/fdir identical guard vs adapt, including never-flip at L = 10 |
| K8 cadence | PASS | R = 60, L = 1/7/10: tf1_fastchk <= tf1_adapt (144/168/0 vs 144/240/0); flips whenever adapt flips; tf1 >= 136 |
| K9a fastewma | PASS | R = 60 fastewma L = 1: flips = 1 (tf1 = 144) |
| K10 hygiene | PASS | ASCII-only, no world literals, one fn main, reused sources unmodified, da_learn.zag untouched, local commits with explicit pathspecs, never pushed |

## Tested findings

1. **The latency curve has a cliff, not just a slope.**
   tf1_adapt = 144/160/240 at L = 1/3/7, then flips = 0 for
   L >= 10 on R = 60. The prereg's steady-state bound
   (L <= 11 feasible) is consistent: the realized troughs at
   240/256 cleared L = 7 (needed qhi < ~128) but not L = 10
   (needed qhi < ~93).
2. **Rescue latency is a flip-rule property.** K7 holds
   exactly, including the never-flip case: guard's
   data-driven eager commit (tc = 96, Dc = 3) is rescued (or
   not) at tick-identical times as the quirk's zero-data
   commit. Commit history does not affect rescue timing.
3. **Cadence buys trough sampling, not quantization.**
   fastchk at L = 7: tf1 = 168 vs 240 (J 142 -> 118). The
   72-tick gain refutes the 8-tick quantization story and
   confirms trough-gating: the rescue waits for query-gap
   troughs, and denser checkpoint sampling catches troughs
   the 16-grid misses.
4. **Estimator speed dominates at high L.** fastewma flips at
   the first post-shift checkpoint (tf1 = 144) for L = 1, 7,
   10; at L = 7 its eager stint is rs = 22, od = 10 --
   field-comparable to adapt at L = 1. J = 102 beats fixed
   lazy (112), the only arm to do so.
5. **The too-late boundary is L = 7 on this cell; L >= 10 is
   never-flip.** V(L) = 91/59/-9/-1 at L = 1/3/7/10.
   fastewma is the only arm with V(10) > 0 (132 < 133).
6. **High-L flip existence is seed-dependent.** R = 120 (same
   regime, D32 = 1) flips at L = 30 (tf1 = 208); R = 60 never
   flips at L >= 10. Portable claims are the monotone
   theorem (K5c) and the steady-state bound, not the exact
   cliff location.

## Honest scope limits

- One seed per cell (R = 60's trough realization determines
  the cliff location); the R = 120 contrast shows
  seed-dependence but two seeds are not a distribution.
- One shift per episode at tick 128 (inherited); multiple
  shifts and gradual drift remain untested.
- The latency-reduction variants were tested only where the
  rescue matters (R = 60 L = 1/7/10); their behavior on other
  cells is characterized by K4c accounting, not barred.
- Whether the flip threshold *should* scale with L (a
  threshold redesign) was explicitly a non-goal; this lane
  characterizes the inherited rule.
- L is caller-stated, not measured (inherited).
- The stale-data facet of the degenerate interval remains
  untested (inherited non-goal).

## Recommendations

1. **Treat rescue latency as a first-class design variable.**
   The flip rule's evidence bar ((L+1)*qhi < dlo) makes
   rescue latency grow superlinearly in effect: linear tf1
   growth to L = 7, then a never-flip cliff. Any future
   flip-threshold work should target the query-side
   uncertainty term (qhi), which gates the rescue, not the
   drift estimate.
2. **Estimator speed is the highest-leverage latency lever
   tested** (tf1 240 -> 144, J 142 -> 102 at L = 7), well
   above cadence (240 -> 168, J 142 -> 118). If a future lane
   revisits the EWMA weight, the tradeoff to characterize is
   transient interval width vs mean-tracking speed across
   seeds, since this lane tested one seed.
3. **Do not read the L = 10 never-flip as architectural.**
   R = 120 flips at L = 30. The cliff location is a property
   of the realized query-gap trough process; the portable
   results are K5c (monotonicity), K7 (quirk exoneration),
   and the (L+1)*qhi < dlo mechanism.
4. **Keep the K5a replication pattern** for future
   copy-plus-delta lanes: byte-comparing the overlapping
   sweep against the parent's frozen run caught (would catch)
   both accidental behavior changes and znc name-dependent
   miscompiles in one check.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0);
  pinned znc znc_linux_x86_64_abed8aa1 (sha256-verified
  in-script: 498abcb5...); no Python invoked at any point.
  Output analysis via grep/cmp/awk/shell only. fl_posthoc.sh
  is labeled post-hoc analysis, not a bar re-adjudication:
  it prints finding tables on the frozen data and must not
  move any frozen bar. (Posthoc display note: its lazy-J row
  prints 0 because the lazy CELL line carries L = -1 while
  the table passes the column L; the bars never use that
  path. True J_lazy on R = 60 is 14 + 14*L: 28/56/112/154
  at L = 1/3/7/10.)
- No new seed probe: cells inherited from SPEC-COLD-START's
  frozen data; D32 = 0 re-confirmed by K5b (tc = 32, Dc = 0
  in all four adaptive arms on R = 21/60/82).
- Git: `/usr/bin/git` directly (safebin git symlink breaks
  writes per AGENTS.md); explicit pathspecs; commits local,
  never pushed. Commit order on the lane dir: d8d697a07
  (PREREG + NAMECHECK) -> aaee920e4 (implementation). No
  amendments; no post-implementation bar changes.
- `da_learn.zag` not modified (separate lane only, per task).
- fl_spec.zag is a minimal documented delta on the parent's
  cs_spec.zag ([FL-DELTA] markers: pol-5 post-shift cadence
  via hoisted cres flag, pol-6 7/8 EWMA via hoisted ewa/ewd
  weights, pol-5/6 naming and adapt/apol plumbing;
  [FL-RENAME] cs_ -> fl_; the estimator base form, margin
  test, commit rule, flip rule, guard, and pol-3 code are the
  parent's, unchanged; pol 3 dormant, not swept). The
  parent's cs_spec.zag is byte-unmodified in its own lane
  (K10). For pol in {0,1,2,4} the tick dynamics are
  unchanged, verified by K5a byte-identity.
- Repro: `./fl_build.sh` assembles the binary, builds with
  the pinned znc, runs 3x (byte-identity + kill-bar
  adjudication); `./fl_posthoc.sh` prints the finding tables
  on the frozen data. All sources and logs are in this lane
  directory.
