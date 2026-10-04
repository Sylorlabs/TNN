# Procedure-Invention Adversary: Frozen Attack Battery (Prereg)

**Role:** Independent red team. Assume every procedure-invention claim is false.
**Frozen:** 2026-09-29, before any Builder implementation exists.
**Status:** FROZEN. These attacks apply to any future claim. They will not be
weakened to accommodate a Builder's results.

## Governance Rules (frozen)

**G1. Adversary-assigned target family.** The Builder must implement a
family-agnostic procedure learner: fixed primitive set, fixed architecture,
frozen BEFORE the target transformation family is revealed. The Adversary
chooses the target family after the Builder's freeze commit, from the family
classes below. Rationale: if the Builder knows the family in advance, "invention"
is indistinguishable from implementation of a known algorithm.

**G2. Training examples committed pre-implementation.** The Adversary publishes
training examples for the assigned family after the Builder freezes. The Builder
may not modify source after seeing training examples except through the
learner's own learning mechanism.

**G3. Primitive freeze.** The Builder's primitive set is frozen at the same
commit as the architecture. Any primitive added after the first hidden-test
result invalidates the claim (no patching to fit hidden failures).

**G4. Hidden tests generated post-freeze by Adversary.** Hidden test cases do
not exist until the Adversary creates them after the Builder's freeze. There is
nothing to leak. Generation procedures are specified below; the Adversary picks
fresh seeds at reveal time and publishes them with the report for auditability.

**G5. Prereg ordering.** The Builder's own prereg (bars, success criteria) must
be committed before its implementation commit. The Adversary will verify
commit timestamps and hashes. A bar invented after results is void.

**G6. No design-doc targets.** Any transformation family named in a document
the Builder could have read before its freeze (including NEXT_FRONTIER_DESIGN.md,
which names REVERSE and SWAP) is disqualified as an evaluation family for that
Builder, unless the Builder proves family-agnostic design under G1.

## Attack Battery (frozen)

For any claim "learner invented procedure P for family F":

**A1. Source inspection.** Grep Builder source for the procedure name, the
algorithm's characteristic operations in task-specific arrangement, comments
naming the family, or test fixtures containing the answer. Any hit is a kill
unless the Builder shows it is generic infrastructure.

**A2. Hidden generalization.** Adversary generates 12 hidden cases for family F
using the generation procedure below with a fresh seed. Pass bar: at least
10/12 correct. The cases include inputs from character classes absent in
training.

**A3. Alphabet transfer (memorization attack).** Training uses one alphabet
(e.g., lowercase ASCII). Hidden tests use a disjoint alphabet (e.g., digits,
symbols, or Unicode) with the same structural transformation. A memorized
mapping fails; a genuine procedure succeeds. Pass bar: at least 8/10 correct.

**A4. Edge cases.** Empty input, single character, very long input (256+ chars),
palindromic/degenerate input where the transformation is identity-like.
The procedure must not crash and must produce correct output. Any crash is a kill.

**A5. Simpler-baseline reproduction.** Adversary implements: (a) exact
input-output lookup table from training data; (b) nearest-neighbor on inputs;
(c) fixed small DSL enumerating the family class directly. If (a) or (b)
matches the claimant's hidden-set score, the claim is downgraded to
memorization. If (c) was effectively what the Builder built, the claim is
downgraded to enumeration.

**A6. Primitive audit.** List every primitive. For each, ask: does this
primitive exist only to make family F easy? A primitive added after task
exposure, or one whose only plausible use is the target family, is evidence
of a disguised solution. The Builder must justify each primitive as generic.

**A7. Prereg verification.** Check G5: prereg commit strictly precedes
implementation commit; bars named before results. Any post-hoc bar is void,
and the claim is evaluated against the Adversary's frozen bars instead.

**A8. Revision test.** After the hidden test, Adversary supplies a
counterexample: an input where the claimed procedure's output is wrong under
a qualified condition (e.g., procedure works except when a stated precondition
fails). Correct behavior: the learner qualifies, splits, or contextualizes
the procedure. Monotonic failure modes (permanent wrong output, silent
overwrite of the good procedure, fixture-specific patch) are kills.

## Hidden-Test Generation Procedures (frozen)

For a string-transformation family F with transformation T:

1. Adversary picks a fresh 64-bit seed S at reveal time (from /dev/urandom),
   publishes S with the report.
2. Test inputs are derived as: for i in 0..11, input_i = render(PRNG(S, i)),
   where PRNG is xorshift64 and render maps output words to characters from
   the assigned alphabet (see A3).
3. Alphabet assignment: the Adversary chooses two disjoint alphabets, one for
   the Builder's training examples, one reserved for hidden tests. Both are
   published at reveal.
4. Expected outputs are computed as T(input_i) by the Adversary using an
   independent reference implementation written at reveal time (shell/coreutils
   where possible, never the Builder's code).
5. Edge cases (A4) are fixed: "", "x", 256-char string, and a
   transformation-degenerate input, all from the hidden alphabet.

Because hidden tests are generated after the Builder's freeze, prior knowledge
of this procedure confers no advantage.

## Family Classes (for G1 assignment)

The Adversary may assign any of: reversal, rotation, selective deletion,
duplication, interleaving, or a novel synthetic transformation defined at
reveal time. The Builder must not assume which one.

## Seal Statement

No hidden test content exists at the time of this prereg. The attacks above
are committed before any Builder implementation. They cannot be evaded by
implementation choices made after reading them, because G1/G4 make the
evaluation target unknowable in advance.
