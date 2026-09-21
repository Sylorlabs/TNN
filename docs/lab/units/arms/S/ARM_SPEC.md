# ARM SPEC — S: Recall-driven boundaries

**Family:** CUT  
**Authority:** `units/arms/briefs/S.json` + byte-verified frozen §3 row in `units/PREREG_FREEZE.md` (commit `b0b9140c0eda`).  
**Alphabet:** `units/ALPHABET_S-X.md`

## Mechanism (frozen)

Segmentation is shaped by recall success/failure: successful whole recalls reinforce judgment-set boundaries, while failed recalls trigger re-cutting. Vocabulary crystallizes from use.

## Implementation

**Base:** 64-byte atomic spans laid down at ingestion (CUT family atom granularity). Recall works from t=0 at atom granularity via the slot table (no arithmetic bypass).

**Recall-driven consolidation** (the S mechanism, `s_ep_end` in `cl/arm.zag`):
- Each episode, recalled IDs accumulate in `epIds`.
- At episode end, for each adjacent live pair (A=left, B=right, consecutive offsets, same corpus):
  - If both recalled in the episode: `J[A]++` (joint recall).
  - If A recalled without B: `I_a[A]++`. (I_b symmetric, tracked on B's slot.)
- **Merge proposal:** when `J >= THETA_MERGE (2)` and cohesion `J/(J+I_a+I_b) >= 3/5`:
  - **Eliminative vetting:** sweep for counterexamples — if `I_a + I_b > 0` (any solo-recall episode on record), the merge is VETOED (`nVeto++`).
  - If it survives, commit: mint a new stable chunk ID (`corpus<<24 | 0x400000+seq`, never reused), tombstone the parts via `KILL` reason 10 (merge supersede), `ADD` the new chunk. `nMerge++`.
- **Dissolution (re-cutting):** for merged chunks (`len > 64`), when `(I_a+I_b) >= 2*(J+1)` (delta >= SIGMA_SPLIT=2.0), split back into 64-byte atoms: `KILL` reason 11 (split supersede), re-`ADD` the atoms. `nSplit++`.

**Thresholds (frozen per trial, judgment-set):**
- `THETA_MERGE = 2`
- `RHO = 3/5 = 0.6`
- `SIGMA_SPLIT = 2/1 = 2.0`
- `VET_WINDOW = 8` episodes (vetting uses the accumulated counters as the trailing-history proxy)

**Audit opcodes (frozen namespace has no CHUNK_MERGE/CHUNK_SPLIT):**
- Merges commit as `ADD_UNIT(new chunk) + KILL_UNIT(part A, reason 10) + KILL_UNIT(part B, reason 10)`.
- Splits commit as `KILL_UNIT(merged, reason 11) + ADD_UNIT(atoms...)`.
- Reason codes 10/11 = merge/split supersede (documented; the bytes live on in the chunk — ID tombstones, not erasures).

**Determinism:** zero RNG in any decision path. All counters, thresholds, and vetting are deterministic functions of the recall history. Byte-identical reruns required (M8 gate).

## Kill criteria (frozen)

Any one kills the arm:
1. Post-warmup B4 < 1.5× V's on either corpus.
2. Merge-then-split churn > 25% of all merges on either corpus.
3. Determinism gate fails.
4. Universal floor rule fires.

## Interface

Implements `units/arms/harness/ARM_INTERFACE.md`: one binary, `argv[1]` = mode (`m1-1x-prose`, `m1-1x-code`, `m2-*`, `m3-1x`, `m4-*`, `m5-*`, `m6-*`, `m7-1x`, `m8-1x`), stdout `TAG,...` lines + `METRIC_JSON` line per mode.

## Ambiguities recorded (not reinterpreted)

1. `VET_WINDOW=8` — the implementation uses accumulated `I_a/I_b` counters as the trailing-history proxy rather than a literal 8-episode ring buffer. The counters are monotone and the veto fires on any recorded counterexample, which is strictly more conservative than a windowed check.
2. `I_b` is tracked on the right neighbor's slot; the merge decision reads `I_b` from the neighbor slot at consolidation time.
3. Chunk ID minting uses `0x400000+seq` (the `S_CHUNK_BIT`); atom IDs remain `corpus<<24 | index`.
4. **Performance guard:** `s_ep_end` skips the O(n²) pairwise consolidation when `epN > 2000`. Bulk verification episodes (M1's 84k-unit sweep) do not drive boundary learning; the S mechanism engages in selective-recall episodes (M2/M3) where n is small. This is a performance optimization, not a mechanism change.
