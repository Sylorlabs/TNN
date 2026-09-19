# N12 strict numeric-view engineering design

Status: pre-execution design, subject to independent final-source review.
Identity: `r33-native-n12-strict-numeric-views-v1`. This file is not a reservation,
preregistration, execution grant, original-behavior recovery, or R33 completion.

## Question and boundary

Can native Zag interpret a declared subset of retained serialized numeric-array
descriptors, preserve their original numeric bit patterns, refuse unsupported or
malformed forms, and reproduce a source-bound read-only inventory in a fresh
process without executing the historical language or changing the parent?

The accepted R27 parent remains step 60423, zero newborn restarts. No learner,
optimizer, graph/BPE/VAD machinery, constructor, reducer, original method,
scientific world, human credential, or new authority is introduced. The fixed
N10 map and original bytes are known engineering comparison material, not fresh
generalization evidence. N10/N11 primaries and frozen source remain untouched.

This advances numeric storage interpretation beyond the prior opaque map.
It does not establish tensor/storage completeness, historical NumPy version,
original inference or update behavior, semantic-digest equivalence, full parent
migration, sensing, protected runtime authority, learning, or promotion.

## Supported descriptor grammar

The input is a live, immutable, validated `ParentMap`. Actual-parent inventory
must load through the unchanged N11 `pb_load`, which binds N10's manifest, every
map page, all original bytes, and accepted structural identity. Synthetic
controls enter through the unchanged native inert scanner and validator. Merely
importing `binding.zag` does not authorize a caller-created map.

Only a REDUCE descriptor for `numpy._core.numeric._frombuffer` or
`numpy.core.numeric._frombuffer`, with exactly four positional arguments and no
subsequent mutation, is accepted. Arguments are an in-band bytes/bytearray
carrier, supported dtype, shape tuple, and C/F order. External buffer references,
object construction, additional BUILD operations, fifth arguments, A/K order,
arbitrary strides and other reducers remain unsupported.

Dtype is a REDUCE for `numpy.dtype` or
`numpy._core._multiarray_umath.dtype`, with the exact constructor tuple
`(kind-width text, False, True)` and exactly one eight-field version-3 state
`(3, endian, None, None, None, -1, -1, 0)`. Supported kind-width forms are
i1/i2/i4/i8, u1/u2/u4/u8, f4/f8, and b1. Endian is explicit `<` or `>`;
`|` is accepted only for one-byte forms. `=` is never guessed from the host.
Boolean flags are not interchangeable with integer zero/one. Structured,
metadata, object, subarray, datetime, extended float and string forms refuse.

Tuple checking verifies the complete chain, exact arity, item operation,
zero second operand, valid target, increasing edge IDs, exact stored tail and
exact zero termination. This closes the inherited negative-terminator gap
locally without editing frozen N10. No arbitrary-map unique-edge-ownership
certification is claimed. Legitimate shared member identities are not forbidden.

Shape rank is 0 through 8. Axes are strict stored integers, nonnegative and at
most 16777216. LONG spans must be in bounds and no longer than eight bytes;
invalid spans cannot become an empty LONG interpreted as zero. All axes are
checked before any dimension multiplication. Nonempty total payload is at most
16777216 bytes and must equal elements times scalar width exactly.

Rank-zero shape contains one scalar. If any axis is zero, the view is empty:
all logical strides are defined as zero and every scalar/index access refuses.
This is an explicit bounded N12 convention, not a claim to reconstruct NumPy's
nonunique empty/singleton in-memory stride tuple. Nonempty C/F strides and the
coordinate API use **elements**, not bytes. Products are checked before
multiplication. All unused dimension/stride fields are zero.

## Ownership and read-only behavior

Each successful `NvView` owns two eight-word arrays and borrows its map.
Do not shallow-copy owning handles; close a view once before releasing its map.
The trusted caller must keep the map and its storage alive and immutable.
Views bind input pointer/length and node/edge storage identities; each public
read rechecks descriptor, dtype, order, shape, strides and extent. Closed-map,
wrong-live-map and safely mutated-handle controls must refuse. These checks are
not generation-safe stale-pointer protection after allocator address reuse,
concurrent mutation detection, or a security boundary against arbitrary memory
writes inside the trusted process.

`nv_bits` returns two unsigned-valued 32-bit limbs in native integer carriers.
It does not normalize floats, convert NaNs, sign-extend integers, or normalize
Boolean bytes. `nv_at` returns an element index or refusal. Invalid reads return
no scalar payload. `nv_row` accepts **no writable caller destination**: it
returns a separately owned allocation, so caller-selected output overlap cannot
modify parent/view memory. The caller releases that allocation with `nio_free`.
The evaluator checks disjointness and mutates the returned row, then verifies
the original bytes and all seven resident map tables remain unchanged.

The `readonly` field only reports a historical bytes versus bytearray carrier.
Zero never grants write permission; neither value asserts kernel protection.
N12 is a trusted read-only engineering API, not the full confined learner runtime.

Status meanings: -9001 unsupported/malformed reducer envelope; -9002 dtype;
-9003 shape/order/arithmetic; -9004 carrier/payload extent; -9005 invalid scalar
or coordinate read; -9006 invalid row request; -9007 allocation failure;
-9008 closed view. Refusal returns empty owning storage and no source identity.

## Record and inventory format

Successful rows are exactly 160 bytes. Four-byte signed little-endian fields
at offsets 0..60 are: node, buffer node, dtype node, scalar kind ASCII, width,
endian ASCII, order ASCII, rank, elements, original offset, byte extent, original
opcode offset, shape node, historical bytes-carrier indicator, dtype-state node,
and zero success status. Offsets 64..95 hold eight dimensions; 96..127 hold
eight logical element strides. Offsets 128..159 contain SHA-256 of the original
payload bytes, without byte-order normalization. Unused fields are zero.

Every REDUCE in the actual parent receives one row in node order. Unsupported
rows contain only node at 0, original opcode offset at 44, and declared negative
status at 60; the remaining bytes are zero. Recognized frombuffer candidates
are counted separately from other reducers. Allocation or unexpected failures
fail the run; they are not classified as unsupported. Expected supported/total
numeric counts are deliberately **not** guessed or frozen after inspection.

Pages contain up to 400 rows / 64000 bytes. At most 1311 pages cover the map's
524288-node envelope. The `R33NV001` manifest has a 160-byte header and 48-byte
entries binding each page ordinal, row count, length and SHA-256. Header fields
bind total rows/pages, candidates, supported, refused candidates, other reducers,
map node/reduction counts, descriptor-wise byte/element totals, exact original
and map-manifest hashes, first/last bit-read count, empties and bytes carriers.
Totals are **per descriptor**, not deduplicated physical storage or complete
learner parameter counts. Each supported payload is hashed in full; scalar
read/re-encoding probes are the first and last elements, not every parent value.

Fresh-process replay reloads the pinned map, rederives all rows, compares every
saved page byte and the complete manifest, and writes no replacement inventory.
Before/after fingerprints cover original bytes and nodes, edges, memo, stack,
marks, globals and opcode histogram. This is a new inventory/replay operation
over known map material, not rerunning N10/N11 experiments.

## Native controls and fixed schedule

Five direct children, in order: invalid invocation, matrix, refusals,
inventory-write, inventory-replay. Subsequent children do not launch after a
failed parent check. Native supervision checks status, start/reap, exact exit,
signal, empty stderr, complete bounded capture, unambiguous check count and
terminal marker. A process exit alone is not a passing result.

Matrix contains 88 combinations of eleven dtypes, two explicit endians, two
orders and two carrier kinds, plus five declared alternate-symbol/one-byte
endian cases. These 93 fixtures use shape (2,3), independent C/F coordinate
formulas and literal expected low/high limbs. Seven supplemental fixtures cover
smallest f4/f8 subnormals in both byte orders, Boolean byte 2, and the asymmetric
64-bit 0x0102030405060708 pattern in both byte orders: 100 positive bit fixtures
total. Literal matrix patterns include all-ones/high-bit/alternating integers,
positive/negative zero, infinities and quiet/signaling NaN payloads.

Refusals cover symbol/kind/arity, fifth argument, dtype state/flags, int-for-bool
flags, unsupported dtype/endian/order, external/readonly-external/text carriers,
short/trailing payloads, bool/float/overlong/malformed-span shape integers,
negative/excessive dimensions including after zero, dimension and byte-product
overflow, rank nine, wrong coordinate rank/index bounds and max-i64 index.
Twenty scalar/rank-eight/zero-axis shape controls cover rank-zero and rank-eight
all-ones in both orders plus a zero at every rank-eight position surrounded by
maximum legal axes in both orders. No empty layout may multiply huge prefixes
or suffixes before detecting emptiness.

The existing twenty shape controls now validate the complete owned 160-byte row:
rank, element/byte counts, all eight authored dimensions, all eight independent
logical strides, unused/reserved fields, source/descriptor provenance and the
digest of the fixture's original payload. The expected layout comes from the
authored shape and declared convention, never from the view's dimension/stride
arrays or a second export. Scalar unused axes are zero, rank-eight all-ones has
eight unit strides, and empty shapes retain every axis with eight zero strides.

The refusals child also starts with 26 explicit LONG controls. Both LONG1 and
LONG4 are covered: eight standalone scalar decodes per opcode (empty zero,
little-endian 80 00 = 128 versus 80 = -128, ff = -1, eight-byte positive/negative
sign extensions and both signed-64 extrema) and five end-to-end views per opcode.
View cases admit empty LONG zero, dimension128 and eight-byte dimension1;
decoded -128 refuses as a shape; eight-byte -1 succeeds in both permitted dtype
size/alignment sentinel fields. The new u1 views validate their complete rows
and scalar/empty behavior. All use the frozen scanner/validator and literal
expectations. These are bounded additions to existing integer/layout scope,
not historical primary reruns or a new learning family. Existing invalid-span
and over-eight-byte refusals remain. The five-child schedule is unchanged.

Separate synthetic-only mutations check cyclic and negative tuple termination,
negative head, count/tail/operation/operand mismatch, invalid LONG span, raw
extent, kwargs, oversized map counts, failed maps, incorrect view metadata,
wrong-live-map association and closed-map/view refusal. Preimages are restored
and fingerprinted; actual parent pages are never corruption targets.

Native resident integer stride is measured before the matrix. Wire fields are
four bytes; resident integer carriers must not be silently assumed four bytes.
Allocation-error branches are inspected and terminal/exit enforcement catches
runtime faults, but this batch does **not** inject allocator failure or qualify
all out-of-memory/leak/concurrency/security behavior. Arbitrary forged pointers,
unmapped slices and use-after-free shallow copies are outside its safe controls.

## Resources, allowed effects and admission

Parent guard: 180 seconds, 1 MiB per file, core zero, 64 descriptors.
Direct child deadlines: 5, 20, 20, 60, 60 seconds, total 165 seconds.
Per-child output ceiling: 1048576 bytes. Observed child RSS ceiling: 402653184
bytes, explicitly not a hard memory sandbox. Native CPU, wall and peak RSS are
retained. No child launches grandchildren or any interpreter.

All experiment outputs are exclusively created below
`Research/R33_NATIVE_N12_RUN_PRIMARY_V1`; launch logs have distinct N12 names.
Read-only parent/map paths are the frozen N10/N11 paths. Compiler, imports,
references, protocol/configuration, independent final review, build pair and
platform must be pinned before the one admitted primary. Every failure remains
consumed and retained; corrections after exposure require a new identity.

The original source snapshot and failed authoring compilation are retained.
Authoring compilation is not testing or primary exposure. Independent review
must precede preregistration; this design and a compiler success alone do not
grant execution permission. The earlier 15-file progress closeout was copied
and verified under `R33_PROGRESS_CLOSEOUT_SNAPSHOT_20260906_V1` before live
bookkeeping changes; its old manifest is never repinned to new live content.

## Reference provenance and review dispositions

Inert local references are `REFERENCES/numpy_v2_3_5_numeric.py.txt` and
`REFERENCES/numpy_v2_3_5_descriptor.c.txt`, carried from the checkpoint's reported
official NumPy v2.3.5 downloads and bound by exact hashes. Their source text
supports the declared frombuffer/reshape and plain dtype grammar. The initial
review did not independently authenticate the tag download, and the historical
parent's actual NumPy version remains unknown. These files are never imported
or executed and are not the source of a learned behavior claim.

Initial independent findings F01/F02: new live-map binding plus pre-read/row
validation and closed state, with ownership limitations stated above. F03:
whole-chain exact-zero tuple validation, including a negative-terminator witness
that the unchanged inherited validator accepts. F04: explicit LONG byte-span
validation before inherited integer decoding. F05: validate every axis first,
then zero-extent canonical logical strides. The previously identified output
alias defect is eliminated by removing the writable-destination API entirely.
The first authoring build's pointer-cast assertion type error is retained and
corrected with separately typed pointer/address temporaries in the evaluator.

The independent final review of the prior evaluator identified only B01
(no valid LONG positive control) and B02 (incomplete scalar/empty/high-rank row
oracle) as preregistration blockers. That report and its exact reviewed sources
are preserved in `PREREVIEW_V1`. The added controls above address those two
findings for focused independent re-review; their presence is not execution
evidence. `views.zag` and all frozen imported implementations are unchanged.
