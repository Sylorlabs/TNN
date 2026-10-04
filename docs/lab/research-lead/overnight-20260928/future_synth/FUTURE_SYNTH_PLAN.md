# Future Synthesis Pass: Plan

**Status: PLAN ONLY.** This document plans a future update to the TNN-3
design synthesis. It writes no synthesis, makes no design decision, and
changes nothing. The future pass itself must follow the same discipline
as the first: read-only collection of committed guidance, inventing
nothing.

**Verdict on this planning task: FUTURE-SYNTH-PLAN-COMPLETE.**

---

## 1. What the current synthesis covers

Commit `a01128de5` (`design_synthesis/TNN3_DESIGN_SYNTHESIS.md`) ties
together six committed inputs, verified complete by the synthesis review
(`19aa5595e`):

1. Floor spec (`f383dd11c`): 6 capabilities to preserve, 4 breaking criteria.
2. Treadmill guard (`1646b9732`): definition, 8 warning signs, 5 checks.
3. SUF implications (`b1835dec6`): Source-Underdetermined Form, zero-to-one
   recipe, per-mechanism cheapest (b) candidates.
4. Bar priority + roadmap (`20d810d4b`, roadmap in `bbe79ddf1`): 24 bars,
   phases P0-P4+PX, critical path.
5. Revision bug report (`8b58c4104`): revision-corruption bug, 3 fixes,
   regression test.
6. Reading order + open items: recommended order, preregistration open items.

The honest line: TNN-2 is fixed templates with variable content; the
envelope is unchanged in kind; ledger 159 claims, zero SURVIVES, L3 zero.

---

## 2. What the future pass should add

Two committed design documents postdate the synthesis's declared input
set and are correctly absent from it. The future pass should incorporate
both.

### 2a. Revision architecture advice (`5a009ff87`)

**Document:** `revision_advice/REVISION_ADVICE.md` (REVISION-ADVICE-COMPLETE).

**What it answers:** the revision bug (synthesis Section 5) gets a concrete
architectural answer, not just a bug description plus fix list.

**Content to incorporate:**

- **Copy-and-commit (replaces in-place revision).** Propose each candidate
  repair as a fresh cell set sharing the unedited remainder; verify against
  the triggering observation plus retained ET_DEP licensing facts; commit
  the winner by updating the MAP's root field (field 20) and answer field
  (field 28); free losers; tombstone superseded cells only after commit.
  On total failure, supersede the MAP and teach the observation as a fact.
- **Why the bug class disappears by construction.** No in-place revert path
  exists to be corrupt; the original graph is untouched during search; the
  frame-allocator alias cannot occur. The bug report's three fixes (reserve
  frame, full snapshot, separate pools) become unnecessary because they
  repaired in-place revision, and in-place revision is retired.
- **MAP retargeting (answers the one-shot limit).** The contradicted object
  is the MAP, not the fact. No shadow fact is taught on revision. The MAP
  node persists across revisions, giving procedure identity; the second
  contradiction reaches the same live MAP and revises again. Multi-step
  correction becomes architecturally possible (convergence still needs a
  termination policy in prereg).
- **Ordering.** Copy-and-commit plus MAP retargeting first; repair-proposal
  generator second; H3-lite repair-dispatcher policy node third (the
  SUF-relevant learner-state write path).
- **Protected-core boundary note.** No new ISA op is needed; the machinery
  is researcher-authored generic code using operations TNN-2 already
  performs. The banked Alternative C decision constrains learner-originated
  mutation, which this design does not cross. The prereg must record this
  explicitly.
- **Four regression tests** for the preregistration: failed interior
  revision is a byte-identical no-op; second contradiction revises the same
  MAP; failure supersedes then facts answer; FW4 floor at 12/12 with no
  added scaffolding.
- **Treadmill-guard honesty note.** SUF still FAILs on the minimal design,
  which is correct. The design must be presented as safe repeatable
  revision, not as addressing R3's ceiling (treadmill warning sign 6:
  failure-mode preservation).

**Placement suggestion:** extend synthesis Section 5 (currently the bug
report) into two subsections: 5a the bug as found, 5b the copy-and-commit
answer. Keep the bug description intact; the answer does not erase the
finding.

### 2b. Treadmill guard integration spec (`abe3d32e5`, fixed by `877d8491a`)

**Document:** `guard_integration/GUARD_INTEGRATION.md`
(GUARD-INTEGRATION-COMPLETE; spec only). Validated by `75ea448e8`
(INTEGRATION-VERIFY-COMPLETE): all six insertion points structurally
valid, no renumbering required.

**What it answers:** the treadmill guard (synthesis Section 2) gets its
operational placement in the TNN-3 preregistration structure. The guard is
a discipline, not a bar; the spec shows exactly where it lives.

**Content to incorporate:**

- **Design decision: one reference, four insertions, two notes.**
  - A (Sec 1, new 1.5): reference naming the guard as the governing
    development discipline.
  - B (Sec 2, end-of-section note): points builders to the per-capability
    treadmill analyses.
  - C (prereg structure Sec 3, Step 4 row): attaches guard warning sign 5
    (H1 widening before H2) to the Step 4 constraint.
  - D (Sec 6, new 6.9): menu check as an architecture-accounting line item
    (researcher-enumerated schema families before/after, recorded with the
    capability-source delta).
  - E (Sec 8, new 8.6): the five checks in full as a verification
    procedure, with dispositions (fail 1 or 2 = reject; fail 3/4/5 =
    return for redesign) and governance-log recording.
  - F (Sec 10, new 10.4): treadmill guard audit (five-check outcomes,
    warning signs reviewed, guard-gaming modes watched, kill-bar movement
    tracked alongside floor status).
- **Status caveat.** The guard governs nothing until Micah reviews the
  preregistration and a TNN-3 preregistration freeze commits. The spec is
  DRAFT; the synthesis must carry that status, not promote it.
- **What it does not do.** Does not turn the guard into kill bars, does not
  add bars to the inventory, does not change any existing bar.

**Placement suggestion:** extend synthesis Section 2 (the treadmill) with
a new subsection on preregistration placement, or add a short Section 7
on governance integration. Either way, keep the guard's own discipline
status explicit: it is referenced, not promoted.

### 2c. Banked decisions compilation (`f4f8fa532`) - reference update only

**Document:** `banked_decisions/BANKED_DECISIONS.md`
(BANKED-DECISIONS-COMPLETE; compilation only, NOT SENT, NOT DECIDED).

**What it is:** a single citable commit for the four banked decisions
(protected-core Alternative C recommendation, six kill-bar questions,
K-H3 review, full TNN-3 preregistration).

**What the future pass should do:** update synthesis Section 6 (open
items) to cite `f4f8fa532` as the compilation commit for the banked
decisions. No new content; just a provenance pointer so the preregistration
author can find all four decisions in one place.

**If Micah has decided by then:** the future pass should record the
decisions as decided (with commit references to Micah's ruling) rather
than as open items. This is the main reason for the timing rule in
Section 3 below.

---

## 3. When the future pass should run

**Trigger: after BOTH of the following are true.**

1. **The freeze report is reconciled and committed.** The reconciled report
   settles the empirical baseline the synthesis summarizes: the corrected
   4/9 (not the draft's 5/9), the K-FZ2-4 determinism result, the W1-W9
   battery, per-cluster analysis, post-evaluation hashes, and the
   re-clustering. The synthesis's honest line ("envelope unchanged in
   kind") should cite the reconciled result, not the provisional one.
   Ledger C160 (the freeze result claim) should also be recorded by then,
   moving the ledger from 159 to 160.

2. **Micah has ruled on the four banked decisions, or explicitly deferred
   them.** The banked decisions directly constrain synthesis content:
   - The protected-core ruling (Alternative C recommended, not decided)
     determines whether the revision advice's boundary note stands as
     written or needs revision.
   - The six kill-bar questions determine the exact bar text the synthesis
     references.
   - The K-H3 review determines H3-lite's scope in the roadmap.
   - The full TNN-3 preregistration review determines whether the guard
     integration spec's insertion points are accepted.

**Rationale.** The synthesis serves the TNN-3 preregistration. It should
reflect settled empirical facts and decided governance, not provisional
numbers and open recommendations. Running the pass before the freeze
reconciliation would bake the draft's 5/9 error (or a provisional 4/9)
into a document meant to be authoritative. Running it before Micah's
rulings would leave the four most consequential governance items as
"recommended, not decided," which is accurate but less useful than the
decided form.

**Fallback.** If Micah explicitly defers one or more banked decisions,
run the pass anyway after the freeze report lands, and mark the deferred
items as DEFERRED BY MICAH with the deferral commit cited. Do not leave
them as silently open; an explicit deferral is a decided status.

**Do not run the pass before the freeze report.** The freeze evaluator is
the empirical anchor for everything the synthesis claims about TNN-2. A
synthesis update that precedes the reconciled report would be building on
the draft the prereg audit already found wrong.

---

## 4. How the future pass should run

**Method (same as the first pass):**

1. Read-only collection. Read the new inputs (`5a009ff87`, `abe3d32e5`
   plus its fixes, `f4f8fa532`, the reconciled freeze report, Micah's
   ruling commits). Do not re-derive, re-argue, or extend them.
2. Extend, do not rewrite. Keep the six existing sections intact. Add the
   revision answer as Section 5b (or a new Section 7); add the guard
   placement as a Section 2 extension (or a new Section 8). Update Section
   6 open items with decision outcomes and the `f4f8fa532` citation.
3. Update the inputs list at the top to name the new commits.
4. Update the honest line only if the ledger or the empirical baseline
   changed (C160, reconciled 4/9, W results).
5. Keep the "invents nothing" discipline: no new bars, no new mechanisms,
   no new fixes, no banked decision made by the synthesizer.
6. Keep the DRAFT status. The synthesis governs nothing until a frozen
   TNN-3 preregistration references it.

**Worker instructions for the future pass:**

- Toolchain guard Step 0 is mandatory (safebin, `which python3 python`
  empty, record in NAMECHECK.md).
- Owned path: extend `design_synthesis/` in place; do not create a
  parallel synthesis directory.
- No em dashes in any written file.
- Paper untouched.
- No sealed contents inspected.
- Commit with explicit pathspecs; nothing pushed.

---

## 5. What the future pass must NOT do

- Must not invent new mechanisms, bars, or fixes beyond the committed
  inputs.
- Must not make any banked decision (protected-core, kill bars, K-H3,
  preregistration approval). Those are Micah's alone.
- Must not run the sealed H2 trap worlds or any new evaluation.
- Must not modify TNN-2 (frozen), the seal, or the paper.
- Must not present the revision advice as addressing R3's ceiling; the
  advice's own treadmill note (SUF still FAILs on the minimal design)
  must be carried forward.
- Must not promote the treadmill guard from discipline to kill-bar status;
  the integration spec is explicit that it stays a discipline.

---

## 6. Checklist for the future pass worker

- [ ] Freeze report reconciled and committed (verify: 4/9 corrected,
  K-FZ2-4 resolved, W1-W9 complete, per-cluster analysis, post-run
  hashes, re-clustering addressed).
- [ ] Ledger C160 recorded (ledger at 160, not 159).
- [ ] Micah's rulings on the four banked decisions located (or explicit
  deferrals cited).
- [ ] Revision advice (`5a009ff87`) incorporated as Section 5b or new
  section, with boundary note and treadmill honesty note intact.
- [ ] Guard integration (`abe3d32e5` + fixes) incorporated as Section 2
  extension or new section, with DRAFT status and discipline-not-bar
  caveat intact.
- [ ] Section 6 open items updated with decision outcomes and `f4f8fa532`
  citation.
- [ ] Inputs list and honest line updated.
- [ ] Zero em dashes; paper untouched; no sealed contents inspected.
- [ ] Committed with explicit pathspecs on `tnn-native-lab`; nothing
  pushed.
