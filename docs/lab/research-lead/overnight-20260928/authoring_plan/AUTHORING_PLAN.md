# TNN-3 Preregistration Authoring Plan

**Status: PLAN ONLY - DRAFT-NOT-FROZEN.** This document plans the authoring
work; it writes no preregistration text, freezes no bar, and decides nothing.
Micah decides all four banked decisions.

Date: 2026-10-01 (UTC). Planner: Authoring Planner subagent.
Verdict: AUTHORING-PLAN-COMPLETE.

## 1. Item-by-item specification

### A. Exact frozen bar text (prereg Section 2)

- **What it is.** The final exact kill-bar statements for every in-scope
  bar, each tied to the specific TNN-2 failure mode it targets (with commit
  references to the three red-team reports `340e94e3e`, `4e329c772`,
  `687ba0219`, the re-clustering `ed2357141`, and the GW evaluation
  `881fbb3d4`). Micah's Q1-Q6 resolutions incorporated verbatim:
  inquiry world counts (3+ vs 5+ per Q1), TOPO(b) log format (per Q2),
  any amended wording. No paraphrase of decisions; the text must match
  what Micah approved.
- **Who does it.** Prereg author (coordinator/writer subagent). Micah
  supplies the Q1-Q6 decisions; the author transcribes them into exact
  text. No one else may wordsmith a decided bar.
- **What it needs.** Decision 2 (Q1-Q6 resolutions). Draft bar text
  (exists, `1722884ad`, `76231baa8`). Red-team reports and failure-mode
  targets for the Section 2.8 citations (all committed).
- **Done when.** Every in-scope bar has one exact frozen statement;
  each statement names its failure-mode target with a commit reference;
  Q1-Q6 resolutions appear verbatim; a second reader can verify
  decision-to-text fidelity line by line.

### B. Structural signature function (prereg Section 3)

- **What it is.** The deterministic structural-signature function fixed
  in the frozen prereg: canonical string specification, calibration test
  results, frozen state-dump format. Calibration pairs are already
  specified: chain k=2 vs k=3 must produce different signatures; the
  same topology with different literals must produce identical
  signatures. Pure Zag implementation.
- **Who does it.** Two roles. (1) Zag builder (implementation subagent):
  writes the function in pure Zag, runs the calibration pairs, records
  results. (2) Prereg author: embeds the frozen specification, the
  calibration results, and the state-dump format into Section 3.
- **What it needs.** Decision 2, Q3 (review recommends one function
  fixed in the frozen preregistration, not per-world). The frozen TNN-2
  build (`f4de7ff46`) as the calibration target. The calibration pairs
  above. Safebin Step 0 guard; forbidden executables = PROCESS-FAIL.
- **Done when.** The function is written, tested, and calibrated in pure
  Zag; both calibration pairs behave as specified; the canonical string
  spec and dump format are written down; Q3's decision selects this
  function as the frozen one.

### C. Adversary protocol specifics (prereg Section 4)

- **What it is.** The K-T3-ADV implementation in full: named independent
  adversaries; post-freeze authorship verification procedure (fail
  closed); limited-visibility specification (what the adversary may and
  may not see); minimum world counts with Q1 resolved; pairwise
  distinctness procedure; per-world non-triviality rationale.
- **Who does it.** Prereg author drafts. Micah approves the named
  adversaries (naming who counts as independent is authority-adjacent;
  escalate to Micah rather than choosing unilaterally). The adversaries
  themselves execute post-freeze; they do not write this section.
- **What it needs.** Decision 2, Q1 (world counts). K-T3-ADV bar text
  (exists). A candidate adversary list (independent agents/teams with
  no stake in the build). The seal protocol template from the TNN-2
  cycle (reusable machinery).
- **Done when.** Adversaries are named and Micah-approved; visibility
  spec is explicit; world counts are fixed numbers (not ranges);
  authorship verification is a step-by-step fail-closed procedure;
  distinctness and non-triviality have checkable procedures.

### D. K-H3 five-part listing (prereg Section 5)

- **What it is.** The builder's actual listing: for every structural
  decision not determined by immediate input, all five parts:
  (1) the decision, (2) the learner-state node and fields, (3) the
  production write path, (4) the triggering event, (5) the sealed test.
  Plus the H3-lite discrimination tests as committed assets.
- **Who does it.** The H3-lite builder/designer (implementation
  subagent): this is builder authoring work that follows the H3-lite
  design. The prereg author assembles the listing into Section 5 but
  may not invent listing entries.
- **What it needs.** Decision 1 (Blocker 1: protected-core path must
  approve H3-lite proceeding to preregistration as a separate step).
  Decision 3 (K-H3 review; the bar is DRAFT-NOT-FROZEN pending Micah's
  review). The H3-lite design (`22197da2c`) as the source the listing
  is written from.
- **Done when.** Every structural decision in the H3-lite design has a
  complete five-part entry; the discrimination tests are committed
  assets; the listing survives a hostile read (no decision missing its
  write path; no write path missing its trigger).

### E. Architecture accounting baseline (prereg Section 6)

- **What it is.** The Section 6 template and attestation procedure:
  cognition source lines added; new hardcoded semantic cases (kill
  threshold: must be zero); new modes/bridges/handlers (kill threshold:
  must be zero); learner-state structures created; capability-source
  delta; ISA freeze attestation procedure. Note: the frozen prereg
  contains the template, the thresholds, and the procedure. The actual
  numbers are recorded at build-freeze time, after implementation
  begins; they are not invented in the prereg.
- **Who does it.** Prereg author writes the template, thresholds, and
  attestation procedure now. The builder fills the numbers at
  build-freeze time.
- **What it needs.** The outline's Section 6 template (exists in
  `206499c03`). The ISA freeze boundary (protected-core ruling on
  record). Nothing from Micah beyond the general preregistration
  approval.
- **Done when.** Section 6 has a fill-in template with exact fields, the
  zero-thresholds are stated as kill conditions, and the ISA freeze
  attestation is a step-by-step procedure a verifier can execute.

### F. Explicit non-claims text (prereg Section 7)

- **What it is.** Section 7: what L2 the design achieves; what L3 it
  does not; which of H1/H2/H3 it addresses and which it does not;
  honest score predictions. Must use the reconciled freeze figure
  (audit-corrected 4/9, `8959a7c14`), never the draft's 5/9.
- **Who does it.** Prereg author, with the design synthesis
  (`a01128de5`) and the roadmap's non-overselling guidance as inputs.
- **What it needs.** Design synthesis (exists). Roadmap
  (`roadmap_update/ROADMAP_WITH_BARS.md`). The reconciled freeze
  result C160 for honest predictions: draft with the audit-corrected
  4/9 now, verify against the reconciled report when it lands
  (expected ~09:00 UTC per `f6061a5a0`; not a blocker per the prereg
  check, but the author must re-check the figure before freezing).
- **Done when.** Every H-level addressed-or-not is stated explicitly;
  the L2/L3 boundary is drawn in the prereg's own words; score
  predictions are honest (no benchmark-maximizing); the 4/9 figure is
  sourced to the reconciled report or the audit.

### G. Section 9: open questions resolved

- **What it is.** Micah's resolutions to Q1-Q6 and the
  signature-function question, with rationale; any amendments to draft
  bar text with rationale. Pure transcription plus rationale capture.
- **Who does it.** Micah decides. Prereg author transcribes. The author
  may not infer, extend, or soften a decision.
- **What it needs.** Decision 2 (Q1-Q6) in full. Nothing else.
- **Done when.** Each of Q1-Q6 has Micah's resolution recorded with
  his rationale; any bar-text amendment traces to a specific decision;
  there are no open questions left in the section.

## 2. Dependency graph

```
Decision 2 (Q1-Q6)
  |---> A (bar text) ------------+
  |---> B-freeze (select fn) --->+---> consistency pass
  |---> C (adversary protocol) --+         ^
  |---> G (Section 9) -----------+         |
                                           |
Decision 1 (H3-lite path)                  |
  +--> Decision 3 (K-H3 review)            |
        +--> D (five-part listing) --------+
                                           |
(no decision)                              |
  |---> E (accounting template) -----------+
  |---> F (non-claims, draft now;          |
  |        verify 4/9 vs C160 later) ------+
  |
  +--> B-prototype (write/calibrate fn now, freeze after Q3)
```

Notes:

- E is fully writable now. No decision gates it.
- F is draftable now with the audit-corrected 4/9; the single
  verification step (re-check against reconciled C160) happens before
  freezing.
- B splits into B-prototype (Zag builder work, startable now; the
  calibration pairs are already specified) and B-freeze (the decision
  to fix this function in the prereg, gated on Q3).
- A, C, G are pure writing/transcription once Decision 2 lands; they
  are parallel with each other.
- D is the longest pole: it needs Decisions 1 and 3, then builder
  authoring against the H3-lite design, then hostile-read review.
- C has a sub-decision: adversary naming goes to Micah. If Micah
  defers naming, Section 4 can still freeze with the naming procedure
  and approval step specified, provided the prereg states that
  explicitly.

## 3. Sequencing (phases)

**Phase 1: start now (no Micah decision needed).**

1. E: prereg author writes the Section 6 template, thresholds, and
   attestation procedure.
2. F: prereg author drafts Section 7 with the audit-corrected 4/9;
   flags the C160 re-check as a pre-freeze gate.
3. B-prototype: Zag builder writes the signature function in pure Zag,
   runs both calibration pairs, records results. Safebin Step 0;
   forbidden executables = PROCESS-FAIL.

All three are parallel. None blocks anything else.

**Phase 2: after Decision 2 (Q1-Q6).**

4. A: prereg author writes exact frozen bar text with Q1-Q6 verbatim.
5. C: prereg author drafts the adversary protocol; Micah approves
   named adversaries (escalate naming as its own micro-decision).
6. G: prereg author transcribes Q1-Q6 resolutions with rationale.
7. B-freeze: Q3's decision fixes the calibrated function from
   B-prototype into Section 3; prereg author embeds spec, results,
   and dump format.

Items 4-7 are parallel with each other. Item 7 depends on Phase 1
item 3 being complete (a function must exist to be frozen).

**Phase 3: after Decisions 1 and 3.**

8. D: H3-lite builder writes the five-part listing from the H3-lite
   design; prereg author assembles Section 5; hostile-read review
   (an independent reader checks every decision has its write path).

This is the critical path's longest pole. It cannot start until both
Decision 1 and Decision 3 are resolved.

**Phase 4: pre-freeze gates.**

9. F re-check: author verifies the 4/9 figure against reconciled C160;
   corrects if the reconciled report differs from the audit.
10. Consistency pass: every in-scope bar has exact frozen text (A),
    a named failure-mode target with commit reference, and a
    verification procedure; Sections 2/3/4/5/6/7/9 cross-reference
    correctly; no dangling references to draft-only content.
11. Freeze: the prereg's first commit strictly precedes any
    implementation commit (ordering bar, git-ancestry verified).

## 4. Staging option: H2-probe preregistration first

The prereg check (`PREREG_READINESS.md`, section 5) recommends staging.
The plan supports it without modification:

- **Stage 1: H2-probe prereg** (K-T3-ADV + K-H2-1..4 + K-STATE-RET
  baseline). Needs from this plan: A scoped to the H2 bars, C, E, F
  scoped to H2, G scoped to H2-relevant questions. Does NOT need B
  (probes run against frozen TNN-2; no new signature function) or D
  (no H3-lite content). Trap worlds are sealed (`86389b108`); this
  stage is freezable as soon as Decision 2 lands.
- **Stage 2: H3-lite prereg** (K-H3). Needs: Decision 1, Decision 3,
  D, plus B and the remaining A/C/F/G scope. Follows Stage 1.
- **Stage 3: full TNN-3 prereg.** Assembles the frozen stages plus the
  mechanism bars (Phase 3 of the roadmap). Staging does not weaken
  any bar; each frozen prereg strictly precedes its implementation.

If Micah prefers a single full preregistration instead of stages,
Phases 1-4 above already describe it; skip this section.

## 5. Staffing (roles)

- **Prereg author** (coordinator/writer subagent): owns A, C, E, F, G,
  Section 3 embedding for B, Section 5 assembly for D, the consistency
  pass, and the freeze commit. One author throughout; no handoffs
  mid-document.
- **Zag builder** (implementation subagent): owns B-prototype
  (signature function in pure Zag, calibration). Reports calibration
  results; does not choose the frozen function (that is Q3).
- **H3-lite builder/designer** (implementation subagent): owns D (the
  five-part listing). Must have the H3-lite design in hand; the
  listing is written from the design, not from memory.
- **Micah** (human): owns Decisions 1-4, adversary naming approval,
  and any amendment rationale. The author transcribes; Micah decides.
- **Independent adversaries** (named in C): execute post-freeze only.
- **Hostile reader** (review subagent, Phase 3/4): checks D's listing
  and the consistency pass. Must not be the prereg author.

## 6. Pre-freeze checklist (all must be YES)

1. Decisions 1-3 resolved by Micah and recorded.
2. A: every in-scope bar has exact frozen text with Q1-Q6 verbatim.
3. B: signature function written, calibrated (both pairs), frozen per
   Q3; spec, results, and dump format in Section 3.
4. C: adversaries named and Micah-approved; fail-closed authorship
   verification is step-by-step.
5. D: five-part listing complete; hostile read passed.
6. E: template, zero-thresholds, attestation procedure in Section 6.
7. F: non-claims explicit; 4/9 figure verified against reconciled
   C160.
8. G: Q1-Q6 resolutions with rationale; no open questions remain.
9. Consistency pass: every bar has text, failure-mode target with
   commit reference, and verification procedure.
10. Freeze commit strictly precedes any implementation commit.

## 7. Risks and mitigations

- **Decision latency.** The plan's Phase 2 and 3 work cannot start
  until Micah decides. Mitigation: Phase 1 (E, F draft, B-prototype)
  runs now; the H2 stage needs only Decision 2, so partial progress
  is freezable even if Decisions 1 and 3 take longer.
- **D as the long pole.** The five-part listing is genuine builder
  authoring, not transcription. Mitigation: start it the moment
  Decisions 1 and 3 land; do not let it wait for A/C/G.
- **B-prototype rework.** If Q3's decision differs from the
  recommendation (one fixed function), the prototype may need
  adjustment. Mitigation: the calibration pairs are decision
  independent; only the freezing choice is gated.
- **C160 divergence.** If the reconciled freeze report differs from
  the audit-corrected 4/9, F's predictions need rework. Mitigation:
  F is drafted with the audit figure and flagged; the re-check is an
  explicit pre-freeze gate (Phase 4, item 9).
- **Adversary naming stall.** If Micah defers naming adversaries,
  Section 4 cannot name them. Mitigation: freeze with the naming
  procedure and approval step specified explicitly, not with
  placeholder names.

## 8. What this plan does not cover

- It does not write any preregistration text.
- It does not resolve or recommend on any banked decision.
- It does not implement the signature function (that is B-prototype,
  a separate builder task).
- It does not cover the freeze evaluator reconciliation, bundle v16,
  or the transfer analysis; those are separate tracks with their own
  owners.
