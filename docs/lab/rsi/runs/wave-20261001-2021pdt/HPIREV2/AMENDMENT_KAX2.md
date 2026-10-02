# AMENDMENT K-AX2: repaired template-aware comparator B4b for H-PI-REV2 step 6

Status: DRAFT AMENDMENT. Not frozen until the coordinator commits this
document alone; the commit-order self-check at the end applies;
UNVERIFIABLE ORDERING voids the re-execution.

Amends: PREREG_PI_REV2_STEP6.md as committed at 042318b7b (the frozen
step-6 prereg for the H-PI-REV2 mechanism, wave-20261001-2021pdt).

Cause: the step-6 verdict (S6_VERDICT.md) was FAIL, cause K-AX2 VOID.
The K-AX2 competence clause ("first_fit >= 0, else void, not a kill")
is unsatisfiable for the B4 the frozen prereg specifies: the specified
stream (1055 benum programs plus 768 single-branch IF completions)
contains no candidate achieving fails=0 on the 5 conflict-updated
checks, by the structural argument recorded in S6_VERDICT.md and in
S6_EXECUTION_LOG.md section 8 (no benum program can fit abc at n=3
needing eval 2 with rab at n=3 needing eval 0; no single IF can branch
on both 'x' and 'r' while leaving abc/defg on v_old). A voided
alternative is neither killed nor tripped, so step-6 PASS was
unreachable under the frozen text through no fault of the mechanism or
the implementation. Per the frozen prereg, void is explicitly not a
kill and not a kill-bar trip; the verdict recommended exactly this:
amend and re-freeze K-AX2, then re-execute.

## Scope: what is preserved unchanged

This amendment replaces ONLY:
(a) the A2/B4 comparator definition, with the A2/B4b definition below;
(b) the K-AX2 bar text, with the amended bar below;
(c) the K-SB5 run-matrix naming (B4 x3 becomes B4b x3);
(d) the b4 cost-accounting field names (become b4b fields).

Everything else in the frozen prereg is preserved verbatim and
unchanged: all 8 step-5 bars (K-SB1, K-SB2, K-SB3, K-SB4a, K-SB4b,
K-SB4c, K-SB5, K-SB6) with their thresholds, K-AX1, K-ABL1, K-ARCH1,
K-ARCH2, the verdict rule, the never-SURVIVES rule, the sealed
evaluation design and adversary protocol, the code-sharing disclosure
requirement, the cost-accounting rule, the honest-boundaries section
(bounded L2 ceiling, not L3), and the pipeline position statement. The
frozen mechanism (proc_revise2.zag at 847a8f10f), the frozen fixtures
T/F1r/F1r-reuse, the frozen K-SB4a expectations, and the adversary byte
are untouched.

## The key design decision

The defect was expressiveness, not effort. The 5 conflict-updated
checks require TWO branches (a branch on 'x'=120 for xy, a branch on
'r'=114 for rab/rqw, with abc and defg staying on v_old), while the
specified B4 stream contains only single-branch candidates. The repair
is the minimal expressiveness repair: nest the prereg's own template
shape twice. B4b's template candidates are

  IF(byte-equality(pos1,byte1), alt, IF(byte-equality(pos2,byte2), alt, v_old))

with pos1,pos2 in {0,1,2} and byte1,byte2 in 0..255, enumerated in one
fixed frozen order (pos1 ascending, then byte1 ascending, then pos2
ascending, then byte2 ascending), concatenated after the 1055 benum
programs in frozen dsearch order. No new operators, no disjunctions,
no researcher-authored branch conditions: the exact IF shape from the
frozen prereg, nested. alt is the first program in frozen dsearch order
fitting F1r alone (measured S6 index 2); v_old is the frozen v1
procedure (measured S6 index 38, first fit on T); both are computed by
the frozen dsearch procedure, never hardcoded. B4b uses no diagnosis,
no ranking, no conflict rule, no rollback: it is blind fixed-order
enumeration over a template-completed space, which is exactly what
"template-aware re-search" means.

Alternatives considered and rejected:
- Keep single-branch B4 and weaken the competence check set: rejected,
  because the efficiency claim under attack is about the 5
  conflict-updated checks; a reduced check set would test a different
  claim.
- Keep single-branch B4 and drop the competence clause: rejected,
  because the clause is what keeps the comparator honest (a
  non-solving baseline is a strawman); dropping it would let a broken
  comparator "kill" the claim.
- Add a two-byte-disjunction template such as
  IF(input[0]==114 OR input[0]==120, ...): rejected, because that
  smuggles researcher knowledge of the answer into the baseline's
  operator set; nesting the prereg's own shape adds expressiveness
  without adding knowledge.

## The B4b specification (frozen by this amendment)

- Candidate stream, in order:
  1. The 1055 benum programs in frozen dsearch order (indices 0..1054).
  2. The nested two-branch template completions: for pos1 in {0,1,2},
     for byte1 in 0..255 ascending, for pos2 in {0,1,2}, for byte2 in
     0..255 ascending: candidate = IF(byte-equality(pos1,byte1), alt,
     IF(byte-equality(pos2,byte2), alt, v_old)). That is
     9 * 256 * 256 = 589,824 candidates. The old B4's 768
     single-branch completions are NOT included: they were proven in
     S6 to never fit, so carrying them would complicate the proof
     without changing any verdict.
  Stream total: 1055 + 589824 = 590879.
- Fitting procedure: evaluate each candidate in stream order against
  the 5 frozen K-SB4a checks (abc->ccc, xy->xx, defg->gggg, rab->rrr,
  rqw->rrr); stop at the first candidate with fails=0.
- Metrics: b4b_first_fit_index = the 0-based stream index of the first
  full fit, or -1 if none fits; b4b_enumerated = candidates evaluated
  until the first full fit (inclusive count), or -1 with
  b4b_stream_total reported if none fits.
- Competence check (negative control, retained in form, repaired in
  substance): B4b must return b4b_first_fit_index >= 0. A B4b failing
  to solve the set is a broken baseline and the run is void, not a
  kill. Unlike the old B4, this clause is satisfiable, proved below.
- Code-sharing disclosure (unchanged in spirit): B4b may reuse only the
  frozen benum algorithm and the template shape stated here; no
  Section B revision-machinery code (diagnose, build_test, specialize,
  conflict rule, rollback) may appear in B4b; the red team audits for
  leakage. The implementer is a different agent from the amendment
  author.
- Sealing (unchanged): B4b has no constructor phase; the F1r-reuse
  input "rqw" appears only as a check pair.

## Satisfiability proof (by construction, with the concrete numbers)

Frozen measured facts used (all from S6 execution evidence or derived
from the frozen source semantics; none are assumptions):
- alt (S6 measured index 2, first dsearch fit on F1r alone) behaves as
  copy-input[0]: abc->aaa, xy->xx, defg->ddd, rab->rrr, rqw->rrr
  (S6_EXECUTION_LOG.md section 7, D1 transcript).
- v_old (S6 measured index 38, displayed [N C1 SUB]) behaves as
  copy-input[n-1] by the frozen eval_node semantics (SUB of N and C1):
  abc->ccc, xy->yy, defg->gggg, rab->bbb (S6 measured), rqw->www
  (derived: last byte 'w' repeated).
- eval_prog is a deterministic pure function of (prog,k,n); no benum
  program fits the conflict-updated set (K-SB4c verified
  impossibility, re-verified in S6: abc at n=3 needs eval 2 at every k
  while rab at n=3 needs eval 0 at every k).

Input bytes: abc=[97,98,99], xy=[120,121], defg=[100,101,102,103],
rab=[114,97,98], rqw=[114,113,119].

Exhibit: C* = IF(byte-equality(0,114), alt,
IF(byte-equality(0,120), alt, v_old)), at nested-loop position pos1=0,
byte1=114, pos2=0, byte2=120. Evaluate on the 5 checks:
- abc: input[0]=97, neither 114 nor 120, so v_old: ccc [ok].
- xy: input[0]=120, not 114, is 120, so the inner branch fires, alt:
  xx [ok].
- defg: input[0]=100, neither, so v_old: gggg [ok].
- rab: input[0]=114, the outer branch fires, alt: rrr [ok].
- rqw: input[0]=114, the outer branch fires, alt: rrr [ok].
fails=0. C* is in the specified stream at a fixed position; the
competence clause is satisfiable. This is not hand-waving: the
candidate, its stream position, and its per-check evaluation are all
explicit.

No-earlier-fit proof (so the efficiency comparison is meaningful). A
full fit requires, per check, given the frozen alt/v_old behaviors:
- abc: alt gives aaa, not ccc, so no branch may fire on abc.
- defg: alt gives ddd, not gggg, so no branch may fire on defg.
- xy: v_old gives yy, not xx, so at least one branch must fire on xy.
- rab: v_old gives bbb, not rrr, so at least one branch must fire on
  rab.
- rqw: v_old gives www, not rrr, so at least one branch must fire on
  rqw.

Benum prefix (indices 0..1054): no fit, by the verified impossibility
above.

Nested stream, index i = ((pos1*256+byte1)*3+pos2)*256+byte2; the
pos1=0 block comes first:
- byte1 < 114: the outer branch fires only on inputs with
  input[0]=byte1. The five checks' input[0] values are {97,100,120,
  114}. If byte1 is 97 or 100, the outer branch fires on abc or defg
  and alt predicts aaa or ddd: fail. Otherwise the outer branch never
  fires and the candidate reduces to IF(byte-equality(pos2,byte2),
  alt, v_old): with pos2=0, one byte2 would have to equal both 120
  (xy) and 114 (rab/rqw) while avoiding 97 and 100: impossible; with
  pos2=1, one byte2 would have to cover input[1] values 121 (xy), 97
  (rab), 113 (rqw) while avoiding 98 (abc) and 101 (defg): impossible;
  with pos2=2, one byte2 would have to cover input[2] values 98 (rab)
  and 119 (rqw): impossible, regardless of the out-of-bounds read
  behavior on xy, which this proof does not depend on. So no candidate
  with byte1 < 114 fits (nested indices 0..87551).
- byte1 = 114: the outer branch fires on rab and rqw, alt gives rrr
  for both [ok]. The inner branch is then tried with pos2=0 first: it
  must fire on xy (input[0]=120) and not on abc (97) or defg (100),
  so byte2=120. For byte2 < 120: byte2 97 or 100 fires the inner
  branch on abc or defg and alt gives aaa or ddd: fail; any other
  byte2 misses xy, which falls through to v_old, yy not xx: fail. The
  first fit is at pos1=0, byte1=114, pos2=0, byte2=120: nested index
  ((0*256+114)*3+0)*256+120 = 87672. Later positions (byte1 > 114,
  pos1 > 0) are never reached in the fixed order.
- Overall stream index of the first fit: 1055 + 87672 = 88727.

Predicted: b4b_first_fit_index = 88727, b4b_enumerated = 88728,
b4b_stream_total = 590879.

Consequence: for every faithful implementation of this frozen spec,
b4b_enumerated = 88728, far above the kill threshold of 5. The
efficiency claim (diagnosis in 5 evals versus blind template-aware
enumeration) is now actually testable, which is the whole point of
this amendment.

## The amended K-AX2 bar (exact text)

K-AX2 (diagnosis beats template-aware search, amended): B4b achieves
b4b_first_fit_index >= 0 on T+F1r evaluated against the frozen K-SB4a
expectations (competence; failure voids the run per the void rule
below, it is not a kill), and b4b_enumerated > revision_evals (5).
Kill (step-6 FAIL): b4b_enumerated <= 5 with competence satisfied,
meaning template-aware re-search matches or beats diagnosis-driven
construction and the K-SB2 efficiency claim is explained away by
search-space completeness; the honest outcome is a downgrade of the
efficiency claim, not a salvage.

Void rule (amended, narrowed): the run is void, never a verdict, if
(a) b4b_first_fit_index < 0, or (b) competence is satisfied but
b4b_enumerated != 88728. Case (a) means the implementation does not
achieve what the satisfiability proof shows is achievable: a broken
baseline. Case (b) means the implementation does not implement the
frozen enumeration order or candidate shape: a spec-fidelity failure.
Either way the remedy is rebuild and re-execute, not a verdict. Why
void cannot recur by the same mechanism as the old B4: the old void
was structural, triggered by every correct implementation because the
spec was unsatisfiable; the new spec is satisfied by the exhibited
candidate C*, so these void clauses can fire only on implementation
error. The void clause is back to its proper job: catching broken
baselines, not describing the spec.

## Re-execution semantics (what the re-run means for the record)

- The re-execution runs the full step-6 matrix with B4b in place of
  B4: 12 runs (M x3, B3 x3, B4b x3, D1 x3) under the amended K-SB5
  wording; all other bars, thresholds, fixtures, and the mechanism are
  unchanged. M, B3, D1 are expected to reproduce their S6 transcripts
  byte-identically; the only new measurement is B4b's.
- Re-execution PASS (all bars hold: K-AX1 kills A1 as before, K-AX2
  kills A2 with b4b_enumerated = 88728 > 5, K-ABL1 shows the expected
  degradation, architecture bars hold): the step-6 verdict is amended
  from "FAIL (cause K-AX2 VOID)" to "PASS on re-execution under
  amendment K-AX2". The original FAIL-on-void stays in the record
  transparently; history is not rewritten.
- Re-execution FAIL with K-AX2 kill (b4b_enumerated <= 5): step-6 FAIL,
  cause K-AX2 kill. Per the frozen prereg, the honest outcome is a
  downgraded efficiency claim: K-SB2's measured 5 vs 1055 against plain
  re-search B1 stands, but the "beats template-aware search" gloss is
  dropped. Recorded as information gained, never salvaged by
  redefining the comparator.
- Re-execution FAIL on any other bar: step-6 FAIL naming the tripped
  bar.
- Re-execution void: no verdict; B4b is rebuilt and re-executed. Void
  is not a kill and not a pass.
- The step-5 PASS record is not touched by any re-execution outcome.
  Verdicts are never SURVIVES; the pipeline position statement is
  unchanged (step 7 OOD remains next after a step-6 PASS).

## Cost accounting (amended field names)

Machine-greppable fields: revision_evals, b1_enumerated,
b3_correct_f1r, b3_correct_reuse, b3_predict_xy, b4b_first_fit_index,
b4b_enumerated, b4b_stream_total, b4b_wall_ms, b3_wall_ms,
d1_fails_total, d1_predict_xy, revision_wall_ms, binary_bytes (each
binary, including the new B4b binary), source_delta_lines (test harness
only), cognition_source_delta (must be 0), new_semantic_cases,
new_modes, new_bridges, new_routers, new_handlers. Kill: any missing
field; any nonzero architecture-growth field; any nonzero
cognition_source_delta. Expected: b4b_first_fit_index=88727,
b4b_enumerated=88728, b4b_stream_total=590879.

## Skeptic self-attack (and answers)

Attack 1, the strawman-in-reverse: "The amendment author knew the
two-branch solution and built a stream containing it. B4b is engineered
to be beaten; the honest comparator was the single-branch B4 and its
void was the honest result."
Answer: the two-branch requirement is a property of the frozen fixture
set, already stated in the step-6 verdict ("the full mechanism's
solution uses two branches"), not an invention of this amendment. A
comparator whose competence clause no implementation can satisfy cannot
test anything; retaining it would leave K-AX2 permanently void and the
efficiency claim permanently untested, which serves neither honesty
nor information gain. The nested template adds expressiveness using
only the prereg's own IF shape, with no new operators, no
disjunctions, and no researcher knowledge of which (pos,byte) pairs are
the answer: B4b still finds the answer only by blind fixed-order
enumeration over 590,879 candidates, with no diagnosis, no ranking, no
conflict rule, no rollback. If anything B4b is a stronger comparator
than B4 (it can solve the set at all), which makes the efficiency
claim's survival more informative, not less. The kill tripwire is
retained: any faithful implementation finding a fit in 5 or fewer
evals kills the claim.

Attack 2, proof fragility: "The predicted 88728 rests on a long case
analysis. One error and every faithful re-execution voids forever: the
same disease as the old spec."
Answer: the proof's premises are frozen measured S6 facts (alt and
v_old behaviors on all 5 checks, the verified benum impossibility,
deterministic eval), and the analysis is checkable line by line; it
deliberately does not depend on out-of-bounds read semantics. More
importantly, the amendment separates the prediction from the bar: the
BAR is b4b_enumerated > 5, which is what judges the claim; the
PREDICTION 88728 is a spec-fidelity check. The old disease was a spec
unsatisfiable by any implementation; the new spec is satisfied by the
exhibited C*, so a void now means implementation error, which is
exactly what a void clause exists to catch. The implementer is a
different agent from the amendment author, and the red team audits B4b
for machinery leakage, so a proof error would surface as a void
pattern, not laundered into a verdict.

Attack 3, smuggled conflict rule: "B4b's nested template with alt on
both branches reproduces the mechanism's repair; the comparator is the
mechanism with extra steps."
Answer: B4b has no conflict rule and cannot change what v_old predicts
on xy (yy). It reaches xy->xx only through alt's native copy-input[0]
behavior, a different causal path from the mechanism's record update
(D1 already showed alt alone gives xx on xy). The bar does not ask B4b
to reproduce the mechanism's internals; it asks whether blind
enumeration over template completions finds a full-fit program
cheaply. That is the efficiency question, unchanged from the frozen
prereg.

Attack 4, minimality: "Why not keep B4 and only fix the competence
clause?"
Answer: the defect was in the comparator's expressiveness relative to
the frozen checks, so the repair belongs in the comparator. Weakening
the check set would test a different claim; dropping the clause would
let a broken comparator kill the claim. The nested template is the
minimal repair that leaves every frozen check, every other bar, and
the verdict rule untouched.

## Commit-order self-check (binding)

This amendment must be committed ALONE by the coordinator before any
B4b implementation file, transcript, binary, or build log exists in the
lane. Verification: `git log --format=%H --
docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/AMENDMENT_KAX2.md` must
show exactly one commit, and that commit must strictly precede the
first commit adding any B4b artifact. UNVERIFIABLE ORDERING voids the
re-execution. No bar in this amendment may be altered after results are
seen; any further change requires a new transparent amendment and
re-freeze. Builders report BUILD-PASS/BUILD-FAIL only.

No em-dashes in this documentation.
