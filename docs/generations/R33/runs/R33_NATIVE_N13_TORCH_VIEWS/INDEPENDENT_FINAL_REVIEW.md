# R33 N13 independent final source/evaluator/config review

Date: 2026-09-06.
Candidate: `r33-native-n13-strict-legacy-torch-views-v1`.

**Disposition: REQUEST_CHANGES. NOT APPROVED FOR PREREGISTRATION.**

Four concrete defects require correction: an incorrect dot-key offset oracle,
two lexer capacity/provenance branches, fixture-generation failure that can
receive passing negative-control credit, and unchecked evaluator allocations.
The first defect alone prevents this candidate's declared successful matrix.
These are static findings; no fixture was executed to discover them.

The omission of actual allocator-fault injection is acceptable as an explicit
NOT COVERED limitation for this narrow prospective engineering qualification.
It does not excuse the independently visible implementation defects below.
No allocator-injection campaign or broader pointer/security work is required
by this disposition.

## 1. Review scope and evidence discipline

Read the native-only execution contract first. Reviewed the complete original
storage, tensor, fixture builder, evaluator, literal oracles, refusal controls,
matrix, inventory, driver, DESIGN and CONFIG files identified in section 8.
The complete initial review and immutable independent oracle were also read;
their identities remain unchanged. The seven frozen dependency sources were
reviewed in the continuing source-review record, including the complete
337-line PROCESS_V3 supervisor. Their exact N12 BUILD_03 identities were freshly
checked against both final candidate build directories.

Inspection was limited to source/document reads, retained-log inspection,
byte comparisons and artifact hashes. No Python, imported runtime, stored
reducer, compiler, numerical evaluator, fixture, primary, training or registry
action was executed by this reviewer. The only file written is this report.
No old experiment was rerun and no implementation or prior review was edited.

The API scope remains a trusted immutable validated map, live unique owners,
and the declared finite evaluator. This is not an arbitrary-pointer,
concurrent-writer, allocator-generation, hostile-host or runtime-authority
review. Official PyTorch v2.9.0 reference text remains semantic reference only;
the parent's original PyTorch version and behavioral equivalence are unknown.

## 2. Blocking findings

### R1 — P1: dot-key positive fixture uses the magic STOP as its expected key offset

Evidence: `matrix.zag:19`, `matrix.zag:41`, `matrix.zag:102-105`;
`evaluator.zag:46-47`; `fixtures.zag:72-84`; `storage.zag:106`.

The independently specified dot-key companion is instantiated as a compact
ByteStorage blob with key `.` and payload `2e 80 02 52`. Its bytes are valid for
the intended restricted carrier. However, `p13_good` obtains the expected PID
key offset by searching the ENTIRE blob for the first occurrence of the key.

For this exact fixture, the first `2e` is R1's STOP at blob offset **14**.
The PID key's actual text operand starts at blob offset **160**. The latter
offset follows the same literal A16 layout, with the one-byte-longer
`ByteStorage` name before the key; shortening the key affects only later bytes.
Thus the row correctly contains `B+160`, while `row_key_at` expects `B+14`,
where B is the outer map's blob start. Equal key bytes do not identify a field.

This is a deterministic wrong expectation, not a parser defect or unknown
runtime behavior. Assuming preceding checks succeed, this is case 99; its
failure prevents the two alias cases and hash-boundary case from running, and
the terminal `cases == 102` assertion also fails. Compilation and identical
binaries cannot establish this fixture's correctness.

Required correction: identify expected key positions from independently pinned
fixture layout/field locations, not an unconstrained substring search. Preserve
the dot-key test and immutable independent oracle. For this compact dot carrier,
pin PID key 160, payload start 194, payload length 4 and blob length 198 if those
additional literal checks are used. These offsets are statically derived, not
obtained by calling `ts_decode` or `ts_row` as their own oracle.

### R2 — P2: length fields crossing the record cap still lose capacity provenance

Evidence: `storage.zag:39`, `storage.zag:47-50`, `storage.zag:57-58`;
`inventory.zag:53-57`; `DESIGN.md:89-105`.

The four-byte-length branch returns `-9101` when `limit-at < 4`, and the
one-byte-length branch returns `-9101` when `at >= limit`. Neither distinguishes
the artificial 4096-byte record limit from the physical input end. Consequently,
a fully present length field crossing the configured cap becomes an ordinary
malformed/unsupported result instead of capacity `-9110`.

Two fixed source-derived witnesses, NOT generated or run:

| Bounded-record input specification | Literal extent and branch |
| --- | --- |
| `80 02 58 f6 0f 00 00`, exactly 4086 bytes `41`, then `58 00 00 00 00 86 2e` | 4100 bytes total. The second BINUNICODE opcode is at 4093; its four length bytes physically occupy 4094..4097, but only two are inside the cap. Line 48 returns `-9101`. |
| `80 02 58 f8 0f 00 00`, exactly 4088 bytes `41`, then `55 00 86 2e` | 4099 bytes total. SHORT_BINSTRING is at 4095 and its physically present length byte is at 4096. Line 50 returns `-9101`. |

Each describes two strings combined with TUPLE2 and STOP, without a stored call.
The examples target the existing bounded header-record API, not admission of
their root as storage metadata. The first string fits inside the cap; the
next length field is what exhausts it. The intended configured-cap result is
`-9110`, as for the already handled payload-operand crossing at line 57.

When such a result reaches inventory, `-9101` is eligible for an ordinary refusal
row; `-9110` would correctly abort qualification. This leaves F1 incomplete.

Required correction: distinguish physical truncation from artificial capacity
exhaustion for both length-field widths before reading the length. Add bounded
near-cap controls and genuine truncated companions with exact expected causes.
Keep frozen dependencies unchanged and revise prospective case counts if controls
are added. No witness execution or new fixture file was authorized or performed.

### R3 — P2: fixture allocation failure can masquerade as a passing negative control

Evidence: `evaluator.zag:16-20`; `refusals.zag:3-10`, `refusals.zag:17-21`,
`refusals.zag:34`.

`p13_hex` returns the same empty slice for allocation failure and invalid/empty
input. `p13_record_hex` does not check that a nonempty literal produced its exact
byte count before recording a case and submitting it to the implementation.

For example, failure to allocate the four bytes for literal `80034e2e` changes
the tested input into an empty slice. Both `ts_prefix(empty,0)` and
`ts_record(empty,0,w)` then return the expected `-9101`; the empty nodes/root
assertions also pass. The case is counted, so fixed case-count accounting does
not expose this substitution. Several other negative-framing cases have the
same problem. This can give a case passing credit for the wrong input even
though the public parser correctly preserves its own allocation failures.

Required correction: fail fixture setup explicitly before invoking the subject
when a nonempty literal does not produce exactly its declared bytes. Preserve
generation status or verify the fixed expected length, and distinguish intentional
empty fixtures/cuts from failed construction. Apply the same setup discipline
to generated carrier/payload baselines used by negative grammar controls.
No target's negative status may discharge a failed-fixture prerequisite.

This finding is source-level failure-path analysis, not an injected OOM result.
It is separate from, and not waived by, N-R01--R05 being NOT COVERED.

### R4 — P2: several new evaluator paths index failed allocations before checking them

Evidence: `matrix.zag:98`, `matrix.zag:102-108`; `refusals.zag:56`,
`refusals.zag:74`, `refusals.zag:101`, `refusals.zag:152`;
`oracles.zag:7-24`, `oracles.zag:61-66`; frozen `inert.zag:15-20`.

`pm_words` explicitly returns a null-backed zero-length slice on allocation
failure. Nevertheless, `p13_alias_controls` immediately performs
`shape[0]=2` and `strides[0]=1`; several refusal setup functions do the same.
The two additional scalar fixtures write `l.indices[0]` before checking
`l13_new`, and dot-key setup writes `o.low`, dimensions, strides, coordinates
and indices before their lengths are validated.

The later `complete_oracle_arrays` check in `p13_good` cannot protect writes
that have already occurred. Depending on generated bounds handling, these paths
can trap or access invalid memory instead of recording a controlled setup
allocation failure and releasing already-owned buffers. This concerns the
candidate's own trusted allocations, not forged pointers or a hostile caller.

Required correction: check every relevant allocation result before the first
index/slice write, record setup failure, free partial owners, and stop that
stage. Use the guarded storage-matrix setup and `l13_layout` allocation check
as the local pattern. Also require valid coordinate scratch/setup objects before
submitting budget-negative cases, so an unrelated failed prerequisite is not
silently hidden by an earlier budget refusal.

## 3. Additional nonblocking corrections

**A1 — P3, rejected-child checks can be labeled verified.** At `driver.zag:23`,
`child_checks` is increased after checking only parsed count, supervisor status
and exit code. Earlier parent checks can already have rejected the child for
nonempty stderr, excessive RSS, incomplete capture or a missing terminal marker.
For example, a zero-exit child with a valid count line but no PASS marker is
rejected at line 22 yet contributes to `verified_completed_child_checks` in
the failure result JSON. The overall primary still fails. Accumulate this
field only after all that child's acceptance checks succeed, or rename and
separate reported counts from verified-completion counts.

**A2 — wording.** `DESIGN.md:34-35` says the element count is followed by exactly
that many scalar bytes. The implementation correctly requires `count * width`
payload bytes. State that explicitly, particularly for the eight-byte types.

## 4. Static case arithmetic and fixture correctness

These are COUNTS OF THE INTENDED SUCCESSFUL CONTROL FLOW, not measured execution
results. `p13_case` counts grouped fixtures, while `p13_check` counts assertions.
The current source/config arithmetic agrees:

| Mode/group | Independent source arithmetic | Cases |
| --- | --- | ---: |
| Matrix ordinary views | 9 nonempty payloads x 3 categories + 8 empty payloads x 3 categories | 51 |
| Matrix extra floating flags | 2 floating types x (3 additional parameter flag pairs + 1 true-gradient tensor) | 8 |
| Matrix extra layout views | 22 A16 layouts + 2 eight-byte scalars + 1 dot-key storage | 25 |
| Matrix successful-view subtotal | 51 + 8 + 25 | 84 |
| Matrix nonfloating gradient refusals | 7 nonfloating payload fixtures x 2 flag choices; the two Bool payloads are distinct fixtures | 14 |
| Matrix remaining groups | 1 complete A16 carrier + 2 alias pairs + 1 hash-budget group | 4 |
| **Matrix total** | **84 + 14 + 4** | **102** |
| Refusals framing | 17 explicit records + 9 cuts (0..8) + 1 oversized length + 5 capacities + 1 GLOBAL limit | 33 |
| Refusals blobs | Variants 1..26 + 2 unsupported storage names | 28 |
| Refusals view grammar/layout | 10 variants in 32..42 excluding 36 + 17 variants in 43..59 + 16 layout calls | 43 |
| Refusals budget/lifetime | 4 open-budget groups + 5 public-budget groups + wrong-map + mutated-handle + closed-handle | 12 |
| Refusals final groups | 1 unit-charge group + 2 integer-one Boolean controls | 3 |
| **Refusals total** | **33 + 28 + 43 + 12 + 3** | **119** |
| Inventory-write | One `p13_inventory(0)` case | 1 |
| Inventory-replay | One `p13_inventory(1)` case | 1 |
| Invalid | Silent early exit 2 before case processing | 0 |

`driver.zag:50-54` asserts these totals inside each successful-work child and
suppresses its PASS marker on failure. The parent does not separately parse
N13_CASES, but requires the zero-failure child count record and exit; within the
fixed trusted dispatcher, that includes the child's case assertion. R1 prevents
the matrix from reaching its intended total despite the arithmetic being right.

### Literal transcription

The 50 nonempty scalar byte/low/high expectations in `oracles.zag:7-45` match
the immutable table: all eight storage types, both Boolean payload variants,
all eight bytes for 64-bit values, unsigned high-bit words, both zero signs,
NaN payloads/signs and quiet-bit-clear patterns. No float conversion appears.
The additional A16 sixteen-word payload also matches its fixed table.

`o13_a16_blob` transcribes the complete independent carrier. Static inspection
agrees with the 15/6/100/55/13-byte record extents, eight-byte count, 64-byte
payload, total 261, PID key start 159 and payload start 197. The matrix compares
the compact builder's complete output against that literal carrier, not just
against its own decoded metadata. It separately asserts the stated offsets.
This is a sound planned comparison; it has not been executed.

The 22 A16 layout definitions match the 17 nonempty and five A16-empty layouts.
Coordinates generated by enumerating the small rectangular fixtures match the
listed coordinate order, while expected storage indices remain literal constants.
V-PRODUCT-MAX has only its two prescribed probes, not an element enumeration.
V-L64/V-D64 have the prescribed offsets and both-word expectations. Empty E-I32
is covered through the ordinary empty storage/tensor matrix. Float flag views
intentionally cover all eight supplied values instead of only the first two;
this extension is disclosed in DESIGN and preserves the literal expectations.

Raw rows check all metadata fields, reserved bytes, dimensions/strides, hash
ranges and owned-output mutation. Their hashes use the frozen SHA implementation
on independently selected byte ranges, not an independent new cryptographic
implementation. The key-offset selection in R1 is the concrete exception.

### Refusal construction and limits of coverage

The 17 explicit record expectations were checked against both lexical framing
and frozen scanner semantics. Capacity constructors reach, respectively, the
65th stack entry, 129th node, 257th edge, the 1024-token ceiling before STOP,
the byte cap, and the GLOBAL operand limit. The 127/128 memo-slot distinction
and protocol-incompatible SHORT_BINBYTES are correctly staged. The 26 blob
variants' selected status families agree with their source mutations under
successful fixture construction; R3 concerns the missing setup prerequisite.

The cross-record memo control uses an R5 GET of slot zero after R3 populated
that slot, as disclosed, rather than the oracle's illustrative R1/R2 pair.
Grammar controls cover missing/extra arguments, inappropriate storage carriers,
NEWOBJ instead of REDUCE, hooks/state variants, and strict Boolean flag nodes.
Layout calls cover rank nine, rank mismatch, negative/over-limit fields,
nonempty product limit, empty-field validation and scalar/one-past storage bounds.

This is not every literal negative case in INDEPENDENT_ORACLES. Examples not
separately instantiated include its exact isolated LONG truncation N-H02,
integer-one sysinfo-endian variant, long-size-field mutation, empty key list,
and the A16 two-axis cumulative-overrun N-L10. Existing related controls do not
make those exact cases executed or covered. The near-cap length-field cases in
R2 are also missing and are now necessary to resolve an actual defect.
Actual allocator injection N-R01--R05 remains NOT COVERED. Do not describe
the totals 102/119 as exhaustive branch coverage or a full oracle-ID census.

## 5. F1/F2 disposition, bounds and ownership

**F1: materially improved, not fully resolved.** Frozen scanner `-8805` becomes
`-9110`; initial map allocation and shape allocation failures become `-9107`.
`ts_bound` returns reopen causes instead of Boolean failure, and `ts_at`,
`ts_bits` and `ts_row` retain them. SHA scratch `-12` becomes row `-9107` after
row cleanup. Closed/mismatched ownership is separate `-9108`, and coordinates
are checked only after successful binding. Inventory admits only -9101..-9104
as ordinary refused rows. R2 still violates this distinction, while R3/R4
undermine the broader evaluator failure-path claims.

**F2: the declared aggregate-work design is adequate for the narrow scope.**
The main TsWork account is created once per child and passed through public
opens, rebinding, header attempts, probes, owned rows and shape allocations.
Row hash input is charged atomically before hashing; fingerprint/page hashes
also charge the main account. A failed reservation does not increase a counter
beyond its limit, and preceding work is not rolled back. Header attempts count
per record, not per five-record blob. This finer-grained unit is disclosed.

The A16 hash boundary is exactly 261 + 64 + 3 = 328 message bytes. The separate
327-byte account refuses without a successful row; the 328-byte account permits
one row and remains exhausted when a distinct view is opened on that same
account. Other fixed control accounts and the inherited pb_load work are
explicitly outside the main log's sums. Direct lexical control calls, fixture
construction, other evaluator scratch and logging are finite harness work,
not comprehensive allocation telemetry. The main counters must not be reported
as total process work or total allocations. No speed or deadline fit was measured.

Within the validated-map precondition, the core storage/tensor code retains
the initially reviewed index proof: inspect all dimensions, detect zero axes
before product checks, bound each nonnegative stride contribution by remaining
storage, treat rank zero as one element, and reject coordinates for empty views.
The raw-tail equality and width cap keep successful byte accesses in the
original payload. Temporary header maps and successful rebinding views are
closed, failed partial shape owners are released, and rows own separate output.
No additional core-view out-of-bounds/lifetime defect was established in that
scope. R4 is a concrete defect in new evaluator setup, not a broader API claim.

## 6. Supervisor, inventory and effect/failure-path review

The current failure handling was traced statically; no new supervisor/I/O fault
injection or replay was performed. Frozen PROCESS_V3 behavior is inherited,
not requalified by this review.

| Surface | Static behavior and limits |
| --- | --- |
| Supervisor initialization | Guard failure returns 3; exclusive root-admission failure returns 4. These exits may lack NATIVE_RESULT.json, so an eventual external launcher must retain exit/launch evidence and any partial directory. Neither is a pass. |
| Child supervision | Nonzero adapter status, not-started/not-reaped child, wrong exit, signal, stderr, excessive/absent RSS, or capture failure increments parent failures. Subsequent `p13_run` calls return without launching another child. Missing/unparseable/duplicate count records and missing PASS markers fail acceptance. A1 concerns count labeling, not an overall false pass. |
| Process containment | PROCESS_V3 uses its existing kernel timer, direct-child kill/reap and per-file output limit. N13 declares only direct-child containment and observational RSS, not process-group or hard-memory isolation. |
| Result publication | JSON counts are explicitly named before-result-write fields. Exclusive result-write and root-close failures suppress the final parent PASS marker even if a partial or apparently clean JSON already exists. That JSON alone is not completion evidence. |
| Parent loading | Failed pb_load causes immediate loaded-map cleanup and return. The inherited loader rejects invalid binding/source/manifest/pages rather than producing unsupported N13 rows. Its older status families are failures, not new allocation-injection evidence. |
| Inventory setup | Parent identity, full fingerprint, output root and all page/manifest/seen/coordinate capacities are checked before the row loop. Failure prevents row processing; final failures and cleanup remain. This setup is better guarded than the evaluator paths in R4. |
| Inventory limits and row errors | Each REDUCE consumes one bounded record slot; only recognized ordinary refusal codes produce refusal rows. Resource/binding/internal errors fail the child. A failed first probe suppresses the second; failed probes prevent successful row publication. Views/rows are released after the attempted record. |
| Pages and manifest | At most 8192 x 256-byte rows, 256 rows/page, 32 pages; 256 + 32 x 48 = 1792 manifest bytes. Under checked caller capacities, page offsets and reserved regions fit. Existing helpers reject oversize/short/nonregular reads and exclusive-create/write/sync failures. A page failure stops further iteration; manifest publication is gated on no prior failures. |
| Fresh replay | Page and manifest reads require exact size and every-byte equality with a fresh derivation. Failed replay-buffer allocation leads to a failed bounded read, not an unchecked comparison of a positive-length buffer. These failures cannot become an ordinary refusal row. They are not all individually identified as allocation failures. |
| Final integrity | Full input and seven resident-table fingerprints, parent identity and training refusal are checked after inventory. A failure here can leave pages/manifest already written, but suppresses child/parent PASS. Such files remain partial evidence and must not be admitted alone. External postrun source/artifact verification remains separately required. |

Supported/refused parent counts are prospectively unknown, as CONFIG records.
Inventory totals describe serialized descriptors; storage uniqueness uses node
IDs. Equal keys, raw bytes or hashes do not prove runtime aliasing. Known-byte
first/last re-encoding is consistency checking, not an independent behavioral
oracle. An inventory with no supported candidates must not be described as
parameter recovery merely because its bookkeeping/replay checks succeed.

CONFIG and source agree on the fixed child sequence, deadlines, result limits,
work-account defaults and run path. The 5/20/20/60/60-second supervisor deadlines
sum to 165 seconds under the 180-second parent guard; this leaves finite overhead
but is not measured timing sufficiency. Invalid exits before child-side deadline
setup and is bounded by its parent supervisor. CPU/file/fd/core limits are inherited
from the parent guard; child-side deadlines are additional. The 384 MiB RSS check
is observational. No general namespace/filesystem sandbox is claimed.

Writes reachable in the planned primary are its exclusive captures, pages,
manifest and result under the designated new run directory. The inspected N13
logic does not call historical mutation, training, network, reducers or a foreign
runtime. This is a source-call-path observation, not authorization to launch it.

## 7. Allocator-injection decision and required next state

Actual allocator fault injection may remain NOT COVERED for a narrowly worded
engineering preregistration after the concrete setup/propagation defects are
fixed. Budget-denial cleanup exercises a different trigger; an empty returned
handle alone is not a measured leak/fault-injection qualification. Keep the
distinction in DESIGN, CONFIG and any later results.

Correct R1--R4 without modifying the initial review or independent oracle.
Reconcile added controls and their exact static case counts with driver/config;
retain the current authoring/build identities as history. Supply the resulting
source/design/config identities for a subsequent final review. A1/A2 should
also be corrected before freezing prospective reporting. This reviewer has
made none of those implementation changes.

No preregistration approval, reservation, freeze, admission, fixture exposure,
primary execution, scientific promotion or behavioral certification is granted.
N10/N11/N12 remain consumed. Existing matching builds do not override this
REQUEST_CHANGES decision.

## 8. Exact reviewed identities

Paths are relative to `/Users/Shared/micah/Documents/TNN/TNN/` unless stated.
The following table's files are under `Research/R33_NATIVE_N13_TORCH_VIEWS/`.
At the original-snapshot inspection, all nine then-live Zag files compared
byte-for-byte equal to their corresponding BUILD_01 and BUILD_02 copies
(18 successful comparisons). This is a historical identity statement, not a
claim about the subsequently amended live files; see section 9.

| File | Lines | SHA-256 |
| --- | ---: | --- |
| storage.zag | 117 | `b3b7cd54acce20fde68c0f7d7e707096c16f79c73826888eae2134c636d1a7c3` |
| tensor.zag | 136 | `c095dd0eb5d984d930f69dd0c23b71d93fbdb24b40503865e243a09470685c79` |
| fixtures.zag | 128 | `016a1df108fe2b67e6fe6e0a1cadc9050a366c78946d81791d12b9ae0c0ebf51` |
| evaluator.zag | 64 | `4d3aa059fc0b9e8a339a7eec6e0f9bfa48fef4011599fe9cd5021ac25d047244` |
| oracles.zag | 94 | `cfa75207a6b83c755e51844e1a7e730f0d5faa49cf1be80d018f1156b47f13cb` |
| refusals.zag | 171 | `75b8d5b2c2a4a4347aee31fd7fdaf926bd164db93542e0d4df3bf0bbeeaa8ee2` |
| matrix.zag | 139 | `29bf59f60124fd07d20d13424aefe5f8bc9e856e15aadc1a2d6b682e55006939` |
| inventory.zag | 92 | `4dee6708704e729092ce024d5e3ca90b56741d63664063d167df883918089987` |
| driver.zag | 55 | `91d18b45e556574964a80e7d916d7469b0cf773621acf7bc97710f8ed5bdf036` |
| DESIGN.md | 224 | `13249640855a26915aebd9fa502e954c6944f1aabadd804b8f70ec714d93e6f7` |
| CONFIG.json | 90 | `e08076edd2b073c0a3721bb0e5b1058db8a2a564c646239ceac68e88abca4d12` |
| INDEPENDENT_INITIAL_REVIEW.md | 205 | `1d6caae05614b1963470e706f5412a817882db24ccacdc4d2a3664489de9f83b` |
| INDEPENDENT_ORACLES.md | 524 | `661945bc7b285fcce89ca47b7303e49ab9bbba282fccfec03428fe62573eb40e` |

Contract: `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md`, 40 lines,
SHA-256 `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e`.

### Frozen dependencies

Each file below is from `Research/R33_NATIVE_N12_NUMERIC_VIEWS/BUILD_03/`.
Each compares byte-for-byte equal to BOTH final N13 build copies, 14 successful
comparisons. This is source identity, not a repeat execution of N12.

| File | Lines | SHA-256 |
| --- | ---: | --- |
| views.zag | 220 | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| binding.zag | 53 | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` |
| mapio.zag | 117 | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` |
| inert.zag | 237 | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` |
| R33_NATIVE_IO_V1.zag | 118 | `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` |
| R33_NATIVE_SHA256_V2.zag | 89 | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| R33_NATIVE_PROCESS_V3.zag | 337 | `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89` |

### Builds, parent and retained preflight evidence

Both final `BUILD_01/n13` and `BUILD_02/n13` are 759680 bytes, compare equal,
and freshly hash to
`17864ff77dc5cf50114341b01d1badb2c63baf66589842b82876527a07d6131d`.
Both compile.stderr files are empty. The task owner reports both compilation
processes settled exit 0; the retained compile.stdout files describe the builds.
This reviewer did not invoke either binary or the compiler.

Compiler `Research/toolchain/znc_macos_arm64_7cacbfc0` freshly hashes to
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`.
Recorded flags are `--target macos-arm64 --no-zagd --no-analyze
--no-foreground-cache`. Host macOS 26.6.2/build 25G83/arm64 is owner-reported;
it was not independently re-queried in this review.

Original `Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl`
freshly hashes to
`31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`.
CONFIG and frozen binding retain map-manifest identity
`b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f`.

The retained PREFLIGHT_01 stdout logs contain the stated 198/217/138/103/17
OK entries, total 673, with no non-OK lines found and all five stderr files
empty. This is inspection of retained verification results, not a fresh
rehash of every one of the 673 underlying artifacts by this reviewer.

| Retained evidence under N13 directory | SHA-256 |
| --- | --- |
| BUILD_01/compile.stdout | `140715a6c0a6fe924ec3b122577dada3b160429dbb3db828e4081a1f8a4d9f0a` |
| BUILD_02/compile.stdout | `a46a8ad4c5c80f1cf469a35d6f5e84e49c9b1bad9177d90011032fc9df254faf` |
| PREFLIGHT_01/n10-artifacts.stdout | `091118302fec9f6167afe263aec19ab790fd3963864600ba0ebf9137853d043a` |
| PREFLIGHT_01/n11-artifacts.stdout | `6b750818d304a15bdb023ddb6b70412cfeabc8ffb07df75011957c4b05ae8586` |
| PREFLIGHT_01/n12-artifacts.stdout | `6f7fd23fdaa37d62a83d178d4c825607d6a32bb0662739a88bb76fa6857af689` |
| PREFLIGHT_01/n12-sources.stdout | `5f8fe7390fba58d0659086b2ba4541fba691c896f3e9648b81148d06305f0e91` |
| PREFLIGHT_01/n12-closeout-snapshot.stdout | `8dc9bf6d662fd70ea632dda7b83586066ea11875b5ecc312e4872ff226a90be2` |

Saved semantic-reference identities were also freshly confirmed unchanged:

| File under REFERENCES/ | SHA-256 |
| --- | --- |
| torch_v2_9_0_storage.py.txt | `ed06de01cc398ad7f428b472049f07944ae892aa1a10d88bd66bba97de4bc785` |
| torch_v2_9_0_utils.py.txt | `b52db634d2378395685499de1fbb2b3a1bef21bb87677d830792179b492edc75` |
| torch_v2_9_0_serialization.py.txt | `7fe6755ba65409b510e75e0435a33f444c893a82ea817ff618a5be5943298a3c` |
| torch_v2_9_0_serialization.cpp.txt | `e960f3d18debb8642bcbdc6612831e0f67876a63647b3727e1cb86edda006d35` |

## 9. Closeout: preserved original snapshot and later unapproved amendment

The main agent reported the dot-key defect during this review and requested
that the original candidate remain the review target. The proposed correction
was the independently derived literal PID-key offset 160, with compact carrier
length 198 and payload offset 194. R1 records the defect in the original source;
it is not silently withdrawn because a later source version exists.

At closeout, fresh source/document hashes confirm that PREREVIEW_V1 preserves
all nine candidate Zag files plus DESIGN.md and CONFIG.json with exactly the
section 8 identities. Both BUILD_01/matrix.zag and BUILD_02/matrix.zag still
hash to the original matrix identity
`29bf59f60124fd07d20d13424aefe5f8bc9e856e15aadc1a2d6b682e55006939`.
The preserved PREREVIEW_V1/BUILD_AND_REVIEW_HISTORY.md was read in full and
hashes to `8ae4e62f4384ed3a288d9fb4db188c1f897a8e23dd6f54c4da2507ae66900297`.
That authoring history is retained context, not new execution evidence.

The live-file differences inspected for this temporal annotation are:

| Live file | Observed amendment | SHA-256 at closeout |
| --- | --- | --- |
| matrix.zag | Eight inserted lines special-case the dot key to offset 160 and check carrier length 198, payload offset 194 and byte 160 equal to 46 when length is 198. | `50a623bf93890e04f4ace0d72b56045ee610aa73c9b95ab2f8ec591afae82ac1` |
| DESIGN.md | Five inserted lines document the dot-carrier constants and first-occurrence-search defect. | `faf1eaba10aa0b98a86c19fc192663cdb89ef59c9fd5884357a42202ba38801b` |
| CONFIG.json | Identity unchanged from the original review. | `e08076edd2b073c0a3721bb0e5b1058db8a2a564c646239ceac68e88abca4d12` |

These observations record the later correction and establish the separation
between original and revised identities. They are not a focused revised-source
review or approval. Original BUILD_01/BUILD_02 evidence does not certify the
amended live candidate. A subsequent review must bind the revised source,
evaluator, design, config and new build identities; a dot-key correction alone
does not resolve R2--R4.

The original review remains REQUEST_CHANGES / NOT APPROVED FOR PREREGISTRATION.
Only this report was edited at closeout. The initial review and independent
oracle remain unchanged. No compiler, fixture, primary, inherited experiment,
registry, implementation or admission action was performed or authorized.

This report's own digest is supplied in the handoff after saving and readback,
not self-embedded. Its disposition applies only to the exact reviewed candidate.
