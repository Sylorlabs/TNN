# HYPOTHESIS: L2 operator epistemic standing (H-OP-ESS)

Worker: L2-ESS-HYPOTHESIS subagent (depth 2/2), 2026-10-03.
Lane: docs/lab/research-lead/overnight-20260928/l2_ess_hypothesis/
Prereg: PREREG.md, frozen alone at commit e2e0d0beb before any
hypothesis text existed. This file written after.
Status: hypothesis only. No implementation, no builds, no runs.
Non-ledger task (claim minting paused).

## 0. Verdict up front

**H1 (primary): YES. L2 operators should carry learner-written
epistemic standing records, and the record IS ESS: instance #5,
second-order, procedure-level.** The frozen ESS criteria (PREREG.md
section 3) classify it as ESS, not as policy, provided the record is
genuinely learner-written (escapes X2), persistent (escapes X1), about
the operator-in-context rather than the world regime (escapes X3), and
shows divergence with behavioral consequence (E4). The COGOPS
applicability record (PATTERN.md survey row 4: procedure bodies +
learned applicability = ESS instance) is the direct precedent;
operator standing is the same pattern one level up, applied to
adaptation operators rather than verification procedures.

**H0 (null, preserved honestly): NO. Operators should NOT have ESS.**
Selection-by-verification is sufficient; a standing record is learned
scheduling policy, and any non-vacuous record risks catastrophic
wrong-skips. H0's case, predictions, and falsifiers are stated in
section 9; H0 is not straw-manned.

The discriminator between H1 and H0 is the record's error kind and
dynamics (section 5, F-A/F-C): endorsement-like dynamics (strike
retirement, probation recovery, context-sensitive distrust a stateless
pre-check cannot reproduce) put it on the ESS side; pure expected-cost
ordering puts it on the policy side.

## 1. The question (PREREG.md section 1)

PATTERN-EPISTEMIC-STATE's survey (PATTERN.md section 5, row 7) found
L2 adaptive-reuse operators (COMBINE=1, SUBSTITUTE=2, TRUNCATE=3,
INVERT=4, ABSTRACT=5, CONCRETIZE=6) to be NON-INSTANCEs under
exclusion X2: OP_MASK is "a driver-set causal-control flag, never
written by the learner" (l2_adaptive_reuse/REPORT.md). Operator
selection is by trial verification under the fixed generic order
[1..6]: the first operator whose full grounding executes to the query
terminal with the required value commits (L2-METAREUSE-EXTEND K3;
L2-INVERT-VALUE adds Form B/Form A inside op 4). PATTERN.md section 7
leaves open whether operators should have ESS: "If an operator lane
adds per-operator applicability learned from verification history,
that record would be ESS instance #5 by the frozen criteria."
Operators are procedures, not structures. This hypothesis resolves
whether ESS applies.

## 2. Category verdict (MC5): ESS, criterion by criterion

- **E1 (S exists checkably): PASS, thin leg.** Procedure bodies are an
  explicitly listed S-kind in PATTERN.md section 1 ("a node, graph,
  procedure body, clause set, or contract the learner constructed or
  holds"). The six operators are procedure bodies (mr_combine,
  mr_substitute, mr_truncate, mr_invert, mr_abstract, mr_concretize)
  the learner HOLDS in its repertoire and selects among in mr_adapt;
  OP_MASK gates them per arm. The criterion says "constructed or
  holds": the learner holds them. Honest caveat: unlike 3 of the 4
  existing instances (belief claim nodes, SUF form elements, COGOPS
  vfy_spec), the operators are researcher-supplied, not learner-built.
  This does not fail E1, but it is the thinnest leg, and it is why
  the evidence bar is set high (F-B): the record must prove its
  learner-written status rather than assume it. The ESS status of the
  record does NOT promote the operators to L3; they remain L2
  machinery. ESS classifies the record, not the machinery.
- **E2 (E is about S's standing): PASS.** The record grades each
  operator's applicability/reliability in context: "SUBSTITUTE has
  succeeded 8/10 on structures with property P, failed 2/10 on
  property Q." This is second-order epistemics in exactly the sense
  of PATTERN.md section 1: like SUF records (the learner's graded
  state about its own representation), operator standing is the
  learner's graded state about its own procedures. It is not graded
  state about the world regime (see X3 below).
- **E3 (distinct causal path): PASS by construction.** Operators are
  defined once in learner.zag (frozen researcher machinery). The
  standing record is written by a separate learner routine
  (op_standing_update, section 4) triggered post-query, reading
  verification outcomes (which operators were tried, which failed,
  which verified-and-committed). Different write sites, different
  update rules, different evidence inputs. The accumulated evidence
  is precisely what PATTERN.md lists E as carrying: runs (trial
  counts), falsification events (verification failures), consequence
  history (commits). None of this is in the operator's bytes.
- **E4 (divergence with behavioral consequence): PASS, testable.**
  S-alone behavior is the current harness: try every OP_MASK-enabled
  operator in fixed order [1..6]. Measured cost (L2-INVERT-VALUE
  REPORT, amended counts): QINV burns 1032 as-ticks on failed trials
  (op-1 599 + op-2 208 + op-3 181 + op-4 Form B 44) before op 4 Form A
  commits (as=1237, ae=2); QABS burns 1001 on failed ops 1-4 before
  op 5 (as=1286); QCONC burns 838 on failed ops 1-5 before op 6
  (as=1102). E-gated behavior skips low-standing operators: TRY lines
  vanish from the trace, as drops, committed operator and val are
  unchanged on solvable queries. The concrete divergence scenario is
  section 6 ("the stale specialist"): the operator exists and its mask
  bit is set, but E withholds the trial.
- **E5 (learner-written): PASS by construction, audited.** The whole
  point is to escape the X2 exclusion that currently disqualifies the
  operators. T2/T3 (PREREG.md section 4): the driver never names an
  operator, form, trace tag, standing value, threshold, or context
  class; standing state and update tags are absent from driver code.
  All E writes originate in the learner's post-query update path.

Exclusions:

- **X1 (transient per-query check):** escaped by persistence: the
  record is per (operator, context-signature) state carried across
  queries (section 3). F-A is the tripwire: if a stateless pre-check
  reproduces every decision, X1 fires and the ESS verdict flips.
- **X2 (researcher-set flag):** escaped by learner authorship (E5).
  F-B is the tripwire: researcher-set thresholds or
  researcher-enumerated context classes collapse the record to
  "OP_MASK with extra steps."
- **X3 (world-regime grading):** escaped by keying. The record is
  keyed by (operator, context-signature) where the signature is
  computed from learner-observable STRUCTURE features (source
  descriptor fields, entry-match flag; section 3), never by a world
  family label or drift estimate. The SPEC lanes were excluded
  because their graded state was about the world regime AND their
  policy arms were researcher-authored; neither holds here. Tripwire:
  if the signature degenerates to a family label, X3 fires.
- **X4 (recomputation of S's fields):** the record summarizes past
  verification OUTCOMES, not the operator's code fields. Like belief
  R2's corroboration runs, past-outcome accumulation is accumulated
  evidence, not recomputation.

The machinery objection ("operators are machinery, so grading them is
policy, not epistemics"): ESS never required S to be learner-built,
and the pattern's machinery/record split is the same as the belief
layer's (claim-node bytes vs b_sup): the operator code is machinery,
the standing record is learner state. COGOPS row 4 already admitted
procedure bodies as S with a learned applicability record as E.
Operator standing is that pattern applied to adaptation operators.

MC5(d) discriminator, stated plainly: the verdict moves from ESS to
"learned policy" if F-A or F-C fires (stateless pre-check suffices,
or no divergence is ever observed). It moves back (H0 falsified) if
P2+P3+P5 are jointly observed (section 7): divergence with
endorsement-like dynamics a scheduler cannot reproduce.

## 3. What standing means (MC1): reference record design

Keying: per (operator op in 1..6, context signature sig). Fields per
cell: SUC (u8 saturating success counter), FAIL (u8 saturating failure
counter), STRK (u8 consecutive-failure strike counter). Cold start is
neutral: an unseen cell (0,0,0) is always tried; the record never
withholds before evidence exists (this bounds F-D exposure at start).

Context signature (reference; builder may extend, may not add world
literals or family labels, per T7): computed once per query at
meta-phase entry from learner-observable features:

- em: entry-match flag = 1 if any live fact has sub==s AND
  rel==d_entry (source descriptor's entry relation), else 0.
- nf: d_nf (the source descriptor's fold count; small structural int).
- pat: 1 if d_entry==0 (pattern MAP with hole entry), else 0.

sig packs (em, nf, pat). Rationale: these are exactly the features
that discriminate the operators' applicability in the frozen lanes
(e.g. SUBSTITUTE requires an entry candidate with rel != d_entry, so
em=1 worlds exclude it by its own filter while ABSTRACT's
interface-match requires em=1; CONCRETIZE requires pat=1 sources).
The signature is computed by a generic function over the query and
the chosen source descriptor; no researcher-enumerated property list.

Worked example (the MC1 bar): after ten queries against sources with
sig=(em=0,nf=3,pat=0), the (SUBSTITUTE, sig) cell reads SUC=8,
FAIL=2, STRK=0: "SUBSTITUTE has succeeded 8/10 on 3-fold sources
whose query start offers no d_entry-matching entry." Against
sig=(em=1,nf=3,pat=0) the cell reads SUC=0, FAIL=6, STRK=3:
"SUBSTITUTE has failed 6/6 where the entry interface already matches;
it is struck for this context." The P/Q of the task prompt are
(em=0) and (em=1): learner-observable structure features, not
researcher labels.

Algebra family (builder preregs exact constants; discriminating tests
are algebra-agnostic): belief-style saturating counters (R2/R3-like:
INC_HI saturating at 255 on verifying commit, DEC floored at 0 on
trial failure, FAIL halved on success so recovery is graded) combined
with a contract-style strike latch (C_FAIL_RUN/U6-like: STRK>=3
consecutive trial failures in the same cell latches a skip). Standing
bar (R7-like learner-adjusted): skip if STRK>=3 OR SUC*2 < FAIL.
Reference constants: commit: SUC=min(255,SUC+8), STRK=0, FAIL=FAIL/2;
trial failure: FAIL=min(255,FAIL+4), STRK=min(255,STRK+1).

## 4. Write path (MC2): from experience, not from driver

New learner routine op_standing_update, called once per query after
mr_adapt returns, reading the trial outcomes the harness already
records per query (which operators were tried: MR_OP_TRIES; which
committed: MR_OP with MR_OP_DECIDED; which failed: tried but not
committed). For each tried (op, sig-of-this-query): on commit apply
the success update; on trial failure apply the failure update.
Untried operators (masked off, or skipped by standing) are not
updated: the record learns only from trials, never from hearsay.

Probation (what makes distrust reversible, PATTERN.md section 4
point 3): every 8th query that touches a struck (op, sig) cell, the
operator is tried anyway (trace MR-OP-PROBATION N). A verifying
probation resets STRK=0 and applies the success update (belief-R2-like
re-accumulation); a failing probation re-strikes. Without probation a
struck operator could never recover, so recovery dynamics are part of
the E algebra under test, not an afterthought. The driver never calls
op_standing_update, never names it, never sets standing state (T3);
the T2 grep-style audit (driver.zag free of operator names, trace
tags, standing offsets, thresholds, signature literals, in the spirit
of the L2 lanes' K3/K7) must pass.

## 5. Gating (MC3): the observable behavioral difference

Insertion point: mr_adapt's per-operator loop, after the existing
mask-bit check, before MR-OP-TRY N. Compute sig once per query at
meta-phase entry. For each op in 1..6: if mask bit clear, MR-OP-SKIP
N (unchanged); else if standing bar fails for (op, sig), print
MR-OP-STANDING-SKIP N and continue (no trial, no ticks); else
MR-OP-TRY N as today. A future experiment may additionally order
trials by standing descending (informational); the primary gated
behavior under test is skip-on-low-standing.

Observable difference vs S-alone: MR-OP-TRY lines vanish for struck
operators; as counts drop by the skipped operators' measured trial
costs (section 2: up to ~1032 as-ticks per query on QINV-class
queries); committed operator, via MAP, and val are unchanged on
solvable queries; ae stays 2 on commits. The trace tags that make
the difference visible: MR-OP-STANDING-SKIP N (gating),
MR-OP-PROBATION N (recovery trials), MR-STANDING-UPD (post-query
writes, summarized per cell).

## 6. Divergence scenario (the T-A/T-B analogue): the stale specialist

Two world families sharing the harness, same six operators, same
fixed order, same OP_MASK=63:

- Family A: as in L2-INVERT-VALUE (all six operators each necessary
  for their query; K5 ablation result stands).
- Family B: query starts whose entry facts all use rel == d_entry of
  the chosen source. SUBSTITUTE's rel != d_entry candidate filter
  then excludes every candidate: op 2 always fails (after its
  candidate scan), while the other five operators keep solvable
  queries. Nothing about op 2's code changed; OP_MASK still enables
  it; it still exists.

After 3 consecutive (op2, sig_B) trial failures, STRK=3 latches:
subsequent family-B queries print MR-OP-STANDING-SKIP 2 where the
fixed-order baseline prints MR-OP-TRY 2 / MR-OP-FAIL 2 (208-ish
as-ticks each, per the QINV op-2 measurement). S exists; E withholds;
behavior differs. This is the exact shape of PATTERN.md's canonical
divergences: T-B's "structure exists, endorsement withdrawn" and the
contract module's "clause structurally present but dc=2 retires it."

Recovery leg: family B' restores one SUBSTITUTE-viable query with the
same sig_B. Probation (section 4) eventually tries op 2; it verifies;
STRK resets; SUC re-accumulates; normal trials resume within a few
exposures. Distrust is reversible by new evidence; retirement never
becomes deletion (the learner cannot delete researcher machinery, and
E must not emulate deletion).

## 7. Predictions (H1)

- P1 (gating saves): on family-B queries, the standing learner's as
  is lower than the ungated baseline's by at least the skipped
  operators' preregistered trial costs, with identical committed
  operators, via ids, and vals on all solvable queries. Measure:
  per-query as/ae, MR-OP-TRY sequences.
- P2 (divergence): there exists at least one (operator, query) with
  mask bit set where the baseline tries-and-fails but the standing
  learner prints MR-OP-STANDING-SKIP (TRY absent). S exists, E
  withholds, behavior differs. Without P2, E4 is untested.
- P3 (reversibility): after a strike-latch retirement, restoring the
  operator's viability in the same context restores trials within K
  exposures (K preregistered), with a graded recovery curve (FAIL
  halving, SUC re-accumulation), not a binary flip. A pure
  threshold/deletion model predicts no recovery.
- P4 (learner-written): T2/T3 audits pass on the implementation: zero
  driver references to operators, standing, thresholds, signatures,
  or trace tags; all E writes from the learner's post-query path.
- P5 (learned context beats global): ablation arm with a single
  global per-operator cell (no sig keying) over-retires: an operator
  struck in family B is wrongly skipped on family-A re-asks sharing
  the operator (observable: wrong skips or lost vals on family A),
  while per-(op, sig) cells do not. If the global counter performs
  identically, the context keying adds nothing and MC1's keying
  claim is weakened.
- P6 (authorship transfer): the record format applies unchanged if
  operators become learner-revised or learner-created (the L3
  direction). The hypothesis predicts no format change is needed when
  S's authorship changes, because E is about held procedures
  regardless of who wrote them. (Forward-looking; not required for
  the first test.)

## 8. Falsifiers (H1)

- F-A (X1: stateless pre-check suffices): the future prereg names an
  explicit rival: a stateless per-query applicability pre-check
  (e.g. "SUBSTITUTE requires an entry candidate with rel != d_entry;
  test entry candidates before trying"). If the rival reproduces
  every skip/trial decision of the standing record on all tested
  families, the persistent record adds nothing: the ESS verdict flips
  to "transient check," i.e. policy. H1 is falsified as ESS (the
  record may survive as an optimization; the category claim dies).
- F-B (X2: researcher authorship): the only workable implementation
  the builder can produce requires researcher-set strike thresholds
  the learner cannot adjust, or researcher-enumerated context classes
  (property P/Q hand-listed per world family, or a family label in
  the signature). Then the record is OP_MASK with extra steps and H1
  fails outright.
- F-C (no divergence): on all tested families, MR-OP-STANDING-SKIP
  never fires for an enabled operator (or every skip coincides with
  a mask-off or a would-fail trial the pre-check also catches). E
  never withholds; the record is vacuous; H1 fails as ESS.
- F-D (harmful withholding; the strong honest negative): a
  standing-gated skip withholds an operator that the ungated baseline
  on the same query shows would have verified, causing query failure
  (val=-2) or a wrong commit, at a rate exceeding the preregistered
  T8 bound. Verdict on firing: operators should NOT have ESS (or this
  E algebra is wrong; the retry is a new algebra under a new prereg,
  not a patch). This falsifier carries the asymmetry H0 relies on:
  each operator is necessary for its query class (K5 ablation), so a
  wrong skip loses the whole query while tick savings are bounded.

## 9. Null hypothesis H0: operators should NOT have ESS

H0's case, stated at full strength: verification is the ground truth
and always has the last word in the L2 harness (K3: "verification
against world facts decides"). A standing record can therefore only
(a) prune trials that would have failed anyway (bounded upside:
hundreds of as-ticks per query against ae=2 commits; a real but
purely performance gain), or (b) withhold an operator that would have
verified (catastrophic downside: full query failure, since each
operator is necessary for its query class). Under this asymmetry the
rational standing bar converges to "always try," i.e. the record is
vacuous; any non-vacuous record is either F-A (a pre-check in a
trench coat) or F-D waiting to happen. Category version: operators
hold no claims, so the record's errors are performance errors, never
endorsement errors; selection among tools is scheduling (policy), and
calling it ESS stretches the pattern the way the NON-DUP verdict
rejected stretching "belief."

H0's predictions: any implemented record either never fires (F-C) or
fires wrongly at a rate no bar eliminates without going vacuous
(F-D); F-A's stateless pre-check captures all the tick savings.

What falsifies H0 (confirms H1): P2+P3+P5 jointly observed.
Divergence (P2) with endorsement-like dynamics, strike retirement
followed by probation-driven graded recovery (P3), and
context-sensitive distrust that a stateless pre-check cannot
reproduce (P5) are not the behaviors of a cost-ordering scheduler;
they are the behaviors of the belief layer's E (R2/R3/R5 dynamics)
and the contract module's E (dc/C_FAIL_RUN dynamics) applied to
procedures. A scheduler does not distrust; it reorders. If the record
distrusts and recovers, H0 falls.

## 10. Builder spec (from this hypothesis alone)

A future experiment lane can implement the test from this section
plus PREREG.md section 4 (T1-T8):

- State: cells for op in 1..6 crossed with sig in 0..SIGMAX-1
  (SIGMAX builder-preregs; reference sig packs (em, nf, pat) as
  section 3). Per cell: SUC, FAIL, STRK (u8 each). Builder chooses
  offsets; offsets must not collide with existing harness state.
- Signature function: prose-spec in section 3; generic over
  (query start s, source descriptor); audited per T7 (no world/answer
  literals, no family labels; K7-style token audit on the new
  learner code).
- Update: op_standing_update post-query (section 4); reference
  constants in section 3; probation every 8th touching query of a
  struck cell.
- Gating: mr_adapt insertion as section 5; trace tags
  MR-OP-STANDING-SKIP N, MR-OP-PROBATION N, MR-STANDING-UPD.
- Experiment skeleton (suggested, builder preregs its own bars):
  arms UNGATED (baseline, mask 63, fixed order) vs STANDING (same
  worlds, record enabled) on the family-A then family-B then
  family-B' curriculum; ablation arm GLOBAL (per-op cells, no sig).
  Kill-bar sketch: identical committed ops/vals/vias on solvable
  queries across UNGATED and STANDING; as(STANDING) < as(UNGATED)
  by at least the skipped trial costs on family B; P2/P3
  demonstrated in trace; F-D bound (T8) stated numerically, e.g.
  zero wrong-skip-caused failures on the designed families.
- Rival: the F-A stateless pre-check must be named in the future
  prereg and run as a competing arm.

## 11. Why it matters (beyond the lanes)

OP_MASK is driver-set control: the researcher lesions operators per
arm. Learner-owned standing moves that control into learner state,
which is the architectural-compression direction (capability vs
researcher-control lines; learner authority). For the continuing
learner (one learner across families, no task labels, no per-arm
lesioning), operator standing is exactly the memory policy needed to
stop re-trying dead operators without a researcher in the loop. And
per Micah's 2026-10-03 cross-domain ruling, the signature must be
computed from learned/structural properties only: the day domains are
renamed or stripped, (em, nf, pat)-style structural features survive
while any label-based policy breaks. The record is domain-blind by
construction.

## 12. Non-claims and governance

- Hypothesis only; no code written, no binary built, no world run.
  Nothing in the L2 lanes is modified by this document.
- The operators remain L2 machinery under H1; an ESS record about
  them does not make them L3, and no L3 claim is advanced here.
- Evidence so far is one world family (L2-INVERT-VALUE); the
  two-family curriculum of section 6 is proposed, not run.
  Sealed-adversary generality is open future work.
- No new modes, bridges, handlers, edge types, opcodes, or semantic
  cases are proposed. The record is learner state plus three trace
  tags, not a subsystem.
- If H1 is confirmed, the natural next question (not claimed here)
  is whether the record algebra unifies with the belief layer's
  R2/R3/R7 or the contract module's dc/C_FAIL_RUN (PATTERN.md's open
  P3 substrate question); the hypothesis is deliberately
  algebra-agnostic so that test can discriminate.
- No em/en dashes in loop documentation. Commits local with explicit
  pathspecs; never pushed. Non-ledger task: nothing minted.

## Files

- `NAMECHECK.md` (Step 0 toolchain guard; commit-order self-check)
- `PREREG.md` (frozen meta-criteria MC1-MC5, ESS criteria E1-E5/X1-X4,
  future-test standards T1-T8; frozen alone at e2e0d0beb)
- `HYPOTHESIS.md` (this file: H1/H0, predictions P1-P6, falsifiers
  F-A-F-D, builder spec)
