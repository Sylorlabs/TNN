# R33-N05A — durable native telemetry, prospective engineering protocol

Identity: `r33-native-n05a-durable-telemetry-v1`. One primary, forty
prospectively specified direct-child invocations. No learner, training, world
generator, scientific partition, canonical mutation, or authority grant.

The preceding N05 design/stub and D01 design/reservation are retained unchanged.
Neither is registered as an executed experiment. This implementation has a new
identity and does not appropriate either incomplete freeze as source evidence.
N01A/B/P, N02/A, N03/A, N04 and B000/C01/C02/C03 remain consumed history.

## Hypothesis and changed-variable ledger

A versioned, bounded, native append/publication layer can preserve N04 V2 event
semantics and caller-recorded causal bytes across fresh-process reconstruction,
detect the registered corruptions, and expose every abandoned reservation
without acknowledging an unpublished event or inventing missing evidence.

Allowed changes: durable record encoding, integrity and identity checks,
exclusive reservation, publication/acknowledgment, bounded recovery, and native
engineering fixtures. The exact N04 telemetry V2 accumulator, IO V1, SHA256 V2
and PROCESS V3 imports are unchanged and pinned with the new build. Familiar
crash shapes from N03A are deliberately reused as component integration
regressions, not fresh scientific populations or repeated old primaries.

Forbidden: changes to learner state, teachers, sensory transformations,
optimization, representations, historical protocols/oracles, grants, or canonical
status. Fixture IDs, six causal-role labels, byte patterns, capacity, and
expected metrics belong to the engineering evaluator, not a learner.

## Encoding and commit contract

Root: 128 bytes, magic/version, capacity (1..16), five positive telemetry
identities, fixed 88-word metric ABI and 1152-byte event ABI, reserved zeros,
SHA256. A caller-supplied root configuration must match exactly at recovery.

Each immutable event: version, length, ordinal, persistent attempt number,
event ID, parent ordinal, predecessor SHA256, whole-record SHA256, reserved
zeros, signed little-endian 88-word N04 event, and six 112-byte causal slots.
Slots are, in order: evidence, memory, hypothesis, decision, consequence, update.
Each holds an explicit missing marker or 1..64 exact caller-supplied bytes with
their digest; inactive tails and reserved bytes must be zero. These are recorded
engineering payloads, not generated explanations or proof of causal truth.
Missing slots remain missing after replay; no default narrative fills them.
Payloads over 64 bytes require a future encoding, never truncation.

The store is a trusted single-writer engineering directory. Reserve an exclusive
`attempt-N.bin` and sync its directory before writing. Sync complete record bytes,
publish by an exclusive hard link `event-N.bin`, sync the directory, then update
the live accumulator and acknowledge. Existing records are never overwritten by
the production API. Rejected requests before reservation consume no attempt.
Post-reservation failures poison the handle until close/recovery. A failure after
publication is explicitly indeterminate, not reported as a successful rollback.

Recovery checks contiguous bounded event and attempt names, record integrity,
root identity, unique event IDs, parents, canonical causal slots, N04 semantics,
and byte equality of every published event with its retained attempt. It rebuilds
the accumulator from records, not a stored metric summary. Unpublished attempts
remain on disk and are reported separately as complete or incomplete. No
unpublished event enters the accumulator. Invalid committed history exposes no
usable state. The API refuses event 17 and attempt 33 before allocation.

This is process-death/fsync engineering, not a hardware power-cut guarantee,
authenticated human identity, hostile same-user containment, arbitrary directory
enumeration, full learner state persistence, or a complete causal learner schema.
The reserved namespace is event 1..17 and attempt 1..33; arbitrary foreign files
and out-of-namespace malicious filenames are outside this certificate.

## Prospective primary schedule and literal controls

1. Invalid mode: exit 2, no output.
2. Normal writer and fresh replay: twelve authored metric events; all 168 metric
   words and every causal byte equal the writer artifacts. Independently assert
   events 12, exposures 2, unique 1, replay 1, request 1, refusal 1, retrieval 1,
   accepted update 1, rejected update 1, ever-lost 1, final lost 0, rescue 1.
   Understanding/teacher competence/transfer/calibration remain unmeasured.
3. API refusal/alias/identity/causal-input checks preserve complete prior state,
   inputs, attempt count and head. A second writer cannot acquire the lock.
4. Sixteen-event capacity writer and fresh replay; event 17 is refused.
5. Thirty-two failed partial reservations and fresh replay; all remain visible,
   zero committed records, attempt 33 refused.
6. Five writer deaths at reservation, half-write, full-file sync, publication,
   and directory-sync boundaries, each followed by a fresh replay. Deaths exit
   73. Expected committed count is 0 for boundaries 1..3, 1 for 4..5; attempt
   count 1 throughout; incomplete count 1 for 1..2 and 0 otherwise.
7. Real parent SIGKILL after a half-write marker, followed by fresh recovery.
   Expected supervisor timeout -7608, signal 9, reaped; incomplete count 1.
8. Injected pre-publication sync-failure seam and fresh recovery: no commit,
   one complete unpublished attempt, live state unchanged, explicit error.
9. Injected post-publication sync-failure seam and fresh recovery: indeterminate
   acknowledgment error, live state unchanged, published record recovered once.
10. Eight separately constructed corruption directories, each with setup and a
    fresh rejection process: checksum (-8103), incomplete committed record
    (-8101), duplicate event ID (-8104), stale parent (-8104), root metadata
    (-8101), reordered ordinal (-8104), invalid causal slot (-8102), unsupported
    event version (-8101). Preserve exact preimages before diagnostic mutations;
    metadata/semantic mutations are resealed where specified to distinguish
    semantic validation from checksum-only rejection.

Forty child invocations total. Any unexpected assertion, signal, exit, output
truncation, missing terminal marker, resource overrun, or unreaped child fails
the primary and stops subsequent cases. Source/oracles freeze before exposure.
Observed assertion count is reported from native counters, not estimated.
No retry or post-hoc expectation changes under this identity.

## Resources, review, artifacts, and exit boundaries

Native parent uses frozen PROCESS V3 with 60-second guard, 1 MiB per-file ceiling,
core dumps off, 64 descriptors. Ordinary child deadline 15 seconds; the explicit
kill case 1 second. Positive observed per-child RSS must be <=256 MiB; RSS is not
hard containment. Native supervisor records CPU, nonmonotonic wall observation,
RSS, output lengths, exit/signal, and reaping. Actual totals are not fixture
resource fields. No network, Python, shell evaluator, legacy loads, or learner
execution. Compiler invocation, artifact copying and host hashes are operational.

Review is main-agent bounded engineering/source review. Current tool discovery
exposes no spawn-agent function; no independent verdict or scientific/authority
review gate is claimed. All source/config/import/compiler/build/review identities
must be captured in FREEZE.json and checked before primary admission. Build-only
failures remain preserved. The run directory is exclusively
`Research/R33_NATIVE_N05A_RUN_PRIMARY_V1`; only new N05A source/build/launch and
closeout artifacts plus the shared current-state/registries/handoff/journal are
authorized writes. Prior drafts, imports, evidence and parent archives are not.

Preserve preregistration, reservation, frozen sources/configuration, compile logs,
binary identities, raw native assertions, process resources, damaged bytes and
preimages, result/analysis, architecture diff, consumed evidence, manifest,
next-step rationale, journal and handoff. Completion qualifies only the stated
engineering envelope. Continue sensor and parent/authority dependencies before
any training, without a newborn reset. R27 stays step 60423/restarts 0.
