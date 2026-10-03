# PREREG_AMENDMENT1: L2-METAREUSE-COMPOSE-2

Pre-verdict, transparent. Amends PREREG.md sections 5c
and 6 (D-K5). No counting-rule or learner-code change.

## The error

PREREG.md section 5c predicted for the ABLATE-ABS arm
(mask 47: ops 1,2,3,4,6) QD1: "op=6, tries=6". The
in-Zag falsifier caught this on the first run
(FALSIFIERS 1; K5-ad1tries=5).

Root cause: MR_OP_TRIES (state 1380) is incremented
only when an operator is actually TRIED (mask bit
set), not when it is SKIPPED. This is the frozen
behavior, identical in phase 1 and phase 2. With op5
masked out, QD1 tries only 5 operators (1,2,3,4,6),
so tries==5. The prereg author counted the masked op5
as a try; the code never did.

## Corrected predictions (ABLATE-ABS arm only)

- QD1: op==6, tries==5, dec==1, via==4, val==59.
  (Phase 1: ops 1,2,3,4 tried, op5 SKIP, op6 tried.)
- QD2: op==6, tries==10, dec==1, via==5, val==63
  (unchanged: phase 1 contributes 5 tries
  [ops 1,2,3,4 tried, op5 SKIP, op6 tried]; phase 2
  on Z4 contributes 5 more [ops 1,2,3,4 tried, op5
  SKIP, op6 tried and verifies]).
- QD3: val==-2, tries==15, op==-1 (unchanged:
  5 + 5 + 5).
- t16==2 with e_has(5,3,16)==1 and
  e_has(5,4,16)==0 (unchanged).

D-K5 is amended to read "QD1: op==6, tries==5,
via==4, val==59" for the ABLATE-ABS arm. All other
bars, predictions, and falsifiers are unchanged. The
driver's in-Zag check is updated to the amended bar
(a_d1_tries!=5).

No mechanism, world, or learner change: the
implementation behaved exactly per the frozen
mask-gated tries counting. This amendment corrects
the prereg's arithmetic, not the experiment.
