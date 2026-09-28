# N13A bounded evaluator-fingerprint memory correction

Identity: r33-native-n13a-fingerprint-scratch-v1.
Status: implemented and double-compiled; NOT reviewed, registered, admitted or executed.

## Question and inherited boundary

Can the existing native legacy-storage qualification complete under the SAME
402653184-byte observed RSS ceiling after removing only its evaluator's
full-message fingerprint copies? N13 failed at409862144bytes. Its sole primary,
all original sources/oracles and failed artifacts remain consumed and immutable.

INHERITED_N13_DESIGN.md and INHERITED_N13_CONFIG.json retain the exact N13
grammar, ownership, work surfaces, refusal codes, original finite matrix102 and
refusals123, inventory encoding and exclusions. All those semantics remain in
force unless this document explicitly identifies a prospective N13A difference.
This is known-evidence corrective engineering, not fresh generalization,
original-method behavior, full migration, training, authentication or promotion.
Canonical R27 remains step60423/restarts0 and its bytes are never modified.

## Exact implementation delta

The13 files storage/tensor/fixtures/oracles/matrix/refusals/views/binding/mapio/
inert/IO_V1/SHA256_V2/PROCESS_V3 are byte-identical copies of N13 BUILD_05.
The inventory implementation differs only in N13A log labels. Its256-byte rows
and R33TS001 manifest format, storage identity, refusal policy and output order
are unchanged. The public reader still revalidates on access; no header cache
or global arena reset is introduced. Row/page hashes and the bound-loader
implementation remain the original allocating native SHA256_V2.

evaluator.zag adds p13_fingerprint_hash and replaces only the eight fingerprint
hash calls. One152-word/1216-byte scratch allocation is owned by each fingerprint
call and reused sequentially across its eight complete messages. Output remains
a separate owned256-byte fingerprint. Failed work reservation or hash prevents
publication of that partial fingerprint. Logical hash charges are unchanged,
attempts remain charged and prior successful charges are not refunded.

fingerprint_sha.zag allocates nothing. Its private compression routine receives
one64-byte block and the fixed workspace:64schedule words,8digest words,64round
constant words and128bytes of final padding. Every digest resets all152words,
loads the same standard constants and processes original full blocks directly.
The final remainder0..63 bytes is copied into zeroed padding; remainder>=56
uses two final blocks. The complete input length is encoded as64big-endian bits.
This computes one complete-message digest, not a digest of independent chunks.

The public helper requires live valid slices, input length0..33554360, output
at least32bytes and exactly152scratch words. Invalid extents return-7403.
Any overlap between the complete input/output/workspace slices returns-7401.
These checks precede all writes, including scratch reset. Adjacent disjoint
slices are allowed. All outputs and scratch are caller-owned; no returned
borrowed scratch digest or shared owning handle is introduced. This is not
arbitrary-pointer, concurrency, allocator-generation or hostile-host security.

driver.zag adds a10-second hash-controls child before the existing matrix.
It uses new N13A log/result/terminal labels and the exclusive N13A run root.
All complete-child acceptance and failure-containment conditions are unchanged.

## Native qualification schedule

Six direct children: invalid, hash-controls, matrix, refusals, inventory-write,
inventory-replay. Expected exits2/0/0/0/0/0 and grouped cases0/15/102/123/1/1.
Deadlines5/10/20/20/60/60seconds total175 under the unchanged180second parent
guard. Deadline overhead fit is unmeasured. All children must satisfy observed
RSS<=402653184, empty native stderr, exact capture, no signals, successful
start/reap, zero-failure count and terminal marker. File/capture cap1MiB, fd64,
core0. Direct-child containment only; RSS is not hard memory isolation.

The15 new grouped cases comprise11externally published known-answer vectors,
one256-call dirty-workspace reset group, argument/alias refusals, full input plus
seven-table fingerprint compatibility/integrity controls, and logical budgets.
HASH_ORACLE_PROVENANCE.md names exact messages, lengths, digests and retained
NIST/RFC source hashes. These were transcribed by the main author; the failed
reviewer task did NOT independently author or approve them. They are independent
published expected values, not derived from this candidate. Independent exact
source/evaluator/config review remains mandatory before registration.

Each vector also checks the frozen old SHA against the literal expected value;
that compatibility computation does not supply the oracle. Guards surround the
output and the152-word workspace. Controls include short/long/empty scratch,
short output, exact/partial input-output alias, input-scratch and output-scratch
alias, valid adjacent slices, and a physically allocated33554361-byte rejected
overmaximum input. Allocation/setup failures are sticky failures, not successful
negative controls. Actual allocator OOM injection remains NOT COVERED.

A small authored inert map is fingerprinted against all eight frozen-SHA span
digests. Each input/table span is changed individually, checked for exactly its
corresponding digest change, restored and checked for exact baseline recovery.
No reader, validation or learner runs while these isolated test bytes are altered.
Budget controls require atomic refusal, exact3-byte admission, same-account
exhaustion, retained charges after argument error and no partial fingerprint.
Direct helper argument controls and fixed low-budget accounts are separately
bounded controls, not reset production accounts or unreported inventory work.

The unchanged inventory must classify every REDUCE and create all required
pages/manifest, then a fresh process must reproduce every byte from a fresh
bound load. N13's prior228candidate observations are known, unaccepted historical
data; they are not tuned new scientific oracles. Postrun byte comparison to N13
artifacts may establish known regression compatibility but cannot rescue a
failed new gate or retroactively qualify the failed N13 primary.

## Resource argument and retained uncertainty

Under the pinned compiler, _zag_free does not reclaim allocations. This change
does not pretend otherwise. Each fingerprint still consumes256output bytes and
1216scratch bytes cumulatively, plus allocator alignment/header overhead. The
two fixed-parent fingerprints therefore request2944bytes here instead of copying
110333672 logical input/table bytes plus each old hash's working arrays.
This is source arithmetic, not measured RSS savings or promised runtime fit.

Remaining allocations include55166836requested live parent bytes/tables,
140083200cumulative header-table bytes for the known inventory's4560attempts,
3006112bytes of seen table, loader staged reads and full-message/page SHA copies,
old row/page hash scratch, independently owned rows/shapes, page65536/manifest1792,
numeric/string logging, compiler arena alignment and process/runtime overhead.
The unchanged per-child API work limits are opens65536, records327680,
probes16384, rows8192, logical hash bytes268435456 and shape attempts131072.
These are not total allocation counters. No static all-input RSS certification
is claimed. The new hash child separately allocates its33.55MB refusal input,
1MB vector, small map/control copies and finite logs; all are under its same
prospective RSS acceptance gate. No old code or compiler is rewritten.

## Build, review and launch discipline

BUILD_01 failed compilation on a test helper's mistaken value-pointer field
access, before any execution. BUILD_02 contains its planned source snapshot but
was not compiled after that failure. Both remain retained. The helper was fixed
in the live candidate; BUILD_03/04 compiled successfully with empty stderr and
byte-identical858752-byte binaries, SHA256
df5e8bfa67d75c068346f4cc6b636109ccdb3161ac272523359920f0df90d00a.
Original compiler command session64903 settled exit0/chunka6f0ca.

Compiler is the unchanged znc_macos_arm64_7cacbfc0 with SHA256
3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956.
Source-first flags: --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache.
No N13A mode has run. Review failure details are in REVIEW_BLOCKER.json.
Do not register, freeze, admit or launch this candidate until the required
independent exact-source/evaluator/config approval succeeds. Then preserve
unique one-primary reservation, exact imports/compiler/config/effect freeze and
separate admission. Retain all negatives, original-command exit evidence,
postrun identity checks and independent result review. Never retry a consumed
primary or adjust oracles/RSS thresholds after exposure.
