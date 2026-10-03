# PREREG: Rule Revision (counterexample refines an overgeneralized RULE)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
This prereg commit contains ONLY this PREREG.md. No kill bar below may be
weakened or reinterpreted after results are seen.

## Hypothesis

CONTRACT-REVISION-COMPLETE showed a verification failure driving
learner-owned revision by counterexample, but the revision was a
value-keyed exception (33 -> NUM appended to a list). The rule itself
(ALWAYS output NODE) was never revised, and the learner could say nothing
about inputs it had never probed. Open question: can the learner revise
the RULE itself, so the refined structure generalizes to unseen inputs?

Hypothesis: a verification failure can drive learner-owned RULE revision
end to end in pure Zag. The learner (1) holds an overgeneralized RULE
(constant: always predict output kind NODE, induced by the generic rule
induction from limited teaching probes), (2) commits to DD on input 33
with the rule-predicted outcome NODE, (3) takes the world rejection,
(4) runs the generic blame walk with learner-initiated probes, which
yields the counterexample (input 33, predicted NODE, actual NUM) and
appends the probe outcome to the learner's observation log, (5) runs a
generic first-deviation-split operator over its own observation log,
which induces a THRESHOLD rule (output NODE iff input < 33, else NUM)
with no component-specific or value-specific constants, so that
(6) the refined rule predicts correctly on the counterexample input and
on previously-correct inputs, and (7) predicts correctly on NEW inputs
(34, 30) the learner never probed. The revision content (T=33, kinds
NODE/NUM) is discovered by the learner from its own recorded experience;
the researcher supplies only the generic rule machinery (constant and
threshold forms, the induction and split operators), exactly as the
researcher supplies the generic H1 finalize rule but not the signatures.

What makes this a RULE revision rather than an exception: the refined
structure is a predicate over input values (form + threshold + two
kinds), not a lookup entry. It answers queries for inputs absent from
the observation log (34, 30). A value-keyed exception for 33 cannot do
that. The exception machinery does not exist in this program at all.

## World (exact, frozen)

Facts, relation 91 (chain): (31,91,32), (32,91,33), (33,91,34).
Fact subjects: 31, 32, 33. Value 34 appears as object only.

Kind probe (real H1 logic): kind(v) = 1 (NODE) iff v appears as a fact
subject, else 2 (NUM). So kind(31)=1, kind(32)=1, kind(33)=1, kind(34)=2,
kind(35)=2.

Components (fixed true behaviors; the learner never sees these definitions,
only probe observations):
- C (id 0): chain-follow on r=91. C(31)=32, C(32)=33, C(33)=34, else -1.
- D (id 1): v+1. D(30)=31, D(31)=32, D(32)=33, D(33)=34, D(34)=35.

Compositions (ids frozen): DD = (D,D) id 0; CC = (C,C) id 1.

Teaching observations (frozen probes; identical pairs for C and D):
- C: (31->32), (32->33).
- D: (31->32), (32->33).

Rule representation (learner state, per component): form 0 = CONSTANT
(predict kc for every input), form 1 = THRESHOLD (predict klo iff input
< T, else khi). Cells: form, T, klo, khi, kc.

Generic rule induction (rule_induce): from the component's observation
log of (input, observed output kind) pairs, if all observed output kinds
are equal to k, the induced rule is CONSTANT(k) with majority/tie-break
on the first observed kind. There is no other induction path in TEACH,
so with the frozen probes both components honestly induce CONSTANT(NODE).
The frozen world makes the overgeneralization factual: kind(D(33)) =
kind(34) = NUM while the rule predicts NODE for every input.

Generic refinement operator (learner_refine, the first-deviation split):
reads the recorded counterexample (which names the blamed component) and
that component's observation log; computes the current rule's prediction
for every logged input; collects the logged inputs the current rule
mispredicts; takes the smallest such input as the split point T; sets
klo to the old rule's prediction at T (the kind the old rule got wrong)
and khi to the observed kind at T; writes the THRESHOLD rule
(form=1, T, klo, khi). No-ops when the log contains no misprediction.
No component-specific or value-specific constants appear in the
operator; the driver passes it no values.

Contract prediction: for a concrete input value, apply the component's
rule (rule_pred). Composition prediction uses the rule for the first
link (input value known) and the H1 kind-level seam check for the second
link (intermediate value not tracked). The H1 signatures (sig_in,
sig_out) are still induced by the real H1 machinery for the seam check
and are never rewritten by the refinement.

## Downstream world law (fixed, not per query)

The downstream machine accepts iff the final output kind equals the goal
kind. All goals want NODE (kind 1). The gate latch is the only consequence
signal the learner may read on the commit path. The learner never receives
actual output values on the commit/update path; they appear in the
transcript as labeled driver instrumentation only.

Refutation probes (learner-initiated experiments): after a rejection, the
learner may probe a component on a concrete input value through the fixed
component interface (comp_run) and apply its own kind probe to the result.
Each probe outcome is appended to the learner's observation log. This is
the same lawful interface used by H1 teaching probes; it is active
inquiry, not an answer key.

## Phase plan (exact, frozen)

- TEACH: init world facts; probe C on (31,32),(32,33) and D on
  (31,32),(32,33) through the fixed interface; each probe outcome is
  appended to the component's observation log; run rule_induce for both
  components; emit OBS lines and TEACH lines with the induced rules.
  Frozen setup note: D's probes cover 31,32 only; the true kind(D(33)) =
  kind(34) = NUM, so D's induced rule CONSTANT(NODE) is honestly
  overgeneralized.
- Z2: goal input=33, want NODE. Driver directs commit to DD. Rule
  prediction (CONSTANT(NODE)): NODE. Commit recorded PENDING before
  execution. World executes: D(33)=34, D(34)=35. Downstream: kind(35)=2
  -> gate=0 REJECT. Update: conf(DD) 0->-1 (source=gate).
- REFUTE: driver invokes learner_refute on the failed composition
  (DD, input 33). The learner walks the chain from the known input value:
  link 0 = D on 33: rule predicts NODE; learner probes D on 33, observes
  out=34, kind=NUM, appends (33,NUM) to D's observation log; NUM != NODE
  -> counterexample recorded in learner state: ce_comp=D, ce_in=33,
  ce_pred=NODE, ce_actual=NUM; walk stops at the first mismatch. Blamed:
  D. The transcript states the rule was refuted.
- REVISE: driver invokes learner_refine (unconditional; it no-ops when
  no counterexample is recorded). learner_refine reads the ce cells and
  D's observation log [(31,NODE),(32,NODE),(33,NUM)]; the smallest
  mispredicted input is 33; the old rule's prediction there was NODE;
  the observed kind there is NUM; it writes the THRESHOLD rule
  (form=1, T=33, klo=NODE, khi=NUM). No component-specific or
  value-specific constants appear in learner_refine; the driver passes
  no values to it. The transcript renders the rule before and after and
  a RULE-FIT line applying the refined rule to the observation log.
- RETEST: learner predicts D(33) with the refined rule -> 33 is not <
  33 -> NUM. World truth kind(D(33)) = kind(34) = NUM. Match required.
- REGRESS: learner predicts D(31) -> 31 < 33 -> NODE, D(32) -> 32 < 33
  -> NODE. World truths kind(D(31)) = kind(32) = NODE, kind(D(32)) =
  kind(33) = NODE. Match required.
- GENERALIZE: learner predicts D(34) and D(30) with the refined rule.
  Neither input was ever probed (no OBS line for 34 or 30 anywhere in
  the transcript; build.sh verifies). 34 is not < 33 -> NUM; world truth
  kind(D(34)) = kind(35) = NUM. 30 < 33 -> NODE; world truth kind(D(30))
  = kind(31) = NODE. Match required on both. This is the bar that a
  value-keyed exception could not pass.
- Z4: new problem, goal input=33, want NODE. learner_select over
  rule-admissible compositions with the refined rules: DD is now
  inadmissible (rule prediction for D(33) is NUM, which breaks the seam
  against sig_in(D)=NODE); CC remains admissible (C's rule unchanged).
  Choice: CC. No execution (C's own overgeneralization is out of scope;
  see boundaries).
- Z5: goal input=31, want NODE. Driver directs commit to DD. Refined
  rule prediction: 31 < 33 -> NODE. World executes: D(31)=32, D(32)=33.
  Downstream: kind(33)=1 -> gate=1 ACCEPT. Update: conf(DD) -1->0
  (source=gate). The refinement did not break the previously working
  composition.

## Frozen predictions

- P1: TEACH lines read C rule=ALWAYS(NODE) and D rule=ALWAYS(NODE);
  OBS lines show probes on 31,32 only for both components; D's
  observation log holds exactly (31,NODE),(32,NODE).
- P2: Z2 COMMIT predicted=NODE status=PENDING; EXEC actual=35;
  CONSEQUENCE gate=0 REJECT; UPDATE conf(DD) 0->-1 (source=gate).
- P3: REFUTE link=0 line reads comp=D in=33 rule-pred=NODE
  probed-out=34 probed-kind=NUM MISMATCH; COUNTEREXAMPLE line reads
  comp=D in=33 pred=NODE actual=NUM; a RULE-REFUTED line names D's rule
  ALWAYS(NODE) as wrong on probed input 33; no link=1 line is emitted
  (walk stops at first mismatch).
- P4: REVISE before line reads D rule=ALWAYS(NODE); REVISE after line
  reads D rule=IF(in<33,NODE,NUM); RULE-FIT line reads fit=3/3 on the
  observation log [(31,NODE),(32,NODE),(33,NUM)]; C's rule stays
  ALWAYS(NODE).
- P5: RETEST line reads D(33) rule-pred=NUM world-kind=NUM MATCH;
  REGRESS lines read D(31) rule-pred=NODE world-kind=NODE MATCH and
  D(32) rule-pred=NODE world-kind=NODE MATCH.
- P6: GENERALIZE lines read D(34) rule-pred=NUM world-kind=NUM MATCH
  and D(30) rule-pred=NODE world-kind=NODE MATCH, each noting the input
  was never probed; zero OBS lines mention 34 or 30 (build.sh check).
- P7: Z4 SELECT: DD inadmissible, CC admissible, choice=CC (no
  execution). Z5: COMMIT predicted=NODE, EXEC actual=33, gate=1 ACCEPT,
  UPDATE conf(DD) -1->0.
- P8: 3/3 runs byte-identical.

## Kill bars

- K-RR-1 (D's contract is an overgeneralized RULE, not a missing
  exception): transcript TEACH line shows D rule=ALWAYS(NODE), a
  constant RULE object; the source contains zero exception machinery
  (build.sh grep for exception/exc constructs returns 0); contract
  prediction is rule_pred, a predicate over input values, not a lookup;
  the generic rule_induce (majority of observed output kinds) produced
  the constant rule from the limited probes; the frozen world makes the
  overgeneralization factual: kind(D(33))=kind(34)=NUM while the rule
  predicts NODE for every input.
- K-RR-2 (verification failure refutes the rule): Z2's CONSEQUENCE
  gate=0 REJECT line precedes the REFUTE lines (line-number ordering);
  the COUNTEREXAMPLE line names the specific input 33 where D's rule
  mispredicts (pred=NODE, actual=NUM); the RULE-REFUTED line states the
  rule ALWAYS(NODE) was wrong on the probed input; the ce cells hold
  (comp=1,in=33,pred=1,actual=2); the walk is generic (loops over chain
  links, stops at first mismatch) and its outcome is determined by the
  world, not by researcher constants.
- K-RR-3 (learner induces a REFINED RULE, not an exception): transcript
  REVISE lines show D's rule changing ALWAYS(NODE) -> IF(in<33,NODE,NUM)
  in learner state; the only rule-cell writes in the program are the
  write sites inside the generic rule_induce and learner_refine
  (build.sh grep check); learner_refute and learner_refine contain no
  33/34/30 literals and no D-specific constants (build.sh sed-scoped
  check); the driver passes no values to either function (both read
  learner-state cells); the revision content (T=33, NODE below,
  NUM at/above) originates in the learner-recorded observation log;
  RULE-FIT 3/3 shows the refined rule fits the learner's own recorded
  experience.
- K-RR-4 (refined rule generalizes to new inputs): GENERALIZE lines read
  D(34) rule-pred=NUM world-kind=NUM MATCH and D(30) rule-pred=NODE
  world-kind=NODE MATCH; world-kind is computed by the fixed probe_kind
  law applied to the world's true D(34)=35 and D(30)=31, not from any
  stored answer (grep -ci 'expected' over both sources returns 0);
  build.sh verifies zero OBS lines mention 34 or 30, so these are
  genuinely unseen inputs; a value-keyed exception for 33 could not
  have produced either prediction.
- K-RR-5 (no forgetting of previously-correct cases): REGRESS lines read
  D(31) rule-pred=NODE MATCH and D(32) rule-pred=NODE MATCH; Z5 shows
  the DD composition on the previously probed input 31 still commits
  with predicted NODE and is accepted (gate=1, conf(DD) -1->0); the
  threshold keeps the below-33 region on the old kind.
- K-RR-6 (determinism): 3/3 runs byte-identical (sha256 equal, cmp
  pairwise).

## Architecture accounting (frozen constraints)

Pure Zag, safebin PATH, no Python (guard re-verified in build.sh). Zero
new modes, zero bridges, zero handlers, zero new opcodes, zero new
MAP/edge types (standalone program). The observation log and the
refinement operator are learner-state machinery, not modes: no
conditional dispatch on task labels anywhere (grep for mode/bridge/
handler returns 0; the word "mode" does not appear in the sources, the
rule form selector is named rule_form). Output via one preallocated
buffer and a single raw syscall write (no _zag_print for dynamic
content). State cells u8-backed with little-endian pack/unpack (no as
*i32 slice construction).

## Known boundaries (not flaws in the claim)

- The rule class (CONSTANT / single THRESHOLD on input order) is
  researcher-supplied machinery; the content (T=33, the two kinds) is
  learner-discovered. The claim is learner-driven rule revision within
  this class, not open-ended rule invention (not L3).
- The refinement operator performs a single split at the first
  deviation; multi-split or multi-predicate refinement is not
  implemented and not claimed.
- The generalization along integer input order works because the frozen
  world has that structure (D is v+1, kind flips at 34); the learner
  exploits it through the threshold operator. No claim is made that the
  learner discovered the world's law, only that its induced rule
  generalizes correctly on the tested unseen inputs.
- The blame walk stops at the first mismatching link; deeper
  multi-link fault localization is not claimed.
- C's contract is equally overgeneralized (true C(33)=34 is NUM); C is
  not revised in this experiment, and Z4 performs no execution, so no
  claim is made about C.
- The refutation probe lets the learner observe intermediate values as
  experiment outcomes; the commit/update path still never receives
  actuals. The distinction is labeled in the transcript.
- Toy scale; mechanism demonstration with frozen bars, not a generality
  or SURVIVES claim.
