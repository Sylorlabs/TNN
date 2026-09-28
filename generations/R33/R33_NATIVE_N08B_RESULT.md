# R33-N08B — bounded kernel-worker isolation passed

Sole primary exited0; all five children reaped, all15 worker assertions and67
parent checks matched. Native JSON records65 parent checks before successful
result-save/root-close. Both predecessors remain frozen negative.

The worker read its exact32-byte allowed input. Protected canary read/write-open/
chmod/rename/unlink, symlink-target read and unlisted-file creation were refused.
All64 canary bytes stayed unchanged after every child. Deliberately inherited
non-CLOEXEC descriptor40 and every other nonstdio descriptor were absent in the
worker. Supervisor signal0 and fork were denied. Raw socket creation returned-1
under the explicit denied-syscall policy. Unlisted /usr/bin/true execution was
denied. Removing permission for the worker's own executable prevented entry,
with no unrestricted fallback. These are actual kernel-boundary observations,
not mere checks against caller-supplied permission flags.

The spin child was killed by the parent timer at observed508,623us, signal9,
native status-7608. Flood produced exactly4096 captured bytes then signal25,
status-7609. All corresponding status, capture and resource assertions matched.

Evidence: [native result](R33_NATIVE_N08B_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[supervisor](R33_NATIVE_N08B_LAUNCH.stdout),
[worker checks](R33_NATIVE_N08B_RUN_PRIMARY_V1/worker-probe.stdout),
[profile](R33_NATIVE_N08B_RUN_PRIMARY_V1/probe-profile.sb).
Native result SHA25627e787adcc7ec4ff649a24b62864bf7e85ec95397bd33194628b8de87acfa1ec;
supervisor SHA256dd25472d47dc5b96e0e5d2d87981a59630570173a93037862405e6fc4fb29c11.
ChildCPU537,125us, summed observed wall725,983us, peakRSS4,374,528bytes; host0.99s,
peakRSS4,374,528bytes. No worker/controller survivor matched the scoped check.

Scope is this pinned macOS26.6.2/build25G83 loader/profile and native worker,
including blocked fork in this lane. It is not arbitrary kernel-exploit defense,
host-administrator protection, hard RSS enforcement, real human authentication,
full authority/causal integration, parent migration or R33 completion. Loader
and policy syntax remain deprecated/private platform dependencies. Main review
is not independent security certification. No control-root high-water binding
is claimed yet; integrate it before rejecting stale learner checkpoints.

Twenty consumed diagnostic batches, zero training, actual human grants, newborn
restarts or canonical mutation. R27 remains step60423. Continue protected-state
anchoring and genuine continuing-parent/learner integration.
