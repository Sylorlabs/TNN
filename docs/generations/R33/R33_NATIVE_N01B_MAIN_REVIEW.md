# N01B bounded engineering review and review-attempt disposition

Main-agent review, 2026-09-05. This is not an independent reviewer approval.
The pending independent N01B reviewer and parent-blob auditor both returned a
terminal infrastructure error: missing cwd in trusted execution context. Neither
produced the assigned review file. No failed review is counted as successful.
The completed earlier N01 review and N01A/N01P negatives remain applicable
criticism, not final-source certification.

Reviewed PROCESS_V3 identity
04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89,
IO_V1 b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e,
and the literal-oracle driver d186fa8b235fe15449c113d88686483eb7bd84066d606ef72fb41e6be7b325c9
before the narrowly described BUILD02 amendment. Read the complete supplied
V3 source and actual current driver, design and installed Darwin event ABI.
The source freeze binds the final amended driver separately.

## Strongest criticism and dispositions

An outer alarm alone cannot guarantee a child is reaped if its parent dies.
V3 instead registers the kernel one-shot timer before fork, polls wait4 for
early exit, and kills/reaps the direct child on timer delivery or supervision
error. The fixture child deliberately lacks a wall alarm. Its inherited CPU
ceiling and busy-loop shape are a final safety bound, not evidence that V3 works.
If the primary does not report all four reaped children, treat it as failure and
inspect the actual child processes; never silently call it qualified.

No descendant/process-group, hostile-code, same-user protection, hard RSS or
arbitrary kernel-hang liveness claim is admitted. The final reap is blocking.
The tested scope is reviewed direct-child engineering fixtures only. Live
learner execution and protected authority remain prohibited.

N01P falsified casts as a remedy for imported constants. Current driver expected
values are independent numeric literals; V3's operational constants are local
to its own source, and no numeric constants from V3 cross into the driver.
The driver calls exported functions/structs, which remain subject to the native
execution checks. No compiler was changed or substituted.

The original duration check admitted zero elapsed time. BUILD02 now requires
an observed 80,000 <= wall_us < 5,000,000 for the 100ms unguarded case. This rejects
an immediate/units-error outcome but does not make gettimeofday monotonic, certify
precision, or prove absence of clock adjustment. Enforcement still uses kqueue.

Output ceiling is RLIMIT_FSIZE for every regular file written by the child,
not an output-only quota. Future journal tests must allow record header overhead.
Regular-file checks themselves allocate after output creation; only the main
preflight buffers are allocated before artifacts. Partial artifacts are preserved.
Closed descriptors/checked terminal result do not imply exhaustive fd-leak or
allocation-failure qualification.

## Missing falsifiers and what not to claim

No fault injection exercises kqueue creation/registration/wait failure, allocation
failure, parent death, descendant creation, same-user adversarial changes, real
symlink attacks or EINTR storms. Those remain unqualified. Expected normal exit,
timer kill/reap, output-limit termination and exec127 must all actually occur.
An assertion count, compile success or favorable review cannot replace them.

## Build-provenance deviation

The preceding worker reused unexecuted BUILD01 while changing the oracle. Earlier
context recorded binary 92adbec799a9642b2ce13d4e6f1fa662229c8b6fe3fdee96ac5f84cc121cac6f;
the current BUILD01 is 41cb3b4b34b5d659731d0d4b961f6149c0563fbd187fd0282b32d6658cfb0f21.
Do not claim the older binary is retained or that BUILD01 was immutable. No N01B
primary had been registered/executed. Current BUILD01 source/import/design bytes
were copied beside the current binary before any new edit; new compilation uses
BUILD02. This deviation remains documented rather than rewritten as compliance.

## Admission recommendation

Proceed only with a separately preregistered, bounded non-learning engineering
primary, with the independent-review gap explicit as in prior component work.
This does not discharge any independent scientific, sensory, migration, safety
authority, promotion or full-program gate. Preserve negative outcomes unchanged.
