# R33-N08A: dyld bootstrap corrective kernel-worker qualification

New identity `r33-native-n08a-dyld-bootstrap-isolation-v2`; one sole primary,
five native children,15 expected worker checks. N08's primary and sources remain
immutable negative. This regression deliberately reuses its known five-case
protocol, source-level oracle, resources and synthetic fixture shapes; it is
not new scientific evidence. All new implementation and evaluation is Zag.

Parent protocol: Research/R33_NATIVE_N08_ISOLATION/PREREGISTRATION.md, read in
full and incorporated with only the changes below. New run and source paths
use N08A. Native result/parent terminal identify N08A; low-level N08_WORKER_*
markers intentionally remain unchanged as copied regression-oracle identifiers.

Evidence-grounded correction: the actual report
/Users/Shared/micah/Library/Logs/DiagnosticReports/worker-2026-09-05-201656.ips
identifies N08 worker PID45937 and an abort inside dyld ignition_halt/boot_boot/
CacheFinder before main. Report SHA256
d738f4a88f31abd7d9348ec9a050fa30db38b1962b40f62e194194c4a84065d7.
No worker test failure is inferred from that bootstrap abort.

Apple's installed dyld-support.sb explicitly supplies process-bootstrap rules:
read/test/map the listed OS/App cryptex paths and their ancestors, specific dyld
syscalls/fcntl operations, sandbox-check operation2, root-directory access and
open/openat/fstatat/dup calls needed by libignition. The complete file was
read, copied byte-exact to this new directory, and hashed at
06215a5d32689aefe395c29710e182eb54ba22162f50df8b4842290f8a19bf1c.
The new profile imports that exact local copy. It does not import the broader
system.sb/bsd.sb permissions and adds no user-data, network, fork or control
write authority. An initial cp -p reported a metadata chflags denial after the
bytes copied; the settled destination hash is exact. No OS file was modified.

Success/failure schedule is otherwise identical to N08: probe14 assertions,
forbidden /usr/bin/true execution1 assertion, denied worker launch,500ms spin
timeout and4096byte output ceiling; all five must be reaped and all parent
checks pass. EPERM/EACCES, immutable64-byte control preimage, absent inherited
descriptors, exact captures and terminal markers remain mandatory. Any new
failure stops this sole primary and requires another separate identity.

Main-author engineering review only. This is a prospective correction, not
proof of the actual cause or successful confinement. No independent security
certification, real human grant, full runtime, scientific data, learner, accepted
R27 use, training or promotion. Persist all source/config/review/reservation,
build pins, native results/captures/resources/preimages, analysis, hashes,
registries, journal and handoff before continuing the protected-anchor work.
