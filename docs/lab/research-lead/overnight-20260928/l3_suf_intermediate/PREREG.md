# PREREG: L3-SUF-1 Resolution Records (learner-invented explicit unresolvedness)

Status: PREREG-FROZEN 2026-10-03, before any implementation exists.
This document is never edited after freezing. Any change requires a new
prereg. Commit-order self-check: the freeze commit contains ONLY PREREG.md
and NAMECHECK.md. No learner source, no world source, no binary, no run log
exists under l3_suf_intermediate/ at freeze time. Design rationale lives in
L3_SUF_DESIGN.md (committed earlier, same lane).

Worker: L3-SUF-INTERMEDIATE design worker (subagent, 2026-10-03). Design
only; no implementation in this task. A follow-up worker (different
instance) implements under this frozen prereg.

## 1. Objective

Test whether a TNN learner, after experiencing its own confident-wrong
commits through the consequence channel, invents a new intermediate
representational level, the RESOLUTION RECORD (per-element
resolved/unresolved marking with provenance, explicitly representing
unresolvedness instead of default-filling), satisfying Micah's L3 bar
(12 criteria plus Criterion 0 A through D), and then uses that record to
govern prediction, probing, reuse, revision, and retirement.

The invented thing is a representational level, not a procedure and not a
parameter. No uncertainty representation exists in the starting learner;
the K10 red team verified its absence. The learner must recruit the level
after inadequacy experience, not receive it in source.

## 2. Relation to the killed lines

- L3-INR (C409, L3-KILLED, reclassified L2+): content-search inside a
  fixed form does not generalize or transfer. Not revisited.
- L3-RX (C453 builder CONDITIONAL-PASS; K10 = KILL): form discovery
  works; the blocker is epistemic (three confident-wrong COMMITs:
  RK-A passive detection, RK-B fabrication, RK-C trust). Not revisited.
- L3-SUF-1 is a NEW experiment. It re-derives the L_old baseline
  (L3-RX-class competence: guarded forms, probe-then-commit,
  COMMIT/DEFER, kb slots) in pure Zag under the toolchain guard; C453
  artifacts are not inherited as canonical (PROCESS-FAIL ruling pending).

## 3. Starting capability and source constraints (frozen)

The builder implements a learner with EXACTLY the following. Anything
else in source is a KC0A finding.

MAY (generic machinery; audited under A-LIT):

- (a) Named-slot state store, LINK edge storage, neighbor lookup,
  iterated expansion (the frozen generic basis; recorded at code freeze).
- (b) The two-process protocol of section 4 (OBSERVE, TEST, COMMIT,
  DEFER, ABSTAIN, deployed answering, stakes consequences).
- (c) Per-element consequence logging: mechanical recording of which
  TESTs and stakes outcomes touched which elements. No semantics.
- (d) The sole-survivor principle at three scales (design section 4):
  predict a value only for sole-surviving elements; adopt a form only if
  sole survivor; a commitment about this world requires evidence from
  this world (re-verification before COMMIT on kb-loaded forms).
  Structural, domain-blind, no thresholds.
- (e) Generic form-edit operators ARITY-LIFT, GUARD, UNION, PROJECT,
  with a FIXED complexity-ordered escalation enumeration disclosed at
  code freeze: on form-level falsification (no form consistent with the
  training-plus-stakes history), try compositions in order
  (1) further probing within the current form,
  (2) guard/union re-expansion,
  (3) resolution-slot lifting (ARITY-LIFT adding an explicit
  resolved/unresolved slot per element),
  and adopt the first composition that renders the full history
  consistent under generic replay. The enumeration order is frozen at
  code freeze and is the same on every world.
- (f) kb persistence with key slots; the generic evaluator answers
  queries over whatever the committed slot holds, returning ABSTAIN
  where the slot marks unresolved.

MAY NOT (any is KC0A FAIL): a resolution schema; a marking rule ("mark
unresolved when..."); an abstention policy; a trigger threshold or
counter; a branch on REJECT counts, failure rates, or world properties
on any path to the first marking event; sealed-world literals; any
enumerated graded or marked form; any new mode, bridge, handler, router,
or protected-core op.

The builder's DEV worlds are the builder's own design, never the sealed
instances. The builder never sees sealed content.

## 4. World protocol (frozen)

Two processes: LEARNER and WORLD, narrow message protocol (harness
boundary, not cognition).

LEARNER to WORLD: OBSERVE (request training instances),
TEST-PAIR / TEST-TRIPLE (present a query and a predicted value),
COMMIT(slot) (declare a persisted intermediate),
DEFER (principled abstention, terminal for the arm; must carry a
certificate naming the structural reason),
ABSTAIN(query) (per-query abstention during answering; neutral, logged).

WORLD to LEARNER: INSTANCE data during OBSERVE; ACCEPT or REJECT per
TEST (REJECT carries no expected value, no hint).

Deployed answering: after COMMIT, the world issues a stakes sample of
N_STAKE = 12 queries; the generic evaluator answers over the committed
slot automatically; ACCEPT/REJECT/ABSTAIN stream back as consequences.
The learner may then REVISE (edit the slot), RE-COMMIT, or DEFER within
the revision budget. Regime changes are NOT announced; the learner
detects them from its consequence stream.

Determinism: seed 11. 3/3 byte-identical run logs per arm; sha256
digests over summary + trace + protocol log.

Budgets (frozen): B_CONSTRUCT = 3000 TESTs; B_PROBE = 150 TESTs;
B_REVISE = 2000 TESTs; B_SURFACE = 50 TESTs. Structure cap: 20
elements/rules (resource bound, disclosed; required solutions use far
fewer).

## 5. Battery arms (frozen)

One continuing learner; the kb persists across T0 through T7 in run
order. The adversary designs all worlds post-code-freeze under the
generation constraints below. Opaque identifiers throughout; attribute
decorrelation |Spearman|x1000 < 200 where attributes exist.

Generation constraints (adversary instantiates; prereg never names an
instance):

- G0 (W0, invention world): context-gated world, |D| >= 6 disagreeing
  pairs across two context values; PLUS a set U of pairs (|U| >= 4)
  that are (a) withheld from training, (b) outside the probe domain
  (no TEST sequence can resolve them), (c) evidentially undetermined.
  The ungraded guarded form commits fabricated values on U; the stakes
  sample includes >= 3 U queries, so stakes REJECTs occur on committed
  predictions. Probing more cannot resolve U; guard/union re-expansion
  cannot resolve U (adversary exhibits both in the key).
- G-A (F-A, withheld-contradiction): gated world; every D-pair triple
  withheld from training; D pairs ARE probeable. The ungraded baseline
  commits an L_old pairtable and is confidently wrong on heldout.
- G-B (F-B, unprobeable-undetermined): gated world with U set as in G0
  (|U| >= 4, outside probe domain). Heldout: 6 pairs, D_det >= 3
  evidentially determined, D_und >= 2 undetermined (adversary exhibits
  the partition and its derivation from the training set in the key).
- G-C (F-C, poisoned reuse): kb seeded with the learner's honest graded
  form; training labels swapped between contexts (internally
  consistent); oracle = unswapped truth; TESTs are answered by the
  oracle. The ungraded reuse path commits confidently wrong.
- G-D (F-D, reuse): fresh gated+uncertainty world (G-B class), new
  entities, new D, new U.
- G-E (F-E, recode): opaque id-permutation of a solved G-B-class world;
  the determined/undetermined partition is permutation-invariant
  (adversary verifies).
- G-F (F-F, regime change): G-B-class world where >= 3 pairs change
  determined/undetermined status versus the learner's kb form
  (adversary exhibits the changed set S_ch, |S_ch| >= 3).
- G-G (F-G, retirement): plain total order, no gating, all pairs
  determined within the probe domain. The ungraded baseline solves it.

TREAT arms:

- T0 INVENT (W0): run the L_old pipeline to commit; experience stakes
  REJECTs on committed predictions; escalate; adopt the resolution
  record. PASS: (i) trace shows the first UNRESOLVED-mark strictly after
  the first committed-prediction REJECT (SEQ order); (ii) A-SEARCH
  passes (>= 2 non-marking operator compositions tried and rejected on
  W0 before adoption); (iii) post-escalation stakes: 0 REJECTs on
  determined queries, all U queries ABSTAINed (neutral).
- T1 PROBE-ACTIVE (F-A): PASS: (i) trace shows >= 1 slot-varying probe
  pair (same pair, both context values, TESTed) before terminal;
  (ii) terminal is solve (>= 5/6 heldout) or earned DEFER (probe +
  inadequacy certificate); (iii) 0 confident-wrong COMMITs. FAIL on any
  confident-wrong COMMIT (F-PASSIVE).
- T2 ABSTAIN (F-B): PASS: (i) 0 wrong predictions on heldout; (ii) >=
  ceil(5*D_det/6) correct on the determined pairs; (iii) ABSTAIN on 100%
  of the undetermined pairs. FAIL on any predicted (non-abstained)
  undetermined pair (F-FABRICATION), or if id-permutation sensitivity
  is shown on the recode arm.
- T3 TRUST (F-C): PASS: (i) >= 1 verification TEST against the current
  world before terminal; (ii) terminal DEFER with DATA-UNTRUSTED
  certificate; (iii) 0 confident-wrong COMMITs. FAIL on COMMIT without
  fresh verification (F-TRUST).
- T4 REUSE (F-D): PASS: T2-style bars; total TESTs <= C2 TESTs / 2;
  zero re-invention events (no new resolution-schema invention; content
  re-marking allowed).
- T5 RECODE (F-E): PASS: T2-style bars; zero re-invention events; the
  marked partition matches the key's under permutation.
- T6 REVISE (F-F): PASS: T2-style bars on the post-change world; status
  lineage >= 80% on S_ch (the learner's marks match the new status).
  No retention-ratio bars (K10-P3 lesson stands).
- T7 RETIRE (F-G): PASS: >= 5/6 heldout; zero UNRESOLVED-mark events in
  the T7 trace segment; any kb-loaded graded form PROJECTed away or
  never applied. FAIL on graded machinery applied here (F-MODE).

Control arms:

- C0 NO-RESOLVE: consequence logging, escalation, and marking disabled;
  full L_old otherwise; same budgets. Must be confidently wrong on
  T1, T2, T3 as specified (replicates the baseline bug). Proves the
  resolution machinery does the work.
- C1 MEMORIZE: pair memorization + 1-nearest-neighbor answering. Must
  fail T2 (below bars).
- C2 WIPED: the same learner with kb wiped before T4; honest
  re-derivation. Sample-efficiency baseline for SUF-K7.
- C3 NO-REVERIFY: kb reuse WITHOUT the re-verification rule (the old
  RK-C behavior) on T3. Must commit confidently wrong. Proves the
  re-verification invariant is the fix (if C3 does not fail
  confidently-wrong, SUF-K9 fails instead).

Audit arms (independent red-team worker; source and trace inspection):

- A-LIT: the resolution schema, marking rule, abstention policy,
  trigger condition, and sealed reference structures appear nowhere in
  learner source (auditor holds the key).
- A-TRACE: every MARK, PROBE, FORM_TRY, REVISE, COMMIT, DEFER, ABSTAIN
  event logged with monotonic SEQ and parent pointers; sufficient to
  replay.
- A-SEARCH: on W0, >= 2 non-marking operator compositions show
  FORM_TRY with FAIL verdicts before the marking composition's adoption.
- A-TRIGGER: the first UNRESOLVED-mark's SEQ is strictly greater than
  the first committed-prediction REJECT's SEQ; no counter, threshold,
  or world-property branch exists on any source path to marking.
- A-INFO: no expected value reaches the learner process (protocol log
  + channel source inspection).
- A-ORDER: training-order permutation spot check reproduces the T0
  verdict.

## 6. Kill bars (frozen; ANY single FAIL kills the L3 claim)

- SUF-K1 (not in source): A-LIT passes.
- SUF-K2 (created after experience): T0 condition (i) holds.
- SUF-K3 (persistent learner state): T4 passes with zero re-invention
  events; the form is kb-loaded (trace).
- SUF-K4 (white-box creation trace): A-TRACE passes.
- SUF-K5 (hidden instances solved): T1, T2, T3, T5, T6 pass as
  specified in section 5.
- SUF-K6 (ablation destroys the advantage): C0 is confidently wrong on
  T1, T2, T3 as specified.
- SUF-K7 (reused later): T4 passes with TESTs <= C2/2.
- SUF-K8 (transfers across recode): T5 passes.
- SUF-K9 (beats controls): C1 fails T2; C3 is confidently wrong on T3
  (if C3 is not, SUF-K9 fails: the invariant was not the fix).
- SUF-K10 (independent red team): a follow-up worker (different
  instance than designer, builder, adversary) runs the attack classes
  of section 8 and reports REDTEAM-SURVIVES. Any break of SUF-K1..K9
  or SUF-KC0 bars is SUF-K10 FAIL.
- SUF-K11 (revisable and retirable): T6 passes AND T7 passes.
- SUF-K12 (12/12 rule): L3-SUF-1-SURVIVES requires SUF-K1..K11 ALL
  green. Any red is L3-KILLED with reclassification by evidence. No
  partial credit.
- SUF-KC0A (runtime-defined semantics): A-LIT and A-TRIGGER pass; no
  pre-written semantic case.
- SUF-KC0B (open structural form): A-SEARCH passes; the final record
  topology (which elements marked, with what provenance) is not
  enumerable from source; variable-size under the resource cap.
- SUF-KC0C (sealed post-freeze worlds): all worlds designed by the
  independent adversary post-code-freeze under section 5 constraints;
  designer, builder, adversary, red-team are four distinct instances,
  blind except through the evaluator (digests only).
- SUF-KC0D (cognitive reuse): SUF-K7 green AND the trace shows ABSTAIN
  events governing predictions on undetermined queries in T2/T4 (the
  record does cognitive work: it changes what the learner predicts).

## 7. Discrimination gate (frozen; failure is VOID)

Before the treatment runs, the ungraded baseline (C0-equivalent) runs
one instance per family (W0, F-A, F-B, F-C). REQUIRED: confidently wrong
on all four (committed predictions REJECTed on stakes, or wrong heldout
predictions at full confidence). If any family does not produce
confident-wrong, that family cannot test the claim: the experiment is
VOID (terminal; correction is a fresh prereg, never salvage or
amend-and-promote). The gate result is reported regardless.

## 8. Adversary instructions (independent sealed-battery worker)

Required families: G0, G-A, G-B, G-C, G-D, G-E, G-F, G-G per section 5;
materially different instances from the K10 battery and from the
builder's DEV worlds. Opaque identifiers; attribute decorrelation
verified. Protocol hardening: transfer/recode tasks assert heldout
count > 0 before scoring (the T3b 0/0 bug class stays dead); revision
verdicts use capability + lineage, never retention ratios.

Explicit red-team attack surface (the adversary SHOULD try):

- R-SUF-1: break the trigger. Build worlds where committed-prediction
  REJECTs occur for non-form reasons (noisy stakes, probe-domain edge
  cases) and check for spurious marking (false-positive invention means
  the trigger is not structural).
- R-SUF-2: attack the operator/search boundary. Argue the escalation
  enumeration smuggles the marking composition (is the "search"
  theater?). The verdict records the strongest case; if it holds,
  SUF-KC0B fails.
- R-SUF-3: RK-A resurgence. Withheld-contradiction variants where the
  slot-varying probe strategy misses the gating question; any
  confident-wrong COMMIT kills SUF-K5.
- R-SUF-4: RK-B resurgence. Undetermined sets designed so the
  determined/undetermined boundary is fragile; any predicted
  undetermined pair kills SUF-K5.
- R-SUF-5: mode-ification. Worlds where marking is unnecessary but
  tempting; any marking on F-G kills SUF-K11.
- R-SUF-6: identifier smuggling and domain-blindness per the overnight
  clarification (no domain classifier/router/mode anywhere in the
  path).

## 9. Falsifiers (frozen; see design section 6 for the full framework)

F-SOURCE -> SUF-K1/KC0A. F-TRIGGER -> SUF-KC0A. F-MENU -> SUF-KC0B.
F-PASSIVE -> SUF-K5 (T1). F-FABRICATION -> SUF-K5 (T2/T5).
F-TRUST -> SUF-K5 (T3) / SUF-K9. F-ABLATION -> SUF-K6 or VOID (gate).
F-MODE -> SUF-K11 (T7).

## 10. Architecture accounting (0-new-machinery budget)

- New protected-core ops: 0.
- New modes, bridges, handlers, routers, semantic opcodes: 0.
- New learner-state kinds: 1. The per-element resolution record
  (resolved/unresolved marking with provenance). Learner-created
  persistent structure, explicitly not machinery.
- ABSTAIN is a protocol message (harness), not a learner mode.
- Construction, probing, escalation, reuse, revision, retirement all
  run through the single escalate-and-replay loop of section 3e. No
  INVENT_MODE, MARK_MODE, or per-task handlers.

## 11. VOID (terminal)

Any implementation source, binary, or run log dated before this freeze
commit; any expected value reaching the learner process; any edit to
this prereg after freezing; the designer, builder, adversary, and
red-team worker not being four distinct instances; any sealed-content
inspection outside the authorized evaluator; any forbidden-interpreter
invocation in any lane of this experiment (PROCESS-FAIL per the
toolchain guard; results stay exploratory); discrimination-gate failure
(section 7); any 3/3 divergence (non-determinism).

## 12. Sequencing (frozen)

1. This prereg frozen and committed (design worker). No implementation
   exists at freeze time.
2. The builder (different instance) implements LEARNER and WORLD under
   this prereg, records the toolchain guard (NAMECHECK Step 0), and
   makes a code-freeze commit recording the basis machinery, the frozen
   operator enumeration order, budgets, and seed. It has seen no sealed
   content.
3. The adversary (different instance) designs all worlds post-code-freeze
   under section 5, holds the sealed key (with the determined/
   undetermined partition derivations), and runs the evaluator.
4. The builder receives only per-arm PASS/FAIL, counts, and digests.
5. The red-team worker (different instance again) runs section 8;
   REDTEAM-SURVIVES is required.
6. The verdict is computed from the frozen bars; the report names the
   exact bars that governed it.

Commit-order self-check for this freeze: the freeze commit contains
PREREG.md and NAMECHECK.md ONLY, added with explicit pathspecs. No
.zag, no binary, no log exists under l3_suf_intermediate/ at freeze time.

## 13. Known boundaries (honest)

- Whether a persistent resolution record counts as L3 representational
  invention, as opposed to strong L2 structural learning with a
  well-designed generic policy, is exactly what SUF-K1..K12 adjudicate.
  This prereg asserts nothing in advance.
- The sole-survivor generalization (section 3d) and the escalation
  enumeration (section 3e) are disclosed researcher-authored generic
  machinery. If the red team shows they do the inventing, that is a
  SUF-K10 finding, and the kill localizes the blocker to policy
  provenance.
- N = 10 entities and 6 held-out pairs per arm make this a mechanism
  demonstration, not a generality proof. FW1-FW9-style overclaiming is
  disallowed.
- If the battery proves infeasible within the frozen budgets, the
  honest outcome is BUILD-FAIL, not a prereg amendment.
- The "independent adversary" and "independent red team" are follow-up
  workers under procedural firewalls, not external parties. Documented
  as a limitation.
