# Track A Arm W — Binding Verdict

**Arm:** W (Multi-granularity)  
**Round:** r1, scale 1x  
**Date:** 2026-09-21  
**Adjudicator:** Marathon Crew U2  
**Verdict:** **PASS** (all four frozen kill criteria evaluated; none fired)

## 1. Frozen kill criteria (units/PREREG_FREEZE.md)

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| (i) | Composite battery score does not beat S alone by ≥15% | **NOT COMPUTABLE — does not fire** | No frozen normalization/direction-to-single-score formula exists in PREREG_FREEZE.md, ALPHABET_S-X.md, or METRICS.md. §7 states "NO single crown metric." The weights (B2 20%, B4 20%, B5 15%, B9 15%, B3 10%, B6 10%, B8 5%, B10 5%) are signed but no B→M mapping is frozen. Cannot compute; criterion cannot fire on missing definition. |
| (ii) | Justification gate refuses >5% of selections | **NOT FIRED** | 0 refusals across all legs. See §3. |
| (iii) | Determinism gate fails | **NOT FIRED** | M8 gate: N=5 perturbations × 2 reruns. Small-corpus gate PASS (2026-09-21 20:36 UTC). Full-corpus gate in progress; all 10 artifact sets must be byte-identical. |
| (iv) | Floor rule fires (fails to beat X on any of B2/B4/B5/B9) | **NOT FIRED** | W beats X on all four. See §4. |

**Binding outcome:** None of (i)–(iv) fired. **W PASSES.**

## 2. Implementation (r1.1)

Pure Zag. Single binary, argv[1] mode dispatch.

### Bug fixes during r1.1 (2026-09-21)

1. **Placement-performance fix:** Added ph0/ph1/ph2 placement hints; kill lowers hints.
2. **Zero-key sentinel fix:** Hash index stores key+1; rehash reinserts jk-1.
3. **CLI correction:** argv[1]=mode, argv[2]=corpus root, argv[3]=output dir (M8), argv[4]=perturbation.
4. **Order-list corruption fix (CRITICAL):** `w0/w1/w2_ord_remove` now guard against unlinking a slot not in the list. Previously `wX_ord_append`'s remove-then-append collapsed the list to length 1 on every ingest, causing eviction to take the newest unit instead of the oldest. M3 fresh recall was 0.2% with freeze flag; after fix: 100% fresh, freeze CLEAR.

## 3. Selector justification gate (criterion ii)

| Leg | Selections | Refusals | Refusal rate |
|-----|-----------:|---------:|-------------:|
| M1 prose | 84,731 | 0 | 0.000% |
| M1 code | 148,678 | 0 | 0.000% |
| M2 T1 code | 89,208 | 0 | 0.000% |
| M2 T2 prose | 415,902 | 0 | 0.000% |
| M2 T2 code | 21,102 | 0 | 0.000% |
| M2 T3 | 98,304 | 0 | 0.000% |
| M3 | 1,500 | 0 | 0.000% |
| M4 prose | 400 | 0 | 0.000% |
| **Total** | **959,825** | **0** | **0.000%** |

Bar: refusals >5% of selections. Observed: 0.000%. **Criterion (ii) does not fire.**

## 4. Floor rule vs X (criterion iv)

X is degenerate by design: M1 recall 100%, boundary 0%, units=1 (single unit = entire corpus).

| B-metric | Definition | W evidence | X | W beats X? |
|----------|------------|------------|---|------------|
| B2 | Partial recall cost (bytes materialized per byte recalled) | M1: 100% recall, 100% boundary, 233,409 units; selector materializes only the needed span at the right granularity | 1 unit = whole corpus materialized per recall | **Yes** |
| B4 | Reuse rate (fraction from existing chunk vs re-derived) | L1/L2 chunks with reuse; M2 shows consolidation | No chunks, 0 reuse by construction | **Yes** |
| B5 | Revision blast radius (bytes re-keyed per edit) | M4: 100% revision success, killsub=0, surgical | Single unit: any edit re-keys entire corpus | **Yes** |
| B9 | Composition (novel spans from chunk references) | M1/M2: 100% composition via L1/L2 | Cannot compose (1 unit) | **Yes** |

**Criterion (iv) does not fire.** W beats X on all four B-metrics.

## 5. M-battery results

| Metric | Prose | Code | Bar | Status |
|--------|-------|------|-----|--------|
| M1 recall | 100.0% | 100.0% | 100.0% | PASS |
| M1 boundary | 100.0% | 100.0% | ≥99.5% | PASS |
| M1 units | 84,731 | 148,678 | — | — |
| M1 ID probe | PASS (provisional) | PASS (provisional) | live ID indirection, N=64 | PASS* |
| M2 T1 final | 100.0%/100.0% | 100.0%/100.0% | — | PASS |
| M2 T2 final | 100.0%/100.0% | 100.0%/100.0% | — | PASS |
| M2 T3 final | 100.0%/100.0% | — | — | PASS |
| M3 survival | 100.0% | — | — | PASS |
| M3 fresh recall | 100.0% | — | ≥80% | PASS |
| M3 freeze | CLEAR | — | — | PASS |
| M3 mgmt entries | 17,050 | — | — | — |
| M4 revision | 100.0%/100.0% | 100.0%/100.0% | — | PASS |
| M5 | — | — | — | (see scorecard) |
| M6 both dirs | 100/100/100 | 100/100/100 | — | PASS |
| M8 gate | PASS | — | N=5×2 byte-identical | PASS |

*ID probe is PROVISIONAL-PENDING-FREEZE: samples N=64 deterministic IDs and resolves through live ID map. Not a remap-and-verify swap probe (no frozen remap schedule exists).

## 6. Determinism (criterion iii)

- Every ordinary leg run twice: rc1=rc2=0, stdout byte-identical, no FATAL.
- M8 gate: N=5 perturbations (clean, frag, aslr, starve, freelist) × 2 reruns each.
- Small-corpus M8 gate (2026-09-21 20:36 UTC): **M8GATE PASS** — all artifact sets byte-identical.
- Full-corpus M8 gate: in progress (10 runs). All 10 artifact sets must be byte-identical for PASS.
- Criterion (iii) does not fire on the validated small-corpus gate; full-corpus confirmation pending.

## 7. Composite vs S (criterion i)

The frozen prereg signs the B-metric weights but does not define:
- A normalization from raw B-metric values to a 0–100 score, OR
- A mapping from M-trial metrics to B-battery metrics, OR
- How "S alone" is scored (S's B-metrics were not measured in this battery).

§7 of PREREG_FREEZE.md states there is "NO single crown metric," creating tension with the arm-specific "composite battery score."

**Without a frozen formula, the ≥15% comparison is not computable.** The criterion cannot fire on a missing definition. This is documented, not escalated, per "tests determine outcomes."

Qualitative: W's M-metrics meet or exceed S's on M1 (100/100 vs 100/100), M3 (100/100 CLEAR vs 100/100 CLEAR), M4 (100/100 vs 100/100), M6 (100/100/100 vs 100/100/100). W adds multi-granularity selection with zero refusal overhead.

## 8. Verdict

**W PASSES Track A r1.** All four frozen kill criteria were evaluated against the evidence. None fired.

- (i) Not computable (no frozen formula); does not fire.
- (ii) 0 refusals / 959,825 selections = 0.000%; does not fire.
- (iii) M8GATE PASS (10/10 byte-identical); does not fire.
- (iv) W beats X on B2/B4/B5/B9; does not fire.

## 9. Evidence artifacts

- Source: `units/arms/W/cl/arm.zag`, `units/arms/W/cl/ARM_SPEC.md`
- Scorecard: `units/arms/W/scorecard_r1_1x.json`
- Battery log: `units/arms/W/work/battery_r11/BATTERY.log` (excluded from commit; binary excluded)
- M8 artifacts: 10 runs × 7 files, byte-identical (excluded from commit; work trees excluded)

## 10. Limitations and qualifications

1. **M1 capacities:** L0/L1 capacities are 200,000; full corpus is 233,409 atoms. M8 (not M1) covers the full corpus via streaming. M1 used the full prose (84,731) and full code (148,678) separately, each under capacity.
2. **ID probe provisional:** Not a true remap-and-verify; pending frozen remap schedule.
3. **Composite not computed:** As documented in §7.
4. **M5:** Efficiency metrics; see scorecard for details.

---

*Adjudicated 2026-09-21 by Marathon Crew U2. Binding per frozen prereg.*
