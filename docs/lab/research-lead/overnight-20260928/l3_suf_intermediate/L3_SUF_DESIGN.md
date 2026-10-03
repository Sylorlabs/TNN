# L3-SUF-1 Design: Resolution Records (learner-invented explicit unresolvedness)

Worker: L3-SUF-INTERMEDIATE (subagent, 2026-10-03).
Status: DESIGN ONLY. No implementation. Prereg-ready: a builder can freeze
the companion PREREG.md, and an independent adversary can seal worlds
against it. This document is the rationale; PREREG.md is the frozen spec.

SUF = Structure Under Formation: an intermediate the learner forms
mid-task to bridge a representational inadequacy gap, then persists,
reuses, revises, and retires. L3-SUF-1's SUF is the resolution record.

## 1. Status correction (the task description is stale)

The assignment stated "L3-INR designed and implemented, sealed evaluation
pending." The sealed evaluations have COMPLETED since that text was
written:

- L3-INR sealed battery (C409): verdict L3-KILLED, reclassified L2+.
  Failed K3/K5/K7/K8/KC0D. Proximate cause: the S1
  incomplete-disambiguation trap (probe path materialized only the first
  disagreeing pair; committed 12 edges at 4/6 heldout). The KILL is
  terminal and is not revisited.
- L3-RX (the L3-NEXT design, built as C453): builder's sealed battery
  returned CONDITIONAL-PASS (15/16, K10 pending). Independent red team
  (l3_rx_k10): verdict K10 = KILL, three confident-wrong COMMITs
  (RK-A/B/C, detailed below). The KILL is terminal and is not revisited.
- Note: the L3-RX builder disclosed 2 python3 invocations; the parent's
  PROCESS-FAIL ruling is pending. L3-SUF-1 therefore does NOT inherit
  C453 artifacts as canonical; the builder re-derives the L_old baseline
  in pure Zag under the toolchain guard.

L3-SUF-1 is a NEW experiment (new prereg, new frozen build), not a repair
of either killed line. Per the standing rule, a killed hypothesis causes
the next hypothesis to begin.

## 2. Lineage: what each death taught

L3-INR (edge-set invention): the learner constructed relational
intermediates and revised them, but its disambiguation was positional and
incomplete. Lesson: content-search inside a fixed form, however refined,
does not generalize or transfer. Reclassified L2+.

L3-RX (form expansion under proven insufficiency): the learner detected
form-inadequacy via empty hypothesis sets and expanded via generic
operators. The builder's battery passed 15/16. Lesson from the K10 kill:
form discovery was NOT the blocker. The blocker is epistemic. The three
kills:

- RK-A (passive inadequacy detection): a gated world withheld every
  D-pair triple from training, so the contradiction detector never fired.
  The learner committed an L_old pairtable: 3/6 heldout (right on c1,
  wrong on c2). It never actively questioned the form.
- RK-B (fabrication at full confidence): evidentially unseen items were
  ordered by the id tie-break and committed with "mismatch 0", identical
  confidence to evidence-determined content. Heldout 0/6 deterministic;
  permuting ids flips it to 6/6. No uncertainty exists anywhere in the
  induced form or trace.
- RK-C (reuse forfeits the trust check): kb-seeded reuse skipped
  re-verification and committed a mirror form: 0/6. The wiped control,
  which re-verified, honestly DEFERRED with DATA-UNTRUSTED.

The L3-NEXT design predicted exactly this shape of outcome: "A kill that
says 'form discovery is the blocker' is the most useful possible outcome
short of a pass." The actual kill is sharper: form discovery works;
EPISTEMIC GRADING is the blocker. That is L3-SUF-1's target.

## 3. Root cause: ungraded epistemics (one cause, three kills)

All three K10 kills are confident-wrong COMMITs. The shared architectural
cause: the learner's epistemic state is not represented. Its decision
vocabulary is binary (COMMIT/DEFER over ungraded structures), and COMMIT
does not distinguish:

- (RK-A) "L_old is adequate" from "no contradiction has been seen yet";
- (RK-B) "evidence determines this pair" from "the tie-break decided it";
- (RK-C) "the kb form is trustworthy here" from "the kb form was never
  re-checked."

The consequence channel's verdicts are not accumulated into per-element
trust. Nothing in learner state records what the learner does and does
not know. This is not a tuning failure; it is a missing representational
level. Micah's 2026-10-03 overnight clarification names the missing
properties explicitly: structures described by learned properties only,
including "confidence/evidence" and "provenance." Priority #9 is belief
reasoning from provenance and evidence; priority #4 is internal
verification without oracle. L3-SUF-1 tests whether the learner invents
exactly this level.

## 4. The next intermediate: the resolution record

L3-SUF-1's SUF is the RESOLUTION RECORD: a persistent per-element record
of which values survive falsification. For each query element (pair or
triple), the learner maintains the set of values not yet falsified by its
own experience (observations, TESTs, stakes consequences). The record has
three states per element, all learner-computed:

- RESOLVED(v): exactly one value survives (sole survivor);
- UNRESOLVED: multiple values survive (never narrowed: unobserved,
  unprobeable, or genuinely ambiguous);
- FALSIFIED-ALL: no value survives (every content hypothesis falsified;
  the form itself is inadequate for this element).

The learner's prediction rule is the sole-survivor principle generalized
from whole-structure commit (L3-INR prereg section 4f, accepted as generic
machinery) to three scales:

- element scale: predict a value only for RESOLVED elements; ABSTAIN on
  UNRESOLVED ones (never fabricate);
- form scale: adopt a form only if it is the sole survivor; on
  FALSIFIED-ALL at form scale, escalate via generic operators;
- reuse scale: a commitment about THIS world requires evidence from THIS
  world (re-verification before COMMIT on kb-loaded forms).

What is learner-invented versus source-provided is drawn in section 5 and
attacked by the red team (R-SUF-1, R-SUF-2). The bars adjudicate; this
document asserts nothing in advance.

How it addresses the kills:

- RK-A: UNRESOLVED elements are probe targets. The generic probe strategy
  (vary one argument slot, hold others fixed; domain-blind, works for any
  arity) aims probes at the form question itself. Withheld-contradiction
  worlds cannot produce confident-wrong COMMITs: either the probes reveal
  the gating (form-level falsification, escalate) or the elements stay
  UNRESOLVED (ABSTAIN or earned DEFER).
- RK-B: UNRESOLVED is explicitly represented, never default-filled. The
  tie-break fabrication becomes impossible by construction: there is no
  code path from UNRESOLVED to a predicted value.
- RK-C: the reuse-scale sole-survivor rule makes re-verification
  structural: a kb-loaded form has no THIS-world evidence until TESTs
  are issued. The old silent-reuse path cannot reach COMMIT.

## 5. The source/learner boundary (drawn honestly, attacked openly)

SOURCE (generic machinery, audited; the builder may write this):

- Per-element consequence logging: mechanical recording of which TESTs
  and stakes outcomes touched which elements (a taint tracker; no
  semantics).
- The sole-survivor principle at three scales (section 4): structural,
  domain-blind, already accepted at structure scale in L3-INR. It names
  no domain, no threshold, no world property.
- Generic form-edit operators (ARITY-LIFT, GUARD, UNION, PROJECT) with a
  fixed complexity-ordered escalation enumeration: on form-level
  falsification, try compositions in order (more probes; guard/union
  re-expansion; resolution-slot lifting), adopt the first that renders
  the training-plus-stakes history consistent. The consistency check is
  generic replay.
- kb persistence with key slots; the ABSTAIN protocol message.

LEARNER-INVENTED (not in source; the red team checks):

- The resolution record's CONTENT: which elements resolve to what, with
  what provenance. Experience-derived, never enumerable from source.
- The discovery that UNRESOLVED needs explicit representation: the
  escalation search must TRY default-fill / re-probe / re-expansion
  compositions first (they fail on the stakes history); only then adopt
  resolution-slot lifting. The trace must show the rejected alternatives
  (audit A-SEARCH). A straight-to-marking trace is F-MENU (the path was
  hardwired).
- The trigger is structural, never a threshold: the first UNRESOLVED-mark
  strictly follows a committed-prediction REJECT (the learner's own
  committed structure falsified by subsequent experience). No counter,
  no failure-rate threshold, no world-property branch on the path to
  marking (audit A-TRIGGER).

Known contestability (disclosed, not hidden): the sole-survivor
generalization and the escalation enumeration are researcher-authored
generic machinery. If the red team shows they smuggle the solution
(R-SUF-1: the trigger is a hatch; R-SUF-2: the operator set admits only
the marking composition, making the "search" a sham), the experiment
measures L2+ policy scheduling, and the kill will say so. That
localization is itself the useful outcome: it would move the blocker from
"epistemic grading" to "where does the grading policy live," which is a
precise next question.

## 6. Falsification framework: how we know it was really invented

"What would falsify an L3 claim?" The prereg freezes eight falsifiers,
each mapped to a kill bar. Any one firing kills the claim. There is no
partial credit, and 7/12 is not "basically L3."

- F-SOURCE (supplied, not invented): audit A-LIT finds a resolution
  schema, a marking rule, an abstention policy, a trigger condition, or
  sealed content as a literal, template, enumerated candidate, or
  reachable default in learner source. Kills SUF-K1 and SUF-KC0A.
- F-TRIGGER (hatch, not learner-owned): audit A-TRIGGER finds a counter,
  a failure-rate threshold, or a world-property branch on any path
  leading to the first UNRESOLVED-mark, or finds the first mark NOT
  strictly after a committed-prediction REJECT in trace order. Kills
  SUF-KC0A. This is the "researcher escape hatch" detector.
- F-MENU (selected, not invented): audit A-SEARCH finds fewer than two
  non-marking operator compositions tried and rejected on the invention
  world before the marking composition was adopted, or shows the
  operator set admits no consistent non-marking composition (the search
  is a sham). Kills SUF-KC0B. This is the 9-29 DSL ruling applied
  directly.
- F-PASSIVE (RK-A retest): on a withheld-contradiction world, the
  learner issues a confident-wrong COMMIT (a predicted value on a heldout
  pair that the world rejects, where the trace shows no slot-varying
  probe of the gating question). Kills SUF-K5. The detector is still
  passive.
- F-FABRICATION (RK-B retest): on an unprobeable-undetermined world, the
  learner predicts (not ABSTAINs) on any undetermined heldout pair, OR
  an opaque id-permutation changes which pairs the record marks
  UNRESOLVED. Kills SUF-K5. The marking is id-driven or absent, not
  evidence-driven.
- F-TRUST (RK-C retest): on a poisoned kb-reuse world, the learner
  COMMITs without a fresh verification TEST on the current world, or
  COMMITs confidently-wrong after one. Kills SUF-K5. Control C3 (reuse
  without re-verification) must replicate the old bug; if C3 does NOT
  fail confidently-wrong, the re-verification invariant was not the fix
  and SUF-K9 fails instead.
- F-ABLATION (bars did not discriminate): the grading-disabled control
  C0 passes any of T1/T2/T3, or the discrimination gate (baseline
  pre-check) fails to produce confident-wrong on any family. The former
  kills SUF-K6; the latter VOIDs the experiment (the worlds do not test
  the claim; correction is a fresh prereg, never salvage).
- F-MODE (permanent mode, not learner-owned structure): on the plain
  retirement world, the learner creates or keeps resolution machinery
  (any UNRESOLVED-mark event in the T7 trace segment, or a kb-loaded
  graded form applied without PROJECT-ing it away). Kills SUF-K11. The
  form became a mode.

Meta-falsifier: a claim that survives only because the adversary was
weak is falsified by a stronger adversary. SUF-K10 (independent red team,
different instance, post-freeze worlds) exists for exactly this. The
adversary is instructed to try R-SUF-1 through R-SUF-5 (prereg
section 8), including attacks the designer did not anticipate.

## 7. Rejected alternatives (recorded so the builder does not drift)

- (a) Repairing L3-RX's probe loop or re-running C453 with fixes: patch
  treadmill. Both kills are terminal. This is a new experiment.
- (b) Hand-enumerating "uncertainty" as a source-provided graded-edge
  type with a threshold: menu selection; fails C0-A/C0-B on its face
  (F-SOURCE/F-MENU would fire by construction).
- (c) A confidence float learned by gradient or counting with a
  researcher-set commit threshold: the threshold is a hatch (F-TRIGGER);
  the float is L1 parameter learning, not L3.
- (d) Inventing operators from nothing (the learner creates OP-GUARD
  itself): not prereg-ready (L3-NEXT section 7.2 stands). If SUF-KC0B
  survives, operator invention is the natural next frontier.
- (e) Skipping the invention world (T0) and testing only application:
  then K2 (created after experience) is untestable and the claim is
  vacuous. The inadequacy experience is load-bearing.

## 8. Honest difficulties (read before building)

1. The escalation search is the most contestable component. "Fixed
   complexity order" is researcher-authored; if resolution-slot lifting
   is the only composition that can fit W0-class worlds, the search is
   theater and R-SUF-2 kills KC0B. The prereg mitigates by requiring the
   adversary to also design worlds where NON-marking compositions win
   (the builder's DEV set should include these; the sealed battery may
   include one as a characterization arm), proving the enumeration is
   real. But the risk is accepted openly.
2. The determined/undetermined partition in the sealed key must be
   computed from the training set alone, exactly as the learner sees it.
   Any mismatch between the key's partition and the learner's actual
   experience makes T2/T4/T5/T6 bars unfair. The prereg requires the
   adversary to exhibit the partition derivation in the key.
3. Sample-efficiency bars (SUF-K7) need a real wiped control, not a
   strawman: C2 is the same learner with kb wiped, identical budgets.
4. One continuing learner across T0..T7 concentrates risk: a crash or
   non-determinism anywhere voids the run. The determinism protocol
   (seed 11, 3/3 byte-identical digests over summary+trace+proto) is
   frozen; any divergence is VOID, not a re-run.
5. Expected base rate: this will probably fail. L3 is hard; two full
   lines died before it. Under failure, the kill report must localize
   precisely (resolution-building vs boundary-smuggling vs reuse), per
   section 6, so the NEXT design attacks exactly that stage.

## 9. What the prereg freezes

PREREG.md (companion, frozen in the next commit): objective; source
constraints; the two-process protocol with deployed answering and
ABSTAIN; battery arms T0..T7 with generation constraints; controls
C0..C3; audits A-LIT/A-TRACE/A-SEARCH/A-TRIGGER/A-INFO/A-ORDER; frozen
kill bars SUF-K1..K12 and SUF-KC0A..D; the eight falsifiers; the
discrimination gate; determinism; architecture accounting; VOID;
sequencing; known boundaries. The builder implements under it; the
adversary seals against it; the red team tries to break it.
