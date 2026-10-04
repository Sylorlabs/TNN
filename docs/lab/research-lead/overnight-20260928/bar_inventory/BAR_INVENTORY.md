# Kill Bar Master Inventory

**DRAFT-NOT-FROZEN - AWAITING MICAH REVIEW**

This document inventories every kill bar drafted during the overnight TNN-2/TNN-3 cycle. It creates no new bars and modifies none. All bars remain DRAFT-NOT-FROZEN; nothing here governs any build until Micah reviews and freezes them through the normal preregistration process.

Total: **24 bars** across 6 source documents (plus 1 synthesis document that created none).

---

## 1. Master list by source

### 1a. Original TNN-3 kill bars (11) -- `tnn3_killbars/` (`76231baa8`)

| Bar | Short name | One-line description |
|---|---|---|
| K-T3-ADV | Adversarial process | Independence, post-freeze authorship, minimum world counts, fail closed |
| K-T3-TOPO | Learner-chooses-topology audit | Mutual non-isomorphism via signature function; at least one passing sealed shape absent from builder's fixture log |
| K-T3-CON-1 | Sealed construction (derived content) | Two structurally different sealed constructions with derived content |
| K-T3-CON-2 | Construction reuse (C0-D) | Construction output reused later; cognitive reuse evidence |
| K-T3-INQ-1 | Derived discriminating need | Inquiry need derived from experience, not supplied |
| K-T3-INQ-2 | Evidence updates behavior | Inquiry outcome updates later behavior; closes the missing L6 link |
| K-T3-INQ-3 | Ambiguity handled non-arbitrarily | Swap test: non-arbitrary resolution under ambiguity |
| K-T3-INQ-4 | Inquiry reuse and transfer (C0-D) | Inquiry structures reused and transferred |
| K-T3-REV-1 | Sealed repairs (derived content) | Two structurally different sealed repairs with derived content |
| K-T3-REV-2 | Retained-set regression | Unrelated retained knowledge still verifies after revision |
| K-T3-REV-3 | Successive revision including revert | Revise, revise again, revert; not one-shot |

### 1b. H3-lite policy revisability (1) -- `tnn2_h3lite/` (`22197da2c`)

| Bar | Short name | One-line description |
|---|---|---|
| K-H3 | Policy revisability | Every structural decision lists: decision, learner-state node/fields, production write path, triggering experience, sealed history-dependent variation test. Failure conditions (a)-(d): source-literal decision, read-only policy, unreachable write path, researcher-supplied histories. |

### 1c. Target selection (2) -- `tnn2_targetsel/` (`01c2aacfe`)

| Bar | Short name | One-line description |
|---|---|---|
| K-TSEL-1 | Learner-chosen composition targets | Swapped A/B success histories reverse attempt order (history-discrimination test) |
| K-TSEL-2 | No oracle shortcut | Score updates read only learner verification outcomes, never oracle fields |

### 1d. Reuse path (2) -- `tnn2_reusepath/` (`5f15b9309`)

| Bar | Short name | One-line description |
|---|---|---|
| K-REUSE-1 | Query-time MAP execution | White-box trace shows tag-20 MAP read before any fact hit; answer equals MAP executed output |
| K-REUSE-2 | No shadow facts | No `ev_teach_in` from promotion/revision inserts a fact with the same (s, r) as a live MAP |

### 1e. H2 masked verification (4) -- `tnn2_h2probes/` (`4631c5918`)

| Bar | Short name | One-line description |
|---|---|---|
| K-H2-1 | Masked accuracy | Committed answers on sealed trap worlds beat frozen first-executable baseline by margin M; paired unmasked controls pass |
| K-H2-2 | Lie resistance | Explicit uncertainty/refusal on oracle-contradicting trials; zero promotions of fact-contradicting candidates |
| K-H2-3 | Criterion causality and revisability | Learner-state value in accept/reject causal chain; ablation flips decision; criterion changes after prediction errors |
| K-H2-4 | Domain neutrality and reuse | No per-family acceptance branches; at least one masked-trial structure executed by query path later |

### 1f. Gap bars (4) -- `gap_bars/` (`36e5a70e1`)

| Bar | Short name | One-line description |
|---|---|---|
| K-COMP-OP | Learner-originated composition operators | Passing composed graph non-producible by any researcher operator in builder's fixture log |
| K-INQ-INFO | Informativeness-ranked inquiry | On non-dominated uncertainties, learner ranks inquiries by expected informativeness matching independent checker |
| K-XMECH | Graceful cross-mechanism interference | On sealed interference worlds: detection, supersession-or-repair, retained-set integrity; response varies with interference type |
| K-STATE-RET | Structure retention | Rejected candidate structures recoverable from learner state (structural signatures), not just verdict counts |

### Synthesis (0 new) -- `tnn3_prereg_struct/` (`206499c03`)

The preregistration-structure synthesis inventories the 17 bars known at its writing (the 11 K-T3-*, K-H3, K-TSEL-1/2, K-REUSE-1/2), maps dependencies, specifies the roadmap order, identifies 5 gaps, and proposes a 10-section preregistration outline. It creates no bars itself. The 5 gaps were subsequently filled by the K-H2-1..4 (already existing in `4631c5918`) and the 4 gap bars above.

---

## 2. Categorization

### Minimal TNN-3 (21 bars)

These are the bars the minimal TNN-3 (per the roadmap `67a420cca` and the prereg structure `206499c03`) is expected to address:

- All 11 K-T3-* bars
- K-H3 (Step 2: H3-lite)
- K-TSEL-1, K-TSEL-2 (Step 4: H1 widening, after H2)
- K-REUSE-1, K-REUSE-2 (Parallel: reuse path)
- K-H2-1, K-H2-2, K-H2-3, K-H2-4 (Step 1: H2 masked probes; must precede Step 4)
- K-XMECH (rides the same sealed battery)

### Future-generation (2 bars)

Explicitly acknowledged as non-claims for the minimal TNN-3; drafted with teeth for a future generation:

- K-COMP-OP (operator invention: H1 at operator level remains researcher-enumerated in minimal TNN-3)
- K-INQ-INFO (informativeness criterion: post Step 3)

### Audit-grade preferred (1 bar)

The kill-bar review recommended audit-grade placement over bar-grade; both formulations drafted, audit-grade preferred:

- K-STATE-RET (diagnostic infrastructure; complements K-T3-TOPO's signature function)

---

## 3. Count summary

| Category | Count |
|---|---|
| Minimal TNN-3 | 21 |
| Future-generation | 2 |
| Audit-grade preferred | 1 |
| **Total** | **24** |

By source: 11 + 1 + 2 + 2 + 4 + 4 = 24. No double counting.

---

## 4. Duplicates and overlaps

**No exact duplicates found.** The following are near-overlaps or intentional defense-in-depth, documented here so a future preregistration does not accidentally merge distinct bars:

1. **K-H2 (gap bars) vs K-H2-1..4 (H2 probe design).** Not a duplicate. The gap-bars document explicitly synthesizes (not duplicates) the four K-H2 sub-clauses from `4631c5918` into the prereg-structure order. The canonical bar text lives in `tnn2_h2probes/H2_PROBE_DESIGN.md`.

2. **K-COMP-OP vs K-T3-CON-1/2.** Different level. CON-1/2 govern composition of researcher-authored operators over learner-authored operands. K-COMP-OP governs invention of the operators themselves (one level up). The MUL comparator's "larger finite menu" objection survives at operator level even if CON-1/2 pass.

3. **K-INQ-INFO vs K-T3-INQ-3.** Complementary. INQ-3's swap test applies where one guide dominates by design. K-INQ-INFO applies to non-dominated uncertainties where the dominance test does not apply. Together they cover the informativeness space.

4. **K-XMECH vs K-T3-REV-2.** Related but distinct. REV-2 checks retained-set integrity after revision. K-XMECH checks graceful degradation when mechanisms interfere (detection, supersession-or-repair, response varying with interference type).

5. **K-STATE-RET vs K-T3-TOPO.** Complementary. TOPO's signature function is reused by K-STATE-RET to check rejected-structure retention. TOPO governs passing structures; STATE-RET governs rejected ones.

6. **K-REUSE-1 vs K-T3-CON-2.** Different level. CON-2 is construction reuse as C0-D evidence. REUSE-1 is the query-time execution mechanism (MAP read before fact hit) that makes any C0-D claim testable.

7. **K-TSEL-1/2 vs K-T3-TOPO.** Different question. TOPO audits topology diversity of passing structures. TSEL tests learner-authored selection among composable targets via history discrimination.

**Intentional defense-in-depth overlaps** (from the prereg structure synthesis, section 4; not accidents):

- K-T3-TOPO(b) / K-H3(d): anti-gaming (fixture-log absence plus history-dependent variation).
- K-T3-CON-2 / K-REUSE-1: reuse vs composition (output reuse plus execution mechanism).
- K-T3-INQ-2(a) / K-T3-REV-3: supersession lifecycle (evidence updates plus successive revision).

---

## 5. Open questions affecting the bars

The kill-bar review (`eb354e3a2`) left 6 open questions for Micah (with recommendations). These affect bar text and must be resolved before freezing:

1. World counts per bar (recommendation: raise inquiry to 5+ scenarios).
2. Topology logging format (recommendation: keep logging, format fixed in preregistration).
3. Structural-signature function: single vs per-world (recommendation: single function fixed in preregistration).
4. INQ-3 prescriptiveness (recommendation: keep as drafted).
5. Kill bars vs falsifiers (recommendation: keep all as kill bars, not falsifiers).
6. C0-A regression strength (recommendation: retain as drafted, do not strengthen).

Additionally: K-STATE-RET placement (bar-grade vs audit-grade) is Micah's call; the review's audit-grade recommendation is recorded as preferred.

---

## 6. Provenance table

| Bar | Source document | Source commit | Status |
|---|---|---|---|
| K-T3-ADV | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-TOPO | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-CON-1 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-CON-2 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-INQ-1 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-INQ-2 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-INQ-3 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-INQ-4 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-REV-1 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-REV-2 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-T3-REV-3 | `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | DRAFT-NOT-FROZEN |
| K-H3 | `tnn2_h3lite/H3LITE_DESIGN.md` | `22197da2c` | DRAFT-NOT-FROZEN |
| K-TSEL-1 | `tnn2_targetsel/TARGET_SELECTION_DESIGN.md` | `01c2aacfe` | DRAFT-NOT-FROZEN |
| K-TSEL-2 | `tnn2_targetsel/TARGET_SELECTION_DESIGN.md` | `01c2aacfe` | DRAFT-NOT-FROZEN |
| K-REUSE-1 | `tnn2_reusepath/REUSE_PATH_DESIGN.md` | `5f15b9309` | DRAFT-NOT-FROZEN |
| K-REUSE-2 | `tnn2_reusepath/REUSE_PATH_DESIGN.md` | `5f15b9309` | DRAFT-NOT-FROZEN |
| K-H2-1 | `tnn2_h2probes/H2_PROBE_DESIGN.md` | `4631c5918` | DRAFT-NOT-FROZEN |
| K-H2-2 | `tnn2_h2probes/H2_PROBE_DESIGN.md` | `4631c5918` | DRAFT-NOT-FROZEN |
| K-H2-3 | `tnn2_h2probes/H2_PROBE_DESIGN.md` | `4631c5918` | DRAFT-NOT-FROZEN |
| K-H2-4 | `tnn2_h2probes/H2_PROBE_DESIGN.md` | `4631c5918` | DRAFT-NOT-FROZEN |
| K-COMP-OP | `gap_bars/GAP_BARS.md` | `36e5a70e1` | DRAFT-NOT-FROZEN (future-generation) |
| K-INQ-INFO | `gap_bars/GAP_BARS.md` | `36e5a70e1` | DRAFT-NOT-FROZEN (future-generation) |
| K-XMECH | `gap_bars/GAP_BARS.md` | `36e5a70e1` | DRAFT-NOT-FROZEN |
| K-STATE-RET | `gap_bars/GAP_BARS.md` | `36e5a70e1` | DRAFT-NOT-FROZEN (audit-grade preferred) |

All 24 bars are DRAFT-NOT-FROZEN. Nothing here governs any build until Micah reviews the 6 open questions and the bars are frozen through the normal preregistration process.
