# PREREG: L2-COMPOSE-CHAIN4B (4-operator combination generality probe)

Frozen 2026-10-03 by the L2-COMPOSE-CHAIN4B-RETRY worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE. Any pre-verdict
correction goes in a PREREG_AMENDMENT file, transparent,
never silent.

## 1. Mandate and scope

L2-COMPOSE-CHAIN4-PASS demonstrated one 4-operator chain,
[6,5,4,4] (CONCRETIZE -> ABSTRACT -> INVERT Form A ->
INVERT Form B), with zero learner changes. Disclosed
non-claim: "One [6,5,4,4] chain does not establish
general 4-operator composability."

This wave tests whether a DIFFERENT 4-operator
combination works, with the 4th operator different
from INVERT (op4). Specifically the candidates
[6,5,4,1], [6,5,4,2], [6,5,4,3], [6,5,4,5], [6,5,4,6].

## 2. Preregistered infeasibility hypothesis

H-4B: No 4-operator chain with 4th operator != INVERT
is feasible on the frozen learner with the [6,5,4]
prefix. The [6,5,4] prefix is forced (QD3 must be
INVERT: it is the only operator that discriminates
Z5 from Z4 via aend/reversed-rels). Given Z4/Z5/Z6
with identical dnf=3/dvr=4:

- [6,5,4,2] (SUBSTITUTE 4th): SUBSTITUTE needs
  rel != de(Z6)=23; to block it on Z4/Z5 (de=29)
  the entry rel must be 29; but then ABSTRACT (op5,
  tried after op2) fires on Z4 (rel==29 match).
  Preempted: 2-chain, not 4-chain.
- [6,5,4,5] (ABSTRACT 4th): ABSTRACT needs
  rel == de(Z6)=23; but then SUBSTITUTE (op2, tried
  before op5) fires on Z4 (23 != 29). Preempted.
- [6,5,4,6] (CONCRETIZE 4th): needs folds novel vs
  Z6's (22,23); Z5 shares (22,23), so it fires on
  Z5 first. 3-chain, not 4-chain.
- [6,5,4,1] (COMBINE 4th): COMBINE uses only
  dnf/dvr (identical on Z4/Z5/Z6); cannot
  discriminate, fires on Z4 first.
- [6,5,4,3] (TRUNCATE 4th): needs a short walk;
  mA' (dnf=2) preempts via its own TRUNCATE or
  SUBSTITUTE/ABSTRACT on the short walk.

The de-discriminator is symmetric: any entry rel
either matches Z4/Z5's de (triggering ABSTRACT
there) or mismatches it (triggering SUBSTITUTE
there). INVERT alone escapes via the aend
discriminator, which no other operator has.

## 3. Empirical discrimination probes

Two minimal probes on the frozen learner + extended
world. Both reuse the validated [6,5,4] prefix
(QD1/QD2/QD3 identical to chain4, building
Z4 id 3, Z5 id 4, Z6 id 5).

Probe S ([6,5,4,2] candidate): QD4S=(180,187,67).
Region f44-f51: entry (180,29,181) [rel 29 blocks
SUBSTITUTE on Z4/Z5 by exclusion, allows it on Z6],
3-fold (22,23) walk 181->187 [not novel vs mA' or
Z6, blocking CONCRETIZE in phase 1], value
(187,4,67) fresh. Predicted: phase 1 all 6 fail;
phase 2 on Z4: op1 fail, op2 excluded (29==29),
op3/op4 fail, op5 FIRES (rel==29, walk verifies).
QD4S: op==5, tries==11, dec==1, via==3, val==67,
phit==0. A [6,5] 2-chain: SUBSTITUTE is preempted
and can never be the 4th link.

Probe A ([6,5,4,5] candidate): QD4A=(190,197,68).
Region f52-f59: entry (190,23,191) [rel 23 matches
Z6's de for ABSTRACT], 3-fold (22,23) walk
191->197, value (197,4,68) fresh. Predicted:
phase 1 all 6 fail; phase 2 on Z4: op1 fail, op2
FIRES (23 != 29, walk verifies). QD4A: op==2,
tries==8, dec==1, via==3, val==68, phit==0. A [6,2]
2-chain: ABSTRACT is preempted and can never be
the 4th link.

If both probes preempt as predicted, H-4B's core
(de-discriminator impossibility) is empirically
confirmed for the two most plausible candidates;
[6,5,4,1], [6,5,4,3], [6,5,4,6] stand refuted by
the section 2 analysis.

## 4. Frozen build specification (build G)

- learner.zag: byte-identical to chain4's learner.zag
  (sha256 6e8ed1e047e9dee8311a264aaec9a995ddbb723f5b284e21c18baa0e68038ddd,
  verified at copy time). ZERO changes.
- world_G.zag: chain4's world_F.zag (44 facts,
  sha256 9197c57320515f2a186a9bb752cc74ff7a46b27b4240ac1c4be3b7e5b6be58a2)
  PLUS 16 probe facts f44-f59 (defined in section 3).
  60 facts total. The driver never names an operator.
- driver_G.zag (new): teaches MAPs as chain4;
  queries QD1(90,97,59), QD2(140,148,63),
  QD3(160,167,65), QD4S(180,187,67),
  QD4A(190,197,68). Single FULL arm (mask 63).
  Records op/tries/dec/via/val/phit per query.
  In-Zag falsifier count.
- Build: `cat learner.zag world_G.zag driver_G.zag
  > comp_G_full.zag`, pinned znc.

## 5. Frozen predicted outcomes (build G)

- QD1: op==6, tries==6, dec==1, via==3, val==59,
  phit==0. (chain4 6a.)
- QD2: op==5, tries==11, dec==1, via==4, val==63,
  phit==0. (chain4 6a.)
- QD3: op==4, tries==16, dec==1, via==5, val==65,
  phit==0. (chain4 6a.)
- QD4S: op==5, tries==11, dec==1, via==3, val==67,
  phit==0. (section 3.)
- QD4A: op==2, tries==8, dec==1, via==3, val==68,
  phit==0. (section 3.)
- FALSIFIERS 0.

## 6. Frozen kill bars (build G)

- G-K1 (prefix replicates): QD1 op==6 tries==6;
  QD2 op==5 tries==11; QD3 op==4 tries==16.
- G-K2 (preemption): QD4S op==5, tries==11,
  via==3, val==67 (NOT op==2/via==5); QD4A op==2,
  tries==8, via==3, val==68 (NOT op==5/via==5).
- G-K3 (determinism): 3 runs of comp_G_bin
  byte-identical (shell sha256).
- G-K4 (hygiene): FALSIFIERS==0; oth==0.

## 7. Falsifiers (in-Zag, build G)

F-PRE: QD1/QD2/QD3 op/tries != section 5.
F-SUB: QD4S op!=5 or tries!=11 or via!=3 or
  val!=67 (SUBSTITUTE was not preempted).
F-ABS: QD4A op!=2 or tries!=8 or via!=3 or
  val!=68 (ABSTRACT was not preempted).
F-PHIT: any phit!=0.
F-OTH: oth!=0.

## 8. Verdict rule

L2-COMPOSE-CHAIN4B-PASS (infeasibility confirmed)
iff ALL of: (1) G-K1 through G-K4 hold, i.e. both
probes preempt exactly as predicted (op==5/via==3
for QD4S, op==2/via==3 for QD4A); (2) 3/3
byte-identical; (3) zero falsifiers; (4) learner.zag
sha256-identical to chain4's learner (no learner
change).

If QD4S fires op==2 via==5, H-4B is FALSIFIED:
[6,5,4,2] is feasible and the wave reports a
positive 4-chain discovery instead. If QD4A fires
op==5 via==5, likewise for [6,5,4,5]. Either
falsification overrides the infeasibility claim.

## 9. Standing rules

- Prereg frozen BEFORE implementation; this file +
  NAMECHECK.md committed ALONE.
- Pure Zag; safebin PATH; no python3/python.
- as/ae informational only; determinism by 3/3
  byte-identical.
- L2 only; this wave cannot promote to L3.
- No em/en dashes in loop documentation.
- Commits local with explicit pathspecs; nothing
  pushed. Chain4 lane never modified.
- Non-ledger task; verdict only, no claim minting.
