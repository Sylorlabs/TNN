# R33-N01A: failed native supervisor correction

The sole BUILD02 primary failed: 66 native CHECK rows, 21 reported failures,
four children started, all four immediately killed/reaped after status -7510
(NRV2_CLOCK). Normal exit, an actual parent deadline, the output-flood limit and
exec127 therefore remain unqualified. The original execution reported exit1;
the retained failure marker and source failure return agree. There was no separate
launch exit-status file, and this closeout does not invent one.

Read the complete [raw output](R33_NATIVE_N01A_RUN_PRIMARY_V1/supervisor.stdout),
[machine result](R33_NATIVE_N01A_RUN_PRIMARY_V1/RESULT.json),
[resource log](R33_NATIVE_N01A_RUN_PRIMARY_V1/supervisor.host.stderr), and
[frozen protocol](R33_NATIVE_N01A_PREREGISTRATION.md).

Two problems must remain distinct. The monotonic-clock call failed in the pinned
native binary; newer compiler source is not proof of that binary's support.
Separately, several named constants in expected-i64 assertion positions printed
pointer-like values instead of the authored integers. Constant lowering/widening
is a hypothesis, not a root cause established by this run. Correcting the oracle
afterward cannot turn N01A into a pass. The 45 other rows do not qualify V2.

The frozen source, imports, compiler, build, preregistration, reservation and raw
outputs are unchanged. Four reaped children demonstrate cleanup in this observed
clock-failure path only, not descendant containment or general supervisor safety.
The whole run tree, including empty child logs and the empty fs directory, is
retained. Host time displayed 0.27 seconds; parent maximum RSS was 1,310,720 bytes.
Rounded CPU displays are not exact zero measurements.

This is consumed, author-visible engineering evidence. No scientific population,
learner training, parent-state load, canonical mutation or authority unlock took
place. R27 remains canonical at step60,423 with zero newborn restarts.

The distinct proposed N01B/V3 correction is under review. Native kernel-timer
supervision and explicit-width assertions must be independently exercised under a
new preregistration before N03 journal testing. Historical N01/N01A failures and
scope deviations remain permanent evidence, not fixtures to silently replay.
