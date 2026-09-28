# N13 strict legacy Torch view engineering design

Identity: `r33-native-n13-strict-legacy-torch-views-v1`.
Status: authoring for independent final review. No fixture exposure, experiment
reservation, preregistration, freeze or launch admission is granted by this file.

## Question and exclusions

Can native Zag interpret the declared legacy storage/tensor/parameter descriptor
subset, preserve the serialized scalar bits and storage association, refuse
unsupported forms with resource provenance intact, and reproduce its inventory
in a fresh process while leaving R27 step60423/restarts0 unchanged?

This is known-parent and finite synthetic engineering evidence. It is not fresh
scientific validation, original Python inference/update equivalence, recovery of
the historical PyTorch version, semantic-digest recomputation, a full parameter
census, complete parent migration, sensory qualification, training or promotion.
No reducer, constructor, callback, import, Torch runtime, unpickler, graph/BPE/VAD
machinery, learner, optimizer, credential or scientific world is executed.

The earlier N12 Unicode U7 label exclusions remain exclusions of that frozen
numeric grammar. N13 does not rerun or broaden N12. N10/N11/N12 are consumed.

## Inputs, semantic grammar and exact bytes

The API accepts a trusted, live, immutable, validated ParentMap and unique owning
view handles. The actual parent enters through unchanged N11 `pb_load`, which
verifies the N10 manifest, every retained page, all original bytes and accepted
structural identity. Synthetic outer pickles enter through the unchanged native
inert scanner and validator. All inputs remain inert data.

Storage is an unmutated `torch.storage._load_from_bytes` REDUCE with one in-band
bytes argument. Its blob has exactly five protocol-2 pickle records, then an
eight-byte nonnegative little-endian element count and exactly count multiplied
by scalar width payload bytes. Each record has a distinct memo table. The lexer identifies a bounded
complete prefix while skipping operand bytes; the frozen scanner validates the
entire prefix with STOP at its exact end. STOP-valued bytes inside an operand or
the raw tail are never instructions. Lexical admission does not imply valid
stack, memo, tuple or dictionary semantics.

The records are magic LONG bytes `6cfc9c46f9206aa85019`; integer version1001;
exact sysinfo with true Boolean little_endian, version1001 and type sizes
short2/int4/long4; a BINPERSID for exactly
`(storage, torch.<allowed storage>, key, cpu, count, None)`; and a one-item list
containing the same key. Keys contain 1–64 printable non-space ASCII bytes.
Type names/widths are Byte1, Char1, Short2, Int4, Long8, Float4, Double8 and Bool1
with the literal `Storage` suffix. Half, complex, arbitrary device, storage-view
metadata, additional keys and unsupported protocols are refused, not relocated.

Tensor is an unmutated six-argument `torch._utils._rebuild_tensor_v2` REDUCE:
storage, integer storage offset, size tuple, stride tuple, Boolean gradient,
and unmutated no-argument `collections.OrderedDict` REDUCE hooks. The optional
seventh metadata argument is outside this grammar even when None. Parameter is
an unmutated three-argument `_rebuild_parameter` REDUCE: admitted tensor,
independent Boolean parameter gradient, and the same exact hooks grammar.
Both tensor and effective parameter flags are retained. Either true flag
requires FloatStorage or DoubleStorage. No autograd capability is claimed.

Rank is 0–8; every dimension, stride and offset is a strict nonnegative integer
at most16777216. All axes are validated before detecting zero axes and computing
products. Nonempty logical elements are at most16777216. Greatest addressed
storage index is checked incrementally before multiplying/adding strides.
Rank zero has one element. Empty tensor strides are preserved, and empty offset
must be at most storage count; storage-only empty views have normalized stride0.
Noncontiguous, overlapping and zero strides are permitted within those bounds.
Coordinates and offsets use elements, not bytes. Empty views expose no scalar.

The public bit API returns two unsigned-valued 32-bit words without float
arithmetic, sign extension, NaN canonicalization or Boolean normalization.
Synthetic noncanonical Bool bytes are raw-transport controls, not constructor
or runtime-value claims.

## Ownership, error causes and aggregate work

Each view owns two eight-word arrays and borrows its parent. Close each owning
handle once before releasing its map; no shallow owning copies. Public access
rechecks live input/node/edge storage identity and rederives the complete view.
This is not arbitrary-pointer, allocator-generation reuse, concurrency, malicious
same-user or host-administrator security certification.

Every public row returns a new owned 256-byte allocation, never a caller-chosen
writable destination. The caller frees it. Row mutation and disjointness controls
must leave input bytes and all seven resident map tables unchanged.

Status map:

| Code | Meaning and disposition |
| --- | --- |
| -9101 | Unsupported/malformed outer grammar or header framing/stack/memo semantics. |
| -9102 | Unsupported storage metadata/type/device/key/sysinfo or gradient-dtype combination. |
| -9103 | Raw count/payload extent disagreement. |
| -9104 | Shape/stride/offset/rank/arithmetic admission refusal. |
| -9105 | Invalid coordinate after successful live binding. |
| -9106 | Unexpected row serialization/hash argument failure; fail the primary. |
| -9107 | Actual allocation failure; fail the primary, never an ordinary unsupported row. |
| -9108 | Closed/mismatched live view association or safely altered owning handle. |
| -9110 | Header lexer/scanner capacity exhausted; fail the primary unless this exact finite control expects it. |
| -9111 | Explicit aggregate work allowance exhausted; same rule. |
| -9112 | Evaluator bit re-encoding/internal failure; fail the primary. |
| -9113 | Failed evaluator fixture-setup prerequisite; fail before subject parsing, not a target refusal. |

For inventory, only -9101 through -9104 are ordinary refused rows. Resource,
allocation, binding and unexpected failures never silently become unsupported
coverage. Resource causes propagate through open, bound, coordinates, bits and
row rather than being hidden by a generic false/error result. Negative tests
assert exact codes, often both prefix and scanner surfaces, not mere nonzero.

Both one-byte and four-byte length fields distinguish physical input truncation
from crossing the artificial record cap. Four additional fixed controls pair
complete 4100/4099-byte near-cap records (-9110) with their genuinely truncated
4096-byte counterparts (-9101). The fixed input literals came from independent
final review R2, before exposure; none is inferred from a returned parser value.

Every nonempty hexadecimal record requires its exact literal byte length before
being submitted. Intentional zero-length cuts derive only from a successfully
built nine-byte baseline. Generated negative carriers require complete nonempty
construction and fixed payload lengths; array/coordinate/oracle capacities are
checked before their first indexed write or budget-negative use. Failure stops
the affected stage with setup failure and partial-owner cleanup; a target's
expected rejection cannot compensate for a failed fixture prerequisite.

One nonreset TsWork account per child limits public opens including rebinding
65536, header record attempts327680, public probes16384, public rows8192,
hash-message bytes268435456 and shape-allocation attempts131072. Attempts are
charged before the work; prior charges are not rolled back on later failure.
Rows charge blob+payload+key message bytes, not SHA padding/scratch. Hashes for
new evaluator fingerprints/pages also charge that account. The inherited fixed
N11 loader's bounded work is outside these new counters and remains under the
same OS deadline. Fixed low-budget controls use separate explicitly limited
accounts; their main log does not purport to sum those isolated counters.

This resolves initial-review F1 with cause-preserving APIs and scanner capacity
codes, and F2 by bounding aggregate repeated parsing, allocation, probes and
whole-storage hashing. It does not introduce a cache or claim measured speedup.
OS deadlines and observed RSS checks remain required in addition to work limits.

Actual allocator-failure injection is NOT QUALIFIED. The finite second-shape
allowance denial tests partial cleanup on a budget refusal, not an OOM event.
INDEPENDENT_ORACLES N-R01–R05 are explicitly not covered experimentally. Actual
allocation error paths are statically reviewable and propagate -9107; no claimed
runtime fault-injection pass, allocator security or memory isolation follows.

## Independent controls and exact finite schedule

The immutable independent oracle table is `INDEPENDENT_ORACLES.md`, SHA256
661945bc7b285fcce89ca47b7303e49ab9bbba282fccfec03428fe62573eb40e.
Its payloads and expected unsigned words are literally transcribed to oracles.zag,
not obtained by running ts_* or by choosing values after exposure. Nine nonempty
payloads cover all eight names and raw noncanonical Bool bytes; eight matching
empty fixtures cover each storage type. Every nonempty scalar is checked against
the independently supplied low/high words in storage, tensor and parameter form.
Floating tensor/parameter flag combinations and integer true-flag refusals are
separate finite cases. Flag matrix uses the complete supplied payload, including
the two zero patterns, rather than limiting those views to the first two values.

The independent A16 blob has exactly261 bytes: five record extents15/6/100/55/13,
raw count8, payload64. The builder's compact A16 output must equal every literal
byte. Header decoding must report payload start197, PID key start159 and keylen3.
Twenty-two A16 tensor layouts cover scalar, ranks1–8, contiguous, transposed,
gapped, overlapping, zero strides, last-element bounds, singleton stride maximum,
the logical-element maximum with only two probes, and five empty layouts.
Additional 64-bit scalar fixtures and the dot-key/opcode-valued raw fixture pin
high-word handling and inert framing. The other eight empty tensor fixtures
include the independent E-I32 zero-storage case. Full rows compare every field,
all dimensions/strides, reserved zeros, exact hash inputs and source provenance.

The compact dot-key ByteStorage carrier has literal length198, PID-key offset160
and payload offset194. Its key's byte value46 also occurs as each header STOP;
the row oracle must not use a first-occurrence dot search as the key location.
These literal layout checks were added during static review before any execution.

Two alias-pair cases contrast a memo-shared storage node with separately
serialized byte-identical storage blobs. Equal keys/digests never imply alias.
Closing one independently owned view must not invalidate its sibling. The A16
row fails with327 hash bytes, succeeds with exactly328, and refuses a second
uncached row under the SAME exhausted account even with a newly opened handle.

Matrix has exactly102 cases:84 successful view fixtures,14 nonfloating gradient
refusals, one complete-carrier check, two alias cases and one hash-boundary case.
Refusals has exactly123 cases:37 record/framing/capacity controls,28 blob/type
controls,43 view grammar/layout controls,12 budget/lifetime groups, one unit
budget group and two integer-one-as-Boolean controls. These are grouped cases,
not a claim that each case performs exactly one assertion or one API call.

Negative branch coverage includes length-delimited STOP companions, every cut
of one short record, forbidden opcodes, open marks, duplicate/unbound memo,
127/128 memo boundaries, stack/node/edge/token/byte/GLOBAL-line limits, bad magic,
version/endian/sysinfo/device/type/key/cardinality/count/tail, five/seven tensor
args, two/four parameter args, zero/two storage args, bytearray/text/NEWOBJ storage,
hooks None/dict/nonempty/BUILD/one-list-argument forms, scalar/rank/product/span
limits, true gradients on each nonfloat type, and actual closed owning handles.
The missing cross-record memo case uses the fifth-record GET of a prior record's
slot rather than the independent table's illustrative first/second record pair.
Not every suggested negative byte mutation in the independent table is separately
instantiated; qualification is the exact frozen finite evaluator, not exhaustive
format or adversarial fuzzing. No actual OOM, arbitrary pointers or stale copies.

## Inventory, replay, resources and effects

Every REDUCE receives one 256-byte row in node order, capped at8192 records.
Supported row offsets0..72 hold node/category/tensor/storage/buffer, kind/width,
storage count, blob/raw/key offsets and lengths, storage offset, rank, logical
elements and both gradient flags. Offset76 is zero success status;80 is original
opcode offset;84..95 are zero. Dimensions96..127 and strides128..159 have eight
signed-32-bit little-endian fields each. SHA256 blob/raw/key occupies160..255.
Refusal rows retain only node0, category4, negative status76 and opcode offset80.

Pages have at most256 rows/65536 bytes; at most32 pages. The R33TS001 manifest
has256 header bytes and48 bytes per page, maximum1792. It binds counts, categories,
descriptor-wise bytes/elements, raw/map hashes, probe/empty counts and storage
node identity totals. Header168..255 stays zero; no transient pointers/timing/
work counters enter deterministic bytes. Work counters are logged separately.
Each entry has ordinal, rows, bytes, reservedzero and SHA256 page bytes.

Storage identity deduplication uses serialized storage NODE IDs, not source keys,
blob hashes, physical memory, runtime storage aliasing or complete learner parameter
coverage. Descriptor totals may repeat the same storage. Even distinct serialized
nodes can have byte-identical contents; these are not automatically coalesced.
Supported/refused parent counts remain unknown prospectively, not chosen as an
oracle after exposure. First/last logical-coordinate raw re-encoding is a known-
byte consistency check, not original-method execution or independent behavior.

Five direct children: invalid exit2; matrix, refusals, inventory-write and a fresh
inventory-replay exit0. Each declares its fixed case count and zero failures.
Parent guard180s; child deadlines5/20/20/60/60s, capture/file ceiling1MiB, fd64,
core0 and observed child RSS at most402653184 bytes. The RSS check is observational,
not enforced hard memory isolation. Direct child PID supervision only; no
grandchild or process-group containment claim. No network or foreign program
execution is in the evaluator. Compilation invokes only the pinned native compiler.

The result's verified_completed_child_checks is incremented only after all of
that child's exit, supervision, capture, stderr, resource, count and terminal
marker checks have passed. Reported counts from rejected children are not credited.

All output is exclusive under Research/R33_NATIVE_N13_RUN_PRIMARY_V1. Replay
reads retained pages/manifest without replacing them and compares every byte
against a fresh derivation. Input and seven resident tables are fingerprinted
before/after; accepted identity and training refusal remain exact. Original
parent and all old artifact/source hashes must also pass external operational
verification after the primary. Those hash checks do not rerun old experiments.

Any unexpected exit/signal/stderr, failed oracle, incomplete capture, deadline,
resource limit, identity mismatch, I/O failure, missing terminal marker or child
prevents a pass and further child launch. Keep the sole attempt and partial files;
do not rerun, alter its oracle or broaden grammar after exposure. Correction then
requires a distinct reviewed identity. Subsequent qualification requires final
review, preregistration, reservation, exact double-build freeze and separate
launch admission, then postrun review and complete bookkeeping/closeout.
