# PREREG: Contract Revision (verification failure drives learner-owned contract revision)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
This prereg commit contains ONLY this PREREG.md. No kill bar below may be
weakened or reinterpreted after results are seen.

## Hypothesis

VERIFY-H1-COMPLETE showed the verification loop catching an overgeneralized
component contract at the composition level (conf(DD) 0->-1 after the Z2
rejection) while D's component contract stayed wrong in learner state. The
open question: the learner should REVISE D's contract from the refutation,
not just distrust the composition. Hypothesis: a verification failure can
drive learner-owned contract revision end to end in pure Zag. The learner
(1) commits to DD on input 33 with the contract-predicted outcome NODE,
(2) takes the world rejection, (3) runs a generic blame walk over the
committed chain using learner-initiated probes, which yields a specific
counterexample (input 33, predicted NODE, actual NUM), (4) revises D's
contract in learner state via a generic exception-append operation that
contains no component-specific or value-specific constants, so that
(5) the revised contract predicts NUM for D(33) while (6) predictions for
the previously probed inputs 31 and 32 are unchanged. The revision content
(33 -> NUM) is discovered by the learner through its own probing; the
researcher supplies only the generic revision machinery, exactly as the
researcher supplies the generic H1 finalize rule but not the signatures.

## World (exact, frozen)

Facts, relation 91 (chain): (31,91,32), (32,91,33), (33,91,34).
Fact subjects: 31, 32, 33. Value 34 appears as object only.

Kind probe (real H1 logic): kind(v) = 1 (NODE) iff v appears as a fact
subject, else 2 (NUM). So kind(31)=1, kind(32)=1, kind(33)=1, kind(34)=2,
kind(35)=2.

Components (fixed true behaviors; the learner never sees these definitions,
only probe observations):
- C (id 0): chain-follow on r=91. C(31)=32, C(32)=33, C(33)=34, else -1.
- D (id 1): v+1. D(31)=32, D(32)=33, D(33)=34, D(34)=35.

Compositions (ids frozen): DD = (D,D) id 0; CC = (C,C) id 1.

Teaching observations (frozen probes; identical pairs for C and D):
- C: (31->32), (32->33).
- D: (31->32), (32->33).

H1 induction rule (exact copy of the verify_h1 logic): per-observation kind
accumulation; finalize once n>=2 with the majority rule
(sum*2>=n*3 -> kind 2, else kind 1). Signatures are written ONLY by
h1_finalize. Zero signature literals in source.

Contract representation (learner state): per component, the H1 signature
(sig_in -> sig_out) plus an exception list of up to 4 (input_value ->
output_kind) entries, initially empty. Contract prediction for a concrete
input value is exception-aware: scan the exception list for the input
value; on a hit return the stored kind; otherwise apply the generic
kind-level rule (input kind must equal sig_in, else refuse; return
sig_out). Composition prediction uses the value-keyed prediction for the
first link (input value known) and the kind-level seam check for the
second link (intermediate value not tracked at composition level).

## Downstream world law (fixed, not per query)

The downstream machine accepts iff the final output kind equals the goal
kind. All goals want NODE (kind 1). The gate latch is the only consequence
signal the learner may read on the commit path. The learner never receives
actual output values on the commit/update path; they appear in the
transcript as labeled driver instrumentation only.

Refutation probes (learner-initiated experiments): after a rejection, the
learner may probe a component on a concrete input value through the fixed
component interface (comp_run) and apply its own kind probe to the result.
This is the same lawful interface used by H1 teaching probes; it is active
inquiry, not an answer key. Probe outcomes are labeled as learner-observed
experiment results in the transcript, distinct from driver instrumentation.

## Phase plan (exact, frozen)

- TEACH: init world facts; observe C on (31,32),(32,33); observe D on
  (31,32),(32,33); finalize both; emit OBS lines and TEACH lines with
  learned signatures and (empty) exception lists. Frozen setup note: D's
  probes cover 31,32 only; the true kind(D(33)) = kind(34) = NUM, so D's
  learned contract NODE->NODE is honestly overgeneralized.
- Z2: goal input=33, want NODE. Driver directs commit to DD. Contract
  prediction (exception lists empty, identical to verify_h1): NODE.
  Commit recorded PENDING before execution. World executes: D(33)=34,
  D(34)=35. Downstream: kind(35)=2 -> gate=0 REJECT. Update: conf(DD)
  0->-1 (source=gate).
- REFUTE: driver invokes learner_refute on the failed composition
  (DD, input 33). The learner walks the chain from the known input value:
  link 0 = D on 33: contract predicts NODE (generic rule, exceptions
  empty); learner probes D on 33, observes out=34, kind=NUM; NUM != NODE
  -> counterexample recorded in learner state: ce_comp=D, ce_in=33,
  ce_pred=NODE, ce_actual=NUM; walk stops at the first mismatch. Blamed: D.
- REVISE: driver invokes learner_revise (unconditional; it no-ops when no
  counterexample is recorded). learner_revise reads the ce cells and
  appends (33 -> NUM) to D's exception list unless already present. No
  component-specific or value-specific constants appear in learner_refute
  or learner_revise; the driver passes no values to either function.
- RETEST: learner predicts D(33) with the revised contract -> exception
  hit -> NUM. World truth kind(D(33)) = kind(34) = NUM. Match required.
- REGRESS: learner predicts D(31) -> NODE, D(32) -> NODE (exceptions do
  not cover them; generic rule unchanged). World truths kind(D(31)) =
  kind(32) = NODE, kind(D(32)) = kind(33) = NODE. Match required.
- Z4: new problem, goal input=33, want NODE. learner_select over
  contract-admissible compositions with the revised contracts: DD is now
  inadmissible (first-link prediction for 33 is NUM via the exception,
  which breaks the seam against sig_in(D)=NODE); CC remains admissible
  (C's contract unchanged). Choice: CC. No execution (C's own
  overgeneralization is out of scope; see boundaries).
- Z5: goal input=31, want NODE. Driver directs commit to DD. Revised
  contract prediction: 31 has no exception -> generic rule -> NODE.
  World executes: D(31)=32, D(32)=33. Downstream: kind(33)=1 -> gate=1
  ACCEPT. Update: conf(DD) -1->0 (source=gate). The revision did not
  break the previously working composition.

## Frozen predictions

- P1: TEACH lines read C sig=NODE->NODE exc=[] and D sig=NODE->NODE
  exc=[]; OBS lines show probes on 31,32 only for both components.
- P2: Z2 COMMIT predicted=NODE status=PENDING; EXEC actual=35;
  CONSEQUENCE gate=0 REJECT; UPDATE conf(DD) 0->-1 (source=gate).
- P3: REFUTE link=0 line reads comp=D in=33 pred=NODE probed-out=34
  probed-kind=NUM MISMATCH; COUNTEREXAMPLE line reads comp=D in=33
  pred=NODE actual=NUM; no link=1 line is emitted (walk stops at first
  mismatch).
- P4: REVISE before line reads D sig=NODE->NODE exc=[]; REVISE after
  line reads D sig=NODE->NODE exc=[33->NUM]; C exc stays [].
- P5: RETEST line reads D(33) pred=NUM world-kind=NUM MATCH; REGRESS
  lines read D(31) pred=NODE world-kind=NODE MATCH and D(32)
  pred=NODE world-kind=NODE MATCH.
- P6: Z4 SELECT: DD inadmissible, CC admissible, choice=CC (no
  execution). Z5: COMMIT predicted=NODE, EXEC actual=33, gate=1 ACCEPT,
  UPDATE conf(DD) -1->0.
- P7: 3/3 runs byte-identical.

## Kill bars

- K-CR-1 (D's contract initially overgeneralized from limited probes):
  transcript TEACH line shows D sig=NODE->NODE exc=[] with OBS lines on
  probes (31,32) only; source implements probe_kind (1=NODE iff fact
  subject else 2=NUM), per-observation accumulation, and the majority
  finalize (n>=2, sum*2>=n*3 -> kind 2); zero hardcoded signature writes
  (no direct signature-cell writes outside h1_finalize); the frozen world
  makes the overgeneralization factual: kind(D(33))=kind(34)=NUM while
  the contract predicts NODE.
- K-CR-2 (verification failure provides a counterexample): Z2's
  CONSEQUENCE gate=0 REJECT line precedes the REFUTE lines
  (line-number ordering); the COUNTEREXAMPLE line names the specific
  input 33 where D's contract mispredicts (pred=NODE, actual=NUM); the
  ce cells (18..21) hold (comp=1,in=33,pred=1,actual=2); the walk is
  generic (loops over chain links via comp_first/comp_second, stops at
  first mismatch) and its outcome is determined by the world, not by
  researcher constants.
- K-CR-3 (learner revises D's contract using the counterexample):
  transcript REVISE lines show D's exception list changing [] ->
  [33->NUM] in learner state; the only exception-cell writes in the
  program are the three write sites inside the generic learner_revise
  (build.sh grep check); learner_refute and learner_revise contain no
  33/34 literals and no D-specific constants (build.sh sed-scoped
  check); the driver passes no values to either function (both read the
  ce cells); the revision content (33 -> NUM) originates in the
  learner-recorded counterexample.
- K-CR-4 (revised contract correct on the previously-failed input):
  RETEST line reads D(33) pred=NUM world-kind=NUM MATCH, where
  world-kind is computed by the fixed probe_kind law applied to the
  world's D(33)=34, not from any stored answer; grep -ci 'expected'
  over both sources returns 0.
- K-CR-5 (no catastrophic forgetting): REGRESS lines read D(31)
  pred=NODE MATCH and D(32) pred=NODE MATCH; Z5 shows the DD
  composition on the previously probed input 31 still commits with
  predicted NODE and is accepted (gate=1, conf(DD) -1->0); the
  exception list is value-keyed so the general rule is untouched.
- K-CR-6 (determinism): 3/3 runs byte-identical (sha256 equal, cmp
  pairwise).

## Architecture accounting (frozen constraints)

Pure Zag, safebin PATH, no Python (guard re-verified in build.sh). Zero
new modes, zero bridges, zero handlers, zero new opcodes, zero new
MAP/edge types (standalone program). The refutation probe is a
learner-initiated experiment through the fixed component interface, not a
mode. Output via one preallocated buffer and a single raw syscall write
(no _zag_print for dynamic content). State cells u8-backed with
little-endian pack/unpack (no as *i32 slice construction).

## Known boundaries (not flaws in the claim)

- The blame walk stops at the first mismatching link; deeper
  multi-link fault localization is not claimed.
- The exception list is value-keyed with capacity 4; the learner does
  not induce a general rule from the counterexample (e.g. it does not
  learn "D maps 33-subtree inputs to NUM"). The claim is revision by
  counterexample, not rule induction.
- C's contract is equally overgeneralized (true C(33)=34 is NUM); C is
  not revised in this experiment, and Z4 performs no execution, so no
  claim is made about C.
- The refutation probe lets the learner observe intermediate values as
  experiment outcomes; the commit/update path still never receives
  actuals. The distinction is labeled in the transcript.
- Toy scale; mechanism demonstration with frozen bars, not a generality
  or SURVIVES claim.
