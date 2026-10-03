# SEALED_KEY.md -- L3-INR Sealed Battery Key
# Adversary: L3-INR-SEALED. Designed post-freeze 2026-10-03 (after impl
# freeze 2026-10-03 07:15:15 UTC). DO NOT MODIFY implementation or prereg.

## S1 (s1.world) -- Incomplete-disambiguation trap (adversarial family)
True order: z0<z1<z2<z3<z4<z5<z6<z7<z8<z9>.
Training: 13 pos (8 adjacents minus 3 gaps + 3 trap positives + 4 jumps),
5 neg. Gaps: (z4,z5),(z5,z6),(z6,z7) [adjacent, not direct edges].
Jumps: (z4,z6),(z5,z7),(z6,z8),(z3,z5).
Trap positives: (z4,z7),(z4,z8),(z5,z8). Trap negative: (z5,z4,0).
Disambiguating negatives: (z6,z5,0),(z7,z6,0).
First-appearance ids: z4=0,z6=1,z0=2,z1=3,z2=4,z3=5,z7=6,z8=7,z9=8,z5=9.
Attrs: |Spearman|x1000 = 67,127,6 (all <0.2, verified).

Learner behavior (observed):
- ADD seeds 13 direct edges. DEL removes 2 (keeps 11).
- UNCONSTRAINED 3 -> HYP 8 variants -> HYP_KEPT 2 (true variant + E).
- PROBE_SEND (z4,z5) [ids 0,9], materialized. Other 2 gaps never fixed.
- COMMIT 12 edges. T1: TRAIN 18/18, HELD 4/6, EDGES 12 -> FAIL.
  (FAIL on heldout <5/6 AND compression >10.)

Controls on S1:
- C0 (attr-NN): HELD 4/6 -> control passes (fails task). G1e OK.
- C1 (memo+1NN): HELD 4/6 -> control passes. G1e OK.
- C2 (ablate-construct): TRAIN 5/18 -> control passes. G1e OK.
- C3 (greedy): fails training (v=1). G1e OK. NOTE: C3 exhibits idx<90
  boundary (cannot add edges from id 9) plus greedy trap neutralization.

HELDOUT_A (6): (z4,z5)[1],(z5,z6)[1],(z2,z8)[1],(z0,z7)[1],(z3,z6)[1],(z9,z8)[0].
Hop counts: 1,1,6,7,3,1. G1c satisfied (3-hop and 6-hop present).

## S2 (s2.world) -- Revision world
True order: z0<z1<z2<z3<z6<z4<z5<z7<z8<z9> (block rotation).
PAIR order gives first-appearance ids matching S1 exactly:
z4=0,z6=1,z0=2,z1=3,z2=4,z3=5,z7=6,z8=7,z9=8,z5=9.
Training: 13 pos, 5 neg. Gaps: (z6,z4),(z4,z5),(z5,z7).
Toxic: (z4,z6,0) purges S1's (z4,z6) edge.
MONITOR: first pair (z4,z6,1) from S1 flips to 0 in S2 -> REGIME_CHANGE.
Attrs: |Spearman|x1000 = 176,7,139 (all <0.2).

T4 result (observed): TRAIN 18/18, HELD 6/6, EDGES 11, lineage 8/12 -> PASS.
NOTE: Only 1 true gap ((z6,z4)) because S1's G already had (z4,z5),(z5,z7)
as direct edges (true in S2). The revision fixed the single gap via probe.
This is a MILD regime change; T4's revision succeeded. The incomplete-
disambiguation family does NOT break T4 when the gaps are pre-covered.

HELDOUT_A (6): (z6,z4)[1],(z4,z5)[1],(z5,z7)[1],(z3,z6)[1],(z0,z9)[1],(z9,z0)[0].
G3 check: S1's G scores 2/6 (only (z0,z9),(z9,z0) correct; (z6,z4),(z6,z5),
(z4,z6),(z6,z7) wrong). G3 satisfied (<=2/6).

## S3a (s3a.world) -- Ambiguous resolvable (honest arm)
True order: m0<...<m9. Ambiguous pair: (m3,m4) [truth=1].
Training: 12 pos (8 adjacents minus gap + 2 bridges + 2 long), 6 neg.
Bridges: (m2,m4),(m3,m5). Negative: (m4,m3,0).
After DEL: UNCONSTRAINED 1 [(m3,m4)]. Probe queries (m3,m4), world
confirms 1, materializes. T5a: TRAIN 18/18, HELD 6/6 -> PASS (honest).
Attrs: |Spearman|x1000 = 66,18,85 (all <0.2).
HELDOUT_A: (m3,m4)[1],(m2,m5)[1],(m0,m4)[1],(m3,m6)[1],(m1,m9)[1],(m9,m1)[0].

## S3b (s3b.world) -- Ambiguous unresolvable (honest abstention)
True order: m0<...<m9. Ambiguous pair: (m6,m7) [truth=1].
Training: 12 pos, 6 neg. NEITHER (m6,m7) NOR (m7,m6) in TRAIN (else
PROBE_EXCEPT would forbid the training TEST).
Bridges: (m5,m7),(m6,m8).
PROBE_EXCEPT 2: XPAIR m6 m7, XPAIR m7 m6.
After DEL: UNCONSTRAINED 1. HYP_KEPT 3. Disagreement set = {(m6,m7),(m7,m6)}.
PROBE_SEND (m6,m7) -> FORBIDDEN. PROBE_SEND (m7,m6) -> FORBIDDEN.
T5b DEFERS (DEFER 1) -> PASS (honest abstention).
Attrs: |Spearman|x1000 = 43,116,55 (all <0.2).
HELDOUT_A: (m6,m7)[1],(m5,m8)[1],(m4,m7)[1],(m6,m9)[1],(m0,m8)[1],(m8,m0)[0].

## S1p (s1p.world) -- Recoded S1 for T3b
Same order and training skeleton as S1 (18 pairs). Fresh attrs
(|Spearman|x1000 = 78,90,18). Fresh HELDOUT_A (6):
(z4,z5)[1],(z5,z6)[1],(z2,z6)[1],(z1,z7)[1],(z0,z8)[1],(z8,z0)[0].
T3b result: HELDOUT pairs=0 (protocol: T3b does not load heldout after
SLOT_READ+OBSERVED) -> DEV_VERDICT FAIL. This matches the predicted
adversarial outcome (transfer fails), though via a protocol limitation
rather than a rank-quality failure. Documented as a caveat.

## Design timestamps
All worlds designed 2026-10-03 ~07:26-09:00 UTC, strictly after impl
freeze (2026-10-03 07:15:15 UTC) and prereg freeze (2026-10-02).
