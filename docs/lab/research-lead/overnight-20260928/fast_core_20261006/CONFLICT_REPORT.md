# Conflict is rejected, pollution scales linearly, ambiguity is detected

Date2026-10-07. Prereg6220d44f0. Generic object arena prototype (add1/double
primitives, binary composition, shortest-first enumeration,4096 cap). NOT frozen-core
integration. Two renames (primitive codes swapped, arena IDs shifted) give identical
numbers; all bars passed, instrumentation_unexpected0.

## T-A True negative transfer (order conflict)

Target T=2x+1 = [double,add1]. Wrong short token W=[add1,double]=2x+2 injected first.

| Arm | Candidate tests | Primitive effects | Heldout x5..12 | Promoted root |
|---|---|---|---|---|
|Clean library|5|12|8/8|composition of [double,add1]|
|+ wrong token W|7|17|8/8|NOT W (new composite id)|
|+ W, flat-executed|7|17|8/8|NOT W|

The wrong token is enumerated (cost +2 tests) and rejected by the verifier. It is
never promoted: the acquired root is a fresh composite node id beyond the injected
wrong-token id range, and heldout stays8/8. H-safe confirmed; H-broken refuted on
this fixture. H-polluted confirmed as a small work cost. Flat arm ties exactly,
so no nesting-specific effect is claimed here.

## T-B Library pollution scaling

K distinct wrong composites [add1^j,double] = 2x+2j, j=1..K.

| K | Candidate tests | Primitive effects | Heldout |
|---|---|---|---|
|0|5|12|8/8|
|4|13|44|8/8|
|8|21|108|8/8|
|16|37|332|8/8|
|32|69|1164|8/8|

Candidate tests are exactly linear: tests = 2K+5. Executed primitive effects grow
superlinearly because longer distractor programs cost more per probe. Correctness is
never lost. This is measurable negative transfer pressure: a polluted library taxes
every future acquisition. No asymptotic claim beyond K<=32 and length<=6.

## T-C Honest abstention under ambiguity

Train target2x+1 on P1={0}, P2={-2,0}, P3={-2,0,2}, P4=P3+{4}. Constructor enumerates
ALL fits within budget and groups them by outcome on fixed probe inputs {1,3,5,7}.

| Training set | Distinct outcomes | Behavior | Heldout x5..12 |
|---|---|---|---|
|P1 (one point)|6|ABSTAIN|-|
|P2 (two points)|1|answer|8/8|
|P3 (three points)|1|answer|8/8|
|P4 (+ witness)|1|answer|8/8|

With one observation, six different programs fit and disagree on heldouts (x+1,
2x+1, 4x+1 and longer equivalents). Abstention is correct: the world is genuinely
underdetermined. Adding the distinguishing witness collapses the set to one.
Probe inputs are a disclosed generic diagnostic, not answer labels.

**Cost of honesty:** ambiguity detection runs the full 126-candidate enumeration,
versus 5 tests for first-fit acquisition. Knowing-when-to-answer costs roughly25x
candidate work in this toy. That tradeoff must not be hidden; a production design
would need cheaper uncertainty estimates, and any such estimator is a new hypothesis
to test, not a free win.

## What this does and does not establish

Established in this prototype: verifier rejects attractive wrong shortcuts;
library pollution has predictable cost; the constructor can detect underdetermination
and abstain, and resolves when evidence disambiguates. Two encodings agree.

Not established: search order and grammar remain researcher-owned; no self-chosen
applicability, no learned proposal policy, no representation invention, no production
integration, no speed/memory claim. Probe-set selection is researcher-chosen. The
abstention mechanism enumerates a fully disclosed finite space, so this is bounded
knowing-when-to-answer, not open-ended uncertainty in natural domains.

## Reproduction

conflict_run.sh: pure-Zag report, unchanged frozen-core prefix compare, driver
loop/bar lint, three fresh native compile-gated runs with byte-identical nonempty
logs and binaries, source/compiler/PREREG hashes. bash -n and git diff --check.
No check failed.

NEXT: make proposal order and retention consequence-sensitive so pollution cost
drops without losing coverage; compare against frequency/cost-ranked flat library at
equal total work. Only then ask whether experience-built organization changes HOW
methods are generated rather than merely which macros are available.
