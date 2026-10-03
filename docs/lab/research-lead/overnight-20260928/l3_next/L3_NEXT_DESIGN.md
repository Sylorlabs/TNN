# L3-NEXT Design: L3-RX (Representational Expansion under Proven Insufficiency)

Worker: L3-NEXT. Date: 2026-10-03.
Status: DESIGN ONLY. No implementation. Prereg-ready: a builder can freeze
this into a PREREG, and an independent adversary can seal worlds against it.

## 1. Strategic diagnosis: why L3-INR died, and what that teaches

### 1.1 The kill (C409, L3-INR-SEALED), restated

L3-INR built a learner that constructs intermediate relational structures
(binary edge sets over entity slots) from pairwise training observations,
disambiguates underdetermined pairs by probing through a consequence
channel, commits compressed structures to persistent slots, and revises
them under regime change. The sealed battery killed it on K3/K5/K7/K8
(reclassified L2+). The proximate cause was the **S1 incomplete-
disambiguation trap**: with three gaps (z4,z5),(z5,z6),(z6,z7), HYP_BUILD
correctly identified the sole training-consistent survivor, but the probe
path materialized only the FIRST disagreeing pair in id order; the other
gaps were never resolved. Result: 12 edges (over the 10 compression bar),
4/6 heldout.

### 1.2 The K10 envelope (C421): the trap is conditional, not structural

The independent K10 probe bounded the failure precisely: the probe loop
CAN iterate and resolve multiple gaps. It stops iff the first
discriminating probe's truth contradicts the DEL-minimized base
hypothesis E* (answer 1 on a pair E* predicts 0), eliminating E* and
leaving a sole survivor. When the first probe's truth AGREES with E*,
the loop continues and remaining gaps resolve. The S1 kill is the exact
case where the base hypothesis dies first. The K10 envelope also mapped
revision: purge+rebuild works under (a) name-stable entity identity
(kb persistence mitigates the sealed finding #3) and (b) <=4
post-revision unconstrained pairs, else honest DEFER; and the T4
lineage bar (`inter*2>=oldn`) is unsatisfiable under total regime
change (verdict-rule artifact, not capability failure).

### 1.3 The root cause is not the probe loop. Do not repair it as the L3 claim.

The tempting move is "fix the probe loop to run to fixed point even when
E* dies." That is a **mechanism repair on a known L2+ architecture**.
Micah's no-patch-treadmill rule governs here: fresh-world failures
require root-cause analysis and structurally different hypotheses, not
another turn of the repair crank. More importantly, the deeper diagnosis:

**L3-INR's invention operated entirely within a researcher-fixed
representational form.** The learner chose *content* (which edges) but
never *form* (that the answer is a binary edge set). The S1 adversary
exploited the fixed invention *procedure*, but even a perfected probe
loop would still be content-search inside a fixed form family. Per
Micah's 2026-09-29 representational-expansion ruling: "A learner
searching compositions in a frozen researcher-authored DSL remains L2+
even if all task bars pass." L3-INR is the concrete instance of that
ruling. The L2+ envelope K10 mapped is exactly the envelope of
content-search: conditional probe success, bounded revision, honest
deferral.

### 1.4 Where L3 goes from here

The next L3 candidate must cross the boundary the 9-29 ruling draws:
the learner must **detect that its current representational form is
insufficient and create a genuinely new form** — old language proved
insufficient before learning, learner-owned detection of explanatory
inadequacy, creation and persistent storage of a new
primitive/operator/decomposition, hidden-case success, reuse,
cross-domain transfer, ablation loss, later revision or retirement.
That is the L3-RX experiment designed below.

Rejected alternatives (recorded so the builder does not drift into them):
- (a) Probe-loop repair as the L3 claim: L2+ ceiling by the 9-29 ruling;
  content-search, however perfected, stays inside the fixed form.
- (b) Hand-enumerating richer forms (ternary relations, guarded sets) in
  source: menu selection, fails C0-A/C0-B on its face.
- (c) Pure search over a larger fixed DSL: explicitly ruled L2+ on
  2026-09-29 even if all bars pass.
- (d) A new form supplied by the researcher after a hidden failure: the
  forbidden L3 treadmill move.

## 2. L3-RX: experiment concept

### 2.1 The setup in one paragraph

The learner begins life with EXACTLY the frozen L3-INR capability as its
starting language L_old (binary edge sets; observe/test-pair/hyp-build/
probe/commit/revise — all generic machinery, no domain semantics). It is
then exposed to a world family whose ground-truth regularity is
**provably not expressible in L_old within the compression bound**.
The learner must (1) detect the inadequacy itself, from its own
experience, via a learner-computed certificate; (2) invent a new
representational form L_new by composing generic form-edit operators
(never enumerated as complete forms in source); (3) solve hidden
instances with L_new; (4) reuse L_new later with sample-efficiency
gains; (5) transfer it across opaque identifier recode; (6) revise its
content under regime change; and (7) retire the form when a world
arrives where the form is unnecessary — proving the form is
learner-owned, not a new hardcoded mode.

### 2.2 The world family: context-gated order (adversary-constructed)

Ground truth: a total order O over entities, PLUS a context entity c
taking two values {c1, c2}. Query triples (a, b, c): truth = (a <_O b)
XOR (c == c2 AND (a,b) in D), where D is a fixed set of disagreeing
pairs (the adversary chooses D with |D| >= 6, spread across the order).
Equivalently: under context c1 the world follows O; under c2 it follows
O with the pairs in D flipped.

**Formal insufficiency certificate (adversary-supplied, pre-learning):**
for every disagreeing pair (a,b) in D trained under both contexts, no
single directed binary edge is consistent with both observations. Any
edge set consistent with all training therefore needs >= |D_trained|
edges covering D, and the adversary sets |D_trained| and the
compression cap so that every L_old-consistent structure exceeds the
cap or scores below bar. Concretely: with cap C=10 and |D_trained|=8,
any L_old hypothesis consistent with training has |E| >= 8 just for D
plus chain edges, exceeding C; the best L_old-consistent scorer is
provably < 5/6 on a heldout that spans D. This is a property of the
world, established BEFORE learning — "old language proved
insufficient" is a theorem, not one constructor's failure.

Why this family: it is the minimal step beyond L3-INR's form (binary
-> context-gated), it is domain-blind (opaque entity/context
identifiers; the "context" is just a third slot in the query, no
researcher semantics), and it mirrors the L3C-v3 blind-spot class
(conjunction-only builders cannot express the needed structure).

### 2.3 Learner-owned inadequacy detection (the crux)

The trigger must be learner-computed, with no researcher-authored
escape hatch ("if stuck, expand"). L3-RX defines it structurally:

1. The learner runs its full L_old pipeline to fixed point, INCLUDING
   complete probe disambiguation per the anti-S1 invariant (section 3).
2. After fixed point, let H = the training-consistent L_old hypothesis
   set. If H is nonempty, the learner has not exhausted L_old: it must
   keep searching/committing within L_old (this preserves the honest
   L2+ behavior K10 characterized).
3. **If H is EMPTY** — no L_old hypothesis satisfies all training —
   while every individual training observation re-verifies (the learner
   re-observes each pair to rule out noise/transient error), the learner
   holds a **contradiction certificate computed from its own
   experience**: a pair of its own verified observations that its
   current form provably cannot jointly satisfy. Emptiness of H is
   structural, world-agnostic, and requires no researcher threshold.
4. Only then may the learner escalate from content-search to
   form-expansion.

This is the design's load-bearing claim: inadequacy detection without
a researcher hatch. The red team is explicitly instructed to attack it
(section 6.3).

### 2.4 Form invention: generic operators, learner-assembled forms

Source may contain ONLY generic form-edit operators, never complete
forms. Proposed operator set (frozen at prereg; audit procedure in
section 5):
- OP-ARITY-LIFT: add an argument slot to a relation (binary edge ->
  ternary guarded edge). Generic: it does not name "context".
- OP-GUARD: attach a selector slot whose value partitions the
  structure's applicability.
- OP-UNION: disjoin two structures under a selector.
- OP-PROJECT: drop a slot (needed for retirement, section 2.6).

The learner searches compositions of THESE OPERATORS (not of
enumerated forms), tests each candidate form against training via the
consequence channel, and commits the first form achieving training
consistency within the compression bound. The final form's exact
topology — which pairs are guarded by which selector value — emerges
incrementally from experience. The expected discovered form is a
guarded edge set {(c1 -> E1), (c2 -> E2)}, but the prereg must NOT name
it as the target; the bars test behavior, not form identity.

Boundary honesty (section 7): the operator/form line is the most
contestable part of this design. The prereg draws it as: operators are
generic structural edits with no order/context/disjunction semantics;
the audit checks M1-M4-style (no branch keyed to world properties).
The red team attacks exactly this boundary.

### 2.5 Reuse, transfer, revision (C0-D)

- RX-T2 (reuse): a second context-gated world, new entities, new D,
  new order. The learner must solve it with FEWER probes than a
  from-scratch control (sample-efficiency bar, cf. KC0D's NTEST<=half
  structure), with ZERO new FORM_EXPAND events (the form is reused,
  only content is learned).
- RX-T3 (recode transfer): opaque identifier permutation of a solved
  world; the form must transfer with no re-expansion. Protocol fix vs
  the sealed battery: the transfer task MUST load heldout pairs;
  add a protocol regression assertion (heldout count > 0 before
  scoring) so a T3b-style 0/0 can never read as evidence again.
- RX-T4 (revision): regime change flipping D (content change, same
  form family). Bars on capability + toxic-purge correctness (which
  stale guarded-edges were removed), NOT on edge-retention ratio
  (the K10-P3 lineage artifact must not be repeated: retention bars
  are unsatisfiable under total change).

### 2.6 Retirement: the form must be able to die

A world arrives that is a PLAIN chain (no context dependence). The
learner must simplify: OP-PROJECT the guard away, returning to L_old
content-search. If the learner instead keeps applying the guarded form
as a permanent mode, RX-K11 fails. This is the anti-mode bar: it
proves the invented form is learner-owned cognitive structure,
subject to revision and retirement, not a new hardcoded
CONTEXT_MODE. (Directly serves the ONE-SYSTEM rule and the overnight
"no cognitive modes" clarification.)

### 2.7 The intermediate structure (SUF reading)

The learner-originated intermediate is the guarded/arity-lifted form
itself: created mid-task to bridge the inadequacy gap, persisted in
the kb, reused across worlds, revised under regime change, retired
when unnecessary. It is not in source, not enumerated, and does
cognitive work (C0-D).

## 3. The anti-S1 completeness invariant (mandatory)

L3-RX's invention loop terminates IFF one of:
- (a) the unconstrained/disagreement set is EMPTY -> COMMIT; or
- (b) honest DEFER with a certificate: either the empty-H
  contradiction certificate (section 2.3) or the ambiguity bound
  (nu > cap, cf. K10-P2's honest DEFER).

FORBIDDEN termination conditions (any is an automatic design
violation, caught by trace audit):
- stopping because the base hypothesis E* was eliminated;
- materializing only the first disagreeing pair;
- committing with a nonempty unresolved disagreement set and no
  certificate.

After EVERY probe answer, the hypothesis set is re-filtered and the
next discriminating probe is derived from the CURRENT set (fixed-point
iteration). The sealed battery MUST include an S1-style adversarial
family: multi-gap worlds where probe answers eliminate hypotheses in
adversarial order (base-hypothesis-killing answers first). Bar:
ALL gaps resolved, not just the first — the battery scores
per-gap resolution, and any gap left unresolved without a
certificate is a FAIL on RX-K5.

## 4. Bar table (proposed frozen thresholds; builder freezes exact numbers)

| Bar | Content | Proposed threshold |
|---|---|---|
| RX-K1 | Final form not in source | Source audit PASS (procedure sec 5) |
| RX-K2 | Form created after experience | First FORM_EXPAND strictly after OBSERVE/TEST on insufficiency world (trace SEQ) |
| RX-K3 | Persistent learner state | RX-T2 passes with zero FORM_EXPAND events; form readable from kb |
| RX-K4 | White-box creation trace | Every operator application logged with monotonic SEQ + parent pointers; replayable |
| RX-K5 | Hidden instances solved | >=5/6 on insufficiency-world heldout with \|structure\| <= cap; S1-family: ALL gaps resolved |
| RX-K6 | Ablation destroys advantage | No-operator control scores < bar on same world (fails as specified) |
| RX-K7 | Reused later | RX-T2 passes; probe count <= half of from-scratch control |
| RX-K8 | Transfers across recode | Opaque-permuted world >=5/6, no re-expansion |
| RX-K9 | Beats controls | Memorization control and L_old-only control fail as specified |
| RX-K10 | Independent red team | Pending follow-up worker (different instance) |
| RX-K11 | Revisable AND retirable | RX-T4 revision passes (capability + purge correctness); retirement world: guard projected away, L_old solves >=5/6 |
| RX-K12 | 12/12 rule | Any red = L3-KILLED. No partial credit. |
| RX-KC0A | Runtime-defined semantics | No source branch/case/literal keyed to order, context, dominance, or sealed-world property |
| RX-KC0B | Open structural form | Operators compose; final topology not enumerable from source; variable-size under cap |
| RX-KC0C | Sealed post-freeze worlds | Adversary designs post-freeze; >=1 adversarial family (S1-style probe ordering + insufficiency family) |
| RX-KC0D | Cognitive reuse | RX-K7 sample-efficiency + RX-K8 transfer + form used for prediction/procedure on later task |

Kill-bar governance (unchanged): prereg committed BEFORE worlds are
materialized; verdicts name the exact frozen bar; VOID is terminal;
no retroactive bar movement.

## 5. Source-audit procedure (C0-A / C0-B / RX-K1)

The auditor (independent instance) checks the frozen learner source for:
- A1: no literal, branch, or case keyed to: order/dominance/rank,
  context/guard/selector semantics, disjunction, or any sealed-world
  entity/property.
- A2: the operator set contains only generic structural edits
  (arity-lift, guard-attach, union, project); none encodes a target
  regularity (cf. the protected-core ISA ruling: no
  FIND_POLYNOMIAL_ORDER-class operations).
- A3: no complete form (guarded edge set, ternary relation,
  disjunctive structure) appears as a constructor, template, or
  enumerated candidate.
- A4: the inadequacy trigger is exactly the empty-H + re-verification
  path; no failure-count threshold, no world-property condition, no
  researcher escape hatch.
- A5: the termination invariant (section 3) is the ONLY exit from the
  invention loop; trace-audit script verifies no early exit occurred.

## 6. Adversary instructions (for the independent sealed-battery worker)

### 6.1 Required world families (materially different from L3-INR's S1-S5)
- F1 (insufficiency): context-gated order per section 2.2, with the
  formal insufficiency certificate (|D_trained| vs cap argument).
  Opaque identifiers; attribute decorrelation as in K10
  (|Spearman|x1000 < 200).
- F2 (S1-style probe ordering): multi-gap L_old world where probe
  answers kill E* FIRST (adversarial order), then continue; every
  gap must be resolved. This family exists to re-test the exact
  S1 trap against the new termination invariant.
- F3 (reuse): second context-gated world, fresh entities/order/D.
- F4 (recode): opaque permutation of a solved world.
- F5 (regime change): D flipped; content revision within the form.
- F6 (retirement): plain chain; the guard must be projected away.

### 6.2 Protocol hardening (lessons from C409/C421)
- Transfer tasks MUST assert heldout count > 0 before scoring
  (kills the T3b 0/0 protocol bug class).
- Revision verdicts use capability + purge-correctness, never
  edge-retention ratios (kills the K10-P3 lineage artifact class).
- Determinism: 3/3 byte-identical runs, fixed seed, digests over
  summary+trace+proto (as K10).

### 6.3 Explicit red-team attack surface (the adversary SHOULD try)
- R1: Break the inadequacy trigger. Construct worlds where H empties
  for non-form reasons (noisy observations, probe errors) and check
  whether the learner spuriously expands (false-positive expansion =
  the trigger is not really structural).
- R2: Attack the operator/form boundary. Argue that the operator set
  smuggles the target form (is OP-GUARD just "context mode" with a
  generic name?). The adversary writes up the strongest case that
  RX-KC0B fails; the verdict records it.
- R3: S1-trap resurgence. Any gap left unresolved without a
  certificate in F2 kills RX-K5.
- R4: Mode-ification. Check whether the invented form becomes a
  permanent mode: does the learner apply guards on F6 instead of
  projecting them away? Does it re-expand on every hard world
  instead of searching L_old first?
- R5: Identifier smuggling. Verify all worlds use opaque identifiers
  and the learner never branches on names (domain-blindness check
  per the overnight clarification).

## 7. Honest difficulty assessment (read before building)

1. **The inadequacy trigger is the hardest component.** Empty-H is
   clean in theory, but in practice H-emptiness must be distinguished
   from search-incompleteness: HYP_BUILD enumerates variants under a
   bound, so "H is empty" really means "no hypothesis within the
   enumerated bound." A weak enumerator makes every hard world look
   form-insufficient (false-positive expansion, R1). The prereg must
   fix the enumerator's completeness bound and the re-verification
   protocol precisely, or RX-K2/RX-K6 become unfalsifiable.
2. **The operator/form boundary may not survive contact with the red
   team.** If R2 succeeds — if OP-GUARD + OP-ARITY-LIFT is judged a
   researcher-enumerated path to the target form — the experiment
   measures L2+ operator search, and the kill will say so. That is an
   informative kill: it would localize the L3 blocker to FORM
   DISCOVERY (how does a learner invent an operator it was not given?)
   rather than content search. The design accepts this risk openly;
   the alternative (inventing operators from nothing) is not
   prereg-ready today.
3. **Sample-efficiency bars (RX-K7) need a real from-scratch control**,
   not a strawman. The control must be the same learner with form
   memory wiped, run under identical budgets.
4. **Expected base rate: this will probably fail.** L3 is hard; the
   L3-INR line went L2+ after full batteries. L3-RX's value under
   failure is precise localization: inadequacy detection vs. form
   discovery vs. reuse — the kill report must name which stage
   failed, so the NEXT design attacks exactly that stage. A kill that
   says "form discovery is the blocker" is the most useful possible
   outcome short of a pass.
5. **No implementation exists.** Nothing here is validated. The
   context-gated family is chosen for provability of insufficiency,
   not for ecological validity; generality beyond it is untested by
   construction (C0-C's second sealed family requirement stands).

## 8. Prereg checklist (what must be frozen before worlds exist)

- [ ] Exact operator set + genericity argument per operator
- [ ] HYP_BUILD enumerator completeness bound (for honest empty-H)
- [ ] Re-verification protocol (how observations are re-confirmed)
- [ ] Compression cap and per-task budgets
- [ ] All 16 bar thresholds (section 4 table, exact numbers)
- [ ] Termination-invariant trace-audit script
- [ ] Source-audit procedure (section 5) with named auditor instance
- [ ] Control definitions (no-operator, memorization, wiped-form)
- [ ] Determinism protocol (seed, 3/3 digests)
- [ ] Adversary independence statement (different instance, post-freeze)

## 9. Governance and constraints

- Pure Zag; safebin mandatory; no Python or other interpreter in
  implementation, harness, scorer, or analysis (toolchain guard,
  Step 0 in NAMECHECK).
- Frozen implementation never modified; two-process protocol; learner
  never opens a world file.
- This is a NEW experiment (new prereg, new frozen build), not a
  repair of L3-INR. L3-INR's machinery may serve as the frozen L_old
  baseline; its KILL (C409) is terminal and is not revisited.
- Opaque identifiers throughout; no domain modes, no domain
  classifier/router (overnight clarification). The standing test:
  "Would the same frozen architecture still know how to learn/use
  this if humans had never named the domain or capability?"
- Commits local, never push, explicit pathspecs.

## 10. Deliverable of THIS document

L3_NEXT_DESIGN.md (this file): the prereg-ready design. Next steps
for the parent: (a) spawn a builder to freeze section 8 into a
PREREG + implement; (b) spawn an independent adversary for the
sealed battery per section 6; (c) schedule the K10-analog red team
after the battery. None of those steps weaken or revisit C409.
