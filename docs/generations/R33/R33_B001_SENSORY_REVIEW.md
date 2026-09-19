# R33-B001 independent sensory / architecture review

Status: independent code/design review for the next corrective batch. No experiment,
fixture, training run, qualification run, registry edit, canonical mutation, or learner
authority change was performed by this review.

## Evidence boundary

Executed evidence available to this review is limited to the already-completed B000
primary result. B000 reports one fixture exposure, zero training runs, no canonical
mutation, no learner authority grant, and `sensory_qualification=false`. Its native
result matches all five preregistered defect witnesses:

- distinct visual arrays can collapse to the same relational signature;
- an impulse between acoustic sample positions can be invisible to the sampled distance;
- the 8,193rd trace attempt is dropped while the recorded count remains 8,192;
- short segmentation/reconstruction capacity returns a partial result without a failure;
- an all-protected LRU set still returns slot 0 as an eviction candidate.

Those are executed negative witnesses for the copied legacy helpers only. Everything
below is independent source/design analysis and a proposed falsification boundary for
new R33 code. It is not executed evidence.

## Strongest criticism

The most dangerous false positive for B001 is to implement a bounded exact copy of a
native numerical array and call that "raw sensory ingress." Copying `[]i32` values
exactly proves only array transport after an upstream producer has already chosen the
encoding, sign interpretation, channel order, sample/frame boundaries, dimensions,
stride, and metadata. It cannot detect a parser that swapped channels, lost signedness,
normalized samples, reordered pixels, accepted inconsistent lengths, or fabricated a
numerical feature array before the R33 boundary.

S0 therefore has to begin at an encoded byte boundary (or an equivalently explicit
physical sensor byte contract), not at a pre-decoded feature array. The source bytes,
their declared encoding, and their physical metadata must remain independently
recoverable. Derived `i32`/feature views may be created beside that record, but they
cannot be the evidence used to prove raw identity.

## Minimum actual S0 evidence

The minimum credible S0 certificate for one admitted encoding is a bounded native path:

`source bytes -> validate metadata -> owned immutable RawRecord -> save -> fresh-process reload -> exact bytes + exact metadata`

For the exact configuration under test, require all of the following:

1. Hash and length the original source byte sequence before parsing. Do not compute the
   reference only from the post-parse numerical representation.
2. Admit the bytes through the same public native ingress API intended for R33.
3. Record exact payload bytes plus encoding/version, dimensions, channel order, sample or
   pixel format, stride/layout, clock domain, timestamps/order IDs, source provenance,
   and declared transform lineage.
4. Retrieve the stored payload and compare byte-for-byte and field-for-field with the
   independent source reference.
5. Save the record, terminate the native process, reload in a fresh native process, and
   repeat the exact comparisons, including cursor/order state where applicable.
6. Demonstrate explicit rejection for malformed or out-of-envelope inputs. A rejected
   observation must not become an ordinary successful record, partial record, silent
   truncation, or eviction.

An `i32` decoding can be tested as an additional view, but exact equality of that view
is not a substitute for steps 1-6.

## Minimum actual S1 evidence

S1 needs to show that a distinction present in the admitted source bytes remains
available to the learner, not merely that the archive can reproduce bytes.

Use evaluator-only paired counterexamples whose source encodings differ in exactly one
controlled item while all unrelated metadata is held fixed. At minimum:

- audio: one signed PCM sample differs, including a sign-only or least-significant-bit
  difference at a location missed by the legacy 12-point sampler;
- vision: one pixel/channel byte or a coordinate permutation differs while histogram or
  legacy invariant summaries can remain equal;
- temporal: one event-order/timestamp field differs while payload values are otherwise
  equal.

For each pair, prove both (a) exact raw decode/retrieval differs at the intended location
and (b) a diagnostic raw bypass exposes that location to an available learner input with
the downstream mechanism held fixed. If only the evaluator can inspect the raw record,
S0 may pass while S1 remains unproven.

The bypass is a qualification intervention only. It must not inject the evaluator's
answer, semantic boundary, object ID, phoneme/word label, or target class.

## API preconditions that should be contractual

The new ingress/record API should validate preconditions before any committed mutation:

- recognized encoding/version and byte order;
- bounded payload length and bounded metadata length;
- dimensions/channel/frame/sample counts whose checked product exactly matches the
  declared payload layout;
- checked arithmetic for `count * channels * bytes_per_item`, offsets, strides, and
  destination sizes; integer overflow is a hard error;
- valid sample/pixel width and signedness for the declared encoding;
- valid channel order / plane order / stride with no implicit default that changes the
  interpretation of bytes;
- sample rate or equivalent time base in the declared allowed domain;
- explicit clock domain, event/order identifier policy, and tie/reorder rule;
- destination capacity sufficient for the entire atomic record, or an explicit
  `INSUFFICIENT_CAPACITY(required=...)`-style result;
- payload integrity/hash metadata either verified or explicitly marked absent; a hash
  mismatch is never an ordinary observation;
- ownership/aliasing semantics defined at the API boundary;
- any derived representation that depends on a codebook/model carries an immutable
  version/digest binding to that exact dependency.

Malformed preconditions must fail before incrementing record counts, modifying protected
state, consuming an eviction candidate, advancing a durable cursor, or exposing a
partially admitted observation.

## Required falsification tests

### 1. Byte ingestion versus numerical-array copying

Provide a literal encoded byte record and an independently computed source digest. Pass
the bytes through the real ingress/parser. Verify stored bytes and decoded values. Then
construct the same decoded `i32` values directly and show that this second route is
reported as a different lineage/boundary, not accepted as evidence that the byte parser
worked.

Falsifier: a parser defect can be introduced conceptually (wrong endian, swapped channel,
signed-to-unsigned interpretation) while the prebuilt numerical array still passes. If
the test suite would remain green, it is not an S0 ingress test.

### 2. Signed PCM extrema and sign preservation

For an explicitly declared little-endian PCM16 record, include byte encodings for
`-32768`, `-1`, `0`, `1`, and `32767`, plus alternating extrema. Require exact decoded
signed values and exact byte reserialization. Repeat a paired S1 test where only `-1`
versus `+1` changes.

Falsifier: abs/rectification, unsigned interpretation, clipping, normalization, or
endianness reversal must fail exact comparison rather than merely changing a distance
score.

### 3. Metadata / length inconsistency

Reject, without partial commit:

- empty payload where the selected modality forbids it;
- payload one byte short and one byte long for declared shape;
- channel count zero or outside the envelope;
- invalid/unknown encoding version;
- stride smaller than a row/frame or inconsistent with payload length;
- metadata claiming more samples/frames than physically present;
- trailing bytes when the encoding contract forbids them;
- arithmetic-overflow shapes/length products;
- invalid timestamp/time-base combinations;
- corrupted payload hash or metadata digest.

For every rejection, compare pre/post record count, protected-memory digest, cursor,
and destination sentinel bytes. They must be unchanged.

### 4. Capacity boundary and atomicity

For every bounded store/transport/reconstruction operation test `required-1`, `required`,
and `required+1`, plus zero and declared maximum capacity.

At `required-1`, require an explicit failure and the exact required size if the API can
report it. No prefix may be presented as a successful observation. At `required`, the
entire record must commit. At `required+1`, the unused tail must remain untouched or
specified. Also test a request beyond the maximum envelope and checked size arithmetic
overflow.

This boundary is essential because B000 already demonstrated that the legacy
segmentation/reconstruction helpers silently return prefixes when output capacity is
short.

### 5. Aliasing / ownership

The architecture contract calls for an immutable payload reference. That is not enough
unless ownership is explicit.

Tests required:

- ingest from a caller buffer, mutate the caller buffer afterward, and prove the admitted
  RawRecord is unchanged;
- retrieve a payload view and prove callers cannot mutate the canonical stored bytes, or
  that retrieval returns an owned copy with explicit semantics;
- test exact source/destination alias and partial overlap if the API accepts mutable
  buffers; otherwise require explicit rejection before mutation;
- admit two records from the same caller buffer reused at different times and prove the
  first record does not change when the buffer is reused;
- save/reload and prove no pointer/address identity is required for payload identity.

If R33 intentionally uses borrowed storage, then the owner lifetime and immutability
guarantee must be part of the protected contract and tested. A borrowed mutable slice is
not an immutable sensory record.

### 6. Protected-memory selection

For a full exact-memory store:

- all slots protected -> explicit refusal/spill status and no selected victim;
- mixed protected/unprotected -> victim is always unprotected;
- no protected slots -> deterministic policy result;
- zero slots -> explicit no-capacity result;
- tied ages -> deterministic documented tie break;
- malformed length/count mismatch -> rejection, not out-of-bounds selection;
- failure to place a new raw record -> existing protected record bytes and metadata stay
  bit-identical.

Capacity pressure may produce an explicit degraded/rejected observation, but must never
silently reinterpret `protected_exact` as an eviction preference. B000's all-protected
selection of slot 0 is the executed negative witness this change must eliminate.

### 7. Stale codebooks / dependency versioning

Exact RawRecord identity should not depend on a chunk/codebook at all. If a derived
compressed or segmented view references one, bind that view to the exact codebook
version and digest.

After encoding a derived view, test:

- codebook entry value changed;
- entries reordered with otherwise identical values;
- codebook truncated;
- an ID reused for different content;
- same nominal version with a different digest;
- version/digest unavailable after fresh-process reload.

Each mismatch must return an explicit `STALE_CODEBOOK`/dependency error for the derived
view. It must not silently reconstruct different content. The immutable raw payload must
remain retrievable and exact despite the stale derived view.

This directly addresses the legacy `r31_reconstruct` dependency on live `c_len/c_data`
arrays and prevents a passing same-process round trip from being mistaken for durable
reversibility.

### 8. Ordering and temporal metadata

Use otherwise identical records with strictly increasing IDs, duplicate IDs, tied
timestamps, out-of-order timestamps, and explicit reorder-policy variants. Verify that
the admitted ordering exactly matches the declared policy and survives save/reload.

Do not use wall-clock arrival alone as the oracle. Record the clock domain and ordering
rule. An implementation that silently sorts by timestamp, silently accepts duplicates,
or changes tie order must fail S0 for a contract that promised deterministic order.

### 9. Derived-loss raw-bypass test

Re-use the already-established defect shapes as adversarial S1 pairs: visual permutation
twins and an acoustic impulse located between legacy sample positions. Require the
derived legacy route to be allowed to collide while the new raw route preserves and
exposes the difference.

This is stronger than replacing one lossy summary with another: it demonstrates that
loss in an optional abstraction does not destroy the admitted source evidence.

## Principal confounds to exclude

1. **Post-parse oracle confound.** Hashing or comparing only the decoded numerical array
   cannot detect parser/encoding mistakes. The source-byte oracle must be independent.
2. **Fixture-construction confound.** Constructing `[]i32` samples directly in Zag skips
   the physical byte/metadata boundary that S0 is supposed to qualify.
3. **Same-process alias confound.** A round trip can appear exact because both sides
   reference the same mutable memory or codebook. Mutate the source and use fresh-process
   reload.
4. **Capacity-prefix confound.** Equality on the returned prefix can hide omitted tail
   data. Success requires declared completeness and exact total length.
5. **Codebook-self-consistency confound.** Encoding and decoding against the same mutable
   live codebook proves internal consistency at one instant, not durable reversibility.
6. **Evaluator leakage confound.** The raw-bypass diagnostic may select a coordinate to
   inspect, but it must not supply the correct semantic answer or hidden target label.
7. **Derived-view substitution confound.** A preserved raw archive that is inaccessible
   to the learner can pass storage checks but not S1 information availability.

## Recommended architecture change

Make the exact sensory record a first-class substrate object separate from every learned
or hand-authored representation:

`RawRecord = owned immutable bytes + exact physical metadata + provenance + integrity + order identity`

Derived numerical arrays, signatures, chunks, embeddings, PAM inputs, and learner-created
abstractions should reference the RawRecord and declare their transform/dependency
lineage. They must not overwrite or become the sole representation of the admitted raw
record during the qualified retention horizon.

Ingress should be transactional: validate all lengths/metadata and reserve complete
bounded storage first; then copy/commit atomically. Capacity failure returns an explicit
status without partial mutation. Protected exact-memory selection must return "no legal
victim" when all candidates are protected. Derived codebook-backed representations must
carry immutable dependency version/digest bindings, while raw recovery remains codebook-
independent.

This is the minimum architecture that makes the S0/S1 claims falsifiable rather than
dependent on naming a post-processed array "raw."

## Concrete B001 component candidate review

Status: bounded read-only code/API/test review of `R33_B001_COMPONENTS.zag` and
`R33_B001_C01_DRIVER.zag`. Neither file was compiled or executed by this review. No
fixture has run. This section assesses a **COMPONENT engineering regression candidate**,
not full B001, S0 natural ingress, persistence, or learner qualification.

### What the source design does improve

By inspection, the candidate directly addresses several B000-era component defects:

- `r33_pcm16le_decode` validates channel/rate bounds, even byte length, channel-aligned
  sample count, destination capacity, and byte-carrier range before copying decoded
  values to the caller. The signed conversion for PCM16LE is source-correct by inspection:
  unsigned values `32768..65535` are mapped by subtracting `65536`.
- `r33_pcm16le_encode` pre-validates signed i16 range and capacity and stages the encoded
  bytes before output mutation.
- `r33_rgb8_ingest` bounds width/height to `1..64` before `width*height*3`, requires exact
  payload length, validates each byte carrier as `0..255`, and uses staged exact copy.
- `r33_order_accept` requires one fixed clock ID, the exact next ordinal, and
  nondecreasing ticks; cursor mutation occurs only after all rejection checks.
- `r33_protected_lru` returns `-1` when no unprotected victim exists. The historical
  all-protected fallback is absent.
- `r33_reconstruct_exact` separates literal/chunk kind from value, so negative signed
  literals no longer collide with the historical negative-ID literal convention. It
  computes required output length before writes and refuses insufficient capacity.
- `r33_commit_logged` performs its visible validation before mutation, writes the
  five-field in-memory log record first, and updates state second. That is a valid narrow
  single-process log-before-update ordering property; its own source comments correctly
  disclaim disk durability, concurrent atomicity, authenticated authority and rollback.

These are code/design observations only. They are not regression results until a bounded
driver run is evaluated against an independent expected-output contract.

### Concrete bugs and misleading-claim risks

#### C01-01: the driver is not self-verifying

`R33_B001_C01_DRIVER.zag` records metrics/vectors but contains no pass/fail assertions for
their expected values. `main()` always emits `audit.completed=1` and returns `0` if it
reaches the end. Therefore process exit `0` or `audit.completed=1` can establish only
**driver completion**, not component correctness.

The currently present B001 file set contains no separate B001 expected-output manifest or
result parser. Before any regression-pass claim, an external evaluator must independently
assert every required status/value/invariant, or the driver must eventually gain an
equivalent bounded assertion layer. This is especially important for negative controls:
an incorrect return code is still merely printed and does not make the driver fail.

#### C01-02: exhaustive PCM roundtrip is partly self-consistency-confounded

The driver generates all 65,536 two-byte PCM codes, decodes them, re-encodes the decoded
values, and checks byte roundtrip mismatch count. This is useful coverage, but the
roundtrip alone is not an independent signed-decoding oracle: paired decode/encode bugs
can be mutually inverse and still reproduce the original bytes.

The required independent assertion is:

`decoded[i] == i` for `0..32767`, and `decoded[i] == i-65536` for `32768..65535`.

The driver currently prints all decoded values, so an external evaluator could apply that
oracle, but no such evaluator is present in the reviewed B001 files. Do not call the PCM
mapping exhaustively verified merely because `pcm.roundtrip_byte_mismatches==0`.

#### C01-03: driver output volume can invalidate the regression run

`pcm.all_i16_codes` emits 65,536 vector lines and `vision.maximum_pixels` emits another
12,288. This is far beyond the 65,536-byte per-stream output ceiling used by the already
executed B000 launcher. If that envelope or a similar bounded-output launcher is reused,
the C01 output will be truncated or terminated before the evaluator can observe the full
oracle material.

The exhaustive test should be represented by bounded independent mismatch counts,
boundary/sentinel vectors, and/or independently specified digests rather than requiring
tens of thousands of printed rows. Until the future launcher contract is known, this is
a concrete execution-design blocker for claiming the present driver is safely bounded.

#### C01-04: stale codebook detection is version-only, not content-bound

`R33ChunkBook` contains mutable `lengths` and `values` slices plus `version`, but no digest
or immutable snapshot identity. `r33_reconstruct_exact` rejects only when
`expected_version != book.version`. If codebook contents are changed or reordered while
the integer version remains unchanged, reconstruction uses the modified content and can
return success with different output.

The driver's `chunk.stale_version` control tests only a mismatching version (`6` versus
`7`). It does **not** test same-version content mutation, ID reuse, reordering, or digest
mismatch. Therefore the candidate does not yet satisfy the stronger stale-codebook
boundary described earlier in this review. Calling the codebook "frozen" is currently a
caller convention, not an enforced property.

Recommended architecture change remains: bind every codebook-backed derived view to an
immutable codebook identity/digest (or owned frozen snapshot) in addition to a version.

#### C01-05: this is still not a RawRecord or natural-ingress boundary

The module explicitly uses `[]i32` as byte carriers and states that it is not an OS device
driver. That scoping is correct and should remain prominent. PCM `channels` and `rate`
are validated but not stored with returned samples; RGB `width` and `height` are checked
but not persisted with the copied pixels; there is no provenance, payload hash, immutable
owned sensory record, save/reload path, or fresh-process retrieval.

Consequently C01 can support a component-engineering statement such as "bounded PCM16LE
decode/encode and RGB8 carrier-copy routines behave as specified" after execution, but
not "raw sensory ingress passed S0." The earlier byte-originated RawRecord test remains
the minimum S0 gate.

#### C01-06: `r33_exact_copy` is generic i32 copy, not byte validation

The file-level comment says byte-carrier arrays contain `0..255`, but `r33_exact_copy`
itself accepts every i32 value. The driver intentionally demonstrates this with
`raw.signed_copy`, including i32 extrema. That is a valid generic exact-copy regression,
but it is not evidence that an arbitrary `r33_exact_copy` input is a valid byte record.

The modality-specific PCM/RGB APIs do perform byte-range validation. Claims should keep
those boundaries separate: generic i32 exact-copy correctness versus validated byte-
carrier ingress.

#### C01-07: empty PCM is currently accepted

For `bytes.len==0`, valid channels/rate and any nonnegative destination capacity,
`r33_pcm16le_decode` computes zero samples and returns success. The driver records
`pcm.empty_status` but does not encode an expected result.

This is not necessarily wrong, but the contract must choose explicitly whether an empty
PCM observation is valid or malformed. Do not describe C01 as rejecting all empty or
malformed sensory payloads unless the intended empty semantics match this behavior.

#### C01-08: capacity tests exist but do not form the full boundary matrix

The driver includes useful insufficient-capacity sentinels for raw copy, PCM decode and
chunk reconstruction, plus the maximum `64x64` RGB frame. It does not systematically
exercise `required-1`, `required`, and `required+1` with unused-tail sentinels for every
write API. In particular, PCM encode lacks a short-output control, and successful calls
with oversized destinations are not used to prove that the unused tail remains unchanged.

Thus "capacity failure is explicit in sampled controls" is supportable after execution;
"all capacity boundaries are qualified" is not.

#### C01-09: `vision.overflow_dimensions` does not exercise arithmetic overflow

The huge dimensions in `vision.overflow_dimensions` are rejected by the `1..64` bounds
before `width*height*3` is evaluated. That is good defensive ordering and makes the
multiplication safe for admitted inputs, but the metric name is misleading if interpreted
as a checked-arithmetic overflow test. The evidence would be "huge dimensions are
rejected before multiplication," not "runtime multiplication overflow was detected."

#### C01-10: alias controls are not yet complete

The driver covers exact-source/destination alias for PCM decode and generic copy, and
codebook/output alias refusal for chunk reconstruction. It does not cover partial-overlap
slices, PCM encode alias, or all reconstruct overlap combinations.

By source inspection, staged PCM/generic copy and staged reconstruction appear intended
to preserve source-before-call semantics, while reconstruction explicitly rejects output
overlap with codebook storage. Partial-overlap behavior remains unexecuted evidence and
should not be generalized from exact-alias controls.

`r33_arrays_disjoint` also performs pairwise address comparison in O(a.len*b.len) time.
Its current reviewed callers are otherwise bounded, but the helper itself has no intrinsic
size bound; do not present it as a generally scalable alias primitive outside those
component envelopes.

#### C01-11: the log test proves ordering, not log integrity

`r33_commit_logged` verifies only the prior log record's stored version and prior `new
value` against current state. It does not validate the prior record's event ID, parent,
old value, earlier records, or an integrity digest. The driver's `trace.corrupt_last`
control mutates the checked version field, so it demonstrates one detected corruption
shape only.

Do not infer complete trace corruption detection, causal ancestry validation, rollback,
crash atomicity, or durable audit continuity from C01. The narrow claim "within one
process, after preflight, this function writes its current log record before updating the
state fields" matches the reviewed source.

### Candidate-specific falsification priorities before claiming a component pass

Without expanding C01 into full S0, the minimum high-value additions to its future
evaluation boundary are:

1. an independent expected-output contract so wrong metrics make the regression fail;
2. bounded exhaustive PCM signed-mapping comparison against the mathematical oracle,
   without printing 65,536 decoded rows;
3. same-version codebook-content mutation/reorder tests;
4. `required-1/exact/required+1` and untouched-tail checks for each write API;
5. partial-overlap alias tests and PCM encode alias behavior;
6. explicit empty-PCM policy;
7. corruption of unchecked log fields/earlier records to demonstrate exactly which
   integrity properties are and are not enforced.

None of these require claiming natural sensor bytes, persistence, or learner access.
They are the bounded component-level falsifiers appropriate to the stated C01 scope.

## Missing experiment that should gate sensory claims

The most important missing experiment is a fresh-process, byte-originated S0/S1 paired
counterexample test on one real declared encoding (audio is the cleanest first target):

1. start from literal PCM bytes and independent metadata;
2. ingest through the public native R33 byte API;
3. save and reload in a fresh process;
4. verify byte/metadata identity and signed decode;
5. compare two inputs differing only at an unsampled/sign-sensitive sample;
6. show the lossy derived route may collide but the diagnostic raw learner route remains
   distinguishable;
7. repeat at capacity boundary and with source-buffer mutation after admission.

Until that exists, an exact numerical-record implementation is useful architecture work
but not actual natural-audio S0/S1 evidence.

## What not to claim

Do not claim any of the following from B000 or from this review:

- that R33 now has qualified sensory ingress;
- that exact copying of `[]i32` or another numerical feature array proves raw byte ingress;
- that B000 executed a correction, training run, learner qualification, or promotion;
- that passing S0 would establish S2 usable perception, transfer, semantics, or general
  intelligence;
- that preserving bytes in storage proves those distinctions are available to the learner;
- that a same-process reconstruction with the same mutable codebook proves durable
  reversibility;
- that a lossy legacy helper proves the whole architecture is universally incapable of
  discrimination;
- that a certificate extends beyond the exact encoding, size/rate/dynamic-range,
  metadata, retention horizon, source/configuration, and resource envelope actually
  tested;
- that any R33 result establishes a full R27-to-R33 checkpoint migration unless that
  migration is separately executed and qualified.

## Files actually inspected

- `Research/R33_HANDOFF.md`
- `Research/R33_SENSOR_QUALIFICATION_PLAN.md`
- `Research/R33_B000_RUN_PRIMARY_V1/RESULT.json`
- `Research/R33_SUBSTRATE_AUDIT.md`
- `Research/R33_ARCHITECTURE_CONTRACT.md`
- `Research/tnn_r32_epistemic_chunking.zag` (legacy source around `trace_emit`,
  `core_relational_signature8`, `acoustic_window_distance`, `lru_evict_candidate`,
  `r31_segment`, and `r31_reconstruct`)
- `Research/R33_B000_SOURCE.zag` (copied helpers and evaluator-only B000 fixture driver)
- `Research/R33_B001_COMPONENTS.zag` (read-only component/API review; not compiled or run)
- `Research/R33_B001_C01_DRIVER.zag` (read-only driver/test-boundary review; not compiled
  or run)

The B001 corrective candidate is treated only as source-backed component design. It is
not treated here as executed evidence.
