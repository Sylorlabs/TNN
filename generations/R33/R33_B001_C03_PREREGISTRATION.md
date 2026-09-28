# R33-B001-C03 — external durable collector and native replay

New bounded engineering component, not a scientific learning batch. The causal
question extends B000's silent trace saturation and C01's in-memory log-before-
mutation tests to real persisted generic transitions and fresh native replay.
B000/C01/C02 are consumed; they will only be verified from retained artifacts.
No historical learner, data generator or checkpoint is executed.

## Architecture and ownership

Native Zag applies and checks generic transition records through the frozen
`r33_commit_logged` helper. A new replay driver consumes `TNNTXN01` plus an initial
value, bounded event count and five-word events. It prints actual state and log
words. An external Python laboratory supervisor persists these native-checked
transition records using a single-writer lock, exclusive staged file creation,
file fsync, atomic no-replacement hardlink publication and directory fsync.
Staging paths remain retained, including partial interrupted writes.

Python is the external persistence/verification/test supervisor, not TNN learning,
reasoning or action selection. Scalar values41/52/63/75 are generic test fixtures;
assigning them is not described as learning. Isolated fixture initialization is
not a newborn TNN restart. No continuing brain is loaded or modified.

Records bind sequence, previous digest, transaction ID, native transition and
committed-unit count. Recovery refuses missing, corrupt, reordered, noncanonical
or inconsistent committed records and returns unpublished staging identities
without treating them as commits. A complete published event is authoritative
even when its writer died before acknowledgment. Same-ID/same-content retry is
idempotent; conflicting reuse fails. Scalar restoration appends a new transition
and does not rewind journal history or committed-unit count. Actual CPU/output/
RSS of rejected or interrupted attempts is separately retained by the external
batch supervisor; committed units are not falsely labeled total spent compute.

## Exact diagnostic schedule

`R33_B001_C03_CONFIG.json` names21 groups. Each group has a separately initialized
bounded fixture, with deliberately repeated control transitions. These are
author-visible engineering regressions, not independent worlds or fresh learning
examples. The frozen runner specifies every subprocess and oracle before launch.

The groups cover normal fresh replay, scalar restoration, trace-capacity+1,
idempotent retry, conflicting retry, stale version, five real writer-process
terminations, injected ENOSPC, hash corruption, sequence gap, truncated committed
record, resealed inconsistent state, altered root, committed symlink, concurrent
writer refusal, pending-stage quota and native malformed-parent rejection.

Crash hooks call `os._exit(73)` before write, during a partial write, after file
fsync, after atomic publication, or after directory fsync. Expected recovery is
the before-state for the first three and committed after-state for the latter
two. Each successful crash recovery then continues with a new transaction and
replays in another native process. Injected ENOSPC is an explicit simulated
write failure, not exhaustion of the user's disk. Published corruption is
fail-closed, never silently repaired. Original fixture bytes are retained before
intentional corruption. Symlinks are confined to the new test fixture tree.

## Oracle, admission and resource contract

Every native result is checked against exact independently specified state/log
values, not process exit alone. Every externally recovered event is exported
unchanged to native replay. The journal's Python arithmetic validates serialization
and causal consistency; it does not provide learned decisions. External authoring
unit tests are separately identified and never count as native execution.

One primary batch only. Freeze config, native source/imports, compiler/build,
supervisor, runner, tests, protocol and test-result identities before admission.
Each process has wall≤10s, CPU≤5s, each output≤64KiB, measured RSS≤256MiB;
batch wall≤180s. Native subprocesses use the previously tested deny-write/network/
fork sandbox profile. Trusted external writer/readback processes operate only
on the explicitly bound new C03 run tree. They are not arbitrary learner code.
Each journal is limited to3 committed events,4096 conservatively counted pathname
bytes and32 entries, including retained staging. Any first mismatch stops the
batch; preserve failure, consumed attempt, original source and checker.

## Review, hardcoding and exclusions

Inherited independent architecture/safety/sensory reviews motivate durable audit,
before-or-after recovery, no history rewind and native-state evidence. Main-agent
review covers only this bounded engineering component. The recent independent
sensory follow-up failed rate limiting and the safety follow-up returned no
verdict; neither is an approval of C03. Current independent adversarial review
remains required before scientific or live-runtime qualification.

The root contract is pinned test data, not a cryptographically protected human
policy. SHA256 provides artifact integrity, not authenticated authorization.
Native proposal verification and external commit are not a qualified hostile-
coordinator transaction. Advisory locks and no-follow/exclusive file operations
do not establish isolation from a malicious same-user process. Process death
on a running host is not a power-cut/storage-controller test. No F_FULLFSYNC,
signature, protected signing key, live learner, optimizer/RNG/recurrent-state
rollback, exact-once external action or whole-brain migration is claimed.

Hardcoded machinery: file protocol, bounded counters, hash checks, order rules,
safe generic transition primitive and diagnostic values. No domain knowledge,
English vocabulary, task labels or hidden evaluator state is learner input.
The human authorized research implementation; automated fixtures are test
assistance, not teacher competence credited to TNN. Authority grants remain0.

## Records and next dependency

The primary run retains admissions, all native/writer/recovery stdout/stderr,
original and intentionally corrupted fixtures, staged/committed records, resource
reports, result and manifest. Registries, exposure history, current state, journal
and handoff are updated. Read-only verification reparses retained evidence; it
does not execute the native cases again. R27 stays canonical at60423/restarts0.
Full parent continuity, S1/transform lineage, integrated telemetry, protected
authority and scientific freshness still gate B002 and later B003.
