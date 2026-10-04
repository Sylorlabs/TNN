# Result: BEAM G2 Refutation-Seeking IV Policy

Date: 2026-09-30. Worker: G2 Beam Builder.
Verdict: **G2-FAIL**.

## Summary

The G2 refutation-seeking IV policy was implemented per the frozen
preregistration (commit d4485706f). All controls reproduced byte-identical.
All three batteries ran 3/3 byte-identical with zero stderr. Pure Zag
throughout; zero Python at every stage.

G2 did not improve R3 Arm 2. The refutation-seeking IV policy changed
which interventions were selected but did not produce better
compositional reuse. Multiple frozen falsifiers fired.

## Implementation

Files under beam_g2/:
- r1g.zag: byte-identical copy of beam_unified_clean/r1u.zag
  (md5 36114a681a9b1a52af70eb6bc5953d19). Unchanged per prereg.
- r3g.zag: r3u.zag with select_iv_u replaced by select_iv_g2.
- frg.zag: frecu.zag with select_iv_u replaced by select_iv_g2.
- r1_base.zag, r3_base.zag, frec_base.zag: frozen baseline sources
  for control reproduction.

The select_iv_g2 function implements the frozen interleave:
even iv_idx uses the verbatim disagreement selector;
odd iv_idx uses refutation-seeking (minimize beam-internal agreement
about the champion's prediction; tie-break by max disagreement,
then lowest x). Only IV selection changed; candidate generation,
retention, scoring, drivers, and seeds are unchanged.

Diff verification: r3g.zag and frg.zag differ from their bases only
in the select_iv function and its two call sites (each). r1g.zag is
byte-identical to r1u.zag.

## Controls (K2 prerequisite)

All three base batteries recompiled with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256 498abcb5)
and run 3x:

- R1: 3/3 byte-identical, md5 89cb21e6359bafaf3d02d34575d3bd0a.
  Matches committed unified clean output.
- R3: 3/3 byte-identical, md5 6a8568a7232de691606e09712df0f17d.
  Matches committed unified clean output.
- FREC: 3/3 byte-identical, md5 95b87706c9763e22e075a5b11fc79f38.
  Matches committed unified clean output.

Zero stderr bytes on all control runs. Baseline is solid; G2 ran
against an unmoved baseline.

## G2 runs (K3)

- R1: 3/3 byte-identical, md5 89cb21e6359bafaf3d02d34575d3bd0a
  (identical to control; r1g.zag unchanged).
- R3: 3/3 byte-identical, md5 c0f8e82b2982796c1aef53875fb8d7df
  (differs from control; G2 changed IV selections).
- FREC: 3/3 byte-identical, md5 9d59166cdecd04313f0d583fc4d12b94
  (differs from control; G2 changed IV selections).

Zero stderr bytes on all G2 runs. Zero Python at every stage from
task start. K3 holds.

## Falsifier evaluation

### R1 (regression guard; r1g.zag unchanged)

- F-FIT: FIRES. 0/5 seeds reach EVFIT=32/32 (observed 31,31,31,31,29).
  Frozen bar requires 4/5. Same as unified baseline.
- F-NODOM: FIRES. NODOMV > 0 on all 5 seeds (636, 700, 565, 688, 1550).
  Same as unified baseline; cause is the retention ordering, not G2.
- F-BLOAT: FIRES. Seed 85021 MAXSIMS=1328 exceeds CEIL=1219.
  Same as unified baseline.
- F-TIE-HONEST: does not fire (TIECHECK=OK on all seeds).
- F-CASE: does not fire (no new machinery in R1).

### R3 (primary outcome)

Arm 1 (regression guard):
- A1-PASS=1 (REUSE_IV 0, true=64/64; SCRATCH_IV 24, true=57/64).
  Baseline was A1-PASS=1 (64/64 vs 54/64). F-REGRESS does not fire.

Arm 2 (primary):
- A2 REUSE_IV 24, true=49/64, HAS_D=1.
- A2 SCRATCH_IV 24, true=43/64.
- A2-PASS=0.
- Baseline was 52/64. G2 scored 49/64: no improvement.
- F-DIVERSE-FAIL: FIRES.

Other R3 falsifiers:
- F-NODOM: FIRES (NODOMV 1211, 1084, 1299 on three of four drivers).
- F-BLOAT: does not fire (max MAXSIMS=1246 < CEIL=1263).
- F-CASE: does not fire. The refutation selector uses only the
  learner's own beam predictions (node_pred on learner nodes).
  No target, family, sealed answer, library identity, or D identity
  enters the selection.

### F-RECFOLD (exploratory)

- F-NODOM: FIRES (NODOMV > 0 on all 15 instances).
- F-BLOAT: FIRES (P1-I1-S44 MAXSIMS=1273 exceeds CEIL=1243).
- B1/B2/B3 per frozen bars: Instance 1 shows 64/64 true on I1/I2
  seeds with bobs_true at chance (33/64), consistent with the
  unified baseline pattern. Instances 2-3 remain at chance.

## Alternative explanation A1

Pre-registered: "merged, then would have lost anyway." The G0 Q
candidates had low evidence accuracy (1,1,1,9 of 64); the merge rule
may not be the binding constraint.

Kill conditions (both required):
- (a) E-shaped candidates proposed with accuracy above 32/64.
- (b) R3 Arm 2 improves relative to unified baseline (52/64).

Result:
- (b) FAILS. Arm 2 scored 49/64 under G2 vs 52/64 baseline.
  No improvement.
- (a) UNRESOLVED. The G2 build does not include G0-style
  operator-histogram instrumentation; Q-signature prevalence cannot
  be assessed from the standard output. Per the prereg, this is
  reported honestly rather than inferred.

Since (b) fails, A1 is not killed. A1 SURVIVES: the evidence-accuracy
caveat stands. Better IV selection did not produce behaviorally-good
E-shaped candidates.

## Verdict

**G2-FAIL.**

Kill bars:
- K1: PASS. Prereg d4485706f committed strictly before implementation.
- K2: PASS. R1, R3, FREC all ran; all falsifiers evaluated.
- K3: PASS. Pure Zag; 3/3 byte-identical; zero stderr; zero Python.

Fired falsifiers: F-FIT, F-DIVERSE-FAIL, F-NODOM, F-BLOAT.

The refutation-seeking IV policy does not repair the R3 Arm 2
compositional reuse failure. The G0 caveat survives: low-accuracy
Q-shaped candidates are not explained by poor IV selection alone.

Honest scope: this is a bounded-L2 search result. Not L3, not
Criterion 0, not a Q4 revival. The G2 mechanism is generic search
machinery that failed to help on this compositional form.

## Recommendation

The IV policy is not the binding constraint on Arm 2. The G0
evidence-accuracy caveat points at candidate generation or the
evidence itself. A future prereg could test whether the generator
ever proposes high-accuracy E-shaped candidates under any IV policy,
or whether the retention ordering (F-NODOM) interacts with
compositional reuse. Do not run G3 without a new prereg that
addresses the surviving A1.
