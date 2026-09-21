# M2 — Compositional counter IDs — Arm Specification

Family: IDENT. Track A representation bake-off, round r1.
Worktree: `units/arms/M2/` (implementation: `cl/arm.zag`, substrate:
`substrate/R33_NATIVE_SHA256_V2.zag`, `substrate/R33_NATIVE_IO_V1.zag`;
root-level `R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` copies exist
because `cl/arm.zag` imports `../R33_NATIVE_SHA256_V2.zag`).
Pure Zag, zero randomness in any decision path, byte-identical reruns.
Built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 0. Authority and corrections (binding)

Controlling authority, in order:

1. `~/workspace/tnn-lab/units/arms/briefs/M2.json`
2. The coordinator's byte-verified frozen row
3. Nothing else from the coordinator

Frozen M2 row (§3 mechanism / binding kill), verified 2026-09-21
(brief and row match byte-for-byte):

- Mechanism: "Counter IDs composed canonically (sorted ascending) for
  multi-span units; max composition depth frozen."
- Binding kill: "Single-byte leaf edit invalidates > 25% of cached
  compositions in the recall benchmark, OR ID recomputation > 10% of
  recall latency on the 10x run."

If the brief and the frozen row disagree: BLOCK and report. They do not.

Two coordinator corrections are acknowledged (both received 2026-09-21):

1. The original variable-length-ID mechanism and recall/swap kill bars were
   a dispatch error and are VOID. They must not influence design, measurement,
   or verdict.
2. The first correction was paraphrased; the second correction supplied the
   authoritative verbatim row and the authority order above. The verbatim row
   governs.

An earlier 10,682-byte variable-length-ID implementation was built under the
void dispatch, then DELETED. It must not influence results.

## 1. Mechanism (frozen)

M2 extends ARM M's counter-ID leaf layer with compositional parent IDs for
multi-span units:

- Leaves: fixed 64-byte chunks, monotonic counter IDs (issuance order).
  The leaf layer is ARM M's `M` struct, renamed to `M2`, with identical
  semantics (A15: PROVISIONAL-PENDING-FREEZE, runs on the leaf counter-ID
  mapping).
- Multi-span units: adjacent live leaves (in ID order) pair into depth-1
  compositions; adjacent depth-1 units pair into depth-2 compositions.
  Odd leftovers remain uncomposed. Maximum composition depth is FROZEN AT 2.
  Deeper composition requests are refused/audited (no depth-3+ construction
  path exists).
- Parent IDs are composed canonically: child IDs sorted ascending before
  encoding, so (A,B) and (B,A) yield the same parent. Original sequence order
  is stored separately from sorted canonical order.

Canonical parent encodings (byte-exact):

- Depth 1: `0x01 || 0x02 || be32(min leaf ID) || be32(max leaf ID)` = 10 bytes.
- Depth 2: `0x02 || 0x02 || lexicographically sorted child SHA-256 IDs`
  = 66 bytes.

Parent ID = SHA-256 of the canonical encoding (32 bytes).

The composition cache stores: parent ID, sorted children, sequence children,
depth, span (offset/length), corpus, and hash-map state. Lookup is by 32-byte
parent ID through an open-addressed hash map (FNV-1a 64-bit over the ID,
linear probing).

## 2. Frozen design choices (pre-result)

All choices below were frozen in the source header BEFORE any M2 arm result
was viewed:

- Max composition depth: 2.
- Deterministic topology: adjacent live leaves in ID order → depth-1;
  adjacent depth-1 → depth-2; odd leftovers uncomposed.
- Canonical encodings as above; parent ID = SHA-256.
- Sequence order stored separately from sorted canonical order.
- Content-changing leaf revision = kill + re-add with a NEW counter ID
  (persistent-identity kill semantics); repair-to-source remains in-place.
- K1 probe: select the leaf referenced by the most cached compositions,
  flip one byte, kill/re-add it, count stale cached compositions.
- K2: parent-ID recomputation + cache lookup time vs total leaf+composed
  recall time on the 10x corpus; kill above 10%.
- A15: PROVISIONAL-PENDING-FREEZE, leaf counter-ID mapping.

## 3. Store layout

`M2` struct = ARM M's leaf arrays plus:

- `comp_cap`, `comp_n`: composition record capacity/count.
- `comp_ids`: 32 bytes per composition (parent IDs).
- `comp_ch0`, `comp_ch1`: sorted child IDs (32B each for depth-2;
  for depth-1, 4B leaf IDs zero-extended in the low 4 bytes).
- `comp_seq0`, `comp_seq1`: sequence-order children (32B each).
- `comp_depth`: u8 per composition (1 or 2).
- `comp_off`, `comp_len`, `comp_cor`: span metadata.
- `comp_map`: open-addressed parent-ID → index map (key 32B + i32 value).
- `comp_mcap`: map capacity (power of two).

Leaf arrays: `offs`, `lens`, `corps`, `flags`, `shifts`, `pidx`, `eps`
(identical to ARM M).

Composition construction (`m2_build_compositions`): pairs adjacent live
leaves globally in ID order. NOTE: in M8 (which ingests prose then code as
separate corpora), this can pair the final prose leaf with the first code
leaf; the span metadata records each composition's corpus explicitly, and
recall resolves through the per-corpus registry. Cross-corpus pairs are
structurally valid (the parent ID commits to child IDs, not byte spans).

Recursive validity (`m2_comp_verify`): recomputes the parent ID from live
children and compares byte-exact; returns 0 (stale) if any child is dead or
the recomputed ID mismatches.

Composed recall (`m2_recall_composed`): map lookup by 32-byte parent ID,
verify, then recall leaves in SEQUENCE order and concatenate.

## 4. M1–M9 integration

- M1 (`t_m1`): ingests corpus, builds compositions, runs the standard M1
  recall + swap probe on leaves, then benchmarks composed recall (all cached
  compositions, byte-exact vs concatenated leaf bytes) and runs the binding
  K1 cascade probe (worst-case leaf edit). JSON fields added:
  `m2_composed_total`, `m2_composed_recall_tenths`, `m2_k1_stale`,
  `m2_k1_total`, `m2_k1_stale_tenths`, `m2_k1_verdict`.
- M2–M7: use the leaf counter-ID layer (compositions built in M1, M8, K2;
  the shared procedures M2–M7 are byte-identical to ARM M's).
- M8 (`t_m8`): ingests prose + code, builds compositions, captures a store
  image that includes the full composition table and hash map. Perturbation
  reruns (frag/aslr/starve) must reproduce the image byte-identically.
- K2 (`t_m2_k2`, modes `m2-k2`/`m2-k2-code`): ingest 1x corpus (10x pending),
  build compositions, then:
  - T_recall: recall all leaves + all compositions (with integrity verify).
  - T_recompute: standalone parent-ID recomputation + map lookup for all.
  - Kill if T_recompute / T_recall > 10%.

## 5. Binding kill criteria (frozen row)

- K1: Single-byte leaf edit invalidates > 25% of cached compositions in the
  recall benchmark → KILLED. (Measured: worst-case leaf = the leaf referenced
  by the most compositions; stale = compositions failing `m2_comp_verify`
  after kill+re-add.)
- K2: ID recomputation > 10% of recall latency on the 10x run → KILLED.

If any applicable 1x or binding criterion kills/disqualifies the arm: STOP,
produce unchanged death evidence (do not bend the prereg).

## 6. Known limitations / open review items

- K2 timing uses syscall 228 (`now_ns`); verify safety under codegen
  constraints. Timing variance observed (33–64% on small corpus); use
  warmup + median for the binding 10x run.
- `eprint(_zag_i64_to_str(...))` does not free the returned strings (minor
  leak in K2 stderr diagnostics; stdout unaffected).
- Cross-corpus composition in M8: see §3.
- Depth-3+ refusal: no explicit public compose-request path yet; the
  constructor only builds depths 1–2.
- Composition coverage: built in M1, M8, K2; M2–M7 exercise the leaf layer.
- M8 image sizing vs 2^25 slice-indexing ceiling: verified by construction
  (composition table ≪ 33M entries at 1x).

## 7. Build

```bash
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  cl/arm.zag -o <out>
```

Run from `units/arms/M2/` (relative import `../R33_NATIVE_SHA256_V2.zag`).
Battery: `~/workspace/tnn-lab/units/arms/harness/run_metric.sh <bin> <mode>
~/workspace/tnn-lab/units/arms/harness/corpora/r1 <workdir>` per leg;
M8 via `m8_gate.sh`. Scratch under `~/workspace`, never `/tmp`.
