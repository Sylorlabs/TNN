# H1 — Full Deliberation Per Boundary: ARM_SPEC

**Track:** A (Representation bake-off)
**Mechanism:** Boundaries as cognitive acts: every cut proposed, evidenced, and committed through inspect/propose/commit with a frozen noticer list and integer evidence weights.
**Status:** Implementation complete; 1x battery in progress (2026-09-21).
**Prereg:** commit `b0b914c0eda`, branch `tnn-native-lab`, repo `sylorlabs/TNN`.
**ID probe:** A15 64-remap probe implemented, labeled `PROVISIONAL-PENDING-FREEZE`.

## 1. Cognitive Architecture

H1 treats every chunk boundary as a deliberate cognitive act, not a mechanical split. For each 4 KiB window of input, the arm:

1. **INSPECT** — Four frozen noticers scan the window and nominate candidate cut positions:
   - Newline runs (priority 4)
   - Structural punctuation `{}[]();` (priority 3)
   - Sentence punctuation `.!?` (priority 2)
   - 256-byte grid fallback (priority 1)

2. **PROPOSE** — The top-16 nominations by (priority, position) become cut candidates. Each candidate accumulates integer evidence:
   - Separation evidence: `+1` per byte of distance from the previous cut (normalized)
   - Reuse evidence: `+2` if the exact span exists in the live store (dedup hit)
   - Vocabulary evidence: `+1` if the span matches a pinned vocabulary entry
   - Value evidence: `+0` (weight zero — value does not influence boundaries)

3. **COMMIT** — A candidate commits iff `score >= BAR` (BAR=60). The commit:
   - Allocates a slot in the live store
   - Records the span (corpus, offset, length) with a unique chunk ID
   - Logs `OP_CUT_COMMIT` (or `OP_ADD` for the chunk) to the audit ledger
   - If no candidate meets BAR, the cut is **refused** (`OP_CUT_REFUSE`), the deliberation is logged, and the remaining window tail becomes a fallback commit.

### Deliberation Accounting
- `delib_ops`: Total integer operations during deliberation (evidence accumulation, comparisons).
- `delib_cuts`: Number of committed cuts.
- `delib_ref`: Number of refused cuts.
- `delib_cand`: Number of candidates evaluated.
- Kill criterion: refusal rate >30% AND mean ops per cut >10^4.

### BAR Sensitivity
Each commit is also scored at BAR±10% (54 and 66). If the commit decision differs at either threshold, a `sens_flip` is recorded. Kill criterion: >25% of cut decisions flip.

## 2. Live Store

- **Capacity:** 4,096 slots (W=4096), 16 noticer nominations per window (C=16).
- **Dedup:** Exact span-key `(corpus, offset, length)` maps to slot. Reused spans get `+10` raw reuse evidence.
- **Eviction:** Weakest-first (lowest strength, oldest first). Killed slots are tombstoned; stale dedup entries fail liveness checks.
- **Pins:** Trainer-pinned chunks are immune to eviction. Pinned spans get `+20` raw vocabulary evidence.
- **Value:** Marking valuable sets a flag; weight is zero so it does not affect boundaries (per frozen spec).

## 3. Audit Ledger

Every state-changing operation logs a 64-byte entry:
- Layout: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60.
- Opcodes: `OP_ADD`(1), `OP_KILL`(2), `OP_PIN`(3), `OP_WEAKEN`(4), `OP_EVICT`(5), `OP_DEFECT`(6), `OP_REVISE`(7), `OP_REFUSE`(8), `OP_CUT_PROPOSE`(9), `OP_CUT_COMMIT`(10), `OP_CUT_REFUSE`(11), `OP_VAL`(12), `OP_SWAP_PROBE`(19).
- Retained mode: ledger kept in memory for M8 byte-identical artifacts.
- Stream mode: ledger folded into SHA-256 digest for large runs.

## 4. Metric Modes

| Mode | Description |
|------|-------------|
| `m1-1x-prose` / `m1-1x-code` | Ingest corpus, verify all chunks, 64 A15 swap probes, report recall/boundary/refusal/delib/sensitivity. |
| `m2-t1-prose` / `m2-t1-code` | T1 (10%) ingest + probe episodes, ETC for 3-consecutive ≥99.5% recall / ≥95% boundary. |
| `m2-t2-prose` / `m2-t2-code` | T2 (smaller) curriculum, same ETC criterion. |
| `m2-t3-1x` | T3 (1MB) single episode. |
| `m3-1x` | Churn: 3k fresh adds, 3k kills, 50 weakens, 4k fresh adds; valuable survival + fresh recall. |
| `m4-1x-prose` / `m4-1x-code` | 100 boundary + 100 content defects, ≤20 repair episodes. |
| `m5-1x` | Memory: RSS delta + slot table bytes; audit density (entries per KB). |
| `m5-baseline` | Empty-store baseline (allocates + touches slot table). |
| `m6-p2c-1x` / `m6-c2p-1x` | Transfer: train prose→test code (and reverse); revision check. |
| `m7-1x` | Provisional C′: XOR corruption every 100th unit, lookup `(l*37)%n`. |
| `m8-1x <root> <out> <pert>` | Combined M1+M3 with perturbation; byte-identical artifacts. |

## 5. Determinism

- Zero RNG in decision paths. All tie-breaks by (priority, position, ID).
- Byte-identical reruns verified by the harness (two runs diffed).
- Integer arithmetic only; no floating point in cognition.

## 6. Known Limitations (from implementation)

1. **Nomination cap:** 256 nominations per 4 KiB window; punctuation-heavy windows may truncate before top-16 selection. Violates full-window priority semantics in edge cases. (Logged as ambiguity.)
2. **Span-key packing:** `(cid<<36)|(off<<12)|len` collides when `len=4096`. (Not yet fixed; len is capped below 4096 by window size.)
3. **M1 probe schedule:** Fixed to exactly 64 via `(pi*nchunks)/64` stride (was modulo-based, could yield 63).
4. **A15 probe:** Side-channel (reads ledger, not memory). Labeled provisional.
5. **M7:** Reports N/A per B-64 reference; H1 runs the provisional C′ schedule but the kill-bar comparison is ambiguous.

## 7. Kill Criteria (frozen)

H1 dies if ANY one fires:
1. Reuse hit rate ≤ fixed-64B baseline + 10 absolute points at equal live-store slots on both corpora.
2. Refusal rate >30% AND mean deliberation ops per committed cut >10^4.
3. BAR ±10% sensitivity flips >25% of cut decisions.

## 8. Build Notes

- Single binary: `work/arm_bin`, `argv[1]` selects mode.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Source: `cl/arm.zag` (~1,700 lines), imports substrate relatively from `cl/`.
- znc bugs worked around: ZNC-2026-09-21-004 (slice-let off local struct), ZNC-2026-09-21-002 (slice as *u8), 2^25 slice limit.
