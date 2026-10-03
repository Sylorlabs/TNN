# Discount Mechanism Specification

**Status:** SPECIFICATION ONLY. No implementation. No variant built.
**Verdict:** DISCOUNT-COMPLETE.

## 0. Problem statement

The contradiction-break probe (`510b6cb42`) established three facts:

1. A single contradicting observation breaks the bootstrap inference loop.
2. The break is permanent: failed bootstraps teach nothing, so the
   contradiction stays at the top of the recency-ordered evidence window
   indefinitely.
3. Recovery requires external intervention (six taught facts to displace
   one contradiction from the cap-6 window). The learner contributes
   nothing to its own recovery.

The probe's key sentence: "The learner has no mechanism to remove,
discount, or work around it." After Phase 7, subject 2001 has two live
contradictory facts (idx7=42, idx39=99) with no resolution mechanism.

This specification defines the minimal machinery for "discount": a
graded, reversible, learner-writable suspicion attached to each FACT,
with a production read path in the bootstrap evidence scan. The goal is
narrow: give the "stop" an "exit." It is not a general solution to
source conflation, revision correctness, or epistemic grounding. Those
limits are stated explicitly in Section 6.

## 1. Defining discount

### 1.1 What discount is

Discount is a per-FACT signed integer, stored in learner state, recording
accumulated evidence against that fact's reliability as inference
evidence. Positive values mean suspicion; zero means undisputed;
negative values (bounded) mean confirmed.

It is graded: one conflicting observation produces slight discount; repeated
conflicts produce heavy discount. It is reversible: confirming observations
reduce it. It is consumer-scoped: in the minimal specification it affects
only the bootstrap evidence scan, not retrieval, trial premises, or
query answers.

Formally: for each FACT node n, `discount(n)` in Z, initialized 0.
A threshold T (researcher-chosen, documented in Section 3.2) partitions
facts into evidence-eligible (`discount <= T`) and evidence-excluded
(`discount > T`) for the bootstrap consumer.

### 1.2 Why not deletion

1. **Irreversibility.** Deletion destroys information. A contradicted fact
   may later be vindicated (the contradiction may itself be noise, a
   miscalibrated sensor, or a superseded observation). Discount preserves
   the fact and its history; deletion forecloses recovery.
2. **Conflation of epistemics with budget.** The only removal mechanism in
   TNN-2 is eviction, which is budget-driven. Deleting a fact for epistemic
   reasons would mix "I doubt this" with "I need the node slot." Discount
   separates the epistemic judgment from the resource decision.
3. **No clean deletion exists.** TNN-2 has no epistemic deletion path;
   eviction is the sole removal and it is destructive and corrupting
   (`986c52fdc`). Building deletion would be a larger change than building
   discount.

### 1.3 Why not CON demotion

CON (the type-3 self-edge marking supersession) differs from discount on
four axes:

1. **Binary vs graded.** CON is all-or-nothing. A fact contradicted once
   after ten confirmations is treated identically to a fact contradicted
   on its first test. Discount accumulates proportionally.
2. **Write-once vs reversible.** Once CON-marked, no path restores the
   fact. Discount decreases on confirming evidence (rehabilitation).
3. **Invisible to the consumer that needs it.** `bootstrap_miss` does not
   check `is_superseded` (teach-observe finding 3a). CON is visible to
   `activate` and `ev_act` but not to bootstrap. Discount's defining
   requirement is a production read path in `bootstrap_miss`; without it,
   discount would be CON-shaped theater.
4. **Different epistemic situations.** CON marks "superseded by a newer
   value for the same (s,r)" (a lifecycle event). Discount marks "evidence
   has accumulated against this fact's reliability" (an epistemic
   judgment). A fact can be superseded but undisputed, disputed but
   current, or both. The mechanisms are orthogonal, not substitutes.

### 1.4 Discount vs confidence

Discount is not a confidence value on the fact's truth. It is a
liability score on the fact's use as evidence. A heavily discounted fact
may still be true (it was the genuine 99 among self-generated 42s). The
claim is narrower: this fact has been associated with inference failure
often enough that the bootstrap should stop counting it. Truth and
evidence-eligibility are separated deliberately, because the system
cannot reliably determine truth without source provenance (Section 6.3).

## 2. Minimal machinery

### 2.1 State

**D1. Discount field.** One signed i32 per FACT node. Proposed location:
field 12 (byte offset 12), currently unused on tag-1 FACT nodes per the
genuine-state layout census (fields in use: 0 tag, 20 s, 24 r, 28 o,
32 clock, 36 live; fields 4, 8, 12, 16 free). Initialized to 0 at node
creation in all five FACT-writing paths (`ev_teach`, `ev_teach_in`,
`promote_graph`, `bootstrap_miss`, `t2_revise_graph`).

**D2. Threshold T.** One global integer, researcher-chosen, stored as a
constant (not learner-writable in the minimal spec). Proposed initial
value: T=2. Rationale: T=0 would exclude on first suspicion (too
aggressive, equivalent to binary); T=1 allows one free contradiction;
T=2 requires a repeated pattern before exclusion. The exact value is a
researcher-owned decision (Section 7); the learner owns only the
per-fact discount values.

**D3. Confirmation floor.** Lower bound -C on discount (proposed C=5),
preventing runaway negative accumulation from repeated confirmations of
a long-lived fact. Without a floor, an ancient fact could accumulate
arbitrary negative discount, making future contradiction effectively
impossible to register. The floor keeps the mechanism responsive.

No new node types. No new edge types. No new opcodes. One field, one
constant, one floor.

### 2.2 Write paths

**W1. Contradiction increments.** In `ev_observe`, on the mismatch path
(existing fact value != observed value): `discount(old_fact) += 1`, in
addition to the existing CON edge and `revise_on_contradict` call. The
observation contradicts the stored fact; the stored fact becomes more
suspect. This is the observation-driven write path.

**W2. Confirmation decrements.** In `ev_observe`, on the match path
(existing fact value == observed value): `discount(matched_fact) -= 1`,
floored at -C. The observation confirms the stored fact; suspicion
decreases. This is the rehabilitation path and the reason discount is
not write-once.

**W3. Minority increments on bootstrap failure.** In `bootstrap_miss`,
when the unanimity check fails AND a strict majority exists (the modal
value has strictly more than half the counted votes): for each counted
fact whose value != modal value, `discount(fact) += 1`. The outlier
facts are associated with an inference failure; they become more
suspect. On a tie (no strict majority), no discount is written; the
mechanism declines to judge genuinely ambiguous evidence.

W1 and W2 are the symmetric observation-driven pair. W3 is the
inference-driven path and the one that makes the contradiction break
recoverable (Section 4). W3 is also the most heuristic of the three
(Section 6.3); it is included because without it, teach-path
contradictions (which bypass `ev_observe`) can never be discounted.

Note on `ev_teach`: teaching performs no contradiction check, so no
discount write occurs on the teach path. A teacher re-asserting a value
does not automatically rehabilitate it. This is conservative: teaching
is instruction, not evidence, and conflating the two is the existing
teach/observe problem, not something discount should deepen.

### 2.3 Read paths

**R1. Bootstrap evidence exclusion (REQUIRED).** In `bootstrap_miss`,
the evidence scan skips FACTs with `discount > T`. This is the defining
read path. Without it, discount is write-only theater (the T4 pattern).
The scan is otherwise unchanged: same relation filter, same
most-recent-first order, same cap of 6, same unanimity gate at k=3.

**R2. Retrieval bid penalty (OPTIONAL, not minimal).** `activate` could
subtract a bid penalty proportional to discount. This would make
discounted facts rank lower in query answers. Excluded from the minimal
spec because: (a) it changes query semantics beyond the stated problem
(bootstrap fragility); (b) the CON mechanism already handles the
"replaced value" case for retrieval; (c) each additional read path is
a new behavioral surface to validate. Documented here as a design
option for future work, not part of the minimal mechanism.

**R3. Trial premise filtering (OPTIONAL, not minimal).** `t2_gather`
could exclude discounted facts from licensing premises. Excluded for
the same reasons as R2, plus: trial construction on suspect premises is
a subtler question (a suspect premise with no alternative may be better
than no premise). Open design question.

The minimal mechanism is D1+D2+D3+W1+W2+W3+R1. One field, one threshold,
one floor, three write paths, one read path.

### 2.4 Reachability

Unlike H3-lite Node 2 (proven unreachable, `b0ad6c5d3`), every discount
write path is reachable from the initial state:

- W1/W2 fire on the first `ev_observe` call (no precondition beyond a
  stored fact).
- W3 fires on the first non-unanimous bootstrap with a strict majority
  (no precondition beyond the existing bootstrap machinery).
- R1 is active from initialization (discount 0 <= T for all facts).

There is no circular dependency: the discount values start at 0, the
threshold is a constant, and the write paths do not require prior
discount state. The mechanism is live from the first experience.

## 3. Relating discount to the bootstrap

### 3.1 How bootstrap uses discount

The modified `bootstrap_miss` evidence scan:

1. Scan live tag-1 nodes with matching relation, most-recent-first,
   cap 6 (unchanged).
2. Skip nodes with `discount > T` (new, R1).
3. Collect values from eligible nodes (unchanged logic on the
   filtered set).
4. If fewer than k=3 eligible facts: return -2 (BOOTSTRAP_FEW,
   unchanged).
5. If unanimous: teach inferred value via `ev_teach_in`, return it
   (unchanged).
6. If not unanimous: apply W3 (discount minority facts), return -2
   (unchanged return, new write).

The unanimity gate still does its job (contradiction stops inference).
Discount adds the exit: repeated stops accumulate suspicion on the
outlier until it is excluded, and inference resumes on the remaining
evidence.

### 3.2 Recoverability: the contradiction-break scenario replayed

Phase 3-5 of `510b6cb42` with discount (T=2):

- Contradiction taught: (3001,50,99), discount 0. Window:
  [99(d0), 42(d0) x5].
- Query 1: not unanimous. Strict majority (five 42s vs one 99).
  W3: discount(99-fact) = 1. Return -2.
- Query 2: 99-fact discount 1 <= 2, still counted. Not unanimous.
  W3: discount(99-fact) = 2. Return -2.
- Query 3: 99-fact discount 2 <= 2, still counted. Not unanimous.
  W3: discount(99-fact) = 3. Return -2.
- Query 4: 99-fact discount 3 > 2, excluded by R1. Eligible window:
  [42 x5]. Unanimous at 5 >= k=3. Bootstrap fires, returns 42,
  teaches new 42-fact. The loop resumes.

Bound: at most T+1 failed bootstraps before exclusion, then
recovery. Compare: currently infinite (permanent break); external
recovery required 6 taught facts. Discount gives a learner-internal
exit with a bounded cost of T+1 = 3 wasted queries.

Note what did NOT happen: the 99-fact was not deleted. `activate`
still returns 99 for (3001,50). The fact persists in the store; it is
only excluded from bootstrap evidence. If later observations confirm
99 (W2), its discount decreases and it re-enters the evidence pool.
The mechanism degrades gracefully rather than committing
irreversibly.

### 3.3 The minimal change, isolated

If only one change were permitted, it would be W3+R1 (minority
discount on bootstrap failure plus evidence exclusion). W1/W2 handle
the observe path, but the contradiction-break probe's Phase 3 used
`ev_teach` (no observe, no contradiction check), so W1/W2 alone would
not have recovered that scenario. W3 is the load-bearing write path
for teach-path contradictions. R1 is load-bearing for all of it:
without the read path, every write is theater.

Minimal recoverable subset: D1 (field) + D2 (threshold) + W3 + R1.
W1, W2, D3 are natural completions, not strictly required for the
exit.

## 4. Distinguishing discount from H3-lite

### 4.1 Node 2 (guide template policy)

H3-lite Node 2 moves the inquiry guide default action/content into
learner state. It answers: "when I am uncertain, what action should
I take?" Discount answers: "when I am inferring, which stored facts
should I trust as evidence?" Different node types (guide nodes vs
FACT nodes), different consumers (`ev_act` vs `bootstrap_miss`),
different triggering experiences (uncertainty resolutions vs
contradictions and inference failures).

They are complementary, not overlapping. A system could have optimal
inquiry guides and still need discount (contradictory evidence
paralyzes bootstrap regardless of how well uncertainty was
investigated). A system could have perfect discount and still need
guides (uncertain situations require action selection even with
clean evidence).

Node 2 is additionally proven unreachable (`b0ad6c5d3`, circular
dependency in the majority-of-three rule). Discount has no such
defect (Section 2.4). The mechanisms are independent; Node 2's status
does not affect discount's viability.

### 4.2 Node 1 (trial order policy)

Node 1 revises which assembler family to try first. Discount revises
which facts count as evidence. If both existed, they would compose:
discount cleans the evidence pool, Node 1 orders the trial families
that consume it. No interference: Node 1 reads policy node fields;
discount reads FACT field 12. Disjoint state, disjoint consumers.

### 4.3 Node 3 (repair topology policy)

Node 3 selects revision repair topologies based on success counters.
Discount's W1 write path fires in `ev_observe` on mismatch, adjacent
to but independent of `revise_on_contradict`. If Node 3 existed and
discount existed, a contradiction would both increment discount on the
old fact (W1) and trigger topology-selected revision. Complementary:
discount judges the evidence, Node 3 judges the repair method.

### 4.4 Summary of the distinction

H3-lite moves three fixed choices into learner-state policy nodes
(trial order, inquiry defaults, repair dispatch). Discount adds a
per-fact epistemic liability score with its own read/write paths.
H3-lite is about *how the system acts*; discount is about *what the
system trusts*. Both are bounded L2 (researcher-defined mechanism,
learner-filled values), but they occupy disjoint mechanism space.

## 5. What discount does not solve

### 5.1 Source conflation (the deep limit)

Discount is source-blind. W1 treats a contradicted teaching identically
to a contradicted observation. W3 treats a minority self-generated
guess identically to a minority genuine observation. The teach/observe
analysis (`8744796fb`) showed the conflation is load-bearing; discount
works within it, not against it.

Consequence: in the contradiction-break scenario, the discounted 99-fact
was the only genuine evidence, and the preserved 42s were
self-generated. Discount (via W3) excluded truth to preserve a
self-referential loop. The mechanism fixed fragility by doubling down
on the epistemic problem. This is stated plainly because it is the
central honest limit: discount trades epistemic purity for robustness,
and the trade is only acceptable because the alternative (permanent
paralysis from one observation) is strictly worse. Source provenance
remains the actual fix; discount is a pragmatic mitigation.

### 5.2 The V2 hole

Discount does not touch revision correctness. `t2_revise_graph` still
accepts any repair with `out != -999999` without checking
`out == new_o` (`705833a27`). A discounted fact that licenses a MAP
still triggers revision on contradiction; the revision can still be
wrong-but-running and accepted. Orthogonal mechanisms.

### 5.3 Self-referential confidence

Section 5.1's consequence restated: discount with W3 makes the
bootstrap loop *more* robust, and the loop is epistemically ungrounded
(`ee7815de8`). After discount excludes the 99, the loop runs on
purely self-generated 42s with no remaining internal check. Discount
removes the only thing that was stopping it (the contradiction).
The unanimity gate was accidentally serving as a grounding check;
discount routes around it.

This is not an argument against discount (permanent paralysis is
worse), but it is an argument that discount must be paired with
source separation before any confidence claim. The bootstrap's
"confidence" after discount-assisted recovery is confidence in
self-consistency, not confidence in truth.

### 5.4 Learner-internal criteria

The threshold T, the majority rule, the W1/W2/W3 triggers, and the
R1 exclusion are all researcher-authored. The learner does not choose
to discount; it executes the rule. The per-fact discount values are
learner-state (they change with experience), but the *criterion* for
discounting is fixed. This is bounded L2 structural learning in the
H3-lite pattern, not L3, not a learner-internal criterion in the
K-H2 sense. A learner that invented its own discounting policy would
be a further step; this spec does not take it.

### 5.5 Forgetting (R1-R6)

Discount is adjacent to forgetting requirement R1 (retention priority
in learner state) but does not implement it. Discount modulates
evidence eligibility; it does not delete, compress, retire, or
reclaim. R2 (utility-grounded deletion), R3 (compression), R4
(retirement), R5 (revisable forgetting), R6 (dependency-aware
eviction) are all unaddressed. Discount is an epistemic mechanism,
not a retention mechanism, though a future retention policy could
read discount values as one input among others.

## 6. Treadmill and validity risks

### 6.1 The threshold T

T is a researcher magic number. If T is tuned per benchmark until a
desired result appears, it is a treadmill surface. Mitigations, in
order of strength:

1. Fix T once (proposed: 2), document the choice and its rationale,
   never tune it against results.
2. Report sensitivity: any evaluation using discount must report
   results at T=1, T=2, T=3 to show the finding is not
   threshold-fragile.
3. Long-term: make T itself learner-writable (a further H3-lite-style
   node), moving the choice from researcher to learner state. Out of
   scope for the minimal spec.

### 6.2 The majority heuristic (W3)

W3 assumes the majority is more likely correct. In adversarial or
low-redundancy worlds, the majority can be wrong (five
self-generated 42s vs one genuine 99, as demonstrated). W3 then
punishes truth. This is inherent to any source-blind heuristic and
cannot be fixed within discount; it requires source provenance.
The spec includes W3 because the alternative (no teach-path
discount write) leaves the demonstrated fragility unfixable, but
W3 should be flagged in every evaluation as the highest-risk
component.

A conservative variant: W3 fires only when the minority facts are
themselves bootstrap-generated or otherwise suspect. But
"suspect" requires source info the system lacks. The variant
collapses to the provenance problem. Documented as a known
limitation, not resolved.

### 6.3 Interaction with the confirmation floor

The floor -C bounds rehabilitation. If C is too small, long-confirmed
facts are as fragile as new ones (a single contradiction erases years
of confirmation). If C is too large, ancient facts become
undiscountable (discount can never climb out of a deep negative
well). C=5 is proposed as a middle value; like T, it is a researcher
choice that must be fixed and sensitivity-reported, not tuned.

### 6.4 Validity condition

Discount is valid as a *fragility fix* if and only if R1 has a
production read path in `bootstrap_miss` (no theater) and the
evaluation reports T-sensitivity (no threshold tuning). Any
implementation missing R1 is write-only and must be classified with
the theater audit. Any evaluation tuning T per result is
benchmark-fitting and invalid.

## 7. Standing metrics (for this specification)

This is a specification; no implementation exists, so behavioral
counts are zero. The researcher-owned vs learner-owned accounting
below describes what an implementation *would* record.

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 in this document
  (specification only). An implementation would add: discount field
  layout, threshold T, floor C, W1/W2/W3 trigger rules, R1
  exclusion rule, strict-majority definition. Estimated: 7.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (no implementation).
  An implementation would produce: per-fact discount values
  (learner-writable, experience-driven). Counted per fact.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 (the discount criterion is
  researcher-authored; Section 5.4).
- REUSE EVENTS: 0.
- REVISION EVENTS: 0.
- COGNITION LINES: 0 added (specification only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

Classification if implemented: bounded L2 (researcher-defined
mechanism, learner-filled values), H3-lite pattern. Not SUF, not L3,
not a learner-internal criterion.

## 8. Recommended next steps (for the coordinator, not this task)

1. **Empirical validation (unfrozen variant).** Implement D1+D2+W3+R1
   (the minimal recoverable subset, Section 3.3) and replay the
   contradiction-break battery. Predicted: recovery within T+1
   queries, 3/3 byte-identical. This is the falsifiable core of
   the spec.
2. **T-sensitivity.** Run the same battery at T=1,2,3. The
   recoverability claim must hold across all three; the bound
   (T+1) should scale accordingly.
3. **Adversarial W3.** Construct a world where the majority is
   wrong and W3 punishes truth. Measure the damage. This bounds
   the heuristic's risk (Section 6.2).
4. **W1/W2 completion.** Add the observe-path writes and test the
   `ev_observe` contradiction scenario (Phase 7 of `510b6cb42`).
   Predicted: the observe-taught 99-fact accumulates discount via
   W1 on subsequent contradictions, and rehabilitation via W2
   works on confirmation.
5. **Do not proceed to R2/R3** (retrieval/trial read paths) until
   R1 is validated. Each read path is a separate behavioral claim.

None of the above is authorized by this task. This task ends at
specification.

**Verdict: DISCOUNT-COMPLETE.**
