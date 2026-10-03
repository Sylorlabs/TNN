# SPEC-COLD-START: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_cold_start/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-FAIL (K5)**

## Summary

This lane tested the cold-start quirk disclosed by SPEC-ABSTENTION-TRAP:
with (dh,ed) = (0,0) the inherited margin test's price interval
degenerates to {0}, making any L >= 1 eager-decisive -- a zero-data
eager commit at e = 32. 40 episodes (4 regime cells x 10 arms: fixed
lazy, fixed eager, adapt pol 2 and guard pol 4 at L in {0,1,3,7}),
one binary, pure Zag, safebin-built, 3/3 byte-identical (sha256
59e04ecd5e0a33fddc1a8daed2f879098150b74b1683aabea98f1af6fdd01c6d).

The guard arm (pol 4) is the lane's experimental delta: identical to
adapt in every respect except that a dec = 2 (eager-decisive) outcome
is not committed while dh = 0 and ed = 0 (the degenerate {0} price
interval); the episode stays undecided, falling through to
budget-default at e = 128. Everything else (EWMA, margin test, flip
rule, arrival mechanics, seeds) is the parent's, unchanged; the
parent's at_spec.zag is byte-unmodified (K8) and superseded here by
copy-plus-delta (cs_spec.zag, [CS-DELTA] markers). Cells were
engineered for D32 = 0 (zero drifts in ticks 0..31) by the pre-prereg
seed probe, so the quirk fires by construction on CS0/CS1/CS2; CS3
carries the same regime as CS1 with D32 = 1 as a guard-purity
control.

**Headline:** the quirk is real and fires exactly as disclosed, and
the harm is real but bounded: on the lazy-optimal cell at L = 1 the
guard saved 14 cost units (42 -> 28) against the quirk's
wrong-direction eager commit. But the preregistered K5 bar is FAILED,
and the failure is a bar-drafting error, not a mechanism defect:
K5 demanded end-of-episode sel = 1 on CS1 while preregistered K7a
demanded the flip rule rescue the same episodes to sel = 0 -- the two
clauses are mutually unsatisfiable on R = 60. The quirk itself (the
actual scientific claim: tc = 32, cm = 2, Dc = 0, degenerate
snapshot) is confirmed 9/9. The refined finding is sharper than the
bar it replaced: the quirk is a zero-data *prior* (eager), the guard
is a zero-data *prior* (abstain/lazy), and neither dominates -- the
flip rule bounds either wrong prior's damage, with rescue latency
growing in L.

## The K5 failure (root cause)

Frozen K5 required, on R in {21,60,82} for L in {1,3,7}: adapt
tc = 32, cm = 2, sel = 1, Dc = 0, dh = dlo = dhi = pnum = phin = 0,
phid >= 1. Measured on R = 60 (CS1): tc = 32, cm = 2, Dc = 0, and
the full degenerate snapshot exactly as disclosed -- but sel = 0,
not 1. The episode committed eager at e = 32 with zero data (the
quirk fired), then the inherited opposite-decisive flip rule moved
it to lazy post-shift (flips = 1, tf1 = 144/160/240 for L = 1/3/7,
fdir = -1, final sel = 0). cm = 2 still records the eager commit;
sel is end-of-episode state.

The error: K5's sel = 1 clause described commit-time state, but the
CELL line reports end-of-episode state, and frozen K7a *required*
flips >= 1 and final sel = 0 on exactly these R = 60 episodes. K5
and K7a as written cannot both be satisfied on CS1 -- a drafting
inconsistency in the prereg, found by the bar itself. The mechanism
is not defective (K4c structural accounting passed; the flip is the
inherited, preregistered rescue); the bar was over-specified. What
survives, stronger: **the quirk is a commit-time event** (tc = 32,
cm = 2, Dc = 0, dh = dlo = dhi = pnum = phin = 0, phid = 1 --
confirmed 9/9 on all D32 = 0 cells, with query data present,
Qc = 5/1/2), while sel is post-commit state owned by the flip rule.

## Answers to the four questions

1. **Characterize the quirk? Confirmed exactly as disclosed.**
   9/9 adapt L in {1,3,7} lines on the D32 = 0 cells show tc = 32,
   cm = 2, Dc = 0, dh = dlo = dhi = pnum = phin = 0, phid = 1: the
   {0} price interval treated as decisive for every L >= 1, at the
   first checkpoint, with zero drift observations. Query data does
   not prevent it (Qc = 5, 1, 2 across the three cells; phid comes
   from maxi(qlo,1)). L = 0 never goes eager anywhere (sel = 0,
   cm != 2 on all four cells; cm = 0 budget-default on the
   D32 = 0 cells).
2. **Is it a real problem? Yes, measured, L-selective, flip-bounded.**
   On CS1 (sparse -> drift-dense, lazy-optimal post) at L = 1:
   J_adapt = 42 vs J_guard = 28 -- the quirk's wrong-direction
   eager commit cost 14 (50% more), via 22 restamps during the
   e = 32..144 eager stint before the flip rescued it. At L = 3 the
   rescue is near-complete (74 vs 75); at L = 7 the rescue came too
   late (tf1 = 240, rs = 118) and adapt (142) underperformed even
   fixed eager (133) and fixed lazy (112) -- the quirk plus slow
   flip was worse than either fixed policy there (finding, not a
   bar). Flip rescue latency grows with L (tf1 = 144/160/240),
   because larger L needs stronger evidence to go lazy-decisive.
3. **Should the margin test require minimum data? The guard is safe
   but not a strict improvement -- it is a tradeoff, not a fix.**
   Mechanics (K6): the guard blocked 9/9 degenerate eager commits
   (no guard line with cm = 2 and Dc = 0; every guard eager commit
   has Dc >= 1); it never binds at L = 0 (field-identical to adapt
   on all 4 cells) and never binds where drift data exists
   (field-identical to adapt at every L on CS3, including identical
   J = 11/22/44/94). It is a pure degenerate-case intervention.
   But it does not dominate: it wins on CS1-L1 (28 < 42) and
   CS0-L1 (8 < 13) and loses on CS2 at every L (19 vs 28/56/112)
   and CS0-L3/L7 (13 vs 16/32), where its abstention paid refusals
   at (1+L) each while waiting for data that never became decisive
   (guard hit budget-default com = 2 on CS0/CS2 at all L >= 1).
   The guard also commits on real evidence: on CS1-L3,7 it
   committed eager at tc = 96 with Dc = 3 (data-driven, pre-shift),
   then flipped post-shift at the same ticks as adapt (160/240).
4. **Or is zero-data eager actually correct? Sometimes -- it is a
   prior, and priors pay when they match the world.** Where the
   world is eager-optimal (CS2: 19 vs 28 at L = 1, wider at
   L = 3,7) or genuinely sparse (CS0-L3,7: 13 vs 16/32), the
   quirk's zero-data eager commit beats the guard's abstention.
   With zero data at e = 32 the right choice is unknowable; the
   experiment measures the two priors' costs, and neither
   dominates. The flip rule is what bounds either wrong prior's
   damage (adapt never approached fixed-eager's 133 on CS1-L1).

## Kill-bar adjudication

| Bar | Status | Detail |
|-----|--------|--------|
| K1 prereg order | PASS | probe fc4f4cb2b -> PREREG e414d0733 -> NAMECHECK 569a6b312 -> implementation b077eff00; no implementation file in prereg commit |
| K2 toolchain | PASS | safebin PATH, no python3/python, znc sha256 verified in-script |
| K3 determinism | PASS | build clean, exit 0, stderr empty, 3/3 byte-identical (59e04ecd...), 40 CELL lines |
| K4 anchoring | PASS | cross-arm (D,Q) identical; fixed-arm identities; splits show the shift (CS1/CS3 Dpost = 128, CS2 Qpost = 128, CS0 sparse); structural accounting on all 32 adapt+guard lines; lc = 0 everywhere (pol 3 dormant) |
| K5 quirk | **FAIL** | quirk-core confirmed 9/9 (tc = 32, cm = 2, Dc = 0, degenerate snapshot); sel = 1 clause violated on R = 60 (sel = 0 after the preregistered K7a flip); K5/K7a mutually unsatisfiable on CS1 -- bar-drafting error |
| K6a guard blocks | holds | 9/9 degenerate commits blocked; every guard cm = 2 has Dc >= 1 |
| K6b L0 identity | holds | guard field-equal adapt at L = 0 on all 4 cells |
| K6c CS3 identity | holds | guard field-equal adapt at every L on R = 120 (J identical: 11/22/44/94) |
| K7a wrong-direction | holds | R = 60 adapt L in {1,3,7}: flips = 1, sel = 0, fdir = -1; tf1 = 144/160/240 |
| K7b harm | holds | R = 60 L = 1: J_guard = 28 < J_adapt = 42 |
| K7c benefit | holds | R = 82 L = 1: J_adapt = 19 < J_guard = 28 (wider at L = 3,7: 19 vs 56/112) |
| K7d default | holds | R = 21 L in {3,7}: J_adapt = 13 < J_guard = 16/32 |
| K8 hygiene | holds | ASCII-only, no world literals, one fn main, reused sources unmodified, da_learn.zag untouched, local commits with explicit pathspecs, never pushed |

"holds" = the preregistered condition was evaluated on the frozen
3/3-byte-identical data and is satisfied; not claimed as a passed
kill bar since the lane verdict is FAIL.

## Tested findings

1. **The quirk is a commit-time event with the exact disclosed
   signature.** 9/9: tc = 32, cm = 2, Dc = 0, dh = dlo = dhi =
   pnum = phin = 0, phid = 1. It fires with query data present
   (Qc = 5/1/2); the drift side alone degenerates the interval.
   sel is post-commit state and must not be barred at commit-time
   granularity.
2. **Harm is concentrated at small L and bounded by the flip.**
   CS1-L1: 42 -> 28 for the guard. The eager stint's cost is the
   restamps before rescue (rs = 22/38/118 at L = 1/3/7); rescue
   latency grows with L (tf1 = 144/160/240). At L = 7 the rescue
   was too late and adapt (142) lost to fixed eager (133) and
   fixed lazy (112).
3. **The guard is behaviorally pure.** Zero delta at L = 0 and on
   the D32 = 1 control cell; blocks only the degenerate commit.
   Where it abstains through the budget it runs lazy (cm = 0);
   where data arrives it commits on evidence (R = 60 L = 3,7:
   eager at tc = 96, Dc = 3).
4. **Neither zero-data prior dominates.** Scoreboard (J, lower is
   better): CS0-L1 guard 8 < 13; CS0-L3,7 quirk 13 < 16/32;
   CS1-L1 guard 28 < 42; CS1-L3 ~tie 75 vs 74; CS2 quirk 19 <
   28/56/112 at L = 1/3/7. The right zero-data default depends on
   the world's realized price, unknowable at e = 32.
5. **The stale-data facet is real by construction but untriggered
   here.** (dh,ed) = (0,0) also holds when ancient drifts fully
   decay (~129 drift-free ticks for ed); the 128-tick pre-shift
   window cannot produce it, so this facet is noted, not tested.

## Honest scope limits

- One shift per episode at tick 128 (inherited); multiple shifts,
  pre-commit shifts, and gradual drift remain untested.
- Four cells, one drift/query family; D32 = 0 was realized by seed
  selection, not sampled from a cold-start distribution -- the
  scoreboard is conditional on the quirk firing, not a base rate.
- K5's FAIL is a bar-drafting error (K5/K7a inconsistent on CS1);
  the quirk confirmation stands, but the lane verdict is FAIL per
  the frozen bars.
- The stale-data facet of the degenerate interval (decayed ancient
  drifts) was not exercised and remains untested.
- L is caller-stated, not measured (inherited).
- The guard's post-128 behavior is terminal abstention (pol-2-like);
  guard+recheck interaction was not tested (pol 3 dormant).

## Recommendations

1. **Do not silently adopt the guard as a permanent margin-test
   rule.** It is safe (K6b/c: zero behavioral change where data
   exists) but not a strict improvement (K7c/d: the quirk wins
   where eager is right). Changing the commit rule alters
   honest-commit semantics the same way the recheck altered
   honest-abstention semantics: bank for Micah's governance
   decision with this report as evidence.
2. **Refined K5 for any follow-up lane:** bar commit-time fields
   only (tc, cm, Dc, snapshot interval fields); never bar
   end-of-episode sel where the flip rule is in play.
3. **Open a flip-latency lane.** tf1 = 144/160/240 across L shows
   rescue latency growing with L; at L = 7 the rescue was too late
   to beat fixed policies. Whether the flip threshold should scale
   with L is untested.
4. **Keep the probe-inversion pattern** (D32 = 0 selection) for
   cold-start studies; it made the quirk fire deterministically.
5. **Test the stale-data facet** (129+ drift-free ticks
   re-degenerating the interval) in a dedicated lane with a longer
   pre-shift window.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0); pinned
  znc znc_linux_x86_64_abed8aa1 (sha256-verified in-script:
  498abcb5...); no Python invoked at any point. Output analysis via
  grep/cmp/awk/shell only. cs_posthoc.sh is labeled post-hoc
  analysis, not a bar re-adjudication: it evaluates K6/K7/K8 as
  "holds" on the frozen data and must not move any frozen bar.
- Seed probe (probe.zag) ran pre-prereg, examined arrival counts
  only, and selected R = 21/60/82 (D32 = 0) and R = 120
  (D32 = 1) by the frozen lowest-R rule on disjoint ranges.
- Git: `/usr/bin/git` directly (safebin git symlink breaks writes
  per AGENTS.md); explicit pathspecs; commits local, never pushed.
  Commit order on the lane dir: fc4f4cb2b (probe) -> e414d0733
  (PREREG) -> 569a6b312 (NAMECHECK) -> b077eff00 (implementation).
  No amendments; no post-implementation bar changes. The K5
  failure was not re-barred: verdict stands as BUILD-FAIL.
- `da_learn.zag` not modified (separate lane only, per task).
- cs_spec.zag is a minimal documented delta on the parent's
  at_spec.zag ([CS-DELTA] markers; parent file byte-unmodified,
  verified in K8): pol-4 minimum-data guard as a hoisted blk flag
  in cs_checkpoint, pol-4 naming/plumbing. For pol in {0,1,2} the
  tick dynamics are unchanged; pol 3 inherited dormant.
- Repro: `./cs_build.sh` assembles the binary, builds with the
  pinned znc, runs 3x (byte-identity + kill-bar adjudication);
  `./cs_posthoc.sh` prints the finding tables on the frozen data.
  All sources and logs are in this lane directory.
