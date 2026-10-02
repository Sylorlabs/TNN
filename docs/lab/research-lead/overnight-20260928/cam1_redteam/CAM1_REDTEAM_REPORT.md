# CAM-1 Red Team: Adversarial Audit of Trial-Based P-DEP

Target: `cam1.zag` (818 lines), commit `371d20743`.
Prereg: `construct_apply/PREREG_CAM1.md`, commit `68a41be8a`.
Amendments: integration spec A1-A12 (`62e5ebb9f`), ISA boundary ruling
(`0525377f3`).
Auditor stance: assume the build's claims are false; attack each vector.
All findings verified by direct source inspection (line numbers cited).

## Vector 1. Anti-oracle: does trial-based P-DEP truly discover?

**ATTACK-SUCCESS (partial). The mechanism is menu selection, not composition.**

`propose()` (lines 296-408) tries templates in fixed priority:
COPY_A, then DBL_A, then ADD_AB. Each candidate is tested
independently via EQ against EVERY construction subject, and the
first template that holds on all of them wins (`found=1` stops the
search). The priority ordering does not fabricate answers: any
template that survives the all-subjects EQ test is a valid predictor
of the construction data, and the priority is a defensible
simplicity bias (fewer ops first). Input relations are tried in
sorted relation-ID order (align() sorts IDs, lines 228-243), which
is arbitrary but deterministic.

The real oracle problem is the menu itself. The live template set is
{LITERAL, COPY_A, DBL_A, ADD_AB} (lines 77-82; B_COPY_B and B_DBL_B
are defined but never used, dead code). The learner composes
nothing. It selects among four researcher-composed forms. On the W3
test, `z = x + y` is "discovered" only because B_ADD_AB is in the
menu. A regularity of the form `z = x * y`, `z = x - y`, or
`z = 2x + 3y` is undiscoverable by construction.

This inverts the prereg's own anti-menu argument. The frozen prereg
(68a41be8a, lines 97-100) states: "No ADD case, no MUL case, no
operator menu exists in the source." The amended implementation now
contains an ADD case (B_ADD_AB, B_DBL_A) and a 4-item operator menu.
The ISA ruling traded the finite-difference oracle for a
template-menu oracle. The builder implemented the amended direction
faithfully, but the honest label for P-DEP as built is **bounded
template matching**, and genuine compositional discovery (learner
composing novel expressions from the basis) is deferred to COMP-1.
Per Micah's L3 criteria, menu selection does not count as invention.

Severity: the mechanism is honest about what it does (tests pass,
abstains cleanly on P5), but its discovery ceiling is the
researcher's menu. Any claim stronger than "selects among 4
templates" is unsupported.

## Vector 2. Criterion-0: where do the semantics live?

**ATTACK-SUCCESS. The MAP semantics live in a researcher-written
dispatch, killing any L3 reading.**

The promoted MAP node stores `payload = [body_kind, in_a, in_b,
literal]` (promote(), lines 447-478). The meaning of `body_kind` is
implemented in `eval_body()` (lines 413-431), a four-way branch:

- line 417: `if(c1==B_LITERAL()){ return c4; }`
- line 418: `if(c1==B_COPY_A()){ return subj_obj(ws, m, s, c2); }`
- lines 419-423: B_DBL_A branch
- lines 424-428: B_ADD_AB branch

Each branch was written before training. The learner's persistent
state holds only an index into a researcher-defined semantic table.
Per L3 Criterion 0-A: if "where are the semantics implemented?" is
answered "in this dedicated switch branch written before training",
the L3 claim is killed. That is exactly the answer here.

The builder's BUILD_REPORT claims "0 semantic cases." That claim is
false on the C0-A reading: there are four dedicated semantic
branches plus six researcher-fixed B_* constants. The accurate
accounting is 4 semantic cases, 0 modes, 0 bridges, 0 handlers.

On the bounded-L2 reading (the approved program), this is
consistent: the core supplies mechanism, the learner supplies
indices. But no L3 claim can survive contact with eval_body.

## Vector 3. Finite-difference residue

**ATTACK-PASS. Finite-difference is genuinely out.**

Grep over cam1.zag: no occurrences of diff, order, coef, fit,
polynomial, or deriv outside comments that declare them OUT (header
lines 7-12, propose() comment lines 280-289). No subtraction
operator anywhere in the cognitive path. No MUL or DIV (the only
`*` tokens are byte-offset address computations `n*36`, `e*12`,
`nc*5`, which are memory layout, not cognitive arithmetic). The
discovery path uses only EQ comparisons and ADD compositions
(`zt!=za+za`, `zt!=za+zb`). The ISA boundary ruling is honored in
the code.

## Vector 4. VERIFY honesty

**ATTACK-SUCCESS (partial). The train/test split is real, but
standing is circular.**

What is honest: `propose()` tests candidates on construction
subjects; `verify()` (lines 433-456) tests on held-back subjects
and requires EVERY held-back triple with the trigger relation to
predict exactly via EQ, with `checked>=1` (a candidate verified
against zero held-back triples is rejected). The P6 test
demonstrates VERIFY rejecting a spurious construction-time
regularity (2x on construction subjects, broken on holdback).
Corroboration carries the precision, as the builder's ablation
shows.

What is circular: `promote()` (lines 463-477) writes SUPPORTS edges
from the SAME held-back facts used for verification. The standing
that later gates APPLY (`st>=1`, query() line 509) is therefore a
re-encoding of the verification outcome, not independent evidence.
No mechanism exists for a MAP to earn additional SUPPORTS from
fresh post-promotion experience; standing can only decrease (via
CONTRADICTS). "Standing derived from evidence edges" (A5/A11) is
implemented, but the evidence is the verification set itself.

Secondary: the train/test split is a caller convention.
`run_loop()` receives `holdback` as a parameter; nothing in the
mechanism enforces or records that the holdback subjects are
disjoint from construction subjects. A caller passing construction
data as holdback would silently verify against training data. The
tests are honest; the mechanism does not guarantee the honesty.

## Vector 5. K1/K2/K3 independent verification

- **K1: PASS.** Independently verified via `git merge-base
  --is-ancestor`: prereg `68a41be8a`, integration spec `62e5ebb9f`,
  and ISA ruling `0525377f3` are all ancestors of `371d20743`.
  Prereg strictly precedes implementation.
- **K2: MIXED.** Zero modes, zero bridges, zero task-specific
  handlers: PASS (query() branches only on exact-hit, MAP tag plus
  trigger equality, standing threshold, and eval success; no
  world/task/relation-identity branches). Zero hardcoded semantic
  cases: FAIL (four dedicated branches in eval_body, six B_*
  constants; see Vector 2). Zero regularity detectors: PASS (see
  Vector 3).
- **K3: PASS.** Pure Zag. `build.err` contains zero python
  mentions; the single python mention in BUILD_REPORT.md is the
  "zero Python" claim itself. Toolchain guard recorded in the
  builder's NAMECHECK.md. This audit invoked no forbidden
  executable (guard check in this lane's NAMECHECK.md).

## Minor findings

- Dead code: B_COPY_B (line 79) and B_DBL_B (line 82) are defined
  but never referenced. The single-input trial loop covers copy via
  B_COPY_A with ra ranging over all input relations; doubling of
  the b-input is never tried. Harmless but the menu is effectively
  4 live templates, not 6.
- The `standing()` comment (line 145) mentions USE and CONFIRMS
  edge types in the +1 set, but the code counts only SUPPORTS
  (+1) and CONTRADICTS (-1). Comment/code mismatch; behavior
  matches A11's signed bid for the types actually emitted
  (promote() only writes SUPPORTS and INSTANCE_OF).

## Verdict: CAM1-REDTEAM-COMPLETE

Summary of attacks:
1. Anti-oracle: ATTACK-SUCCESS (partial) - menu selection among 4
   researcher-composed templates, not learner composition.
2. Criterion-0: ATTACK-SUCCESS - semantics in eval_body's
   pre-training dispatch; no L3 reading survives.
3. Finite-difference residue: ATTACK-PASS - genuinely removed;
   ISA boundary honored.
4. VERIFY honesty: ATTACK-SUCCESS (partial) - real train/test
   split, but standing re-encodes the verification set; split is
   caller convention, not mechanism-enforced.
5. K1/K2/K3: K1 PASS, K3 PASS, K2 MIXED (semantic-case claim
   inaccurate).

The build is an honest bounded-L2 mechanism that does what its
tests claim. It is not a discovery engine beyond its menu, and its
own "0 semantic cases" accounting is wrong. Recommended ledger
posture: CAM-1 survives as bounded L2 template-matching with
honest verification; the compositional-discovery frontier belongs
to COMP-1, where the learner must compose rather than select.
