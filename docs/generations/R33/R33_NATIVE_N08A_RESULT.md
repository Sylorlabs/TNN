# R33-N08A — bootstrap repaired; socket-denial check failed

Sole primary exited1 after its first child, reaped with exit1/signal0. Unlike
N08, the worker entered main and executed14 assertions:13 matched, one did not.
Protected read/write/chmod/rename/unlink, symlink-target read, unlisted creation,
supervisor signal0, fork and inherited-descriptor checks matched. Exact allowed
input checks matched. The socket syscall did not satisfy the required EPERM/
EACCES predicate. Its raw return was not logged, so no specific raw return or
actual successful network connection is inferred. No connection was attempted.

This batch is FAILED, not full isolation qualification. The native parent credits
zero checks from wholly passing worker modes, reports five failures including
the incomplete five-child schedule, and executed25 parent checks including save
and close. Four later modes remain unexecuted. Protected64-byte fixture stayed
exact. Old N08/N08A expectations and sources remain frozen; a new correction is
required. No old primary is rerun and the failure is not silently waived.

Evidence: [native result](R33_NATIVE_N08A_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[worker checks](R33_NATIVE_N08A_RUN_PRIMARY_V1/worker-probe.stdout),
[supervisor](R33_NATIVE_N08A_LAUNCH.stdout). Worker-log SHA256
e598d1f812a68e447f9d34460eecc474a4af710cfbc44ae1ba4edf0853eb31cc;
supervisor SHA256f9f051a7d23e042eee7a6959dd45455a9477f46a47478c71636db839000e6055.
ChildCPU16,027us/wall222,132us/peakRSS1,425,408bytes; host0.45s/maxRSS1,622,016.

The reviewed installed Apple profiles distinguish network operations and syscall
filtering. N08B will additionally deny socket/socketpair/socket_delegate syscall
entry with an explicit errno, preserving the same required failure predicate
and adding raw return telemetry. This is a prospective enforcement change,
not proof of its effectiveness. All fixtures remain disposable and non-learning.
Nineteen consumed diagnostic batches, zero training/new grants/canonical mutation.
