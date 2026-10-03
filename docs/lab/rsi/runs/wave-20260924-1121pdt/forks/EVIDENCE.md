# Fork Battery Evidence, wave-20260924-1121pdt

Run date: 2026-09-24 PDT. Runner: fork-battery subagent. Working copy
~/workspace/tnn-rsi, branch tnn-native-lab, HEAD 42e24b381 (merge of
Micah's overnight commits). Nothing committed, nothing pushed, no
working-tree modifications made by this runner.

Pinned znc sha256:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Scratch: ~/workspace/tnn-forkbattery-1121pdt (NOT /tmp). Per-fork
subdirs each contain: znc (chmod +x copy), znc_probe.zag, fixture
sources, built binaries, RESULT.txt, full.log (shell battery),
harness.log (pure-Zag battery), znc.path.

## Method

1. Ran `git fetch origin` (read only; local branches untouched). The
   clone has only origin/tnn-native-lab as a remote-tracking ref, so
   the remaining remote heads were fetched read only into FETCH_HEAD
   via `git fetch origin refs/heads/fs-gr1 refs/heads/main refs/heads/r2-7`
   (no local ref created or updated, no merge, no reset, no push).
2. Extracted each fork's znc read only via
   `git show <ref>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`,
   copied it into the per-fork scratch subdir, chmod +x there.
   Also extracted `src/tools/toolchain/znc_probe.zag` from each
   fork for the fork-tree test.
3. Ran the frozen shell battery per fork (B1, B2, B3, NEG1, NEG2,
   plus fork-tree probe compile+run).
4. Built the pure-Zag harness from
   docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag
   (extracted read only from branch
   tnn-native-lab-wave-archive-20260923-2321pdt; 507 lines, sha256
   f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
   matches expectation) using the pinned znc, and ran it per fork
   with cwd = fork scratch dir and ./znc.path naming the fork's own
   znc copy. The harness binary returns 0 on VERDICT=PASS, 1 otherwise.

## Enumeration and verdicts

znc sha256 matched the pinned sha on every fork: all 11 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | znc sha256 | shell battery | harness |
|---|---|---|---|---|---|
| local tnn-native-lab (working copy) | local-tnn-native-lab | 42e24b38159016256c9c508faa3a0b2162ba6dde | pinned match | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | pinned match | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | pinned match | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt (created this wave) | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | pinned match | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | pinned match | PASS | VERDICT=PASS |
| origin/tnn-native-lab | origin-tnn-native-lab | 2eb04e1b8445784ac127e60141dc0fc6910588ea | pinned match | PASS | VERDICT=PASS |
| origin/fs-gr1 | origin-fs-gr1 | 61aef5669a1aa907c2a8d9602f91ed2881aab39f | pinned match | PASS | VERDICT=PASS |
| origin/main | origin-main | fac34a19f2ad892bba608991c4468cb123e08360 | pinned match | PASS | VERDICT=PASS |
| origin/r2-7 | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | pinned match | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | pinned match | PASS | VERDICT=PASS |
| origin/wg-freeze | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | pinned match | PASS | VERDICT=PASS |

Battery detail per fork (shell driver): B1 compile+run stdout
byte-identical to "FORKBATTERY-OK 42" PASS; B2 rerun identical and two
recompiles byte-identical (sha256 equal) PASS; B3
`znc check forkbat_hello.zag --strict --no-zagd` exit 0 PASS; NEG1
unterminated-string compile exit 1 and check exit 1 (fails as required)
PASS; NEG2 wrong-output program compiled and ran fine with stdout
differing from expected (fails byte-compare as required) PASS;
fork-tree probe `znc_probe.zag` compiled, ran, stdout exactly
"R32_ZNC_PROBE_OK" PASS. The harness logs additionally show
b3_check_stdout=[znc: OK -- all capability claims proven] on every fork.

Per-fork results:
- [local-tnn-native-lab RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/RESULT.txt)
- [local-archive-2321pdt RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/local-archive-2321pdt/RESULT.txt)
- [local-archive-0221pdt RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/local-archive-0221pdt/RESULT.txt)
- [local-archive-0521pdt RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/local-archive-0521pdt/RESULT.txt)
- [local-wave-debate-session-1-backup RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/local-wave-debate-session-1-backup/RESULT.txt)
- [origin-tnn-native-lab RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/origin-tnn-native-lab/RESULT.txt)
- [origin-fs-gr1 RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/origin-fs-gr1/RESULT.txt)
- [origin-main RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/origin-main/RESULT.txt)
- [origin-r2-7 RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/origin-r2-7/RESULT.txt)
- [origin-reorg-phase-0-1 RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/origin-reorg-phase-0-1/RESULT.txt)
- [origin-wg-freeze RESULT.txt](sandbox://workspace/tnn-forkbattery-1121pdt/origin-wg-freeze/RESULT.txt)

Full logs sit next to each RESULT.txt as full.log (shell battery) and
harness.log (pure-Zag harness report).

## forktest/* detached worktrees

Recorded ABSENT, not tested, per task instruction. Discrepancy note:
on inspection the six forktest/* detached worktrees from last wave do
physically exist in this environment at
~/workspace/tnn-rsi-wave3/forktest/ (main 293602fb1, r2-7 a0e7f8ba2,
reorg_phase-0-1 991432226, tnn-native-lab bd3097874,
wave-debate-session-1-backup 3947dca1a, wg-freeze f875b3417, plus an
additional tnn-native-lab-remote cea8db22f), all with valid checkouts
registered in this repo's `git worktree list`. They were not tested,
per instruction, but the "do not exist in this clone" premise did not
hold. Recommend the parent reconciles whether these need a battery run.

## Harness parity statement

No invocation discrepancy. The harness uses exactly the frozen
invocations: compile with
`znc forkbat_hello.zag --no-zagd --no-analyze --no-foreground-cache -o <bin>`
then run the produced binary directly (never parsing znc's stdout
status line into program output), and
`znc check forkbat_hello.zag --strict --no-zagd` for strict checks.
Differences that are cosmetic only: the shell driver wrote the hello
fixture single-line while the harness embeds it multi-line (both print
byte-identical "FORKBATTERY-OK 42"); the harness additionally verifies
the reference sha256 of the expected string
(5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066)
and runs subprocesses via fork/pipe/execve with no shell. Both drivers
agree on every fork: 11/11 shell OVERALL=PASS and 11/11 harness
VERDICT=PASS, exit code 0.

## Mode observation (working-copy znc)

`src/tools/toolchain/znc_linux_x86_64_abed8aa1` in the working tree has
mode 100755 (-rwxr-xr--) versus 100644 committed at HEAD; the working
copy is byte-identical to the pinned sha
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(same as the committed blob). Mode-only drift, no byte drift.

## Python contact

None. Every step used shell commands only: git, sha256sum, cmp, printf,
chmod, grep, wc, the znc binaries themselves, and the compiled pure-Zag
harness binary. No Python interpreter was invoked at any point.

## Summary

11/11 forks PASS. Every enumerated branch and fork, local (tnn-native-lab
at 42e24b381, the three wave archives, wave-debate-session-1-backup)
and remote (origin/tnn-native-lab, fs-gr1, main, r2-7, reorg/phase-0-1,
wg-freeze), carries a znc binary byte-identical to the pinned
498abcb5 sha and passes the full frozen battery on both the shell
driver and the pure-Zag harness: B1, B2, B3, both negative controls
failing as required, and the fork-tree probe compiling and printing
R32_ZNC_PROBE_OK. Nothing broke anywhere. The six forktest/* detached
worktrees are recorded ABSENT/not tested per instruction, though they
were found physically present at ~/workspace/tnn-rsi-wave3/forktest/,
a discrepancy the parent should reconcile.

## Addendum: forktest/* detached worktrees (coordinator correction)

The worker recorded the six forktest/* detached worktrees as ABSENT per the
wave brief. That premise was wrong: they physically exist at
~/workspace/tnn-rsi-wave3/forktest/ and are registered in this repo's
`git worktree list` as detached HEAD checkouts. The coordinator ran the
frozen battery read-only against each worktree's own znc copy (scratch
~/workspace/tnn-forkbattery-1121pdt/forktest_extra/<label>/, worktrees
untouched). Result: 7/7 PASS (B1, B2, B3 PASS; NEG1 and NEG2 fail as
required; znc byte-identical to pinned 498abcb5 everywhere). Full per-fork
logs: forktest_extra/<label>/RESULT.txt.

| Worktree | Detached HEAD | PASS/FAIL | znc sha256 |
|---|---|---|---|
| forktest/main | 293602fb1 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/r2-7 | a0e7f8ba2 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/reorg_phase-0-1 | 991432226 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/tnn-native-lab | bd3097874 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/tnn-native-lab-remote | cea8db22f | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/wave-debate-session-1-backup | 3947dca1a | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |
| forktest/wg-freeze | f875b3417 | PASS | 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |

Corrected fork-battery total this wave: 18/18 PASS (11 from the worker's
enumeration plus 7 forktest worktrees). The ABSENT/NOT TESTED row in the
enumeration table above is superseded by this addendum. The pure-Zag
harness was not rerun on the 7 worktrees (the worker completed before the
correction); the frozen shell battery is the instrument of record for them.

Also recorded: origin/tnn-native-lab moved during this wave. The worker
tested the new remote tip 2eb04e1b8 ("NO-STUPID-LIMITS: limits audit",
Micah, 2026-09-24) read-only via FETCH_HEAD: PASS. Local tnn-native-lab is
2 commits behind that tip; the coordinator will merge it (no reset, no
rebase) before closing the wave.
