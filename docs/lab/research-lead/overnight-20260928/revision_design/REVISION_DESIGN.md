# TNN-3 Revision Design (Draft)

**Status: DRAFT-NOT-FROZEN.** This document drafts a revision design; it
implements nothing, freezes nothing, and authorizes no work. It becomes
binding only if a TNN-3 preregistration references it and Micah approves.
No em dashes are used in this document per the loop style rule.

Date: 2026-10-01 (UTC). Drafter: Revision Design Drafter.
Input: `revision_advice/REVISION_ADVICE.md` (commit `5a009ff87`), adopted
in full and transcribed here as a design specification.

Verdict on completion: REVISION-DESIGN-COMPLETE.

## 0. Design summary

TNN-3 revision is built from two separable changes:

1. **Copy-and-commit:** revision proposes each candidate repair as a fresh
   cell set sharing (not moving) the unedited remainder of the original
   graph, verifies candidates, and commits the winner by updating the MAP
   node's root and answer fields. Nothing is revised in place.
2. **MAP retargeting:** the contradicted object is the MAP, not the fact.
   No shadow fact is taught on MAP revision. The MAP node persists across
   revisions, giving procedure identity across revision.

Together these fix the two frozen defects: the revision-corruption bug
(`bug_report/REVISION_BUG.md`, in-place revert broken by frame-allocator
aliasing) and the one-shot limit (second contradiction on the same (s, r)
never reaches the graph). Minimal TNN-3 keeps the single-schema repair
operator on this new substrate; widening to multiple repair families is a
later, separate phase.

## 1. Copy-and-commit procedure

On a contradiction that reaches a live MAP (see section 2), the revision
machinery executes these four steps in order:

**Step 1, propose.** Build each candidate repaired graph as a fresh cell set
that shares (references, does not move) the unedited remainder of the
original graph. The original graph is never tombstoned during the search.
The existing cell assemblers (`t2_lit`, `t2_set`, `t2_guard`, `t2_mov`,
`t2_inc`, `seq_link`, `t2_kill_edge`) already produce fresh cells; this is
the pattern the revision-generalization analysis specified ("tombstoning
only after a winner verifies"). Minimal TNN-3 uses the single-schema
operator: tombstone the stale BRANCHEQ-guarded SETREG, insert a new SETREG
holding the observed literal, assembled as a fresh cell set over the shared
remainder.

**Step 2, verify.** Run each candidate through `t2_try_verify` against two
evidence sources: (a) the triggering observation `o`, and (b) the retained
licensing facts reachable from the MAP's ET_DEP edges. The retained set
exists in learner state today and is unused by TNN-2 revision; using it is
what makes a repair a repair rather than a one-case fix. Candidates are
tested in the stated minimality ordering (smallest cell-set delta first,
ties by assembly order); the first verified winner is committed.

**Step 3, commit.** On the first verified winner, point the MAP's stored
root (MAP field 20) at the winning graph and update its answer field (MAP
field 28). Free the losing candidates. Tombstone the superseded original
cells only after the commit, outside any verification. The commit is a
single field update on the MAP node plus cleanup; no graph is ever patched
in place.

**Step 4, fail honestly.** On total verification failure (no candidate
verifies), change nothing, mark the MAP superseded (type-3 self-edge), and
teach the observation as a fact. This is the reuse-path design's section
4.3 rule, adopted unchanged. Future queries on (s, r) then answer from the
fact path with the MAP skipped.

**Why the bug class is gone.** There is no in-place revert path to be
corrupt, because nothing is reverted: the original graph is untouched
throughout the search, failed candidates are freed, and the commit is a
single field update on the MAP node. Verification never runs while any
node the commit depends on is tombstoned, so the frame-allocator alias
(verification's `t2_exec` clobbering the tombstoned node the revert needs
intact) cannot occur. The bug report's recommended fixes (reserve the
frame, full-field snapshot, separate free pools) are unnecessary; they were
repairs to in-place revision, and in-place revision is retired by this
design.

## 2. MAP retargeting specification

Copy-and-commit alone does not fix the one-shot limit: the second
contradiction still needs to reach the revision machinery. The design
therefore adopts the reuse path's retargeting (`tnn2_reusepath/`, section
4) as specified:

1. The contradicted object is the MAP, not the fact. `ev_observe` on a
   mismatch runs the same MAP lookup the query path uses for (s, r); the
   live MAP found there is what gets revised. Fact-level observation and
   MAP-level revision share one lookup, so the contradiction cannot fork
   into a shadow lineage.
2. No shadow fact is taught on MAP revision. Derived answers live in MAPs;
   observed answers live in facts. The fact lineage no longer forks,
   because revision no longer teaches.
3. The MAP node persists across revisions: its identity is the MAP node
   itself, and its current procedure is whatever graph its root field
   (field 20) points to. This supplies the "procedure identity across
   revision" item the C0-D analysis listed as missing.

With retargeting in place, the second contradiction on the same (s, r)
finds the same live MAP, the repair machinery proposes edits on the
current graph, and a second commit happens. Multi-step belief correction
becomes architecturally possible. Convergence is not guaranteed; the
preregistration must specify a termination policy (section 6 below).

**Floor preservation note.** FW4 (floor F2) tests law change and revert on
the fact-level path, and both TNN-1 and TNN-2 pass it at 12/12. The
MAP-level revert (GW8) fails. This design addresses the MAP level and must
not regress the fact level; regression test 4 (section 5) enforces this.

## 3. Data structures and ISA interaction

- The MAP node keeps its existing layout. The design uses field 20 (root)
  and field 28 (answer) as the commit targets, and the type-3 self-edge as
  the supersession marker. No new MAP fields are introduced.
- ET_DEP edges from the MAP to its licensing facts are read during
  verification (step 2b) and are not modified by revision.
- **No new ISA operation is needed.** The repair machinery is
  researcher-authored generic code performing ALLOC, field WRITE, LINK,
  KILL/tombstone, and structural READ, all of which frozen TNN-2 already
  performs inside `revise_on_contradict`. The 4-op ISA plus EXECUTE covers
  every edit the operators need.
- **Protected-core boundary (recorded, not decided here).** The banked
  protected-core decision (brief `092566072`, Alt C recommended: H3-lite
  only, defer structural mutation) constrains learner-originated
  structural mutation. This design does not cross it: the repair machinery
  is researcher-authored, and the learner-side contribution is selection
  (the H3-lite repair-dispatcher policy node choosing family and order),
  not mutation. If a future generation proposes learner-authored repair
  operators (K-COMP-OP territory), that crosses the line and must wait for
  Micah's ruling. Record this boundary in the preregistration.

## 4. Build and widening order

The design separates substrate from widening so each is testable alone:

1. **Copy-and-commit plus MAP retargeting (this design).** Prerequisites:
   K-REUSE-1/2 pass (the retargeting is the reuse path's section 4, so the
   bar priority's Phase 2 ordering is load-bearing for revision too).
2. **Repair-proposal generator (later widening).** Needs this substrate as
   its execution environment. Doing the repair family first, on in-place
   revision, would multiply the bug class across five operators instead of
   one. The five repair families from the revision-generalization analysis
   (guard-predicate edit, branch rerouting to existing steps, multi-step
   coordinated repair, step-count/step-type conversion, and the fifth named
   in the generalization document) plug into step 1 unchanged, without
   changing steps 2-4.
3. **Repair-dispatcher policy node (H3-lite).** The learner-state write
   path: which repair family to try first, revised by experience via the
   copy-then-revise bootstrap. This is the SUF-relevant part: without it,
   even a five-family repair space is researcher-enumerated order over
   researcher-enumerated schemas, and the SUF check on revision stays FAIL.

**Honest prediction.** Scores unchanged on FW1-FW9 (the answers are the
same; only the mechanism is sound), while the architecture gains (a)
revision that cannot corrupt itself, (b) revision that can fire twice, and
(c) an observable repair event for the kill bars to test.

## 5. Regression tests (preregistration must name all four)

1. **Failed interior revision is a byte-identical no-op.** Contradict an
   interior fact, force verification failure, assert (a) the graph
   re-executes to its pre-revision answer and (b) a white-box field dump
   of every graph cell matches the pre-revision snapshot byte-for-byte.
   The boundary mapper's pY/pZ diagnostics are the model. This test would
   have caught the frozen bug.
2. **Second contradiction revises the same MAP again.** Contradict, verify
   the repair commits; contradict the repaired answer on the same (s, r);
   assert the same MAP node is the revision target the second time and its
   root field changes. This test would have caught the one-shot limit.
3. **Revision failure supersedes, then facts answer.** Present a
   contradiction no repair family can satisfy; assert the MAP carries a
   type-3 self-edge, the observation is taught as a fact, and the next
   query answers from the fact path with the MAP skipped. The honest
   failure path must be exercised, not assumed.
4. **Floor preservation.** FW4 (floor F2) at 12/12 on all three probe
   groups: the MAP-level changes must not regress the fact-level
   law-change/revert behavior. Per the floor spec's anti-gaming clause,
   the same seven floor tests must pass with no more researcher
   scaffolding than TNN-2 needed.

## 6. Termination policy (preregistration must specify)

Because retargeting makes repeated revision possible, the preregistration
must name a termination policy so a pathological observation stream cannot
thrash one MAP forever. Minimum acceptable form: a revision budget per MAP
(e.g., N commits per MAP per evaluation battery, N frozen in the prereg),
or a no-progress detector (a commit that does not change the answer field
counts as stalled and supersedes the MAP). The policy itself is prereg
content, not design content; this design only requires that one exists and
is frozen before evaluation.

## 7. Kill bar relations

- **K-T3-REV-1/2/3** should be drafted against the copy-and-commit
  substrate first: regression tests 1-3 above are their natural content.
  They are extended when the repair family widens. The bars must not
  presuppose multi-topology repair; the substrate bars must pass on the
  single-schema operator, or the widening has no foundation.
- **K-REUSE-1/2** are prerequisites in build order (section 4, item 1).
- **K-T3-ADV** is the process precondition for any sealed evaluation of
  the substrate (bar priority Phase 0).

## 8. Treadmill-guard honesty clause

The treadmill guard's Check 1 (SUF) still FAILs on this minimal design,
which is correct and expected. This design adds safe, repeatable revision;
it does not address R3's structural-revisability ceiling, and it must not
be presented as doing so. Presenting copy-and-commit as "the revision fix"
would be failure-mode preservation (guard warning sign 6). The design's
claimed property is exactly: revision cannot corrupt the graph, and
revision can fire more than once. Nothing more.

## 9. What this design does not cover

- The five repair families' detailed semantics: see the
  revision-generalization analysis.
- The repair-dispatcher policy node: see the H3-lite design.
- Inquiry and construction: untouched. Composition of all three
  mechanisms' revisions is integration territory (K-XMECH).
- Whether multi-step correction converges in adversarial regimes: open
  question, to be measured under the sealed battery, not settled by
  design.

*End of draft. No source modified. No design adopted. No scores claimed.
Paper untouched.*
