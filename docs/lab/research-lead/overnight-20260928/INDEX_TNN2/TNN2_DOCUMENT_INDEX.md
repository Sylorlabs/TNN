# TNN-2 Overnight Research: Document Index

Index of all TNN-2 documents produced during the overnight cycle of
2026-09-30/2026-10-01 (PDT), under
`docs/lab/research-lead/overnight-20260928/`. Commit hashes verified via
`git log` on branch `tnn-native-lab`. Entries marked UNTRACKED are
in-progress worker output not yet committed; entries marked DRAFT are
committed but explicitly not frozen.

Ledger state at index time: 159 claims (C143-C159 recorded in commits
`503a3bedc` and `af093bd94`), zero new SURVIVES, L3 achieved anywhere: zero.

## 1. Build

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `tnn2_prereg/` | TNN2_PREREG.md | `7c1e30522` | Frozen preregistration for the TNN-2 build: three targeted repairs (construction, inquiry, revision) with kill bars K-T2-1..K-T2-5 | TNN2-PREREG-FROZEN |
| `tnn2_build/` | TNN2_BUILD_REPORT.md | `f4de7ff46` | Build report: 1591 lines Zag, 46/46 assertions, three byte-identical runs; no new opcodes, modes, bridges, or handlers | TNN2-BUILD-PASS |
| `tnn2_build/` | tnn2.zag / tnn2_bin | `f4de7ff46` | Frozen source and binary. Source SHA-256 `a29972ca...`; binary SHA-256 `6044f91f...` | (frozen asset) |
| `tnn2_repro/` | REPRO_REPORT.md | `fdf1fa626` | Independent reproduction of the frozen build: six transcripts, byte-identical SHA-256 `37c7b552...` | TNN2-REPRO-PASS |

## 2. Freeze

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `core_freeze_tnn2/` | CORE_FREEZE_TNN2_PREREG.md | `ce1a7c5f8` | Frozen preregistration for the CORE-FREEZE-TNN2 evaluation: FW1-FW9 primary battery, W1-W9 supplementary, three deterministic runs per world, kill bars K-FZ2-1..K-FZ2-5 | CORE-FREEZE-TNN2-PREREG-FROZEN |
| `core_freeze_tnn2_shim/` | SHIM_REPORT.md | `23c2c0206` | Zero-cognition shim build report; shim source SHA-256 `33795c19...`, binary SHA-256 `9217054c...` | SHIM-BUILD-PASS |
| `freeze_worlds_v2/` | WORLD_DESIGN.md | `200387b42` | Design of the sealed FW1-FW9 evaluation worlds | (design asset) |
| `freeze_worlds_v2/` | SEAL.md | `396895595` | Seal record for the 16 frozen world files; seal commit strictly precedes the freeze prereg | (seal asset) |
| `core_freeze_tnn2_eval/` | FREEZE_REPORT.md | UNTRACKED | Evaluator's draft report: internally inconsistent (claims 5/9, table shows 4 PASS; verdict COMPLETE while K-FZ2-4 PENDING). Do not quote. | DRAFT-INCONSISTENT |
| `seal_integrity/` | SEAL_INTEGRITY.md | `0c97a669a` | Integrity check of the sealed FW worlds without inspecting contents: all 16 files present, hashes match, git clean, no contamination | SEAL-INTEGRITY-CHECK-COMPLETE |
| `freeze_audit/` | PREREG_COMPLIANCE_AUDIT.md | `8959a7c14` | Audit of the evaluator's draft against the frozen prereg: the 5/9 claim is an arithmetic error (correct: 4/9); premature COMPLETE verdict; FW6 correctly FAIL; six reconciliation steps specified | PREREG-COMPLIANCE-AUDIT-COMPLETE |
| `freeze_interpretation/` | FREEZE_INTERPRETATION.md | `a1295cb22` | Honest interpretation templates for every possible freeze outcome (4/9, 5-8/9, 9/9, W divergence): five standing rules, four scenario templates, C0-D caveat | FREEZE-INTERPRETATION-DRAFT-COMPLETE (draft) |
| `reclustering/` | RECLUSTERING_DRAFT.md | `ed2357141` | Draft re-clustering analysis required by the prereg when the score is at or below 4/9 (the diagnosis is falsified) | RECLUSTERING-DRAFT-COMPLETE (draft) |

Key finding from the audit: the correct freeze score is **4/9**, matching TNN-1's
4/9. Under the prereg (">4/9 confirms the diagnosis" vs "at or below 4/9
falsifies and requires re-clustering"), the TNN-2 diagnosis is falsified.

## 3. Red Teams

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `tnn2_redteam_construction/` | CONSTRUCTION_REDTEAM.md | `340e94e3e` | Independent attack on runtime executable-graph construction: 3 finite researcher-written assembler families, fixed bounds and order, sum family dead in production, oracle `expected` verification, no DEC emission | CONSTRUCTION-ATTACK-SUCCESS (bounded L2, not L3) |
| `tnn2_redteam_inquiry/` | INQUIRY_REDTEAM.md | `4e329c772` | Independent attack on inquiry: learner-originated miss/uncertainty infrastructure exists, but constant action 30 and constant content -999; no discriminating question, no uncertainty-resolution path | INQUIRY-ATTACK-SUCCESS (L3 hardcoded, L6 absent) |
| `tnn2_redteam_revision/` | REVISION_REDTEAM.md | `687ba0219` | Independent attack on revision: one researcher-authored literal-patch topology; learner selects only the stale cell and the observed literal; reducible to L0 storage | REVISION-ATTACK-SUCCESS (L1 parameter filling) |
| `tnn2_synthesis/` | REDTEAM_SYNTHESIS.md | `42b4dfa91` | Synthesis of all three attacks: shared "enumerated-schema / filled-slot" pattern (researcher chooses form, learner fills indices and literals); three hypotheses H1 (enumerated output space), H2 (oracle verification), H3 (procedures live in source) | REDTEAM-SYNTHESIS-COMPLETE |

Shared pattern: "capability improved within the researcher-enumerated
envelope; the envelope is unchanged in kind."

## 4. Analyses

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `tnn2_altexp/` | ALTERNATIVE_EXPLANATIONS.md | `ccee9e5e6` | Simplest accounts for each mechanism: construction as parameterized lookup keyed by an environment-supplied answer; inquiry as a sticky miss alarm with a fixed output wire; revision as overwriting a stored constant; unified account "answer-fed, not answer-derived" | ALTERNATIVE-EXPLANATION-ATTACK-COMPLETE |
| `tnn2_inquiry_generalization/` | INQUIRY_GENERALIZATION.md | `dedfad368` | Learner state records verdicts but not the structures those verdicts were about; trial discards candidates before `miss_inquire`; derived max-split inquiry and type-3 supersession possible within ISA but researcher-authored | INQUIRY-GENERALIZATION-ANALYSIS-COMPLETE |
| `tnn2_revision_generalization/` | REVISION_GENERALIZATION.md | `edbb0e9b5` | t2_trial wiring possible within ISA but needs new machinery; five repairs unexpressible; provenance gaps in sum graphs; "in at least one test" was a process loophole | (analysis complete) |
| `tnn2_interaction/` | INTERACTION_ANALYSIS.md | `9009ff259` | No closed feedback loops; inquiry is a dead-end pipeline; revision cannot change construction's grammar or verifier; sum MAPs unrevisable; promoted graphs never executed at query time; no unsupervised learning loop | INTERACTION-ANALYSIS-COMPLETE |
| `tnn2_dof/` | DEGREE_OF_FREEDOM_MAP.md | `d2af26581` | Full decision-point enumeration over the cognition path: pure LEARNER decisions 0; MIXED 5; RESEARCHER ~240; verification is answer-keyed (largest capability lever, not learner-owned); 10 decisions movable without new opcodes | DEGREE-OF-FREEDOM-MAP-COMPLETE |
| `tnn2_c0d/` | C0D_STRUCTURAL_ANALYSIS.md | `8bfb80fdd` | `promote_graph` shadows itself via `ev_teach_in` at line 541; graphs are value traces, not portable procedures; no FW1-FW9 score, even 9/9, can establish C0-D; minimal wiring sketched | C0D-STRUCTURAL-ANALYSIS-COMPLETE |
| `tnn2_compression/` | COMPRESSION_ANALYSIS.md | `b2a6ae82c` | 1591 lines; ~103 dead in cognition; sum assembler dead; 1591 to 1488 safe, to 1456 unified; 1200 ceiling needs architectural deletion | (analysis complete) |
| `tnn2_governance/` | GOVERNANCE_AUDIT.md | `622363372` | Post-build governance audit: all 9 items PASS (prereg order, kill bars, ISA freeze, pure Zag, safebin, hashes, scope, verdict discipline, contamination) | (audit PASS) |
| `tnn2_frontier/` | FRONTIER_BACKLOG.md | `65effc909` | 17 ranked research questions by information gain; Q1/Q2 already answered by red teams | (backlog complete) |
| `tnn2_mulcompare/` | MUL_COMPARISON.md | `e2e34a4ac` | MUL Rung B was strong L2 not L3 (CALL researcher-authored); TNN-2 imported propose/execute/verify/promote, not composition; inlining is the freeze-compatible composition route; target-selection policy is the underexploited learner-authority site | MUL-COMPARISON-COMPLETE |
| `tnn2_transfer/` | TRANSFER_ANALYSIS.md | UNTRACKED | Developmental transfer/reuse probes (worker still active at index time) | (in progress) |
| `tnn2_boundary/` | probes/ | UNTRACKED | Capability-boundary mapping probes (worker still active at index time) | (in progress) |

## 5. Designs

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `tnn2_h3probe/` | H3_FEASIBILITY.md | `94cecdba4` | The frozen 4-op ISA cannot express structural workspace mutation (ALLOC, field WRITE, LINK, KILL); no production write path to construction order, guide schema, or repair topology; full H3 raises a protected-core boundary decision banked for Micah | H3-FEASIBILITY-PROBE-COMPLETE |
| `tnn2_h3lite/` | H3LITE_DESIGN.md | `22197da2c` | Three learner-state policy nodes (trial search order, revisable guide template, repair dispatcher) requiring no ISA change; draft K-H3 bar; changes locus of control, not scores; explicitly NOT IMPLEMENTED | H3LITE-DESIGN-COMPLETE (design only) |
| `tnn2_targetsel/` | TARGET_SELECTION_DESIGN.md | `01c2aacfe` | Fourth H3-lite site: per-MAP score scalars updated by a fixed-form rule; the two needed signals (reuse history, composition outcomes) do not exist; target selection is downstream of the reuse path; draft K-TSEL-1/2; explicitly NOT IMPLEMENTED | TARGET-SELECTION-DESIGN-COMPLETE (design only) |
| `tnn2_reusepath/` | REUSE_PATH_DESIGN.md | `5f15b9309` | Minimal reuse path: MAP-first query branch, delete the shadow teach at 541, retarget contradiction at the MAP; makes C0-D testable (not true); honest prediction is scores unchanged; draft K-REUSE-1/2; explicitly NOT IMPLEMENTED | REUSE-PATH-DESIGN-COMPLETE (design only) |
| `tnn2_movable/` | MOVABLE_PRIORITIES.md | `f70ab617c` | All 10 movable decisions ranked by impact/difficulty: top 3 quick wins are trial phase order, comb gate, repair target selection; "zero learner-owned criteria is the disease; zero pure decisions is the symptom" | MOVABLE-PRIORITIES-COMPLETE |
| `tnn2_h2probes/` | (empty) | UNTRACKED | H2 masked verification probe designs, Step 1 of the TNN-3 roadmap (worker still active at index time) | (in progress) |

## 6. Roadmaps

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `tnn3_prereq/` | TNN3_PREREQUISITES.md | `f795807cc` | Eight prerequisites before a TNN-3 preregistration; largest unresolved item is the completed sealed post-freeze GW evaluation; also requires reconciled freeze, current ledger, H3 analysis, governance closure | TNN3-PREREQUISITES-MAPPED |
| `tnn3_roadmap/` | TNN3_ROADMAP.md | `67a420cca` | Minimal TNN-3 (three components, explicitly not L3); H1/H2/H3 relations; three biggest risks (prereg spec gap redux, revisability theater, solving H1 before H2); recommended order: H2 probes, H3-lite, repair/inquiry, H1 only after H2, reuse path in parallel | TNN3-ROADMAP-SYNTHESIS-COMPLETE |
| `tnn3_killbars/` | TNN3_KILLBARS_DRAFT.md | `76231baa8` | Draft kill bars K-T3-ADV, K-T3-TOPO, K-T3-CON-1/2, K-T3-INQ-1/2/3/4, K-T3-REV-1/2/3; six open questions banked for Micah | TNN3-KILLBARS-DRAFT-COMPLETE (DRAFT-NOT-FROZEN) |
| `tnn3_killbar_review/` | KILLBAR_REVIEW.md | `eb354e3a2` | Independent review: draft is well-constructed, all 11 bars achievable, verification sound, no redundancy; recommendations on all six open questions | KILLBAR-REVIEW-COMPLETE (DRAFT-NOT-FROZEN stands) |
| `tnn3_prereg_struct/` | (empty) | UNTRACKED | Synthesis of all kill-bar drafts into one preregistration structure (worker still active at index time) | (in progress) |
| `protected_core_decision/` | PROTECTED_CORE_BRIEF.md | `092566072` | Decision brief for Micah on structural graph mutation: exact decision, alternatives, evidence, consequences, recommendation; prepared, NOT decided | PROTECTED-CORE-BRIEF-COMPLETE (brief only) |

## 7. Evaluations

| Directory | Document | Commit | Description | Verdict |
|---|---|---|---|---|
| `postfreeze_adversary/` | ADVERSARY_DESIGN.md | `e409f5eea` | Eight sealed adversarial generality worlds GW1-GW8 (5-hop chains, cyclic doubling, hierarchical reuse, guard retarget, inquiry-gated construction, inquiry state battery, interleaved, revision lifecycle); predictions frozen; TNN-2 untouched | ADVERSARY-DESIGN-COMPLETE |
| `postfreeze_adversary/` | SEAL_GW.md | `e409f5eea` | Seal record for GW1-GW8: id range [40000,49999], anti-smuggling scan clean, SHA-256 table | (seal asset) |
| `gw_eval/` | GW_EVAL_REPORT.md | UNTRACKED | Authorized independent evaluation of frozen TNN-2 on GW1-GW8, three runs per world (worker still active at index time) | (in progress) |
| `morning_report/` | MORNING_REPORT_DRAFT.md | `6afd38930` | Assembled morning report: 10 sections covering the full red-team cycle, with corrected 4/9 freeze score, GW status, movable priorities, and roadmap order; explicit banners DRAFT / SCORE PENDING / BARS NOT FROZEN | MORNING-REPORT-UPDATE-COMPLETE (draft) |

Note: the battery is GW1-GW8 (eight worlds), not GW1-GW9.

## 8. Ledger

| Document | Commit | Description |
|---|---|---|
| `canonical_ledger/CLAIM_LEDGER.md` (C143-C149) | `503a3bedc` | TNN-2 prereg, build, repro, freeze prereg, shim, Micah ruling, eval pending |
| `canonical_ledger/CLAIM_LEDGER.md` (C150-C159) | `af093bd94` | Red-team cycle: three ATTACK-SUCCESS verdicts, synthesis, alternative explanations, interaction, DOF-adjacent findings |

No freeze score recorded in the ledger (the evaluator's draft is inconsistent;
reconciliation pending). L3 achieved anywhere: zero.

## In-progress at index time (UNTRACKED, not indexed above)

- `tnn2_transfer/` (developmental transfer/reuse probes)
- `tnn2_boundary/` (capability-boundary mapping)
- `tnn2_h2probes/` (H2 masked verification probe designs)
- `tnn3_prereg_struct/` (preregistration structure synthesis)
- `gw_eval/` (GW1-GW8 evaluation, three runs per world)
- `core_freeze_tnn2_eval/` (freeze evaluator; draft inconsistent, do not quote)

## Reading order (suggested)

1. `tnn2_build/TNN2_BUILD_REPORT.md` (`f4de7ff46`) for what was built.
2. The three red-team reports (`340e94e3e`, `4e329c772`, `687ba0219`), then
   `tnn2_synthesis/REDTEAM_SYNTHESIS.md` (`42b4dfa91`).
3. `tnn2_altexp/ALTERNATIVE_EXPLANATIONS.md` (`ccee9e5e6`) for the simplest
   accounts.
4. `tnn2_dof/DEGREE_OF_FREEDOM_MAP.md` (`d2af26581`) and
   `tnn2_c0d/C0D_STRUCTURAL_ANALYSIS.md` (`8bfb80fdd`) for the structural
   core.
5. `freeze_audit/PREREG_COMPLIANCE_AUDIT.md` (`8959a7c14`) for the freeze
   score correction.
6. `tnn3_roadmap/TNN3_ROADMAP.md` (`67a420cca`) for what comes next.
7. `morning_report/MORNING_REPORT_DRAFT.md` (`6afd38930`) for the consolidated
   summary.
