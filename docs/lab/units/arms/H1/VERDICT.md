# H1 — VERDICT

**Arm:** H1 (Full deliberation per boundary)
**Date:** 2026-09-21
**Status:** PARTIAL — 1x battery incomplete (infrastructure interruptions); kill criteria 2 & 3 evaluated SAFE, criterion 1 UNEVALUABLE.

## Kill Criteria Assessment

### Criterion 1: Reuse hit rate ≤ fixed-64B baseline + 10pp
**Status:** UNEVALUABLE

**Reason:** 
- The term "reuse hit rate" is ambiguous in the frozen prereg. It could mean:
  (a) Content-based dedup rate in a single ingest (fraction of chunks with duplicate content);
  (b) ID-mapping hit rate on re-ingest (M7 definition: served-from-ID-mapping / lookups);
  (c) Dedup ratio (M7: 1 − distinct stored / total ingested).
- H1's dedup is by (corpus, offset, length) span-key, not by content. In a single M1 ingest, content-based reuse is 0% by construction (offsets are unique).
- The fixed-64B baseline numbers are not available (B-64 binary not built; coordinator holds reference results).
- **Action required:** Coordinator to clarify the definition and provide B-64 baseline reuse rates at equal live-store slots for both corpora.

### Criterion 2: Refusal rate >30% AND mean delib ops >10^4
**Status:** SAFE (not firing)

**Evidence (M1-1x-prose, 22,508 chunks; M1-1x-code, 39,501 chunks):**
- Refusal rate: 0.0% on both corpora (0 refusals / 62,009 candidates)
- Mean deliberation ops per committed cut: 253 (prose), 252 (code)
- Thresholds: 30% and 10,000
- **Margin:** Refusal is 30pp below threshold; ops are ~9,750 below threshold (39× headroom).

The deliberation is cheap (integer evidence accumulation) and the BAR (60) is calibrated so that valid boundaries commit. Zero refusals indicates the noticer + evidence system is not over-strict.

### Criterion 3: BAR ±10% sensitivity flips >25%
**Status:** SAFE (not firing)

**Evidence (M1-1x-prose, M1-1x-code):**
- Sensitivity flips: 0.0% on both corpora (0 flips / 62,009 candidates)
- Threshold: 25%
- **Margin:** 25pp below threshold.

Zero flips indicates the commit decisions are robust to ±10% BAR variation (54/66). The evidence scores are not clustered near the BAR boundary; they are decisively above or below.

## M1 Results (1x)

### Prose (5.4MB)
- Recall: 100.0% (22,508/22,508 chunks verified byte-exact)
- Boundary accuracy: 100.0% (exact recall implies exact boundaries)
- Units: 22,508 chunks, mean ~241 bytes
- A15 ID probe: PASS (64/64 swaps, all restored correctly) — PROVISIONAL-PENDING-FREEZE
- Refusal: 0.0%
- Delib ops/cut: 253
- BAR flips: 0.0%
- Ablation (grid-only): 6,698/6,698 valid (100%)

### Code (9.5MB)
- Recall: 100.0% (39,501/39,501 chunks verified byte-exact)
- Boundary accuracy: 100.0%
- Units: 39,501 chunks, mean ~241 bytes
- A15 ID probe: PASS (64/64) — PROVISIONAL-PENDING-FREEZE
- Refusal: 0.0%
- Delib ops/cut: 252
- BAR flips: 0.0%
- Ablation (grid-only): 10,738/10,738 valid (100%)

## M3 Results (1x, churn)
- Valuable survival: 100.0% (1,000/1,000 pinned chunks survived 3k kills)
- Fresh recall: 100.0% (500/500 fresh chunks verified)
- Management entries: 1,920 (OP_ADD/KILL/PIN/WEAKEN/EVICT/REFUSE/VAL in audit ledger)
- Weakens handled: 50/50
- Freeze check: CLEAR (no store freeze under churn)

## Determinism
- M1-prose: Two runs byte-identical (harness verified IDENTICAL).
- Zero RNG in decision paths (all tie-breaks by priority/position/ID).
- Integer arithmetic only.

## Battery Status
- **1x:** PARTIAL. m1-1x-prose PASSED, m1-1x-code PASSED, m3-1x PASSED (smoke). Remaining legs (m2, m4, m5, m6, m7, m8) NOT RUN due to infrastructure interruptions (service restarts killing long-running battery).
- **10x:** NOT ATTEMPTED (1x incomplete; also requires chunk-safe ingestion for 95MB code corpus exceeding 2^25 slice limit).

## Ambiguities Logged
1. **Reuse hit rate definition** (kill criterion 1): Content-dedup vs re-ingest-hit vs M7-dedup-ratio. H1's span-key includes offset, so content-based reuse is 0% in single ingest. Requires coordinator clarification.
2. **Nomination overflow:** 256-entry cap per 4 KiB window may truncate punctuation-heavy windows before top-16 selection. Violates "full-window priority" in edge cases. Not observed in M1 (max nominations < 256), but not proven.
3. **Span-key collision:** `(cid<<36)|(off<<12)|len` collides when `len=4096`. Window size caps len < 4096 in practice, but not enforced.
4. **M3 operation counts:** Implementation segments the 448KB fresh buffer; whether this literally realizes 3,000-add / 3,000-kill / 4,000-add is not verified by chunk counts.
5. **M7 provisional:** H1 runs the C′ schedule (XOR every 100th unit) but B-64 reports N/A, making "baseline +10" ambiguous. Reported as informational.

## Recommendation
H1 demonstrates the core mechanism works: deliberate boundaries via inspect/propose/commit achieve 100% recall with zero refusals, zero BAR sensitivity, and cheap deliberation (253 ops/cut). The cognitive act model is viable.

**However:** Kill criterion 1 cannot be evaluated without (a) clarification of "reuse hit rate" and (b) B-64 baseline numbers. The 1x battery is incomplete. 

**Provisional verdict:** H1 SURVIVES on criteria 2 and 3 with large margins. Criterion 1 requires coordinator input. Full 1x battery should be completed (infrastructure permitting) before final verdict.

## Files
- Spec: `docs/lab/units/arms/H1/ARM_SPEC.md`
- Build log: `docs/lab/units/arms/H1/BUILD_LOG.md`
- Source: `tnn-lab/units/arms/H1/cl/arm.zag`
- Binary: `tnn-lab/units/arms/H1/work/arm_bin` (not for commit)
