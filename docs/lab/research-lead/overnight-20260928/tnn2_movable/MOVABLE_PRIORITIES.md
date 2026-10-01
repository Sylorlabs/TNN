# TNN-2 Movable Decisions: Prioritized Assessment

**Status:** Analysis only. NOT IMPLEMENTED. No source edits were made.
**Input:** Degree-of-freedom map, commit `d2af26581` (read-only).
**Target:** Frozen `tnn2.zag` at `f4de7ff46`. Cognition path only.

The DOF map identified 10 researcher decisions movable to learner state
without new opcodes, using only existing node/edge types and the frozen 4-op
ISA. This document assesses each on impact, difficulty, risk, and
prerequisites, ranks them by impact/difficulty ratio, names the top 3 quick
wins, and takes a position on whether "pure LEARNER decisions: 0" is a
problem.

Scoring convention: Impact H=3/M=2/L=1 (with halves where warranted);
Difficulty Easy=1/Moderate=2/Hard=3. Ratio = Impact / Difficulty.

---

## 1. Trial phase order (K1)

**The decision.** `t2_trial` tries assemblers in the fixed order
chains -> sums -> counts -> single hops. The movable version keeps
per-assembler success/failure counts in learner state (written by
`promote_graph`, read by `t2_trial`) and tries assemblers in order of past
success.

**Impact: Medium.** Changes which reading wins on ambiguous worlds. The DOF
map notes the masked t_f2 preference for the 2-hop reading is an order
artifact; a learner-adapted order would remove that artifact. No new
capability on unambiguous worlds. Primarily a locus-of-control move.

**Difficulty: Easy.** Add counter fields to learner state, increment on
promotion, sort the phase dispatch by counts. The phase bodies are unchanged.

**Risk: Low-Medium.** Cold start needs a sensible default (the current fixed
order as the initial prior). Existing tests could change outcome if early
success counts diverge from the fixed order, but the fixed order is itself
arbitrary, so divergence is not a regression in any principled sense.

**Prerequisites: None.** Self-contained.

**Ratio: 2.0** (2/1)

---

## 2. Chain depth bound k <= 4 (K2)

**The decision.** Chain lengths tried are fixed at k = 2, 3, 4 (longer
first). The movable version uses adaptive deepening: a learner-state miss
counter per (s, r) raises the depth cap after repeated failures.

**Impact: Low-Medium.** Would make 5+ hop chains representable, extending the
envelope slightly. The topology remains the fixed chain wiring, so the
envelope changes in size, not in kind.

**Difficulty: Moderate.** Requires per-(s,r) miss counters, depth-cap logic,
and generalizing the assembler loop beyond the hardcoded 2..4. The assembler
is likely parameterizable, but the 1000-step execution budget then binds:
deeper chains cost more steps.

**Risk: Medium.** Deeper chains increase execution cost and risk budget
exhaustion (fail-closed -999999). The current 5-hop refusal is a clean
"unrepresentable" signal; adaptive deepening could convert it into silent
budget failure, which is harder to diagnose.

**Prerequisites: None.** Related to #1 (both modify the trial loop) but
independent.

**Ratio: 0.75** (1.5/2)

---

## 3. Sum subset enumeration order (K7)

**The decision.** Sum subsets are enumerated in fixed largest-first order
(sz = m down to 1, mask descending). The movable version orders subsets by
learner-kept priors over subset sizes.

**Impact: Low, effectively zero in production.** This is a search-efficiency
optimization, not a capability change. Critically, the sum phase is gated on
`comb_present` (a type-8 node no cognition-path code can create; only test
line 1106 creates one). The phase is dead in production, so reordering its
search has no production effect.

**Difficulty: Easy.** Trivial to implement, but pointless without #4.

**Risk: None** (dead code path in production).

**Prerequisites: #4 (the comb gate).** Without resurrecting the sum phase,
this move is moot.

**Ratio: 0.0 in production** (1/1 nominal, but gated to zero)

---

## 4. The `comb_present` gate (K6)

**The decision.** The sum phase requires a type-8 node that only test
scaffolding creates. The movable version lets the learner set its own
combination-mode marker node after observing additive structure, instead of
requiring the externally created type-8 node.

**Impact: High.** Resurrects an entire dead assembler branch in production.
The sum family becomes reachable for the first time outside tests. Genuine
capability expansion within the fixed sum topology (unrolled INC chains),
though the topology itself stays researcher-fixed.

**Difficulty: Moderate.** Needs (a) a learner-observable signal of "additive
structure", (b) a marker node the learner sets, (c) the trial loop checking
the learner's marker instead of the type-8 node. The crux is (a): the
trigger for "additive structure" must itself not be a researcher-fixed rule
in disguise (e.g., "if three sums observed, set marker" is just another
fixed threshold). A defensible trigger: repeated successful verifications of
sum-shaped candidates in masked mode, which is behavioral evidence rather
than a count threshold.

**Risk: Medium-High.** If the trigger is too lax, the sum phase fires
inappropriately and burns the 900-step sum budget on non-additive worlds. If
too strict, it never fires and the move is dead. The trigger calibration is
the entire risk.

**Prerequisites: None** technically. Makes #3 relevant.

**Ratio: 1.5** (3/2)

---

## 5. Repair operator choice (P5)

**The decision.** `t2_revise_graph` implements one fixed repair: find the
DEP-tagged SET cell under its guard, tombstone it, insert a SET holding the
observed literal, rewire. The movable version trials over repair operators
(replace literal, retarget guard, drop link, change slot), each re-executed
and kept only on verification, mirroring the `t2_trial` propose/verify loop.

**Impact: High.** Directly addresses the revision red team's core finding
(single repair topology; C0-A/B/C FAIL). The generalization analysis
enumerated five structurally different repair topologies; this move lets the
learner select among operators rather than executing one. Moves revision
from L1 parameter filling toward L2 structural search. Does not address H1
(the operators themselves remain researcher-written).

**Difficulty: Hard.** Each operator needs a correct implementation with exact
revert. The trial loop must try each, re-execute, verify, and revert
failures without corrupting workspace state. This is essentially building a
mini trial loop inside revision. Significant new code on a delicate path
(the existing revert-on-failure is already subtle).

**Risk: High.** Revision's revert path is load-bearing; trying multiple
operators multiplies corruption opportunities. Each operator's revert must
be exactly inverse. A bug here silently corrupts the workspace. Also
interacts with the acceptance criterion (#9): with multiple operators, what
counts as "verified" matters more than it does for the single literal swap.

**Prerequisites: None** strictly, but pairs naturally with #6 (target
selection): the full generalization is operators x targets. Doing #6 first
is the cheaper stepping stone.

**Ratio: 1.0** (3/3)

---

## 6. Repair target selection (P3, P4)

**The decision.** The stale cell is the LAST tag-101 cell with a DEP edge to
the contradicted fact; the guard is the LAST BRANCHEQ whose field12 points
at it. Ties are broken by scan order, a deterministic artifact. The movable
version tries each matching candidate in turn, re-executes, and keeps the
first that verifies.

**Impact: Medium.** Addresses a narrower failure than #5: target selection
rather than operator selection. Helps when several stale cells or guards
match. The single-operator limitation remains the larger bottleneck, so this
is a partial fix.

**Difficulty: Moderate.** Loop over candidates instead of picking last;
re-execute each; revert failures. Less new code than #5 (no new operators,
just iteration over existing match logic).

**Risk: Medium.** Same revert delicacy as #5 but fewer moving parts. The
candidate enumeration must be complete (missing a candidate is a silent
capability loss relative to the current last-wins rule, which at least picks
something).

**Prerequisites: None.** Ideal stepping stone to #5.

**Ratio: 1.0** (2/2)

---

## 7. Guide probe content (L5)

**The decision.** `miss_inquire` copies the triggering query's (s, r) into
the guide template. The movable version chooses the probe (s', r') from
uncertainty-ranked candidates in learner state.

**Impact: Medium nominal, low real.** Would make the probe differ from the
trigger, which is a locus-of-control move. But without a discriminating-need
derivation (the L3 failure: the learner never computes what evidence would
discriminate), the probe selection criterion is itself arbitrary. Moving the
constant without making it informative changes the value, not the
vacuity. The interaction analysis found inquiry is a dead-end pipeline (no
cognition consumer reads guides); changing what the dead end contains is
low-value until the dead end is connected.

**Difficulty: Moderate.** Needs uncertainty ranking in learner state,
candidate generation, and a selection rule. The selection rule risks being
researcher-authored (another fixed criterion), which would just relocate the
hardcoding.

**Risk: Low-Medium.** Nothing in the cognition path depends on the probe
being (s, r) (guides are write-only in production), so breakage risk is low.
But for the same reason, the value is low.

**Prerequisites: None.** Note: only worth doing alongside connecting
inquiry to a consumer (the dead-end fix), otherwise it is theater.

**Ratio: 1.0 nominal** (2/2), **discounted for dead-end**

---

## 8. Action selection criterion (M4)

**The decision.** `ev_act` selects by fixed rule: argmax bid over
context-matching 1-2 hop neighbors of POLICY_ROOT, tie by edge order. The
movable version keeps per-guide learned values in learner state and selects
on those, decoupling action selection from the bid formula (bid stays for
eviction).

**Impact: Medium.** Would let the learner prefer actions with good track
records. But the candidate pool is currently content-identical guides
(constant 30/-999 differing only in s), so there is little for learned
values to differentiate. Value scales with guide differentiation (#7 and the
broader inquiry fix).

**Difficulty: Moderate.** Per-guide value storage, an update rule, and
selection on values. The hard part is the reward signal: what tells the
learner an action was good? Without a grounded reward, the "learned values"
are just another fixed rule with extra steps.

**Risk: Medium.** `ev_act` is called by the driver on act lines; FW6-style
expectations exist around its output. Changing selection could break
regression tests that expect the current behavior. The bid/action decoupling
itself is safe (bid keeps its eviction role).

**Prerequisites: None.** Low value until guides differentiate.

**Ratio: 1.0** (2/2)

---

## 9. Acceptance criterion (J3)

**The decision.** `t2_try_verify` accepts a candidate iff the executed value
equals the driver-supplied `expected` (unmasked), or accepts the first
candidate unconditionally (masked). The movable version consults a
learner-held acceptance threshold or consistency check instead of the
external answer key.

**Impact: Very High.** This is the H2 hypothesis (oracle verification). The
DOF map calls the answer key "the largest capability lever in the system and
it is not learner-owned." Moving it is the single biggest step toward
genuine discovery rather than answer-fed retrieval. Per the interaction
analysis, a self-generated verification criterion would simultaneously give
inquiry a real question and revision a real check. It conditions H1: widening
the construction grammar is pointless while verification is still oracle-fed,
because a larger menu under a generous oracle is just a larger lookup table.

**Difficulty: Very Hard.** Requires a learner-internal correctness signal,
which is exactly what the current answer-keyed design avoids. Candidate
signals (prediction error, cross-candidate consistency, simplicity,
compression) are each a research problem with failure modes. This is not a
code change; it is a research program. The synthesizer's recommended order
(H3 check, then H2 probes, then H1 widening) puts this second for a reason:
it needs its own masked-probe experiments before any implementation.

**Risk: Very High.** The oracle currently guarantees correctness on training
worlds. A wrong learner criterion promotes wrong graphs silently, which is
worse than failing to promote. Validation requires the sealed GW battery;
without it, there is no way to distinguish a good criterion from a
self-consistent delusion.

**Prerequisites: Foundational.** Nothing else depends on it technically, but
strategically it gates the value of #1-#8: moving locus of control while the
oracle remains is rearranging the waiting room.

**Ratio: 0.75-1.0** (3/3-4), **but highest strategic priority**

---

## 10. Contradiction protocol (O2)

**The decision.** On hit-with-different-value, the fixed protocol is:
CON self-edge, `revise_on_contradict`, history record, teach new fact, REF
edge new -> old, return 0. The movable version lets learner-kept track
records decide which of several conflicting facts to keep.

**Impact: Low-Medium.** Makes contradiction handling less rigid. In current
evals contradictions are rare and the fixed protocol (trust the new
observation, revise toward it) is reasonable. Value is in locus of control,
not capability.

**Difficulty: Moderate.** Track records per fact, a decision rule, and
integration with `revise_on_contradict`. The decision rule needs a
justification (recency? source reliability? corroboration?) that is not just
another fixed threshold.

**Risk: Low.** Contradictions are infrequent; the default (keep new) can
remain the prior, so worst case the behavior is unchanged.

**Prerequisites: None.**

**Ratio: 0.75** (1.5/2)

---

## Ranking by impact/difficulty ratio

| Rank | # | Decision | Impact | Difficulty | Ratio | Notes |
|------|---|----------|--------|------------|-------|-------|
| 1 | 1 | Trial phase order | M (2) | Easy (1) | **2.0** | Cleanest locus move |
| 2 | 4 | Comb gate | H (3) | Mod (2) | **1.5** | Resurrects dead branch; trigger is the crux |
| 3 | 5 | Repair operator choice | H (3) | Hard (3) | 1.0 | Core revision fix; pair with #6 |
| 3 | 6 | Repair target selection | M (2) | Mod (2) | 1.0 | Cheaper stepping stone to #5 |
| 3 | 8 | Action selection criterion | M (2) | Mod (2) | 1.0 | Needs reward signal; low value until guides differentiate |
| 6 | 9 | Acceptance criterion | VH (3) | VHard (4) | 0.75 | Highest strategic priority; a research program, not a task |
| 6 | 2 | Chain depth bound | LM (1.5) | Mod (2) | 0.75 | Envelope size, not kind |
| 6 | 10 | Contradiction protocol | LM (1.5) | Mod (2) | 0.75 | Rare path; low stakes |
| 9 | 7 | Guide probe content | M (2) | Mod (2) | 1.0 nominal | Discounted: dead-end pipeline; theater without a consumer |
| 10 | 3 | Sum subset order | L (1) | Easy (1) | 0.0 eff. | Moot without #4; do not do alone |

---

## Top 3 quick wins

**Quick win 1: Trial phase order (#1).**
Highest ratio (2.0), Easy difficulty, Low-Medium risk. Move the fixed
chains -> sums -> counts -> hops order into learner-state success counts,
defaulting to the current order cold-start. Removes the order artifact the
DOF map identified in masked t_f2. Self-contained; no prerequisites. This is
the H3-lite trial-policy node in miniature.

**Quick win 2: The comb gate (#4).**
Ratio 1.5, Moderate difficulty. Replace the externally-gated type-8 node
check with a learner-set combination marker driven by behavioral evidence
(repeated sum-shaped verifications in masked mode, not a count threshold).
Resurrects the entire sum family in production for the first time. The
trigger design is the whole task; get it wrong and the phase either never
fires or fires wastefully. Recommend a conservative trigger (high bar for
first setting, easy to unset on counter-evidence).

**Quick win 3: Repair target selection (#6).**
Ratio 1.0, Moderate difficulty, Medium risk. Iterate over all matching stale
cells/guards with re-execution instead of last-in-scan-order. Narrower than
#5 (operator choice) but much cheaper, and the natural stepping stone: once
targets are iterated, adding operators (#5) is an outer loop over the same
machinery. Do #6 first, #5 second.

**Explicitly not a quick win: the acceptance criterion (#9).** It has the
highest strategic importance (it is H2, the oracle problem, the largest
capability lever) and the worst ratio. It must be a sequenced research
program (masked probes first, per the synthesizer's order), validated
against the sealed GW battery, not a task. Anyone proposing to "just move"
it is underestimating the problem.

**Do not do alone: sum subset order (#3).** It is moot without #4. If #4 is
done, #3 can ride along as a trivial follow-up.

**Defer until the dead end is fixed: guide probe content (#7).** Changing
what a write-only pipeline contains is theater. Connect inquiry to a
consumer first (the interaction analysis's dead-end finding), then revisit.

---

## Position: is "pure LEARNER decisions: 0" a problem?

**Yes, but the fix is misdescribed as "add pure decisions."**

The MIXED category as currently constituted is not sufficient for
intelligence, because in every one of the 5 MIXED points the *selection
criterion* is researcher-fixed (argmax bid, first-to-verify under a fixed
order, lowest id, scan order). The learner's role is exhausted by "state
happens to contain value X, so the fixed rule picks index i." Data varies;
judgment does not. That is indexing, not deliberation.

But the LEARNER/MIXED binary understates the real design space. Consider
`ev_act` with a learner-held value function (movable #8): the space is still
researcher-fixed (neighbors of POLICY_ROOT) and the form is still "pick one
candidate," so it classifies as MIXED, yet the *criterion* is now
learner-shaped and revisable from experience. That is a qualitatively
different kind of MIXED from the current fixed-criterion kind.

The precise statement of the problem: **no decision anywhere in the
cognition path has its criterion owned by the learner.** Every selection
uses a researcher-fixed criterion over learner-supplied data. The learner
supplies the facts; the researcher supplies the judgment. Zero pure-LEARNER
decisions is the symptom; zero learner-owned criteria is the disease.

This reframes the 10 movable decisions. The high-value moves are exactly
the ones that relocate *criteria*, not just data:

- #1 moves the phase-order criterion (fixed order -> success counts).
- #5/#6 move the repair criterion (fixed schema/scan order -> trial over
  operators/targets with verification).
- #8 moves the action criterion (fixed bid -> learned values).
- #9 moves the acceptance criterion (external key -> internal signal).

Moves #2, #3, #7, #10 relocate parameters or constants, which is weaker:
the criterion stays fixed, only its inputs vary. Those are worth doing
(#1 shows even parameter moves have value), but they do not touch the
disease.

H3-lite is best understood in these terms: it does not create pure-LEARNER
decisions ex nihilo; it moves three criteria (search order, guide defaults,
repair preference) from source literals into learner-state policy nodes with
production write paths. That is the correct unit of progress. A future
criterion for "enough" learner authority: for every structural decision the
system makes, the preregistration can name the learner-state fields holding
the criterion and the production path that revises it. That is the K-H3 bar
the H3-lite designer drafted, and it is a better target than maximizing a
count of pure decisions.

One caution: relocating a criterion is necessary but not sufficient. A
learner-owned criterion updated by a researcher-fixed update rule (e.g.,
"swap on success" with a fixed threshold of 8) is one level up from a fixed
criterion, not the top. The H3-lite design is honest about this: its
thresholds and margins are documented as researcher-chosen heuristics. Full
regress ends at the ISA, which is correctly frozen as protected machinery.
The honest claim for the movable set is "criteria in learner state with
production write paths," not "no researcher choices anywhere."

---

## Verdict

MOVABLE-PRIORITIES-COMPLETE
