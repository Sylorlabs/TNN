# R33-N01 — native Zag macOS substrate qualification

New non-learning engineering identity `r33-native-n01-darwin-io-v1`. Not a repeat
of C03: new native descriptor, I/O and limit adapter; no Python execution.
Expected outputs are design, not results. Freeze this protocol, sources, binary,
compiler and build identities before the sole primary execution.

The27 `CHECK` assertions in the frozen driver test directory creation, root open,
exclusive no-follow child creation, regular-file type, duplicate create refusal,
parent traversal refusal, exact six-byte write/read with signed-byte extremes,
file and directory fsync, full-size/capacity refusal, untouched tail, hardlink
publication without replacement, advisory lock/second-writer refusal, fresh file
descriptor read and missing-file status. Success requires all assertions match,
`FAILURES,0`, exit0 and empty stderr. Two separate negative processes require
native one-second wall deadline termination by SIGALRM and one-second CPU limit
termination by the host's CPU-limit signal (SIGXCPU or SIGKILL), not normal exit.

The only write target is the new `Research/R33_NATIVE_N01_RUN_PRIMARY_V1/fs`
directory. Refuse an existing primary directory at admission. No accepted parent,
historical generator, learning, real sensor, milestone or grant is involved.
The process installs native CPU10s, wall10s, file-size1MiB, zero-core and64-fd
limits; the negative cases lower their respective limit to1s. A native Zag parent
uses fork/execve/wait4, an empty child environment and exclusive child stdout/
stderr files, checks exit/signal outcomes and measured RSS<=256MiB, and prints
`N01_NATIVE_SUPERVISION_PASS,3` only after all three processes match. Its own
CPU/wall deadline is30s. Peak RSS remains measured, not hard-contained. Parent
shell only invokes that binary and preserves its stdout/stderr/host metadata;
all supervision, case operations, assertions and deadline enforcement are Zag.
No replacement scientific evaluator in another language is introduced.

The local Zag Linux/ext4 store was inspected but not imported: its required
filesystem and syscall layout differ from this macOS/arm64 environment. This is
a new explicit Darwin adapter, not silent requalification of that existing code.
Compiler source/installed SDK are inspection references; only the actual pinned
compiler build/run establishes supported native behavior. Preserve compile or
runtime failures with exact identities and never rerun the primary invisibly.

These controls do not establish power-loss durability, cryptographic integrity,
malicious-process isolation, full native journal recovery, learner rollback,
sensory S0/S1/S2, telemetry, whole-parent migration or R33 completion. Native
journal/telemetry work follows verified primitive behavior. Independent review
capacity failures remain visible; main-agent engineering review is not an
independent scientific approval. R27 remains canonical60423/restarts0.
