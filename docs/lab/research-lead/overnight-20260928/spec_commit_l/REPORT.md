# SPEC-COMMIT-L: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_commit_l/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (K1-K9 all pass)**

## Summary

This lane answered the frozen next question from SPEC-L-DISCIPLINE:
whether the pre-shift commit rule, the last remaining L-entry point
besides J accounting, can also run L-free. 88 episodes (4 inherited
regime cells x 22 arms: fixed lazy, fixed eager, fix2 / noeg /
coml1 / comlg / comnoeg in {1,3,7,10}), one binary, pure Zag,
safebin-built, 3/3 byte-identical (sha256
84e7f53e5ee04718585a91741cf8b472b3aba2a767474fc9db7554f3a8cc17b5).

The three new arms are the lane's experimental deltas, all running
the parent's noeg L-free flip discipline and differing only in the
pre-shift commit rule (com == 0 branch): pol 13 "coml1" calls
nr_decide with L := 1 (both directions L-free; quirk preserved);
pol 14 "comlg" is coml1 plus the minimum-data guard (dec == 2
suppressed while (dh,ed) = (0,0); quirk blocked, data-driven eager
kept); pol 15 "comnoeg" drops the commit rule's eager direction
entirely (lazy-only `plod < plon`; quirk channel closed by
construction). Everything else (EWMA, flip mechanics, guard and
pol-3 code, arrival mechanics, seeds) is the parent's, unchanged:
32 fix2/noeg lines are byte-identical to the parent's frozen run
(K4d).

**Headline: the commit rule's L is load-bearing, and usefully so --
the opposite of the flip discipline's L.** Removing L from the
commit rule changes behavior observably (K6a: on R = 120 the
L = 7/10 eager commit at tc = 112 disappears; coml1 sits at
cm = 0/tc = 128 like L = 1/3 at every L), and the change is
J-harmful at high L under the caller-stated cost ratio (K7a:
J = 78 -> 88 at L = 7, 93 -> 121 at L = 10). The L-driven eager
commit front-ran the post-shift drift-dense regime, trading rebuilds
(1 each) for refusals (L each). Under L-free scoring it looks
harmful (J' = 48 -> 22), which is exactly the diagnostic tension
J' is for. The quirk, examined explicitly, is L-invariant: it fires
identically under L := 1 (K5a/K5c), so an L-free commit rule must
still pick a quirk policy -- and under L-free commit the eager
direction does zero data-driven work anywhere tested (K8b: comlg ==
comnoeg modulo P= on all 16 cell/L pairs): it is purely the quirk
channel. Recommendation: keep L in the commit rule by the same
definitional right as J accounting; do not extend the L-free program
to it.

## Answers to the four questions

1. **Is the commit rule's L-dependence load-bearing? Yes.**
   K6a: coml1 (L := 1 commit) on R = 120 is dynamically identical
   to the parent's frozen noeg L = 1 line (mod P=/L=) at every L:
   cm = 0, tc = 128, flips = 0, rb = 11, rf = 11. The parent's
   noeg L = 7/10 lines sit at cm = 2/tc = 112. Removing L from the
   commit rule therefore changes observable behavior: the
   data-driven eager commit at tc = 112 exists only because of L.
   (Contrast the flip discipline, where removing L changed nothing.)
2. **Was the L-driven behavior economically useful? Yes, under J.**
   K7a: J_coml1(120,L) = 11 + 11L exactly (22/44/88/121) vs the
   frozen J_noeg(120,7) = 78 and J_noeg(120,10) = 93. The L-driven
   eager commit saved 10 units at L = 7 and 28 at L = 10: it
   committed eager at tc = 112 on pre-shift evidence, then rode the
   first 32 ticks of the post-shift drift-dense regime rebuilding
   (rs = 38) instead of refusing at L each, before the L-free flip
   rule rescued it to lazy at tf1 = 160. Under J' the same commit
   looks harmful (48 vs 22 flat) -- the expected tension: J' prices
   refusals at 1, so any refusal-avoidance looks wasteful; the
   caller stated refusals cost L, and the commit rule is where that
   price is actually spent.
3. **Quirk implications, explicitly.** The quirk is L-invariant
   (frozen analysis, confirmed): with (dh,ed) = (0,0), phin = 0 and
   phid >= 1, so `1*phid > phin` fires exactly as `L*phid` did for
   every L >= 1. K5a: coml1 reproduces the exact quirk signature
   (tc = 32, cm = 2, Dc = 0, dh = dlo = dhi = phin = 0, phid = 1)
   on R = 21/60/82 at every L; K5c: coml1 == noeg (mod P=) on all
   three quirk cells -- the L-free commit changes nothing where the
   quirk dominates. An L-free commit rule must still choose what to
   do about the quirk, and the scoreboard (K7c, J, lower better)
   shows neither zero-data prior dominates, under the L-free flip
   discipline as under adapt:
   - R = 21 (sparse): guard wins at L = 1 (8 < 13); quirk wins at
     L = 3/7/10 (13 < 16/32/44).
   - R = 60 (harm cell): guard wins at L = 1 (28 < 42) and L = 3
     (56 < 62); quirk wins at L = 7 (102 < 112) and L = 10
     (132 < 154). The guard arm never commits (cm = 0/tc = 128,
     Dc = 5) and never flips; the quirk arm commits eager at 32
     and is rescued at tf1 = 144.
   - R = 82 (query-dense, eager-right): quirk wins at every L
     (19 < 28/56/112/154).
   The quirk is a zero-data eager prior; the guard is a zero-data
   abstain prior; the flip rule bounds either wrong prior's damage.
   Same moral as SPEC-COLD-START, now measured under the L-free
   flip discipline.
4. **Does the eager direction do data-driven work under L-free
   commit? No -- nowhere tested.** K8b: comlg == comnoeg (mod P=)
   on all 16 cell/L pairs. comlg keeps `phid > phin` wherever data
   exists; comnoeg drops eager entirely; they are identical
   everywhere, so `phid > phin` never fired with data on any of the
   4 cells at any L. The only eager commits under L-free commit
   were the quirk's zero-data ones (coml1). The commit rule's eager
   direction, once L is removed, is purely the quirk channel.

## Kill-bar adjudication

| Bar | Status | Detail |
|-----|--------|--------|
| K1 prereg order | PASS | prereg 060aae0b8 -> implementation ad3dc47cd; no implementation file in prereg commit |
| K2 toolchain | PASS | safebin PATH, no python3/python, znc sha256 verified in-script |
| K3 determinism | PASS | build clean, exit 0, stderr empty, 3/3 byte-identical (84e7f53e...), 88 CELL lines |
| K4 anchoring | PASS | cross-arm (D,Q) identical (22 arms x 4 cells); fixed-arm identities; splits show the shift; structural accounting on all 80 adaptive lines; lc = 0 everywhere |
| K4d replication | PASS | 32 fix2/noeg lines byte-identical to parent frozen run (delta is surgical) |
| K5a quirk preserved | PASS | coml1: tc=32, cm=2, Dc=0, degenerate snapshot on R=21/60/82 at every L |
| K5b quirk killed | PASS | no comlg/comnoeg line with cm=2 AND Dc=0 on R=21/60/82; no comnoeg cm=2 anywhere |
| K5c quirk identity | PASS | coml1 == noeg modulo P= on R=21/60/82 at every L |
| K6a core | PASS | coml1 == parent noeg L=1 on R=120 (mod P=/L=) at every L: cm=0/tc=128/flips=0/rb=11/rf=11; parent L=7/10 at cm=2/tc=112, so removing L changes behavior |
| K6b guard idle | PASS | comlg == coml1 modulo P= on R=120 at every L |
| K6c no data eager | PASS | comnoeg == coml1 modulo P= on R=120 at every L |
| K7a economics | PASS | J_coml1(120,L) = 11+11L (22/44/88/121) vs J_noeg(120,7)=78, J_noeg(120,10)=93 |
| K7b J' tension | FINDINGS | J'_coml1(120,L) = 22 flat vs J'_noeg(120,7/10) = 48: J-beneficial but J'-harmful |
| K7c quirk scoreboard | FINDINGS | guard wins R=21 L=1, R=60 L=1/3; quirk wins R=21 L>=3, R=60 L>=7, R=82 all L |
| K8a controls | PASS | zero flips on R=21/82 for coml1/comlg/comnoeg at every L |
| K8b eager channel | FINDINGS | comlg == comnoeg (mod P=) 16/16: no data-driven eager work under L-free commit |
| K8c R=60 trace | FINDINGS | coml1: quirk at 32 + rescue at 144; comlg/comnoeg: cm=0/tc=128, Dc=5, no flips |
| K9 hygiene | PASS | ASCII-only, no world literals, one fn main, reused sources unmodified, da_learn.zag untouched, parent lane unedited, local commits with explicit pathspecs, never pushed |

## Tested findings

1. **The commit rule is the economic decision point, and L belongs
   there by definitional right.** The flip discipline decides
   *direction* from evidence (L-free); the commit rule decides
   *whether to pay rebuilds now to avoid refusals later* -- a
   decision that is meaningless without the caller-stated refusal
   price L. Removing L from the commit rule is observably different
   (K6a) and J-worse at high L (K7a). This is the same definitional
   argument that keeps L in J accounting, now with behavioral
   evidence: L in the commit rule does real economic work.
2. **The L-driven eager commit was a front-run, not just a
   mistake.** tc = 112 (pre-shift) eager commit, 38 restamps across
   the shift boundary, flip to lazy at 160. It traded 32 rebuilds
   for 6 refusals: at L = 7 that is +32 -42 = -10 (J 78 vs 88).
   The flip rule being L-free does not erase the commit's value;
   per the parent's recommendation 4, the commit and flip decisions
   stay separate -- this lane does not reintroduce L into the flip
   bar.
3. **Under L-free commit, the eager direction is the quirk and
   nothing else.** 16/16 comlg/comnoeg identities (K8b). Any future
   L-free commit design must therefore decide the quirk question
   explicitly: there is no "data-driven eager" left to preserve
   once L is out. The quirk is not a side effect of L; it is
   orthogonal to it (L-invariant, K5a/K5c).
4. **The quirk scoreboard under the L-free flip discipline
   reproduces the COLD-START moral.** Neither the zero-data eager
   prior (quirk) nor the zero-data abstain prior (guard) dominates:
   the right zero-data default depends on the world's realized
   price, unknowable at e = 32. The flip rule bounds either wrong
   prior (R = 60: rescue at tf1 = 144 in the quirk arm; no rescue
   needed in the guard arm, which simply never commits).

## Honest scope limits

- One seed per cell (inherited); the trough realizations determine
  exact commit ticks, though the line identities are exact.
- One shift per episode at tick 128 (inherited); multiple shifts
  and gradual drift remain untested.
- L swept at {1,3,7,10} only (inherited); L = 0/15/20/30 tails not
  re-swept. L is caller-stated, not measured (inherited).
- The "no data-driven eager work under L-free commit" claim rests
  on 4 cells x 4 L; adversarial cells could in principle make
  `phid > phin` fire with data. The claim is bounded, not general.
- The stale-data facet of the degenerate interval (decayed ancient
  drifts re-degenerating the price interval) remains untested, as
  in SPEC-COLD-START.
- Whether an L-aware flip rule would beat the L-free flip on
  R = 120 at high L is out of scope (the parent lane settled the
  flip discipline as L-free; this lane does not revisit it).

## Recommendations

1. **Keep L in the pre-shift commit rule.** It is load-bearing
   (K6a) and J-beneficial at high L (K7a), by the same definitional
   right as J accounting: the commit decision prices refusals at
   the caller-stated L. Do not extend the L-free program to the
   commit rule.
2. **Keep the flip discipline L-free.** Nothing in this lane
   rehabilitates L in the flip bar (parent recommendation 4
   stands): the commit-side L-dependence is a property of the
   economic commit decision, not evidence the flip needs L.
3. **The quirk stays a governance question.** Guard vs eager-prior
   is a tradeoff under the L-free flip discipline too (K7c); the
   flip rule bounds either wrong prior. Bank with this report as
   evidence; do not silently adopt comlg/comnoeg.
4. **Adopt the working discipline as: L-free flip (noeg/fix2) +
   L-bearing commit + L-bearing J accounting.** L enters exactly
   where prices are spent (commit, accounting), nowhere else.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0);
  pinned znc znc_linux_x86_64_abed8aa1 (sha256-verified
  in-script: 498abcb5...); no Python invoked at any point.
  Output analysis via grep/cmp/awk/sed/shell only. cl_posthoc.sh
  is labeled post-hoc analysis, not a bar re-adjudication: it prints
  finding tables on the frozen data and must not move any frozen bar.
- No new seed probe: cells inherited from SPEC-L-DISCIPLINE's frozen
  data; D32 = 0 re-confirmed by K5a.
- Git: `/usr/bin/git` directly (safebin git symlink breaks writes per
  AGENTS.md); explicit pathspecs; commits local, never pushed. Commit
  order on the lane dir: 060aae0b8 (PREREG + NAMECHECK) ->
  ad3dc47cd (implementation) -> build artifacts -> REPORT.md.
  No amendments; no post-implementation bar changes.
- `da_learn.zag` not modified (separate lane only, per task).
- cl_spec.zag is a minimal documented delta on the parent's
  ld_spec.zag ([CL-DELTA] markers; full diff reviewed before
  build): scl_commit_decide dispatch, pol-14 blk flag,
  nr_decide_ft hoisting for pol 13/14/15, nr_polname names,
  apol/adap wiring. For pol in {0,1,7,10} the tick dynamics are
  unchanged, verified by K4d byte-identity. The parent's
  ld_spec.zag / ld_main.zag are byte-unmodified in their own lane
  (K9).
- Repro: `./cl_build.sh` assembles the binary, builds with the
  pinned znc, runs 3x (byte-identity + kill-bar adjudication);
  `./cl_posthoc.sh` prints the finding tables on the frozen data.
  All sources and logs are in this lane directory.
