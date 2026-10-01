# Architectural Guidance: TNN-3 Revision

**Status: ADVICE ONLY.** This document advises; it designs nothing,
implements nothing, and authorizes nothing. Any TNN-3 revision work
must go through its own preregistration with frozen kill bars.
No em dashes are used in this document per the loop style rule.

Date: 2026-10-01 (UTC). Advisor: Architecture Advisor.
Verdict on completion: REVISION-ADVICE-COMPLETE.

## 0. The two constraints, stated precisely

**Constraint A: the revision-corruption bug** (`bug_report/REVISION_BUG.md`,
from boundary map Surprise 1, probe pE E4). When `t2_revise_graph` patches
an interior SETREG and the verification re-execution fails, the REVERT path
is corrupt: verification's `t2_exec` allocates its frame via `alloc_node`,
which returns the just-tombstoned stale node; `fr_set` overwrites its
fields (f4=0, f8=0, f20=frame garbage); the revert restores only node type
and live-flag. The graph is permanently broken (`t2_exec` returns -999999
forever; the SETREG slot field 0 < 1000 fails the execute guard) while
`ev_query` keeps answering the stale 201 from the promoted fact. White-box
state and query answers diverge silently. There is no repair path.

**Constraint B: the one-shot limit** (boundary map Surprise 2, probes pE
E2/E3). A second contradiction on the same (s, r) never reaches the graph:
the first revision taught a new fact, which has no graph provenance edges,
so `revise_on_contradict` finds no MAP to revise. Revision follows the
ORIGINAL fact's provenance exactly once. No convergence, no
revert-to-original, no multi-step correction. The system cannot be talked
back to the original answer through the revision path.

**Constraint C (background): the single-schema ceiling** (re-clustering R3,
revision red team `687ba0219` ATTACK-SUCCESS). `t2_revise_graph` always
produces the same topology: tombstone the stale BRANCHEQ-guarded SETREG,
insert a new SETREG holding the observed literal. The learner chose the
operands; the researcher chose the topology. All three mechanisms SUF-FAIL
(`suf_check/`, commit `8ef148a42`): the source-underdetermined decision
list is empty for revision.

## 1. The central answer: do not revise in place; copy and commit

**TNN-3 should not revise graphs in place.** It should revise on copies
and commit the winner. Concretely:

1. **Propose:** build each candidate repaired graph as a fresh cell set
   that shares (references, does not move) the unedited remainder of the
   original graph. The original graph is never tombstoned during the
   search. The existing cell assemblers (`t2_lit`, `t2_set`, `t2_guard`,
   `t2_mov`, `t2_inc`, `seq_link`, `t2_kill_edge`) already produce fresh
   cells; this is the pattern the revision-generalization analysis
   specified ("tombstoning only after a winner verifies").
2. **Verify:** run each candidate through `t2_try_verify` against (a) the
   triggering observation `o` and (b) the retained licensing facts
   reachable from the MAP's ET_DEP edges. The retained set exists in
   learner state today and is unused by TNN-2 revision; using it is what
   makes a repair a repair rather than a one-case fix.
3. **Commit:** on the first verified winner under a stated minimality
   ordering, point the MAP's stored root (MAP field 20) at the winning
   graph and update its answer field (MAP field 28). Free the losing
   candidates. Tombstone the superseded original cells only after the
   commit, outside any verification.
4. **Fail honestly:** on total verification failure, change nothing,
   mark the MAP superseded (type-3 self-edge), and teach the observation
   as a fact. This is the reuse-path design's section 4.3 rule, adopted
   unchanged.

**Why this answers Constraint A:** the bug class disappears by
construction. There is no in-place revert path to be corrupt, because
nothing is reverted: the original graph is untouched throughout the
search, failed candidates are freed, and the commit is a single field
update on the MAP node. The frame-allocator alias (verification
clobbering a tombstoned node the revert needs intact) cannot occur,
because verification never runs while any node the commit depends on
is tombstoned. The bug report's recommended fixes (reserve the frame,
full-field snapshot, separate free pools) become unnecessary; they were
repairs to in-place revision, and in-place revision is the thing being
retired.

**Why this answers the search half of Constraint C:** the same substrate
carries the multi-topology widening when TNN-3 is ready for it. The
repair-proposal generator (revision-generalization section 1) needs
exactly this shape: enumerate candidate edits, verify each, commit the
winner. Building copy-and-commit first and the repair family second
keeps the two changes separable and testable. The five repair families
already enumerated (guard-predicate edit, branch rerouting to existing
steps, multi-step coordinated repair, step-count/step-type conversion,
and the fifth in the generalization document) plug into step 1 without
changing steps 2-4.

## 2. The one-shot limit is fixed at the MAP, not in the graph

Copy-and-commit does not by itself fix Constraint B: the second
contradiction still needs to *reach* the revision machinery. The root
cause is that revision teachings are shadow facts without provenance,
so the contradiction path follows the original fact's provenance exactly
once and then forks into the void.

The fix is the reuse path's retargeting (`tnn2_reusepath/`, section 4),
which this guidance adopts:

1. The contradicted object is the MAP, not the fact. `ev_observe` on a
   mismatch runs the same MAP lookup the query path uses for (s, r);
   the live MAP found there is what gets revised.
2. No shadow fact is taught on MAP revision. Derived answers live in
   MAPs; observed answers live in facts. The fact lineage no longer
   forks, because revision no longer teaches.
3. The MAP node persists across revisions: its identity is the MAP
   node itself, its current procedure is whatever graph its root
   field points to. This supplies the "procedure identity across
   revision" item the C0-D analysis listed as missing.

With this in place, the second contradiction on the same (s, r) finds
the same live MAP, the repair machinery proposes edits on the current
graph, and a second commit happens. Multi-step belief correction becomes
architecturally possible. Convergence is still not guaranteed; the
preregistration must specify a termination policy (e.g., revision
budget per MAP, or a no-progress detector) so that a pathological
observation stream cannot thrash one MAP forever.

Note the floor-spec distinction: FW4 (floor F2) tests law change and
revert on the fact-level path and both TNN-1 and TNN-2 pass it at
12/12. The MAP-level revert (GW8) fails. The guidance above addresses
the MAP level; it must not regress the fact level. The floor spec's
breaking criteria apply.

## 3. What stays narrow, and what the widening needs

**Minimal TNN-3 revision keeps the single-schema operator**, moved onto
the copy-and-commit substrate with MAP retargeting. This is deliberate:
Constraints A and B are fixed without widening the repair space, which
means the fix is testable independently of the multi-topology question.
The honest prediction is the reuse design's: scores unchanged on
FW1-FW9 (the answers are the same; only the mechanism is sound), while
the architecture gains (a) revision that cannot corrupt itself,
(b) revision that can fire twice, and (c) an observable repair event
for the kill bars to test.

**The repair-proposal generator is a separate, later widening** (H1/H3
territory per the roadmap; Phase 3/P4 in the bar priority). It needs:

- The copy-and-commit substrate (section 1), as its execution
  environment. Doing the repair family first, on in-place revision,
  would multiply the bug class across five operators instead of one.
- The H3-lite repair-dispatcher policy node (`tnn2_h3lite/`), as the
  learner-state write path: which repair family to try first, revised
  by experience (copy-then-revise bootstrap). This is the SUF-relevant
  part: without it, even a five-family repair space is
  researcher-enumerated order over researcher-enumerated schemas, and
  the SUF check on revision stays FAIL.
- The treadmill guard's Check 4 (property check): each new repair
  family must name which cluster's SUF sub-property it addresses
  (R3's is structural revisability proper), or it is menu growth.

**Ordering constraint:** copy-and-commit plus MAP retargeting (this
guidance) before the repair-proposal generator (generalization
analysis) before the repair dispatcher (H3-lite). The bar priority's
critical path (K-T3-ADV, K-H3, Phase 3, K-TSEL-1/2) is consistent with
this order; K-T3-REV-1/2/3 should be written against the substrate
first, then against the widened space.

## 4. Protected-core interaction: no new ISA operation is needed

The banked protected-core decision (brief `092566072`, Alt C
recommended: H3-lite only, defer structural mutation) does not block
this guidance. Two distinctions:

1. **The repair machinery is researcher-authored generic code**,
   exactly like `t2_revise_graph` today. It performs ALLOC, field
   WRITE, LINK, KILL/tombstone, and structural READ, all of which the
   frozen TNN-2 already performs inside `revise_on_contradict`. The
   guidance asks for no new ISA operation and no new primitive: the
   4-op ISA plus EXECUTE already covers every edit the repair
   operators need. The banked decision constrains *learner-originated*
   structural mutation (learner-built graphs mutating graphs); the
   repair machinery is not learner-originated, so it stays on the
   permitted side of the Alt C line.
2. **The learner-side contribution is selection, not mutation.** Under
   H3-lite, learner state (the repair-dispatcher policy node) chooses
   which repair family to attempt and in what order; the researcher
   code performs the edits. If a future generation proposes
   learner-authored repair operators (K-COMP-OP territory), that
   crosses into the banked decision and must wait for Micah's ruling.
   The minimal revision design here does not cross it.

Record this boundary in the preregistration so a later dispute about
"who moved the graph" has a written answer.

## 5. Regression tests the preregistration must name

1. **Failed interior revision is a no-op (Constraint A).** Contradict
   an interior fact, force verification failure, assert (a) the graph
   re-executes to its pre-revision answer and (b) a white-box field
   dump of every graph cell matches the pre-revision snapshot
   byte-for-byte. The boundary mapper's pY/pZ diagnostics are the
   model. This test would have caught the frozen bug.
2. **Second contradiction revises again (Constraint B).** Contradict,
   verify repair commits; contradict the repaired answer on the same
   (s, r); assert the same MAP node is the revision target the second
   time and its root field changes. This test would have caught the
   one-shot limit.
3. **Revision failure supersedes, then facts answer (section 1.4).**
   Present a contradiction no repair family can satisfy; assert the
   MAP carries a type-3 self-edge, the observation is taught as a
   fact, and the next query answers from the fact path with the MAP
   skipped. This is the honest-failure path; it must be exercised,
   not assumed.
4. **Floor preservation.** FW4 (floor F2) at 12/12 on all three probe
   groups: the MAP-level changes must not regress the fact-level
   law-change/revert behavior. Per the floor spec's anti-gaming
   clause, the same seven floor tests must pass with no more
   researcher scaffolding than TNN-2 needed.

## 6. Relation to the kill bars and the guard

- **K-T3-REV-1/2/3** should be drafted against the copy-and-commit
  substrate first (tests 1-3 above are their natural content), then
  extended when the repair family widens. Do not let the bars
  presuppose multi-topology repair; the substrate bars must pass on
  the single-schema operator or the widening has no foundation.
- **K-REUSE-1/2** are prerequisites in the build order: MAP retargeting
  (section 2) is the reuse path's section 4, and the revision advice
  assumes it. The bar priority's Phase 2 ordering (reuse track before
  Phase 3 mechanism bars) is therefore load-bearing for revision too.
- **Treadmill guard checks** applicable here: Check 1 (SUF) will still
  FAIL on the minimal revision design, which is correct and expected;
  the guard's verdict for checks 1-2 is "reject," but the minimal
  design is not claiming a cluster move, so the applicable reading is
  Check 4: the design must state the property it adds (safe,
  repeatable revision) and must not be presented as addressing R3's
  structural-revisability ceiling. Presenting copy-and-commit as "the
  revision fix" would be failure-mode preservation (warning sign 6).

## 7. What this guidance does not cover

- The five repair families' detailed semantics: see the
  revision-generalization analysis. This guidance specifies only the
  substrate they run on.
- The repair-dispatcher policy node: see the H3-lite design. The
  learner-state write path is specified there.
- Inquiry and construction: untouched by this guidance. The
  composition of all three mechanisms' revisions is integration
  territory (K-XMECH).
- Whether multi-step correction converges in adversarial regimes:
  open question, to be measured under the sealed battery, not settled
  by advice.

*End of guidance. No source modified. No design adopted. No scores
claimed. Paper untouched.*
