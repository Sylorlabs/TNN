# PREREG_AMENDMENT1: L2-COMPOSE-CHAIN4B

Frozen 2026-10-03, BEFORE implementation. Transparent
correction to PREREG.md section 4.

## Constraint discovered

`f_teach` hard-caps at 44 facts (`if(n>=44) return -1`).
world_F.zag already uses all 44. The 16 probe facts
(f44-f59) cannot be added. A full [6,5,4] prefix +
probes world is infeasible under the frozen learner.

## Revised design (minimal preemption probe)

The preemption logic does not require the full [6,5,4]
prefix. If a 4th-link candidate is preempted by an
earlier operator on Z4 (the FIRST Z tried in phase 2),
it can never be the 4th link, because phase 2 always
tries Z4 before Z5/Z6.

Build G (revised):
- learner.zag: byte-identical to chain4's (sha256
  6e8ed1e0..., verified). ZERO changes.
- world_G.zag (31 facts): f0 (10,24,11) [id 0];
  f1-f6 mA' (20->25, val 51); f7-f14 mP' (70->77,
  val 52); f15-f22 QD1 region (90->97, val 59);
  f23-f30 Probe S region (180->187, val 67);
  f31-f38 Probe A region (190->197, val 68).
  39 facts total, under the 44 cap.
- driver_G.zag: teaches id0/mA'/mP'; QD1(90,97,59)
  -> Z4 (id 3) via op6; QD4S(180,187,67);
  QD4A(190,197,68). FULL arm (mask 63).

Probe S region (f23-f30): (180,29,181),
(181,22,182),(182,23,183),(183,22,184),
(184,23,185),(185,22,186),(186,23,187),
(187,4,67). Entry rel 29.

Probe A region (f31-f38): (190,23,191),
(191,22,192),(192,23,193),(193,22,194),
(194,23,195),(195,22,196),(196,23,197),
(197,4,68). Entry rel 23.

## Revised predicted outcomes

- QD1: op==6, tries==6, dec==1, via==3, val==59,
  phit==0. Z4 built (id 3).
- QD4S: phase 1 all 6 fail (3-fold region vs
  mA' dnf=2; CONCRETIZE not novel vs (22,23));
  phase 2 on Z4: op1 fail, op2 excluded (29==29),
  op3/op4 fail, op5 FIRES. op==5, tries==11,
  dec==1, via==3, val==67, phit==0.
- QD4A: phase 1 all 6 fail; phase 2 on Z4: op1
  fail, op2 FIRES (23 != 29, walk verifies).
  op==2, tries==8, dec==1, via==3, val==68,
  phit==0.
- FALSIFIERS 0.

## Revised kill bars

- G-K1: QD1 op==6 tries==6 via==3 val==59.
- G-K2: QD4S op==5 tries==11 via==3 val==67
  (SUBSTITUTE preempted); QD4A op==2 tries==8
  via==3 val==68 (ABSTRACT preempted).
- G-K3: 3/3 byte-identical.
- G-K4: FALSIFIERS==0, oth==0.

Verdict rule unchanged: if G-K2 holds,
[6,5,4,2] and [6,5,4,5] are infeasible as 4th
links (preempted at Z4). If QD4S fires op==2 or
QD4A fires op==5, H-4B is falsified.
