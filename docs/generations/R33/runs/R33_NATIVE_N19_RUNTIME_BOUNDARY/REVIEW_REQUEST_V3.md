# Independent Review Request V3 — R33-N19 BUILD_08

Review BUILD_08 as a bounded native Zag runtime-boundary qualification packet.

Scope is explicitly limited to process-death recovery on the pinned macOS host. Do not infer power-loss durability, host-admin rollback protection, descendant process-group containment, learner behavior, scientific validity, or promotion readiness.

Review exact source/binary/compiler identities in `BUILD_08_RECORD.json` and executed evidence in `RUNTIME_QUAL_08_RESULT.json` plus the referenced stdout files. Confirm or reject:

1. host adapter/path custody tests have zero failures, including retained-root rename/replacement behavior and special-file/link refusal;
2. errno mapping distinguishes path, host-ABI, and ordinary I/O failures;
3. failed recovery is explicitly poisoned and never reported as fresh;
4. operational failures produce nonzero process status when failure is the requested behavior;
5. fresh child processes exercise five crash phases and separate recovery processes;
6. RLIMIT_FSIZE is actually enforced and observed file size stays at 32 bytes;
7. wait4 supplies CPU and peak-RSS observations and children are reaped;
8. real open/fsync/close fault fixtures classify as expected;
9. canonical R27, learner state, registry, historical BUILD_06/07 evidence, and scientific populations are untouched.

Return `PASS_WITH_NARROW_SCOPE` only if those claims are supported by executed evidence. Otherwise return `REQUEST_CHANGES` with exact blocking evidence.
