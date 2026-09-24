# Fork Battery Evidence, wave-20260924-1421pdt

Run date: 2026-09-24 PDT. Runner: fork-battery subagent. Working copy
~/workspace/tnn-rsi, branch tnn-native-lab.

HEAD moved mid-wave: the task brief pinned 28088d207, but a concurrent
wave worker committed on tnn-native-lab while this battery ran. HEAD at
evidence time: ef6801b3a4ac427a4ddcedef9b4e073d053f1505 ("tnn_chat FIT
re-verification wave-20260924-1421pdt"). 28088d207 is an ancestor of
ef6801b3. The working-copy fork entry below tested the working tree znc
at run time (HEAD ef6801b3); it is byte-identical to the pinned binary.

Pinned znc sha256:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Scratch: ~/workspace/tnn-forkbattery-1421pdt (NOT /tmp). Per-fork
subdirs each contain: znc (chmod +x copy), znc_probe.zag, fixture
sources, built binaries, RESULT.txt, full.log (shell battery),
harness.log (pure-Zag battery), znc.path. The shell driver lives at
~/workspace/tnn-forkbattery-1421pdt/driver.sh.

## Enumeration vs the wave brief

Ran `git branch -a` and `git worktree list` fresh; no stale lists used.

Local branches found (all in the brief): tnn-native-lab,
tnn-native-lab-wave-archive-20260923-2321pdt,
tnn-native-lab-wave-archive-20260924-0221pdt,
tnn-native-lab-wave-archive-20260924-0521pdt,
tnn-native-lab-wave-archive-20260924-1121pdt,
wave-debate-session-1-backup. No local branch in the brief was absent,
and no unlisted local branch was present.

Remote-tracking refs in this clone: only origin/tnn-native-lab (as last
wave). The brief-listed origin/fs-gr1, origin/main, origin/r2-7,
origin/reorg/phase-0-1, origin/wg-freeze are not remote-tracking refs
here; they were fetched read only into FETCH_HEAD (no local ref
created or updated, no merge, no reset, no push) and extracted read
only via `git show <ref>:<path>`. Nothing was checked out and nothing
was written to any origin/* ref.

Worktrees: all 7 forktest/* detached worktrees from 1121pdt are still
registered with unchanged SHAs: main 293602fb1, r2-7 a0e7f8ba2,
reorg_phase-0-1 991432226, tnn-native-lab bd3097874,
tnn-native-lab-remote cea8db22f, wave-debate-session-1-backup 3947dca1a,
wg-freeze f875b3417. They were battery-tested read only (scratch copies
of each worktree's own znc; worktrees untouched).

Not in the brief, present, NOT tested: three extra detached worktrees at
~/workspace/tnn-rsi-wave3/ (probe, senses, trades, all at bd3097874).
Flagged for the coordinator; outside this task's scope.

## Method

1. `git fetch origin` (read only; local branches untouched) to observe
   the current origin/tnn-native-lab tip.
2. Per remote head: `git fetch origin refs/heads/<name>` into FETCH_HEAD
   only, then extracted the fork's znc and znc_probe.zag read only via
   `git show FETCH_HEAD:<path>`, copied into the per-fork scratch dir,
   chmod +x on the copy.
3. Ran the frozen shell battery per fork (B1, B2, B3, NEG1, NEG2, plus
   the fork-tree probe compile+run), using the frozen invocations:
   `znc <file> --no-zagd --no-analyze --no-foreground-cache -o <bin>`
   then run the produced binary directly (never parsing znc's stdout
   status line into program output), and
   `znc check <file> --strict --no-zagd` for strict checks.
4. Rebuilt the pure-Zag harness from
   docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag
   (extracted read only from branch
   tnn-native-lab-wave-archive-20260923-2321pdt; sha256
   f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
   matches expectation). The rebuilt binary is byte-identical to last
   wave's built harness
   (a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66):
   harness build is deterministic. Ran it per fork with cwd = fork
   scratch dir and ./znc.path naming the fork's own znc copy; the
   harness binary returns 0 on VERDICT=PASS, 1 otherwise.

## Verdicts

znc sha256 matched the pinned sha on every fork: all 19 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | ef6801b3 (tested worktree file) | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | local-archive-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab | origin-tnn-native-lab | 9d4f484bfe86c9ee28b19ee55e9a049af65fd715 | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD) | origin-main | f2a0ecfdc2488162815c36478bc850dd18d3d532 | PASS | VERDICT=PASS |
| origin/r2-7 (via FETCH_HEAD) | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 (via FETCH_HEAD) | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | VERDICT=PASS |
| origin/wg-freeze (via FETCH_HEAD) | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | VERDICT=PASS |
| forktest/main worktree | forktest-main | 293602fb1d4a2fd5d680a3376463d61b0572006b | PASS | VERDICT=PASS |
| forktest/r2-7 worktree | forktest-r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | PASS | VERDICT=PASS |
| forktest/reorg_phase-0-1 worktree | forktest-reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | VERDICT=PASS |
| forktest/tnn-native-lab worktree | forktest-tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| forktest/tnn-native-lab-remote worktree | forktest-tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | PASS | VERDICT=PASS |
| forktest/wave-debate-session-1-backup worktree | forktest-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| forktest/wg-freeze worktree | forktest-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | VERDICT=PASS |

Battery detail per fork (shell driver): B1 compile+run stdout
byte-identical to "FORKBATTERY-OK 42" PASS; B2 rerun identical and two
recompiles byte-identical (sha256 equal) PASS; B3
`znc check <file> --strict --no-zagd` exit 0 PASS; NEG1
unterminated-string compile exit 1 and check exit 1 (fails as required)
PASS; NEG2 wrong-output program compiled and ran fine with stdout
differing from expected (fails byte-compare as required) PASS;
fork-tree probe `znc_probe.zag` compiled, ran, stdout exactly
"R32_ZNC_PROBE_OK\n" PASS. The harness logs additionally show
b3_check_stdout=[znc: OK -- all capability claims proven] on every fork.

## Negative controls

NEG1 and NEG2 discriminated on all 19 forks: NEG1 compile and check
both exited 1; NEG2 compiled and passed check but its stdout differed
from the reference (fails byte-compare as required). No fork reported
CANNOT-CONFIRM. Per-fork RESULT.txt records B1=1 B2_rerun=1
B2_recompile_identical=1 B3=1 NEG1=1 NEG2=1 PROBE=1 and harness exit 0
with VERDICT=PASS everywhere.

## origin/tnn-native-lab tip observed this wave

The remote tip moved twice during this wave. Pre-wave local
remote-tracking ref was e1f78ba35. First `git fetch origin` brought
ad7919c25 ("PAM RT-X: build sources for battery B-3034-X..."); a
follow-up fetch minutes later brought 9d4f484bfe ("CRITIC 4: fix doubled
path ..."), which was stable across re-checks. The battery tested
9d4f484bfe read only (never checked out, never written). Local
tnn-native-lab is behind that tip; the merge is the coordinator's call,
not this runner's.

Remote head changes since 1121pdt: fs-gr1 61aef5669 -> 23f6c0f90;
main fac34a19 -> f2a0ecfd; tnn-native-lab 2eb04e1b8 -> 9d4f484bfe;
r2-7, reorg/phase-0-1, wg-freeze unchanged.

## Coverage notes

- No brief-listed branch was absent; no unlisted branch was present.
- The seven forktest/* worktrees were all still registered and were
  tested read only (unlike 1121pdt, where the worker marked them ABSENT
  and the coordinator tested them after; this wave both the shell
  driver and the pure-Zag harness ran on them: 7/7 VERDICT=PASS).
- Three extra detached worktrees exist at ~/workspace/tnn-rsi-wave3/
  (probe, senses, trades, all at bd3097874); not in the brief, not
  tested. The coordinator should decide whether they need battery
  coverage.

## Mode observation (working-copy znc)

The working tree znc has mode 754 (-rwxr-xr--) versus 100755 recorded in
the index; byte-identical to the pinned sha
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
Mode-only drift, no byte drift. (Last wave the drift was 100755 worktree
vs 100644 committed; the index now records 100755.)

## Python contact

None. Every step used shell commands only: git, sha256sum, cmp,
printf, chmod, grep, wc, stat, the znc binaries themselves, and the
compiled pure-Zag harness binary. No Python interpreter was invoked at
any point. Scratch was under ~/workspace, never /tmp.

## Coordinator attestation (independent judge correction 4, wave-20260924-1421pdt)

Every fork in the table above carries its tested commit sha explicitly
(full 40-char shas in the per-fork table). Tested HEADs pinned: working
copy tnn-native-lab at ef6801b3a4ac427a4ddcedef9b4e073d053f1505 (wave
brief pinned 28088d207, an ancestor; HEAD moved under the battery via
concurrent worker commits); origin/tnn-native-lab at
9d4f484bfe86c9ee28b19ee55e9a049af65fd715 (tested read-only; the tip moved
twice mid-wave: e1f78ba35 to ad7919c25 to 9d4f484bfe). Not tested: three
detached worktrees at ~/workspace/tnn-rsi-wave3/ (all at bd3097874, same
sha as tested forktest/tnn-native-lab; queued for next wave enumeration).

## Summary

19/19 forks PASS. Every enumerated branch and fork (local
tnn-native-lab, the four wave archives, wave-debate-session-1-backup,
origin/tnn-native-lab at the current tip 9d4f484bfe, the five other
remote heads, and all seven forktest/* worktrees) carries a znc binary
byte-identical to the pinned 498abcb5 sha and passes the full frozen
battery on both the shell driver and the pure-Zag harness: B1, B2, B3,
both negative controls failing as required, and the fork-tree probe
compiling and printing R32_ZNC_PROBE_OK. Nothing broke anywhere.
