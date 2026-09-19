# Native Zag journal candidate

This is a new native replacement for C03's historical external Python collector.
It has not executed merely because this source exists. It uses the frozen N02A
corrected SHA256 implementation; V1 failed integrity code is not imported.

The root encodes an exact initial byte snapshot and bounded storage policy.
Each committed record carries sequence, transaction identity, expected parent,
mutation kind, previous-record digest, before/after state digests, exact next
state bytes and its own digest. Recovery verifies all links and byte identities
before returning any operational handle. The root must equal an independently
supplied, frozen initial record; reading a changed disk root is not permission.

Native operator code exclusively creates the journal directory and root/lock
files. An advisory writer lock serializes admitted operations. Each commit
reserves a new attempt file, retains it through partial/failing writes, fsyncs
the complete record, publishes with no-replace hardlink, fsyncs the directory,
then changes live state. Successful duplicate transaction/content returns an
idempotent status; conflicting reuse, stale parent and exhausted capacity fail.
Rollback is a new kind2 snapshot record, never deletion of prior history.

Bounds: state1..65,536 bytes,32 published records,64 reserved attempts, maximum
record65,696 bytes. Named reserved slots are scanned for gaps/out-of-envelope
records; arbitrary unrelated filenames are outside this trusted fixed-driver
API and do not establish hostile-directory quota isolation. Attempts count
persistent reservations, NOT CPU or all rejected invocations. Actual process
resources and rejected calls must additionally appear in supervisor artifacts.

After any partial/published I/O failure the live handle is unusable until closed
and recovered; a failed durability acknowledgement cannot silently return an
old live state as authoritative. Unpublished attempts remain for inspection.
Process-death controls will test five boundaries plus an injected partial-write
failure. This does not simulate host power loss, disk-controller corruption or
an adversarial process with same-user write access. The hash chain is not a
signature, grant or trusted timestamp. No learner can call this privileged
operator API directly in a qualified system; that boundary is not yet proven.

State payloads are opaque bytes. Component tests do not prove they contain a
complete TNN brain, optimizer, RNG, raw-memory policy or pending-action inventory.
Canonical R27 is not loaded, changed or migrated by this work. Generic fixture
initialization is not a newborn learner, and fixture-assigned numbers are not
learning. Current safety/authority/S0/S1/telemetry/dominance gates stay open.
