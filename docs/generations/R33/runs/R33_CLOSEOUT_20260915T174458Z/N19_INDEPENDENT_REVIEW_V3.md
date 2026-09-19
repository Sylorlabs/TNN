# Independent Review V3 — Lane C, 2026-09-15

Disposition: **PASS_WITH_NARROW_SCOPE for the additive repaired candidate only**.
Unmodified BUILD_08 disposition: **REQUEST_CHANGES** (ordinary root fsync/close errors incorrectly become HOST_ABI in `n19_host_probe`). This review does not silently approve, repin, or rewrite BUILD_08. STATUS.json remains the original packet status; no admission or active-candidate switch is performed.

## Identity and evidence custody

Read STATUS.json, REVIEW_REQUEST_V3.md, BUILD_08_RECORD.json, RUNTIME_QUAL_08_RESULT.json, all five referenced stdout files, HOST_ABI_CONTRACT_V1.md, REFUSAL_MATRIX.json, and the runtime/host/tests/supervisor/native-I/O sources. Historical stdout and receipts are witnesses only. The refusal matrix and ABI contract contain prospective/stale status descriptions; they are not fresh execution evidence.

The compiler used was exactly /Users/Shared/micah/Documents/zag/znc, SHA256 3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956. Host: macOS 26.6.2, build 25G83, native macos-arm64 target. The four BUILD_08 source hashes match. BUILD_08's recorded runtime hash resolves to BUILD_08/n19_v3b, and its qualification hash resolves to BUILD_08/n19_qual_v1, NOT the similarly named n19/n19_qual. Host-test hash matches BUILD_08/n19_host_tests. This exact-name distinction matters. Fresh historical-binary reruns below use the hash-matching n19_v3b.

Fresh evidence is INDEPENDENT_V3_FRESH/final.stdout and supplement.stdout. The preliminary execution.stdout is not the final repaired-binary qualification. Exact commands and per-process exit statuses are printed in the logs; run.sh and supplement.sh retain the shell orchestration. Builds/commands/identities are also in INDEPENDENT_V3_FRESH/RECORD.json and evidence.sha256.

## Defect and additive safe repair

Original n19_host_probe returned -1999 for ANY fsync or close failure. Adapter-owned unsupported open flags properly map to HOST_ABI, but an ordinary durability/close I/O failure must be -1905. n19_runtime_boundary_v4_review.zag changes this classification through a shared n19_host_probe_fd helper and adds a closed-root descriptor fixture exercising that actual helper. The final fixture reports -1905 and exits 0 because the expected refusal is asserted. It does not claim EBADF is a disk failure or a power-loss event.

n19_qual_driver_v2_review.zag adds a second nonblocking wait4 for each observed child; Darwin -10 (ECHILD) is required and printed. Source and BUILD_08 remain immutable. No compiler modification occurred.

## Direct fresh findings

| Required row | Direct evidence / boundary |
|---|---|
| Root/path custody | Host failures 0. Root retained over live→moved rename and live replacement; held and moved roots read exact before/after bytes while replacement refuses both. Empty/dot/parent/absolute/traversal/embedded-NUL/length-bound leaf checks pass. Real root-symlink opening and lookup refuse PATH, exit 1 in supplement.stdout. |
| Links/special files | Real symlink, hardlink on both original and alias, directory and FIFO all refuse -1904. Candidate operational probes independently return exit 1 for each. FIFO is opened nonblocking before regular-file checking. Stat logic requires current UID, regular type and nlink=1; newly created files require 0600. These are exercised fixture types, not an exhaustive device/socket/race qualification. |
| Errno classes | Executed mapping assertions separate ENOENT/EBADF/EACCES/EEXIST/ELOOP→PATH, adapter-owned EINVAL/ENOTSUP/ENOSYS→HOST_ABI, and EIO/EMFILE/ENOSPC→IO. These mapping tests are explicitly synthetic inputs, not OS fault observations. Real missing open emits raw -2/PATH; real closed-descriptor fsync and close emit raw -9/IO. Repaired host-probe helper also refuses IO. |
| Failed recovery poisoning | Atomicity case asserts prior counters 7/3/96/7 survive, poisoned=1, recovered=0. The append source gate refuses poisoned state; a subsequent append on that same state was not separately executed. Fresh empty/torn crash journals emit poisoned and exit 1. Missing leaf and missing-root recovery emit poisoned/PATH and exit 1. Source sets flags through n19_recovery_refuse, rather than merely printing a label. |
| Operational exits | Missing recovery/probe/append/root, duplicate exclusive write and unsafe-type probes all exit 1. Valid host/io/write/append/recovery/probe/retained sequence exit 0. Expected-refusal assertion fixtures intentionally exit 0; they are not successful operational requests. |
| Five crash phases | Ten distinct fork+exec children per matrix: phase exits 80/81/82/83/84; files 0/16/32/32/32. Separate recovery exits 1/1/0/0/0 with poisoned/poisoned/recovered/recovered/recovered states. Final repaired matrix and fresh pinned BUILD_08 runtime matrix each failures 0, supervisor exit 0. These are abrupt process exits, not power-loss simulation. |
| RLIMIT_FSIZE | Child applies hard+soft limit 32 and attempts 64 bytes. Final repaired child signal 25, file 32, CPU 843 us, RSS 1507328 bytes; pinned historical runtime child signal 25, file 32, CPU 924 us, RSS 1490944 bytes. Parent independently measures file size; shell stat confirms 32. Both supervisors exit 0. |
| Accounting/reaping | wait4 syscall 7 populates user+system CPU and ru_maxrss before the second wait. All 22 final supervised children print second_wait=-10; observed CPU and RSS are positive. No configured limit is substituted for a measurement. Ordinary successful-path direct-child reaping is evidenced; interrupted/error fallback exhaustion and descendant groups are not qualified. |
| Protected state | Pre-run hashes of current-state and both experiment/consumed registries verify unchanged. Pre-run manifest for all existing BUILD_0*/RUNTIME_QUAL_0* files verifies unchanged, including BUILD_06/07/08/09. Canonical parent raw-byte hash remains 31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a and policy hash remains 983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8; no deserialization executed. Source call graph contains no learner/registry/state reader, and all writable arguments resolve to additive lane fixtures. Current-state fields remain canonical R27, step 60423, newborn restarts 0. |

## Claim boundaries and exclusions

PASS is limited to the pinned repaired binaries, owner-created local fixtures, exercised refusal types and successful direct-child process-death paths. It establishes no scientific exposure, learner authority, training, behavioral equivalence, successor promotion or production qualification. No learn opened. No Python, PyTorch, NumPy, pickle execution, historical verifier, or foreign ML runtime was used. Shell hashing of canonical serialized bytes is not loading that serialization.

Explicit exclusions: **power-loss durability; host-admin rollback protection; descendant process-group containment**. Concurrent hostile same-user replacement/hardlink races, exhaustive socket/device failures, CPU-ceiling enforcement and interrupted wait fallback are not evidenced by these checks. Root identity across a fresh reopening is not authenticated; retained-descriptor custody is what passed.

No remaining blocker for this narrow repaired disposition. BUILD_08 itself remains REQUEST_CHANGES unless replaced by an explicitly pinned repaired candidate through a separately authorized integration step. Historical receipt validity and historical mutation before this lane cannot be established by a lane-start hash; only preservation during this lane is claimed.
