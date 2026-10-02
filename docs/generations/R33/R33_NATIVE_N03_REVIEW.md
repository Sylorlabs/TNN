# R33-N03 independent native journal review

Review date: 2026-09-05 (America/Los_Angeles).

Scope: bounded read-only semantic/API review of the native opaque-snapshot journal and
its 25-case N03 engineering schedule. No Python was executed or edited. No native case,
fixture, generator, learner, training, registry, journal source, driver source, SHA
source, IO source, process source, accepted parent, or scientific evidence was mutated
or executed by this review.

This review is bound to the source identities observed at review close:

- `Research/R33_NATIVE_JOURNAL_V1.zag` — SHA-256
  `b02f3a92a5a8ad0f104e9940b0e50d6bdcf343f2f4b628738a09f914ba881e38`
- `Research/R33_NATIVE_N03_DRIVER.zag` — SHA-256
  `9c69341a27127b115db8b05a90c10ce420ed8d1999abbf37799f88abb63b9c24`
- `Research/R33_NATIVE_JOURNAL_DESIGN_V1.md` — SHA-256
  `90ceca7ee4f634c49877bfa07a944d2c0aa9ed3b5328c6673ccff89ff746c01e`
- corrected `Research/R33_NATIVE_SHA256_V2.zag` — SHA-256
  `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- frozen `Research/R33_NATIVE_IO_V1.zag` — SHA-256
  `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e`
- current `Research/R33_NATIVE_PROCESS_V2.zag` — SHA-256
  `1006fe5dad48c3399d159ab4920d3a02ca12ed0d62470e363a3ab52f78705e56`

The previously reported N02A SHA KAT result is dependency context, not evidence rerun by
this reviewer. The preserved failed SHA V1 is not treated as successful.

## Verdict

**SOURCE DESIGN IS PROMISING BUT THE CURRENT 25-CASE N03 SCHEDULE IS NOT SUFFICIENT FOR
THE FULL DESIGN CLAIM.** The publish ordering and normal recovery chain are coherent by
inspection, but there are two concrete source/test defects and several important
unfalsified boundaries. A future successful N03 run can support a narrow process-crash
opaque-snapshot journal claim only after the findings below are dispositioned or
explicitly excluded.

## Strongest criticism

The advertised journal payload envelope and the actual N03 child resource envelope are
inconsistent.

The journal accepts state lengths through 65,536 bytes (`nj_root_record`, line 42) and
documents a maximum transaction record of 65,696 bytes. But every N03 child sets
`RLIMIT_FSIZE=65,536` (`R33_NATIVE_N03_DRIVER.zag`, lines 30-34), and the current
PROCESS_V2 child also installs its output/file-size limit before `execve`. At maximum
state size:

- `root.bin` is `64 + 65,536 = 65,600` bytes;
- an event/attempt record is `160 + 65,536 = 65,696` bytes.

Both exceed the child's 65,536-byte hard file-size limit. The practical event payload
ceiling under this exact N03 harness is at most 65,376 bytes before header overhead, not
the 65,536 bytes claimed by the generic source contract.

The current driver uses only 16-byte fixture state, so none of its 25 scenarios can
discover this mismatch. Do not claim the 65,536-byte state envelope was qualified by N03
unless the process/file-size envelope is made compatible and boundary-tested.

## Concrete defects

### N03-R1 — recovery ignores failure of the root-head SHA computation

`nj_recover` allocates `j.head`, copies the initial state, then calls
`ns_sha256(expected,j.head)` without checking its return value (journal line 110).

If SHA allocation or another SHA call precondition fails at this point, an empty journal
can continue to `j.status=0` with an invalid/zero head because there is no event record to
force a later mismatch. That produces an operational handle after an integrity primitive
failed. This violates the design statement that recovery verifies integrity before
returning an operational handle.

Required semantic rule: any root-head hash failure must make recovery fail explicitly and
expose no operational state.

### N03-R2 — the injected partial-write control does not prove a partial write occurred

For crash modes 2 and 6, `nj_commit` calls `nio_write_all` on half the record and then
`nio_sync`, but ignores **both** return values (journal lines 184-186). Crash mode 2 exits
73 regardless; mode 6 poisons the handle and returns `-8008` regardless.

Recovery counts an attempt as long as it is a regular file with length between zero and
the maximum record size (lines 139-146). Therefore the existing `write-failure` scenario
can pass even if the intended half-record write wrote zero bytes or its fsync failed.

The current test establishes "an attempt reservation existed and the live handle was
poisoned," not "a partial record was durably written and then safely ignored by
recovery." A valid partial-write falsifier must independently check the retained attempt
length/prefix (and the intended sync result where observable) before claiming that
boundary was exercised.

### N03-R3 — duplicate-transaction I/O failures are misclassified as transaction conflict

When a transaction ID already exists, `nj_commit` reopens the corresponding event and
defaults `code=-8007` (lines 159-166). Any open/read failure in that path returns `-8007`
instead of an I/O/integrity error such as `-8008`/`-8001`.

Under the trusted, unchanged-directory model this may not occur normally, but it is an
API classification defect: "conflicting transaction" is not equivalent to "could not
read the prior transaction needed to determine idempotency." Do not claim fail-cause
attribution is complete.

### N03-R4 — `kind=2` is a trusted label, not an enforced rollback target

The basic scenario appends the original fixture bytes with `kind=2` and calls this
`rollback_append`. The journal validates only that kind is 1 or 2; it does not require a
kind-2 payload to equal any historical state, name the historical sequence being
restored, prove authorization, or enforce rollback policy.

Thus the defensible statement is "the fixture appended a new kind-2 snapshot whose bytes
equaled the initial fixture while retaining prior history." It is not evidence for a
general rollback mechanism or rollback authority.

### N03-R5 — alias semantics are not fully specified or falsified

The current `caller_detached` check is useful: it mutates the ordinary `next` buffer after
commit and confirms journal state is detached. But `nj_commit` accepts any `next` slice
whose length matches state and does not reject overlap with `j.state`, `j.head`, or
`j.transactions`.

This matters because the journal fields are directly accessible. If a state length is 32
and `next` aliases `j.head`, the commit's final head update mutates the caller's input
slice after publication. With a 128-byte state, aliasing `j.transactions` can likewise
change the supplied slice when the transaction table is updated. The persisted record is
staged first, so this is not presently an identified record-corruption bug, but input
immutability/idempotent-retry semantics become surprising.

Additionally, generic `nj_copy` is a forward copy and is not memmove-safe for arbitrary
partially overlapping source/target slices. Current internal uses reviewed here are
disjoint/staged, but the helper itself must not be advertised as overlap-safe.

The API should either reject internal-buffer aliasing explicitly or publish and test its
allowed alias semantics.

### N03-R6 — failed-attempt provenance is reservation-level, not content-integrity level

Recovery counts `attempt-N.bin` files by contiguous presence, regular-file type and size
only. It does not hash or parse unpublished attempts, bind them to transaction IDs, or
prove which attempt produced a published event. Published event records themselves are
hash-validated; failed/unpublished attempts are not.

This is consistent with treating attempts as retained reservations, but it means N03
must not claim cryptographic/content integrity or full provenance for failed attempts.
The event-to-attempt relation also depends on filesystem hardlink identity rather than an
explicit attempt ID stored in the transaction record.

## Commit/recovery observations that are sound by source inspection

- Initialization constructs the root record before the first filesystem effect; directory
  creation is exclusive and partial initialization is preserved rather than reused.
- Recovery requires `root.bin` to byte-match an independently reconstructed root from the
  caller-supplied initial bytes before exposing state.
- A writer advisory lock is acquired before root/event recovery and held in the returned
  live handle.
- Event recovery checks contiguous event names, record sequence, transaction ID domain,
  fixed state length, parent sequence, kind, prior-head digest, before-state digest,
  after-state digest and record digest before advancing state.
- Transaction IDs are checked for duplication across the recovered published sequence.
- New commits enforce `parent == current sequence` and refuse published/attempt capacity
  before reserving another attempt.
- The normal commit order is: create attempt -> persist reservation directory entry ->
  write/fsync complete attempt -> no-replace hardlink publication -> directory fsync ->
  live-state/head/transaction-table update.
- After checked I/O failures past reservation, the live handle is poisoned until recovery.
- A successful duplicate published transaction with matching parent/kind/payload returns
  idempotent status without creating another attempt.

These are code/design findings, not executed N03 evidence.

## Adequacy of the 25-child schedule

The count is internally consistent: basic + reload (2), five crash phases each followed
by recovery and verify (15), partial-write + reload (2), two capacity cases (2), and four
corruption cases (4), totaling 25.

It is a reasonable first engineering schedule for **process-death publication ordering**
at small state size. It is not an exhaustive journal qualification.

The five process-death boundaries are useful and correctly distinguish the intended
process-crash visibility semantics:

- phases 1-3: attempt exists but no published event -> recover old state;
- phases 4-5: hardlink event exists -> recover committed state;
- verification retains the failed attempt and confirms a resumed/duplicate operation.

This remains process-death testing only. In particular, phase 4 (link before directory
fsync) cannot establish power-loss durability; after ordinary process death the link is
still visible in the live filesystem cache.

The four corruption cases cover an unresealed payload edit plus resealed changes to the
prior-head digest, before-state digest, and sequence. They do not establish resistance to
a same-user actor who recomputes the unkeyed hash chain, which the design correctly
excludes.

## Missing falsifiers before broader journal claims

1. **State-size envelope:** initial/next lengths 0, 1, exact effective maximum, declared
   65,536 maximum, and 65,537 refusal. Resolve the RLIMIT_FSIZE/header mismatch first.
2. **Root integrity:** wrong independently supplied initial bytes, truncated root,
   extended root, changed root metadata/envelope, and root hash-integrity failure.
3. **Partial-write reality:** verify the injected attempt is exactly the intended prefix
   length and bytes; do not infer this from `-8008` alone.
4. **Same-transaction retry before publication:** after crash phases 1, 2 and 3, retry the
   original transaction ID/payload and prove one published event plus retained prior
   attempt(s), with stable later idempotency.
5. **Gap detection:** event-1 missing with event-2 present; attempt-1 missing with
   attempt-2 present; confirm failure exposes no state.
6. **Out-of-envelope slots:** explicit event-33 and attempt-65 presence on recovery, not
   only commit-time refusal/no-attempt-65 checks.
7. **Transaction integrity:** two otherwise valid/resealed event records reusing a
   transaction ID; transaction ID zero/negative-encoded/high-bit malformed values.
8. **Record shape:** truncated and extended event records, wrong magic, wrong payload
   length, invalid kind, nonzero reserved field, stale parent, and after-state hash edit.
9. **Alias boundaries:** `next` equal to state/head/transaction storage where lengths
   permit, plus an explicit contract for partial-overlap helper behavior.
10. **Allocation/error injection:** especially root-head SHA failure during recovery and
    allocation/name failure after a durable attempt exists but before publication.
11. **Existing/partial journal root:** second `nj_init` refusal and recovery behavior from
    a directory containing only `writer.lock`, only `root.bin`, or other documented
    partial initialization states.
12. **Failed-attempt provenance:** if stronger audit claims are desired, prove retained
    attempt content/integrity and event-to-attempt binding; otherwise keep the claim at
    reservation counting only.

Not all of these must fit the first N03 batch. They are the boundaries that must remain
explicitly unqualified if omitted.

## Provenance and claim boundary

The record format provides **structural journal lineage**: root identity from externally
supplied initial bytes, sequence, transaction ID, parent sequence, mutation kind,
previous-record digest, before/after state digests and record digest.

It does **not** itself record or authenticate operator identity, human grant, compiler or
source identity, wall-clock timestamp, branch identity, semantic reason, sensor source,
learner decision provenance, or attempt ID. Those may be supplied by later trusted
telemetry/supervision artifacts, but they are not properties of this journal record.

The root oracle is also external: if a caller supplies different initial bytes together
with a correspondingly different journal tree, the journal has no signature/root of
trust that decides which one is authorized. That is correct for the stated trusted
operator component scope and must remain explicit.

## Forbidden claims

Even if all 25 scheduled children later execute exactly as expected, do not claim that
N03 establishes:

- power-loss, storage-controller, APFS crash-consistency, or hardware durability;
- a signed, authenticated, tamper-resistant or same-user-adversarial audit log;
- full integrity/provenance of unpublished failed attempts;
- a general rollback engine, rollback authorization, or verified historical rollback
  target semantics;
- the documented 65,536-byte state capacity unless the N03 file-size envelope mismatch
  is corrected and boundary-tested;
- arbitrary alias/overlap safety;
- exhaustive allocation-failure or partial-write handling from the present schedule;
- full causal provenance, trusted timestamps, grants, or authority;
- a complete brain/checkpoint containing optimizer, RNG, memory policy, pending actions,
  raw sensory records, telemetry, or all continuing-parent state;
- R27 migration, parent mutation, newborn initialization, learning, training, learner
  competence, sensory S0/S1/S2, scientific qualification, promotion, milestone/grant
  change, dominance, or R33 completion;
- that corrected SHA-256 is a signature or authorization mechanism;
- that the preserved failed SHA V1 or any failed historical review became successful.

## Precise defensible claim after a future clean N03 run

Subject to disposition of N03-R1/R2 and the capacity-envelope mismatch, a clean primary
can support only a statement of this form:

> Under the exact pinned native Zag/macOS component configuration and small opaque fixture
> states exercised by N03, the trusted-operator journal observed the specified exclusive
> initialization, advisory single-writer recovery, append-only attempt reservation,
> no-replace hardlink publication, process-crash recovery boundaries, sequence/parent and
> published-transaction checks, exact published-state recovery, sampled idempotency,
> sampled capacity refusal and sampled corruption rejection. The result is an engineering
> component regression, not a power-loss durability, signed-authority, full-brain,
> sensory, learning or scientific qualification.

No N03 native case was executed to reach this review verdict.
