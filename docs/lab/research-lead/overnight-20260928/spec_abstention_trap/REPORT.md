# SPEC-ABSTENTION-TRAP: REPORT

**Lane:** docs/lab/research-lead/overnight-20260928/spec_abstention_trap/
**Date:** 2026-10-03
**Status:** Non-ledger (claim minting paused). Local commits only, never pushed.
**Verdict: BUILD-FAIL (K5b)**

## Summary

This lane mapped the abstention trap left open by SPEC-REGIME-CHANGE:
pre-shift budget-default (com = 2) is terminal, so an episode that
abstains before the shift cannot react when the regime changes. 60
episodes (6 regime cells x 10 arms: fixed lazy, fixed eager, adapt
pol 2 and recheck pol 3 at L in {0,1,3,7}), one binary, pure Zag,
safebin-built, 3/3 byte-identical (sha256
5258aa3f2f3574e121ad0e90e23af425d54a48bfdbdd67654196417e9775163f).

The recheck arm (pol 3) is the lane's experimental delta: identical
to adapt pre-shift, except budget-default at e = 128 is deferred,
not terminal. At each post-shift checkpoint it re-runs the inherited
margin test and commits on decisive evidence (lc = 1 flags the late
commit). Everything else (EWMA, margin test, flip rule, arrival
mechanics, seeds) is the parent's, unchanged; T3 (R = 1) is
seed-identical to parent R1 and its pol-0/1/2 lines are byte-equal to
the parent's (K4c), validating the rebuild.

**Headline:** the trap is real, and the recheck avoids it cleanly.
But the preregistered boundary hypothesis (abstention counts monotone
in pre-shift density) is FALSIFIED: K5b failed, n_abstain = 2 on both
the sparse end (T1) and the dense end (T5). Root cause below. The
refined characterization is sharper than the hypothesis it replaced:
the trap is selective in (L, realization)-space, not density-space.

## The K5b failure (root cause)

Prereg predicted T1 (16,16 pre-shift) would abstain 4/4 and T5 (4,4)
would abstain 2/4 (L = 0,1), i.e. n_abstain(12) >= 3 > = n_abstain(13).
Realized: n_abstain = 2 on both (L = 0,1 trapped; L = 3,7 committed
eager pre-shift).

On T1 the pre-shift realization was query-dense (Dpre = 8, Qpre = 14;
at tc = 80: dh = 71, qh = 227, qlo = 67, dhi = 171): the price upper
bound phin/phid = 104/67 ~= 1.55 fell below L = 3, so L = 3,7
committed eager decisively at tc = 80, correctly (realized pre-shift
price ~= 0). On T4 (8,8) the same escape happened at tc = 64; on T5
(4,4) at tc = 32. The trap only stranded L = 0,1, where the interval
still straddled L.

The error in the hypothesis: "symmetric sparse pre-shift keeps the
price interval straddling all L" assumed the realization would be
symmetric. Burst-modulated arrivals realize asymmetrically often
enough that larger L escape via legitimate decisive commits. The
mechanism is not defective (K4c byte-identity; snapshots coherent);
the hypothesis was too coarse. What survives, stronger: **the trap's
robust core is small L under thin evidence.** L = 0,1 trapped on
every sparse pre-shift cell (T0, T1, T2, T4, T5); L = 0 additionally
can never go eager by construction.

## Answers to the four questions

1. **When does the trap trigger?** When the pre-shift price interval
   straddles the caller's L at every checkpoint e in {32..128}, so
   the episode hits the e = 128 budget undecided (cm = 0, com = 2,
   terminal). Measured: L = 0,1 trap on all five sparse pre-shift
   cells (16/16, 8/8, 4/4 pre-shift); L = 3,7 escape when the
   realization (or denser data) tightens the price upper bound below
   L. The boundary is selective in L and realization-dependent; the
   density-monotone formulation is falsified (K5b). Practically: thin
   pre-shift evidence plus small L (unit refusal cost, the most
   natural setting) is the trap zone. Cold start / rare events, not
   a contrived seed.
2. **Is it a real problem? Yes.** On T1-L1 the trapped episode paid
   J = 22 (rb = 11, rf = 11), identical to fixed lazy, vs 15 for
   fixed eager: 11 post-shift refusals that a timely eager commit
   would have avoided. Same pattern on T4 (32 vs 30) and T5 (66 vs
   64). The trap converts honest pre-shift abstention into a
   stuck-lazy post-shift policy at measurable cost.
3. **Can it be avoided? Yes, by deferring the abstention.** The
   recheck arm late-committed eager at tc = 144 on every trapped
   L = 1 episode (T1, T4, T5: lc = 1, sel = 1, cm = 2), with zero
   recheck-induced flips anywhere (the 3 total rechk flips are the
   inherited T3 flips, field-identical on adapt), zero wrong-direction
   late commits, and strict J improvement everywhere the trap fired:
   T1 22 -> 17, T4 32 -> 29, T5 66 -> 59. On T4/T5 the recheck even
   beat fixed eager (29 < 30, 59 < 64): the adaptation dividend from
   running lazy while evidence was thin, then committing eager when
   the regime turned.
4. **Or is the trap correct behavior? No, on these cells:
   H-trap-correct is rejected.** The recheck did not thrash (max 1
   flip/episode, total 3, all inherited), never committed eager at
   L = 0 (K6b), never invented an eager commit where the post-shift
   world was lazy-optimal (T2: zero sel = 1, J identical per L), and
   stayed deferred under stationary sparsity (T0: all com = 2, no
   late commits, J within +1). Terminality was not protective here;
   it was the defect. Nuance: the honest-abstention *principle*
   survives inside the recheck, which still only commits on decisive
   evidence and still abstains when evidence stays thin. What was
   wrong was abstain-forever across a regime change, not abstention.

## Kill-bar adjudication

| Bar | Status | Detail |
|-----|--------|--------|
| K1 prereg order | PASS | probe de48ebc8a -> PREREG c75ed50ae -> NAMECHECK 704489c51 -> implementation efdf43deb; no implementation file in prereg commit |
| K2 toolchain | PASS | safebin PATH, no python3/python, znc sha256 verified in-script |
| K3 determinism | PASS | build clean, exit 0, stderr empty, 3/3 byte-identical (5258aa3f...), 60 CELL lines |
| K4 anchoring | PASS | cross-arm (D,Q) identical; fixed-arm identities; splits show the shift; T3 pol-0/1/2 byte-equal parent R1 (modulo lc); T3 rechk field-equal adapt |
| K5a trap occurrence | PASS | T1 adapt L = 0,1 both cm = 0 |
| K5b boundary | **FAIL** | n_abstain(12) = 2 < 3 (n_abstain(13) = 2 <= 3 held); density-monotone hypothesis falsified |
| K5c dense escape | holds | T5 adapt L = 7 cm = 2 (measured; lane already failed) |
| K6a late commit | holds | T1 rechk L = 1: lc = 1, sel = 1, cm = 2, tc = 144 exactly as predicted |
| K6b L0 safety | holds | all 6 rechk L = 0: sel = 0, cm != 2; T1-L0 clean cm = 0 |
| K6c no thrash | holds | total rechk flips = 3 (all inherited T3), max 1/episode, T0 zero |
| K6d mirror harmless | holds | T2 rechk: zero sel = 1; J identical per L; flips equal |
| K6e/f accounting | holds | lc iff (rechk and tc > 128); late cm = 2 restamp identity rs = 1+(D-Dc); full structural accounting on all 40 adapt+rechk lines |
| K7a/d economics | holds | wherever trap fired and recheck fired eager: J strictly better (22->17, 32->29, 66->59) |
| K7b/c | holds | T2 J identical; T0 J within +1 |
| K8 hygiene | PASS | ASCII-only, no world literals, one fn main, 9 reused sources unmodified, da_learn.zag untouched, local commits with explicit pathspecs, never pushed |

"holds" = the preregistered condition was evaluated on the frozen
3/3-byte-identical data and is satisfied; not claimed as a passed
kill bar since the lane verdict is FAIL.

## Tested findings

1. **The trap is (L, realization)-selective.** Abstention table
   (adapt cm = 0): T0 4/4, T1 {0,1}, T2 4/4, T3 0/4, T4 {0,1},
   T5 {0,1}. L = 3,7 escaped on T1/T4/T5 via pre-shift eager
   commits at tc = 80/64/32 when the realized price upper bound
   cleared L. The robust trap core is L in {0,1} under thin
   pre-shift evidence.
2. **Deferred abstention strictly dominates terminal abstention on
   every trapped episode measured.** Three cells x L = 1, all
   correct-direction, all prompt (tc = 144), all strictly cheaper,
   zero thrash. The recheck also correctly late-committed *lazy*
   on the mirror cell (T2: L = 0,1 @144, L = 3,7 @160, all sel = 0),
   where abstention had been fine: it re-decides, it does not
   bias eager.
3. **Adaptation dividend.** T4/T5-L1 recheck J (29, 59) beat fixed
   eager (30, 64): running lazy while evidence was thin, then
   committing eager at the shift, outperformed either fixed policy.
4. **The recheck changes nothing when pre-shift is decisive.**
   T3 rechk lines are field-equal to adapt on all numeric fields
   (K4d); the 3 rechk flips are the inherited parent-R1 flips.
5. **Design-phase quirk (disclosed, guarded by the probe):** with
   (dh,ed) = (0,0) the inherited margin test's price interval
   degenerates to {0}, making any L >= 1 eager-decisive: a zero-data
   eager commit at e = 32. The probe's D32 >= 1 selection rule kept
   this out of the sealed cells; the quirk itself is untested and
   belongs in a cold-start lane, not a patch here.

## Honest scope limits

- One shift per episode at tick 128 (inherited); multiple shifts,
  pre-commit shifts, and gradual drift remain untested.
- Six cells, one drift/query family; the (L, realization)
  selectivity claim rests on 5 sparse pre-shift cells.
- K5b's falsification leaves the full boundary surface unmapped;
  the refined characterization (interval-straddles-L) is measured,
  not yet preregistered-and-confirmed.
- L is caller-stated, not measured (inherited).
- The recheck semantics change honest-abstention behavior; per the
  parent REPORT's recommendation it needs a governance decision,
  not silent adoption.

## Recommendations

1. **Do not silently adopt the recheck.** The experiment validates
   deferred abstention as the avoidance mechanism, but changing
   budget-default from terminal to deferred alters honest-abstention
   semantics: bank for Micah's governance decision with this report
   as evidence.
2. **Re-map the boundary with the refined hypothesis.** A follow-up
   lane should preregister the (L, realization) selectivity claim
   directly: engineer pre-shift price intervals near specific L
   values and test abstention per L, rather than using density as a
   proxy.
3. **Cold-start lane for the zero-data degenerate commit.** The
   (dh,ed) = (0,0) -> eager-decisive quirk found during design is a
   real margin-test edge; it deserves its own preregistered lane.
4. **Keep the T3 seed-identity pattern.** Byte-equality against the
   parent's frozen output caught no defect here, which is exactly
   what makes it worth keeping: it is a cheap, strong rebuild
   validator.

## Process notes

- Pure Zag throughout; safebin mandatory (`which python3` /
  `which python` empty, recorded in NAMECHECK.md Step 0); pinned
  znc znc_linux_x86_64_abed8aa1 (sha256-verified in at_build.sh);
  no Python invoked at any point. Output analysis via
  grep/cmp/awk/shell only.
- Seed probe (probe.zag) ran pre-prereg, examined arrival counts
  only, and selected R = 10/12/11/14/13 by the frozen D32 >= 1
  rule; T3 fixed at R = 1 for cross-lane identity.
- Git: `/usr/bin/git` directly; explicit pathspecs; commits local,
  never pushed. Commit order on the lane dir: de48ebc8a (probe) ->
  c75ed50ae (PREREG) -> 704489c51 (NAMECHECK) -> efdf43deb
  (implementation). No amendments; no post-implementation bar
  changes. The K5b failure was not re-barred: verdict stands as
  BUILD-FAIL.
- `da_learn.zag` not modified (separate lane only, per task).
- at_spec.zag is a minimal documented delta on the parent's
  rc_spec.zag ([AT-DELTA] markers; full diff reviewed before
  build): pol-3 deferred re-check branch, lc flag at CS+116,
  pol-3 plumbing/naming. For pol in {0,1,2} the tick dynamics are
  unchanged (K4c byte-identity confirms empirically).
- Repro: `./at_build.sh` assembles the binary, builds with the
  pinned znc, runs 3x (byte-identity + kill-bar adjudication).
  All sources and logs are in this lane directory.
