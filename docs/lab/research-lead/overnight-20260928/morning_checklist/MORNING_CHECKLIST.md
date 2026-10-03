# Morning Checklist for Micah

**DRAFT.** Prepared 2026-10-01 (UTC) for your morning catch-up. Checklist
only; the linked documents are the authoritative sources. Nothing here is
a new finding or a decision.

**Bottom line up front:** TNN-2 is fixed templates with variable content,
a real L2 advance over TNN-1, but the envelope is unchanged in kind. The
three targeted changes moved zero freeze worlds (corrected score 4/9,
byte-identical to TNN-1). The sealed adversarial battery GW1-GW8 scored
2/8 WORLD-PASS. Ledger: 159 claims, zero new SURVIVES, L3 zero anywhere.

---

## [ ] 1. Read the 10-minute guide

Start here: `reading_guide/READING_GUIDE.md` (commit `46de16972`).

It gives you three documents in order, about 10 minutes total:

1. `session_summary/SESSION_SUMMARY.md` (`2d213a972`, ~8.5KB): the whole
   story in five sections. Accomplishments, critical findings, pending
   items, and the four items banked for your decision.
2. `gw_eval/GW_EVAL_REPORT.md` (`881fbb3d4`): the generality test that
   matters. 2/8 WORLD-PASS (GW6, GW7), per-world results against frozen
   predictions, 3/3 byte-identical runs, binary and shim hashes matched
   pre- and post-run.
3. `protected_core_decision/PROTECTED_CORE_BRIEF.md` (`092566072`): the
   one architectural decision that needs you. Four alternatives analyzed,
   Alternative C recommended (not decided).

If you have 30 minutes, the guide adds five more (red-team synthesis,
degree-of-freedom map, prereg audit, re-clustering draft, TNN-3 roadmap).
If you have an hour, seven more (the three red-team reports, C0-D
analysis, H2 probe design, kill-bar draft plus review, morning report).

---

## [ ] 2. Review the four banked decisions

None of these were decided autonomously. Each lists what it is, the
recommendation on record, and what you are asked to decide.

### Decision 1: Protected-core structural ops

- **What:** Whether the protected core may expose structural graph mutation
  (ALLOC, field WRITE, LINK, KILL, structural READ) to learner-built
  executable graphs. The H3 probe proved the frozen 4-op ISA cannot express
  structural revision; full H3 requires closing that effect-domain gap.
- **Where:** `protected_core_decision/PROTECTED_CORE_BRIEF.md` (`092566072`).
- **Recommendation on record:** Alternative C: H3-lite only, defer the
  structural question, with explicit triggers for re-examination (H3-lite
  evaluated and showing a "criteria without procedures" ceiling, or a
  sealed world requiring procedure topology H3-lite cannot express).
- **You are asked to approve:** (a) H3-lite may proceed to preregistration
  as a separate step; (b) the structural question stays banked with
  triggers; (c) Alternative A (permanent forbid) is rejected.

### Decision 2: Six kill-bar open questions

- **What:** Open questions on the TNN-3 kill-bar draft (`76231baa8`).
  The independent review (`eb354e3a2`) found all eleven bars achievable
  and gives a recommendation on each; you decide.
- **Where:** `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` and
  `tnn3_killbar_review/KILLBAR_REVIEW.md`.
- **The six, with the review recommendation on each:**
  1. World counts: review recommends raising inquiry to at least five scenarios.
  2. K-T3-TOPO(b) builder signature-logging burden: review recommends keeping,
     with the log format fixed in preregistration.
  3. Structural-signature function per-world vs fixed: review recommends one
     function fixed in the frozen preregistration.
  4. Whether K-T3-INQ-3 is too prescriptive: review says keep as drafted.
  5. Kill bars vs falsifiers: review says keep all as kill bars.
  6. C0-A regression bar strength: review says retain without strengthening.
- **Note:** all bars remain DRAFT-NOT-FROZEN until you review. The prereg
  structure synthesis (`tnn3_prereg_struct/PREREG_STRUCTURE.md`, `206499c03`)
  inventories 17 bars with dependencies, and the gap-bars draft
  (`gap_bars/GAP_BARS.md`, `36e5a70e1`) adds five more (K-H2, K-COMP-OP,
  K-INQ-INFO, K-XMECH, K-STATE-RET). Total on record: 24 bars, none frozen.

### Decision 3: K-H3 review

- **What:** The H3-lite kill bar is DRAFT-NOT-FROZEN and needs your review
  separately before any H3-lite preregistration.
- **Where:** `tnn2_h3lite/H3LITE_DESIGN.md` (`22197da2c`).
- **Recommendation on record:** none yet; the bar is drafted, not reviewed.

### Decision 4: Full TNN-3 preregistration

- **What:** Pending decisions 1-3. The roadmap order is fixed and you have
  already ruled on the key constraint: H1 widening before H2 is the
  treadmill you forbade.
- **Where:** `tnn3_roadmap/TNN3_ROADMAP.md` (`67a420cca`).
- **Order on record:** H2 masked probes (Step 1), then H3-lite (Step 2),
  then repair/inquiry completion (Step 3), then H1 widening only after H2
  (Step 4). Reuse path proceeds in parallel. Full H3 banked behind your
  protected-core decision.

---

## [ ] 3. Check what is still running

Status as of this checklist. Committed results are on `tnn-native-lab`
(local only, nothing pushed).

**Complete and committed (no action needed):**
- GW1-GW8 evaluation: `881fbb3d4`, GW-EVAL-COMPLETE, 2/8 WORLD-PASS.
- All red teams, analyses, designs, roadmaps, briefs, and inventories
  listed in `INDEX_TNN2/TNN2_DOCUMENT_INDEX.md` (40+ documents).

**Still running or uncommitted (check before relying on them):**
- `core_freeze_tnn2_eval/`: the freeze evaluator. Its draft is internally
  inconsistent (claims 5/9, table documents 4 passes). Do not quote any
  score from it. The six reconciliation steps in the prereg compliance
  audit (`8959a7c14`) are the authoritative requirement: correct 4/9,
  resolve K-FZ2-4 determinism, complete W1-W9, complete per-cluster
  analysis, verify post-run hashes, then commit.
- `tnn2_transfer/`: developmental transfer/reuse probe worker.
- `tnn2_boundary/`: capability-boundary mapping worker.
- `h2_trapworlds/`: H2 trap-world builder (design and seal files written;
  verify commit landed).

**Gated on the above:**
- Ledger C160 (the reconciled freeze result) is not recorded. It should
  be recorded only after the reconciled evaluator report lands.
- Bundle v16 is NOT created. The inventory and 13-item verification
  checklist are ready (`bundle_v16_prep/BUNDLE_V16_INVENTORY.md`,
  `801dc071d`). Creation waits on freeze reconciliation.

---

## [ ] 4. Suggested first actions (in order)

These are suggestions, not decisions. Each is reversible and independent.

1. **Read the 10-minute guide** (section 1 above). It is the fastest path
   to the full picture.
2. **Skim the four banked decisions** (section 2 above) and note which
   ones you want to take up first. Decision 1 (protected-core) gates the
   H3-lite preregistration path; Decision 2 (kill bars) gates the full
   TNN-3 preregistration.
3. **Confirm the freeze evaluator's status.** If its reconciled report
   has landed, verify the 4/9 correction and the six reconciliation steps
   before the score is quoted or ledgered as C160.
4. **Confirm the three uncommitted worker dirs** (`tnn2_transfer`,
   `tnn2_boundary`, `h2_trapworlds`) have landed cleanly, or re-dispatch
   them if they died.
5. **When freeze reconciliation and all worker dirs are committed,**
   authorize bundle v16 creation per the checklist in `bundle_v16_prep/`.

---

## Quick reference: key commits

| Commit | What |
|---|---|
| `2d213a972` | Session summary (start here) |
| `46de16972` | Reading guide (10-min / 30-min / 1-hour orders) |
| `881fbb3d4` | GW eval: 2/8 WORLD-PASS |
| `092566072` | Protected-core brief (Decision 1) |
| `8959a7c14` | Prereg audit: draft 5/9 wrong, correct 4/9 |
| `ed2357141` | Re-clustering draft: diagnosis falsified |
| `42b4dfa91` | Red-team synthesis: enumerated-schema / filled-slot |
| `d2af26581` | Degree-of-freedom map: 0 pure learner decisions |
| `8bfb80fdd` | C0-D analysis: no score can establish reuse |
| `67a420cca` | TNN-3 roadmap |
| `76231baa8` | Kill-bar draft (Decision 2); review `eb354e3a2` |
| `4631c5918` | H2 probe design (Step 1 of roadmap) |
| `206499c03` | Prereg structure: 17 bars, dependencies, gaps |
| `36e5a70e1` | Gap bars: K-H2, K-COMP-OP, K-INQ-INFO, K-XMECH, K-STATE-RET |
| `801dc071d` | Bundle v16 prep (inventory only, not created) |

Branch: `tnn-native-lab`. All commits local. Nothing pushed.

**Verdict: MORNING-CHECKLIST-COMPLETE.**
