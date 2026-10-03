# PREREG: L2-ESS-HYPOTHESIS

Status: PREREG-FROZEN. No implementation exists at this commit and none
will be built in this lane. This file holds frozen META-CRITERIA only:
the questions the hypothesis must answer, the concreteness bar each
answer must clear, the frozen ESS criteria that judge the category
question, and the standards any future experimental test must meet.
The hypothesis itself (predictions, falsifiers) is recorded in
HYPOTHESIS.md, written only after this freeze. Non-ledger task (claim
minting paused).
Scope: `docs/lab/research-lead/overnight-20260928/l2_ess_hypothesis/` only.
Worker: L2-ESS-HYPOTHESIS subagent (depth 2/2), 2026-10-03.
Parent mandate: PATTERN-EPISTEMIC-STATE named the P1 pattern
"Epistemic-Structural Separation (ESS)" and its survey found L2
adaptive-reuse operators (COMBINE/SUBSTITUTE/TRUNCATE/INVERT/ABSTRACT/
CONCRETIZE) to be the conspicuous absence: OP_MASK is driver-set, never
learner-written (exclusion X2). PATTERN.md section 7 leaves open whether
L2 operators should have ESS. This lane formulates the hypothesis; it
does not implement anything.

## 1. The question to be hypothesized

Should L2 adaptive-reuse operators carry learner-written epistemic
standing records, and if so is that record ESS (as PATTERN.md section 7
suggests: "that record would be ESS instance #5 by the frozen criteria")
or is it something else (e.g. learned scheduling policy)? The operators
are procedures, not structures; the hypothesis must resolve whether ESS,
designed for structures, applies to them.

## 2. Frozen meta-criteria: what the hypothesis must answer

The hypothesis is ACCEPTED as complete only if it answers all five,
each clearing its concreteness bar. Vague or partial answers are
grounds for rejection of the hypothesis document, not for amendment
of these criteria.

- MC1 (standing meaning): What, exactly, would an operator's "standing"
  consist of? Bar: named record fields (counters, scalars, flags, sets),
  their keying (per operator alone, or per operator crossed with what),
  and one worked example of the form "SUBSTITUTE has succeeded 8/10
  times on structures with property P, failed 2/10 on property Q" with
  P and Q stated as learner-observable structure features, not
  researcher labels.
- MC2 (write path): How does the learner write and update the record?
  Bar: the causal path from experience to record stated as write sites
  distinct from the operator definitions (which routine runs, on what
  trigger, reading what evidence), with an explicit driver-blindness
  condition: what the driver is forbidden from naming or setting.
- MC3 (gating): How does the record gate behavior? Bar: the exact
  decision the record changes relative to the current S-alone behavior
  (fixed-order trial verification of all OP_MASK-enabled operators),
  stated as an observable difference in trial sequences or counts, with
  the trace tags that would make the difference visible.
- MC4 (predictions and falsifiers): Bar: at least three testable
  predictions with observable measures, and at least three falsifiers,
  each firing condition stated as an observable outcome. Must include
  the honest negative: the falsifier(s) under which the verdict is
  "no, operators should NOT have ESS", with that outcome's own
  predictions stated (the null hypothesis H0 must be given its case,
  not straw-manned).
- MC5 (category verdict): Is the record ESS or something else? Bar: the
  verdict must apply the frozen ESS criteria of section 3 below,
  criterion by criterion, to the pair (S = operator procedure, E =
  standing record). It must address: (a) the COGOPS precedent
  (PATTERN.md survey row 4: procedure bodies + learned applicability
  record = ESS instance); (b) the "operators are researcher-supplied
  machinery" objection; (c) why the SPEC exclusion X3 does or does not
  apply; (d) what observation would move the verdict from ESS to
  "learned policy" or back. A verdict of "both / it depends" without a
  stated discriminator fails MC5.

Concreteness bar (all): a future builder must be able to implement a
test of the hypothesis from the hypothesis document alone: record
layout shape, update rule shape, gating rule, context features, and
audit requirements must be specified, not gestured at. Algebraic
constants may be left to the future experiment's own prereg, but the
algebra FAMILY must be named (e.g. belief-style saturating counters
vs contract-style strike latches) with the discriminating tests
stated algebra-agnostically.

## 3. Frozen ESS criteria (the category judge)

Summarized from PATTERN.md sections 1-2; mechanism-neutrality holds
(the pattern lane rejected names that biased toward the belief-layer
flavor). The MC5 verdict must test each:

- E1: S exists checkably. A procedure body is an explicitly listed
  S-kind ("a node, graph, procedure body, clause set, or contract
  the learner constructed or holds").
- E2: E is a record ABOUT S's standing (applicability, trust,
  determination, coverage), not about the world regime.
- E3: E is written by a causal path distinct from S's construction:
  different write sites, different update rules, different evidence
  inputs; E accumulates evidence S's bytes alone do not carry
  (runs, falsification events, consequence history).
- E4: S and E can DIVERGE, and the mechanism's observable behavior
  (selection, use, probing) differs from what S-alone would dictate.
- E5: E is learner-written. A researcher-set control flag never
  written by the learner is excluded outright.

Exclusions (any one disqualifies the ESS classification):

- X1: a transient per-query check with no persistent record.
- X2: a researcher-set control flag never written by the learner
  (the current OP_MASK; the hypothesis must show its record escapes X2).
- X3: graded state about the WORLD regime rather than about a learner
  structure's standing (the SPEC policy-lane exclusion).
- X4: a deterministic recomputation of S's fields at read time.

## 4. Standards for any future experimental test (T1-T8)

A builder testing this hypothesis must preregister its own experiment;
that prereg must at minimum satisfy:

- T1: frozen kill bars with named falsifiers before implementation.
- T2: driver-blindness audit: the driver never names an operator, a
  form, a trace tag, a standing value, a threshold, or a context
  class (grep-style check in the spirit of the L2 lanes' K3/K7).
- T3: the standing record's write path is learner-side only; standing
  state offsets and update trace tags are absent from driver code.
- T4: determinism: byte-identical runs (the L2 lanes' K6 standard).
- T5: pure Zag implementation; safebin toolchain; no forbidden
  interpreters (worker toolchain guard).
- T6: no new modes, bridges, handlers, edge types, opcodes, or
  semantic cases beyond what the hypothesis names.
- T7: context classes for the record must be computed from
  learner-observable structure features by a generic function; no
  researcher-enumerated property lists, no world/answer literals in
  the signature function (K7-style audit).
- T8: a wrong-skip bound: the prereg must state the maximum tolerable
  rate at which standing-gated skips withhold an operator that the
  ungated baseline shows would have verified, and what verdict
  follows if the bound is exceeded.

## 5. Amendment and void rules

- These meta-criteria are frozen at the commit recorded in section 6.
  Any later change requires a transparent PREREG_AMENDMENT file stating
  what changed and why; silent edits void the freeze.
- If the hypothesis document fails MC1-MC5, the remedy is to rewrite
  the hypothesis, not to amend these criteria.
- A VOID verdict on any future experiment built from this hypothesis
  is terminal for that experiment; correction proceeds only as fresh
  preregistration plus fresh sealed worlds.

## 6. Commit-order self-check

- PREREG.md (+ NAMECHECK.md) committed alone first; no hypothesis
  text existed at that commit.
- HYPOTHESIS.md written only after the prereg commit; it must cite
  the prereg commit hash.
- No em/en dashes in loop documentation. Commits local with explicit
  pathspecs; never pushed.
