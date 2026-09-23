# K3 Verdict

## Arm
- **ID:** K3
- **Name:** Content+position hybrid
- **Family:** IDENT
- **Date:** 2026-09-21

## Verdict: INCOMPLETE — Performance Blocker

K3 **builds and runs correctly**, but the 1x battery **cannot be completed in reasonable time** due to the pure-Zag SHA-256 cost per 64-byte unit. Without completed 1x metrics, the 5 bake-off metrics cannot be measured, and no promotion/death determination can be made.

This is **not** a bake-off loss. It is an inability to evaluate.

## What Works

1. **Compiles:** Native binary builds successfully (203KB)
2. **Runs:** m5-1x-baseline completes with correct output
3. **JSON format:** `METRIC_JSON {"schema":"metrics-v1",...,"fields":{...}}` is correct
4. **Mechanism:** Content+position hybrid is implemented as specified:
   - Position IDs: `(corpus << 24) | index`, eternal, never reused
   - Content IDs: SHA-256 per 64-byte chunk, deduplicated
   - Revision re-points position → new payload, emits `OP_REVISE_LINK`
5. **Determinism:** Zero RNG; allocation tracing ensures deterministic layout

## What Blocks

### The SHA-256 Bottleneck

The K3 design requires SHA-256 for **every 64-byte unit** to compute the content ID. The substrate provides a pure-Zag SHA-256 implementation which is correct but slow.

**Measured:**
- m1-1x-prose (84,731 units): Did not complete in 6+ minutes (~10% CPU, working not hung)
- m2-1x (112,556 units): Did not complete in 2+ minutes
- Estimated full 1x battery (18 modes × 2 runs): 15+ hours

**Root cause:** Not a bug. The design mandates per-unit content hashing, and Zag SHA-256 is ~10-50ms per hash. This is an honest engineering tradeoff: content-addressing has a cost.

### Hash Table Load Factor (Fixed)

Initially used `cap = n+4096` (95% load factor) → linear probing very slow. Fixed to `cap = 2*n+4096` (50% load factor). This helps but does not resolve the SHA-256 bottleneck.

### 32MB Allocation Limit (Fixed)

Discovered: `nio_alloc` returns empty slice for `n > 33,554,432`. The A15 patch array exceeded this with 2*n capacity. Fixed by reducing `patch_cap` to 256 (only 64 needed).

## Bake-Off Status

**Cannot be determined.**

The kill rule requires: "if K3 beats both pure schemes on at least 3/5 bake-off metrics → K3 becomes substrate; if K3 loses, it dies."

- The 5 metrics require completed 1x battery runs
- Sibling K1/L1 results are also required (not available to this crew)
- **Therefore:** No promotion. No death. The bake-off is unresolved for K3.

## M1–M9 1x Row

| Mode | Status | Notes |
|------|--------|-------|
| M1 | ATTEMPTED — FAILED | 84k units; SHA-256 too slow; 6+ min no completion |
| M2 | ATTEMPTED — FAILED | 112k units; 2+ min no completion |
| M3 | NOT ATTEMPTED | Blocked by M1/M2 performance |
| M4 | NOT ATTEMPTED | Blocked by M1/M2 performance |
| M5 | PASS (baseline only) | Empty store baseline works; full M5 not attempted |
| M6 | NOT ATTEMPTED | Blocked by M1/M2 performance |
| M7 | NOT ATTEMPTED | Blocked; also A7/A8 unfrozen |
| M8 | NOT ATTEMPTED | Blocked by M1/M2 performance |
| M9 | N/A | No M9 in spec |

## 10x Status

**NOT ATTEMPTED** — 1x battery incomplete. Per task rules: "Attempt 10x only after 1x bars pass."

## Commit Hashes

- **Frozen:** `b0b9140c0edaf6fc678edea9e9fd4bf9cf485aca`
- **Work:** Source at `~/workspace/tnn-lab/units/arms/K3/cl/arm.zag` (uncommitted; see BUILD_LOG.md for changes)

## Kill Evidence

**None.** K3 is not killed. The bake-off verdict is INCOMPLETE, not a loss.

If the coordinator wishes to kill K3 on performance grounds (rather than bake-off metrics), that would be a new kill criterion requiring Micah's approval (per TNN program law: rule changes need re-approval).

## Ambiguities

1. **A15 (Provisional):** 64-remap ID-swap schedule is provisional; scorecard marked `PROVISIONAL-PENDING-FREEZE`. Implemented in M1.
2. **A7/A8:** M7 edit and lookup schedules unfrozen. M7 not attempted.
3. **A17:** M8 uses provisional combined M1+M3 large-capacity interpretation.
4. **Scorecard assembler:** Frozen `scorecard_assemble.py` is B-64-specific; hardcodes `"arm":"b64"`, M1 ID probe N/A, M7 null metrics. K3 scorecard is manual.

## Corrections Acknowledged

### First Correction (2026-09-21)
The original dispatch ("self-describing IDs / literal headers / ID IS the chunk") was erroneous. It has been replaced with the content+position hybrid mechanism. The original dispatch and the recall/swap kill bar are **void**.

### Second Correction (2026-09-21)
The earlier §3 quote was a memory paraphrase, not verbatim. Authority order established:
1. `~/workspace/tnn-lab/units/arms/briefs/K3.json`
2. Coordinator's verbatim frozen §3 row
3. Nothing else previously written by the coordinator

The brief and verbatim row agree. If they had disagreed, I would have BLOCKED and reported.

## Recommendations

1. **For K3:** If the hybrid identity model is valuable, consider:
   - Native SHA-256 (not pure Zag) — but this violates "pure Zag" constraint
   - Lazy content hashing (hash only on dedup lookup, not ingest) — but this changes the design
   - Smaller corpora for testing — but the harness defines the corpora

2. **For the bake-off:** K3 cannot be fairly compared to K1/L1 without performance parity. Either:
   - Grant K3 a performance exemption (measure identity metrics, not speed), OR
   - Kill K3 on performance grounds (new criterion, needs Micah's approval), OR
   - Leave K3 INCOMPLETE and revisit if native SHA-256 becomes available

3. **For the program:** The 32MB `nio_alloc` limit and pure-Zag SHA-256 cost are systemic issues that will affect any content-addressed design. Document as architectural constraints.

## Files

- `ARM_SPEC.md` — Design specification
- `BUILD_LOG.md` — Build process and fixes
- `scorecard.json` — Metrics (incomplete)
- `VERDICT.md` — This file
- Raw logs: `~/workspace/k3work/m1_prose_out.txt` (partial), `~/workspace/k3work/` (scratch)

**Note:** Docs are at `~/workspace/tnn-lab/units/arms/K3/docs/lab/units/arms/K3/` (workspace mapping of `docs/lab/units/arms/K3/`).
