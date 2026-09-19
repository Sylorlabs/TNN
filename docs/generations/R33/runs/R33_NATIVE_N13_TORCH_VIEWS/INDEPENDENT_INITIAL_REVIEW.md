# R33 N13 independent initial engineering review

Date: 2026-09-06.

Disposition: INITIAL STATIC REVIEW ONLY. PREREGISTRATION IS NOT APPROVED.
Final source, native fixture builder/evaluator, design, dependency closure and
execution bounds must receive a separate final review before any approval.

## Scope and evidence

Read `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` first. Read both N13
source files completely, followed by the complete six-file dependency closure
listed below. Consulted selected portions of the saved official PyTorch v2.9.0
reference text; that version is a semantic reference, NOT an identification of
the continuing parent's historical PyTorch version.

This review used filesystem inspection and artifact hashing only. No Python,
runtime imports, stored reducers, compiler, tests, primary run, training or
registry writes were performed. No consumed N12 work was rerun. The sole file
written by this reviewer is this report; no implementation was changed.

The native fixture builder was appearing concurrently during review; its
contents and the eventual evaluator/design are not included in this initial
review. Findings below concern the two exact N13 source versions identified
here, not an assumed final source freeze.

All paths in the hash tables are relative to
`/Users/Shared/micah/Documents/TNN/TNN/`. Both N13 source hashes matched before
the full-file reads and again after dependency/reference inspection.

### SHA-256: implementation and contract

| File | SHA-256 |
| --- | --- |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/storage.zag` (all 101 lines) | `9573dc64bee4383415d69a7e9cbbf344370d858a76ca7c95af07572867994aff` |
| `Research/R33_NATIVE_N13_TORCH_VIEWS/tensor.zag` (all 127 lines) | `88a6c26d8263daae3bdc635d32d323ae093cd86c2a8546df3b908bf3f065b905` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/views.zag` (all 220 lines) | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| `Research/R33_NATIVE_N11_PARENT_CUSTODY/binding.zag` (all 53 lines) | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` |
| `Research/R33_NATIVE_N10_PARENT_MAP/inert.zag` (all 237 lines) | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` |
| `Research/R33_NATIVE_N10_PARENT_MAP/mapio.zag` (all 117 lines) | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` |
| `Research/R33_NATIVE_IO_V1.zag` (all 118 lines) | `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` |
| `Research/R33_NATIVE_SHA256_V2.zag` (all 89 lines) | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` (all 40 lines) | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` |

The six dependency digests also match the corresponding source entries in
the existing `Research/R33_NATIVE_N12_PINS.sha256`; those entries were inspected,
not regenerated. This is a source-identity observation, not a new N12 execution
or a qualification of an eventual N13 staged build/import resolution.

### SHA-256: saved semantic references

Reference paths below are under `Research/R33_NATIVE_N13_TORCH_VIEWS/REFERENCES/`.
Hashes identify whole files; only the stated semantic portions were read.

| File | SHA-256 | Portions consulted |
| --- | --- | --- |
| `torch_v2_9_0_serialization.py.txt` | `7fe6755ba65409b510e75e0435a33f444c893a82ea817ff618a5be5943298a3c` | Constants at 55-68; legacy saver at 985-1145; persistent loader and record sequence at 1720-1845. |
| `torch_v2_9_0_storage.py.txt` | `ed06de01cc398ad7f428b472049f07944ae892aa1a10d88bd66bba97de4bc785` | Storage reduction at 238-258 and 1233-1255; `_load_from_bytes` at 528-540. |
| `torch_v2_9_0_utils.py.txt` | `b52db634d2378395685499de1fbb2b3a1bef21bb87677d830792179b492edc75` | Tensor rebuilding/hooks at 170-247; parameter rebuilding at 472-506. |
| `torch_v2_9_0_serialization.cpp.txt` | `e960f3d18debb8642bcbdc6612831e0f67876a63647b3727e1cb86edda006d35` | Raw storage writer at 234-310 and reader at 323-369. |

## Findings requiring disposition before final approval

### F1 — P2: resource failures lose their cause in public read/refusal paths

Evidence: `storage.zag:46-50`; `tensor.zag:85-110,112-126`;
`inert.zag:31-38,60-78,100-109`; `R33_NATIVE_SHA256_V2.zag:28-39`.

The return-value ambiguity is concrete, although its effect on the unfinished
evaluator cannot yet be assessed:

- `ts_record` maps every scan/validation failure to `-9101`, including frozen
  scanner capacity failure `-8805` (nodes, edges, memo or stack), whereas initial
  allocation failure is separately reported as `-9107`.
- `ts_bound` calls `ts_open` again. Any failed reopen, including `-9107`, becomes
  boolean failure. A subsequent `ts_at`/`ts_bits` reports `-9105`, the same result
  used for invalid coordinates; `ts_row` reports `-9106`.
- A SHA scratch-allocation failure during `ts_row` is also collapsed into
  `-9106`, rather than remaining distinguishable as a resource failure.

All these paths fail closed; this is not evidence of an out-of-bounds read.
The qualification risk is attributing a refusal to the intended malformed-input
or coordinate control when the actual cause was capacity/allocation failure.
Checking only "negative status" is insufficient, and checking the existing
accessor status alone cannot always distinguish those causes.

Minimal disposition: preserve failure provenance in an N13 result/diagnostic
path, or otherwise make cause-ambiguous qualification outcomes inconclusive.
Specify the error taxonomy in the design. Negative controls must identify the
intended failing stage and must not count unrelated resource failures as passes.
Keep the frozen N10/N12 dependencies unchanged. No fix was implemented here.

### F2 — P2: repeated parsing and whole-storage hashing need aggregate work limits

Evidence: `tensor.zag:59,61,85-110,123-125`; `storage.zag:46-50,69-98`;
`inert.zag:15-18,31-35`.

Every successful `ts_bits` access reaches `ts_bound`, which reopens the view,
lexes/scans/validates five fresh header maps, and allocates two shape arrays.
For the fixed capacities in this source, that is 5 x 7 + 2 = 37 allocations
and 153,728 bytes of explicitly zero-initialized word arrays per successful
binding recheck, before accounting for allocator overhead. These figures are
derived from source, not measured performance.

`ts_row` additionally hashes both the entire containing storage blob and the
entire raw storage payload for each row. Many tensor/parameter descriptors may
legitimately share one storage. Thus a 16 MiB input limit is not a 16 MiB limit
on aggregate bytes hashed or a modest bound on all element-access work.

This is a design/evaluator obligation, not an observed timeout or a demand to
rewrite the interpreter. Freeze finite budgets for views visited, coordinate
reads, rows emitted, cumulative bytes hashed and retained output allocations,
plus the native process limits. Budget exhaustion must stop with an explicit
partial/refused outcome, never silently omit work or count as successful
qualification. A fixed, bounded coordinate sample is sufficient if the design
claims sampled evidence only. No timing or stress experiment was performed.

## Semantic boundaries that must be explicit

The current source implements a restricted serialized view, not general Torch
loading or reconstruction. Preserve these distinctions in the final design:

- `storage.zag:20-50` limits each protocol-2 record to 4,096 bytes, 1,024 lexical
  tokens after PROTO, and 256 bytes across the two GLOBAL lines. Scanner
  capacities are 128 nodes, 256 edges, 128 memo slots and 64 stack/mark slots.
  These are additional admission limits, not proof that every otherwise valid
  protocol-2 encoding is supported.
- `storage.zag:70` compares the exact ten-byte LONG representation of the magic
  number. The type/key/device/None and one-key-list restrictions are also
  intentionally narrow. Unsupported equivalent encodings must not be labeled
  corrupted historical data without further evidence.
- `tensor.zag:50-77` additionally limits every dimension, stride and offset to
  16,777,216, limits nonempty logical element count to that value, and requires
  `offset <= storage_count` even for empty tensors. Freeze that empty-offset
  policy and test its boundary; this review does not establish equivalence with
  every zero-size view accepted by Torch's underlying `set_` implementation.
- Zero strides and overlapping nonnegative-stride views are admitted. `ts_at`
  returns a storage ELEMENT index, not a byte offset or a flattened logical
  tensor index. `TsView.bytes` and the row's payload digest describe the WHOLE
  storage, not only the tensor's occupied elements or bounding span.
- Storage-only views use rank one and normalize the empty storage stride to
  zero (`tensor.zag:64`). Tensor views retain serialized strides even when empty.
  These conventions must not be confused with recovered runtime object state.
- The saved v2.9.0 helper has optional tensor metadata, but N13 intentionally
  admits exactly six tensor arguments and three parameter arguments with empty
  hooks. Seventh-argument metadata, other rebuild helpers, storage views,
  unsupported types/devices and nonempty hooks remain outside this candidate.

## Static observations supporting the current approach

No additional concrete in-scope bounds or ownership defect was established in
the reviewed versions. This statement is limited to source inspection and the
live, immutable, validated-map/single-owner preconditions.

`ts_prefix` consumes length-delimited operands and both GLOBAL lines before
recognizing STOP, then `ts_record` scans and validates the exact slice. The
frozen scanner requires STOP to end that slice with one result and no open
MARK. Header metadata is not used as a license to execute saved code.

The five-record sequence, magic, version, storage PID tuple and trailing
eight-byte element count agree with the consulted legacy serialization source.
The `type_sizes.long == 4` check is consistent with the reference's `Struct("=l")`;
it should not be changed merely because a host C long may have a different size.
The C++ reference writes little-endian storage/count data; requiring a true
little-endian sysinfo flag is an additional intentional N13 restriction.

`ts_decode:99` requires the raw byte count to consume the remainder exactly.
Successful temporary header maps are closed before advancement; failure paths
close allocated maps. Returned offsets point into the still-live input blob,
not into freed temporary node/edge allocations.

`ts_open:63-77` detects zero axes before multiplying dimensions. For a nonempty
view, the incremental greatest-index check keeps each nonnegative stride
contribution within `storage_count - 1`. Rank zero has one logical element and
still requires a valid storage offset. Empty views have no valid coordinates.
Width/count caps then keep subsequent byte addressing within the decoded raw
payload under the stated map preconditions.

`ts_fail` releases both owned shape arrays, including partial allocation;
`ts_bound` releases its temporary successful view; `ts_row` returns a separate
owned buffer and frees it on hashing/serialization failure. The underlying
allocators zero the unused shape slots and reserved row bytes. No caller-owned
output buffer is used to overwrite map/input memory.

## Minimum controls for the final native design/evaluator

These are review requirements for the main author's new bounded N13 design,
NOT executed experiments or permission to run anything before final review.

| Area | Required controls |
| --- | --- |
| Record framing | STOP-valued bytes inside allowed length-delimited and GLOBAL operands; truncation at opcode/length/operand/STOP boundaries; oversized lengths; wrong protocol; missing/extra records; forbidden executable opcodes in headers; per-record memo reset; correct lexical boundary followed by an invalid stack/memo/root; documented capacity refusals distinguished from other failures. |
| Storage semantics | Positive cases for all eight names/widths including zero and nonzero counts; exact magic/version/sysinfo; wrong module/type/device/endian/type-size; mismatched PID/key-list key; zero/oversized/non-ASCII key; non-None storage-view metadata; multiple storage identities; signed/overflow/count mismatch; short payload and trailing bytes. Raw payload containing opcode-like bytes must remain raw. |
| Tensor/parameter grammar | Storage one-argument, tensor six-argument and parameter three-argument forms; exact empty OrderedDict hooks; bad arity, extra metadata, BUILD/state/nonempty hooks and other rebuild names refused; separate tensor/parameter gradient flags, all Boolean combinations on supported floating storage, and gradient-bearing integer/Boolean refusal. |
| Addressing and bits | Rank zero and ranks one through eight; rank nine refusal; negative and over-limit dimensions/strides/offsets; zeros at different axes; explicit empty-offset boundary; contiguous, transposed, gapped, overlapping and zero-stride layouts; exact last valid address and one-past failures; wrong coordinate count and per-axis bounds. Pin expected storage indices and raw low/high words independently of `ts_open`/`ts_at`/`ts_bits`, including high-bit patterns and all eight bytes for 64-bit values. |
| Ownership and rows | Successful and partial-allocation cleanup; closed-view refusal using the actual cleared handle; wrong live-map association; independently owned rows, documented zero-reserved bytes and all three hash ranges; unchanged input/map bytes; no inference of alias identity solely from equal keys or equal payload hashes. No arbitrary-pointer, reuse or concurrent-writer campaign is requested. |
| Evaluator integrity | Independent expected fixture values rather than the interpreter serving as its own oracle; exact branch-specific refusal accounting; F1/F2 disposition; finite aggregate budgets and authorized output paths; complete final source/dependency/compiler/target/design pins. Any failure or unperformed item remains explicit. |

## Handoff

Initial review is complete for the listed source hashes. Main-author source
changes, the completed native fixture builder/evaluator, and the final design
require a subsequent final-review request. There is no preregistration,
launch, training, behavioral-reconstruction or scientific approval in this
report. N12 remains consumed; this review authorizes no repeat execution.
