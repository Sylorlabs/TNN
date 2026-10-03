# REPORT: COGOPS-TRANSITION-PREDICT-2 (c22)

## Verdict: 8/9 kill bars PASS. Transition inequality PREDICTS.

The leadership-transition inequality `ra/rb < (m_N−m_W)/(φ_W−φ_N)`
cleanly predicts NEED→WHOLE transitions on new (k, ledger)
parameters with fresh strategy contexts. The probe (exact
formalization of the score race) predicts all 74 battery stages
byte-exact, including transition stages t=8 (P1, k=2) and t=12
(P2, k=3), and zero transitions for k=12 (Q1, Q2).

## Kill bars
- K1 (P1 NEED→WHOLE at exactly P1b-8): PASS. chosen=3 at t1..t7,
  chosen=2 at t8..t10. One leadership change, NEED→WHOLE, at t=8.
- K2 (P2 NEED→WHOLE at exactly P2b-12): PASS. chosen=3 at t1..t11,
  chosen=2 at t12..t15. One leadership change, NEED→WHOLE, at t=12.
- K3 (Q1 zero transitions): PASS. chosen=3 at all 10 test stages.
- K4 (Q2 zero transitions): PASS. chosen=3 at all 10 test stages.
- K5 (k-monotonicity: 8 < 12): PASS. More incumbent wins → later
  transition, as the inequality predicts (higher k → lower φ_N →
  lower threshold → more ledger accumulation needed).
- K6 (3/3 byte-identical, empty stderr): PASS. sha256
  2463fd16244ec5a4a11f66ba578d72b86f750ebd1a4786a7fa0891867369ed22.
- K7 (setup bytes identical to c21): FAIL (specification error).
  S1A..S6L byte-identical. S6B differs ONLY in nfacts (89 vs 77):
  the 12 new world facts required for fresh contexts. All
  learning dynamics identical (rev=5, nrel, ids, cnts). The kill
  bar as written did not account for the new facts; the
  scientific content (setup learning identity) holds.
- K8 (0 DET-HEDGE): PASS. Zero hedge firings across 80 stages.
  The nn=3 design avoids the nn=4 setup exact-tie structurally.
- K9 (probe fidelity, 74/74): PASS. Probe's per-stage chosen
  predictions match observed DET-STRAT at every battery stage.

## Design flaws fixed (from c21)
1. Probe simulates full selection (argmin + hedge gate) in EVERY
   stage, with per-turn (u,w,c) updates and within-stage ledger
   updates. Validated: 69/69 c21 DET-STRAT byte-exact, 2/2 hedges.
2. Fresh (nn,rel) contexts per arc: P1=(3,617), P2=(3,619),
   Q1=(3,621), Q2=(3,623). New rels mirror 613's 3-fact pattern;
   pilot verified NEED-winnable/unwinnable with identical costs.
3. nn=3 for all arcs avoids the nn=4 setup-stage-2 exact tie.

## Falsification status
K1 and K2 both PASS: the inequality's predictive claim STANDS.
K3 and K4 both PASS: the no-transition condition STANDS.
K5 PASS: the monotone-k prediction HOLDS.
The inequality is genuinely predictive, not post-hoc.

## Implementation notes
- plan_drop after every stage (mandatory; plan table has 4 slots).
  0 declines across 74 stages.
- Build: c20_base + c18_world + c20_world_add + c22_world_add +
  c20h_learn + c22_main → c22h_bin. Pinned znc, safebin, pure Zag.
- c22_world_add.zag committed with prereg (frozen world design).

## Files
- PREREG.md, NAMECHECK.md (frozen, committed 1dcd51f73 before impl)
- c22_probe.zag, c22_probe_c21replay.txt, c22_probe_c22predict.txt,
  c22_stages_predicted.txt (frozen predictions)
- c22_world_add.zag (frozen world design)
- c22_main.zag, c22_build.sh (implementation)
- c22h_run1/2/3.txt (3/3 byte-identical), c22h_compile.txt
