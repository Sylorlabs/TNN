# R33-N08 — failed before worker entry; isolation unqualified

Sole frozen primary exited1. Only the first of five planned children started;
it was reaped with signal6 (SIGABRT), exit sentinel-1, empty stdout/stderr and no
worker-entry marker. No worker assertion ran. Seven parent assertions failed
including the incomplete schedule;25 total parent checks include result save and
root close. Later four modes were not launched. Do not rerun this identity.

The parent verified all64 protected fixture bytes unchanged after the child.
No isolation behavior, network/fork denial, descriptor closure, timeout or flood
qualification follows from an abort before worker entry. Launcher/profile/host
compatibility remains under diagnosis; the evidence does not yet identify a
specific sandbox rule as the cause. No expected code or frozen source is changed.

Evidence: [native result](R33_NATIVE_N08_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[launch output](R33_NATIVE_N08_LAUNCH.stdout),
[retained profile](R33_NATIVE_N08_RUN_PRIMARY_V1/probe-profile.sb),
[worker capture](R33_NATIVE_N08_RUN_PRIMARY_V1/worker-probe.stdout).
Result SHA25607176c762d219cb91cec61a5f3493545bf1bc0d4c50696517b0da36a6aab5722;
launch SHA256213ab42be884835e4fa073ee65492d2b7887494f7e2371d79924c5b1881998c1.

Observed childCPU7,008us/wall191,065us/peakRSS770,048bytes; host elapsed0.39s,
peakRSS1,622,016bytes. Scoped process observation found no n08/worker survivor.
A first diagnostic-report glob expanded to no matches; this is not proof no
crash report exists in another location. OS diagnostic investigation follows.

Both compiled pairs and the admitted35 pins remain retained. Main engineering
review does not turn this failed primary into a qualified protection boundary.
Eighteen diagnostic batches consumed, zero R33 training, no real human grant,
newborn restart, canonical mutation or promotion. R27 remains60423/restarts0.
Continue a separately identified source-grounded correction and preserve N08.
