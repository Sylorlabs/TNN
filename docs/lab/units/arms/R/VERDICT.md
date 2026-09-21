# VERDICT.md — Arm R (Compression cuts, MDL/DP)

## Authority acknowledgment
1. The original dispatched "Deliberate boundary revision" definition was wrong and is **VOID**.
2. An earlier coordinator paraphrase of frozen §3 was superseded.
- Authoritative: **R — Compression cuts (MDL/DP)**, family CUT.
- Mechanism: "Chunks are compression units: cut where description length is minimized (suffix-array/LCP + DP over cost)."
- Binding kill: boundary F1 against whitespace/punctuation joints and arm O's taught spans, separately, must beat fixed-64B by ≥10 points on both corpora; **or** held-out M1 recall with R-cuts must beat the 64B baseline.

## Build verdict: SUCCESS
- Source: `units/arms/R/cl/arm.zag` compiles cleanly with frozen znc toolchain.
- Binary: `work/r_bin` (261,808 bytes), one-binary mode dispatch.
- Pure Zag, deterministic, zero RNG.

## Correctness verdict: VERIFIED (tiny corpora)
- `x-segcheck` on 240-byte corpus: `X-SEGCHECK,4,1` — 4 chunks, byte-identical rerun confirmed.
- `m1-prose` on 240-byte corpus: `M1,prose.bin,100.0,100.0,4` — 100% recall, 100% boundary.
- Suffix array, LCP, DP, ingest, recall all function correctly.

## Battery verdict: BLOCKED ON PERFORMANCE
- **1x battery CANNOT COMPLETE**: `m1-prose` on 5.4MB prose timed out after 15 minutes during suffix-array construction.
- Root cause: prefix-doubling SA does ~946M cget/cset operations for n=5.4M; Zag function-call overhead too high.
- Estimated: >15 min for 5.4MB prose, >30 min for 9.5MB code. Full 1x (20+ runs) needs 10+ hours; 10x needs 100+ hours.
- **10x: NOT ATTEMPTED** (1x blocked).

## Kill evaluation: CANNOT EVALUATE
- Boundary F1 vs 64B: BLOCKED (requires full-corpus segmentation).
- Arm O taught spans: BLOCKED (artifact absent; O unit has only `cl/` and `substrate/`).
- Held-out M1 recall vs 64B: BLOCKED (requires full-corpus runs).
- **No kill fires** — insufficient evidence to evaluate.

## Provisional ambiguities (non-frozen)
- `L=64`, `ref_cost=2`: provisional examples, not frozen.
- Boundary-F1 formula, tolerance: proposed, not frozen.
- A15 swap schedule: PROVISIONAL-PENDING-FREEZE.
- M7 reuse, C′ edit, M6 frozen-dict, A17 M8: provisional/open.

## Path forward
1. Optimize SA: inline array accesses (avoid cget/cset overhead) or implement SA-IS linear-time.
2. Or: use faster repeat-finding (e.g., suffix automaton) while preserving MDL/DP semantics.
3. Re-run battery after optimization.
4. Obtain arm O taught-span artifact for kill leg 1.

## Commit
- Source, BUILD_LOG.md, VERDICT.md, ARM_SPEC.md to be committed.
- `work/` (binaries, logs, fixtures) excluded.
