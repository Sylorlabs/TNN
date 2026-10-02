# Banked Decisions: Status Tracker

Date: 2026-10-01 (PDT). Status: TRACKING ONLY. All four decisions remain UNDECIDED. This document records what is needed for each. It makes no decisions and adds no recommendations.

Source of record for the four decisions: `banked_decisions/BANKED_DECISIONS.md` (commit `f4f8fa532`). This tracker transcribes and monitors that compilation.

---

## Decision 1: Protected-core structural operations

**Source:** `protected_core_decision/PROTECTED_CORE_BRIEF.md` (commit `092566072`). PREPARED FOR MICAH, NOT DECIDED.

**What it asks:** May the protected core expose structural graph mutation operations to learner-built executable graphs, and if so, which?

**Alternatives on record:**
- A. Forbid structural ops. ISA stays 4 ops. Full H3 permanently impossible. Recommendation: reject.
- B. Allow the minimal structural set (ALLOC, WF, LINK, KILL, structural READ). ISA grows to about 10 ops. Irreversible in practice.
- C. H3-lite only, defer the structural decision. RECOMMENDED, NOT DECIDED. No ISA change now; revisit only on explicit triggers.
- D. A second executable graph type. Rejected by the brief; conflicts with the One-System Rule.

**Status:** UNDECIDED. Recommendation on record (Alt C) is not a decision.

**What is needed:**
1. Micah answers three questions: (a) whether H3-lite may proceed to its own preregistration; (b) whether the structural question stays banked with the recorded triggers; (c) whether Alternative A (permanent prohibition) is rejected.
2. Nothing freezes the TNN-3 ISA until this is answered, because the preregistration freezes the ISA (Decision 4 dependency).

**Who decides:** Micah. Escalation class: protected-core boundary change.

**Blocks:** Decision 4 (full preregistration freeze, via ISA freeze). Does not block H2 probes (Step 1, frozen TNN-2, no ISA change).

---

## Decision 2: TNN-3 kill-bar open questions (six)

**Source:** `tnn3_killbar_review/KILLBAR_REVIEW.md` (commit `eb354e3a2`). REVIEW ONLY. All bars DRAFT-NOT-FROZEN.

**What it asks:** Answer the six open questions on the kill-bar draft (11 bars, now 24-bar master inventory: 21 minimal + 2 future + 1 audit).

**Questions and review recommendations on record:**
- Q1. World counts. Recommendation: raise inquiry evaluation to 5+ scenarios.
- Q2. TOPO(b) builder burden. Recommendation: keep; specify log format in prereg.
- Q3. Signature function. Recommendation: one function fixed in the frozen prereg.
- Q4. INQ-3 prescriptiveness. Recommendation: keep as drafted.
- Q5. Kill bars vs falsifiers. Recommendation: keep all as kill bars, not falsifiers.
- Q6. C0-A regression bars. Recommendation: retain, do not strengthen.
- Plus: state-retention probe for the governance audit (audit-grade, not bar-grade).

**Status:** UNDECIDED. All six questions open. Recommendations on record are not decisions.

**What is needed:** Micah accepts or rejects each of the six recommendations (and the audit-grade state-retention probe). This unlocks the TNN-3 preregistration freeze.

**Who decides:** Micah. Governance: bar content gates the freeze.

**Blocks:** Decision 4 (preregistration freeze content). Does not block Decision 1 or Decision 3.

---

## Decision 3: K-H3 policy-revisability bar review

**Source:** `tnn2_h3lite/H3LITE_DESIGN.md` section 6 (commit `22197da2c`). DRAFT-NOT-FROZEN.

**What it asks:** Review the drafted K-H3 bar: freeze it to govern H3-lite's preregistration, or send it back with changes.

**Bar summary:** For every structural decision the mechanism makes that is not determined by its immediate input, the preregistration must list: (1) the decision, (2) the learner-state node and fields storing it, (3) the production (non-test) code path writing those fields, (4) the experience event triggering the write, (5) a sealed test showing the decision taking different values after different experience histories. Failure conditions (a)-(d) cover source literals, read-only policy, unreachable write paths, and demonstration-encoded decisions.

**Explicit scope limit:** Passing K-H3 does not establish L3. It establishes revisability of policies by experience, a precondition for procedure-level learning claims.

**Status:** UNDECIDED. Draft text exists; not frozen; governs nothing until frozen.

**What is needed:** Micah reviews K-H3 and either freezes it for H3-lite or returns it with changes.

**Who decides:** Micah. Governance: bar review.

**Blocks:** Nothing else strictly. K-H3 can freeze independently to govern just the H3-lite preregistration (smallest unit). Decision 1 gives the structural context for full H3 but H3-lite needs no ISA change, so Decision 3 can move in parallel with Decision 1.

---

## Decision 4: Full TNN-3 preregistration

**Source:** `tnn3_prereg_struct/PREREG_STRUCTURE.md` (commit `206499c03`); roadmap `67a420cca`; bar priority `20d810d4b`. All DRAFT-NOT-FROZEN.

**What it asks:** Approve the whole TNN-3 preregistration: roadmap order, frozen bars, authorization to begin implementation.

**Roadmap order on record:** Step 1: H2 masked probes. Step 2: H3-lite. Step 3: repair-proposal generator plus inquiry resolution. Step 4: H1 widening, only after H2. Reuse path in parallel with Step 2.

**Status:** UNDECIDED. Structure drafted (10-section outline, 24-bar inventory, 5 gaps). Depends on Decisions 1, 2, 3.

**What is needed:**
1. Decision 1 answered (governance gate: the preregistration freezes the ISA).
2. Decision 2 answered (content gate: the bars it freezes).
3. Decision 3 answered (or at least K-H3's status resolved, since it sits inside Phase 2 of the plan).
4. The 5 gaps in the prereg structure identified and closed.
5. A preregistration freeze commit that strictly precedes any implementation.

**Who decides:** Micah. Governance: full freeze authorization.

**Blocks:** All TNN-3 implementation. Nothing implements TNN-3 until this freeze commits.

**First executable subset:** The H2 freeze (K-H2-1..K-H2-4) is the first executable step. Three sealed trap worlds stand ready (`86389b108`); the H2 evaluator awaits Micah freezing K-H2-1..K-H2-4 and authorizing the evaluator (prepared in `micah_brief_h2/H2_BRIEFING.md`).

---

## Dependency summary

| Decision | Depends on | Blocks |
|---|---|---|
| 1. Protected-core | none (governance gate) | Decision 4 (ISA freeze) |
| 2. Six questions | none (content gate) | Decision 4 (bar content) |
| 3. K-H3 | none (smallest unit) | Decision 4 (Phase 2 content); can freeze independently for H3-lite alone |
| 4. Full prereg | Decisions 1, 2, 3 | All TNN-3 implementation |

Decision 4 cannot proceed until 1, 2, and 3 are answered. Decisions 1 and 2 are mutually independent. Decision 3 can be decided and frozen independently in parallel.

## Execution order allowed before any decision

- H2 probes (Step 1) run against frozen TNN-2 with a frozen K-H2 freeze: needs Micah to freeze K-H2-1..K-H2-4 and authorize the evaluator, but no TNN-3 build and no ISA change. Prepared; not run.
- TNN-2 analysis work (completed handoffs) needed no decision.
- The freeze evaluator (FW battery reconciliation) needed no decision.

## Status log

- 2026-10-01: Tracker created. All four UNDECIDED. No decision made. Nothing sent to Micah.
