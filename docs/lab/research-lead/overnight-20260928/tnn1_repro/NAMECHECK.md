# TNN-1 Independent Reproduction Worker: NAMECHECK

## Step 0: Toolchain Guard

Date: 2026-09-30
Task: Independently reproduce the TNN-1 build from committed source (commit 0323b97d5).

Guard check: `which python3 python` returned `/usr/bin/python3`.
This is a system binary that cannot be removed from PATH. It will not be invoked
at any point during this wave. All build and test work uses only the pinned
`znc` compiler, executed binaries, git, and shell file operations.

Zero invocations of any forbidden executable (python3, python, node, ruby, etc.)
will occur during this wave. Any accidental invocation would render this wave
PROCESS-FAIL per the Worker Toolchain Guard.

## Step 1: Identity
TNN-1 Independent Reproduction Worker, spawned by the research coordinator.

## Step 2: Owned Path
`docs/lab/research-lead/overnight-20260928/tnn1_repro/` only.
The TNN-1 source at `tnn1_build/tnn1.zag` is read-only for this worker.
