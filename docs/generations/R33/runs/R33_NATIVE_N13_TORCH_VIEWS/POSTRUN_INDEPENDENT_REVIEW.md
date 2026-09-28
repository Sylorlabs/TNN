# R33 N13 independent postrun review

Date: 2026-09-06.
Consumed candidate: `r33-native-n13-strict-legacy-torch-views-v1`.
Selected executable: `BUILD_05/n13`; comparison executable: `BUILD_06/n13`.

**TERMINAL VERDICT: FAIL_CONSUMED -- INVENTORY_WRITE_RSS_LIMIT_EXCEEDED.**

The parent correctly rejected the fourth child and did not launch inventory
replay. Preserve this sole attempt as failed engineering evidence. Neither a
retry of N13 nor a standalone replay is authorized. This report is not approval
of an unwritten correction, a new preregistration, admission, or scientific or
behavioral certification.

## 1. Scope and inspection method

Read `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` first. Read FREEZE.json,
ADMISSION.json, PREREGISTRATION.md and the complete existing V2 final review.
Inspected the complete bounded native and launch logs, the selected source
paths governing acceptance and allocation, retained postrun hash-verification
logs, output extents/digests, and the inventory manifest as inert bytes.

Whole child logs were scanned, not just their terminal summaries: every distinct
record and its multiplicity was inspected, with identical repeated records
compacted for display. Case and summary records were also read in source-file
order with line numbers. Whole-file searches found no unequal CHECK record in
any child log and no unexpected child-log record format. Inventory's repeated
row-copy records were inspected in their original run-length order. These are
operational inspections of retained text, not a replacement numerical evaluator.

All paths below are relative to `/Users/Shared/micah/Documents/TNN/TNN/` unless
specified. `N13/` abbreviates `Research/R33_NATIVE_N13_TORCH_VIEWS/`; `RUN/`
abbreviates `Research/R33_NATIVE_N13_RUN_PRIMARY_V1/`; `LAUNCH/` abbreviates
`Research/R33_NATIVE_N13_LAUNCH_PRIMARY_V1/`.

No primary, child, compiler, test, reducer, Python, alternate-language numerical
runtime, training or inherited experiment was executed. No agent was spawned.
No source, config, oracle, prior review, registry or consumed artifact was edited.
The sole write is this new report. An optional combined read-only inspection was
blocked before returning evidence; a subsequent simple manifest byte read
succeeded. No result is claimed from the blocked inspection.

## 2. Frozen acceptance and observed terminal result

FREEZE and ADMISSION bind the 384-entry manifest, V2 approval, selected binary,
five-child schedule, exact case totals, resource limits, and the single-attempt
failure policy. The preserved preregistration requires ALL child acceptance
checks, result publication/close, parent terminal PASS and outer exit zero.
Child exit zero and result JSON alone are expressly insufficient.

The retained launch interval is 2026-09-06T22:27:14Z through 22:27:45Z, with
`exit_code.txt` equal to 1. The task owner identifies the settled native command
as session 72555, chunk 3e3256, exit 1. That session identifier is owner-supplied;
this reviewer did not poll or relaunch it. Retained files support one recorded
supervisor invocation, and the frozen rule consumes the identity on that attempt.
This verdict does not assert that registry closeout has already been performed.

| Child | Observed exit | Native CHECK / CASE records | Child-reported failures | Peak RSS, bytes | Parent acceptance |
| --- | ---: | --- | ---: | ---: | --- |
| invalid | 2 | 0 / 0; empty captures | Not applicable | 1392640 | Accepted expected refusal mode |
| matrix | 0 | 8166 / 102 | 0 | 218349568 | Accepted |
| refusals | 0 | 1059 / 123 | 0 | 29868032 | Accepted |
| inventory-write | 0 | 7168 / 1 | 0 | 409862144 | Rejected: RSS gate |
| inventory-replay | Not launched | None | Not measured | Not measured | Not evaluated |

All four attempted children have supervisor status zero, started=1, reaped=1,
signal=0 and empty native stderr. No child timeout is reported. The three
work-child count records are unique, end with zero failures, and each has its
own terminal CHILD_PASS. The parent still rejects inventory-write because its
resource check is an independent requirement.

The decisive difference is exact:

`409862144 - 402653184 = 7208960 bytes = 6.875 MiB`.

Observed peak is 390.875 MiB against the frozen 384 MiB cap. Do not round this
down, raise the cap, subtract allocator overhead, or substitute another memory
metric. The supervisor reads `usage[4]` in frozen PROCESS_V3 at line 155; driver
line 17 compares that value against the frozen ceiling. The allowed outer
`time -lp` output separately reports the same maximum RSS. Its differently
named peak-memory-footprint field is not the preregistered acceptance metric.
Outer timing text in host.stderr is not nonempty native child stderr.

LAUNCH/native.stdout:40 contains the failed RSS check. Line 44 then reports
`all_five_children_completed,4,5`. The latter is a consequence of the intended
fail-stop, not a second independent cause requiring an attempted replay.
The JSON's two parent failures are therefore correctly attributed.

## 3. Count acceptance and failure containment

The selected `driver.zag:12` returns before launching another child when the
parent failure count is nonzero. Inventory-write fails RSS at line 17 before
line 23 can credit its reported checks. The subsequent replay call at line 32
therefore performs no launch. The complete directory listing contains neither
inventory-replay.stdout nor inventory-replay.stderr, and the parent log has
exactly four PROCESSV3 records.

The accepted-child check total is exactly `8166 + 1059 = 9225`. Inventory's 7168
checks remain observable diagnostics but are not accepted-child credit. The sum
16393 of all three reporting children's CHECK records must not be relabeled as
verified accepted checks. Invalid mode contributes no child checks. There are
four attempted/reaped children but only three accepted modes, including invalid.

The native parent emits 40 checks before result publication: 9 invalid-mode
checks, 10 for each of the three work children, then the all-five check. Result
write and root close add two successful checks, giving 42 total parent CHECK
records and still two failures. Thus the JSON names
`parent_checks_before_result_write=40` and
`parent_failures_before_result_write=2` are accurate, not truncated final counts.

Result publication and output-root close succeed. Driver line 40 then returns
1, before the terminal parent PASS at line 41. No
`R33_N13_BOUNDED_TORCH_VIEW_ENGINEERING_PASS` appears. This is a completed,
recorded failure, not an open invocation, missing result, crash or replay timeout.
A1's revised accepted-count gate worked on the resource-failure path.

The observed matrix/refusal totals agree with the pre-exposure static 102/123
schedule. Their logs retain the dot-key and A16 comparisons, the four new
length-field controls, and allocation/setup prerequisites. Their successful
partial results do not turn this failed aggregate primary into qualification.
Actual allocator-fault injection remains NOT COVERED.

## 4. Inventory observations and artifact status

The rejected child reports 7089 classified REDUCE nodes, comprising 228 declared
Torch candidates, all supported by its narrow descriptor grammar, and 6861
other reducers. It reports 76 storage, 76 tensor and 76 parameter descriptors,
76 unique serialized storage nodes, 152 shared references, 456 first/last probes,
zero empty views and zero probe failures. Descriptor-wise bytes are 9738528;
unique storage-node bytes are 3246176; logical descriptor elements are 2434632.
These are labeled observations from an unaccepted inventory stage, not an
approved parameter census, runtime alias claim, migration or behavioral recovery.

The 7168 checks reconcile directly with source: 8 setup checks + 7089 row-copy
checks + 56 page-hash/write checks + 7 aggregate accounting checks + 2 integer
serialization checks + 1 manifest-write check + 4 final integrity/close checks
+ 1 case-count check. Probe successes do not add per-probe CHECK lines; only
probe failures would do so. No such failure appears.

Observed work remains below every separate work allowance:

| Inventory counter | Observed | Frozen main allowance |
| --- | ---: | ---: |
| Opens, including revalidation | 7773 | 65536 |
| Header-record attempts | 4560 | 327680 |
| Coordinate/bit probes | 456 | 16384 |
| Owned-row attempts | 228 | 8192 |
| Logical hash-input bytes | 131682668 | 268435456 |
| Shape-allocation attempts | 1824 | 131072 |

This proves neither total allocation headroom nor RSS headroom. Inherited loader
work is outside these counters, as disclosed before exposure.

All 28 page files and the manifest exist: pages 1..27 are 65536 bytes each;
page 28 is 45312 bytes, or 177 rows. Hence `27*256+177=7089` and page bytes total
1814784. The 1600-byte manifest equals `256+28*48`; total page-plus-manifest bytes
are 1816384. Header identity fields match the pinned parent and N10 manifest.
Its 28 ordinal/row/byte entries and all embedded page digests agree by inspection
with fresh operational hashes of the retained files. Reserved header/entry bytes
inspected are zero. This is artifact integrity inspection, NOT fresh-process
rederivation of descriptor rows. The required replay never happened.

Retain all pages, the manifest, native result, four capture pairs, and every
launch file as failed-attempt evidence. They must not be admitted as a recovered
parent or used to claim replay success. Do not delete them to make the exclusive
run path available again, launch replay alone, or switch to the comparison
binary to retry the consumed identity.

## 5. Source-grounded memory finding

### M1: repeated temporary allocation is not reclaimed by the pinned ARM64 backend

The relevant original compiler source was read from the local repository
`/Users/Shared/micah/Documents/zag`, immutable commit
`7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c`, rather than a later working-tree
allocator implementation. The commit's `bootstrap/znc` bytes freshly hash to
the exact selected compiler SHA-256. This binds the repository snapshot and
bootstrap artifact; it is not a new self-host rebuild or compiler-parity test.

In `selfhost/native/arch/aarch64/acodegen.zag:2129`, lowering `_zag_free` evaluates
its argument and returns zero without reclaiming memory. Lines 2140 onward do
the same for string free. `_zag_malloc` routes to the arena allocator at line
2152. `ac_emit_alloc` at line 3540 onward allocates from 64 MiB bump arenas,
grows by another mapping when needed, and explicitly never frees incrementally.

The relevant source connections are concrete:

| Call path | Allocation behavior |
| --- | --- |
| IO_V1:5,12 and inert.zag:15,20 | `nio_alloc`/`pm_words` use `_zag_malloc`; their free wrappers call the non-reclaiming `_zag_free`. |
| storage.zag:62 and inert.zag:31 | Every successfully framed header calls `pm_init` with new 128-node/256-edge/128-memo/64-stack storage, including globals and histogram. Closing clears the owner but does not reclaim arena bytes. |
| tensor.zag:88,101,117 | Access/row binding reopens the descriptor, repeating header allocation. This is intentional revalidation, not an identity cache. |
| SHA256_V2:28,47,81 | Every hash allocates and writes a padded copy of the entire input plus 512/64/512-byte working arrays; final frees do not reclaim these bytes. |
| evaluator.zag:43,54 | Each fingerprint hashes the full input plus all seven resident tables, before and after inventory. |
| mapio.zag:73 and IO_V1:79 | The bound loader also allocates page/hash scratch and a staged read buffer for each read, outside the new work counters. |

The seven header-map arrays request exactly 30720 bytes per successful
initialization: `10240+8192+1024+512+512+8192+2048`. For the observed 4560
header-record attempts, which in this successful child all reach these
initializations, that is 140083200 bytes of cumulative requested table storage,
before allocator headers, alignment and other allocations. The observed
131682668 logical hash bytes likewise entail at least that much cumulative
padded-copy storage in the current SHA paths, before hash working arrays and
the inherited loader's separate hashes. These allocations are zeroed/copied,
not merely address-space reservations left untouched.

The parent-map header reports 375763 nodes, 244250 edges and 175954 memo slots.
Its loaded raw bytes and seven arrays require 55166836 requested bytes before
metadata, staging and allocation overhead. Two fingerprints alone therefore
cover 110333672 logical bytes. The seen table adds another 3006112 requested
bytes. These static extents show substantial known allocation pressure without
invoking a numerical evaluator or inferring it from compilation.

This establishes a source-level accumulation mechanism consistent with the
measured failure. It does not identify a unique instruction at which the peak
occurred, provide a byte-exact RSS decomposition, or show that one particular
scratch replacement will necessarily bring a new run under the cap. There is
no per-allocation trace in this attempt. No injected OOM or allocation-null
failure was observed; exceeding an observational RSS gate is not an OOM test.

The V2 review did not qualify physical reclamation or measured RSS fit. Its
source-level cleanup statements must not now be interpreted as proof that the
selected machine allocator returned memory for reuse. This report records that
limitation explicitly while preserving the earlier immutable review unchanged.

## 6. Bounded correction advice -- proposal only

A new native candidate should change memory lifetime, not the 402653184-byte
RSS threshold, descriptor semantics, oracle values or rejection criteria.
Adding more calls to `nio_free`/`pm_free_words` cannot fix this backend's
non-reclamation. Neither generic allocator-library names nor a different
compiler's later free implementation establish behavior under this pinned toolchain.

The defensible bounded mechanism is explicit reusable temporary workspaces or
a bounded reclaiming region/pool implemented natively for the new candidate:

1. Separate long-lived immutable parent data and independently owned public
   views/rows from short-lived header parsing, hash and I/O scratch. Bound the
   workspace/pool and allocate it once; reset/reuse only after every temporary
   owner in that lifetime has finished. Do not reset the compiler's global bump
   cursor, unmap an interior bump allocation, or invalidate a live sibling view.
2. Reuse a header-map workspace with the SAME 128/256/128/64 capacities. Clear
   all seven tables, histogram, memo state, stack/marks, roots and counters before
   the next exact-prefix scan. Record memo independence must remain real. Shared
   scratch may only be internal: a public owning ParentMap returned by an API
   must not silently become a borrowed buffer overwritten by the next call.
3. Use bounded reusable SHA scratch or a native streaming SHA implementation
   which retains the exact SHA-256 of each complete message. Process original
   64-byte blocks directly and bound final padding storage; do not hash chunks
   separately and combine their digests. Reset digest state for every message.
   A reusable working-state allocation avoids accumulating even a fixed small
   allocation on every hash. A full-message scratch alternative must be sized
   for the largest admitted message, including resident node-table fingerprints,
   not merely a storage blob. Dropping fingerprints is not a correction.
4. Preserve independent lifetimes for all public owned outputs. A reclaiming
   native region allocator is an alternative when transparent owner lifetimes
   are needed: retain the allocator-issued base/extent, validate allocation and
   release outcomes, and return only that owner's region to reuse. Newly mapped
   region release must not be simulated by `_zag_free`. Keep this within the
   declared trusted-owner API; no arbitrary-pointer security expansion is needed.

The new resource argument must include bound-loader staging/hashes, the live
parent arrays, header workspace, simultaneously live view/row owners, page and
manifest buffers, fingerprints, logging/string allocations, and compiler/runtime
overhead. Any still-used bump allocation must be included cumulatively. A fixed
workspace is useful only when it is actually reused rather than allocated again
per record. If scratch management changes inherited dependencies, use distinctly
versioned copies/imports and a new freeze; do not edit N10/N11/N12 or N13 history.

Preserve parse/binding revalidation, exact input ranges and bytes, both raw words,
empty/noncontiguous/overlapping views, serialized identity, node ordering, owned
row disjointness, failure causes, publication rules, and full replay requirements.
Charge the same logical work surfaces, including each header attempt and the
uncached A16 `261+64+3=328` hash bytes, even when storage is reused. Do not disguise
workspace exhaustion as ordinary unsupported input or reset budgets on reclamation.
Any changed physical-allocation accounting requires explicit prospective naming
and reconciliation, not silent changes to the existing counter interpretation.

Necessary prospective evidence includes source-level lifetime/reset bounds,
fresh native controls for reuse without stale memo/hash state or output aliasing,
exact hash/row-byte compatibility, failure cleanup/provenance, and full-process
RSS evidence at the SAME cap. SHA padding boundary controls must be independent
of the replacement hash code. Known N13 input/result exposure must remain
disclosed; preserved N13 tests are not to be rerun or relabeled fresh evidence.
The continuing no-repeat contract governs the new candidate's separately reviewed
fixture plan and admission. Actual allocator-fault injection remains NOT COVERED
unless a new expressly reviewed native mechanism supplies it.

This is justified correction advice, not an implementation, measured saving,
approval of new source, or authority to start experiments. No particular new
candidate has been written or reviewed by this report.

## 7. Identity verification and required closeout

Fresh reviewer hashes match the selected/comparison binaries, compiler, nine
current N13 sources, config, design, contract, parent raw bytes, N10 map manifest,
all earlier review/oracle identities, FREEZE/ADMISSION and preregistration.
Both builds still compare equal; 18 live-source/build comparisons and 14
N12-origin/build import comparisons succeed. No evidence of candidate drift was
identified. Prior V2 section 7's nine-source and seven-import hashes remain the
exact source identities used here, not repinned or replaced identities.

The main agent's retained postrun verification files contain 384 freeze-pin OK
lines, 2 admission-pin OK lines, and 198/217/138/103/17 historical OK lines
(673 historical, 1059 combined entries), with no non-OK lines and empty stderr
for all seven groups. This reviewer inspected those complete verification logs
and freshly hashed the important objects listed here; this is NOT a claim to
have independently repeated all 1059 underlying comparisons. Hash agreement
preserves evidence custody but cannot rescue a failed resource gate.

Closeout must record the consumed failure, exact RSS excess, accepted counts,
unlaunched replay and unaccepted inventory artifacts. Preserve the complete
384-entry freeze manifest and two-entry admission manifest unchanged. Add this
report, all failed-run artifacts and verification logs to a NEW postrun artifact
and historical-closeout snapshot through the single writer. Update the continuing
journal, handoff and consumed/experiment bookkeeping as failure, not success;
this reviewer has not made those writes or certified their completion.

### Decision and source identity anchors

| Object | SHA-256 |
| --- | --- |
| Research/R33_NATIVE_N13_PINS.sha256 | `e4524aee001b396c6b2cdc06fc970e9612ccca14d125fba852bc13e99fa32ab6` |
| Research/R33_NATIVE_N13_ADMISSION_PINS.sha256 | `b5d006543dab22e124d8ac322ec6986f35816af2d722794b00b687c7a8461573` |
| N13/FREEZE.json | `23de99c6708a1d3d9315948cd2746ca7db67b41a62a8c06d9357599fc4225cf7` |
| N13/ADMISSION.json | `64ec5d8eff6d46730177d3fd46b8c7fae3f98748b325d2e90df6fa3d9f05b4ca` |
| N13/PREREGISTRATION.md | `310ed629e4a87dccc0241236c0b8f0877a980413a0b4a746c76eaf38769d16d2` |
| N13/INDEPENDENT_FINAL_REVIEW_V2.md | `81cdb899a26306cfc0beecead2268f8e5aa553b542d658fc168db04d49791b3e` |
| N13/INDEPENDENT_FINAL_REVIEW.md | `d8f520cedf7e97fc6ad8a94fa4704b902f7ab60726fbd014aa73b778ed6b22b2` |
| N13/INDEPENDENT_INITIAL_REVIEW.md | `1d6caae05614b1963470e706f5412a817882db24ccacdc4d2a3664489de9f83b` |
| N13/INDEPENDENT_ORACLES.md | `661945bc7b285fcce89ca47b7303e49ab9bbba282fccfec03428fe62573eb40e` |
| N13/BUILD_05/n13 and BUILD_06/n13, each 776192 bytes | `4678cfd0577c80dc9f8b3bb8b59309882aeca336deea4bb3458f6585d13ea46c` |
| Research/toolchain/znc_macos_arm64_7cacbfc0 and commit bootstrap/znc | `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956` |
| N13/DESIGN.md | `47f89a2e715695683697b0514a1529752b7e686cb44b8a08ab8f8afb456bd000` |
| N13/CONFIG.json | `e012f1984a6e265973acdbee782b71a504c7274c18b2b6d5b138bdd84a3ed708` |
| Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` |
| Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl | `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a` |
| Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/manifest.bin | `b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f` |
| Commit 7cacbfc0 selfhost/native/arch/aarch64/acodegen.zag; allocation excerpts inspected | `cf4d60fc0778a1982324c01d11966ad6360bf6ee0e0f49246423645c71663596` |
| Same commit selfhost/std/allocator.zag; read as source, not invoked | `c80e9dac7e43ed6266d80a3f0e7ae967bdd66d56e7dd8a3375c0a2a55a7cf839` |

### Complete native and launch log identities

| Object | Lines / bytes | SHA-256 |
| --- | --- | --- |
| RUN/matrix.stdout | 8277 / 255462 | `d897b65f9906c6bf94a0901f700be9190a18f10ba77dfc7f4b2e761c860f7db9` |
| RUN/refusals.stdout | 1191 / 38637 | `532bda0ae8d614f6386e58d70a5dcce385cd4271281847bdb6b43831331d36c2` |
| RUN/inventory-write.stdout | 7194 / 208868 | `3d844b499eee0eb92986984054d1f6288730e1c1bac92b07b61bb486db5c0be9` |
| RUN/invalid.stdout and all four native stderr files | 0 / 0 each | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| RUN/NATIVE_RESULT.json | Retained failure result | `9370c9373b78165550403c90adae98ce34f1d3b8a1643188c769251d14b6d82a` |
| RUN/torch-manifest.bin | 1600 bytes | `3f56153b9d9e1d6b9c8f3f9af05f8d2f47a88d83bad5d7b91b577c00d0888c33` |
| LAUNCH/native.stdout | 64 / 2125 | `a9ff5cfdc3533e1318b8fe1ef42df3f30f62dc6fa3de07b47d5c065f5eb7d9fb` |
| LAUNCH/host.stderr | 20 / 755 | `3b650a0ab66ee29244db4dadcc1fa2c3d5dcf30f1c777509731af15226bbecae` |
| LAUNCH/start_utc.txt | 1 / 21 | `0757ef0219f8229209c56f5eb708a9946e6f77fd9c211711e54f3c0464c300fd` |
| LAUNCH/end_utc.txt | 1 / 21 | `60db7e0c323643ab33dc0b9d8890b647d2974161c8e78415383b676afee4237f` |
| LAUNCH/exit_code.txt | 1 / 2 | `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865` |

### Retained postrun verification identities

All paths are under Research/, with prefix `R33_NATIVE_N13_POSTRUN_`.
All corresponding stderr files are empty and have the empty-file digest above.

| stdout suffix | OK lines | SHA-256 |
| --- | ---: | --- |
| PINS.stdout | 384 | `4771cfefcef9d38cdcadbfb84e2be2c5659fefa45841ea0bdadebdb78c779bd8` |
| ADMISSION.stdout | 2 | `1697f066e078bea8921182cfafcb6d86f4f319819edad30986136ba9ff2596a0` |
| N10.stdout | 198 | `091118302fec9f6167afe263aec19ab790fd3963864600ba0ebf9137853d043a` |
| N11.stdout | 217 | `6b750818d304a15bdb023ddb6b70412cfeabc8ffb07df75011957c4b05ae8586` |
| N12.stdout | 138 | `6f7fd23fdaa37d62a83d178d4c825607d6a32bb0662739a88bb76fa6857af689` |
| N12_SOURCES.stdout | 103 | `5f8fe7390fba58d0659086b2ba4541fba691c896f3e9648b81148d06305f0e91` |
| N12_CLOSEOUT.stdout | 17 | `8dc9bf6d662fd70ea632dda7b83586066ea11875b5ecc312e4872ff226a90be2` |

The 28 fresh page digests were checked against the complete retained manifest;
that pinned manifest binds their exact ordinal/digest list. They still require
inclusion as files in the single writer's new artifact-closeout manifest. No
scientific replay or descriptor regeneration is inferred from those hashes.

## 8. Terminal handoff

**N13 is consumed and failed.** Matrix and refusal child evidence is retained;
inventory-write is resource-rejected; inventory-replay is unexecuted. Accepted
child checks remain 9225, not 16393. Parent exit is 1 with no terminal PASS.

The source-grounded next engineering issue is non-reclaiming temporary memory
under the pinned ARM64 allocator. A new bounded native reclamation/reuse design
must preserve the same RSS cap and semantics and undergo its own review and
prospective gates. No unwritten correction is approved here. Parent continuity,
training, migration, scientific promotion and broader R33 completion remain
unestablished by this failed primary.

This report's own digest is supplied only after saving and readback, not
self-embedded. All earlier reviews, inputs and consumed output remain unchanged.
