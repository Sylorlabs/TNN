# R33-B001-C03 retained result — historical mixed-language component

Status: **21/21 engineering groups matched; not a native-only supervisor.**
The sole primary run completed at 2026-09-05T19:58:12.434411Z. Its frozen
[machine result](R33_B001_C03_RUN_PRIMARY_V1/RESULT.json) and
[manifest](R33_B001_C03_RUN_PRIMARY_V1/MANIFEST.json) remain unchanged.

There were 80 native Zag replay executions and 173 subprocesses in total.
The latter include the Python persistence/recovery supervisor. Five writers
deliberately exited73; thirteen expected rejections exited4. Total subprocess
CPU was3.941901s, batch wall5.033220209s, peak subprocess RSS25,100,288 bytes,
and combined stdout39,971 bytes.124 external authoring checks had passed before
admission; they are not new native tests and were not rerun for this report.

The groups exercised native scalar transition replay, trace capacity, duplicate
and conflicting transactions, stale proposals, five writer-death boundaries,
injected write failure, corruption, missing/truncated/inconsistent records,
changed root, committed symlink, second writer refusal and staging quotas.
Scalar restoration appended history rather than rewinding it. This does not
establish rollback of a real learner's parameters, optimizer, memory or RNG.

Read-only reconciliation checked762 regular-file hashes plus the separately
recorded symlink target:763 manifest entries, not763 regular-file digests.
Result SHA256: `6d3cf8b78bd45cc3784cbff312a415ffa8b07f79d916029e9bbcf0778e5e3822`.
Manifest SHA256: `b288f96e30361842d445e9627605855c901e40cbf318e3dbf5799aeb04101eab`.

## Current disposition

The user's subsequent native-Zag-only correction excludes this Python
supervisor from the forward runtime, supervision and evaluation path. Preserve
the historical source, all results, failures and consumed identity. Do not
rewrite or rerun C03 to relabel it native-only. Its replacement needs new Zag
source, preregistration and exact evidence identities; inherited controls are
engineering regressions, not fresh scientific evidence.

No physical-power-loss, hostile same-user isolation, signed checkpoint,
authenticated human grant, full sensory qualification, integrated training
telemetry, full-parent migration, learning, consciousness or promotion follows
from C03. R27 stays canonical at60423, zero newborn restarts.
