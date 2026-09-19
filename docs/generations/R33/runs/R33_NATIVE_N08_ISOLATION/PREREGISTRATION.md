# R33-N08: kernel-confined native worker engineering

Identity `r33-native-n08-kernel-worker-isolation-v1`. One prospective primary,
five scheduled direct children, stop at the first unexpected result. All test,
supervision and worker code is native Zag. Apple's installed sandbox-exec is
an OS policy-loader dependency, not an evaluator, shell script or substitute
cognition implementation. No Python or other authored execution language.

Changed variable: introduce a deny-default kernel sandbox around a separate
native worker instead of an unrestricted same-user process. Frozen IO_V1,
SHA256_V2 and PROCESS_V3 remain unchanged. N07 is not reexecuted. Known hostile
control shapes are disclosed engineering reuse, not fresh scientific evidence.

Native launcher redirects stdin to /dev/null, closes descriptors3..63, supplies
an empty environment and execs Apple's loader with an exact inline profile.
There is no unsandboxed fallback. The kernel policy allows public system loader
reads, exact worker binary execution/read, one32-byte input and own stdout/stderr
data writes. It does not authorize arbitrary writable scratch space, control
files, network, other programs, child creation or signals to the supervisor.
A deliberately inherited non-CLOEXEC protected fixture at fd40 tests descriptor
closure. The worker executable contains no trainer/controller keys or control
file contents. No accepted R27 bytes or real credentials enter these tests.

Sole order: (1) probe; (2) forbidden executable; (3) profile without executable
permission; (4) bounded infinite worker killed by parent deadline; (5) output
flood killed/limited by kernel file ceiling. The first probe has14 exact checks:
allowed input open/length/bytes; protected read/write-open/chmod/rename/unlink;
symlink-target read; unlisted file creation; network socket; signal0 against
supervisor; fork; all nonstdio descriptors closed. EPERM or EACCES is required
for denied syscall returns. Any unexpected child fork exits immediately and is
reaped by its worker; it still fails the probe. The executable probe attempts
only /usr/bin/true, requiring refusal and a worker terminal marker. Its one
check plus14 probe checks total15. No potentially harmful real-world target.

Only disposable files under R33_NATIVE_N08_RUN_PRIMARY_V1 can be damaged by these
adverse probes. Exact protected preimage is retained before exposure and all64
original bytes are compared after each child. The denied-launch case must exit
nonzero below120, signal0 and no worker-entry marker, with no fallback. Ordinary
children require exit0, stderr empty,15 exact successful worker assertions total,
entry/pass markers and complete captures. Spin requires native supervisor status
-7608, timed_out1, signal9 and entry marker; flood requires-7609, output-limit1,
entry marker and <=4096bytes. Every child must be reaped. Any unexpected behavior
fails this sole primary; corrections get new identities, never altered oracles.

Parent60seconds; normal child15seconds; spin500milliseconds; flood4096bytes;
other captures262144bytes; observed childRSS<=256MiB; inherited core0/fd64.
Native parent records actual counters/resource observations and terminal result.
No hard RSS guarantee or arbitrary kernel-exploit resistance is inferred.

Trainer input: no human grant. Synthetic allowed bytes and protected canary are
driver-only engineering oracles; worker receives no protected contents. Values,
paths, ABI numbers, quotas and policy literals are hardcoded test/protocol data,
not cognition. No learning, scientific worlds, canonical mutation or promotion.

Review: implementing main-agent engineering review, not an independent security
certification or scientific grant. Installed Apple manual calls sandbox-exec
deprecated; installed bsd.sb calls policy syntax private/changeable. Qualifying
this exact macOS/build/loader/profile does not promise forward compatibility or
complete system-call coverage. Denying fork may close this lane's descendant
escape, but does not establish full runtime authority, real human identity,
antirollback durability, total resource accounting or parent migration.

Freeze exact new sources/imports/compiler/configuration, both builds, installed
loader/OS identity and normative local documentation before exposure. Preserve
all outcomes/preimages, raw captures, native results, hashes, registry/consumed
history, resource report, analysis, architecture delta, journal and handoff.
Next: integrate a separately retained authority high-water record with this
worker boundary, then complete learner-state/causal and parent continuity gates.
