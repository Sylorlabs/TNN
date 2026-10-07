# Fast iteration 2 - scorer, control, and method forks

Base ownership 91b2acc29; prior fast checkpoint 58482c9c1.
Private branch fast/method-identifiability. Original source and histories untouched.
Write before drivers. No AGI/L3 promotion. Pure Zag scientific computation.

## A. Scorer qualification
QUESTION: can bounded endpoint-set parsing fix first-endpoint greediness without
changing the represented production tables?
H0: original matcher exact enough; H1: endpoint-set composition is required.
FORKS: original greedy matcher, iterative depth-indexed chart of all endpoints,
independent hand-language oracle (labels only). Do not use chart-generated labels.
MINIMUM WORLDS:
1. Original fixed fixture, all 340 strings length 1..4 over 3..6; designated root
   A0 accepts {334}, any-NT accepts {33,334,3345}.
2. Overlapping alternatives A0->A1 4; A1->3|34, both rule orders and terminal rename.
   root {34,344}, union {3,34,344}; 340 queries each.
3. Genuine recursive A0->34 | 3 A0 4; A1/A2 empty. All 510 strings length 1..8
   over {3,4}, both orders and terminal rename. Root/union language 3^n4^n,
   n=1..4. Depth cap 8 cannot exclude any valid tested string.
4. Left-recursive A0->34 | A0 4; A1/A2 empty, same 510 strings/orders/rename.
   Root/union language one 3 followed by n 4s, n=1..7. Chart must handle left
   recursion because previous-depth cells are used, not same-depth recursion.
5. Explicit depth bound: balanced grammar cap=1 allows n<=2 (root at depth0,
   child at depth1). Valid deeper strings are bound exclusions, not learning failures.
CONTROLS: empty table rejects all; rule/terminal permutations; original fixture;
whole-string consumption; root separately from union. Chart recurrence includes
one layer for depth0; all 9 layers cover NT depth0..8.
BAR: chart vs oracle zero false positives/negatives in every declared condition;
original matcher must reproduce earlier ambiguous signature. Report greedy errors
in recursive conditions, do not require a prediction for every individual count.
Forward generator returns one witness, not exhaustive generation; membership must
accept the oracle-valid witness but generation coverage is not established.
KILLS: broken implementation if chart disagrees, not grammar representation.
NEXT: only qualified scorer may grade depth induction.

## B. Control forks
QUESTION: can generic explicit controls preserve stored rejects and isolate histories?
FORKS growth: unchanged hull u_grow; atomic grow-if-no-known-reject; fresh u_induct.
Use earlier accepts 2,4 reject6 new success8. Gate copies candidate arena, grows,
checks retained reject table, commits iff none admitted. Expect gate rejects update
and keeps reject6 excluded but cannot learn success8; reinduct learns8 preserving6.
Report all grid1..10 and heldout-only1,3,5,7,9,10; no generalization claim from fit.
Additional attack: one-field positive interval [2,4] historical negative x=10;
grow to8 passes known-reject gate but admits unobserved forbidden x=6. Distinguish
known-counterexample preservation from complete authorized safety.
FORKS locality: original shared arena; separate arenas; context-local wrapper over
unchanged API (copy a contract + its judgment/history into isolated temporary
execution arena, copy results back). Three A failures, B revision call, then A
revision call. Explicit per-contract contexts, no task/world labels.
Expect original shared B rev=1; separate/local B rev=0 and A req survives B call;
A rev then1. Record that wrapper copy cost is unmeasured, no production integration.
A judgment window and B window distinct; no leaked shared labels into local contexts.
KILLS: proposed fork if bars fail; passing is engineering control, not learned policy.
NEXT: actual-effect authority guard and revocation/alias/replay path tests.

## C. Uncacheable method ownership and disambiguation
QUESTION: can a generic compositional learner acquire a reusable executable method
on heldout inputs, and does its benefit survive strong simple non-program rivals?
This is NEW EXPLORATORY MICRO-LEARNER, not canonical TNN and not a repair of P5.
Primitive library step(z,op,arg): op0=z+arg; op1=z*arg. Constants -2..3,
program lengths1..2; declared count: 12 length1 + 144 length2 =156 candidates. No complete target
program literal in learner. Enumerative synthesis from training observations
is deliberately a rival-explainable L2 method acquisition, NEVER L3.
World family: f(x)=a*x+b, a1..3,b-2..2 (15 worlds), independent arithmetic oracle.
Train x=-2,0,2; heldout x=5..12 (never-observed values). Fixed order generic menu;
persistent program candidate ID decoded generically; evaluator has no world label.
ARMS: retained program only (facts erased); facts only exact lookup+abstain;
method erased facts retained; fresh no-data menu first candidate; recompute same
enumeration from retained facts; affine slope/intercept interpolation using same
observations; equal-candidate-budget uniformly selected menu, exact expectation
by exhausting all156 candidates, not lucky single RNG draw.
BARS: retained program correct120/120; facts lookup0/120 with abstention; method
erasure removes benefit; recompute and affine interpolation also correct120/120.
Report candidate evaluations (not wall-time speedup) for acquisition/recompute.
This proves learned executable state is sufficient in this tiny family, not necessary
versus a flat sufficient statistic, not meta-learning, not integration, not AGI.

DISAMBIGUATION fork: two possible laws f=x and f=2x; first observation x0->0
cannot distinguish. Enumerate consistent candidates and abstain if predictions
at x3 disagree. Both possible worlds must get identical pre-witness uncertainty.
Then observe x2->2 or x2->4: query x3 must predict3 or6 respectively; facts-only
still cannot replayx3. No target/world identity delivered to learner.
REVISION fork: overwrite observations for same inputs when new law arrives;
reacquire method via same source code; evaluate fresh heldout band. Report source-
fixed revision, not self-invented revision policy (overwrite/reinduct researcher rule).
NEGATIVE attack: unseen world x*x not expressible in this library on train -2,0,2;
no consistent method, learner must abstain rather than source patch or false success.
NEXT: ask whether same-state transfer helps acquisition on laws outside fixed DSL;
source-enumeration and simple-statistic controls survive any positive.

## Execution and artifacts
Prereg commit precedes implementation. Each driver plus original prefix assembled
by shell, all scientific oracles/comparisons in Zag. Artifacts in this directory:
PREREG.md, scorer_driver.zag, scorer.zag, control_driver.zag, control.zag,
method_driver.zag, method.zag, run.sh, REPORT.md, environment.txt, provenance.txt,
{scorer,control,method}_compile{1,2,3}.txt and _run{1,2,3}.txt.
Fresh compile gates run; nonempty output; exit1 on bar discrepancy; repeat3 hashes.
Generated binaries ignored. Source and original-prefix integrity checked. New source
lint and shell syntax checked. Unexpected observations retained before any repair;
repairs explain cause and rerun affected checks without moving scientific bars.

## Ongoing-loop boundaries
Complete successive falsifiers while session execution permits; no unbounded shell
job pretending to be an AI researcher. Every checkpoint states done vs planned.
Test explicit reasonable forks, not an impossible promise to exhaust all designs.
No push/deploy/core merger without user authorization. Do not alter historical logs.
