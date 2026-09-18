# R33 N13 independent focused final review V2

Date: 2026-09-06.
Candidate: `r33-native-n13-strict-legacy-torch-views-v1`, corrected source identities below.

**Disposition: APPROVE_FOR_PREREGISTRATION.**

R1-R4 are resolved by source inspection, and A1/A2 are addressed. No unresolved
in-scope blocker was identified in this corrected candidate. Approval is limited
to narrow, prospective native read-only descriptor-view engineering qualification
of the exact source, evaluator, design, config and build identities in this report.
It is not a passing experiment result or authorization to execute anything.

The original final review remains REQUEST_CHANGES for its original snapshot.
This separate report does not rewrite that decision, the independent oracle,
or any consumed N10/N11/N12 evidence.

## 1. Scope and evidence

Read `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` first. Continued from the
prior independent review, read all nine current N13 source files and complete
DESIGN/CONFIG, inspected their differences from PREREVIEW_V1, and reviewed the
immutable oracle and seven frozen dependency sources. Inspection included
source reads, retained build-log reads, artifact hashes and byte comparisons.

No Python, alternative-language evaluator, runtime import, stored reducer,
compiler invocation, fixture/test, primary, training, registry or implementation
operation was performed. The only new write is this V2 report. Successful builds
are retained artifacts, not executions by this reviewer; original build-command
exit-zero settlement and absence of fixture exposure are owner-reported.

The declared API accepts a trusted, live, immutable, validated ParentMap and
unique owning handles. Review does not expand this into arbitrary-pointer,
concurrent-writer, allocator-generation, hostile-host or runtime-authority safety.
Saved official PyTorch v2.9.0 material remains an inert semantic reference, not
identification of the parent's historical version or proof of behavioral parity.

Unless otherwise stated, file references are relative to
`/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/`.
Line references identify the exact current sources pinned in section 7.

## 2. Disposition of prior findings

### R1: CLOSED -- independently fixed dot-key provenance

`matrix.zag:25` overrides the general key search with literal PID-key offset
160 for key `.`. It checks blob length 198, payload offset 194, and byte 160
equal to 46 after the length guard. `matrix.zag:50` compares the row key address
against the outer blob start plus that literal offset, not the first STOP at 14.
Dot fixture setup at `matrix.zag:116` retains payload `2e 80 02 52` and literal
unsigned word pairs `(46,0), (128,0), (2,0), (82,0)`.

Independent static extent arithmetic agrees with `fixtures.zag:72`: the first
three records end at 121; the compact ByteStorage PID record has 54 bytes and
ends at 175; the single-dot-key list has 11 bytes and ends at 186; the eight-byte
count ends at 194; the four-byte payload ends at 198. The PID text starts at 160.
The longer ByteStorage type name shifts the corresponding A16 key start by one;
the shorter key changes later extents. No expected offset is obtained from
`ts_decode`, `ts_open` or `ts_row`. DESIGN and CONFIG pin the same constants.

### R2: CLOSED -- physical truncation and artificial capacity are distinct

`storage.zag:48` checks the physically remaining four length bytes before the
record-cap remainder. `storage.zag:51` does the equivalent checks for the
one-byte length. A physically incomplete length returns -9101; a complete
length crossing the artificial cap returns -9110. Neither length is read before
those checks. The operand-extent checks at line 59 retain the same distinction.

The four new controls at `refusals.zag:57` instantiate the independently specified
witnesses at the bounded-record surface, not the whole-blob minimum-size gate:

| Control | Exact construction and branch | Expected prefix / record status |
| --- | --- | --- |
| Four-byte length, complete | `80 02 58 f6 0f 00 00`, 4086 bytes `41`, then `58 00 00 00 00 86 2e`; total 4100. Second opcode at 4093; length bytes at 4094..4097 cross cap 4096. | -9110 / -9110 |
| Four-byte length, physically truncated | First 4096 bytes of the preceding completed fixture. Only two of the four second-length bytes remain physically present. | -9101 / -9101 |
| One-byte length, complete | `80 02 58 f8 0f 00 00`, 4088 bytes `41`, then `55 00 86 2e`; total 4099. Second opcode at 4095; length byte at 4096 is physically present but outside the cap. | -9110 / -9110 |
| One-byte length, physically truncated | First 4096 bytes of the preceding completed fixture. The second opcode's one-byte length is physically absent. | -9101 / -9101 |

The complete input must have its exact 4100/4099-byte extent before submission
or slicing. Each failure also requires empty owned nodes and root zero through
`p13_record_check`. There is no scanner allocation on these lexical-failure paths.
These are four correctly staged planned controls, not four executed passes.

### R3: CLOSED -- failed fixture construction cannot satisfy a negative oracle

`refusals.zag:10` rejects empty/odd literal specifications and requires the
generated record to equal `hex.len / 2` before counting and submitting it.
Failure to allocate `80034e2e` therefore produces a setup failure, not credit
for the unrelated empty-input rejection. The nine-byte truncation baseline is
checked before creating cuts 0..8; its intentional empty cut is not confused
with failed construction.

`evaluator.zag:22` provides explicit byte/word prerequisites. `p13_parse` checks
a completed nonempty outer fixture before scanning and returns a failed map
with -9113 on missing input. Nonempty generated-carrier checks are sufficient
for these fixed callers because `f13_finish` at `fixtures.zag:22` frees and
returns empty on any builder error; it does not return a partial successful
prefix. Deliberately malformed completed fixtures, including the short variant,
remain distinct from construction failure.

The refusal paths check fixed payload extents, completed carriers, and relevant
fingerprint/map prerequisites before expected subject rejection. In particular,
the negative-view fingerprint must have 256 bytes before `ts_open`, and the
wrong-map control requires a successfully parsed second map before testing its
binding rejection. A setup failure is sticky in the evaluator's failure count;
logging a containing grouped case before such a failure cannot make the child
pass or contribute accepted-child checks.

### R4: CLOSED -- indexed setup and coordinate prerequisites are guarded

The O13 readiness check at `oracles.zag:48` requires both 16-word oracle arrays,
count 0..16, width 1..8 and exact count-times-width payload length. The L13 check
at line 70 requires dimensions/strides/coordinates/indices capacities 8/8/128/16,
rank 0..8 and at most 16 probes. Both constructors retain their own guards before
writing arrays; these added caller guards protect subsequent setup writes.

The ordinary matrix, additional scalar, dot-key, alias and hash-boundary setups
now validate their owners before the corresponding indexed writes or slices
(`matrix.zag:81`, 103, 107, 111, 117, 119, 126, 143). Refusal shapes/strides are
checked before their first writes (`refusals.zag:82`, 107, 136, 196). Coordinate
scratch is validated before the public and unit budget-negative operations at
lines 155 and 208, so a missing coordinate allocation cannot be hidden by an
earlier budget refusal. Failure returns release already-created byte buffers,
word arrays, fingerprints, views and maps as applicable.

The positive row's hash scratch is checked, and the frozen SHA function rejects
a short output before writing it. Positive coordinate scratch has a length
guard before slicing/indexing. Some safe diagnostics can continue after a sticky
failure; that is not a passing negative control or an unchecked indexed write.
No remaining instance of the concrete R4 defect was established in this scope.

### A1 and A2: ADDRESSED

`driver.zag:23` now requires `s.failed == 0` before adding a successful child's
reported checks. Because `p13_run` begins only with zero failures, this follows
all of that child's supervisor/start/reap/exit/signal/stderr/RSS/capture/count/
terminal-marker acceptance checks. A rejected child is not credited. Checks
from previously accepted children may remain in a failed overall result, which
is appropriate; the overall pass still requires every child and final publication.

`DESIGN.md:34` now explicitly states count multiplied by scalar width payload
bytes, matching `storage.zag:117`, rather than equating element count with bytes.

## 3. Static case arithmetic and oracle fidelity

The following totals describe intended successful control flow, not measured
results. Setup assertions do not add grouped cases. The four new length-field
controls are the only case-count increase.

| Group | Independent source arithmetic | Cases |
| --- | --- | ---: |
| Matrix ordinary views | 9 nonempty payloads x 3 categories + 8 empty payloads x 3 categories | 51 |
| Extra floating flags | 2 floating types x (3 extra parameter flag pairs + 1 true-gradient tensor) | 8 |
| Extra layouts | 22 A16 layouts + 2 eight-byte scalars + dot-key storage | 25 |
| Nonfloating gradient refusals | 7 nonfloating payload fixtures x 2 flag choices; the two Bool payloads are distinct | 14 |
| Remaining matrix groups | Complete A16 carrier + 2 alias cases + hash-boundary group | 4 |
| **Matrix total** | **51 + 8 + 25 + 14 + 4** | **102** |
| Refusal framing | 17 explicit records + 9 cuts + oversized length + 5 capacity controls + GLOBAL limit + 4 new length-field controls | 37 |
| Blob/type refusals | Variants 1..26 + 2 unsupported type names | 28 |
| Grammar/layout refusals | 10 variants in 32..42 excluding 36 + 17 variants in 43..59 + 16 layout calls | 43 |
| Budget/lifetime groups | 4 open-budget + 5 public-budget + wrong-map + mutated-handle + closed-handle | 12 |
| Remaining refusal groups | Unit-charge group + 2 integer-one Boolean controls | 3 |
| **Refusal total** | **37 + 28 + 43 + 12 + 3** | **123** |
| Inventory-write / inventory-replay | One case in each separate mode | 1 each |
| Invalid mode | Silent exit 2 before case processing | 0 |

`driver.zag:50`, CONFIG's `[0,102,123,1,1]` and DESIGN's totals agree. The fixed
child dispatcher checks its case total before emitting zero-failure counts and
PASS. Compilation alone supplies none of this arithmetic or fixture evidence.

The oracle diff adds readiness helpers without changing the expected literals.
Inspection against INDEPENDENT_ORACLES confirms all 50 scalar payload/unsigned
low/high-word rows, including all eight bytes of 64-bit values, high bits, both
zero signs, NaN signs/payloads and quiet-bit-clear patterns. No float conversion
or runtime numerical-value claim is used. A16's additional 16 words agree too.

The A16 complete literal carrier remains 261 bytes: record extents 15/6/100/55/13,
count 8 and payload 64. `matrix.zag:101` independently requires length 261 and
compares every byte of the compact builder's output with that literal carrier,
then checks payload start 197 and PID-key start 159. Two failed empty builders
cannot satisfy the independent length assertion. Its row's uncached message
length remains 261 + 64 + 3 = 328; the 327/328 boundary and second handle on the
same exhausted account remain correctly separated.

The 22 A16 layouts retain their literal storage indices and small coordinate
enumerations. Product-maximum coverage uses only two probes, not enumeration of
16777216 elements. Eight-byte scalar probes, noncontiguous/overlapping/zero-stride
views and empty-view refusal semantics remain intact. The expanded floating-flag
fixtures use all supplied payload values, a previously disclosed extension.

Coverage remains finite, not an exhaustive oracle-ID or branch census. Exact
suggestions not separately instantiated still include the isolated LONG
truncation, integer-one sysinfo endian, long-size mutation, empty key list and
A16 two-axis cumulative-overrun example. Related controls are not those exact
tests. DESIGN retains this limitation; the four necessary R2 witnesses are now
included. Actual allocator injection remains explicitly NOT COVERED.

## 4. Failure provenance, bounds and ownership

F1 is closed at the source-review level. The corrected cap branches retain
-9110; temporary-map and shape allocation failures retain -9107; revalidation
causes propagate through bound/access/bits/row; -9108 binding and -9105 coordinate
failures stay separate. Inventory permits only -9101..-9104 as ordinary refused
rows. Harness setup failure is distinct and cannot become unsupported coverage.

The core tensor code is byte-identical to the original reviewed tensor source.
All axes are validated before zero-axis/product handling. Rank zero has one
element; an empty view exposes no element and accepts offsets only through the
storage count. Nonempty stride contributions are bounded by remaining storage
before multiplication/addition. Raw count/width/tail equality confines scalar
bytes to the original payload. Successful raw words are nonnegative 32-bit
halves, not sign-extended or normalized values.

The reviewed ownership discipline is unchanged: map lifetime exceeds borrowed
views; each view owns its shape arrays; revalidation's temporary view is closed;
failed partial shapes and rows are released; successful rows own independent
output. This is a source proof within the declared preconditions, not a runtime
leak measurement or protection against invalid owning copies.

F2 remains adequate for this narrow candidate. One nonreset main account per
child bounds opens 65536, records 327680, probes 16384, rows 8192, logical hash
bytes 268435456 and shape-allocation attempts 131072. Reservations precede work,
reject invalid/excessive charges, and do not roll back prior attempts. Rebinding
is included. Row hash input is charged atomically before hashing; new evaluator
fingerprint/page hashes also use that account.

The fixed separate low-budget control accounts and inherited bounded `pb_load`
work outside the new counters remain disclosed. These counters do not purport
to measure total process work, all allocations, peak memory or elapsed-time fit.

## 5. Supervisor, inventory and effect checks

Rechecked the complete driver/inventory and frozen supervisor/I/O dependencies
statically; none was run or requalified here.

The five direct-child modes and exits match CONFIG. Deadlines 5/20/20/60/60
seconds total 165 under the 180-second parent guard; actual overhead sufficiency
is unmeasured. File/capture ceiling is 1 MiB, descriptor limit 64, core limit zero,
and observed child RSS ceiling 402653184 bytes. RSS is observational, not hard
memory isolation; containment covers the direct child, not a process group.

Supervisor/setup/timer/capture failures, wrong exits, signals, nonempty stderr,
RSS failures, malformed/duplicate counts and missing PASS prevent acceptance
and subsequent child launches. Initial guard/admission failures can return 3/4
without a result JSON; an eventual authorized launcher must retain that evidence.
Final result write/close failures suppress the parent terminal PASS. A result
JSON or partial output directory alone is not completion evidence.

Inventory validates bound parent loading and its setup owners before iteration.
Only ordinary grammar/storage/layout refusal produces an ordinary refused row;
resource, allocation, binding and internal failures prevent a successful child.
Failed first probes suppress later probes; failed probes prevent successful row
publication. Per-record row/view owners are released.

The 8192-row bound fits 32 pages of 256 x 256-byte rows. Manifest capacity is
256 + 32 x 48 = 1792; the final page-entry hash ends exactly at byte 1792.
Replay reads are extent-checked by the frozen reader before positive-length
comparison, including allocation-failure paths. Page/manifest publication or
replay failure cannot become a successful refusal row. Final fingerprint,
identity or training-refusal failure may leave partial artifacts, but no PASS.

Parent count expectations remain unknown. First/last raw re-encoding is a
known-byte consistency check, not an independent behavioral oracle. Storage
deduplication uses serialized node identity, not matching keys/digests or runtime
aliasing. No supported-parameter census or full migration follows from bookkeeping.

The inspected prospective call paths write only exclusive captures, pages,
manifest and result under the designated new run directory; historical mutation,
training, stored calls, network and a foreign evaluator are not invoked. The
parent/manifest identities in CONFIG agree with frozen binding source. This turn
did not rerun inherited experiments or rehash the 673 historical artifact set;
the previous retained-log evidence is not new V2 execution evidence.

## 6. Accepted limitations and authority boundary

Actual allocator fault injection N-R01..N-R05 remains **NOT COVERED** and is
acceptable for this narrow engineering preregistration. Budget-denial cleanup
is not OOM qualification. Concrete source-level setup/provenance defects have
been addressed without using that limitation to waive them.

Preregistration should retain the exact finite schedule, counters, exclusions,
single-attempt/no-repeat discipline and failure/partial-artifact policy reviewed
here. This approval does not perform or authorize registry writes, reservation,
source freeze, fixture exposure, primary launch, admission, scientific promotion,
training, behavioral certification or parent migration. Those remain separate
required actions/gates. Changed sources/config/design/builds are not silently
approved by this report.

## 7. Exact reviewed identities

The following current identities were freshly hashed and match the owner's pins.
Each of the nine source files compares byte-for-byte equal to its copy in BOTH
BUILD_05 and BUILD_06: 18 successful source comparisons.

| Current file | Lines | SHA-256 |
| --- | ---: | --- |
| storage.zag | 119 | `008d9618c13496cfde458cf4575e022a70c0045a3e94e83848cf506358034ad2` |
| tensor.zag | 136 | `c095dd0eb5d984d930f69dd0c23b71d93fbdb24b40503865e243a09470685c79` |
| fixtures.zag | 128 | `016a1df108fe2b67e6fe6e0a1cadc9050a366c78946d81791d12b9ae0c0ebf51` |
| evaluator.zag | 76 | `ce06d2b50e2d3cb913137e1faa0c48e171032bb074b4f394bf0cbbc5a6ab71ff` |
| oracles.zag | 104 | `eaa313907f8128c723abbd263d1323002ea5d44b76321193fa74b3a6ee813900` |
| matrix.zag | 160 | `c2d6669d5dc0538739601dd10fd3334c860c1f2e655f3e206c52ba29934c9275` |
| refusals.zag | 223 | `9cf41054048b3cb67423a2d076242cceb939d40eaffe3cd820ea028c719ca310` |
| inventory.zag | 92 | `4dee6708704e729092ce024d5e3ca90b56741d63664063d167df883918089987` |
| driver.zag | 55 | `89941c6d5f8c18b94b04b5f4a70f1be365dfdc81bfd62faf299b294329143aff` |
| DESIGN.md | 248 | `47f89a2e715695683697b0514a1529752b7e686cb44b8a08ab8f8afb456bd000` |
| CONFIG.json | 96 | `e012f1984a6e265973acdbee782b71a504c7274c18b2b6d5b138bdd84a3ed708` |

All transitive import declarations were inspected. The closure is these nine
N13 sources plus the seven files below, each byte-identical in both builds to
`Research/R33_NATIVE_N12_NUMERIC_VIEWS/BUILD_03/`: 14 successful comparisons.

| Frozen dependency | SHA-256 |
| --- | --- |
| views.zag | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| binding.zag | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` |
| mapio.zag | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` |
| inert.zag | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` |
| R33_NATIVE_IO_V1.zag | `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` |
| R33_NATIVE_SHA256_V2.zag | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| R33_NATIVE_PROCESS_V3.zag | `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89` |

Both `BUILD_05/n13` and `BUILD_06/n13` are 776192 bytes, compare equal, and hash to
`4678cfd0577c80dc9f8b3bb8b59309882aeca336deea4bb3458f6585d13ea46c`.
Both compile.stderr files are empty. Retained stdout identifies signed native
macos-arm64 output, 744516 text bytes, 10103 data bytes and zero external build
tools. The owner reports both original compile commands settled exit 0; these
logs are not a substitute for independent runtime testing.

The compiler at `Research/toolchain/znc_macos_arm64_7cacbfc0` was hashed, not run:
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`.
Recorded flags: `--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`.

| Retained build evidence | SHA-256 |
| --- | --- |
| BUILD_05/compile.stdout | `0af8fe6dd1331af770cee3358bb2974f925b4128a60a69a2ba8cb346ce57e396` |
| BUILD_06/compile.stdout | `41a92997ecab3ea55576a084217729a20a75bdf010c724e5e1a3fbfbbb033b0e` |
| Each compile.stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## 8. Preserved review lineage and closeout

PREREVIEW_V1's original nine sources, DESIGN and CONFIG were freshly hashed
against the identities in the original final report. Its final report compares
byte-identical to the unchanged live original report. The old sources remain
historical rejected candidates; the original verdict is not retroactively changed.

| Preserved evidence | SHA-256 |
| --- | --- |
| Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` |
| INDEPENDENT_INITIAL_REVIEW.md | `1d6caae05614b1963470e706f5412a817882db24ccacdc4d2a3664489de9f83b` |
| INDEPENDENT_FINAL_REVIEW.md and PREREVIEW_V1 copy | `d8f520cedf7e97fc6ad8a94fa4704b902f7ab60726fbd014aa73b778ed6b22b2` |
| INDEPENDENT_ORACLES.md | `661945bc7b285fcce89ca47b7303e49ab9bbba282fccfec03428fe62573eb40e` |
| Current BUILD_AND_REVIEW_HISTORY.md, read only | `f31268e5f41d941e694e585ac467172bf7d2015da9473e70c8144cecc5b9ef20` |

The new report's digest is supplied in the handoff after saving and readback,
not self-embedded. Final disposition for section 7's corrected candidate only:
**APPROVE_FOR_PREREGISTRATION; NO EXECUTION AUTHORIZATION.**
