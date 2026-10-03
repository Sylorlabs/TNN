# PREREG H-PI-REV2: Procedure-Invention v2 Revision Machinery (FROZEN)

**Date:** 2026-09-29 (wave-20260929-1721pdt, design lane first act)
**Parent:** H-REVISE (KILLED; PROC_REVISION_RESULT.md, 2026-09-29). v1
mechanism bounded L2+, 11/12 L3 criteria, failing #12 (revision after a
counterexample) on the RT2 impossibility proof.
**Status:** FROZEN. This file is committed alone, before any implementation
edit, build, or run. No amendments after the freeze commit.

## Relation to the 2026-09-29 strategic reorientation

Micah's reorientation (recorded 2026-09-29) freezes the REVISE
contradiction-guard lane at mature L2+ with no auto-continue. That lane
(vs3_revise, REVISE9/10/11) is a different mechanism from this prereg's
arc. H-PI-REV2 belongs to the procedure-invention frontier (his primary
frontier; L3 criterion 12, "revisable after a counterexample"), not to
the frozen REVISE lane, and it is not an automatic vN+1 successor: v1 was
KILLED on a genuine capability gap (the RT2 impossibility proof), not on
an edge case, and this prereg tests the missing capability, not a
hardening tweak.

Per the reorientation's result-label rule, the implementation wave
reports BUILD-PASS or BUILD-FAIL only. "SURVIVES" below is therefore
replaced: on all bars passing, the verdict is BUILD-PASS (bounded
revising mechanism, all frozen bars pass). Promotion to
SURVIVES/BOUNDED/DOWNGRADED/KILLED requires the full pipeline:
independent reproduction, baseline attack, OOD test, ablation, transfer,
independent adversary.

This prereg is designed against Mandatory L3 Criterion 0: current
language cannot represent the observed transformation (K-RV2-1(b)
rechecks the impossibility) -> learner detects inadequacy (monitor,
K-RV2-3) -> creates primitive P (K-RV2-1(a)(c)) -> P explains the
observations (P6/P7) -> solves hidden cases (F1-reuse, K-RV2-1(d)) ->
reused in another domain/class (F2 adversary, K-RV2-7) -> ablating P
removes the advantage (P9, K-RV2-2). Whether that amounts to Criterion 0
satisfaction stays with the verdict debate and the independent red team.

## What this prereg is and is not

This prereg freezes a fair empirical test of a revision architecture for
procedure invention. It does NOT claim the architecture satisfies L3
criterion 12, and it does NOT claim Micah's tightened L3 gate (recorded
2026-09-29: "Did TNN expand its own representational language? If the
answer is no, it remains L2+") is satisfied. The gate is operationalized
below as measurable sub-bars (K-RV2-1 a-e); whether they amount to
gate satisfaction is the verdict debate's call, with the standing skeptic
attacks (S1-S5) recorded for that debate. A SURVIVES verdict here means
"bounded revising mechanism, all frozen bars pass," not "L3 achieved."

## The impossibility this design answers

H-REVISE proved: no program with signature P(k,n) -> index can jointly
satisfy the Family X training sequences and the counterexample sequence
("abc"->"ccc" needs P(k,3)=2; "xab"->"xxx" needs P(k,3)=0; identical
(k,n) inputs, contradictory outputs). K-RV2-1(b) rechecks this on the
ported implementation: the v1 DSL provably cannot express the revision.
The v2 architecture answers by letting the learner construct a new
content-test primitive from data, so the revised procedure's effective
signature includes input content. The construction machinery is generic
and frozen below; the specific primitive is data-derived.

## Architecture (frozen)

Built by porting the frozen H-REVISE discovery enumeration from
sem_l3/proc_revise_test.zag verbatim (cmp-verified port, declared at
implementation time; that file is frozen history, not under active
development). New file: sem_l3/proc_revise2.zag. The port must pass
K-RV2-5 (discovery regression). Pure Zag. Pinned znc 498abcb5.

New machinery (generic, frozen here):

1. **Procedure store.** Persistent, versioned. Each version: {id, program,
   provenance {created_by, trigger_example, diagnosis, parent_version},
   status}. Statuses: ACTIVE, SUBSUMED (retained as a component of a
   later version), SUPERSEDED-EXAMPLE (applies to example records, not
   procedures; see conflict rule). ROLLBACK(v) reactivates v.
2. **Example log.** Every observed (input, output) with status CURRENT or
   SUPERSEDED. Examples are never deleted.
3. **Monitor loop.** After discovery, new examples arrive through
   observe(input, output). The monitor predicts with the ACTIVE procedure
   and compares. On mismatch it emits COUNTEREXAMPLE_DETECTED(input) and
   triggers diagnosis. The observe() path contains no branch on input
   content; detection is purely predict-vs-actual mismatch (audited,
   K-RV2-3).
4. **Diagnosis operator.** Given failing set F and passing set P (from the
   example log under the ACTIVE procedure): enumerate candidate
   conditions (position p, byte b) such that every f in F has byte b at
   position p. Rank: position p ascending (frozen simplicity bias:
   earlier positions preferred as condition sites; disclosed, attacked
   in S5). Conflicts with P do not disqualify; they are recorded.
   Output: the top-ranked (p, b) plus the list of conflicting P examples.
   If no candidate exists: emit CANNOT-DIAGNOSE (honest abstention; the
   revision test is then INCONCLUSIVE, not a pass).
5. **Primitive-construction kit** (generic bounds, disclosed): from a
   diagnosed (p, b), mechanically construct the test primitive
   P_test(input) = (input[p] == b). The kit can only build byte-equality
   tests at positions (bounded scope, S2). The literal bytes ('x', the
   adversary's c) must not appear in the diagnose/construct/revise
   functions; they flow from data (audited, K-RV2-7).
6. **Revision operator SPECIALIZE.** v_new = IF(P_test, alt, v_old), where
   alt = smallest v1-DSL program fitting F's index sequences (re-run of
   the ported search, restricted to F), v_old = the ACTIVE procedure.
   Append v_new to the store with provenance {trigger, diagnosis (p,b),
   parent v_old}.
7. **Conflict rule** (newer trusted evidence overrides): a passing
   example that satisfies P_test but was observed under v_old is marked
   SUPERSEDED in the example log (provenance: overridden by the revision
   trigger; retained, never deleted). Trust assumption (disclosed
   residual): observed examples are trusted; forged counterexamples would
   cause spurious revision (not tested here).

## Frozen fixtures

- **T (Family X training):** ("abc"->"ccc"), ("xy"->"yy"),
  ("defg"->"gggg"). Expected P0 discovery: [N C1 SUB] broadcast-last
  (index 38 as in H-REVISE Phase 1; semantic check n-1 for n=1..6).
- **F1 (design-visible counterexample, the exact H-REVISE fixture):**
  ("xab"->"xxx"). Extraction: 'x' occurs once in "xab" at index 0, so
  seq [0,0,0] extracts cleanly (RT2-C unambiguous case).
- **F1-reuse (held from the learner until after revision):**
  ("xqw"->"xxx"). Tests within-class generalization of the invented
  primitive with no further revision.
- **F2 (adversary-sealed):** generator frozen here; instance chosen by
  the red team at verdict time. The red team picks c from the allowed
  set {i,j,k,l,m,n,o,r,t,u,v,w} (lowercase letters occurring nowhere in
  T/F1/R inputs and not as a first byte of any R input, so the F2 class
  is disjoint from all frozen evidence). Counterexample: (c+"ab" ->
  c+c+c). The implementation exposes argv[1]: if present and a single
  allowed letter, main() runs the F2 phase after P7. Single execution at
  verdict; the designer may not iterate on F2.
- **R (regression cell, 8 pairs from RT2-A):** ("zag"->"ggg"),
  ("12"->"22"), ("q"->"q"), ("hello"->"ooooo"), ("ptc"->"ccc"),
  ("s"->"s"), ("eghjjupazbnf"->"ffffffffffff"), ("q"->"q") [the last
  repeats the disclosed/hidden pair from the two RT2-A phases].
- **V1 discovery regression:** PI-1a reverse (("abc"->"cba"),
  ("def"->"fed"), ("xy"->"yx"), ("hello"->"olleh")) and PI-1b identity
  (("abc"->"abc"), ("xy"->"xy")), no counterexample present.

Note on the design-lane "875-regression cell": the 1421pdt design lane
mentioned an "875-regression cell" as a mandatory kill bar. No 875-case
regression cell exists in any committed document (searched sem_l3,
preregs, run records); the reference is ungrounded. This prereg defines
its regression cell exactly as R above. If the note's author produces
the 875-case cell, it may be added by prereg amendment before
implementation.

## Frozen protocol (phases)

- **P0 discovery.** Train on T. Emit discovered program + search trace.
- **P1 store.** v1 stored ACTIVE with provenance {discovery, T}.
- **P2 monitor.** observe("xab","xxx") through the unflagged channel.
  Expected: predicts "bbb", actual "xxx", COUNTEREXAMPLE_DETECTED("xab").
- **P3 diagnosis.** F={"xab"}, P={"abc","xy","defg"}. Expected:
  (p=0, b='x'), with conflict recorded: "xy"->"yy" has 'x' at 0.
  Candidates (1,'a') and (2,'b') are clean but lose on the frozen
  position-ascending rank.
- **P4 construction.** P_x(input) = (input[0]=='x'), mechanically built
  from (0,'x').
- **P5 alternative search.** Smallest v1-DSL program fitting F's
  sequences. Expected: C0 (broadcast-first; evaluates to 0 for all k).
- **P6 revision.** v2 = IF(P_x, alt, v1). v1 status -> SUBSUMED
  (else-branch of v2). "xy"->"yy" example -> SUPERSEDED (overridden by
  F1; retained with provenance).
- **P7 verification.** Predictions: "abc"->"ccc" (unchanged),
  "xy"->"xx" (CHANGED: frozen expected consequence of the conflict
  rule), "defg"->"gggg" (unchanged), "xab"->"xxx" (fixed).
  observe("xqw","xxx"): monitor predicts "xxx", no new revision.
  R: 8/8. Full run 3/3 byte-identical.
- **P8 adversary F2.** Red team runs the frozen binary with argv[1]=c.
  Expected: detection, diagnosis (0,c), v3 = IF(P_c, alt_c, v2),
  "mab"-class correct, all prior predictions unchanged (c is disjoint).
- **P9 ablation.** ROLLBACK(v1): "xab" mispredicted again ("bbb"), T
  predictions restored ("xy"->"yy"). Causal evidence the specialization
  does the work.

## Frozen kill bars

- **K-RV2-1 (L3-gate operationalization).** ALL of: (a) the invented
  primitive P_x appears nowhere in source before revision (grep audit
  over the implementation; only fixture declarations and
  expected-output strings may contain the byte); (b) the v1 DSL cannot
  jointly fit T+F1 (recheck the H-REVISE impossibility on the port: no
  P(k,n)->index program satisfies the failing+passing sets); (c) the
  white-box trace shows (0,'x') derived from the F-vs-P comparison via
  the frozen diagnosis; (d) reuse: F1-reuse correct with no further
  revision, and F2 revised correctly on first execution; (e) P_x
  persists in the store as the ACTIVE procedure's condition.
- **K-RV2-2 (not re-search).** v1 structurally contained as the
  else-branch of v2 (trace/structural check); version history v1->v2->v3
  with provenance; ROLLBACK(v1) restores exactly v1 behavior.
- **K-RV2-3 (autonomous detection).** F1 detected via predict-vs-actual
  mismatch; audit shows no content-based branching in observe().
- **K-RV2-4 (regression cell R).** 8/8 post-revision (after P6 and after
  P8), 3/3 deterministic byte-identical.
- **K-RV2-5 (discovery regression).** Port discovers reverse (PI-1a)
  and identity (PI-1b) with no counterexample present.
- **K-RV2-6 (determinism).** Full P0-P7+P9 run 3/3 byte-identical.
- **K-RV2-7 (generality / anti-tuning).** F2 passes on first execution;
  grep audit post-disclosure: the adversary's c appears nowhere in
  machinery outside data flow; no 'x' literal in
  diagnose/construct/revise functions.

Verdict on all bars passing: BUILD-PASS (bounded revising mechanism, all
frozen bars pass). The implementation wave may not promote to SURVIVES.
Promotion requires the full pipeline: independent reproduction, baseline
attack, OOD test, ablation, transfer, independent adversary, yielding
SURVIVES/BOUNDED/DOWNGRADED/KILLED. The L3-criterion-12 claim and
Criterion 0 stay open for that pipeline and the independent red team.

## Standing skeptic attacks (recorded for the verdict debate)

- **S1 (researcher-added-primitive).** The construction kit is
  researcher-supplied; Micah's NOT-count list bars "the researcher
  adding a primitive after a hidden failure." Prereg answer: the kit is
  generic and frozen before F2 is known; the specific primitive is
  data-constructed. Whether that satisfies the gate is the debate's call.
- **S2 (kit boundedness).** The kit invents only byte-equality tests at
  positions; a counterexample needing another primitive shape yields
  CANNOT-DIAGNOSE. Bounded scope, disclosed, not a general reviser.
- **S3 (menu at one remove).** The diagnosis space (positions x 256
  bytes) is finite; defense: the specific (p,b) is data-selected and the
  composed conditional was never enumerated as a complete candidate.
- **S4 (position-ascending bias).** An unprincipled salience prior that
  matches the tester's intent; a "second letter" world would need a
  different bias. Frozen, generic, disclosed; reuse/adversary tests
  constrain gerrymandering.
- **S5 (trust).** Observed examples are trusted; forged counterexamples
  cause spurious revision. Residual, not tested.

No Python. No em-dashes in wave documentation. This prereg is committed
alone, before any implementation edit, build, or run.
