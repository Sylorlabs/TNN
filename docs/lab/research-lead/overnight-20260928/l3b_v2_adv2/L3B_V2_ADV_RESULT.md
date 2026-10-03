# L3B v2 independent adversary: results

Target: constructor-level redesign, implementation 7a1d3265d (L3B-V2-PASS,
bounded L2). Attack prereg PREREG_L3B_V2_ADV.md frozen alone at 42538c6b6;
addendum PREREG_L3B_V2_ADV_ADDENDUM.md frozen alone at 252440aa4.
Pure Zag, no Python at any stage. Contaminated paper untouched.

## Run 1 verdict: L3B-V2-ADV-FAIL (hand-derivation error)

Observed `ADV-FAMD done creates=8 dispatches=1 recallok=1/1 revisit=2`
against the frozen prediction `revisit 3/3`. All other families matched:
A hidden 0/3, creates 0, nogrowth 2; B hidden 0/3, creates 0, nogrowth 2;
C creates 3, dispatches 3, recallok 3/3; E boundary probe behaved as
predicted. The single miss was my arithmetic: the frozen step() tallies
ONLY in the direct-prediction branch (`if(ok==1)`); a successful
try_dispatch sets disp=1 and resets the failure counter without tallying.
Family D revisit is n=21 dispatch (no tally) + n=22, n=23 direct hits
(2 tallies). Corroborated by the builder's own FAM2 run, which reports
`final=1` from its 2-episode revisit. The mechanism behaved per source;
the adversary's derivation was wrong. The FAIL verdict stands for run 1
and is not reinterpreted.

## Correction (transparent, pre-run-2)

Addendum 1 (252440aa4, committed alone before run 2) amends D-REVISIT3
from `ig(cnt,0)==3` to `ig(cnt,0)==2`, derived from the frozen source and
corroborated by the builder's independent run. No mechanism bar was
weakened: creates=8, dispatches=1, recallok=1/1, the dispatch signatures,
and the no-9th-version requirement are unchanged.

## Run 2 verdict: L3B-V2-ADV-BOUNDED

3/3 runs byte-identical (exit code 1 on all three: see Family E).

Family A (depth-3 required, tl2=n^4): TRACE-NO-GROWTH why=nosearch2
(twice: once on training, once on hidden), hidden 0/3, creates 0.
The 205-program grammar cannot express degree 4; the mechanism tried and
honestly failed. No smuggled semantics. A-NOSEARCH/A-HIDDEN0/A-CREATE0 PASS.

Family B (constant 12 outside 0..8, tl2=n+12): TRACE-NO-GROWTH
why=nosearch2 (twice), hidden 0/3, creates 0. Max p(1) over in-grammar
programs is 10 < 13, so the failure is provable from the grammar, and the
mechanism reports it rather than forcing a fit. B bars PASS.

Family C (ambiguous dispatch): creates 3, dispatches 3, recallok 3/3.
Signatures confirmed exactly as frozen: reactivation
`TRACE-DISPATCH from=3 to=2 on=21`; ambiguous probe at n=6 under R3p law
picks the WRONG version by the first-match rule
`TRACE-DISPATCH from=2 to=1 on=6`; correction
`TRACE-DISPATCH from=1 to=3 on=7`; stability at n=8,9. The mechanism has
no ambiguity representation: on an ambiguous observation it silently
commits to the lowest-index match and must fail once before correcting.
No 4th version was created; no never-constructed version was recalled.
C bars PASS. The wrong-pick-then-correct pattern is honest but crude;
a future redesign should represent ambiguity explicitly rather than
fail-then-redispatch.

Family D (8-version churn + revisit): creates 8 with all eight predicted
TRACE-CREATE key lines confirmed
(V,(A,V,V)), (V,(A,V,C4)), (V,(A,V,C6)), (V,(S,V,C2)),
(V,(M,V,C3)), (V,(M,V,V)), (V,(A,V,(A,V,C1))), (V,(A,V,C1));
revisit `TRACE-DISPATCH from=8 to=1 on=21` with node-id equality
(recallok 1/1), revisit tally 2/3 per the corrected prediction,
creates stays 8. D bars PASS. The version archive recalls rather than
rebuilds under churn.

Family E (9th distinct version, same lifetime as D): the 9th CREATE
attempt executes do_fire with vn=8 against 8-entry archive arrays.
The znc runtime traps the out-of-bounds write:
`panic: slice index out of bounds`, exit code 1, identical 3/3.
Source audit confirms do_fire contains no archive-capacity check.
BOUNDARY finding (not a BREAK input): the mechanism has no principled
response to archive exhaustion. It does not silently corrupt (the runtime
caught it), but a 9th genuinely-new regime is unrepresentable and the
source offers no guard, eviction policy, or error path. Fix required
before any integration: either a capacity discipline in do_fire or an
explicit archive-full signal the learner can observe.

No BREAK condition fired in either run: hidden 3/3 never occurred,
no 4th version in C, no 9th version in D, no recall of a
never-constructed version.

## Kill bars

K1 (prereg committed alone first): PASS. 42538c6b6 strictly precedes all
implementation; addendum 252440aa4 strictly precedes run 2
(merge-base verified).
K2 (all primary predictions match 3/3 byte-identical): PASS on run 2
(13/13 primary bars; run 1 recorded its FAIL honestly).
K3 (pure Zag + shell, u8 cells, no em dashes, contaminated paper
untouched): PASS (shell dash check over all lane files; mechanism
byte-identical to the u8-cell implementation).

## ONE-SYSTEM RULE accounting

Cognition source lines added: 0. New hardcoded semantic cases: 0.
New modes: 0. New bridges: 0. New task-specific handlers: 0.
New learner-state structures: 0. The sealed worlds are attack fixtures in
a replaced main(), never proposed for adoption. Capability-source delta
is zero by construction: the harness asserts the reference mechanism is
a verbatim 652-line prefix of the attack file and the interpreter region
is sha256-identical (aee8090b1429e6206d26d6822ecb6a50f79def7da8cdaf8ae23c2bd5632e480d).

## Interpretation

The constructor-level redesign survives its independent adversary with a
bounded L2 ceiling intact. The honest boundaries are real: the
205-program enumeration is a finite menu with provable edges (degree 3,
constants 0..8), and the mechanism reports menu-exhaustion instead of
forcing fits. Dispatch recalls by node identity under churn. Two
load-bearing limitations are now documented for the redesign lane:
(1) ambiguous observations resolve by silent first-match with no
ambiguity representation; (2) archive exhaustion has no source-level
guard. Per the standing lane ruling, the next step is redesign toward
incremental construction, never grammar expansion.
