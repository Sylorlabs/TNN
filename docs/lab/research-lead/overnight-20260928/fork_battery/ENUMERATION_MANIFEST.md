# ENUMERATION_MANIFEST (fork-battery run, 2026-09-30, wave-20260930-0732pdt)

Run-start pin: 14a92a69da61cb83eaab3cbfec5a356eb552466c (local
tnn-native-lab tip at enumeration time; pinned-commit discipline: every
extraction is by pinned SHA, never by live ref, so mid-battery lane
commits are inert).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e
(unchanged; read-only git ls-remote this run: HEAD/main 27a4271f,
fs-gr1 23f6c0f9, r2-7 2d99d183, reorg/phase-0-1 991432226,
tnn-native-lab bedf8b4aa, wg-freeze f875b3417, pull/1 5802fec8,
pull/2 4b76bb59, pull/3 991432226. Zero new remote refs.)

Enumeration method: the prior wave's 80-entry table carried forward
verbatim, with these changes:
(a) local-tnn-native-lab now tested at the new run-start pin
14a92a69da61cb83eaab3cbfec5a356eb552466c (LIVE); its prior-wave pin
955106ae5 moves to the fixture set under the renamed entry
local-20260930-0732pdt-tip.
(b) The prior wave's LIVE archive entries rotate to fixture:
arch-wave-20260930-0221pdt at 697d4f308 and
arch-wave-20260929-1721pdt-tip2 at dff8c2005.
(c) Zero new local branches since the prior wave; zero new archive
branches; the experimental branches (wave-20260927-0221pdt-exp1/exp2/
sensory at 1010a63c3/a2a36e657/c368b8e1f, wave-debate-session-1-backup at
3947dca1a) resolve to the same SHAs as the existing fixture entries, so
they are covered by pinned-SHA extraction, not re-enumerated.
Total: 81 named entries (1 LIVE, 80 fixture).

Live entries (1):
- local-tnn-native-lab (14a92a69d, run-start tip)
Fixture entries (80): all prior-wave entries at their pins, every SHA
verified to resolve in this repo before the run (git cat-file -t loop,
80/80 commit, zero misses), including the renamed
local-20260930-0732pdt-tip at 955106ae5, arch-wave-20260930-0221pdt at
697d4f308, arch-wave-20260929-1721pdt-tip2 at dff8c2005, and
arch-wave-20260929-1721pdt at 7c11ac5af (old pin of the moved branch).
Duplicate SHA groups carried: {rh-pull-3-head, rh-reorg-phase-0-1,
wt-forktest-reorg} at 991432226; {wave-debate-session-1-backup,
wt-forktest-debate-backup} at 3947dca1a; exp/wt-exp pairs at 1010a63c3,
a2a36e657, c368b8e1f; {wt-forktest-tnn-native-lab, wt-wave3-probe,
wt-wave3-senses, wt-wave3-trades} at bd3097874.
Known forktest commits 293602fb1, a0e7f8ba2, 991432226, bd3097874,
f875b3417, cea8db22f all resolve and are present in the table.
Stale refs/remotes/rh-* (remote "rh" no longer configured) carried as
fixtures at their pins; rh-pull-1-head (5802fec8) and rh-pull-2-head
(4b76bb59) are non-TNN trees with the pinned toolchain path absent
(expected UNTESTABLE).

ARCHIVE-BRANCH IMMUTABILITY CHECK (new this wave, automated in the
enumeration step): every tnn-native-lab-wave-archive-* branch tip was
compared against its previously enumerated pin from the prior wave's
driver table (80 run() lines). Result: 41/41 match, ZERO movement.
In particular tnn-native-lab-wave-archive-20260929-1721pdt remains at
dff8c2005 (no further movement since the prior wave's repointing
finding; 7c11ac5af retained as the fixture pin). The prior wave's
finding stands: archive branches are immutable; the loop re-creates
rather than moves archive branch pointers.

Driver: batch_0732pdt.sh (80 run() lines), derived from batch_fbt.sh by
mechanical edit (wave name, scratch path ~/workspace/fb0930_0732pdt,
run-start pin, live/fixture rotation) plus the declared carry-forward;
body of the run lines byte-identical except the rotation. run_one.sh
sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument.
Harness: REBUILT this run from committed source
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag
(sha256 f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738)
with the pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(command: znc fork_battery.zag -o fork_battery_rebuilt); rebuilt binary
sha256 recorded in FORKBATTERY-RESULT.md and compared against the frozen
instrument ~/workspace/fb1421/fork_battery (a2e6284c...).
Scratch: ~/workspace/fb0930_0732pdt/E/ (80 entry dirs). Zero Python in
battery construction and execution; pure shell, git, sha256sum, pinned
znc, pure-Zag harness.

No em-dashes in this documentation.
