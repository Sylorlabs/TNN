# ENUMERATION_MANIFEST (fork-battery run, 2026-09-30)

Run-start pin: 955106ae5fb7b8e62a9ed6273c3048a5a2f8f156 (local
tnn-native-lab tip at enumeration time; pinned-commit discipline: every
extraction is by pinned SHA, never by live ref, so mid-battery lane
commits are inert).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e
(unchanged since wave-20260930-0221pdt; read-only git ls-remote this run:
HEAD/main 27a4271f, fs-gr1 23f6c0f9, r2-7 2d99d183, reorg/phase-0-1
991432226, tnn-native-lab bedf8b4aa, wg-freeze f875b3417, pull/1
5802fec8, pull/2 4b76bb59, pull/3 991432226. Zero new remote refs.)

Enumeration method: the 0221pdt 77-entry table carried forward verbatim,
with these changes:
(a) NEW local archive tnn-native-lab-wave-archive-20260930-0221pdt at
697d4f308bb8e2a5b65df3502e6a66b5fecd3f2a, LIVE entry
arch-wave-20260930-0221pdt.
(b) Archive branch tnn-native-lab-wave-archive-20260929-1721pdt MOVED
since 0221pdt: was 7c11ac5af (enumerated), now dff8c200590a64023b64e9c3a5fbdc4dcf4766b9
(a descendant; reflog "branch: Created from HEAD"; extra wave-1721pdt
record commits). The moved tip is a new LIVE entry
arch-wave-20260929-1721pdt-tip2; the old pin 7c11ac5af stays as the
fixture arch-wave-20260929-1721pdt.
(c) local-tnn-native-lab now tested at the new run-start pin 955106ae5
(LIVE); its 0221pdt pin 1f681e87b moves to the fixture set under the
renamed entry local-20260930-0221pdt-tip (full date: local-tnn-native-lab
is taken by the new LIVE entry).
Total: 80 named entries (3 LIVE, 77 fixture).

Live entries (3):
- arch-wave-20260930-0221pdt (697d4f308, newly enumerated archive)
- arch-wave-20260929-1721pdt-tip2 (dff8c2005, moved archive branch tip)
- local-tnn-native-lab (955106ae5, run-start tip)
Fixture entries (77): all 0221pdt entries at their pins, every SHA
verified to resolve in this repo before the run (git cat-file -t loop,
77/77 commit, zero misses), plus the renamed local-20260930-0221pdt-tip.
Duplicate SHA groups carried: {arch-wave-20260929-1721pdt,
local-1721pdt-tip} at 7c11ac5af; {arch-wave-20260927-0221pdt,
local-0221pdt-tip} per 1421pdt manifest; {rh-pull-3-head, rh-reorg-phase-0-1,
wt-forktest-reorg} at 991432226; {wave-debate-session-1-backup,
wt-forktest-debate-backup} at 3947dca1a; exp/wt-exp pairs at 1010a63c3,
a2a36e657, c368b8e1f; {wt-forktest-tnn-native-lab, wt-wave3-probe,
wt-wave3-senses, wt-wave3-trades} at bd3097874.
The experimental branches (wave-20260927-0221pdt-exp1/exp2/sensory) resolve
to the same SHAs as the exp fixture entries, so they are covered by
pinned-SHA extraction, not re-enumerated.
Stale refs/remotes/rh-* (remote "rh" no longer configured) carried as
fixtures at their pins; rh-pull-1-head (5802fec8) and rh-pull-2-head
(4b76bb59) are non-TNN trees with the pinned toolchain path absent
(expected UNTESTABLE).

Driver: batch_fbt.sh (80 run() lines), derived from frozen batch_0221.sh
by mechanical edit (wave name, scratch path
~/workspace/fb0930_forkbatt, run-start pin, live/fixture rotation) plus
the declared carry-forward; body of the run lines byte-identical except
the rotation. run_one.sh sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument.
Harness: REBUILT this run from committed source
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag
(sha256 f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738)
with the pinned znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(command: znc fork_battery.zag -o fork_battery_rebuilt). Rebuilt binary
sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
BYTE-IDENTICAL to the frozen instrument ~/workspace/fb1421/fork_battery.
Scratch: ~/workspace/fb0930_forkbatt/E/ (80 entry dirs). Zero Python in
battery construction and execution; pure shell, git, sha256sum, pinned
znc, pure-Zag harness.

No em-dashes in this documentation.
