# R33-N03: incomplete-journal handle sentinel failure

The sole frozen BUILD02 primary returnedexit1 after36 of58 planned children.
All36 children were reaped:30 exited0, five reached deliberate crash boundaries
and exited73, and boundary11 exited1. The parent emitted397 CHECK rows and two
failures (unexpected child exit and missing child pass marker).

Boundary11 correctly rejected a root-only partial journal with error-8008 and
empty state/head/transaction buffers. Its only mismatching child assertion was
the closed lock field: observed-2, expected-1. Source inspection explains it:
nj_close normalizes the field only when its prior value is a nonnegative fd.
A missing writer.lock open returns-2, which is not an open descriptor, but that
error value was retained instead of the documented closed sentinel. This is not
evidence of a descriptor leak, accepted corrupted state or a learner failure.
The preregistered assertion is nevertheless failed, not revised after the run.

All25 base cases and boundaries1..10 matched, including five process-death
boundaries, exact partial-attempt bytes, original-tx retry, capacity checks,
sampled corruption and65536-byte same-process commit/recovery. Boundary12..32
and the final fresh-process maximum reload did not execute. Do not claim that
the58-case schedule or native journal qualification passed.

Read [raw output](R33_NATIVE_N03_RUN_PRIMARY_V1/supervisor.stdout),
[failing child](R33_NATIVE_N03_RUN_PRIMARY_V1/boundary11.stdout),
[full result](R33_NATIVE_N03_RUN_PRIMARY_V1/RESULT.json) and
[frozen protocol](R33_NATIVE_N03_PREREGISTRATION.md).
Host elapsed display was0.74s, maximum RSS6,422,528bytes. Per-child resource and
reap observations remain in the raw PROCESSV3 records; no survivor matched the
post-run scoped process check. RSS was measured, not contained.

All original code, oracles, frozen imports/compiler/build, outputs, journals and
preimages remain retained. The corrective implementation must use journalV2 and
a new N03A identity, explicitly disclosing the known engineering control reuse.
No consumed primary is silently rerun. The actual failure and skipped cases stay
visible in the registry and handoff.

No Python, scientific learner exposure/training, canonical mutation or authority
change occurred. R27 remains canonical60423/restarts0. N01B's narrow supervisor
qualification remains separate from this failed journal batch.
