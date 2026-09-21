# Arm Q — Verdict: KILLED

**Date:** 2026-09-21
**Arm:** Q — Hybrid taught+emergent (ACQ family)
**Brief:** ~/workspace/tnn-lab/units/arms/briefs/Q.json
**Verdict:** KILLED (Death Criterion 1 triggered)

## Death Criteria Evaluation

### Criterion 1: Hybrid must beat max(taught-only, emergent-only) + 3 points
**STATUS: TRIGGERED → KILL**

**Measurements:**
- Q-hybrid (variant=0) M1 prose recall: 100.0%
- Q-taught-only (variant=1, emergent promotions disabled) M1 prose recall: 100.0%
- Q-hybrid M2 episodes-to-criterion: 1
- Q-taught-only M2 episodes-to-criterion: 1
- Q-emergent-only (variant=2, no taught seeding): 0% by design (no vocabulary without seeding)

**Analysis:**
max(taught-only, emergent-only) = max(100.0%, 0%) = 100.0%
Q-hybrid (100.0%) does NOT beat 100.0% + 3 points.

The emergent machinery adds zero measurable value on the primary bar (M1 recall / M2 etc). The hybrid performs identically to taught-only, indicating the "taught proposals seed emergent machinery" mechanism does not improve over pure taught admission on these metrics.

**O/P Comparator Gap (logged, not replaced):**
- O (taught arm): Broken — single M1 leg showed 0% recall, 0 adopted words. Not a valid comparator.
- P (emergent arm): Not finalized — no scorecard or vocabulary export available.
- Per task instructions, missing O/P dependencies are logged here, not replaced with invented criteria. The Q-internal ablation (variant=1) provides the taught-only baseline.

### Criterion 2: Collision resolution kills ≤10% of entries per W episodes
**STATUS: NOT TRIGGERED → PASS**

**Measurements:**
- M2 T1 prose: m2_collisions=0, m2_collide_kills=0
- Kill rate: 0% (well below 10% threshold)

### Criterion 3: Adversarial score ≥ emergent-only
**STATUS: CANNOT EVALUATE**

**Reason:** P (emergent arm) not finalized; no adversarial score available for Q or P. Logged as dependency gap.

## Summary of Test Results

| Metric | Q-hybrid | Q-taught-only | Delta |
|--------|----------|---------------|-------|
| M1 prose recall | 100.0% | 100.0% | 0.0 |
| M1 prose boundary | 100.0% | 100.0% | 0.0 |
| M1 code recall | 100.0% | (not run) | — |
| M2 T1 etc | 1 | 1 | 0 |
| M2 final recall | 100.0% | 100.0% | 0.0 |
| M2 collisions | 0 | 0 | 0 |
| M2 collide kills | 0 | 0 | 0 |
| M3 retention | 100.0% | — | — |
| M4 rev boundary | 100.0% | — | — |
| M5 ledger entries | 262,144 | — | — |
| M6 recall/boundary | 100.0%/100.0% | — | — |
| M7 | N/A (deferred) | — | — |
| M8 | PASS — all 5 perturbations ×2 byte-identical | — | — |

## M8 determinism gate (completed 2026-09-21)

Corpus: `harness/corpora/r1/` (`t1_prose.bin`, `t1_code.bin`).
Each perturbation ran twice; stdout + artifacts (store hash chain,
ledger hash chain, `ledger.bin`, `alloc_trace.txt`, `store_hashes.txt`)
compared byte-for-byte between run1 and run2.

| Perturbation | run1=run2 | stdout | store chain | ledger chain |
|---|---|---|---|---|
| clean | IDENTICAL | `M8,100.0,211168,0` | `ec27bdaf56b82c0d…cafd5` | `4d4f1dba759b18d0…794d25` |
| frag (256 nio_alloc churn pre-pass) | IDENTICAL | `M8,100.0,211168,0` | same as clean | same as clean |
| aslr (1,234,567-byte alloc pad) | IDENTICAL | `M8,100.0,211168,0` | same as clean | same as clean |
| starve (LD_PRELOAD shim: getrandom/getentropy fail, clock_gettime zeroed) | IDENTICAL | `M8,100.0,211168,0` | same as clean | same as clean |
| freelist (arm-internal no-op) | IDENTICAL | `M8,100.0,211168,0` | same as clean | same as clean |

All 5 perturbations are byte-identical across the full artifact set, and all
perturbations match the clean run — i.e. heap layout, allocation churn, and
entropy/clock starvation have zero effect on the arm's output. **M8 gate PASSES.**

## Implementation Notes

**Source:** `cl/arm.zag` in this directory (71,847 bytes, pure Zag, zero RNG)
**Compiler (frozen):** ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

**Key mechanisms implemented:**
- Q store with provenance (taught/emergent/settled)
- 64-byte audit layout (op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60)
- ID/span maps, insertion order, free stack
- Pair co-occurrence, promoted phrase tables
- Teacher counting with two-pass phrase-aware ingestion
- Collision scoring: taught=min(count,1000)+200, emergent=2*min(cooccur,1000), emergent wins ties
- K=7/W=200 promotion with deterministic sorting
- Variant modes: 0=hybrid, 1=taught-only (no promotions), 2=emergent-only (no admission)

## Deviations / Caveats

- **M2 early-exit:** stops after 5 episodes if criterion met (outputs 45 zero-padded M9 entries). Frozen spec may require all 50 episodes. Flagged for review.
- **M7 N/A:** returns N/A (manual lookup rig hits a znc codegen issue; M1 ID probe covers ID integrity).
- **O/P comparator gaps:** O broken (0% recall on its M1 leg); P not finalized. Q-internal variant=1 ablation used as the taught-only baseline. No O/P data invented.

## Verdict Rationale

Arm Q is KILLED by Death Criterion 1. The hybrid mechanism ("taught proposals seed emergent machinery") does not beat the taught-only baseline by the required 3-point margin on M1 recall or M2 episodes-to-criterion. The emergent component adds no measurable value on the primary bar.

The arm is mechanically sound (100% recall, 0% collision kills, full M8 determinism gate passing), but the hybridization hypothesis is falsified by the ablation: taught-only performs identically to hybrid.
