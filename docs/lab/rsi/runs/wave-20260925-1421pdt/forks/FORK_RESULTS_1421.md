# Fork battery results, wave-20260925-1421pdt

Worker 2 (fork battery). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, tested at run-start HEAD 9526cdb5c5d5de732c87583f29d09418894cf8b8.
No commits, merges, resets, rebases, or pushes were made by this worker;
the coordinator commits.

## Summary

All 31 enumerated forks PASS: shell battery (B1, B2 rerun, B2
recompile-identical, B3 `znc check --strict --no-zagd`, NEG1, NEG2,
PROBE) plus the rebuilt pure-Zag harness (VERDICT=PASS, exit 0) on
every fork. znc sha256 matched the pinned sha on every fork.
NEG1/NEG2 discriminated as required everywhere (NEG1 fails compile
and check; NEG2 compiles and checks but its stdout differs from
expected). Zero Python contact anywhere in the run.

GOOD NEWS: the origin/tnn-native-lab tip did NOT move during this
run. Run-start tip 93f0fd54c82cf2af6b1a699b6e56f003707fdc2f was tested
by this battery (entries origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip, both PASS), and the closing
read-only ls-remote reports the identical sha. Both tips that were
untested last wave (695997f5 and 236e5a17815f) are transitively
covered for current-tip purposes via confirmed ancestry of 93f0fd54c
(`git merge-base --is-ancestor`); they were not directly tested at
their own tips. No new untested tip exists for next-wave pickup.

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
tnn-native-lab-wave-archive-wave-20260925-0521pdt,
tnn-native-lab-wave-archive-wave-20260925-0821pdt,
tnn-native-lab-wave-archive-wave-20260925-1121pdt,
wave-debate-session-1-backup. No listed local branch was absent, and
no unlisted local branch was present. New since last wave: the archive
branch tnn-native-lab-wave-archive-wave-20260925-1121pdt (treated as a
fixture this wave per the split rule below, since its SHA has not moved
since it was created).

Remote-tracking refs in this clone: only origin/tnn-native-lab (as last
wave). The listed origin/fs-gr1, origin/main, origin/r2-7,
origin/reorg/phase-0-1, origin/wg-freeze are not remote-tracking refs
here; they were fetched read only into FETCH_HEAD one at a time (no
local ref created or updated, no merge, no reset, no push) and
extracted read only via `git show FETCH_HEAD:<path>`. Nothing was
checked out and nothing was written to any origin/* ref. No fetch
failed this wave.

Worktrees: all 7 forktest/* detached worktrees are still registered
with unchanged SHAs: main 293602fb1d4a2fd5d680a3376463d61b0572006b,
r2-7 a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
reorg_phase-0-1 9914322267e1358e5542a23c72ec51d1a9ae43df,
tnn-native-lab bd30978748fa83bbea6e423a7074cf32b7304291,
tnn-native-lab-remote cea8db22f53ed1294aff5324aa143bd6d1df845e,
wave-debate-session-1-backup 3947dca1a77c00818575dbc7476556c8278b8b7b,
wg-freeze f875b34179f570ba1ad555262cd401ddc4a52848. The three wave3
detached worktrees (probe, senses, trades) are unchanged at
bd30978748fa83bbea6e423a7074cf32b7304291.

## Live vs fixture split

Rule used: Live = fork whose HEAD moved since last wave, or newly
enumerated this wave. Fixture = unchanged-SHA forks tested for
coverage.

Entries total: 31. Live: 3. Fixture: 28. Unique commits tested: 24.

Live: local-tnn-native-lab (moved 0ca683756 -> 9526cdb5c5),
origin-tnn-native-lab (moved 84ed45077 -> 93f0fd54c),
origin-tnn-native-lab-runstart-tip (explicit duplicate: tests the same
commit 93f0fd54c as origin-tnn-native-lab; named explicitly as a
duplicate per the brief).

Fixture: the 12 archive branches (2321pdt, 0221pdt, 0521pdt, 1121pdt,
1421pdt, 1721pdt, wave-1721pdt, wave-2321pdt, wave-0221pdt,
wave-0521pdt, wave-0821pdt, wave-1121pdt), wave-debate-session-1-backup,
the 5 remote heads via FETCH_HEAD, the 7 forktest/* worktrees, and the
3 wave3 worktrees.

The previously untested origin tips from last wave, 695997f5 and
236e5a17815f, are now confirmed ancestors of the merged tip
93f0fd54c (verified with `git merge-base --is-ancestor`): they are
transitively covered for current-tip purposes via confirmed ancestry
of 93f0fd54c; they were not directly tested at their own tips.

All duplicates named explicitly:
- origin-tnn-native-lab-runstart-tip tests the same commit as
  origin-tnn-native-lab (93f0fd54c82cf2af6b1a699b6e56f003707fdc2f).
- wave3-probe, wave3-senses, and wave3-trades each test the same
  commit as forktest-tnn-native-lab
  (bd30978748fa83bbea6e423a7074cf32b7304291).
- forktest-wave-debate-session-1-backup tests the same commit as
  local-wave-debate-session-1-backup
  (3947dca1a77c00818575dbc7476556c8278b8b7b).
- origin-reorg-phase-0-1 (via FETCH_HEAD) tests the same commit as
  forktest-reorg_phase-0-1 (9914322267e1358e5542a23c72ec51d1a9ae43df).
- origin-wg-freeze (via FETCH_HEAD) tests the same commit as
  forktest-wg-freeze (f875b34179f570ba1ad555262cd401ddc4a52848).

## znc mode record

Working-copy pinned znc: file mode 755. All git-extracted copies were
chmod +x in scratch. Git tree modes observed: 100755 on the 2321pdt,
1121pdt, 1421pdt, 1721pdt, wave-1721pdt, wave-2321pdt, wave-0221pdt,
wave-0521pdt, wave-0821pdt, and wave-1121pdt archive branches; 100644
on the 0221pdt and 0521pdt archive branches,
wave-debate-session-1-backup, the origin/tnn-native-lab run-start tip
93f0fd54c, and all five remote heads via FETCH_HEAD. Mode drift is
metadata only: every extracted znc copy sha256 matches the pinned sha.

## Verdicts

znc sha256 matched the pinned sha on every fork: all 31 report
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on every fork:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | 9526cdb5c5d5de732c87583f29d09418894cf8b8 (run-start HEAD; unchanged during this worker's run) | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260923-2321pdt | local-archive-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | local-archive-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | local-archive-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | local-archive-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | local-archive-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-20260924-1721pdt | local-archive-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | local-archive-wave-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt | local-archive-wave-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-0221pdt | local-archive-wave-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-0521pdt | local-archive-wave-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-0821pdt | local-archive-wave-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-1121pdt (new branch, fixture) | local-archive-wave-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab | origin-tnn-native-lab | 93f0fd54c82cf2af6b1a699b6e56f003707fdc2f (run-start tip, tested) | PASS | VERDICT=PASS |
| origin run-start tip (explicit entry) | origin-tnn-native-lab-runstart-tip | 93f0fd54c82cf2af6b1a699b6e56f003707fdc2f (same commit as origin-tnn-native-lab) | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD) | origin-main | 6e621178038f5e0dd61dafa7c70df1e9eca9eb3e | PASS | VERDICT=PASS |
| origin/r2-7 (via FETCH_HEAD) | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 (via FETCH_HEAD) | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df (same commit as forktest-reorg_phase-0-1) | PASS | VERDICT=PASS |
| origin/wg-freeze (via FETCH_HEAD) | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 (same commit as forktest-wg-freeze) | PASS | VERDICT=PASS |
| forktest/main worktree | forktest-main | 293602fb1d4a2fd5d680a3376463d61b0572006b | PASS | VERDICT=PASS |
| forktest/r2-7 worktree | forktest-r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | PASS | VERDICT=PASS |
| forktest/reorg_phase-0-1 worktree | forktest-reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df (same commit as origin-reorg-phase-0-1) | PASS | VERDICT=PASS |
| forktest/tnn-native-lab worktree | forktest-tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as wave3-probe/senses/trades) | PASS | VERDICT=PASS |
| forktest/tnn-native-lab-remote worktree | forktest-tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | PASS | VERDICT=PASS |
| forktest/wave-debate-session-1-backup worktree | forktest-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b (same commit as local-wave-debate-session-1-backup) | PASS | VERDICT=PASS |
| forktest/wg-freeze worktree | forktest-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 (same commit as origin-wg-freeze) | PASS | VERDICT=PASS |
| wave3 probe worktree | wave3-probe | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as forktest-tnn-native-lab) | PASS | VERDICT=PASS |
| wave3 senses worktree | wave3-senses | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as forktest-tnn-native-lab) | PASS | VERDICT=PASS |
| wave3 trades worktree | wave3-trades | bd30978748fa83bbea6e423a7074cf32b7304291 (same commit as forktest-tnn-native-lab) | PASS | VERDICT=PASS |

## Exact shell battery results (per fork)

Every one of the 31 forks recorded the identical pass vector in its
full.log (spot-checked verbatim on local-tnn-native-lab; the vector
pattern was grepped across all 31 full.logs with no exceptions):

- B1: compile exit 0, run exit 0, stdout byte-matches expected.out
  ("FORKBATTERY-OK 42")
- B2 rerun: second run stdout byte-matches expected.out
- B2 recompile-identical: two fresh compiles byte-identical (cmp -s)
- B3: `znc check --strict --no-zagd` exit 0
- NEG1: compile exit nonzero AND check exit nonzero (fails compile and
  check as required); NEG1_fails_as_required=1 on all 31
- NEG2: compiles (exit 0), checks (exit 0), runs (exit 0), stdout
  differs from expected.out; NEG2_fails_as_required=1 on all 31
- PROBE: znc_probe.zag compiles (exit 0), runs (exit 0), stdout
  byte-matches probe_expected.out ("R32_ZNC_PROBE_OK")
- Overall: OVERALL=PASS on 31/31 RESULT.txt files; harness_exit=0
  VERDICT=PASS on 31/31

## Driver provenance

Shell driver adapted from the frozen wave-20260925-1121pdt driver at
~/workspace/tnn-forkbattery-wave-20260925-1121pdt/driver.sh; this wave's
driver is ~/workspace/tnn-forkbattery-wave-20260925-1421pdt/driver.sh.
Deltas: scratch path, wave id, the new archive branch
tnn-native-lab-wave-archive-wave-20260925-1121pdt, and the run-start
tip entry moved to 93f0fd54c82cf2af6b1a699b6e56f003707fdc2f (origin tip
moved 84ed45077 -> 93f0fd54c since last wave; previously untested tips
695997f5 and 236e5a17815f are now ancestors of the merged tip).
wave_head.txt records run-start local HEAD
9526cdb5c5d5de732c87583f29d09418894cf8b8 at 2026-09-25T21:37:10Z. Each
fork scratch dir (under
~/workspace/tnn-forkbattery-wave-20260925-1421pdt/) contains znc
(chmod +x copy), znc_probe.zag, the fixture sources, built binaries,
znc.path, and RESULT.txt/full.log/harness.log. No commits, merges,
resets, rebases, or pushes were made by this worker.

## CANNOT-CONFIRM items

None. The origin/tnn-native-lab tip did not move during this worker's
run (93f0fd54c82cf2af6b1a699b6e56f003707fdc2f at run start and at the
closing re-check), so the run-start tip tested by this battery is still
the latest tip and there are no untested origin tips for next-wave
pickup. Local HEAD was unchanged during the run
(9526cdb5c5d5de732c87583f29d09418894cf8b8 at run start and at closing
check), so no re-run on a moved local tip was needed.

## Closing origin-tip re-check

Run-start origin tip (verbatim, via `git rev-parse origin/tnn-native-lab`
at wave start, matches coordinator expectation):
93f0fd54c82cf2af6b1a699b6e56f003707fdc2f
Closing origin tip (verbatim, via read-only `git ls-remote origin
tnn-native-lab`; updated no local ref):
93f0fd54c82cf2af6b1a699b6e56f003707fdc2f

The tip did NOT move during this run. The battery tested the run-start
tip 93f0fd54c (entries origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip, both PASS). No untested tips exist
for next-wave pickup.

## Python contact statement

Zero Python contact. No python3, no Python scripts, no Python heredocs
were used for any step by this worker or by the driver. Only the pinned
znc binary, the pure-Zag harness, and shell coreutils were used. The
driver and all scratch operations are pure bash; fixtures were written
with shell heredocs.
