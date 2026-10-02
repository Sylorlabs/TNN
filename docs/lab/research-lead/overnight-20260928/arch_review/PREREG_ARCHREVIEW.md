# PREREG: Architecture Review Criteria (P1 lineage)

Date: 2026-09-30.
Status: FROZEN. Committed before the ARCHITECTURE_REVIEW document is finalized.
Scope: review criteria only. No implementation is authorized by this prereg.

## 0. Trigger

The architecture review trigger has fired for the P1 program discovery
lineage. Two consecutive generations failed on the same root cause:

1. GENEXEC2 (commit 8d5f58b89): score ordered beam search over (exact
   desc, mae asc) pruned non monotonic solution prefixes. Result:
   T0, T2, T3, T4, T5 failed; only T1 solved (via P3 assembly).
2. P1 redesign (prereg b236b28): behavioral signature dedup plus
   score ordered CAP eviction still pruned the deceptive prefix
   [IN0, PUSH 2, MUL, PUSH 1] (mae 8) before expansion. Result:
   T0 reached 2/9, kill bar K3 failed. Verdict: REDESIGN-BLOCKED.

Both generations repaired the same adjacent dimension (the
selection/retention criterion of a generate and test population)
while keeping the underlying scheme fixed: linear instruction
sequences grown by appending ops, ranked by an output score. A third
beam variant repair is forbidden. This review answers the trigger
question first, then specifies genuinely different discovery
hypotheses.

## 1. Trigger question and standing assessment

Question: is the current representation itself wrong?

Standing assessment (frozen by this prereg; falsifiable below):
The representation (linear (op, arg) programs over the frozen
GENEXEC2 VM, with CALL for fragments) is expressively adequate for
the 7 task battery. Evidence: P3 assembled a correct conditional for
T1 from parts; T4 and T5 have known CALL based solutions
([IN0, CALL ABS, PUSH 2, SUB, CALL ABS] and the ADD composition).
Every observed failure is a failure to FIND a program, never a
failure to EXPRESS one. The defect localizes to discovery machinery,
not to the VM or the program representation.

Falsifier for the assessment: if every hypothesis specified in the
review fails tasks T0 through T5 on the frozen VM within the frozen
cost budget, the representation assessment is overturned and a
VM level review is triggered instead of further discovery work.

## 2. Review kill bars

- R1 (prereg order): this criteria document is committed before the
  ARCHITECTURE_REVIEW document is finalized. PASS iff the prereg
  commit strictly precedes the review document commit.
- R2 (hypothesis count): the review specifies at least THREE
  hypotheses. At least ONE is a conventional control. At least TWO
  are developed from first principles for TNN. PASS iff all three
  counts hold.
- R3 (hypothesis completeness): every hypothesis states (a) its core
  mechanism and how that mechanism differs from beam search,
  (b) its predictions on the 7 task battery, (c) concrete conditions
  under which it would be falsified. PASS iff all three elements are
  present for every hypothesis.
- R4 (battery design): the review designs a minimal discriminating
  battery over the frozen VM covering all 7 tasks (2x+1, abs, mod3,
  parity, nested abs, fragment composition, adversary function),
  with a per task rationale stating which hypothesis pair the task
  discriminates. PASS iff all 7 tasks are covered with rationales.
- R5 (beam variant ban): any candidate hypothesis that is a beam
  search variant is rejected at review and never implemented. Beam
  variant is defined as: a population of candidate programs grown by
  appending ops, retained by ranking on a scalar output score
  (exact count, MAE, or any reweighting), with a fixed width or CAP.
  This explicitly forbids: larger beam, different beam width,
  another score weight, and task specific prefix protection. PASS iff
  no specified hypothesis meets the beam variant definition.
- R6 (purity): zero Python used in review work; zero em dash bytes
  in committed review documents. PASS iff both hold by byte check.
- R7 (no implementation): this wave produces documents only. No
  .zag source, no binaries, no runs. PASS iff the committed paths
  contain only the prereg and the review document.

## 3. Confirmation rule for later hypothesis testing

When hypotheses are later implemented and tested, a prediction is
confirmed only if the outcome matches AND the construction trace
shows the predicted mechanism. Outcome without mechanism does not
confirm. Example: hypothesis C solving nested abs via hidden
fragment CALLs would not confirm C; it would falsify C's mechanism
claim. Traces must log mechanism mandatory events per hypothesis
(residual values, induction/retrieval events, repair/split events
with justifying counterexamples, niche insertions).

## 4. Frozen references

- Frozen VM: the GENEXEC2 interpreter exactly as committed in
  8d5f58b89 (op set, PUSH range -9..9, DIV/MOD edge semantics,
  CALL/RET, top of stack result). No VM edits during hypothesis
  evaluation.
- Frozen episode sets: T0 x in 0..8; T1 x in -8..8 train with
  held out x in -12..12; T2 x in 0..16; T3 a,b in 0..4;
  T4 x in -6..6; T5 x in -4..8; T6 sealed adversary design after
  freeze.
- Cost budget placeholder: 1,000,000 program evaluations per task
  or 300 seconds wall clock, whichever is reached first. Frozen at
  battery prereg before any hypothesis implementation.

## 5. Out of scope

This prereg does not authorize hypothesis implementation, battery
implementation, or the adversary T6 design. Those are separate waves
with their own preregs. This wave ends with committed documents.
