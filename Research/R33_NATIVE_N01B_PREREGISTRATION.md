# R33-N01B: kernel-timer direct-child corrective regression

Identity r33-native-n01b-kernel-timer-v3. One primary, four native children,
79 native CHECK rows on the complete success path. Known N01A engineering
control shapes are intentionally reused after N01P diagnosis; this is neither
fresh scientific evidence nor a repeat of N01A or N01P. Neither consumed primary
is rerun. The no-repeat and experiment ledgers were checked before allocation.

## Exact source/configuration and changed variables

Use unchanged IO_V1 and PROCESS_V3 with a new BUILD02 source snapshot. V3 uses
Darwin kqueue/kevent with a relative one-shot EVFILT_TIMER, not the broken pinned
clock helper. The N01B oracle uses literal-valued expectations, not imported
numeric constants. BUILD02 adds a broad 80ms-to-5s observed duration bound for
the 100ms unguarded case. Compiler and flags remain pinned: macos-arm64,
--no-zagd --no-analyze --no-foreground-cache. Freeze complete imports, driver,
compiler identity, binary, protocol, review and compile logs before execution.

## Schedule and outcomes required

Native n01b supervise installs nio_guard(20), exclusively creates the run root,
and exercises local scalar width controls, repeated-root refusal, directory
and traversal refusal, labels57/58/64, and retained partial output admission.
Four child runs then must satisfy the actual native assertions:

1. Normal: exit0, no signal, timer registered/not fired, reaped, empty logs.
2. Deliberately unguarded busy loop: parent timer100ms, status-7608, SIGKILL9,
   timer fired, reaped, valid observed duration80,000..4,999,999us and RSS present.
3. Flood: 1024-byte hard file limit, status-7609, SIGXFSZ25, reaped,
   exact1024-byte stdout, empty stderr, no timer firing.
4. Missing executable: child exit127, status0, reaped, no signal, empty logs,
   registered timer not fired. Failed exec is an expected child outcome.

Success requires all79 CHECK rows matching, N01B_FAILURES,0,
N01B_NATIVE_PROCESS_V3_MATCHED_DESIGN,1 and native parent exit0. Capture actual
exit in the execution result; save its value in closeout rather than infer it
from a successful compiler command. Missing rows/markers are not a pass.

## Authority, write scope, trainer and hardcoding

No learner, accepted parent, lesson, scientific generator, new authority,
promotion or consciousness claim. Literal test values are authored engineering
oracles, not learned or innate domain answers. Whole declared fixture tree is
Research/R33_NATIVE_N01B_RUN_PRIMARY_V1, admitted by native mkdir. Reservation
and launch output live at specifically named sibling R33_NATIVE_N01B_RESERVATION.json,
R33_NATIVE_N01B_LAUNCH.stdout and R33_NATIVE_N01B_LAUNCH.host.stderr, then are
copied into the admitted root without replacing existing artifacts.
No Python or other implementation-language runtime may be used.

## Resources, review and claims

Parent wall/CPU20s, file1MiB, core0, fd64; children inherit CPU/file bounds and
lower file limits to65536 or1024. RSS is measured, not contained. The unguarded
busy loop has no child wall alarm; its inherited CPU ceiling is an emergency
fixture bound. Inspect actual survivors after abnormal supervision failure.

The [main review](R33_NATIVE_N01B_MAIN_REVIEW.md) documents the failed independent
review attempt, remaining liveness/containment limits and preceding BUILD01
overwrite deviation. It does not substitute for independent scientific approval.
A clean primary admits only the exercised direct-child component lane for
subsequent trusted engineering fixtures. N03/telemetry still require their own
source review, preregistration, execution and result evidence.

Retain result including negatives, source/build pins, exact logs, resource report,
manifest, consumed-fixture update, architecture diff (host adapter only), next
rationale and handoff/current-state reconciliation. R27 remains60423/restarts0.
