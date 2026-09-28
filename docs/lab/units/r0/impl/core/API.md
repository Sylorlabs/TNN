# R0 Core API — native dual-route endogenous chunker

`r0_core.zag` — Track R0, prereg `PREREG_FREEZE.md` §2 (FROZEN 2026-09-21).
Pure Zag. **Zero randomness in any AI decision path.** Every function is
deterministic given the state arena: no RNG, no clock reads, no
pointer/address hashing, no uninitialized-memory reads (`r0_init` zeroes the
arena explicitly; all tie-breaks are by integer order).

Ported from the recovered R31 spec
(`units/archaeology_r31/docs_generations_R31_tnn_r31_endogenous_chunking.zag`,
i32 32-symbol microstate streams) to **byte streams (alphabet 256)**.
Verified against `ARCHAEOLOGY_R31.md`: `r31_compression_gain =
(n-1)*seen-(n+3)` verbatim; greedy longest-match segmentation with negative-ID
literal fallback; split/merge firing conditions; support-gap abstain (−1);
dual-route trust weights.

## State model

The caller allocates **one** `[]i32` arena of `r0_arena_words()` words
(222,240 words ≈ 870 KiB) via `zalloc_i` and passes it (`st`) to every call.
Layout: 32-word header, 4,096-slot proposal table, 1,024-slot chunk bank,
512-slot pair table, 2,048-entry ledger (16-word sparse entries, stride 64).
No hidden allocation inside the core.

## Legs (R-7 test-both, R-8)

Selected once at `r0_init(st, leg)`; both legs compile into one binary.

| item | leg 0 recovered (R-8) | leg 1 re-derived (R-7) |
|---|---|---|
| promotion | seen ≥ 5, purity ≥ 0.34, utility > 0 | seen ≥ 6, purity ≥ 0.40, utility > 0 |
| purity definition | majority-label fraction (R-1 frozen) | joint-success fraction (label 3 = recall ∧ consistency) |
| compression-term cap | 1000 (1.0) | 500 (0.5) — grounding dominates harder |
| inventory | 700 chunks | 1024 chunks |
| split: learned_conflict | 400 | 500 |
| merge: learned_pair_seen | 3 | 4 |
| merge: learned_gain | 0 | 500 |
| support-gap: learned_min_support / learned_margin | 3 / 2 | 4 / 3 |

Span enumeration 2..8 (`R0_LMAX=8`, R-2 giant-span bar) is identical in both
legs. Utility (i32, scale 1000):
`utility = gain*0.02 + max(0,purity−0.2)*log1p(seen)*len`,
with `gain = (n−1)*seen − (n+3)` verbatim from the recovered spec and the
compression term **capped** per the R-2 anti-giant-span-exploit clause.

## Grounded-consequence labels (R-1)

`r0_observe_span` takes `label`: `-1` = count only; `0..3` = count + label,
bit0 = recall success (a), bit1 = downstream discrimination consistency (b).
Per-occurrence labels accumulate into 4-bin histograms on proposals and
chunks; purity/conflict derive from them.

## Chunk ID semantics (K-R3)

- IDs are **monotonic issuance order**: `0 .. r0_chunk_count(st)-1`.
- IDs are **never reused**. Split/merge/archive **tombstone** the source ID;
  bytes are retained and `r0_chunk_succ` records the successor, so every
  issued ID always resolves — **ghost IDs are impossible by construction**.
- `r0_tombstone_ratio1000` reports tombstoned/live in 1/1000 (K-R3 bar: < 2).
- Segmentation matches **live** chunks only; `r0_reconstruct` resolves any
  issued ID (live or tombstoned) — old segmentations stay byte-exact.

## Function reference

```
// lifecycle
r0_arena_words() i32                          // words to zalloc_i
r0_init(st:[]i32, leg:i32) void               // zero arena, set leg/thresholds/weights
r0_leg(st) i32                                // 0 recovered, 1 re-derived

// observe: enumerate spans 2..8 at every position (R-2); hash+count+label
r0_observe_span(st, seq:[]i32, start:i32, n:i32, label:i32, next_byte:i32) i32
    // label -1 count-only, 0..3 grounded label; next_byte -1 at stream end
    // returns proposal index, -1 if table full / n out of range
r0_find_proposal(st, seq, start, n) i32       // -1 if unknown
r0_proposal_seen(st, p) i32
r0_proposal_contb(st, p) i32                  // first continuation byte, -2 none

// promote: seen>=S AND purity>=P AND utility>0; ranked by utility, stored longest-first
r0_promote(st, idx:[]i32) i32                 // idx scratch >= 4096 i32; returns #promoted
    // emits CUT_PROPOSE + CUT_COMMIT per promoted chunk

// chunk queries
r0_chunk_count(st) i32        // issued IDs = 0..count-1
r0_live_count(st) i32
r0_chunk_state(st, id) i32    // 1 live, 2 tombstoned, -1 unknown
r0_chunk_len(st, id) i32
r0_chunk_use(st, id) i32
r0_chunk_utility(st, id) i32  // 1/1000 units
r0_chunk_succ(st, id) i32     // successor after split/merge, -1 none
r0_chunk_bytes(st, id, out:[]i32, max_out:i32) i32  // resolves any issued ID
r0_tombstone_ratio1000(st) i32

// segment: greedy longest-match; unmatched byte -> literal id = -1-byte
r0_segment(st, seq, seqlen, out_id, out_start, out_len, max_out) i32  // returns n units
r0_reconstruct(st, ids, n, out, max_out) i32   // byte count; -1 on unknown ID (loud, K-R5)

// split/merge — ledger-audited; boundaries are mutable hypotheses
r0_split_at(st, id, split_at) i32      // primitive; -1 unless 2<=split_at<=len-2
r0_maybe_split(st, id) i32            // fires iff use>=3 AND conflict>=learned_conflict
                                      //   AND utility<=learned_utility_floor; splits at len/2
r0_observe_pair(st, a, b) void        // adjacent-ID recurrence (merge evidence)
r0_pair_seen(st, a, b) i32
r0_maybe_merge(st, a, b) i32          // fires iff pair_seen>=learned_pair_seen AND
                                      //   joint_gain-separate_regret>=learned_gain; len<=8
r0_archive(st, id, reason) i32       // CUT_KILL; tombstone without successor
r0_regret_update(st, id, useful, recon_ok, rate) void  // delayed regret -> utility/regret
r0_learn_thresholds(st, merge_helped, merge_regret) void  // deterministic threshold
                                      // adaptation; emits R0_OP_THRESH (never silent)

// support-gap recruitment: largest unsupported raw span, else abstain (-1)
r0_support_gap_recruit(st, seq, seqlen) i32
    // recruits iff support>=learned_min_support AND beats runner-up by learned_margin

// dual route: raw high-fidelity evidence alongside the chunked route
r0_dual_score(st, chunk_score, raw_score, recon_err, disagreement) i32
r0_dual_trust_update(st, chunk_helped, raw_helped, recon_ok, rate) void
r0_should_retrieve_raw(recon_err, disagreement, uncertainty, cost, threshold) i32
r0_w_chunk(st) i32
r0_w_raw(st) i32

// ledger: 16-word entries — op@0, slot@4, rc@8, b1..b5@12..28,
//         a1..a5@32..48, stage@52, d1@56, d2@60 (stride 64 i32 words)
r0_ledger_emit(st, op, slot, rc,
    b1,b2,b3,b4,b5, a1,a2,a3,a4,a5, stage, d1, d2) i32  // entry idx, -1 if full
r0_ledger_count(st) i32
r0_ledger_hash(st) i32   // FNV-1a chain over entries (M8 evidence)
```

## Ledger op codes

Crew-1 scheme (`ALPHABET_A-F.md`: `CUT_PROPOSE=0xC0 …`), adopted as R0's
choice for the arm-D line this track feeds (prereg A-3 unification is
Micah's call; remappable by amendment):

| op | code | emitted by | slot | b1..b3 | d1 / d2 |
|---|---|---|---|---|---|
| CUT_PROPOSE | 192 (0xC0) | promote | proposal idx | len, seen, purity1000 | hash / utility1000 |
| CUT_COMMIT | 193 (0xC1) | promote | chunk id | len, seen, utility1000 | hash / 0 |
| CUT_SPLIT | 196 (0xC4) | split | parent id | parent, child, split_at | parent_util / 1 |
| CUT_MERGE | 197 (0xC5) | merge | new id | left, right, pair_seen | joint_gain / separate_regret |
| CUT_KILL | 198 (0xC6) | archive | id | — | utility / reason |
| CUT_REUSE | 199 (0xC7) | harness | chunk id | use_count | — |
| SPAN_OBSERVE | 200 (0xC8) | observe driver | 0 | n_bytes, n_spans | first_byte / last_byte |
| RECRUIT | 201 (0xC9) | support-gap | new id or −1 | start, len, support | purity / reason* |
| TRUST | 202 (0xCA) | trust update | 0 | w_chunk, w_raw, rate | chunk_helped / raw_helped |
| SEGMENT | 203 (0xCB) | segment | 0 | n_units, n_chunks, n_literals | fnv(bytes) / 0 |
| THRESH | 204 (0xCC) | threshold learn | 0 | learned_gain, learned_pair_seen, learned_conflict | helped / regret |

\* RECRUIT d2 reasons: 0 recruited, 1 low support, 2 margin failed, 3 bank
full, 4 no gap, 5 span already issued.

Stages: 1 sensor, 5 memory, 9 revision, 10 decision (recovered spec).

## Determinism notes (M8)

- FNV-1a hashes are over **bytes only** — never pointers.
- Proposal lookup is insertion-ordered linear scan; promotion sort breaks
  ties by (len desc, hash asc); segment match ties break by lowest ID.
- `r0_init` zeroes the full arena; the core never branches on allocator
  state. Perturbation modes 0..4 in `run_smoke.sh` rearrange the heap before
  and during the run; stdout must be byte-identical.

## Files

- `r0_core.zag` — the core (no `main`; `@import("r0_core.zag")` to use).
- `r0_smoke.zag` — M8 smoke driver (`r0_smoke <leg 0|1> <perturb 0..4>`).
- `run_smoke.sh` — build + N=5 perturbation diff per leg.
- `API.md` — this file.
