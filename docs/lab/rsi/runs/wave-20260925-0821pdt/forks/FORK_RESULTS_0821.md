# Fork battery results, wave-20260925-0821pdt

Worker 2 (fork battery). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, tested at run-start HEAD 382f70f955
(382f70f955dc5dd0e77decf7712bdd51d3ded825). No commits, merges,
resets, rebases, or pushes were made by this worker; the coordinator
commits.

## Summary

All 29 enumerated forks PASS: shell battery (B1, B2 rerun, B2
recompile-identical, B3 `znc check --strict --no-zagd`, NEG1, NEG2,
PROBE) plus the rebuilt pure-Zag harness (VERDICT=PASS, exit 0) on
every fork. znc sha256 matched the pinned sha on every fork.
NEG1/NEG2 discriminated as required everywhere (NEG1 fails compile
and check; NEG2 compiles and checks but its stdout differs from
expected). Zero Python contact anywhere in the run.

ANOMALY: the origin/tnn-native-lab tip moved DURING this worker's
run (run-start 4d613edb1 to closing 40935c121b). The battery tested
the run-start tip only; the new tip 40935c121b822508054297b86ae2ed
b9cec83f56 is untested by this wave's battery and should be picked up
in the next wave's run-start entry.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches expectation). Rebuilt with the pinned znc from this working
copy (src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified before use, file mode 755); built binary sha256:
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
tnn-native-lab-wave-archive-20260924-1721pdt,
tnn-native-lab-wave-archive-wave-20260924-1721pdt,
tnn-native-lab-wave-archive-wave-20260924-2321pdt,
tnn-native-lab-wave-archive-wave-20260925-0221pdt,
tnn-native-lab-wave-archive-wave-20260925-0521pdt (new this wave),
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

Rule used: Live = fork whose HEAD moved since last wave, or newly
enumerated this wave. Fixture = unchanged-SHA forks tested for
coverage.

Live: 4. Fixture: 25.

Live: local-tnn-native-lab (moved 058ee02a8 -> 382f70f95),
origin-tnn-native-lab (moved 4050b1097 -> 4d613edb1),
origin-tnn-native-lab-runstart-tip (duplicate: tests the same commit
4d613edb1 as origin-tnn-native-lab; its tested commit differs from
last wave because the tip moved),
local-archive-wave-0521pdt (new branch this wave at 0ee06268e9).

Fixture: the 9 unchanged archive branches (2321pdt, 0221pdt, 0521pdt,
1121pdt, 1421pdt, 1721pdt, wave-1721pdt, wave-2321pdt, wave-0221pdt),
wave-debate-session-1-backup, the 5 remote heads via FETCH_HEAD (all
SHAs unchanged since last wave), the 7 forktest/* worktrees
(unchanged SHAs), and the 3 wave3 worktrees (unchanged at bd3097874).

Explicit duplicates named: origin-tnn-native-lab-runstart-tip tests
the same commit as origin-tnn-native-lab
(4d613edb11590b23c65d6e65d274b855499fff28); wave3-probe, wave3-senses,
and wave3-trades each test the same commit as forktest-tnn-native-lab
(bd30978748fa83bbea6e423a7074cf32b7304291).

## Closing origin-tip re-check

Run-start origin tip (verbatim, via `git rev-parse origin/tnn-native-lab`
at wave start, matches coordinator expectation):
4d613edb11590b23c65d6e65d274b855499fff28
Closing origin tip (verbatim, via read-only `git ls-remote origin
tnn-native-lab`; updated no local ref):
40935c121b822508054297b86ae2edb9cec83f56

The tip MOVED during this run. The battery tested the run-start tip
4d613edb1 (entries origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip, both PASS). The newly arrived tip
40935c121b is NOT covered by this wave's battery; the coordinator
should pick it up in the next wave. Local HEAD was unchanged during
the run: 382f70f955dc5dd0e77decf7712bdd51d3ded825 at run start and at
closing check, so no re-run on a moved local tip was needed.

## znc mode record

Working-copy pinned znc: file mode 755. All git-extracted copies were
chmod +x in scratch. Git tree modes observed: 100755 on the 2321pdt,
1121pdt, 1421pdt, 1721pdt, wave-1721pdt, wave-2321pdt, wave-0221pdt,
and new wave-0521pdt archive branches; 100644 on the 0221pdt and
0521pdt archive branches, wave-debate-session-1-backup, and the
origin/tnn-native-lab run-start tip 4d613edb1. Mode drift is
metadata only: every extracted znc copy sha256 matches the pinned sha.

## Verdicts

znc sha256 matched the pinned sha on every fork: all 29 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | 382f70f955dc5dd0e77decf7712bdd51d3ded825 (run-start HEAD; unchanged during this worker's run) | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | local-archive-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | local-archive-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1721pdt | local-archive-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | local-archive-wave-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt | local-archive-wave-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-0221pdt | local-archive-wave-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-0521pdt (new this wave) | local-archive-wave-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab | origin-tnn-native-lab | 4d613edb11590b23c65d6e65d274b855499fff28 (run-start tip) | PASS | VERDICT=PASS |
| origin run-start tip (explicit entry) | origin-tnn-native-lab-runstart-tip | 4d613edb11590b23c65d6e65d274b855499fff28 (same commit as origin-tnn-native-lab) | PASS | VERDICT=PASS |
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
| wave3 probe worktree | wave3-probe | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as forktest-tnn-native-lab) | PASS | VERDICT=PASS |
| wave3 senses worktree | wave3-senses | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as forktest-tnn-native-lab) | PASS | VERDICT=PASS |
| wave3 trades worktree | wave3-trades | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as forktest-tnn-native-lab) | PASS | VERDICT=PASS |

## Exact shell battery results (per fork)

Every one of the 29 forks recorded the identical pass vector in its
full.log (spot-checked verbatim on local-archive-2321pdt and
origin-main; the vector pattern was grepped across all 29 full.logs
with no exceptions):

- B1: compile exit 0, run exit 0, stdout byte-matches expected.out
  ("FORKBATTERY-OK 42")
- B2 rerun: second run stdout byte-matches expected.out
- B2 recompile-identical: two fresh compiles byte-identical (cmp -s)
- B3: `znc check --strict --no-zagd` exit 0
- NEG1: compile exit nonzero AND check exit nonzero (fails compile and
  check as required); NEG1_fails_as_required=1 on all 29
- NEG2: compiles (exit 0), checks (exit 0), runs (exit 0), stdout
  differs from expected.out; NEG2_fails_as_required=1 on all 29
- PROBE: znc_probe.zag compiles (exit 0), runs (exit 0), stdout
  byte-matches probe_expected.out ("R32_ZNC_PROBE_OK")
- Overall: OVERALL=PASS on 29/29 RESULT.txt files; harness_exit=0
  VERDICT=PASS on 29/29

## Driver provenance

Shell driver adapted from the frozen wave-20260925-0521pdt driver at
~/workspace/tnn-forkbattery-0521pdt/driver.sh; this wave's driver is
~/workspace/tnn-forkbattery-0821pdt/driver.sh. Deltas: scratch path
(~/workspace/tnn-forkbattery-0821pdt/), wave id, the new archive branch
tnn-native-lab-wave-archive-wave-20260925-0521pdt, and the run-start
tip entry moved to 4d613edb1 (origin tip moved 4050b1097 -> 4d613edb1
since last wave). Each fork scratch dir (under
~/workspace/tnn-forkbattery-0821pdt/) contains znc (chmod +x copy),
znc_probe.zag, the fixture sources, built binaries, znc.path, and
RESULT.txt/full.log/harness.log. wave_head.txt records run-start local
HEAD 382f70f955dc5dd0e77decf7712bdd51d3ded825 at 2026-09-25T15:41:35Z.

## CANNOT-CONFIRM items

The origin/tnn-native-lab tip moved during this worker's run
(4d613edb1 -> 40935c121b). The battery tested the run-start tip
4d613edb1 only, so the new tip
40935c121b822508054297b86ae2edb9cec83f56 is untested by this wave's
battery. This is not a test failure, but it means the wave's fork
coverage does not include the latest origin tip; the coordinator
should run the battery on the new tip next wave. Everything else in
this run is fully confirmed: every enumerated fork ran the full shell
battery and the pure-Zag harness; every znc copy verified byte-identical
to the pinned sha; the harness source and rebuilt binary both matched
expectations; the closing origin-tip re-check was performed.

## Python contact statement

Zero Python contact. No python3, no Python scripts, no Python heredocs
were used for any step by this worker or by the driver. Only the pinned
znc binary, the pure-Zag harness, and shell coreutils were used. The
driver and all scratch operations are pure bash; fixtures were written
with shell heredocs.
