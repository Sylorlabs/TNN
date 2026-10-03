# TNN-3 Preregistration Readiness Checklist

**Status: CHECK ONLY - DRAFT-NOT-FROZEN.** This document assesses readiness;
it does not freeze, amend, or weaken any bar. Micah decides all open items.

Date: 2026-10-01 (UTC). Checker: Prereg Checker subagent.
Verdict: PREREG-CHECK-COMPLETE.

## 1. What a frozen preregistration needs

The authoritative requirements list is the 10-section outline in
`tnn3_prereg_struct/PREREG_STRUCTURE.md` (`206499c03`), section 6.
A frozen TNN-3 preregistration must contain:

1. **Identity and precedence.** Prereg identifier and date; build-freeze
   commit recorded at freeze time; the prereg commit strictly preceding
   implementation (ordering bar, git-ancestry verified); explicit scope
   (which roadmap steps the prereg covers).
2. **Frozen kill bar text.** Exact statements for every in-scope bar,
   each tied to the specific TNN-2 failure mode it targets (with commit
   references to the red-team reports).
3. **Structural signature function.** The deterministic function fixed in
   the prereg, with canonical string specification, calibration test
   results, and a frozen state-dump format.
4. **Adversary protocol.** The K-T3-ADV implementation: designated
   independent adversaries, post-freeze authorship verification
   (fail closed), limited visibility specification, minimum world counts,
   pairwise-distinctness procedure, per-world non-triviality rationale.
5. **Policy revisability listing.** The K-H3 implementation: the five-part
   listing for every structural decision not determined by immediate
   input, plus the H3-lite discrimination tests as committed assets.
6. **Architecture accounting.** Cognition source lines added; new hardcoded
   semantic cases (must be zero); new modes/bridges/handlers (must be
   zero); learner-state structures created; capability-source delta;
   ISA freeze attestation.
7. **Explicit non-claims.** What L2 the design achieves; what L3 it does
   not; which of H1/H2/H3 it addresses and which it does not; honest
   score predictions.
8. **Verification procedures.** 3/3 byte-identical determinism; pure-Zag
   checkers and drivers; safebin Step 0 guard; forbidden executables =
   PROCESS-FAIL; no weakening after results (amendment requires
   transparent re-freeze and full re-run).
9. **Open questions resolved.** Micah's resolutions to Q1-Q6 and the
   signature-function question, with rationale; any amendments to draft
   bar text with rationale.
10. **Governance and audit.** State-retention probe; seal integrity
    verification procedure; contamination checks.

## 2. Ready: what exists in committed drafts

**Bars (ready as drafts).** 24 bars drafted, inventoried (`1722884ad`),
with no exact duplicates and intentional defense-in-depth overlaps
documented. 11 K-T3-* bars (`76231baa8`), K-H3 (`22197da2c`),
K-TSEL-1/2, K-REUSE-1/2, K-H2-1/2/3/4, K-COMP-OP, K-INQ-INFO, K-XMECH,
K-STATE-RET (`36e5a70e1`). Categorization: 21 minimal TNN-3, 2
future-generation (explicit non-claims for minimal TNN-3), 1 audit-grade.
All DRAFT-NOT-FROZEN.

**Achievability reviewed.** The independent review (`eb354e3a2`) found
all 11 K-T3-* bars achievable (genuine L3 passes; clever L2 of the
TNN-2 type deterministically fails) and gave recommendations on all 6
open questions. Redundancy checked: no bars redundant; each covers a
distinct observable.

**Dependencies and order.** Dependencies mapped (`206499c03`, section 2);
priority order P0-P4+PX established (`20d810d4b`); bars mapped to
roadmap phases (`roadmap_update/ROADMAP_WITH_BARS.md`). Critical path:
K-T3-ADV, K-H3, Phase 3 mechanism bars, K-TSEL-1/2. H2 probes and reuse
path off the critical path (parallel, gate roles).

**Supporting specs (draft/proposal).**
- Treadmill guard (`1646b9732`): DRAFT guard spec, 5 checks,
  8 warning signs, per-capability treadmill analysis. Governs TNN-3
  work only if a frozen preregistration references it.
- SUF definition (`64eec921f`): PROPOSAL status. Entrance-gate property;
  governs nothing until incorporated into a frozen preregistration.
- Floor spec (`f383dd11c`): DRAFT preservation spec; 7 capabilities
  (F1-F3 freeze, G1-G3 GW) plus anti-gaming clause. Recommended as a
  regression precondition in the prereg's verification section.

**Failure-mode targets.** Sections 2.8 inputs exist: three red-team
reports (all ATTACK-SUCCESS, `340e94e3e`, `4e329c772`, `687ba0219`),
re-clustering draft (`ed2357141`), GW evaluation (`881fbb3d4`, 2/8),
GW interpretation (`42fa993ab`), boundary map (`8d763d766`), SUF check
(all three mechanisms SUF-FAIL). The prereg author can cite these.

**Process templates.** The TNN-2 cycle established reusable machinery:
prereg commit-order rule, pure-Zag requirement, safebin Step 0 guard,
sealed-evaluator protocol, bundle verification checklist. Sections 1.3
and 8 of the outline can be carried over.

## 3. Missing: what does not exist yet

No frozen preregistration document exists. Nothing below is a criticism
of the drafts; it is the remaining authoring and decision work.

**A. Exact frozen bar text.** Drafts exist for all 24 bars, but Section 2
of a frozen prereg needs the final exact statements with Micah's Q1-Q6
resolutions incorporated (e.g., inquiry world counts 3+ vs 5+ per Q1;
TOPO(b) log format per Q2; any amended wording). Not yet written.

**B. Structural signature function.** Recommendation on record: one
function fixed in the frozen prereg (Q3). The function itself is not
yet written, tested, or calibrated (calibration pairs: chain k=2 vs k=3
must differ; same topology with different literals must not).

**C. Adversary protocol specifics.** K-T3-ADV bar text exists, but
Section 4 needs: named independent adversaries, the limited-visibility
specification, and the minimum world counts with Q1 resolved. Not yet
written.

**D. K-H3 five-part listing.** The bar text exists, but Section 5 needs
the builder's actual listing: every structural decision, learner-state
node/fields, production write path, triggering event, sealed test.
This is builder authoring work that follows the H3-lite design; the
H3-lite discrimination tests exist as design assets.

**E. Architecture accounting baseline.** The Section 6 template exists
in the outline. The actual numbers (source lines, ISA attestation)
are recorded at build-freeze time, after implementation begins.

**F. Explicit non-claims text.** The roadmap's non-overselling guidance
exists; the prereg's Section 7 text is not yet written.

**G. Section 9 (open questions resolved).** Cannot be written until
Micah decides (see blockers below).

## 4. Blockers: decisions only Micah can make

Four banked decisions (`d895c7b44`, morning checklist). Nothing here
is decided; recommendations are on record where noted.

**Blocker 1: Protected-core structural ops (Decision 1).**
Brief `092566072`, PREPARED FOR MICAH - NOT DECIDED. Recommendation on
record: Alternative C (H3-lite only, defer the structural question with
explicit triggers; reject Alternative A, permanent forbid). Micah is
asked to approve: (a) H3-lite may proceed to preregistration as a
separate step; (b) the structural question stays banked with triggers;
(c) Alternative A is rejected. This gates the H3-lite preregistration
path and, behind it, full H3.

**Blocker 2: Six kill-bar open questions (Decision 2).**
Draft `76231baa8`, review `eb354e3a2` with a recommendation on each;
Micah decides:
- Q1. World counts: review recommends raising inquiry to 5+ scenarios;
  keep construction 4+ and revision 3+.
- Q2. K-T3-TOPO(b) builder signature-logging burden: review recommends
  keeping, with the log format fixed in the preregistration.
- Q3. Signature function: review recommends one function fixed in the
  frozen preregistration (not per-world).
- Q4. K-T3-INQ-3 prescriptiveness: review recommends keeping as drafted.
- Q5. Kill bars vs falsifiers: review recommends keeping all as kill
  bars; do not promote.
- Q6. C0-A regression strength: review recommends retaining without
  strengthening.
These gate Section 2 (exact bar text) and Section 9 of the frozen prereg.

**Blocker 3: K-H3 review (Decision 3).**
`tnn2_h3lite/H3LITE_DESIGN.md` (`22197da2c`): the K-H3 bar is
DRAFT-NOT-FROZEN and needs Micah's review separately before any
H3-lite preregistration. No review recommendation on record yet.
This gates Section 5 of the frozen prereg.

**Blocker 4: Full TNN-3 preregistration (Decision 4).**
Pending Decisions 1-3. The roadmap order is fixed: H2 masked probes
(Step 1), then H3-lite (Step 2), then repair/inquiry completion
(Step 3), then H1 widening only after H2 (Step 4); reuse path in
parallel; full H3 banked behind the protected-core decision.

## 5. Readiness verdict

**The TNN-3 preregistration is NOT ready to be frozen.** The drafts are
in unusually good shape: 24 bars inventoried with no duplicates,
achievability reviewed, dependencies and priority order established,
supporting specs drafted, and a 10-section outline ready to receive
them. What is missing is exactly the decision-gated content: Micah's
four banked decisions, then the authoring work in A-G above that those
decisions unlock.

**Sequencing.** The prereg cannot be frozen before:
1. Micah resolves Decisions 1-3 (protected-core path, Q1-Q6, K-H3 review).
2. The prereg author writes Sections 2, 3, 4, 5, 7, 9 incorporating
   those resolutions (A-D, F, G above).
3. The signature function is written and calibrated (B above).
4. A final consistency pass confirms every in-scope bar has exact
   frozen text, a named failure-mode target, and a verification
   procedure.

**Suggested prereg scoping.** The roadmap and priority order support
freezing in stages rather than all at once: an H2-probe preregistration
(Step 1: K-T3-ADV + K-H2-1..4 + K-STATE-RET baseline) can be frozen
first, since the trap worlds are sealed (`86389b108`) and the probes
are runnable against frozen TNN-2. The H3-lite preregistration
(Step 2: K-H3) follows once Blocker 1 approves that path. Staging does
not weaken any bar; each frozen prereg still precedes its
implementation.

**Caveat.** The freeze evaluator reconciliation is still pending (draft
inconsistent; see blocker doc `008e08ab8`). The reconciled freeze
result (C160) is not a prereg blocker: the red-team reports and
failure-cluster analysis the prereg cites are already committed. But
the prereg author should use the reconciled 4/9 figure, not the draft's
5/9, when writing Section 2.8.
