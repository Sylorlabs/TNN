# SPEC-L-DISCIPLINE: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_l_discipline/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-PASS (K1-K9 all pass)**

## Summary

This lane answered the frozen next question from SPEC-FLIP-THRESHOLD:
whether L should enter the discipline at all, now that the fixed bar
(`2*qhi < dlo`) takes L only for J accounting and the unchanged eager
direction. 88 episodes (4 inherited regime cells x 22 arms: fixed lazy,
fixed eager, adapt / fix2 / noeg / noj / nol in {1,3,7,10}), one
binary, pure Zag, safebin-built, 3/3 byte-identical (sha256
36d63552f3e3ec5bfd664bc9b40a1043c47c89ce181881bd5c94726fc0781b4b).

The three new arms are the lane's experimental deltas on the parent's
policy layer, everything else inherited unchanged: pol 10 "noeg"
removes L from the flip-path eager-decisive test (`phid > phin`,
equivalently the direction at L = 1); pol 11 "noj" is a pure alias of
pol 7 (fix2 code path, differs only in the P= name), scored post-hoc
with the L-free J' = rb + rf; pol 12 "nol" is a pure alias of pol 10,
also J'-scored. The commit rule (including the quirk), the EWMA, the
grid, and the arrival mechanics are the parent's, byte-identical on
the overlapping sweep (K5a: 32 adapt/fix2 lines byte-identical to the
parent's frozen run).

**Headline:** L is dead weight in the flip discipline. noeg is
byte-identical to fix2 modulo the P= field on all 4 cells at all 4 L
values (16/16, K6 + K8): removing L from the flip-path eager direction
changes nothing observable, because the eager direction never fires
observably on any tested cell (no fdir = 1 flip, no tf2 > 0 in any of
the 88 episodes). And the fix2 advantage is not a scoring artifact:
under L-free scoring, J'_fix2 = 42 flat across L on the harm cell vs
J'_adapt = 42/56/124/134 and J'_eager = 133 (K7b findings). L survives
in exactly two places: J accounting, where it belongs by definition
as the caller-stated cost ratio, and the pre-shift commit rule,
deliberately out of scope, where it IS observably load-bearing
(R = 120: cm = 0 / tc = 128 at L = 1/3 vs cm = 2 / tc = 112 at
L = 7/10, identical across adapt/fix2/noeg).

## Answers to the three questions

1. **Does removing L from the flip-path eager direction change
   behavior? No.** noeg vs fix2: 16/16 CELL lines identical modulo P=
   across R in {21,60,82,120} and L in {1,3,7,10} (K6 on the harm
   cell, K8 on the controls). The flip-path eager direction
   (`L*phid > phin` vs `phid > phin`) never produces an observable
   flip on these cells: every recorded flip in all 88 episodes has
   fdir = -1 (rescue to lazy) and tf2 = 0 everywhere. The L multiplier
   on the eager direction buys nothing observable; the rescue is a
   one-way trip.
2. **Does removing L from J accounting change the conclusions? No.**
   Alias correctness is barred (K7a: noj == fix2 and nol == noeg
   modulo P=, 32/32: the J-free scoring touches no dynamics). The J'
   findings on R = 60: J'_fix2(L) = 42 at every L (od = 10, rs = 22,
   rebuilds = 32: the fixed bar made the whole episode L-independent,
   so only the scoring varied with L), vs J'_adapt = 42/56/124/134 at
   L = 1/3/7/10 and J'_eager = 133. fix2 beats adapt at every L > 1
   and beats eager under L-free scoring, exactly as under J. The
   threshold-redesign win is robust to L-free scoring, not an artifact
   of L-weighting refusals.
3. **Can the whole flip discipline run L-free? Yes, observably.**
   Both flip directions are now L-free: the lazy bar by fix2
   (`2*qhi < dlo`), the eager direction by noeg == fix2 (the
   `phid > phin` test changes nothing). What still takes L: the J
   cost model (by definitional right: L IS the caller-stated refusal
   cost ratio, and J' = rb + rf is just J at the identity multiplier)
   and the untouched pre-shift commit rule, whose L-dependence on
   R = 120 bounds the claim and is the natural next question.

## Kill-bar adjudication

| Bar | Status | Detail |
|-----|--------|--------|
| K1 prereg order | PASS | prereg 17deee8b9 -> implementation 694619e8c -> rename/artifacts 90070ae9f; no implementation file in prereg commit |
| K2 toolchain | PASS | safebin PATH, no python3/python, znc sha256 verified in-script |
| K3 determinism | PASS | build clean, exit 0, stderr empty, 3/3 byte-identical (36d63552...), 88 CELL lines |
| K4 anchoring | PASS | cross-arm (D,Q) identical (22 arms x 4 cells); fixed-arm identities; splits show the shift; structural accounting on all 80 adaptive lines; lc = 0 everywhere |
| K5a replication | PASS | 32 adapt/fix2 lines byte-identical to parent frozen run (delta is surgical) |
| K5b quirk in new arms | PASS | noeg/noj/nol tc = 32, cm = 2, Dc = 0 on all D32 = 0 cells at L = 1/3/7/10 |
| K5c monotone latency | PASS | flips(Lb)>=1 => flips(La)>=1 and tf1(La)<=tf1(Lb) for every consecutive L pair in every adaptive arm, R = 60 |
| K5d L=1 identity | PASS | noeg L = 1 == fix2 L = 1 and nol L = 1 == noj L = 1 modulo P= on all 4 cells |
| K6 eager direction | PASS | noeg == fix2 modulo P= on R = 60 at L = 1/3/7/10: L not load-bearing in the flip-path eager direction |
| K7a alias correctness | PASS | noj == fix2 and nol == noeg modulo P= on all cells/L (32/32): J-free scoring touches no dynamics |
| K7b J' findings | FINDINGS | J'_fix2 = 42 flat vs J'_adapt = 42/56/124/134, J'_eager = 133 on R = 60: fix2 advantage survives L-free scoring |
| K8 control integrity | PASS | noeg == fix2 modulo P= on R = 21/82/120 at all L; zero flips on R = 21/82; R = 120 flips at tf1 = 160 (fdir = -1) for L = 7/10 only |
| K9 hygiene | PASS | ASCII-only, no world literals, one fn main, reused sources unmodified, da_learn.zag untouched, parent lane unedited, local commits with explicit pathspecs, never pushed |

## Tested findings

1. **The flip-path eager direction is observably dead on all tested
   cells.** 16/16 noeg/fix2 line identities (mod P=). The `L*phid`
   multiplier never decides a flip: no eager-direction flip (fdir = 1)
   and no re-flip (tf2 > 0) occurs in any of the 88 episodes. The
   rescue is one-way; the eager direction's L is pure dead weight.
2. **The fix2 win is not a scoring artifact.** J'_fix2(7) = 42 <
   124 = J'_adapt(7); J'_fix2(10) = 42 < 133 = J'_eager. Under L-free
   scoring the margin is, if anything, cleaner: fix2's episode
   dynamics are fully L-independent (od = 10, rs = 22 at every L), so
   J' is flat at 42 while adapt's J' degrades with L (42/56/124/134).
3. **L-free scoring exposes what L was doing to fix2's J.** J_fix2(L)
   = 42/62/102/132 varies with L only because the scoring weights
   refusals by L; the behavior underneath does not vary at all. J' =
   rb + rf is a useful diagnostic: it separates discipline behavior
   from cost-model weighting.
4. **The commit rule is the remaining L-entry point, and it matters
   there.** R = 120: cm = 0 / tc = 128 (never committed) at L = 1/3 vs
   cm = 2 / tc = 112 (eager commit) at L = 7/10, identical across
   adapt/fix2/noeg (K8 findings table). This lane deliberately did not
   touch the commit rule; its L-dependence bounds the "L is purely
   cost-accounting" claim and is the next question.
5. **Control cells are clean.** Zero flips for all four L-discipline
   arms on R = 21/82 at every L; R = 120 flips only where the regime
   matches the harm cell (L = 7/10, tf1 = 160, fdir = -1), identically
   for fix2 and noeg.

## Honest scope limits

- One seed per cell (inherited); the trough realizations determine the
  exact tf1 values, though the line identities are exact, not
  realizations.
- One shift per episode at tick 128 (inherited); multiple shifts and
  gradual drift remain untested.
- The eager direction can fire unobservably while eager-committed
  (want == cur produces no line change); the L-free claim is about
  observable behavior, which is what the discipline's outputs are.
- The L-free eager direction was tested as `phid > phin` (L := 1);
  other L-free forms (e.g. dropping the direction entirely) were not
  tested, though nothing in the data suggests the direction does work
  that needs replacing.
- L swept at {1,3,7,10} only (inherited); the parent's L = 15/20/30
  tail was not re-swept.
- L is caller-stated, not measured (inherited); none of the arms
  estimate the true cost ratio.

## Recommendations

1. **Adopt the L-free flip discipline as the working discipline.**
   Both flip directions now run without the caller-stated L (lazy:
   `2*qhi < dlo`; eager: `phid > phin`, which changes nothing
   observable). The flip decision should not take L as an argument.
2. **Keep L in J accounting.** L is the caller-stated refusal cost
   ratio; the cost model is where it belongs. Keep J' = rb + rf as a
   diagnostic: it separates what the discipline does from how refusals
   are priced.
3. **The commit rule is the next L question.** R = 120 shows L
   changing the commit outcome (cm = 0 vs cm = 2). A follow-up lane
   should test whether the pre-shift commit rule needs the
   caller-stated L, with the quirk implications examined explicitly
   (the quirk fires through the commit rule's eager direction).
4. **Do not reintroduce L into the flip bar on commit-side grounds.**
   The commit decision and the flip decision are separate; the
   commit's L-dependence does not rehabilitate L in the flip
   discipline.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0);
  pinned znc znc_linux_x86_64_abed8aa1 (sha256-verified
  in-script: 498abcb5...); no Python invoked at any point.
  Output analysis via grep/cmp/awk/sed/shell only. ld_posthoc.sh
  is labeled post-hoc analysis, not a bar re-adjudication: it prints
  finding tables on the frozen data and must not move any frozen bar.
- **sld_ rename (implementation detail, not a bar change).** The first
  build failed with znc arity errors (`ld_emit_cell`/`ld_episode`
  expected 13/8 args): the `ld_` function prefix collides with the
  grandparent spec_lazy_default lane's `ld_*` namespace, which is
  assembled into the same binary with different signatures. Fixed by
  renaming this lane's functions to `sld_*` before any run was
  produced; the prereg's "[LD-RENAME] ft_ -> ld_" note describes the
  rename intent, and no frozen bar references the function prefix.
  The failed build is preserved in the audit trail (implementation
  commit 694619e8c carries the ld_ names; the rename landed in
  90070ae9f alongside the passing artifacts).
- No new seed probe: cells inherited from SPEC-FLIP-THRESHOLD's frozen
  data; D32 = 0 re-confirmed by K5b.
- Git: `/usr/bin/git` directly (safebin git symlink breaks writes per
  AGENTS.md); explicit pathspecs; commits local, never pushed. Commit
  order on the lane dir: 17deee8b9 (PREREG + NAMECHECK) ->
  694619e8c (implementation) -> 90070ae9f (sld_ rename + build
  artifacts). No amendments; no post-implementation bar changes.
- `da_learn.zag` not modified (separate lane only, per task).
- ld_spec.zag is a minimal documented delta on the parent's
  ft_spec.zag ([LD-DELTA] markers: nr_decide_ft hoisted egl flag for
  pol 10/12, lzmult = 1 for pol 10/11/12; [LD-RENAME] ft_ -> sld_
  with the collision note; nr_decide itself, the commit rule, the
  EWMA, the grid, and pol-3 code are the parent's, unchanged; pol 3
  dormant, not swept). The parent's ft_spec.zag / ft_main.zag are
  byte-unmodified in their own lane (K9). For pol in {0,1,2,7} the
  tick dynamics are unchanged, verified by K5a byte-identity.
- Repro: `./ld_build.sh` assembles the binary, builds with the
  pinned znc, runs 3x (byte-identity + kill-bar adjudication);
  `./ld_posthoc.sh` prints the finding tables on the frozen data.
  All sources and logs are in this lane directory.
