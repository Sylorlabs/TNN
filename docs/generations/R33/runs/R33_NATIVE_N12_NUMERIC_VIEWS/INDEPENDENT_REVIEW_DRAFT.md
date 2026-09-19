# N12 independent engineering review — initial source snapshot

Date: 2026-09-06. Disposition: **INITIAL STATIC REVIEW; NOT FINAL PREREGISTRATION APPROVAL.**

The execution contract was read first. This review inspected source text, inert reference text, directory inventories, and SHA256 identities only. No tests, experiments, Python, reducers, compiler probes, parent reconstruction, or evaluator were executed. The sole reviewer-authored file is this draft; registry, implementation, frozen dependencies, and canonical files were not changed by this reviewer.

The main agent was editing concurrently. The reviewed 104-line `views.zag` had SHA256 `7758ba82368a4b9830ce99eec26128db39737d75f414b48fb02db2badcd24b35` on repeated reads. Before writing this draft, the working file changed to `e4830465217bdd6cca04249027df27c695c394271fc013ab1235d1a72afe2559`. **That replacement was hashed but not reviewed.** The main agent's `AUTHORING_INITIAL_V1/views.zag` retains the exact reviewed hash, so all N12 line references below refer to that preserved snapshot. Findings are not assertions that the replacement still contains them. No N12 evaluator was available at initial source inspection. A `driver.zag` appeared during final draft verification; its contents were not reviewed, and its presence does not establish a final evaluator freeze.

## Reviewed source identities

All paths are under `/Users/Shared/micah/Documents/TNN/TNN/`. Hashes identify whole files; reference inspection focused on the relevant routines, not every unrelated NumPy routine.

| Source | SHA256 | Inspection scope |
| --- | --- | --- |
| `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` | Complete contract, read first. |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/views.zag` at review capture; preserved as `Research/R33_NATIVE_N12_NUMERIC_VIEWS/AUTHORING_INITIAL_V1/views.zag` | `7758ba82368a4b9830ce99eec26128db39737d75f414b48fb02db2badcd24b35` | Complete 104-line initial implementation. |
| `Research/R33_NATIVE_N11_PARENT_CUSTODY/binding.zag` | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` | Complete file. |
| `Research/R33_NATIVE_N10_PARENT_MAP/inert.zag` | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` | Complete file. |
| `Research/R33_NATIVE_N10_PARENT_MAP/mapio.zag` | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` | Complete file. |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/REFERENCES/numpy_v2_3_5_numeric.py.txt` | `fc3727bd7bbaa1a1d74a2f50f8157dc86cdfc7bb5cf620b1ebdafd3272439b98` | Inert `_frombuffer`, lines 1957–1961, and surrounding context. |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/REFERENCES/numpy_v2_3_5_descriptor.c.txt` | `a362cbc09924b4b019706e0a7b766fbb37b3e1cd6b85a1c3ef27d0038f2fa5f9` | Inert dtype reduction and state decoding, principally lines 2690–3035. |

Supporting inspection: `Research/R33_NATIVE_IO_V1.zag`, SHA256 `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` (allocation/zeroing/free and nearby substrate); `Research/R33_NATIVE_SHA256_V2.zag`, SHA256 `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` (source-level row-digest dependency inspection, not cryptographic certification); and `Research/R33_NATIVE_N11_PINS.sha256`, SHA256 `552b223f64956d0f366c3525b2ef046f04616926abbbb7729bb9027e000acb20`. The inspected pin entries agree with the reviewed binding/inert/mapio hashes. Existing N10/N11 review and N11 freeze documents were read as historical context, not accepted as new execution evidence.

## Additional findings

### F01 — P1: A view is not bound to the map used to read or export it

Evidence: [initial views.zag:6](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/AUTHORING_INITIAL_V1/views.zag:6), `nv_open` at line 62, `nv_bits` at line 85, and `nv_row` at line 94.

`NvView` records IDs and byte offsets but no owner identity. `nv_bits(p, v, index)` checks status and input extent, not whether `p` is the map from which `v` was opened. `nv_row` likewise combines view metadata with a digest and opcode position obtained from the supplied map. Two live synthetic maps with the same offsets and sizes but different payloads provide a concrete static witness: open the view from A, then supply B to either operation. The code can return B's bits, or a row mixing A's metadata with B's bytes, without a binding failure.

Required correction: define and enforce the map/view association at every operation that reads map data. A supported solution can use a stable owner/generation identity plus validated descriptor/range invariants, or another explicit immutable-owner design. Binding only `node`, length, or offset is insufficient. Pointer equality alone does not establish lifetime across close/reallocation or detect mutation of backing bytes.

This is distinct from parent custody: [binding.zag:49](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N11_PARENT_CUSTODY/binding.zag:49) validates a fixed binding, manifest/raw hashes, and parent identity during `pb_load`. Merely importing that file does not make every `ParentMap` passed to `nv_open` custody-approved. Keep synthetic-map admission separate from the production parent-custody path; bind any exported collection to its source/map identity outside the individual payload digest.

### F02 — P1: Row export can reach an out-of-range raw slice after map close

Evidence: initial `views.zag` lines 94–103; [mapio.zag:72](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N10_PARENT_MAP/mapio.zag:72); [inert.zag:27](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N10_PARENT_MAP/inert.zag:27).

Open a nonempty view, keep its dimensions/strides live, close its map, then call `nv_row`. Closing resets the map and frees the loaded raw storage, but the row function never checks `p.status` or the stored byte range against the current input before constructing `p.input[v.at..v.at+v.bytes]`. Its initial view and output-size checks still pass. The concrete defect is reaching an invalid slice instead of a defined refusal; whether that traps or accesses invalid memory depends on compiler/runtime behavior and was not tested. The initial `nv_bits` does reject this particular closed-map case through its map-status check, so this finding should not be generalized to that function.

Required correction: validate live owner/map status and subtraction-based range bounds before any raw slicing or map-derived access in row export. Closed-map, failed-map, and wrong-map calls must leave the output unchanged and return a declared failure status. Explicitly distinguish a view's own allocations from its borrowed map data.

### F03 — P2: Tuple validation accepts malformed termination; aggregate edge counts are not ownership proof

Evidence: initial `views.zag` lines 16–21 and tuple consumers at lines 43, 51, 64, 67; [inert.zag:213](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N10_PARENT_MAP/inert.zag:213).

`nv_tuple_size` trusts the stored count. `nv_item` returns the requested target before validating the chain's final successor or recorded tail. Full count/tail validation in `pm_validate` covers some malformed shapes, but does not eliminate this defect: its traversal uses `while(edge > 0)` and does not require the terminating value to equal zero. Changing a valid tuple's last successor from zero to -1 leaves its visited count and tail unchanged and can pass that validator. An empty tuple with count/tail zero and head -1 can also pass. N12 then accepts these noncanonical chains.

Required correction: validate the complete bounded tuple chain, including exact arity, valid target IDs, item-only operation 1, zero second operand, strictly increasing valid edge IDs, exact tail, and **exact zero termination**. An empty tuple requires both head and tail zero. Check the representable range of wide fields before narrowing where the admission boundary permits in-memory malformed maps. Do not patch the frozen N10 file as part of N12; add the needed N12 admission checks or explicitly tighten the accepted-map boundary.

The inherited `total == edge_count` condition also does not prove unique edge ownership. For example, owner A visiting edges 1 then 3, owner B visiting edge 3, and unvisited edge 2 gives three visits for three stored edges. This is a validator limitation for arbitrary constructed maps, not evidence of corruption in the hash-bound parent bundle. If unique edge ownership is claimed, validate it explicitly. Shared **member node IDs** through memo references are legitimate and must not be confused with shared edge records.

### F04 — P2, conditional admission defect: Invalid LONG byte spans can become a successful integer zero

Evidence: initial `views.zag` lines 31–32; [inert.zag:84](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N10_PARENT_MAP/inert.zag:84) and line 208.

`pm_raw` returns an empty slice for an invalid span. `pm_small_int` treats a kind-4 node whose returned slice is empty as integer zero and returns success. Thus a malformed or subsequently modified in-memory LONG node can be accepted as a zero shape axis or zero dtype flags. A valid zero-length LONG also denotes zero, so raw-access failure and valid empty encoding must remain distinguishable.

Required disposition: either establish and enforce that every admitted map has validated, immutable raw spans for the entire view lifetime, or explicitly check integer-node bounds before calling the helper. `p.status == 0` alone does not establish that invariant. `mi_load` does perform `pm_validate` before success, so this finding is **not** a claim that a bad raw span bypasses the frozen, hash-checked loader.

For valid spans up to eight bytes, the inspected signed LONG decoder starts from the sign and accumulates from the most significant byte. No additional signed-64 overflow defect was identified in that valid-input path. The greater-than-eight-byte refusal is a subset limit that must be declared, including redundant sign extension; no compiler execution verified the arithmetic.

### F05 — P2, admission-policy issue: Empty-shape acceptance depends on where the zero axis appears

Evidence: initial `views.zag` lines 70–76.

The product loop applies its 16,777,216 ceiling before discovering later zero axes. With a zero-byte buffer and C order, `(4096, 4097, 0)` refuses at the second dimension because its prefix product is 16,781,312. `(0, 4097, 4096)` passes the product and stride calculations; its largest element stride is 16,781,312, which still fits the signed-32 row field. Both have zero elements, allowed individual dimensions, and representable stored strides. This asymmetry is separate from the already identified stride-overflow defect.

Required disposition: freeze whether the limit intentionally applies to every left-to-right prefix, or instead to final element/byte count with a separate stride-representability rule. Under the latter interpretation, validate all axes first, determine emptiness without overflow, then construct bounded strides. Never allow finding a zero to skip validation of later negative, malformed, or excessive dimensions. A conservative prefix restriction may be an explicit supported-subset choice, but cannot silently be presented as an element-count limit.

## Known fixes and interpretation/lifetime boundaries

The following are requirements for re-review, not newly discovered claims against the main agent's pending fixes.

**Output aliasing:** staging the row does not stop the final copy from overwriting protected storage. Check the actual destination write interval against raw input, map tables, and view dimension/stride storage, not just the selected payload. Include partial overlaps and disjoint adjacent slices. If structure-storage aliases are within the supported API, protect those too. Aliasing refusal must precede any output mutation. This was already identified by the main agent.

**Stride bounds:** both arithmetic and on-disk representation need bounds. The initial `(0, 65536, 65536)` C-order view has zero elements but a first element stride of 4,294,967,296; `nv_open` accepts it, whereas `mi_put` cannot encode it in the signed-32 row field. `(0, 16777216, 16777216, 16777216)` also requires a mathematical intermediate of 2^72 in C-order stride construction. Prevent multiplication overflow and decide whether empty-array strides are canonical bounded values or grounds for explicit refusal. Do not defer a supposedly exportable view's layout failure to `nv_row`.

**Units and empty layouts:** the initial strides are in elements, not bytes, and `nv_at` returns an element index. For width 4 and shape `(2,3)`, this API's C/F strides are `(3,1)` / `(1,2)`; byte strides would be `(12,4)` / `(4,8)`. State the unit in the record contract. Empty and singleton-axis layouts need a declared N12 convention, not an assertion that their exact stride tuple reproduces NumPy's in-memory object. NumPy's documentation defines ndarray strides in bytes and notes that empty/singleton-axis strides need not be unique; see the supplementary references below.

**Byte order and bits:** the inert descriptor reference supports the plain version-3 state `(3, endian, None, None, None, -1, -1, 0)` and constructor arguments `(kind-width text, False, True)`. Its reduction code converts native `=` into an explicit endian marker. Rejecting `=` rather than guessing the host order is therefore a defensible strict serialization-subset rule. `nv_bits` performs byte-wise interpretation and returns two unsigned-valued 32-bit limbs held in i64 slots. It does not return a signed integer, floating value, or normalized Boolean. The inspected per-limb accumulation stays within 0..4,294,967,295 for valid widths. Preserve NaN payloads, negative zero, and noncanonical Boolean bytes without arithmetic conversion. A raw-byte digest must hash original bytes, not endian-normalized limbs.

**Readonly is not authority:** the `readonly` field distinguishes serialized bytes from bytearray. A value of zero must not grant a writable N12 operation or permission to alter parent storage. The initial API exposes only reads/metadata output; its mutable backing allocations are not made immutable by that field.

**Ownership and lifetime:** `nv_close` frees the two allocated slices; a shallow struct copy duplicates their pointers, not ownership. Closing one copy leaves the other dangling, and closing both can free the same allocations twice. The same general issue applies to shallow copied maps. Either prevent/manage this with an explicit ownership mechanism or make single ownership, noncopying, no concurrent mutation, and map-outlives-view requirements explicit. Do not claim arbitrary stale-pointer safety. Repeated close of the same cleared variable is different from closing shallow copies. The initial close preserves status zero for a formerly successful view even after clearing its storage; a distinct closed status would make the lifecycle less misleading.

**Reference scope:** the supplied inert `_frombuffer` reference also has optional `axis_order` and a `K` branch. The requested N12 subset is four positional arguments with C/F order; refuse the fifth-argument and K forms rather than silently ignoring them. Reference filenames were preserved as supplied. Their exact upstream release provenance was not independently established here; attempts to retrieve the tagged GitHub text were unavailable. These local hashes identify what was actually inspected.

## Required positive and negative native controls — not executed

These are proposed controls for a newly frozen native Zag evaluator. Author fresh synthetic fixtures; do not rerun consumed historical controls, generate expectations with Python, execute reducers, or use the protected parent as a corruption fixture. Expected values must be fixed independently of the implementation under test. Every negative assertion must check the precise declared failure/disposition and unchanged output/protected preimages, not merely that the process exits.

| Control family | Required positive cases | Required negative or boundary cases |
| --- | --- | --- |
| Symbol and call subset | Each explicitly allowed `_frombuffer` module spelling; each explicitly allowed dtype module spelling; exactly four frombuffer arguments. | Wrong module/name, non-REDUCE node, wrong argument kind/arity, a fifth `axis_order`, C/F alternatives such as A/K, additional BUILD or container mutation on the frombuffer result. Classify unsupported separately from a successful view. |
| Dtype grammar | All 11 forms: i1/i2/i4/i8, u1/u2/u4/u8, f4/f8, b1. Exact Boolean constructor flags; one BUILD; exact eight-item version-3 state. Exercise every admitted endian/width combination, including width-1 policy. | f2, complex, object, structured/subarray, strings/void/datetime, invalid widths or extra text; integer 0/1 substituted for Boolean constructor flags; incorrect state version/arity, metadata/fields, flags, size/alignment, missing or repeated BUILD; `=`, unknown endian, and multibyte `\|`. |
| Tuple integrity | Empty tuple with zero head/tail; exact arities 3, 4, 8; repeated member IDs through memo references. | Negative head/next, nonzero final next, cycle/backward/out-of-range link, mismatched tail/count, extra/truncated chain, wrong edge operation/second operand, invalid target, wide-to-narrow field wrap where admissible. Include negative-terminator cases that the inherited validator does not reject. Test edge sharing separately from legitimate shared members. |
| Shape integers | BININT/BININT1/BININT2 and valid LONG encodings around 0, 127/128, 255/256, and the declared dimension ceiling; genuine empty LONG as zero; sign-extended encodings within the declared width. | Negative/inferred -1 dimensions, Boolean/float/text dimensions, one above the dimension ceiling, i64 extrema as out-of-range dimensions, greater-than-eight-byte LONG under the chosen subset, invalid raw spans distinguished from valid empty LONG. Decoder boundary expectations must not require accepting those extrema as dimensions. |
| Shape and indexing | Scalar `()` has one element and index `[]` maps to zero; singleton axes; rank 8; nontrivial `(2,3)` in C and F. Coordinate `(1,0)` maps to element 3 in C and 1 in F. | Rank 9, wrong coordinate count, negative or axis-equal coordinates, flat index -1 or `elements`, list/non-tuple shape, mismatched payload size. Scalar with zero bytes must refuse; an empty array must reject every element access. |
| Empty arithmetic and export bounds | Zero at first/middle/last axis; multiple zeros; both C and F; all later dimensions still validated. Freeze expected outcomes for `(4096,4097,0)` and `(0,4097,4096)`. | `(0,65536,65536)` and its order/axis variants exercise signed-32 stride representation; the 2^72 example exercises pre-multiplication refusal or bounded empty canonicalization. Negative or excessive axes after a zero still refuse. Test allocation/raw-file ceilings without accidentally making a nominal positive serialized fixture exceed N10's whole-input limit. |
| Raw buffer and provenance | In-band bytes and bytearray produce the declared provenance flag without changing input; exact byte extent, including an empty span at a valid endpoint and unaligned starts. | Text, external buffers, readonly wrappers around external references, negative/out-of-range spans, short/trailing/indivisible byte lengths, overflow-adjacent metadata, failed map status. Do not infer support for opaque tensor/storage records. |
| Endian and integer bit patterns | LE bytes `08 07 06 05 04 03 02 01` and BE bytes `01 02 03 04 05 06 07 08` both give low `0x05060708`, high `0x01020304`. Include every width, all-zero/all-ones, alternating bits, and the 64-bit high bit: low 0, high `0x80000000`. | Wrong endian metadata must change the nonsymmetric interpretation or be rejected under the grammar, never silently normalize input. All-ones u8/i8 yields two `0xffffffff` limbs, not a signed-i64 oracle overflow. |
| Float/Boolean raw fidelity | For f4/f8, explicit bytes for positive/negative zero, infinities, smallest subnormal, and multiple quiet/signaling NaN payload patterns; Boolean bytes 0, 1, 2, 0x80, 0xff remain exact bytes. | Fail any expectation that canonicalizes NaNs, loses zero's sign, sign-extends limbs, or normalizes Boolean raw bytes. Floating equality is not an adequate oracle. No floating computation is necessary. |
| Row contract and aliasing | Exactly 160 bytes written; larger output preserves its suffix; reserved bytes and unused axes have fixed values; all stored fields and original-byte SHA checked independently; adjacent nonoverlapping output succeeds. | Output length 159; partial/full overlap with input including descriptor bytes outside the viewed payload, map tables, dimensions, or strides; failed digest/allocation/validation leaves output unchanged. Repeat negatives against a previously filled output so stale success cannot be mistaken for new output. |
| Binding and lifecycle | Same live owner; multiple distinct views with explicit ownership; close/reopen through the supported lifecycle. | A's view with same-sized B, closed/failed map, closed view, changed descriptor/backing data if mutation detection is promised, and a new allocation at a reused owner address if generation protection is promised. Do not deliberately dereference freed shallow copies as a substitute for implementing or documenting the ownership boundary. |
| Resource/failure paths | Bounded opens, exports, closes, and declared fixture limits. Account for both view allocations and row/digest temporary storage. | First/second view allocation, row allocation, and digest allocation failures through an authorized native failure-injection design; no partial output or leaked live ownership. Freeze timeout, output, allocation, and child-process bounds before exposure; no unregistered runtime probes. |

For C/F controls, use asymmetric dimensions and distinguishable bytes: a coordinate that maps to the last element in both orders is not enough. For tuple and integer corruption controls, identify whether the production loader or N12 boundary is expected to refuse; do not accidentally bypass the boundary in the evaluator and then credit a different layer with the result.

## Final-source re-review gate

This draft does not approve preregistration, execution, or promotion. The next independent review must receive the final N12 source **and** native evaluator, fixture/oracle definitions, source/import/compiler/target/OS-adapter closure, allowed filesystem effects, and resource bounds. Reconcile each finding against the final source hash and verify that the evaluator actually asserts the proposed invariants. Hashes of replacement sources are not evidence that the fixes work.

The final review must also establish the intended custody admission and ownership lifetime contract, record format/stride units, empty-axis rule, error/status meanings, and reference provenance. Retain the frozen N10/N11 sources and distinguish any new N12 wrappers or corrections from those inherited artifacts.

No original-behavior recovery, tensor coverage, training readiness, security certification, or R33 completion is claimed. Stop here and await an explicit final-source re-review request; no background monitoring or execution is authorized by this draft.

## Supplementary documentation consulted

Official NumPy documentation was read only for interpretation terminology, not as a runtime oracle or replacement for the hashed inert references:

- NumPy 2.3 `numpy.frombuffer`: non-native endian interpretation without byteswapping the underlying bytes; buffer-backed view semantics. `https://numpy.org/doc/2.3/reference/generated/numpy.frombuffer.html`
- NumPy 2.3 `numpy.ndarray.strides`: stride units are bytes. `https://numpy.org/doc/2.3/reference/generated/numpy.ndarray.strides.html`
- NumPy 2.3 `numpy.reshape`: C/F indexing orders and broader accepted shape/order forms, which this strict subset need not support. `https://numpy.org/doc/2.3/reference/generated/numpy.reshape.html`
- NumPy ndarray reference: empty/singleton-axis strides are not uniquely constrained by indexing. `https://numpy.org/doc/stable/reference/arrays.ndarray.html` (consulted 2026-09-06; explanatory documentation, not a pinned implementation dependency).
