# N13A independent exact-source/evaluator/config review

Date: 2026-09-06.
Candidate: `r33-native-n13a-fingerprint-scratch-v1`.
Selected build: `BUILD_03/n13a`; comparison: `BUILD_04/n13a`.

**TERMINAL VERDICT: APPROVE_FOR_PREREGISTRATION.**

No unresolved in-scope blocker was found in the exact candidate identified below.
This is approval of a bounded, known-evidence engineering preregistration, not a
passing experiment, measured memory improvement, execution admission, training
grant, scientific/behavioral certification, migration or promotion. The unchanged
384 MiB observed RSS gate and 180-second parent guard remain requirements.

This report does not authorize a launch. No N13A mode was executed during review.
N13 remains a consumed failure; neither its primary nor a standalone old replay
may be retried. No obsolete standalone hash-oracle authorship is claimed.

## 1. Scope, method and evidence boundaries

Read `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` first. Read the complete
current DESIGN, CONFIG, HASH_ORACLE_PROVENANCE and REVIEW_REQUEST, the retained
inherited N13 design/configuration and the previous independent V2 review.
Read all 19 source files and their transitive import declarations. Inspected
the implementation deltas, retained build output, published reference records,
historical review lineage and relevant pinned compiler source.

All unqualified candidate-relative paths in this report resolve under:
`/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH/`.
`N13/` denotes the sibling `R33_NATIVE_N13_TORCH_VIEWS/` directory.

Fresh reviewer checks established 38 live-source/build-copy comparisons, 13
inherited-source comparisons, the inventory label-only diff, both binary
identities, important original-input/compiler hashes, and reference identities.
The retained PREFLIGHT_01 logs contain 384 source-pin, 299 artifact, 11 closeout
snapshot and 2 admission entries: 696 lines, each reporting `: OK`, with no other
log records. That is inspection of the owner's retained verification evidence,
not a claim that this reviewer independently rehashed all 696 historical entries.

The successful original compiler command's session 64903 / chunk a6f0ca / exit 0
is owner-reported. The reviewer independently inspected the retained stdout,
empty stderr, binary extents and byte equality, without invoking the compiler.
The N13A run and launch directories were absent when inspected. This corroborates
the stated pre-exposure stage; absence alone is not an execution-history audit.

No compiler, candidate function/mode, fixture, primary, reducer, training program,
Python or alternate-language/reference evaluator was executed. No agent was
spawned. Official reference streams were retrieved and artifact-hashed only;
no downloaded implementation was run and no message digest oracle was generated.
The sole new write is this report. Prior reviews, oracles, failed artifacts,
source/configuration, registry and implementation files remain untouched.

## 2. Exact delta and import closure

The following 13 files are byte-identical to N13 BUILD_05: storage, tensor,
fixtures, oracles, matrix, refusals, views, binding, mapio, inert, IO_V1,
SHA256_V2 and PROCESS_V3. Their prior bounded grammar, owner assumptions,
allocation/capacity/binding/coordinate distinctions and finite controls remain.

`inventory.zag` differs only in the printed N13A labels at lines 80-87. Its
256-byte rows, R33TS001 manifest, row order, pages, category/refusal handling,
probes, storage-node identity and read-only replay are unchanged.

The three new sources are `fingerprint_sha.zag`, `hash_controls.zag` and
`hash_vectors.zag`. `evaluator.zag:44` adds the charged fingerprint hash wrapper;
lines 49-60 replace only the eight fingerprint hashes. The old `p13_hash` remains
the row/page compatibility hashing path. Driver changes add the hash-controls
mode/schedule and new identity/output labels; they retain the acceptance gate.

The 19-file closure is complete: driver imports inventory and hash_vectors;
inventory/matrix/oracles/refusals reach evaluator; hash_vectors reaches
hash_controls and evaluator; evaluator reaches fixtures, PROCESS_V3 and the new
hash. Fixtures/tensor/storage/views/binding/mapio/inert reach frozen SHA256_V2
and IO_V1. No additional imported implementation or reference runtime is hidden
outside the listed closure. All 19 files match BOTH compiled source snapshots.

## 3. Direct-block hash and allocation mechanism

### 3.1 Digest arithmetic, padding and reset

`fingerprint_sha.zag:13` loads sixteen big-endian message words, expands the
64-word schedule, performs the standard 64 rounds and adds the working state
back modulo 2^32. The eight initial words and all 64 constants at lines 50-51
match retained RFC 6234 sections 5.1 and 6.1. The rotations, choice, majority,
small/big sigma functions and output ordering match sections 5.1 and 6.2.

Values are kept in the unsigned 32-bit range represented by positive i64 values.
The largest relevant multi-term sums and shifts fit that representation before
the 32-bit masks; this is not signed floating conversion or machine-word digest
serialization. The result is exactly 32 big-endian digest bytes.

The 152-word workspace has disjoint regions: schedule words 0-63, state 64-71,
constants 72-135, and final padding bytes 1088-1215. The public function resets
ALL 152 words before each message. Compression writes schedule/state, not the
constant region or pending second padding block.

The full-block loop at line 53 consumes exactly 64 original bytes per iteration.
The remaining 0-63 bytes are copied into the cleared 128-byte tail. The appended
0x80 and full-message bit length occupy one block for remainder below 56 and
two for remainder 56-63. Exact multiples of 64 still receive a final padding
block. The admitted maximum 33554360-byte input has a bit length of 268434880,
well within i64; the length encoding nevertheless writes all eight length bytes.
No input index crosses the admitted slice and no padding write crosses byte 127.

### 3.2 Guards and owner lifetimes

Lines 45-47 require input length 0-33554360, output length at least 32 and exactly
152 workspace words. Invalid extents return -7403. Pairwise overlap between the
complete input/output/workspace slices returns -7401 before any output or
workspace write. Empty input and adjacent disjoint slices are valid. The output
loop writes only its first 32 bytes. These are checks over trusted live slices,
not protection against forged addresses, concurrent writers or allocator reuse.

The private block routine has no independent public argument contract; its
callers here always supply an exact 64-byte block and validated workspace.
Constant-load failure is separately fail-closed before digest output; unlike
extent/alias refusal, that internal path follows workspace reset. The literal
constants and loader extents reviewed here make that path unreachable under the
declared valid-slice assumptions.

`evaluator.zag:49` allocates an independent 256-byte result and one 1216-byte
workspace. Scratch-allocation failure releases the result owner. A hash/budget
failure stops later hashes, releases scratch and suppresses the partial result.
Success releases scratch and returns only the independently owned result.
Nothing returns a digest slice borrowed from scratch. Logical close remains
distinct from physical arena reclamation under this compiler.

### 3.3 No hidden per-block heap allocation identified

The new hash call graph uses scalar arithmetic, borrowed slices, literal tables,
`ns_rotr`, `ns_load_words`, `ns_hex_word`/`ns_hex_digit` and `_zag_slice_ptr`.
None of those paths allocates message/work storage. Frozen allocating
`ns_sha256` is not called from the new digest function.

The retained compiler source was checked beyond the high-level call graph.
In `R33_N13_POSTRUN_MEMORY_DIAGNOSIS/REFERENCES/acodegen_7cacbfc0.zag.txt`,
`ac_slot_scratch` at 528 reserves compile-time frame slots; string literals at
1410 use static data plus frame descriptors; ordinary subslices at 1597-1638
also use frame descriptors, not a heap allocation. Function frame sizing at
3364 includes these slots. `_zag_slice_ptr` at 2460 only loads the data pointer.
The separately emitted heap `__make_slice` routine at 3802 must not be confused
with the ordinary subslice lowering used by this hash loop.

The saved compiler source compares exactly to the immutable local Zag commit
7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c source. That commit's bootstrap/znc
artifact freshly hashes to the selected compiler hash. This is source/artifact
binding, not a new self-host rebuild, formal compiler proof or runtime trace.

## 4. Independent verification of published oracle transcription

The main author transcribed these vectors. This reviewer verified the complete
hex messages and digests against the retained original records, including the
163-byte long message, and checked the RFC ASCII/repetition constructions.
The vectors are independently published expectations, not expectations produced
by either hash implementation or by a prior independent-agent authorship report.

Fresh retrieval of the official NIST archive and RFC text produced the same
artifact hashes as their retained files. Streaming extraction of each selected
NIST member compared byte-for-byte equal to the retained member, including its
CRLF representation. Source selectors and exact reference hashes are pinned
below and in HASH_ORACLE_PROVENANCE.md.

| Case | Official selector / exact construction | Input bytes | Expected SHA-256 |
| --- | --- | ---: | --- |
| 1 | ShortMsg Len=0; actual empty input, not placeholder Msg=00 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | ShortMsg Len=8, Msg=d3 | 1 | `28969cdfa74a12c82f3bad960b0b000aca2ac329deea5c2328ebc6f2ba9802c1` |
| 3 | ShortMsg Len=440 | 55 | `6595a2ef537a69ba8583dfbf7f5bec0ab1f93ce4c8ee1916eff44a93af5749c4` |
| 4 | ShortMsg Len=448 | 56 | `cfb88d6faf2de3a69d36195acec2e255e2af2b7d933997f348e09f6ce5758360` |
| 5 | ShortMsg Len=504 | 63 | `18041bd4665083001fba8c5411d2d748e8abbfdcdfd9218cb02b68a78e7d4c23` |
| 6 | ShortMsg Len=512 | 64 | `42e61e174fbb3897d6dd6cef3dd2802fe67b331953b06114a65c772859dfc1aa` |
| 7 | LongMsg first record, Len=1304 | 163 | `3c593aa539fdcdae516cdf2f15000f6634185c88f505b39775fb9ab137a10aa2` |
| 8 | RFC SHA256 TEST1: ASCII abc, no NUL/newline | 3 | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| 9 | RFC SHA256 TEST2_1, exact 56-byte ASCII pattern | 56 | `248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1` |
| 10 | RFC SHA256 TEST4: 01234567 repeated 80 times | 640 | `594847328451bdfa85056225462cc1d867d877fb388df0ce35f25ab5562bfbb5` |
| 11 | RFC SHA256 TEST3: byte 61 repeated exactly 1000000 times | 1000000 | `cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0` |

NIST records are CAVS 11.0, byte-oriented, generated March 15, 2011; Len is in
BITS, not bytes. ShortMsg record starts are retained lines 8, 12, 228, 232, 260
and 264; LongMsg starts at 8. RFC patterns are at 5138-5150 and the selected
SHA256 expected values at 5425-5442. Hash-vector construction reproduces TEST4's
64-byte pattern repeated ten times through its equivalent eight-byte repetition.

The smaller fixed set is acceptable for this narrow preregistration. Separate
literal lengths 65, 119, 120, 127, 128, 129 and 112 are explicitly NOT covered.
The 112-byte pattern in other RFC hash families is not misattributed as a
verified SHA-256 vector. There is no official CAVP validation claim. Expected
answers remain the published literals even though the frozen old hash is also
checked against them for compatibility.

## 5. Evaluator controls, setup provenance and budgets

`hash_vectors.zag` validates the 154-word guarded pool and 64-byte output owner
before slicing or indexed writes. Each vector requires its literal message
length and both 32-byte expected/reference allocations. The 640-byte pattern
allocation is checked before indexed construction. The million-byte fill is
bounded by its actual slice and must subsequently pass its exact length check.
Bad setup creates a sticky failure; an expected negative cannot erase it.

`hash_controls.zag:34` performs exactly 256 dirty-workspace calls, alternating
fixed abc and empty expectations and checking output guards. Vector calls also
start with poisoned workspace. Input length and digest changes therefore cannot
legitimately depend on prior message state. Separate guards surround the
workspace in the vector and refusal stages. The reset subgroup does not have
its own final workspace-canary assertion before the refusal subgroup re-poisons
the pool; this is a finite coverage limitation, not a claimed exhaustive guard
test. The reviewed write bounds and the other guarded calls leave no blocker.

The refusal group at line 48 covers short output; short, overlong and empty
scratch; exact/partial input-output alias; input-scratch and output-scratch
alias; unchanged output/workspace after refusals; and valid adjacent slices.
The overmaximum control physically allocates 33554361 bytes and verifies that
extent before calling the subject. It is not a forged huge slice or an OOM
control. Valid adjacent processing after the negative calls checks reset/reuse
and leaves the adjacent abc input unchanged.

The fingerprint integrity group at line 86 uses a complete inert five-byte
pickle, `80024b012e`, and the unchanged scanner/validator. Its old-hash reference
covers, in order, input, nodes, edges, memo, stack, marks, globals and histogram.
These are exactly the eight full spans used by the new fingerprint, including
array capacity rather than just active prefixes. The complete 256 bytes match
the eight frozen-hash results and retain the same logical byte charge.

Each span's nonempty prerequisite precedes mutation of byte zero. The original
byte is restored immediately after the new fingerprint call and before any
check, subsequent reader operation or owner release. A complete changed result
must differ in exactly the corresponding 32-byte segment, with all seven others
unchanged. A fresh restored fingerprint must match the entire reference.
The retained baseline remains independently owned across these scratch reuses.
This isolated fixture mutation does not broaden the production reader's trusted
immutable-map contract or modify canonical parent data.

For this small map the full span sum is 88069 bytes: input 5, nodes 40960,
edges 32768, memo 2048, stack 1024, marks 1024, globals 8192, histogram 2048.
The fixed 88068-byte account permits the first seven charges, totaling 86021,
then denies the final histogram charge and must return no partial fingerprint.
The corrected BUILD_03 helper uses the actual histogram byte slice to express
that expected retained charge; the earlier value/pointer compile defect is absent.

The budget group at line 114 requires -9111 and no counter increment for a
three-byte message under allowance two, exact success/charge at three, and
same-account exhaustion thereafter. A separate three-byte account tests -7403
after successful reservation for invalid output and retains all three charged
bytes. Extent/alias/budget negatives preserve output and workspace as specified.

The main per-child TsWork limits stay opens 65536, records 327680, probes 16384,
rows 8192, hash bytes 268435456, shape attempts 131072. Charges precede work and
are not refunded after later error. Fixed limited-control accounts and direct
helper argument controls are explicitly separate; inherited pb_load work remains
outside these counters and inside the process deadline. The counters are not
total memory-allocation counters. The unchanged A16 row charge is 261+64+3=328.

Actual allocation-fault injection remains **NOT COVERED**. Budget-denial cleanup
is not OOM evidence. The lack of injected allocator failures is acceptable for
this bounded engineering preregistration, with that exclusion retained and all
unexpected allocation/extent failures remaining fatal to acceptance. It would
not support an allocator, arbitrary-pointer or comprehensive failure certificate.

## 6. Independent static count reconciliation

These are source-level arithmetic checks, not inferred from successful builds
and not observed N13A execution results.

| Stage | Static decomposition | Grouped cases |
| --- | --- | ---: |
| invalid | Silent expected exit 2, no work group | 0 |
| hash-controls | 11 published vectors + reset + refusals + fingerprint integrity + budgets | 15 |
| matrix | 51 base storage/tensor/parameter views + 8 floating flag views + 25 layout/scalar/dot views + 14 nonfloating gradient refusals + complete carrier + 2 alias groups + hash budget | 102 |
| refusals | 37 framing/capacity + 28 blob/type + 43 view/layout + 12 budget/lifetime + 1 unit group + 2 integer-as-Boolean | 123 |
| inventory-write | One known-parent inventory | 1 |
| inventory-replay | One fresh-process inventory comparison | 1 |

Total grouped cases across the six stages are 242, not 242 individual assertions.
The hash child has 1011 prospective checks on its all-success path: 2 initial
setup + 99 vector + 2 vector workspace guard + 770 reset + 21 refusal + 104
fingerprint + 12 budget + 1 dispatcher case-count check. Failure paths need not
reach that count. The dispatcher still requires exactly 15 completed hash groups
and zero failures, under the unchanged 16000-check ceiling.

The inherited matrix/refusal details were checked in current source, not merely
copied from old prose. The 37 framing cases include the four previously required
length-width controls; 43 view cases are 10+17 grammar variants plus 16 layout
cases. The earlier dot-key fix remains literal PID offset 160, payload 194,
blob length 198. Independent A16 remains a full 261-byte comparison, PID offset
159 and payload 197. Complete near-cap records of 4100/4099 bytes return -9110;
their physically truncated 4096-byte companions return -9101. Prior source,
oracle and negative-setup fixes are preserved, not silently reverted.

## 7. Supervision, acceptance, inventory and filesystem effects

`driver.zag:31` schedules invalid/hash-controls/matrix/refusals/inventory-write/
inventory-replay at 5/10/20/20/60/60 seconds. The sum is 175 seconds, leaving
five seconds within the 180-second parent guard for overhead, whose actual fit
has not been measured. PROCESS_V3 retains its before-fork kernel timer and
direct-child kill/reap handling; gettimeofday is optional reporting, not its
deadline authority. No descendant/process-group containment is certified.

Every attempted child must pass supervisor status, start, reap, expected exit,
zero signal, empty stderr, positive observed RSS at most 402653184, and complete
capture. Exit-zero work children additionally need one valid zero-failure count
record and their terminal CHILD_PASS. The invalid child instead requires silent
exit 2. The child's own dispatcher asserts its exact declared group count.

Critically, `driver.zag:24` credits verified child checks only AFTER all acceptance
checks succeed. A resource-rejected child's reported checks are not credited.
`p13_run` immediately returns after a sticky parent failure, preventing the next
child launch. The later six-child check reports the resulting incompleteness;
it cannot rescue or overwrite the original failure.

Read the complete frozen PROCESS_V3 failure paths: allocation and name setup,
root/open/type failures, kernel queue creation/registration, fork/exec/redirect
failures, wait/timer errors, kill/reap outcomes and capture/size inspection.
Errors remain nonzero or fail expected exit/start/reap/capture checks. Failed
preflight and partial output creation are not qualified child completion.
The inherited direct-child/no-hard-memory-isolation limitations remain explicit.

Inventory still treats only -9101 through -9104 as ordinary unsupported rows.
Allocation, capacity, binding, probe, budget and unexpected row failures are
not downgraded to unsupported coverage. Page/manifest/seen/coordinate setup
checks gate the processing loop. Pages remain at most 65536 bytes, 256 rows each,
32 pages / 8192 rows; manifest bounds are 256+32*48=1792 bytes. Replay checks
exact read sizes and every page/manifest byte, without replacing retained files.
Views/rows close before map/raw owner release. Full before/after fingerprints,
parent identity and the training-refusal check remain required.

The new effects are confined to the exclusive N13A run root, child captures,
inventory pages/manifest and NATIVE_RESULT.json, with the separately managed
launch-evidence directory described by CONFIG. Original inputs and old runs are
read-only. Fixed file/capture 1 MiB, fd 64 and core 0 limits remain unchanged.
Root admission failure and early guard failure may produce no result JSON, so
the later launch record must retain actual original-command stdout/stderr/exit.
Result JSON explicitly describes counters before publication; result-write or
root-close failure suppresses the final parent PASS. JSON alone is insufficient.

## 8. Resource judgment and qualification limits

The narrow correction removes the fingerprint-specific full-message copy and
per-hash allocated schedule/state/constants paths. Its source request is 256
output + 1216 scratch = 1472 bytes per fingerprint, 2944 for the two inventory
fingerprints, before alignment/header overhead. Their unchanged logical inputs
sum to 110333672 bytes. This is an allocation-mechanism argument, not a measured
RSS subtraction or a promise that the next run will pass.

Pinned compiler `_zag_free` at source line 2129 still does not reclaim; the
allocator at 3540 uses nonreclaiming bump arenas. Unchanged cumulative pressure
includes the known 140083200 header-table bytes, 55166836 live parent/input-table
bytes, 3006112 seen-table bytes, loader staging/full-copy hashes, row/page hashes,
row/shape owners, 65536/1792 page/manifest buffers, logs and runtime overhead.
Those known inventory figures are not tuned fresh-science expectations. The
new hash child also carries the actual overmaximum input allocation and its
million-byte vector. Its own RSS and ten-second gate remain independent tests.

The smaller official vector set, lack of a successful maximum-length literal
case, finite reset/canary coverage and unqualified actual OOM injection limit
the claim. They do not invalidate the reviewed narrow source mechanism. No
post-hoc threshold increase, counter reset, grammar change, allocator reset or
old-run promotion is justified. N13's terminal FAIL_CONSUMED remains intact.

## 9. Exact reviewed identities

All following candidate source hashes were freshly checked, including a repeat
after substantive inspection; each source matches BUILD_03 and BUILD_04.

| Source | SHA-256 |
| --- | --- |
| fingerprint_sha.zag | `964b124853742cff257fb1e528aff8ada9492d7cf9ead7f0608e14c4b0ab9392` |
| hash_controls.zag | `0f2a9901534437fba32141e805024596592cc33eb7a23301b7715304f8482e0d` |
| hash_vectors.zag | `cd4c87bece2fd9d6f52a5431b92367920be9a3cb96b54e230ae65b19cdcafc73` |
| evaluator.zag | `6ca7b1a275a819f1459e6fbb752245b0a8d0da037373a5834bdc60162d14f675` |
| driver.zag | `ac4a3aa2f15e031e6b15c35194eae23987be36f016041a0ebee6caed7e0a19e9` |
| inventory.zag | `033d02ecfffe5bb2e4c0ff30f36345580f2eb0328146c8640258a0ab3b7c786b` |
| storage.zag | `008d9618c13496cfde458cf4575e022a70c0045a3e94e83848cf506358034ad2` |
| tensor.zag | `c095dd0eb5d984d930f69dd0c23b71d93fbdb24b40503865e243a09470685c79` |
| fixtures.zag | `016a1df108fe2b67e6fe6e0a1cadc9050a366c78946d81791d12b9ae0c0ebf51` |
| oracles.zag | `eaa313907f8128c723abbd263d1323002ea5d44b76321193fa74b3a6ee813900` |
| matrix.zag | `c2d6669d5dc0538739601dd10fd3334c860c1f2e655f3e206c52ba29934c9275` |
| refusals.zag | `9cf41054048b3cb67423a2d076242cceb939d40eaffe3cd820ea028c719ca310` |
| views.zag | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| binding.zag | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` |
| mapio.zag | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` |
| inert.zag | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` |
| R33_NATIVE_IO_V1.zag | `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` |
| R33_NATIVE_SHA256_V2.zag | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| R33_NATIVE_PROCESS_V3.zag | `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89` |

| Document | SHA-256 |
| --- | --- |
| DESIGN.md | `e8e009b795e3e7c5557adfa32bc985a1f103e1c78e377daaded67ea54b984f9d` |
| CONFIG.json | `6a7c39db3d6cbad473012c9125d11ac053493d649249e93005882a495a059ba7` |
| HASH_ORACLE_PROVENANCE.md | `d8cabbb2575ab107beb26154b97a9926bde31b4c220d7ffdf591458f0cd9a809` |
| REVIEW_REQUEST.md | `4e899a3d61c92c64e6755287cebd9fd51f30c383fbbe6191a9191f0182a04e7f` |
| INHERITED_N13_DESIGN.md | `47f89a2e715695683697b0514a1529752b7e686cb44b8a08ab8f8afb456bd000` |
| INHERITED_N13_CONFIG.json | `e012f1984a6e265973acdbee782b71a504c7274c18b2b6d5b138bdd84a3ed708` |

Both binaries are 858752 bytes and byte-identical, SHA-256
`df5e8bfa67d75c068346f4cc6b636109ccdb3161ac272523359920f0df90d00a`.
Both compile.stderr files are empty, SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Retained stdout identifies signed macos-arm64 output, 816144 text bytes,
14293 data bytes and zero external build tools.

| Build evidence | SHA-256 |
| --- | --- |
| BUILD_03/compile.stdout | `5933f6d0dad8b7a563e62a3d5aa287c806e45d3da62b0431eeda1c85a30e6f34` |
| BUILD_04/compile.stdout | `6e3dbc2ff494c0f65837476129e295d66e41713a1f933d55022d31aed894cbb4` |
| BUILD_01/compile.stdout | `c64c99a8448f99b1baf17560e4feeb9b81f3470da86d3a174f69ff0efcfc159e` |
| BUILD_01/compile.stderr | `dce099626b483c84c7d44ea288acd8c99040477e9096b0cded0764c14f9c19b2` |

BUILD_01's `arm64: unknown field: len` failure and BUILD_02's uncompiled source
snapshot remain history. The inspected helper correction replaces invalid
value-pointer access with `p13_word_bytes(p.hist)` and its byte length. Neither
failed/uncompiled snapshot is an approved or exposed execution candidate.

Compiler path: `Research/toolchain/znc_macos_arm64_7cacbfc0`, SHA-256
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`.
Recorded flags: `--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`.

| Retained official reference | Bytes | SHA-256 |
| --- | ---: | --- |
| REFERENCES/shabytetestvectors.zip | 4909729 | `929ef80b7b3418aca026643f6f248815913b60e01741a44bba9e118067f4c9b8` |
| REFERENCES/SHA256ShortMsg.rsp | 10299 | `75e1cb83994638481808e225b9eb0c1ebd0c232d952ac42b61abce6363be283c` |
| REFERENCES/SHA256LongMsg.rsp | 426209 | `6fac36f37360bcf74ffcf4465c18e30d6d5a04cc90885b901fc3130c16060974` |
| REFERENCES/rfc6234.txt | 236573 | `8f39f02a57bfd1da15634706724a585766e6223f77ecdaf243cad16cd3a1aa1b` |

Provenance URLs are the exact official endpoints recorded in the pinned
HASH_ORACLE_PROVENANCE.md: the NIST CSRC secure-hashing page and
`https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/shs/shabytetestvectors.zip`,
plus `https://www.rfc-editor.org/rfc/rfc6234.txt`. Archive/member hashes pin the
retrieved bytes even if a serving endpoint later changes.

| Historical/input anchor, relative to Research | SHA-256 |
| --- | --- |
| R33_NATIVE_ONLY_EXECUTION_CONTRACT.md | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` |
| R33_NATIVE_N13_TORCH_VIEWS/INDEPENDENT_FINAL_REVIEW_V2.md | `81cdb899a26306cfc0beecead2268f8e5aa553b542d658fc168db04d49791b3e` |
| R33_NATIVE_N13_TORCH_VIEWS/POSTRUN_INDEPENDENT_REVIEW.md | `f5ffe72118bcacae5d21f1b4db810d952db7c9c51c8e8b108e59a837ebb19dfa` |
| R33_NATIVE_N13_TORCH_VIEWS/INDEPENDENT_ORACLES.md | `661945bc7b285fcce89ca47b7303e49ab9bbba282fccfec03428fe62573eb40e` |
| R33_N13_POSTRUN_MEMORY_DIAGNOSIS/REFERENCES/acodegen_7cacbfc0.zag.txt | `cf4d60fc0778a1982324c01d11966ad6360bf6ee0e0f49246423645c71663596` |
| R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl | `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a` |
| R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/manifest.bin | `b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f` |

## 10. Disposition and remaining gates

The independent source-review gate is satisfied only for section 9's exact
candidate. Preregistration, unique reservation, full input/import/compiler/
configuration/effect freeze and separate launch admission remain distinct owner
steps; none was performed here. Changed sources, vectors, configuration or
executables are not silently covered by this approval.

Any later attempt must retain its original-command settlement, all negative and
partial artifacts, complete child acceptance, exact output/input identity checks
and independent postrun review. Only an accepted measured run can establish the
new candidate's RSS/deadline result. No N13 failure credit is retroactively
upgraded, and no learner or canonical state authority follows.

**APPROVE_FOR_PREREGISTRATION; NO EXECUTION AUTHORIZATION.**
The report's own hash is supplied after save/readback, not self-embedded.
