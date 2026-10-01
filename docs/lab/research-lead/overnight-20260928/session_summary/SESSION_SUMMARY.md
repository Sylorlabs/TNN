# Session Summary: Overnight TNN-2 Red-Team and TNN-3 Preparation Cycle

**Status: DRAFT**

**Date:** 2026-10-01 (UTC)
**Scope:** TNN-2 frozen build `f4de7ff46` through red-team cycle, plus TNN-3
preparation work (designs, roadmaps, decision briefs). Pure Zag throughout.
Safebin toolchain guard on every worker. Nothing pushed.

**Do not quote a freeze score from this document.** The evaluator's reconciled
committed report is the authoritative source.

---

## 1. What was accomplished

**TNN-2 build and freeze (completed earlier):**
- Prereg `7c1e30522`, BUILD-PASS `f4de7ff46` (1591 lines), REPRO-PASS `fdf1fa626`
- Freeze prereg `ce1a7c5f8`, shim BUILD-PASS `23c2c0206`
- Seal integrity verified `0c97a669a` (16/16 hashes match, no contamination)

**Red-team cycle (all committed, ledger C150-C159):**
- Construction red team: ATTACK-SUCCESS `340e94e3e`
- Inquiry red team: ATTACK-SUCCESS `4e329c772`
- Revision red team: ATTACK-SUCCESS `687ba0219`
- Synthesis: shared enumerated-schema/filled-slot cause, H1/H2/H3 `42b4dfa91`
- Alternative explanations: answer-fed not answer-derived `ccee9e5e6`
- Ledger `af093bd94`: 149 to 159 claims, zero new SURVIVES, L3 still zero

**Structural analyses:**
- Degree-of-freedom map `d2af26581`: 0 pure learner decisions, 5 mixed,
  approximately 240 researcher decisions
- C0-D structural failure `8bfb80fdd`: promoted graphs never execute at query
  time; value traces not portable
- Interaction analysis `9009ff259`: no closed feedback loops, no unsupervised
  learning loop
- MUL Rung B comparison `e2e34a4ac`: MUL was strong L2 not L3; TNN-2 dropped
  the composition operator at preregistration
- Compression `b2a6ae82c`: approximately 103 dead-in-cognition lines

**TNN-3 preparation (all DRAFT, none implemented):**
- H3 feasibility probe `94cecdba4`: ISA cannot express structural revision
- H3-lite design `22197da2c`: three policy nodes, K-H3 bar drafted
- Target-selection design `01c2aacfe`: fourth H3-lite site, K-TSEL-1/2 drafted
- Reuse path design `5f15b9309`: MAP-first query, K-REUSE-1/2 drafted
- TNN-3 kill bars `76231baa8`: 11 bars drafted, reviewed `eb354e3a2`
  (all achievable, 6 open questions with recommendations)
- TNN-3 roadmap `67a420cca`: minimal TNN-3, H1/H2/H3 relations,
  order H2 probes then H3-lite then H1 widening
- Movable priorities `f70ab617c`: top 3 quick wins ranked
- H2 masked probe design: 3 probes, draft K-H2-1..4 (most recent commit)

**Post-freeze generality battery:**
- GW1-GW8 adversary `e409f5eea`: 8 sealed worlds, predictions frozen,
  TNN-2 untouched; GW evaluator active

**Interpretation and reporting:**
- Prereg compliance audit `8959a7c14` (see critical findings)
- Re-clustering draft `ed2357141` (see critical findings)
- Freeze interpretation draft `a1295cb22`: 5 rules, 4 scenarios
- Morning report `0882dffb8` updated `6afd38930`: 10 sections
- Protected-core decision brief `092566072` (see banked items)

---

## 2. Critical findings

**All three red teams succeeded.** Construction is bounded L2 (three fixed
assemblers, researcher-fixed wirings/bounds/order, sum family dead in
production, oracle verifier). Inquiry is a miss flag with constant action
(CHOICE 30, content -999, no discriminating question, no uncertainty
resolution). Revision is one researcher-authored literal-patch topology
(L1 parameter filling). Shared cause: enumerated-schema / filled-slot.
The researcher chooses the form; the learner fills indices and literals.

**Zero pure learner decisions.** The degree-of-freedom map found 0 learner,
5 mixed, approximately 240 researcher decisions in the cognition path.
The precise statement from the movable-priorities analysis: zero
learner-owned criteria is the disease; zero pure decisions is the symptom.
Every mixed point uses a researcher-fixed criterion over learner-supplied
data.

**The freeze draft is wrong; the corrected score falsifies the diagnosis.**
The prereg compliance audit found the evaluator's draft claims 5/9 but its
own table documents 4 passes (FW1, FW2, FW4, FW5) and 5 failures. Correct
score: 4/9, matching TNN-1 exactly. The re-clustering draft shows the
world-level pattern is byte-identical: zero fixes, zero regressions.
Under the frozen prereg (">4/9 confirms" vs "at or below 4/9 falsifies"),
the diagnosis "TNN-1 fails for lack of X; TNN-2 adds X" is falsified for
all three changes. Revised cause clusters: R1 enumerated construction,
R2 non-contingent inquiry, R3 single-schema revision, with the
enumerated-schema/filled-slot meta-cause explaining why none moved.

**No freeze score can establish C0-D.** Promoted graphs shadow themselves:
`promote_graph` inserts a memoized fact at line 541, and `ev_query` answers
via `activate`, which structurally excludes tag-20 MAP nodes. A promoted
graph executes exactly twice in its life (trial verification, revision
re-verification), never to answer a query. The graphs are value traces,
not portable procedures. Quote: "No FW1-FW9 score, even 9/9, can establish
C0-D for construction, since the output is causally inert at query time
regardless of score."

**GW1-GW8 are the generality test.** Eight sealed adversarial worlds designed
post-freeze from the public architecture claim. Predictions frozen.
The evaluator is active. Per Micah's ruling, FW1-FW9 are a regression
battery; the GW battery is the important generality test.

**Protected-core brief is ready.** The H3 probe proved the frozen 4-op ISA
cannot express structural workspace mutation (ALLOC, field WRITE, LINK,
KILL). Full H3 requires closing this effect-domain gap, which is a
protected-core boundary decision. The brief analyzes four alternatives
and recommends Alternative C: H3-lite only, defer the structural question,
with explicit triggers for re-examination.

---

## 3. Still pending

- **Freeze report reconciliation.** The evaluator must correct 5/9 to 4/9,
  resolve K-FZ2-4 (determinism) before claiming COMPLETE, complete the W1-W9
  battery, complete per-cluster analysis, and verify post-eval hashes.
  Six reconciliation steps are specified in `8959a7c14`. Do not quote any
  score until the reconciled committed report lands.
- **GW1-GW8 evaluation.** The evaluator is active (three runs per world,
  authorized, no TNN-2 modifications). Predictions are frozen in
  ADVERSARY_DESIGN.md.
- **Bundle v16.** Inventory is being prepared. The bundle should wait until
  the freeze reconciles and the GW evaluation completes.

---

## 4. Banked for Micah

These need his decision. None were decided autonomously.

1. **Protected-core structural ops decision.** Brief `092566072` prepared.
   Recommended: Alternative C (H3-lite only, defer), with triggers for
   re-examination. Asked to approve: H3-lite may proceed to preregistration
   (separate); the structural question stays banked; Alternative A
   (permanent forbid) is rejected.

2. **Six kill-bar open questions** (draft `76231baa8`, review `eb354e3a2`
   gives a recommendation on each, Micah decides): (1) world counts,
   review recommends inquiry 5+ scenarios; (2) K-T3-TOPO(b) builder
   signature-logging burden, review recommends keeping with specified
   log format; (3) structural-signature function per-world vs fixed,
   review recommends one function fixed in the frozen prereg;
   (4) whether K-T3-INQ-3 is too prescriptive, review says keep as
   drafted; (5) kill bars vs falsifiers, review says keep all as kill
   bars; (6) C0-A regression bar strength, review says retain without
   strengthening.

3. **K-H3 DRAFT-NOT-FROZEN.** The H3-lite kill bar needs his review
   separately.

4. **Full TNN-3 preregistration.** Pending the above decisions. The roadmap
   order is: H2 masked probes (Step 1), then H3-lite (Step 2), then
   repair/inquiry completion (Step 3), then H1 widening only after H2
   (Step 4). Solving H1 before H2 is the treadmill he forbade.

---

## 5. Bottom line

TNN-2 is fixed templates with variable content: a real L2 advance over
TNN-1's fixed templates with fixed content, but the envelope is unchanged
in kind. The three targeted changes did not move a single world. The
frozen evaluation, whatever its reconciled score, measures capability
within the researcher-enumerated envelope. The GW battery is the test
that matters. The path forward runs through H2 (learner-internal
verification) first, then H3-lite (revisable policies), with the
protected-core structural question banked behind explicit triggers.

**Ledger:** 159 claims. Zero new SURVIVES. L3 achieved anywhere: zero.
