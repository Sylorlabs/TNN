# Reading Guide: Overnight TNN-2 Red-Team and TNN-3 Preparation Cycle

**DRAFT.** Prepared 2026-10-01 for Micah's morning catch-up. This is a
navigation aid only; the documents it points to are the authoritative
sources. Nothing here is a new finding.

**Notation:** document paths are relative to
`docs/lab/research-lead/overnight-20260928/`. Commit hashes are on branch
`tnn-native-lab`, local only, nothing pushed.

**The one-line bottom line (before you read anything):** TNN-2 is fixed
templates with variable content, a real L2 advance over TNN-1, but the
envelope is unchanged in kind. The three targeted changes moved zero
freeze worlds. The adversarial generality battery (GW1-GW8) scored 2/8. Ledger: 159
claims, zero new SURVIVES, L3 zero anywhere.

---

## If you have 10 minutes: read these 3, in this order

### 1. `session_summary/SESSION_SUMMARY.md` (commit `2d213a972`, ~8.5KB)

Why it matters: it is the whole story in five sections, written to be
self-contained. What was accomplished, the critical findings, what is
still pending, and the four items banked for your decision.

What you will learn: all three red teams succeeded (ATTACK-SUCCESS); the
degree-of-freedom map found zero pure learner decisions; the freeze draft
claims 5/9 but its own table documents 4 passes, so the corrected score
is 4/9 and matches TNN-1 exactly; the world-level pattern is byte-identical
to TNN-1 (zero fixes, zero regressions); no freeze score, even 9/9, can
establish C0-D because promoted graphs never execute at query time; the
protected-core brief is ready with Alternative C recommended.

### 2. `gw_eval/GW_EVAL_REPORT.md` (commit `881fbb3d4`, the reconciled result)

Why it matters: this is the generality test that matters. Per your
ruling, FW1-FW9 are a regression battery; the eight sealed adversarial
worlds GW1-GW8, designed post-freeze from the public architecture claim,
are the real test.

What you will learn: **2/8 WORLD-PASS** (GW6, GW7). GW1 (5-hop chains)
failed as predicted: the depth-4 ceiling is architectural. GW2 (cyclic
doubling) failed as predicted: the constructor is DAG-only. GW3
(hierarchical reuse plus revision propagation) failed worse than
predicted: revision did not even work at level 1 when a dependent
structure existed, likely the C0-D shadow mechanism. GW5 (inquiry-gated
construction) failed as predicted: the stale shadow fact answered the
query, so the miss that would trigger inquiry never occurred. GW8
(revision lifecycle) failed: revision is one-shot. The two passes are
bounded positive evidence: inquiry discriminates correctly (GW6, 7/7),
and there is no cross-mechanism interference (GW7, 11/11). All eight
worlds ran 3/3 byte-identical; the TNN-2 binary and shim hashes matched
pre- and post-run.

### 3. `protected_core_decision/PROTECTED_CORE_BRIEF.md` (commit `092566072`, brief only)

Why it matters: it is the one architectural decision that needs you.
The H3 feasibility probe proved the frozen 4-op ISA cannot express
structural workspace mutation (ALLOC, field WRITE, LINK, KILL). Full H3
requires closing that effect-domain gap, which is a protected-core
boundary change and therefore yours.

What you will learn: the exact decision (whether the core may expose
structural graph mutation, and which operations), four alternatives
analyzed (A forbid, B allow a minimal five-op set, C H3-lite only and
defer, D a second graph type rejected), evidence synthesized from the
DOF map, the C0-D analysis, and the ISA ruling, and the recommendation
(NOT a decision): Alternative C, H3-lite only with explicit triggers for
re-examination. It also tells you what you are asked to approve: that
H3-lite may proceed to preregistration (a separate step), that the
structural question stays banked, and that Alternative A is rejected.

---

## If you have 30 minutes: add these 5

### 4. `tnn2_synthesis/REDTEAM_SYNTHESIS.md` (commit `42b4dfa91`)

Why it matters: this is the shared causal account of all three
mechanisms failing. It is the document the other analyses hang off.

What you will learn: the enumerated-schema / filled-slot pattern.
The researcher chooses the form (topology, question, verifier, repair
family); the learner fills runtime-selected indices and literals.
Construction is bounded L2, inquiry is a miss flag with constant
action, revision is L1 parameter filling. Three hypotheses: H1
(enumerated output space), H2 (oracle verification), H3 (procedures
live in source, not learner state). The honest summary line:
"capability improved within the researcher-enumerated envelope; the
envelope is unchanged in kind."

### 5. `tnn2_dof/DEGREE_OF_FREEDOM_MAP.md` (commit `d2af26581`)

Why it matters: this is the source-wide evidence that the learner owns
no criteria. It grounds the roadmap and the protected-core brief.

What you will learn: 0 pure learner decisions, 5 mixed, approximately
240 researcher decisions in the cognition path. Verification is
answer-keyed through `expected` (the largest capability lever, and not
learner-owned). 10 decisions are movable without new opcodes; the top
three quick wins are trial phase order, the combination gate, and
repair target selection. The precise statement: "zero learner-owned
criteria is the disease; zero pure decisions is the symptom."

### 6. `freeze_audit/PREREG_COMPLIANCE_AUDIT.md` (commit `8959a7c14`)

Why it matters: it is why you must not quote 5/9. It also specifies
the six reconciliation steps the evaluator still owes.

What you will learn: the draft report claims 5/9, but its own table
documents exactly four passes (FW1, FW2, FW4, FW5) and five failures,
so the correct score is 4/9. Under the frozen prereg (">4/9 confirms"
vs "at or below 4/9 falsifies and requires re-clustering"), the TNN-2
diagnosis is falsified. The draft's COMPLETE verdict is premature:
K-FZ2-4 determinism is pending, the W1-W9 battery is incomplete,
per-cluster analysis is missing, and post-run hashes are unverified.

### 7. `reclustering/RECLUSTERING_DRAFT.md` (commit `ed2357141`, DRAFT)

Why it matters: this is the prereg-mandated consequence of the
falsified diagnosis. It explains why the three changes moved nothing.

What you will learn: the revised cause clusters (R1 enumerated
construction for FW3/FW8/FW9/half FW7; R2 non-contingent inquiry for
FW6/half FW7; R3 single-schema revision as the ceiling), with the
enumerated-schema / filled-slot meta-cause explaining why none of the
five symptom clusters moved. TNN-3 implications: do not re-attempt
construction as a larger menu; H2 is now the binding constraint on
H1; retain the five symptom clusters as benchmarks but test
learner-originated form.

### 8. `tnn3_roadmap/TNN3_ROADMAP.md` (commit `67a420cca`)

Why it matters: this is the forward plan in one place, with the order
of operations and the three risks named.

What you will learn: minimal TNN-3 (three components, explicitly not
L3); H1/H2/H3 relations and the recommended order (H2 masked
probes first, then H3-lite policy parameterization, then repair
proposal generation plus inquiry resolution, then H1 widening only
after H2, with the reuse path proceeding in parallel and full H3
banked for your governance decision); the three main risks (kill bars
test structure but not useful content, H3-lite becomes revisability
theater, H1 is widened before H2 creating a larger finite menu under
the same oracle).

---

## If you have 1 hour: add these 7

### 9-11. The three red-team reports

- `tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md` (`340e94e3e`)
- `tnn2_redteam_inquiry/INQUIRY_REDTEAM.md` (`4e329c772`)
- `tnn2_redteam_revision/REVISION_REDTEAM.md` (`687ba0219`)

Why they matter: they are the primary evidence. Read the synthesis
first, then these for the mechanism-level detail.

What you will learn: construction has three finite
researcher-written assembler families with fixed bounds, fixed order,
fixed wirings, the sum family dead in production, and oracle `expected`
verification (bounded L2, not L3). Inquiry has learner-originated
miss/uncertainty infrastructure but constant action (CHOICE 30) and
constant content (-999): no discriminating question, no
uncertainty-resolution path (L3 hardcoded, L6 absent). Revision is one
researcher-authored literal-patch topology; the learner selects only
the stale cell and the observed literal; the demonstrated trace is
reducible to L0 storage (L1 parameter filling).

### 12. `tnn2_c0d/C0D_STRUCTURAL_ANALYSIS.md` (commit `8bfb80fdd`)

Why it matters: this is why the reuse question is architectural, not
empirical. It also motivates the reuse-path design.

What you will learn: `promote_graph` shadows itself via
`ev_teach_in` at line 541; `ev_query` answers through `activate`,
which structurally excludes tag-20 MAP nodes. A promoted graph
executes exactly twice in its life (trial verification, revision
re-verification), never to answer a query. The graphs are value
traces with embedded literals, not portable procedures; relation
information exists only as provenance. The standing caveat: no
FW1-FW9 score, even 9/9, can establish C0-D for construction, since
the output is causally inert at query time regardless of score.

### 13. `tnn2_h2probes/H2_PROBE_DESIGN.md` (design only, NOT IMPLEMENTED)

Why it matters: this is Step 1 of the roadmap, and it is ready to
go. The trap-world insight is the key design finding.

What you will learn: three masked-verification probes (withhold
`expected`, lie about `expected`, own acceptance criterion), all
runnable with zero learner source edits (driver-side `mp_run` flags
and world scripts only). The critical insight: the existing masked
branch (lines 501-503) is acceptance without verification (first
candidate with clean execution), not learner-internal verification,
so probe worlds must be search-order traps where the first
executable candidate in the fixed researcher order is wrong. All
three probes are predicted FAIL for TNN-2. Draft kill bars K-H2-1
through K-H2-4 are drafted but DRAFT-NOT-FROZEN; you must freeze
them in a prereg commit before any implementation.

### 14. `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` (commit `76231baa8`, DRAFT-NOT-FROZEN)

Why it matters: these are the frozen-governance instruments for
TNN-3. All eleven are drafted; six questions need you.

What you will learn: kill bars K-T3-ADV, K-T3-TOPO, K-T3-CON-1/2,
K-T3-INQ-1/2/3/4, K-T3-REV-1/2/3. Read with the independent review
(`tnn3_killbar_review/KILLBAR_REVIEW.md`, commit `eb354e3a2`), which
found all eleven achievable and mechanically verifiable, and gives a
recommendation on each of the six open questions: raise inquiry to
at least five scenarios, keep topology logging with the format fixed
in preregistration, use one structural-signature function fixed in
the preregistration, keep INQ-3 as drafted, keep all items as kill
bars not falsifiers, retain C0-A without strengthening.

### 15. `morning_report/MORNING_REPORT_DRAFT.md` (commit `6afd38930`, DRAFT)

Why it matters: it is the consolidated checkpoint the overnight
session assembled for you, with explicit banners (DRAFT, FREEZE
SCORE PENDING, KILL BARS NOT FROZEN). Read it last as a cross-check
against the session summary.

What you will learn: ten sections covering the full red-team cycle
with the corrected 4/9 freeze score, the GW battery status, the
movable priorities, the roadmap order, the open items, the ledger
state (159 claims, zero L3), and a provenance table tying every
claim to its source commit. It notes the battery is GW1-GW8 (eight
worlds), not GW1-GW9.

---

## If you want the full picture: the complete order

After the fifteen above, in this order:

16. `tnn2_altexp/ALTERNATIVE_EXPLANATIONS.md` (`ccee9e5e6`): the
    simplest accounts, "answer-fed, not answer-derived."
17. `tnn2_interaction/INTERACTION_ANALYSIS.md` (`9009ff259`): no
    closed feedback loops, no unsupervised learning loop.
18. `tnn2_mulcompare/MUL_COMPARISON.md` (`e2e34a4ac`): MUL was strong
    L2 not L3; target selection is the underexploited learner-authority
    site.
19. `tnn2_movable/MOVABLE_PRIORITIES.md` (`f70ab617c`): the top three
    quick wins ranked with impact/difficulty.
20. `tnn2_h3probe/H3_FEASIBILITY.md` (`94cecdba4`): the ISA cannot
    express structural revision; the cheap check is confirmed.
21. `tnn2_h3lite/H3LITE_DESIGN.md` (`22197da2c`, design only): the
    three policy nodes, draft K-H3.
22. `tnn2_reusepath/REUSE_PATH_DESIGN.md` (`5f15b9309`, design only):
    MAP-first query, delete the shadow teach, draft K-REUSE-1/2.
23. `tnn2_targetsel/TARGET_SELECTION_DESIGN.md` (`01c2aacfe`, design
    only): the fourth H3-lite site, draft K-TSEL-1/2.
24. `tnn3_prereq/TNN3_PREREQUISITES.md` (`f795807cc`): the eight
    prerequisites before a TNN-3 preregistration.
25. `gap_bars/GAP_BARS.md` (DRAFT-NOT-FROZEN): bars for the five
    prereg-structure gaps (K-H2, K-COMP-OP, K-INQ-INFO, K-XMECH,
    K-STATE-RET).
26. `freeze_interpretation/FREEZE_INTERPRETATION.md` (`a1295cb22`,
    draft): the five standing rules and four scenario templates.
27. `postfreeze_adversary/ADVERSARY_DESIGN.md` (`e409f5eea`): the
    eight sealed worlds and the frozen predictions.
28. `gw_interpretation/GW_INTERPRETATION.md` (if present): the
    interpretation of the 2/8 result.
29. `zero_improvement/ZERO_IMPROVEMENT_ANALYSIS.md` (if present): why
    nothing moved, and what the targeted-repair strategy implies.
30. `final_check/CONSISTENCY_CHECK.md` (if present): the cross-document
    consistency audit.
31. `h2_trapworlds/TRAPWORLD_DESIGN.md` (if present): the sealed trap
    worlds for the H2 probes.
32. `INDEX_TNN2/TNN2_DOCUMENT_INDEX.md`: the full 40+ document
    inventory with hashes, when you need to find anything else.

Supplementary (build and governance provenance, read as needed):

- `tnn2_prereg/TNN2_PREREG.md` (`7c1e30522`): the frozen TNN-2 build prereg.
- `tnn2_build/TNN2_BUILD_REPORT.md` (`f4de7ff46`): BUILD-PASS details.
- `tnn2_repro/REPRO_REPORT.md` (`fdf1fa626`): REPRO-PASS details.
- `core_freeze_tnn2/CORE_FREEZE_TNN2_PREREG.md` (`ce1a7c5f8`): the freeze prereg.
- `core_freeze_tnn2_shim/SHIM_REPORT.md` (`23c2c0206`): zero-cognition shim.
- `freeze_worlds_v2/WORLD_DESIGN.md` (`200387b42`) and `SEAL.md`
  (`396895595`): the sealed FW world design and seal record.
- `seal_integrity/SEAL_INTEGRITY.md` (`0c97a669a`): all 16 files intact.
- `tnn2_governance/GOVERNANCE_AUDIT.md` (`622363372`): nine items PASS.
- `tnn2_compression/COMPRESSION_ANALYSIS.md` (`b2a6ae82c`): the ~103 dead lines.
- `tnn2_frontier/FRONTIER_BACKLOG.md` (`65effc909`): 17 ranked questions.
- `canonical_ledger/CLAIM_LEDGER.md` (C143-C159 in `503a3bedc` and
  `af093bd94`): the ledger entries.
- `bundle_v16_prep/BUNDLE_V16_INVENTORY.md` (`801dc071d`): bundle
  preparation inventory (55 commits since v15).

---

## The four banked decisions, in one place

For reference while reading, these are the items that need you and
only you. None were decided autonomously.

1. **Protected-core structural ops** (`protected_core_decision/`,
   `092566072`). Recommended: Alternative C (H3-lite only, defer the
   structural question, with triggers for re-examination).
2. **Six kill-bar open questions** (`tnn3_killbars/` draft,
   `tnn3_killbar_review/` recommendations). Inquiry scenario count,
   topology logging format, single vs per-world signature function,
   INQ-3 prescriptiveness, kill bars vs falsifiers, C0-A strength.
3. **K-H3 DRAFT-NOT-FROZEN** (`tnn2_h3lite/`). Needs your review
   before any H3-lite preregistration.
4. **Full TNN-3 preregistration** (pending 1-3). Roadmap order is
   fixed: H2 probes, then H3-lite, then repair/inquiry, then H1
   widening only after H2.

---

## What is still running at guide time

These were in progress when this guide was written; check the ledger
and recent commits before relying on them:

- The freeze evaluator (`core_freeze_tnn2_eval/`): the draft is
  internally inconsistent (do not quote it); the six reconciliation
  steps from the audit are the authoritative requirement.
- In-progress worker outputs: `tnn2_transfer/`, `tnn2_boundary/`,
  `tnn2_h2probes/`, `tnn3_prereg_struct/`, `gw_eval/` (now complete,
  `881fbb3d4`), `reading_guide/` (this guide).
- Bundle v16 is NOT created; creation waits on the freeze
  reconciliation (inventory and checklist in `bundle_v16_prep/`).

---

**Verdict: READING-GUIDE-COMPLETE.**
