# Conflict, pollution and honest abstention prereg

Date2026-10-07. Prototype successor to OBJECT_PREREG.md (b64349a89). Same generic
object arena: two integer primitive effects add1/double, binary composition objects,
shortest-first enumeration,4096 candidate cap, generic verifier. Rename swaps the
two primitive numeric codes and shifts arena IDs. No task names, no final methods
preloaded, no task-specific branches.

## T-A True negative transfer (order conflict)

Target T=2x+1 (composition [double,add1]). Before acquisition, inject one WRONG
short composite token W=[add1,double] =2x+2 (fits nothing in training). Hypotheses:
H-safe verifier rejects W (never promoted, heldout correct);
H-polluted W is attempted and inflates work; H-broken W accepted (wrong heldout).
Measure candidate tests, primitive effects, and heldout correctness x5..12.
Compare clean arena (no W). Also flat-executed variant of the same library as a
consistency control (ties expected; no nesting claim being tested here).

## T-B Library pollution scaling

Inject K distinct wrong composite tokens ([add1 repeated j,double] =2x+2j,
j=1..K), K=0,4,8,16,32. Same target and training. Measure candidate tests and
primitive effects as function of K. Hypotheses: H-flat work constant;
H-growing work grows with library; H-explosive grows superlinearly.
Correctness must stay8/8 in all K. This is negative transfer pressure, not an
efficiency claim.

## T-C Honest abstention under ambiguity

Training point sets for target2x+1:
P1={x=0}, P2={x=-2,0}, P3={x=-2,0,2}, P4=P3+{x=4} witness.
Generic constructor enumerates ALL fits within budget, computes each fit's output on
a fixed probe set {1,3,5,7} (probe inputs are NOT answer labels), counts distinct
outcome vectors. If distinct>1 -> abstain (-999999). If distinct==1 -> answer and
score heldout x5..12 (excluding training points).
Bars: P1 must ABSTAIN (multiple fits disagree on heldouts: x+1,2x+1,4x+1 all fit
x=0->1); P2,P3,P4 must answer uniquely and correctly8/8; adding the P1 witness must
move distinct from>1 to1. Renamed encoding must match.
This tests knowing-when-to-answer, not task-specific semantics. If P1 answered,
that is a documented overclaim failure to preserve, not a bar to relax.

## Scope limits

No self-chosen applicability, no learned search policy (enumeration order is still
source-owned), no representation invention, no production integration, no speed or
memory claim. Probe-set choice is a disclosed generic diagnostic, not learned.
Artifacts: CONFLICT_PREREG.md, conflict_driver.zag, conflict.zag, conflict_run.sh,
conflict_environment.txt, conflict_provenance.txt, conflict_compile1..3.txt,
conflict_run1..3.txt, CONFLICT_REPORT.md in fast_core_20261006/. Fresh native
compile-gated repeat3, nonempty byte-equal logs/binaries, pure-Zag science, prefix
integrity of unchanged frozen core, driver loop/bar lint, bash-n, diff-check.
Failures preserved; no bar moved after data. Local commits only, no push/merge.
