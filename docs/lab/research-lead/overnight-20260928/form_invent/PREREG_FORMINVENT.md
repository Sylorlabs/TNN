# PREREG: Form Invention Test

Worker: Form Invention Worker.
Date: 2026-09-30 UTC.
Status: FROZEN before any implementation. This file must be committed
alone before `finvent.zag` exists.

## Objective

The SCALE-TESTED learner (learn_scale/lscale.zag, commit d34e8135c)
selects, fits, retains, and rejects among three researcher-supplied
forms: F0 CONST, F1 LIN, F2 EXC. Its honest scope states it does not
invent forms. This experiment tests that boundary empirically: expose
the learner to families no menu form can represent, and measure
whether it invents a new form, fails cleanly, or misapplies a
wrong form.

## Frozen family specs

Learner machinery is copied verbatim from lscale.zag (fit_const,
fit_lin, fit_exc, fit_form, predict, prior_order, verify_need,
run_family). Only true_subj/true_obj are extended with families
6, 7, 8. Parameters unchanged: BMIN=6, R=4, V0=14, WMAX=3, BMAX=40.

- G (STEP, middle threshold): fam=6. base=6000. T=6003. obj=0 for
  subj<6003, obj=5 for subj>=6003.
- G2 (STEP, edge threshold): fam=7. base=7000. T=7001. obj=0 for
  subj<7001, obj=5 for subj>=7001.
- H (TWO-EXC): fam=8. base=8000. default d=7; exceptions at
  subj=8001 obj=3 and subj=8004 obj=9.

Expected SPEC lines (K1 checks these verbatim):
- SPEC G STEP base=6000 T=6003 lo=0 hi=5
- SPEC G2 STEP base=7000 T=7001 lo=0 hi=5
- SPEC H 2EXC base=8000 d=7 e1=8001->3 e2=8004->9

## Unrepresentability argument (why these need a fourth form)

G at buffer n=6 (subjects 6000..6005, objects 0,0,0,5,5,5):
F0 fails (two distinct values). F1 fails: first two points give
a=0,b=0, fails at subj 6003. F2 fails: d=0, nodd=3, which is
neither 1 nor n-1=5.

H at buffer n=6 (subjects 8000..8005, objects 7,3,7,7,9,7):
F0 fails. F1 fails: first two points give a=-4,b=32007, fails at
subj 8002. F2 fails: d=7, nodd=2 (subjects 8001 and 8004).

G2 at buffer n=6 (subjects 7000..7005, objects 0,5,5,5,5,5):
F2 FITS via the nodd==n-1 branch: d2=5, p=7000, e=0. This is a
near-miss misapplication probe: on all observed data the family
is exactly F2; the form is wrong only with respect to the
unobserved region below 7000. Predicted adopted=2.

## Conditions

- FRESH: fresh learner state per family; run G, G2, H.
- RETAINED: sequential A,B,C,D,E (identical specs to lscale, builds
  uses[F1]=5 and live F1), then G, H, G2.

## Frozen predictions (K2)

| Run | adopted | cost | notes |
|---|---|---|---|
| FRESH G | -1 | 40 | discovery exhausts to BMAX |
| FRESH H | -1 | 40 | discovery exhausts to BMAX |
| FRESH G2 | 2 | 20 | F2 fits at n=6, V=14 verifies |
| RETAINED G | -1 | 40 | 4 refit + 36 discover; refit=0, strikes[F1]=1 |
| RETAINED H | -1 | 40 | 4 refit + 36 discover; refit=0, strikes[F1]=1 |
| RETAINED G2 | 2 | 20 | refit fails (strike), discovery adopts F2 at n=6 |

K2 passes iff all six adopted/cost pairs match exactly.

Falsification note: if G or H adopts any form 0/1/2, the
menu-limitation hypothesis is weakened and the result must say so.

## Supporting control: invention sketch (not learner machinery)

A separate researcher-authored function `sketch_step` scans the
n=6 discovery buffer for a single subject-ordered split into two
constant clusters. It is NOT added to the learner menu; it runs
only as a control to show the families are learnable in principle
(one scan), so that failure implicates the menu, not the data.

Predicted sketch outputs: G buffer -> 1 (fits, t=6003). H buffer
-> 0 (needs two thresholds; correctly refuses). A buffer -> 0
(LIN values all distinct; correctly refuses).

The sketch is not a kill bar. It is reported for interpretation.

## Kill bars

- K1 (spec): PASS iff the run emits the three SPEC lines above
  verbatim and executes all six predicted runs.
- K2 (behavior): PASS iff all six adopted/cost pairs match the
  frozen predictions table exactly.
- K3 (invention requirements): PASS iff the result document
  specifies the machinery a learner would need to invent the
  fourth form, covering at minimum: failure diagnosis from fit
  residuals, a fixed constructive operator vocabulary, failure
  driven candidate generation, a promotion protocol with novelty
  check, and revision on later counterevidence, plus the C0
  mapping for a genuine invention claim.
- K4 (purity): PASS iff pure Zag at every stage (znc, bash, grep,
  git only; zero Python invocations in source, build, execution,
  or analysis), zero em-dash/en-dash bytes in wave files
  (byte-checked), prereg strictly precedes implementation
  (git merge-base --is-ancestor), 3/3 byte-identical runs,
  exit 0, zero stderr.

Verdict INVENT-TESTED iff K1..K4 all pass. The verdict concerns
the test, not an invention claim: the expected finding is that
the learner does not invent the fourth form.

## Governance

- No change to fit_*, predict, prior_order, verify_need,
  run_family. The learner under test is byte-equivalent in
  behavior to lscale.zag on families 0..5.
- The sketch is never called during run_family. Anti-treadmill:
  no new operator or form is added to the learner as a result
  of this experiment.
- Commits local on tnn-native-lab, owned path form_invent/ only.
  No paper edits.
