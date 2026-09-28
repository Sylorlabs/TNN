# R33-B001-C02 — byte-originated record transport

Preregistered engineering diagnostic, not learner training or a sensory/authority
certificate. R27 remains canonical, development step60,423, zero restarts.
The protocol is immutable after registration; findings require a new version,
not editing a consumed checker. BUILD_01 and BUILD_02 failed; BUILD_03 compiled
the prior draft. BUILD_04 compiles the amended source used here. All are retained.

## Question and exact boundary

Can the new native encoded-file API preserve supported payload/metadata through
admission, an owned storage buffer, an owned retrieval copy, snapshot save, a
fresh-process reload and ordered continuation? This is a file transport component,
not a physical microphone/camera, integrated learner input, full S0/S1/S2 gate,
cryptographic provenance, crash durability or complete parent migration.

`R33_B001_C02_CONFIG.json` is the complete 48-process schedule. Thirty capture
cases cover signed PCM extrema, a one-bit audio twin, ordered RGB pixel twins,
maximum audio/RGB, empty PCM, malformed bytes/metadata, insufficient/zero/exact/
extra-tail capacity, and exact/forward/backward overlaps. Six fresh reloads include
the maximum audio payload. One normal continuation plus six temporal controls
cover tied timestamps, duplicate/gap ordinals, backwards time, clock mismatch and
timebase mismatch. Three snapshot overlaps and two corrupt snapshots complete
the schedule. No case is unobserved scientific validation: all are authored
engineering controls, including deliberate reuse of known defect shapes.

## Encoded layout and provenance

Raw magic is `TNNRAW01`; the 64-byte header has twelve unsigned little-endian
32-bit words in this order: encoding, channels, rate, width, height, items,
payload bytes, clock, ordinal, tick, timebase, source. Accepted values fit signed
nonnegative i32; next ordinal must not overflow. The two checksum words occupy
bytes56–63. Payload begins at64, is at most131072 bytes, and has no trailing bytes.

Encoding1 means interleaved signed PCM16LE, channels1–2, sample rate8000–192000,
width/height0, exact frame count and no padding. Channel order is the encoded
interleaved index, not inferred anatomical meaning. Empty PCM is permitted.
Encoding2 means packed row-major RGB8, channels3, width/height1–64, rate0,
exactly width×height×3 bytes, RGB order and no padding. These physical layouts
are generic machine conventions, not learned semantics or semantic boundaries.

The four-word order cursor is clock, next ordinal, last tick, timebase. The
fixture starts `[7,0,-1,1000000]`; ticks are nondecreasing, ordinal exact, and
clock/timebase fixed. Source11 is an authored producer identifier, not an
authenticated human identity or object/task class. The format has no rich
transform-lineage chain, duration or pending-action inventory. Source file hashes,
config identity and physical format interpretation are retained externally.

Snapshot magic is `TNNSNP01`; its 40-byte header stores the order cursor, exact
raw length, version1 and two checksum words, followed by the entire raw record.
Adler components detect the registered accidental corruptions only. They are
dependent components, not independent checks or signatures. External SHA256
binds artifacts but does not authenticate a trainer or make snapshots signed.

## Main-agent source review and independent-review disposition

The inherited independent sensory review requires byte-originated oracles and
fresh-process identity, and explicitly rejects calling array-copy tests S0.
This batch implements a narrow subset of that design. New review was dispatched
to Galileo, but the tool returned a terminal rate-limit error with no verdict.
The previous Sagan safety follow-up also has no verdict. Neither is counted as
approval. The three completed foundation reviews remain exactly as recorded.

Main-agent semantic review found metadata read-after-overlapping-copy in both
admission and restoration. Before registration, metadata is now staged before
copying, and stored cursor consistency is checked before snapshot/retrieval.
Six overlap cases were added; no prior executed source/result was rewritten.
Snapshot creation still uses exists-then-write, with no exclusive-open guarantee,
fsync or crash-atomic rename. It is permitted here only with isolated fresh
single-writer output directories, not concurrent/hostile writers or a live brain.
Caller-managed mutable native slices are not OS-protected immutable storage.
Retrieval uses a separate allocation in these tests, not an arbitrary-pointer
immutability certificate. A one-record store is not lifelong episodic memory.

Admission is solely an ordinary reviewed non-learning component test under the
already human-authorized R33 implementation work. It does not satisfy the
independent current-code review requirement for any scientific qualification or
learner authority expansion. No new scientific batch or milestone is unlocked.

## Oracle and falsification

The Python fixture/evaluator is external. Native Zag alone reads, validates,
copies, restores, snapshots and decodes. Python struct/zlib construct the original
encoded bytes and independently predict every metadata word, signed decoded
sample/pixel, cursor and snapshot byte. All metric/vector key inventories must
match exactly; exit0 alone is insufficient. Valid empty records emit no fabricated
decoded vector. Every unused destination byte must retain its sentinel. Mutating
a separately allocated retrieval copy or capture caller buffer must not change
the retained record. Deliberately overlapping inputs do not claim detachment.

Rejected initial records leave used0, cursor unchanged and every destination byte
unchanged. Rejected continuation leaves the previously restored raw record and
cursor exact; every retained byte is independently checked. Rejections produce
no new snapshot. A resealed snapshot with an inconsistent cursor must be rejected
even though its checksum matches. Input files must remain unchanged.

## Resources, authority and accounting

Pinned compiler: local official macOS ARM64 seed, explicit target, caches/daemon
disabled. Compile budget60s/CPU55s. Each native case: wall≤30s, CPU≤20s,
each output stream≤8MiB, measured peak RSS≤256MiB. Batch case budget180s;
individual deadline is reduced by remaining batch time. A failure stops the
batch, retains all partial output and consumes the attempt. Remaining cases
are not silently retried. The preflight allowed writes only within its fresh
directory and denied outside writes, network operations and forks. Native cases
receive only their own fresh directory write scope. Full filesystem read
isolation and hard RSS containment are not established. No M2 isolation claim.

Trainer-input ledger: the human authorized this research program; authored
literal fixtures are architecture-test assistance, not lessons or learner skill.
Hardcoding ledger: codec/layout, integrity arithmetic, file I/O, capacity/order
rules and test diagnostics only; no English/task answer/evaluator mode enters
a learner because no learner is instantiated. Changed-variable ledger: new
byte-record transport and ownership, compared with earlier carrier helpers;
not a matched cognitive performance comparison. Authority: no grants, no parent
load, no canonical mutation, no external actions except sandboxed test files.

## Required artifacts and next step

Registration freezes source/imports, build/binary, config, runner, tests,
preregistration, source review disposition, preflight, dependencies and actual
external test results. The sole `R33_B001_C02_RUN_PRIMARY_V1` retains reservation,
per-case admissions, inputs, binary, stdout/stderr, snapshots, result and manifest.
Registries, consumed-fixture history, journal/current state and handoff are updated
after execution. Reproduction means parsing retained logs/bytes, not a new run.

The next justified work is a separate durable fail-closed journal/recovery
component and real learner-accessible distinction/provenance tests, alongside
the full continuing-parent audit. B002/B003 remain gated. Never convert this
component result into a natural-perception, learning, consciousness or promotion
claim, nor mark the full R33 program complete.
