# ENUMERATION_MANIFEST (fork-battery run, 2026-09-30, wave-20260930-0805pdt)

Total: 83 named entries (1 LIVE, 82 fixture).

Run-start pin: 593cc5906b9c5b2dca6a80a74140f1c2833883c1 (local
tnn-native-lab tip at enumeration time; pinned-commit discipline: every
extraction is by pinned SHA, never by live ref, so mid-battery lane
commits are inert).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e
(unchanged; read-only git ls-remote this run: HEAD/main 27a4271f,
fs-gr1 23f6c0f9, r2-7 2d99d183, reorg/phase-0-1 991432226,
tnn-native-lab bedf8b4aa, wg-freeze f875b3417, pull/1 5802fec8,
pull/2 4b76bb59, pull/3 991432226. Zero new remote refs.)

Enumeration method: the prior wave's 82-entry table carried forward
verbatim, with these changes:
(a) local-tnn-native-lab now tested at the new run-start pin
593cc5906b9c5b2dca6a80a74140f1c2833883c1 (LIVE); its prior-wave pin
3847065e2298a619096210db2d78d48f176d86c2 moves to the fixture set
under the renamed entry local-20260930-0805pdt-tip.
(b) Zero new local branches since the prior wave; zero new archive
branches; the experimental branches (wave-20260927-0221pdt-exp1/exp2/
sensory at 1010a63c3/a2a36e657/c368b8e1f, wave-debate-session-1-backup at
3947dca1a) resolve to the same SHAs as the existing fixture entries, so
they are covered by pinned-SHA extraction, not re-enumerated.

Live entries (1):
- local-tnn-native-lab (593cc5906, run-start tip)
Fixture entries (82): all prior-wave entries at their pins, every SHA
verified to resolve in this repo before the run, including the renamed
local-20260930-0805pdt-tip at 3847065e2 and the prior rotation
local-20260930-0750pdt-tip at 14a92a69d.
Duplicate SHA groups carried unchanged from the prior wave:
{rh-pull-3-head, rh-reorg-phase-0-1, wt-forktest-reorg} at 991432226;
{wave-debate-session-1-backup, wt-forktest-debate-backup} at 3947dca1a;
exp/wt-exp pairs at 1010a63c3, a2a36e657, c368b8e1f;
{wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses,
wt-wave3-trades} at bd3097874.
Known forktest commits 293602fb1, a0e7f8ba2, 991432226, bd3097874,
f875b3417, cea8db22f all resolve and are present in the table.
Stale refs/remotes/rh-* (remote "rh" no longer configured) carried as
fixtures at their pins; rh-pull-1-head (5802fec8) and rh-pull-2-head
(4b76bb59) are non-TNN trees with the pinned toolchain path absent
(expected UNTESTABLE).

ARCHIVE-BRANCH IMMUTABILITY CHECK (automated in the enumeration step):
every tnn-native-lab-wave-archive-* branch tip was checked against the
set of SHAs pinned in the prior wave's driver table. Result: all 41
existing archive branches resolve to pins in the table, ZERO movement.
No new archive branches. The four previously documented driver entries
with no live branch (arch-wave-20260929-1721pdt-tip2, arch-20260924-0821pdt,
arch-20260927-0821pdt, arch-wave-20260929-1721pdt old pin) remain unchanged
in status. The standing rule holds: archive branches are immutable;
re-create, never move.

Driver: batch_0805pdt.sh (83 run() lines), derived from batch_0750pdt.sh
by mechanical edit (wave name, scratch path ~/workspace/fb0930_0805pdt,
run-start pin, live/fixture rotation) plus the declared carry-forward;
the 81 unchanged run lines byte-identical except the rotation insert.
run_one.sh sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument.
Harness: REBUILT this run from committed source
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag
(sha256 f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738)
with the pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
rebuilt binary sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
BYTE-IDENTICAL to the frozen instrument ~/workspace/fb1421/fork_battery.
Scratch: ~/workspace/fb0930_0805pdt/E/ (83 entry dirs). Zero Python in
battery construction and execution; pure shell, git, sha256sum, pinned
znc, pure-Zag harness.

CONSISTENCY GATE (promoted this wave to a PRE-RUN gate):
consistency_gate.sh now accepts --pre-run, asserting (A1) driver run()
count equals the manifest's declared total and (A2) every run() SHA
resolves, BEFORE the battery executes. The full gate (A1-A4) still
blocks the results commit. Pre-run gate result this wave:
CONSISTENCY-GATE PRE-RUN: ALL PASS (A1: 83==83, A2: 83/83 resolve).

No em-dashes in this documentation.
