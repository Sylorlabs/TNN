# The Four Banked Decisions for Micah

Date: 2026-10-01 (PDT). Status: COMPILATION ONLY. NOT SENT. NOT DECIDED.

This document compiles the four decisions currently banked for Micah into
one place. It transcribes what each source document already says: the
decision, the recommendation on record, and what Micah is asked to decide.
It makes no new recommendations and no decisions.

Bottom line for the whole set: TNN-2 is fixed templates with variable
content, a real L2 advance, but the envelope is unchanged in kind. FW 4/9
(byte-identical to TNN-1, diagnosis falsified). GW 2/8. Ledger 159 claims,
zero new SURVIVES, L3 zero. The four decisions below determine the
direction of TNN-3.

---

## Decision 1: Protected-core structural operations

**Source:** `docs/lab/research-lead/overnight-20260928/protected_core_decision/PROTECTED_CORE_BRIEF.md` (commit `092566072`). PREPARED FOR MICAH, NOT DECIDED.

**What it is:** May the protected core expose structural graph mutation
operations to learner-built executable graphs, and if so, which?

**Background:** The frozen TNN-2 ISA (MOVE, BRANCHEQ, INC, DEC over frame
registers) has one read bridge into the workspace and no write bridge
back. A learner-built executable graph cannot allocate a node, write a
node field, link or kill an edge. The H3 hypothesis (procedures as
learner-built graphs) requires closing this effect-domain gap. The H3
probe (`94cecdba4`) proved the revision procedure cannot be expressed
without structural effects. Growing the core, even with domain-neutral
operations, changes the protected-core boundary, which is why this is
Micah's decision under the escalation boundary.

**The four alternatives:**

- **A. Forbid structural ops.** ISA stays 4 ops. Full H3 permanently
  impossible. H3-lite remains available. Recommendation: reject (too
  strong; the H3 probe showed the gap is tractable and well-localized).
- **B. Allow the minimal structural set.** ALLOC, WF (field write), LINK,
  KILL, structural READ. ISA grows to ~10 ops. Full H3 becomes
  architecturally possible. Irreversible in practice.
- **C. H3-lite only, defer the structural decision. RECOMMENDED, NOT
  DECIDED.** Parameterize the three mechanisms' researcher-chosen
  decision points as reads from learner-state policy nodes, with
  production write paths from experience. No ISA change. Revisit the
  structural question only with explicit triggers (H3-lite implemented
  and evaluated; H3-lite shows a "criteria without procedures" ceiling;
  a sealed world requires a procedure topology H3-lite cannot express).
- **D. A second executable graph type.** Rejected by the brief; conflicts
  with the One-System Rule. Included for completeness.

**What Micah is asked to decide:**

1. Whether H3-lite may proceed to its own preregistration.
2. Whether the structural question stays banked with the triggers above.
3. Whether Alternative A (permanent prohibition) is rejected, keeping
   the question open.

**Explicitly not decided here:** whether to build TNN-3, the TNN-3 kill
bars, or any change to the frozen TNN-2 binary (it stays frozen
regardless).

---

## Decision 2: TNN-3 kill-bar open questions (six of them)

**Source:** `docs/lab/research-lead/overnight-20260928/tnn3_killbar_review/KILLBAR_REVIEW.md` (commit `eb354e3a2`). REVIEW ONLY. All bars remain DRAFT-NOT-FROZEN.

**What it is:** An independent achievability review of the TNN-3 kill-bar
draft (`76231baa8`): 11 bars (K-T3-ADV, K-T3-TOPO, K-T3-CON-1/2,
K-T3-INQ-1/2/3/4, K-T3-REV-1/2/3). Verdict: all 11 achievable by a
genuinely general mechanism within the frozen ISA, each
deterministically failed by a clever TNN-2-type L2 system, no
redundancy, no blocking inconsistencies. Plus a master bar inventory
(`1722884ad`) now stands at 24 bars: 21 minimal TNN-3, 2
future-generation (K-COMP-OP, K-INQ-INFO), 1 audit-grade (K-STATE-RET).

**The six open questions and the review's recommendations:**

- **Q1. World counts.** Recommendation: raise inquiry evaluation to 5+
  scenarios (INQ-1..INQ-4 need 7 scenario slots; 3 forces triple-booking).
- **Q2. TOPO(b) builder burden.** Recommendation: keep the requirement;
  specify the signature-log format in the prereg (test instrumentation,
  not architecture).
- **Q3. Signature function.** Recommendation: ONE function fixed in the
  frozen prereg, not per-world functions (simpler to audit, harder to
  game).
- **Q4. INQ-3 prescriptiveness.** Recommendation: keep as drafted; the
  bar prescribes an observable (ACT selects the dominating guide in both
  swap scenarios), not an internal criterion.
- **Q5. Kill bars vs falsifiers.** Recommendation: keep all as kill bars;
  do not promote to falsifiers. Failure must not be misclassified as
  rule-breaking.
- **Q6. C0-A regression bars.** Recommendation: retain as regression bars;
  do not strengthen. TNN-2 genuinely achieved C0-A; the L3 advance is in
  B/C/D.

**What Micah is asked to decide:** Answer the six questions (accept or
reject each recommendation), which unlocks the TNN-3 preregistration
freeze. Also noted: a state-retention probe for the governance audit
(audit-grade, not bar-grade), per the review's one minor gap.

---

## Decision 3: K-H3 policy-revisability bar review

**Source:** `docs/lab/research-lead/overnight-20260928/tnn2_h3lite/H3LITE_DESIGN.md` section 6 (commit `22197da2c`). DRAFT-NOT-FROZEN.

**What it is:** The H3-lite design (three learner-state policy nodes:
trial search order, guide template, repair dispatcher; `22197da2c`)
drafts one prereg kill bar, K-H3, for Micah's review before it can
govern anything.

**K-H3 (Policy Revisability), draft language:** For every structural
decision the mechanism makes that is not determined by its immediate
input, the preregistration must list: (1) the decision, (2) the
learner-state node and fields storing it, (3) the production
(non-test) code path writing those fields, (4) the experience event
triggering the write, (5) a sealed test showing the decision taking
different values after different experience histories.

**Failure conditions (any one fails K-H3):** (a) structural decision as
a source literal/loop bound/straight-line code with no learner-state
read (the frozen TNN-2 condition for all three mechanisms); (b) read
from learner state but no production write path (read-only policy,
revisability theater); (c) write path exists but unreachable in the
sealed evaluation (write-path theater); (d) demonstration histories
directly encode the expected decision (the change must be an outcome,
not an input).

**Explicit scope limit:** Passing K-H3 does not establish L3. It
establishes that the mechanism's policies are revisable by experience,
a precondition for any procedure-level learning claim. Full H3
(procedures as learner-built graphs) would need a stronger bar; that
bar is not drafted because the protected-core structural-ops decision
(Decision 1) is unresolved.

**What Micah is asked to decide:** Review K-H3 and either freeze it as
the governing bar for H3-lite's preregistration or send it back with
changes.

---

## Decision 4: Full TNN-3 preregistration

**Source:** `docs/lab/research-lead/overnight-20260928/tnn3_prereg_struct/PREREG_STRUCTURE.md` (commit `206499c03`); roadmap `67a420cca`; bar priority `20d810d4b`; integrated roadmap with bar phases in `roadmap_update/` (swept into `bbe79ddf1`). All DRAFT-NOT-FROZEN.

**What it is:** The full TNN-3 preregistration is pending Decisions 1-3.
The structure is drafted (10-section outline, 24-bar inventory with
dependencies, 5 gaps identified) but nothing freezes until Micah rules.

**Roadmap order (fixed):** Step 1: H2 masked probes. Step 2: H3-lite.
Step 3: repair-proposal generator plus inquiry resolution. Step 4: H1
widening, only after H2 (widening before H2 is the treadmill). Reuse
path in parallel with Step 2.

**Bar priority (21 minimal bars, P0-P4+PX):** Phase 0: K-T3-ADV
(process precondition). Phase 1: K-H2-1..4, K-STATE-RET (audit;
runnable now against frozen TNN-2; treadmill guard). Phase 2: reuse
(K-REUSE-1/2) and H3-lite (K-H3) in parallel. Phase 3: mechanism bars
(K-T3-INQ-1/3, K-T3-REV-1/2/3, K-T3-INQ-2). Phase 4: H1 widening bars
(K-T3-CON-1, K-TSEL-1/2, K-T3-TOPO, K-T3-CON-2, K-T3-INQ-4), H2-gated.
Integration: K-XMECH rides the sealed battery. Critical path:
K-T3-ADV to K-H3 to Phase 3 to K-TSEL-1/2.

**What Micah is asked to decide:** The whole TNN-3 preregistration:
approve the roadmap order, freeze the bars (resolving the six open
questions from Decision 2), and authorize implementation to begin.

---

## Relationships among the four

- Decision 4 (full preregistration) depends on Decisions 1, 2, and 3.
- Decision 1 (protected-core) is the governance gate: the preregistration
  freezes the ISA, so the structural question must be resolved before
  the freeze, not after.
- Decision 2 (six questions) is the content gate for the bars the
  preregistration freezes.
- Decision 3 (K-H3) is the smallest unit: it can be frozen independently
  to govern just the H3-lite preregistration, even while Decision 4
  awaits the other answers.
- The H2 freeze (a subset of Decision 4, prepared in
  `micah_brief_h2/H2_BRIEFING.md`) is the first executable step: three
  sealed trap worlds (`86389b108`) await Micah freezing K-H2-1..K-H2-4
  and authorizing the evaluator.

## Provenance

- This compilation: preparation only. NOT SENT. No decisions made.
- Transcribed recommendations only; nothing here invents a recommendation
  not present in the cited source.
- Suggested reading order for Micah: `reading_guide/READING_GUIDE.md`
  (10-min / 30-min / 1-hour tracks).
