# PREREG_AMENDMENT1: world redesign for the 44-fact cap

Frozen pre-verdict 2026-10-03, transparent correction to
PREREG.md. The PREREG.md predictions were hand-simulated
against the frozen operator source but missed a frozen
harness capacity limit.

## What happened

The first build-E run (exploratory, never a verdict
candidate) showed QD3 failing with tries=18 and
FALSIFIERS 19. Trace inspection: Form B's reverse
value lookup printed t*=-1, i.e. the fact scan never
saw (167,4,65). Root cause: `f_teach` in the frozen
learner returns -1 silently when n>=44 (fact table
holds 44 facts: 16+44*8 = 368 = MAP table start).
world_D already teaches 42 facts, so world_E's
f44..f57 were never taught. The mechanism is fine;
the world overflowed a frozen capacity limit.

## Redesign (44 facts exactly)

- Drop world_D's f35-f41 (150->157 region): no build-E
  query uses start 150. Saves 7.
- Drop QD1's dead entry (90,28,91): op1/op2/op3 fail
  identically without it (verified by trace analysis:
  op1 b=1 reaches the route step and fails, b=2 fails;
  op2/op3 land mid-region). Saves 1. QD1 renumbers to
  90->97, val 59 at 97.
- Drop QD2's decoy entry (140,29,141): op5's first
  candidate becomes (140,29,142) directly; all phase-1
  failures unchanged (op1 now fails at the route step
  instead of FAIL-SHAPE). Saves 1.
- Drop mB' and QB: mB' existed only to carry QB.
  Saves 2 (f7, f8). MAP ids shift: mD' id 0, mA' id 1,
  mP' id 2. The pattern is now id 2; CONCRETIZE-built
  Z4's t16 edge is (4,2,16), not (4,3,16). op1's only
  partner is mD'; every op1 failure in the predictions
  was re-verified to still fail (route step, never a
  success).
- Shorten QD4 to 5 facts: (170,23,171),
  (171,22,172), (172,23,173), (173,31,174),
  (174,4,66). QD4=(170,174,66). Re-verified: phase 1
  all fail (op2 foldwalk FAIL-SHAPE at the rel-31
  hop; op3 1-fold lands 173 != 174; op4 Form B
  tstar=174 != 25, Form A dead at (173,22,?); op1/op5/
  op6 fail); phase 2 fails on Z4, Z5, Z6 (op4 Form A
  on Z5 dies at (173,22,?); on Z6 dies at the first
  hop (170,29,?); Form B tstar=174 matches no aend).

Final layout (44 facts): f0 mD'; f1-f6 mA'; f7-f14
mP' (70->77); f15-f22 QD1 (90->97, val 59);
f23-f30 QD2 (140->148, val 63); f31-f38 QD3
(160->167, val 65); f39-f43 QD4 (170->174, val 66).

## Corrected predictions (supersede PREREG section 6)

- Z4 = 4(1,7,90,97,1,1,29,26,27,3,4,0),
  rels[29,26,27,26,27,26,27], facts[15,16,17,18,19,20,21],
  e_add(4,2,16).
- Z5 = 5(1,7,140,148,1,1,29,22,23,3,4,0),
  rels[29,22,23,22,23,22,23], facts[24,25,26,27,28,29,30],
  e_add(5,4,16).
- Z6 = 6(1,7,160,167,1,1,23,22,23,3,4,0),
  rels[23,22,23,22,23,22,29], facts[32,33,34,35,36,37,38],
  e_add(6,5,16).
- FULL: QA via=1 val=51 (QB dropped; E-K1 is
  qa_via==1). QD1: op=6, tries=6, dec=1, via=4,
  val=59, phit=0. QD2: op=5, tries=11, dec=1, via=5,
  val=63, phit=0. QD3: op=4, tries=16, dec=1, via=6,
  val=65, phit=0. QD4: op=-1, tries=24, dec=0,
  val=-2. Re-asks QD1-B/QD2-B/QD3-B via 4/5/6,
  entered=0. t16=3; e_has(4,2,16)=1;
  e_has(5,4,16)=1; e_has(6,5,16)=1;
  e_has(6,2,16)=0; e_has(4,1,16)=0;
  e_has(5,2,16)=0; LINK14 to 4,5,6; mD' live=1;
  oth=0.
- NOREUSE: QD1=QD2=QD3=QD4 val=-2, t16=0, oth=0.
- ABLATE-INV (55): QD1: op=6, tries=5, via=4,
  val=59. QD2: op=5, tries=9, via=5, val=63. QD3:
  val=-2, tries=15, op=-1. QD4: val=-2, tries=15,
  op=-1. t16=2; e_has(4,2,16)=1; e_has(5,4,16)=1;
  e_has(6,5,16)=0; oth=0.
- ABLATE-ABS (47): QD1: op=6, tries=5, via=4,
  val=59. QD2: op=6, tries=10, via=5, val=63
  (reroute). QD3: op=4, tries=14, via=6, val=65.
  QD4: val=-2, tries=20, op=-1. t16=2;
  e_has(4,2,16)=1; e_has(5,2,16)=1;
  e_has(5,4,16)=0; e_has(6,5,16)=1; oth=0.
- FRESH: all QD val=-2, t16=0, oth=0.
- CONTROL (frozen learner): FULL: QD1: op=6,
  tries=6, via=4, val=59, Z4-exact=1; QD2/QD3/QD4:
  val=-2, tries=6, op=-1, dec=0; QD1-B via=4
  entered=0; t16=1; e_has(4,2,16)=1;
  e_has(4,1,16)=0; LINK14 to 4; mD' live=1; oth=0.
  NOREUSE: all val=-2, t16=0.

Kill bars E-K1..E-K8 and falsifiers F-* are
otherwise unchanged, with id 3 -> 2 in every t16
edge bar, QD1 terminal 98 -> 97, QD4 (170,174,66),
and E-K1 = qa_via==1. The 3-chain signature is
unchanged in form: QD3 op==4, tries==16, via==6,
val==65, Z6-exact==1; QD4 tries==24 bounded
termination. The verdict rule is unchanged.

## Why this is a correction, not a weakening

No kill bar was moved to force a pass: every bar
still discriminates (QD3 unsolvable by <=2
operators, solvable by the [6,5,4] chain; QD4
terminates). The change is forced by a frozen
harness capacity limit the prereg missed, and every
prediction above was re-simulated against the frozen
operator source before being frozen here.
