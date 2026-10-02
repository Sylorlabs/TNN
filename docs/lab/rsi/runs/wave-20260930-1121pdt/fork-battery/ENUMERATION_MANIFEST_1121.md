# ENUMERATION_MANIFEST (fork-battery run, 2026-09-30, wave-20260930-1121pdt)

Total: 87 named entries (1 LIVE, 86 fixture).

Run-start pin: 861f4a032d007e06475db8f7a50a7197c80f8f88 (local
tnn-native-lab tip at enumeration time; pinned-commit discipline: every
extraction is by pinned SHA, never by live ref, so mid-battery lane
commits are inert).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e
(unchanged; read-only git ls-remote this run: HEAD/main 27a4271f,
fs-gr1 23f6c0f9, r2-7 2d99d183, reorg/phase-0-1 991432226,
tnn-native-lab bedf8b4aa, wg-freeze f875b3417, pull/1 5802fec8,
pull/2 4b76bb59, pull/3 991432226. Zero new remote refs.)

Enumeration method: the prior wave's 84-entry table carried forward
verbatim, with these changes:
(a) local-tnn-native-lab now tested at the new run-start pin
861f4a032d007e06475db8f7a50a7197c80f8f88 (LIVE); its prior-wave pin
fdadcbe3c7b49887e795462a11664122349591c1 moves to the fixture set
under the new entry local-20260930-1121pdt-tip.
(b) midwave-20260930-0821pdt-97b28e6a6 at
97b28e6a6fffc2c8112c163dc4a3b145c3a7eb74 added: the inert mid-wave
commit noted in the 0821 manifest (CORE-FREEZE-RUN-COMPLETE), rotated
into the fixture set this wave as promised. Named explicitly to avoid
colliding with the 0821 LIVE pin rotation name.
(c) arch-wave-20260930-0821pdt at
bb9b56a34d2063d41118db1b2aa4a0366790f15d added: new archive branch
created this wave, tip SHA absent from the prior driver set.
(d) The other new archive branch (tnn-native-lab-wave-archive-wave-
20260930-0805pdt) resolves to fdadcbe3c, identical to the rotated
local-20260930-1121pdt-tip pin, so it is covered by pinned-SHA
extraction, not re-enumerated (standing precedent for same-SHA refs).
(e) The experimental branches (wave-20260927-0221pdt-exp1/exp2/sensory
at 1010a63c3/a2a36e657/c368b8e1f, wave-debate-session-1-backup at
3947dca1a) resolve to the same SHAs as the existing fixture entries,
so they remain covered by pinned-SHA extraction, not re-enumerated.

Live entries (1):
- local-tnn-native-lab (861f4a03, run-start tip)
Fixture entries (86): all prior-wave entries at their pins, every SHA
verified to resolve in this repo before the run, including the rotation
local-20260930-1121pdt-tip at fdadcbe3c.
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
pre-existing archive branches resolve to pins in the table, ZERO
movement. Two new archive branches: wave-20260930-0805pdt (covered by
existing pin, see (d)) and wave-20260930-0821pdt (new entry, see (c)).
The standing rule holds: archive branches are immutable; re-create,
never move. The four previously documented driver entries with no live
branch (arch-wave-20260929-1721pdt-tip2, arch-20260924-0821pdt,
arch-wave-20260927-0821pdt, arch-wave-20260929-1721pdt old pin) remain
unchanged in status.

46 commits landed on tnn-native-lab since the 0821 run-start pin
(fdadcbe3c..861f4a03), all after the pin; the battery tests only the
pinned commits, so lane progress is inert to this run.

Driver: batch_1121pdt.sh (87 run() lines), derived from batch_0821pdt.sh
by mechanical edit (wave name, scratch path ~/workspace/fb0930_1121pdt,
run-start pin, live/fixture rotation) plus the declared additions; the
84 carried run lines byte-identical except the rotation change.
run_one.sh sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument.
Harness: REBUILT this run from committed source
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag
(sha256 f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738)
with the pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
rebuilt binary sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
BYTE-IDENTICAL to the frozen instrument ~/workspace/fb1421/fork_battery.
Scratch: ~/workspace/fb0930_1121pdt/E/ (87 entry dirs). Zero Python in
battery construction and execution; pure shell, git, sha256sum, pinned
znc, pure-Zag harness.

CONSISTENCY GATE (pre-run gate): consistency checks ran BEFORE the
battery executed: A1 87==87, A2 87/87 resolve.
CONSISTENCY-GATE PRE-RUN: ALL PASS. The full gate (A1-A4) still blocks
the results commit.

No em-dashes in this documentation.
