# Fork battery results, wave-20260925-0221pdt

Worker 2 (fork battery). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, tested at HEAD b4507fb22
(b4507fb22fa176de9d2e4029400ed034802135bd). No commits, merges,
resets, or pushes were made by this worker; the coordinator commits.

## Summary

All 27 enumerated forks PASS: shell battery (B1, B2 rerun, B2
recompile-identical, B3 `znc check --strict --no-zagd`, NEG1, NEG2,
PROBE) plus the rebuilt pure-Zag harness (VERDICT=PASS, exit 0) on
every fork. znc sha256 matched the pinned sha on every fork.
NEG1/NEG2 discriminated as required everywhere (NEG1 fails compile
and check; NEG2 compiles and checks but its stdout differs from
expected). Zero Python contact anywhere in the run.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches expectation). Rebuilt with the pinned znc from this working
copy (src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
file mode 755, no normalization needed); built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to last wave's built harness: harness build is
deterministic). The harness was run per fork with cwd = fork scratch
dir and ./znc.path naming the fork's own znc copy; harness returns 0
on VERDICT=PASS, 1 otherwise.

## Enumeration (fresh, this wave)

Ran `git branch -a` and `git worktree list` fresh; no stale lists used.

Local branches found: tnn-native-lab,
tnn-native-lab-wave-archive-20260923-2321pdt,
tnn-native-lab-wave-archive-20260924-0221pdt,
tnn-native-lab-wave-archive-20260924-0521pdt,
tnn-native-lab-wave-archive-20260924-1121pdt,
tnn-native-lab-wave-archive-20260924-1421pdt,
tnn-native-lab-wave-archive-20260924-1721pdt (new this wave),
tnn-native-lab-wave-archive-wave-20260924-1721pdt,
tnn-native-lab-wave-archive-wave-20260924-2321pdt (new this wave),
wave-debate-session-1-backup. No brief-listed local branch was absent,
and no unlisted local branch was present.

Remote-tracking refs in this clone: only origin/tnn-native-lab (as last
wave). The brief-listed origin/fs-gr1, origin/main, origin/r2-7,
origin/reorg/phase-0-1, origin/wg-freeze are not remote-tracking refs
here; they were fetched read only into FETCH_HEAD one at a time (no
local ref created or updated, no merge, no reset, no push) and
extracted read only via `git show FETCH_HEAD:<path>`. Nothing was
checked out and nothing was written to any origin/* ref. No fetch
failed this wave.

Worktrees: all 7 forktest/* detached worktrees are still registered
with unchanged SHAs: main 293602fb1, r2-7 a0e7f8ba2,
reorg_phase-0-1 991432226, tnn-native-lab bd3097874,
tnn-native-lab-remote cea8db22f, wave-debate-session-1-backup
3947dca1a, wg-freeze f875b3417. The three wave3 detached worktrees
(probe, senses, trades) are unchanged at bd3097874.

## Live vs fixture split

Live (fork whose HEAD moved since last wave, or newly enumerated
this wave): 5. Fixture (unchanged-SHA forks tested for coverage): 22.

Live: local-tnn-native-lab (moved ead33399e2 -> b4507fb22),
origin/tnn-native-lab (moved 787212443 -> 4050b1097),
origin-tnn-native-lab-runstart-tip (moved 14c883855 -> 4050b1097;
tests the same commit as origin/tnn-native-lab this wave),
local-archive-1721pdt (new branch this wave),
local-archive-wave-2321pdt (new branch this wave).

Fixture: the 6 older archive branches (2321pdt, 0221pdt, 0521pdt,
1121pdt, 1421pdt, wave-1721pdt), wave-debate-session-1-backup, the 5
remote heads via FETCH_HEAD (all SHAs unchanged since last wave),
the 7 forktest/* worktrees, and the 3 wave3 worktrees.

## Closing origin-tip re-check

Run-start origin tip (verbatim):
4050b1097941d341c2d02e5efca25fc1877906e5
Closing origin tip (verbatim):
4050b1097941d341c2d02e5efca25fc1877906e5

The tip did not move during this run, so no additional tip needed
testing. origin/tnn-native-lab at 4050b1097 ("Math R2 QUOT addendum")
is the already-CLOSED merge; it was tested read only as a fork and is
not re-litigated here. Local HEAD was also unchanged during the run:
b4507fb22 at run start and at closing check.

## znc mode record

Working-copy pinned znc: file mode 755. All git-extracted copies were
chmod +x in scratch. Git tree modes observed: 100755 on the 1121pdt,
1421pdt, 1721pdt, 2321pdt, wave-1721pdt, and wave-2321pdt archive
branches; 100644 elsewhere. Mode drift is metadata only: every
extracted znc copy sha256 matches the pinned sha.

## Verdicts

znc sha256 matched the pinned sha on every fork: all 27 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | b4507fb22fa176de9d2e4029400ed034802135bd (unchanged during this worker's run) | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | local-archive-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | local-archive-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1721pdt (new this wave) | local-archive-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | local-archive-wave-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt (new this wave) | local-archive-wave-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab (run-start tip) | origin-tnn-native-lab | 4050b1097941d341c2d02e5efca25fc1877906e5 | PASS | VERDICT=PASS |
| origin run-start tip (explicit entry) | origin-tnn-native-lab-runstart-tip | 4050b1097941d341c2d02e5efca25fc1877906e5 | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD) | origin-main | 6e621178038f5e0dd61dafa7c70df1e9eca9eb3e | PASS | VERDICT=PASS |
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
| wave3 probe worktree | wave3-probe | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| wave3 senses worktree | wave3-senses | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |
| wave3 trades worktree | wave3-trades | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | VERDICT=PASS |

## Driver provenance

Shell driver adapted from the frozen wave-20260924-2321pdt driver at
~/workspace/tnn-forkbattery-2321pdt/driver.sh; this wave's driver is
~/workspace/tnn-forkbattery-0221pdt/driver.sh. Deltas: scratch path,
wave id, the two new archive branches
(tnn-native-lab-wave-archive-20260924-1721pdt,
tnn-native-lab-wave-archive-wave-20260924-2321pdt), and the run-start
tip entry updated to 4050b1097. Each fork scratch dir (under
~/workspace/tnn-forkbattery-0221pdt/) contains znc (chmod +x copy),
znc_probe.zag, the fixture sources, built binaries, znc.path, and
RESULT.txt/full.log/harness.log.

## CANNOT-CONFIRM items

None. Every enumerated fork ran the full shell battery and the
pure-Zag harness; every znc copy verified byte-identical to the pinned
sha; the harness source and rebuilt binary both matched expectations;
the closing origin-tip re-check was performed.

## Python contact statement

Zero Python contact. No python3, no Python scripts, no Python heredocs
were used for any step. Only the pinned znc binary, the pure-Zag
harness, and shell coreutils were used.
