# R33-N17 native parent-runtime boundary

Final Lane B refresh: `FINAL_B_20260915_1409/N17_REFRESH/ROW_CLASSIFICATIONS.json`
records 50 fresh native static rows and four independently reviewed inert
equivalents, with 26 source-row blockers. The nine R27 policy rows now have a
hash-bound native parser and tested missing/corrupt refusals. Independent terminal
review is completed/fail-closed; full runtime, fixtures, admission and V91
generation remain unqualified. Isolated reviewed R25 compatibility defects are
repaired, but exact inputs and complete lineage remain blocked. See the final
report for current scope; older counts and unreviewed-descriptor wording below
are historical.

Status: **EXISTING NATIVE STATIC/DIGEST TOOLS FRESHLY EXERCISED; FULL RUNTIME
BOUNDARY NOT QUALIFIED, NOT PREREGISTERED, NOT ADMITTED.**

2026-09-15 Lane B update: `LANE_B_AUDIT_20260915/AUDIT.json` records frozen
native map/view reloads, exact R26/R27 digest matches, 50 source-line static
passes, exact hash-bound R27 policy checks, and unchanged compiler/raw-parent/
map-manifest pins. Canonical R27 remains step 60423, newborn restarts 0.
These are engineering observations, not a mutable parent runtime, scientific
exposure, learner authority, or successor promotion.

The original specification below is historical design text, retained rather
than retroactively rewriting its gates. Its unimplemented-digest/unpopulated-
inventory assertions are superseded by this dated audit. The reserved typed
service, full runtime behavior, negative suite and admission are still not
qualified. The existing R27 tool embeds the previously closed R26 digest text;
this audit independently recomputes and matches that R26 value before accepting
the R27 match. A fused typed service receiving the newly computed R26 output
has not been established. No witness literal is credited as recomputation.

This document defines the smallest native boundary that could safely support a
future R26/R27 continuity qualifier. It is an authoring contract, not an
execution authorization. It does not open the parent, run the current
authoring sentinel, implement a semantic digest, or create a native verifier.

## Evidence boundary

The design is limited to the already-qualified bounded engineering substrate:

- N10's inert, hash-bound parent map and fresh-process paged reconstruction;
- N13A's bounded legacy Torch storage/tensor/parameter views and fresh-process
  inventory replay; and
- the native SHA-256 primitive used by those packets.

N10 evidence establishes structural custody only. N13A evidence establishes a
bounded view/inventory engineering pass only; its native result explicitly says
`semantic_digest_recomputed=false` and `full_parent_migration_verified=false`.
Neither result establishes original behavior, mutable-state continuity,
semantic-digest reproduction, or promotion. The external evidence roots are
immutable inputs to this specification and must be copied or pinned into any
future N17 freeze; live imports are not a freeze.

## Boundary controls

The three controls below are mandatory and are evaluated in order. A later
control cannot repair a failure in an earlier control.

### C0 — custody and source binding

The only parent input is the already-custodied canonical R27 byte stream plus
its N10 map bundle. Before any selector is exposed, a future native process
must validate:

1. the exact raw-parent SHA-256
   `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`;
2. the exact N10 map-manifest SHA-256
   `b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f`;
3. manifest version, page order, complete coverage, page hashes and source
   binding; and
4. reconstructed bytes and inert-map invariants after a fresh-process reload.

The parent bundle, canonical state, registry, review records and governance
files are read-only. A source/hash mismatch returns `REFUSE_SOURCE_HASH` or
`REFUSE_MAP_HASH` and exposes no selector, digest, partial preimage, row count
or continuity disposition.

### C1 — inert typed mapping and bounded views

The boundary exposes data, never historical behavior. The inherited N10/N13A
function shapes are the substrate reference, not an authorization to import a
mutable live tree:

| Operation family | Substrate shape | Required N17 boundary rule |
| --- | --- | --- |
| map construction | `pm_init(input:[]u8,nodes:i32,edges:i32,memo:i32,stack:i32) ParentMap`, then `pm_scan`/`pm_validate` | complete-stream parse and validation before access |
| inert lookup | `pm_kind`, `pm_raw`, `pm_lookup`, `pm_build_state`, `pm_small_int` | selector declares node ID, expected kind, source type and extent |
| numeric view | `ts_open`, `ts_bound`, `ts_at`, `ts_bits`, `ts_row`, `ts_close` | only the reviewed storage/tensor/parameter subset; checked dtype, shape, stride and offset |
| byte hashing primitive | `ns_sha256(input:[]u8,out:[]u8)i32` | substrate control only; not a semantic R26/R27 digest implementation |

Every selector record must carry `selector_id`, source node ID, expected
container/type tag, byte start and length, ordering rule, null/absent branch,
individual input SHA-256 and supported-substrate pin. An unexpected alias,
duplicate selector, unknown type, unsupported reducer/persistent reference,
unbounded extent or implicit conversion is a refusal. No global, reducer,
class, tensor constructor, graph/BPE/VAD mechanism or foreign evaluator may be
invoked.

Required refusal families are stable and non-successful:

`REFUSE_SOURCE_HASH`, `REFUSE_MAP_HASH`, `REFUSE_SELECTOR`, `REFUSE_TYPE`,
`REFUSE_NULL_BRANCH`, `REFUSE_DTYPE`, `REFUSE_SHAPE`, `REFUSE_ORDER`,
`REFUSE_CANONICALIZATION`, `REFUSE_R25_BINDING`, `REFUSE_OVERFLOW`,
`REFUSE_UNSUPPORTED`, and `REFUSE_OUTPUT`.

On any argument or selector refusal, caller-owned output/workspace canaries
must remain unchanged. Limits must be frozen before admission for map nodes,
edges, memo entries, selector count, preimage bytes, numeric elements, JSON
depth, string bytes and wall/resource budget. The existing N10/N13A observed
RSS figures are evidence receipts, not hard containment guarantees.

### C3 — continuity claims and custody separation

The verifier boundary consumes only C0/C1-validated records, reviewed policy
bytes and explicitly admitted native-equivalent fixtures. It emits a typed
record containing `level`, `row_results[]`, `failure_ids[]`,
`historical_witness_used` and `terminal_claim_allowed`.

The semantic-digest service ABI is therefore **reserved but unimplemented**:

```text
digest_r26(validated_views, selector_manifest, r25_binding) -> typed result
digest_r27(validated_views, selector_manifest, recomputed_r26_digest) -> typed result
```

It may publish a separately owned 32-byte digest only after all preimage fields
are finalized, all selector records are exact, and the R25 binding is present.
The retained R26/R27 digest strings are post-construction comparison witnesses,
never preimage inputs. Until those conditions are met, the only valid result is
`NOT_IMPLEMENTED`/`DEFERRED_BLOCKER`; a literal-returning function is invalid.

`historical_witness_used` may document provenance but must never increase native
row counts. Digest equality cannot imply behavioral continuity, complete
mutable-state migration, authority, promotion or R27 superiority.

## Stage gates

| Gate | Required evidence | Current N17 state |
| --- | --- | --- |
| G0 authoring safety | native-only contract, source pins, refusal-only entry point | design/build evidence only |
| G1 / C0 custody | fresh-process map reload, source and manifest binding, immutable input custody | inherited N10 evidence; N17 runtime not qualified |
| G2 / C1 views | populated type inventory, exact selectors, supported numeric layouts and fail-closed controls | schema exists; inventory is unpopulated |
| G3 fixture binding | known-answer bytes, individual hashes, paired negatives and canaries | specifications added; not frozen or executed |
| G4 R26 digest | complete R26 selector/layout closure and R25 raw/digest inputs | blocked; no implementation justified |
| G5 R27/verifier | complete reviewed check matrix and native-equivalent definitions | blocked by unmapped/deferred rows |
| G6 admission | independent review, preregistration, reservation, source freeze and one separate admission | not authorized |

The success ladder remains the one in `DESIGN.md`: identity, R26 digest, R27
digest, required verifier invariants, then full continuity. A higher level is
forbidden while any required lower-level selector, fixture, lineage input or
matrix row remains unresolved.

## Current non-closure

The existing packet still lacks exact selectors and individual hashes for the
R26 numeric/state-dict fields, R27 active-head fields, specialist formatting,
canonical JSON/string/float32 behavior on actual parent values, and the R25
accepted-state/source inputs. The fixture specifications intentionally record
those as pending rather than inventing bytes. Consequently this boundary
advances authoring documentation only: it authorizes no digest/verifier code,
no compile step, no preregistration and no execution.

2026-09-15 final Lane B correction: `FINAL_B_20260915_1409/ROWS.json` now accounts for all 80 source rows: 50 fresh native static passes, four independently reviewed native inert identity/exact-class equivalents freshly replayed, and 26 reviewed fail-closed source rows (R27 5; R26 21). V91 custody matches all 16 oracle strings but native inference generated zero strings; exact method/input bindings remain absent. Stable compiler rebuilds pass. Reviewed isolated R25 compatibility import/constant/allocator correction passes fresh native tests, while actual exact inputs and complete lineage remain blocked. New native policy parser and fused digest adapter are author-verified; independent adapter review pending. Earlier counts/import/compiler blockers above are historical and superseded for this narrow scope. No full continuity, learn, authority, exposure or promotion. See `FINAL_B_20260915_1409/FINAL.json`.
