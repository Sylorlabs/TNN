# Consistency Check: Overnight TNN-2 Red-Team Cycle Deliverables

**Status: CONSISTENCY-CHECK-COMPLETE.** Date: 2026-10-01 (PDT). Worker: Final Checker.
Safebin guard Step 0 PASS (NAMECHECK.md). Check only; no other documents edited.
Paper untouched. This document lists all major verdicts/commits, checks cross-document
consistency, and lists contradictions found.

---

## 1. Major verdicts and commits checked

| Commit | Verdict | Status |
|---|---|---|
| `340e94e3e` | CONSTRUCTION-ATTACK-SUCCESS | Verdict |
| `4e329c772` | INQUIRY-ATTACK-SUCCESS | Verdict |
| `687ba0219` | REVISION-ATTACK-SUCCESS | Verdict |
| `42b4dfa91` | REDTEAM-SYNTHESIS-COMPLETE (shared enumerated-schema/filled-slot cause) | Analysis |
| `8959a7c14` | PREREG-COMPLIANCE-AUDIT-COMPLETE (draft 5/9 claim is arithmetic error; correct 4/9; FW6 FAIL correct; 6 reconciliation steps) | Audit |
| `e409f5eea` | ADVERSARY-DESIGN-COMPLETE (GW1-GW8 sealed, predictions frozen, TNN-2 untouched) | Design |
| `881fbb3d4` | GW-EVAL-COMPLETE, 2/8 WORLD-PASS (GW6, GW7); binary hashes pre/post match frozen values; 3/3 byte-identical runs | Evaluation |
| `42fa993ab` | GW interpretation DRAFT (2/8 consistent with R1/R2/R3 + C0-D; no new cause needed) | Draft |
| `af093bd94` | LEDGER-REDTEAM-CYCLE-COMPLETE (149 to 159 claims; zero new SURVIVES; L3 still zero; freeze score NOT recorded) | Ledger |
| `ed2357141` | RECLUSTERING-DRAFT-COMPLETE (4/9 falsifies prereg diagnosis; R1/R2/R3 cause clusters; meta-cause enumerated-schema/filled-slot) | Draft |
| `76231baa8` | TNN3-KILLBARS-DRAFT-COMPLETE (11 bars; DRAFT-NOT-FROZEN; 6 open questions banked) | Draft |
| `eb354e3a2` | KILLBAR-REVIEW-COMPLETE (all 11 bars achievable; DRAFT-NOT-FROZEN stands) | Review |
| `206499c03` | TNN-3 prereg structure draft: 17-bar synthesis with dependencies, order, gaps | Draft |
| `36e5a70e1` | Gap bars draft: K-H2 (oracle), K-COMP-OP, K-INQ-INFO, K-XMECH, K-STATE-RET (DRAFT-NOT-FROZEN) | Draft |
| `4631c5918` | H2-PROBE-DESIGN-COMPLETE (3 masked probes; draft K-H2-1..K-H2-4 NOT FROZEN) | Design |
| `22197da2c` | H3LITE-DESIGN-COMPLETE (3 policy nodes; K-H3 DRAFT-NOT-FROZEN) | Design |
| `5f15b9309` | REUSE-PATH-DESIGN-COMPLETE (K-REUSE-1/2 drafted, DRAFT-NOT-FROZEN) | Design |
| `01c2aacfe` | TARGET-SELECTION-DESIGN-COMPLETE (K-TSEL-1/2 drafted, DRAFT-NOT-FROZEN) | Design |
| `092566072` | Protected-core decision brief: PREPARED FOR MICAH, NOT DECIDED | Draft |
| `67a420cca` | TNN3-ROADMAP-SYNTHESIS-COMPLETE (H2 probes, then H3-lite, then H1 widening) | Synthesis |
| `a1295cb22` | FREEZE-INTERPRETATION-DRAFT-COMPLETE (scenario templates, no score predicted) | Draft |
| `6afd38930` | Morning report update: 4/9 correction, GW evaluator, movable priorities, roadmap order (DRAFT, score pending) | Draft |
| `2d213a972` | SESSION-SUMMARY-DRAFT-COMPLETE (freeze score NOT quoted; banked items listed) | Draft |
| `801dc071d` | BUNDLE-V16-PREP-COMPLETE (inventory only; no bundle created; paper untouched) | Prep |
| `0c97a669a` | SEAL-INTEGRITY-CHECK-COMPLETE (16/16 FW hashes match; no contamination) | Verification |
| `622363372` | GOVERNANCE-AUDIT-PASS (step 11; eval-in-progress caveat recorded) | Audit |
| `d2af26581` | DEGREE-OF-FREEDOM-MAP-COMPLETE (0 pure learner / 5 mixed / ~240 researcher decisions) | Analysis |
| `f70ab617c` | MOVABLE-PRIORITIES-COMPLETE (top 3: trial phase order, comb gate, repair target selection) | Analysis |
| `8bfb80fdd` | C0D-STRUCTURAL-ANALYSIS-COMPLETE (shadowed MAPs; graphs are value traces) | Analysis |
| `94cecdba4` | H3-FEASIBILITY-PROBE-COMPLETE (4-op ISA cannot express structural revision) | Analysis |
| `e2e34a4ac` | MUL-COMPARISON-COMPLETE (MUL Rung B strong L2; composition operator dropped at TNN-2 prereg) | Analysis |

Still pending (not contradictions, known state):
- Freeze evaluator's reconciled report (draft UNTRACKED in `core_freeze_tnn2_eval/`, internally inconsistent: claims 5/9, table shows 4 PASS, verdict COMPLETE while K-FZ2-4 PENDING). Reconciliation per `8959a7c14` not yet done.
- Bundle v16 creation (inventory done, no bundle built).
- H2 trap worlds built and sealed (not yet run; awaiting K-H2 freeze by Micah).

---

## 2. Consistency checks

### Freeze score (4/9): CONSISTENT
All 5/9 mentions in committed documents refer to the evaluator draft's arithmetic
error and state the audit correction to 4/9 (`freeze_audit`, `reclustering`,
`session_summary`, `morning_report`, `bundle_v16_prep`, `INDEX_TNN2`,
`tnn3_prereq` section 3, `canonical_ledger`, `zero_improvement`, `gw_interpretation`).
No committed document asserts 5/9 as the true score. The ledger explicitly did NOT
record a freeze score (C150-C159 appendix: "freeze score NOT recorded: evaluator
draft inconsistent, awaiting reconciled commit"). Morning report carries the
banners DRAFT / FREEZE SCORE PENDING / DO NOT QUOTE.

### Red-team verdicts: CONSISTENT
All three are ATTACK-SUCCESS: construction `340e94e3e`, inquiry `4e329c772`,
revision `687ba0219`. Synthesis `42b4dfa91`, alternative-explanation attack
`ccee9e5e6`, ledger C150-C159, morning report, and session summary all record
the same three verdicts with the same commit hashes.

### GW count (GW1-GW8): ONE REAL CONTRADICTION FOUND
The adversary design `e409f5eea`, seal record, GW eval `881fbb3d4`, GW
interpretation, session summary, morning report, INDEX_TNN2, and re-clustering
all state GW1-GW8 (eight worlds). Two files say GW1-GW9:
- `tnn2_h3lite/H3LITE_DESIGN.md:498`: "post-freeze adversary (GW1-GW9)"
- `freeze_interpretation/FREEZE_INTERPRETATION.md:19,103`: "(GW1-GW9)"
These are wrong; the battery is eight worlds. (INDEX_TNN2 line 100 already notes
"the battery is GW1-GW8 (eight worlds), not GW1-GW9".)

### Kill-bar counts: CONSISTENT
- 11 bars: TNN-3 kill-bar draft `76231baa8`, reviewed `eb354e3a2`.
- 17 bars: prereg structure `206499c03` inventories 2 cross-cutting + 2 construction
  + 4 inquiry + 3 revision (the 11 from `76231baa8`) + 1 H3-lite + 2 target-selection
  + 2 reuse-path + 1 implied structural signature function = 17. Superset, not a
  competing count. `morning_report` and `session_summary` use 11 for the draft and
  `gap_bars` references the 17 as the prereg-structure total; all consistent.
- 5 gap bars: `36e5a70e1` (K-H2, K-COMP-OP, K-INQ-INFO, K-XMECH, K-STATE-RET),
  DRAFT-NOT-FROZEN, drafted against the five gaps in `206499c03`; not counted in
  either the 11 or the 17.

### Ledger count (159): CONSISTENT
`af093bd94` appended C150-C159 (149 to 159). Session summary, morning report,
INDEX_TNN2, bundle inventory, and `freeze_interpretation/NAMECHECK.md` all state
159 claims. No C160 exists. Zero new SURVIVES and L3 = zero stated consistently
in the ledger, morning report, and session summary.

### DRAFT markers: CONSISTENT
- Freeze evaluator draft: UNTRACKED, DRAFT-INCONSISTENT (INDEX_TNN2 line 30), "Do not quote".
- TNN-3 kill bars: DRAFT-NOT-FROZEN (draft doc, NAMECHECK, review, morning report, session summary).
- K-H2-1..K-H2-4, K-H3, K-TSEL-1/2, K-REUSE-1/2: all DRAFT-NOT-FROZEN in their design docs.
- Protected-core brief: PREPARED FOR MICAH, NOT DECIDED.
- Re-clustering, GW interpretation, morning report, session summary: all marked DRAFT.
- No document weakens a frozen kill bar; no frozen bar is asserted against unapproved thresholds.

### GW evaluation integrity: CONSISTENT
`881fbb3d4` verifies the TNN-2 binary SHA-256 (`6044f91f...`) and shim SHA-256
(`9217054c...`) match the frozen values pre- and post-run, 3/3 byte-identical
runs, eight worlds, sealed assets unmodified, safebin only. Predictions matched
5/8; the three deviations (GW3 worse, GW4/GW8 uncertain-by-design) are documented
in the report itself and cross-checked against the frozen predictions in
`ADVERSARY_DESIGN.md` (GW6 predicted primary PASSES/retirement FAILS as predicted;
GW7 predicted PASS; GW4/GW8 predicted UNCERTAIN). No overclaim: the report states
no GW score would establish L3.

---

## 3. Contradictions and issues found

1. **GW count written as GW1-GW9 in two documents** (the only outright
   contradiction): `tnn2_h3lite/H3LITE_DESIGN.md:498` and
   `freeze_interpretation/FREEZE_INTERPRETATION.md` lines 19 and 103. The battery
   is GW1-GW8 (adversary design, seal, evaluation, interpretation, index all
   agree). These two files need correction by their owners; check-only per
   assignment, so no edit made here.

2. **Stale GW status in the session summary and morning report**: both were
   committed before `881fbb3d4` and describe the GW evaluator as "active" /
   "under evaluation". The evaluation is now complete (2/8 WORLD-PASS). True at
   commit time, stale now. A follow-up morning-report update should record the
   2/8 result and update the INDEX entry for `gw_eval/` (currently "UNTRACKED",
   "worker still active at index time").

3. **Bundle v16 inventory commit count off by four**: `BUNDLE_V16_INVENTORY.md`
   says "55 commits" since v15; `git rev-list --count v15..801dc071d` = 59.
   Minor numerical staleness; the inventory also does not cover the 3 commits
   after it (`881fbb3d4`, `36e5a70e1`, `42fa993ab`).

4. **Stale conditional in `tnn3_prereq/TNN3_PREREQUISITES.md:259`**: "The draft
   5/9 (if confirmed) is a legitimate capability improvement over TNN-1's 4/9"
   was written before the audit disconfirmed the draft's score. The conditional
   ("if confirmed") is now resolvable: the audit found 4/9, so the "if" branch
   is closed. The surrounding synthesis section should be updated to the
   audit-corrected reading when prerequisites are next revised.

5. **INDEX_TNN2 does not cover `gap_bars/`, `zero_improvement/`,
   `h2_trapworlds/`, or `gw_interpretation/`** (committed after the index).
   Expected staleness; index refresh recommended at next index pass.

---

## 4. Nothing pending contradiction elsewhere

- Per-world FW table (FW1, FW2, FW4, FW5 PASS; FW3, FW6, FW7, FW8, FW9 FAIL)
  stated identically in the audit, re-clustering, and zero-improvement analysis.
  FW6 FAIL is confirmed correct (constant CHOICE 30 as degenerate as TNN-1's
  constant CHOICE 0 for the contingent-inquiry requirement).
- Zero-improvement analysis assumes the audit-corrected 4/9 and explicitly says
  it must be revised if the reconciled score differs. Good hygiene.
- The freeze interpretation's Scenario 2 (5/9 through 8/9) is a hypothetical
  template in a document whose stated purpose is "templates for every possible
  freeze outcome", not a score claim. Not a contradiction.
- TNN-1 at 4/9 as the comparison anchor is stated identically in the freeze
  prereg `ce1a7c5f8`, the audit, re-clustering, and GW interpretation.

**Verdict: CONSISTENCY-CHECK-COMPLETE.**
