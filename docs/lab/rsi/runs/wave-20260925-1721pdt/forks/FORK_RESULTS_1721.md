# Fork battery results, wave-20260925-1721pdt

Worker 2 (fork battery). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, tested at run-start HEAD
cc3b63d1a98e6692b887c5cb8589f6fdbd865c17. This worker commits its
results file locally per the wave task; no merges, resets, rebases,
or pushes were made.

## Summary

35 enumerated forks. 33 PASS: shell battery (B1, B2 rerun, B2
recompile-identical, B3 `znc check --strict --no-zagd`, NEG1, NEG2,
PROBE) plus the rebuilt pure-Zag harness (VERDICT=PASS, exit 0).
2 FAIL: origin-pull-1-head and origin-pull-2-head, both extraction
failures, not toolchain failures: the pinned znc path and the probe
path do not exist in those trees (see Failure analysis). On all 33
passing forks, znc sha256 matched the pinned sha and the probe source
sha was identical. NEG1/NEG2 discriminated as required on all 33
(NEG1 fails compile and check; NEG2 compiles and checks but its
stdout differs from expected). Zero Python contact anywhere in the run.

ANOMALY: local HEAD moved during this worker's run. Run-start HEAD
cc3b63d1a98e6692b887c5cb8589f6fdbd865c17 was tested by this battery
(entry local-tnn-native-lab, which ran first at 2026-09-26T00:42:56Z
and completed before the move). At 2026-09-26T00:49:29Z the
coordinator committed bf69a6f387ceb30c06d2ef3b4dd6f0a0170545a0
("fit_authority: add kb.txt and gaz.txt (D1 residual)") on the
working branch. The battery did NOT test bf69a6f38; it is untested
for next-wave pickup. A read-only diff confirms the toolchain path
src/tools/toolchain/ is byte-unchanged between cc3b63d1a and
bf69a6f38 (the new tip only adds kb.txt and gaz.txt), but that is
not a substitute for battery coverage.

GOOD NEWS: the origin/tnn-native-lab tip did NOT move during this
run. Run-start tip 6ba3b28d2f9ca64140d296c3a612b58063c23cdc was
tested by this battery (entries origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip, both PASS), and the closing
read-only ls-remote reports the identical sha. No untested origin
tip exists for next-wave pickup.

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

Ran `git branch` and `git worktree list` fresh; no stale lists used.

Local branches found (15, not 14 as the brief estimated): tnn-native-lab
at cc3b63d1a98e6692b887c5cb8589f6fdbd865c17, 13 archive branches
(tnn-native-lab-wave-archive-20260923-2321pdt at
3aa59360d3f4849358817fae945aab942882ab92,
tnn-native-lab-wave-archive-20260924-0221pdt at
aab82c574098e8f85d909bfddeac368588f76f72,
tnn-native-lab-wave-archive-20260924-0521pdt at
9f681e2719ea45916da19cad15965717bffa82af,
tnn-native-lab-wave-archive-20260924-1121pdt at
b66c6aeabfff03ceca9194386d98b61574ff4601,
tnn-native-lab-wave-archive-20260924-1421pdt at
c5f0383e2713aa91166b01a1a15229937cea4b3f,
tnn-native-lab-wave-archive-20260924-1721pdt at
088a1914efb308f8a5d8f168f1f9878cf7a4fca8,
tnn-native-lab-wave-archive-wave-20260924-1721pdt at
d24bb4b502022efc675dda80e0e97436acc09278,
tnn-native-lab-wave-archive-wave-20260924-2321pdt at
e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155,
tnn-native-lab-wave-archive-wave-20260925-0221pdt at
058ee02a8a31efc66fb8e92293d399752ce33a6f,
tnn-native-lab-wave-archive-wave-20260925-0521pdt at
0ee06268e9118d1812f7a1e1b85ad384f79a583a,
tnn-native-lab-wave-archive-wave-20260925-0821pdt at
393007563d27b931c8af59ad9d9fedc336fbed1d,
tnn-native-lab-wave-archive-wave-20260925-1121pdt at
60a0579973fa64c80ec2501afc1f5d3080b9b8ba,
tnn-native-lab-wave-archive-wave-20260925-1421pdt at
2e2c65fb294e85348d4329ca1e55caf8f6c258a9 (new branch this wave)),
and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b. No brief-listed local
branch was absent, and no unlisted local branch was present.

Remote-tracking refs in this clone: only origin/tnn-native-lab (as
last wave), still at 6ba3b28d2f9ca64140d296c3a612b58063c23cdc after
this run (the driver's explicit-refspec fetches updated no local
ref; branch count is still 15). Read-only `git ls-remote origin`
showed, in addition to the five heads prior waves saw, three pull
request heads not previously enumerated: refs/pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57, refs/pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, and refs/pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df. All eight remote heads
were fetched read only into FETCH_HEAD one at a time (no local ref
created or updated, no merge, no reset, no push) and extracted read
only via `git show FETCH_HEAD:<path>`. Nothing was checked out and
nothing was written to any origin/* ref. No fetch failed this wave.

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

Entries total: 35. Live: 8. Fixture: 27. Unique commits tested: 27.
Unique live commits: 7.

Live: local-tnn-native-lab (moved 9526cdb5c5 -> cc3b63d1a),
origin-tnn-native-lab (moved 93f0fd54c -> 6ba3b28d2),
origin-tnn-native-lab-runstart-tip (explicit duplicate: tests the same
commit 6ba3b28d2 as origin-tnn-native-lab),
local-archive-wave-1421pdt (new branch this wave at 2e2c65fb29),
origin-main (moved 6e621178 -> 0ab8ed6b),
origin-pull-1-head (newly enumerated at 5802fec84; FAIL, see below),
origin-pull-2-head (newly enumerated at 4b76bb59f; FAIL, see below),
origin-pull-3-head (newly enumerated at 991432226; same commit as the
fixture origin-reorg-phase-0-1, PASS).

Fixture: the 12 unchanged archive branches (2321pdt, 0221pdt, 0521pdt,
1121pdt, 1421pdt, 1721pdt, wave-1721pdt, wave-2321pdt, wave-0221pdt,
wave-0521pdt, wave-0821pdt, wave-1121pdt), wave-debate-session-1-backup,
origin-fs-gr1, origin-r2-7, origin-reorg-phase-0-1, origin-wg-freeze
(SHAs unchanged since last wave), the 7 forktest/* worktrees
(unchanged SHAs), and the 3 wave3 worktrees (unchanged at bd3097874).

All duplicates named explicitly:
- origin-tnn-native-lab-runstart-tip tests the same commit as
  origin-tnn-native-lab (6ba3b28d2f9ca64140d296c3a612b58063c23cdc).
- origin-pull-3-head tests the same commit as origin-reorg-phase-0-1
  and forktest-reorg_phase-0-1
  (9914322267e1358e5542a23c72ec51d1a9ae43df).
- wave3-probe, wave3-senses, and wave3-trades each test the same
  commit as forktest-tnn-native-lab
  (bd30978748fa83bbea6e423a7074cf32b7304291).
- forktest-wave-debate-session-1-backup tests the same commit as
  local-wave-debate-session-1-backup
  (3947dca1a77c00818575dbc7476556c8278b8b7b).
- origin-wg-freeze (via FETCH_HEAD) tests the same commit as
  forktest-wg-freeze (f875b34179f570ba1ad555262cd401ddc4a52848).

## Failure analysis (origin-pull-1-head, origin-pull-2-head)

Both failures are extraction failures at the first step, before any
compilation: `git show FETCH_HEAD:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
and `git show FETCH_HEAD:src/tools/toolchain/znc_probe.zag` fail with
"path exists on disk, but not in 'FETCH_HEAD'". Those trees contain
no src/ directory at all (pull/1 root holds .github, Research,
R33_FINAL_CLOSEOUT.json, README.md; commit message "Checkpoint TNN
research state and ignore reproducible artifacts"; pull/2 commit
message "Clarify E53A preregistration boundary"). The extracted znc
copy is therefore empty (sha256 e3b0c44..., the empty hash),
ZNCSHA_MISMATCH is recorded, every compile step no-ops, and both the
shell battery (OVERALL=FAIL) and the harness (exit 1, VERDICT=FAIL)
report failure honestly. This is a property of those forks' contents
(research-state checkpoints with no toolchain), not a toolchain or
extraction-stability regression: on all 33 toolchain-bearing forks
the pinned znc verified byte-identical. Per the P1 scope stamp below,
the battery certifies toolchain and extraction stability only.

## znc mode record

Working-copy pinned znc: file mode 755. All git-extracted copies were
chmod +x in scratch. Git tree modes observed: 100755 on the 2321pdt,
1121pdt, 1421pdt, 1721pdt, wave-1721pdt, wave-2321pdt, wave-0221pdt,
wave-0521pdt, wave-0821pdt, wave-1121pdt, and wave-1421pdt archive
branches; 100644 on the 0221pdt and 0521pdt archive branches,
wave-debate-session-1-backup, the origin/tnn-native-lab run-start tip
6ba3b28d2, and the remote heads fs-gr1, main, r2-7, reorg/phase-0-1,
wg-freeze, and pull/3/head. The pull-1-head and pull-2-head trees
carry no toolchain path (mode field empty). Mode drift is metadata
only: every extracted znc copy that exists sha256-matches the pinned
sha.

## Verdicts

znc sha256 matched the pinned sha on all 33 toolchain-bearing forks:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on all 33:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.
(The two pull-head failures extracted empty files; see above.)

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | cc3b63d1a98e6692b887c5cb8589f6fdbd865c17 (run-start HEAD; the working copy moved to bf69a6f38 after this entry completed, see ANOMALY) | PASS | VERDICT=PASS |
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
| tnn-native-lab-wave-archive-wave-20260925-1121pdt | local-archive-wave-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | PASS | VERDICT=PASS |
| tnn-native-lab-wave-archive-wave-20260925-1421pdt (new branch) | local-archive-wave-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab | origin-tnn-native-lab | 6ba3b28d2f9ca64140d296c3a612b58063c23cdc (run-start tip, tested) | PASS | VERDICT=PASS |
| origin run-start tip (explicit entry) | origin-tnn-native-lab-runstart-tip | 6ba3b28d2f9ca64140d296c3a612b58063c23cdc (same commit as origin-tnn-native-lab) | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD) | origin-main | 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185 (moved since last wave) | PASS | VERDICT=PASS |
| origin/r2-7 (via FETCH_HEAD) | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 (via FETCH_HEAD) | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df (same commit as forktest-reorg_phase-0-1 and origin-pull-3-head) | PASS | VERDICT=PASS |
| origin/wg-freeze (via FETCH_HEAD) | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 (same commit as forktest-wg-freeze) | PASS | VERDICT=PASS |
| origin/pull/1/head (via FETCH_HEAD, new) | origin-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FAIL (no toolchain path in tree; extraction failed) | VERDICT=FAIL (exit 1) |
| origin/pull/2/head (via FETCH_HEAD, new) | origin-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FAIL (no toolchain path in tree; extraction failed) | VERDICT=FAIL (exit 1) |
| origin/pull/3/head (via FETCH_HEAD, new) | origin-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df (same commit as origin-reorg-phase-0-1) | PASS | VERDICT=PASS |
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

Every one of the 33 passing forks recorded the identical pass vector
in its RESULT.txt (the vector pattern was grepped across all 35
RESULT.txt files; only the two FAIL entries deviate, for the
extraction reason above):

- B1: compile exit 0, run exit 0, stdout byte-matches expected.out
  ("FORKBATTERY-OK 42")
- B2 rerun: second run stdout byte-matches expected.out
- B2 recompile-identical: two fresh compiles byte-identical (cmp -s)
- B3: `znc check --strict --no-zagd` exit 0
- NEG1: compile exit nonzero AND check exit nonzero (fails compile and
  check as required); NEG1_fails_as_required=1 on all 33
- NEG2: compiles (exit 0), checks (exit 0), runs (exit 0), stdout
  differs from expected.out; NEG2_fails_as_required=1 on all 33
- PROBE: znc_probe.zag compiles (exit 0), runs (exit 0), stdout
  byte-matches probe_expected.out ("R32_ZNC_PROBE_OK")
- Overall: OVERALL=PASS on 33/35 RESULT.txt files; harness_exit=0
  VERDICT=PASS on 33/35

## Driver provenance

Shell driver adapted from the frozen wave-20260925-1421pdt driver at
~/workspace/tnn-forkbattery-wave-20260925-1421pdt/driver.sh; this wave's
driver is ~/workspace/tnn-forkbattery-wave-20260925-1721pdt/driver.sh.
Deltas: scratch path, wave id, the new archive branch
tnn-native-lab-wave-archive-wave-20260925-1421pdt, the run-start tip
entry moved to 6ba3b28d2f9ca64140d296c3a612b58063c23cdc (origin tip
moved 93f0fd54c -> 6ba3b28d2 since last wave), and the three newly
enumerated remote pull heads fetched read only into FETCH_HEAD (fetch
fallback from refs/heads/<r> to refs/<r> covers the pull refs; no
local ref created). wave_head.txt records run-start local HEAD
cc3b63d1a98e6692b887c5cb8589f6fdbd865c17 at 2026-09-26T00:42:56Z. Each
fork scratch dir (under
~/workspace/tnn-forkbattery-wave-20260925-1721pdt/) contains znc
(chmod +x copy), znc_probe.zag, the fixture sources, built binaries,
znc.path, and RESULT.txt/full.log/harness.log. No merges, resets,
rebases, or pushes were made by this worker; the fetch loop used
explicit refspecs into FETCH_HEAD only, leaving all local branches
and remote-tracking refs untouched (branch count 15 before and after;
origin/tnn-native-lab still 6ba3b28d2).

## CANNOT-CONFIRM items

1. origin-pull-1-head (5802fec84) and origin-pull-2-head (4b76bb59f)
   carry no toolchain in their trees, so the battery could not run on
   them; their FAIL verdicts certify the extraction failure, not a
   toolchain regression. They remain untestable by this battery until
   their trees gain the pinned toolchain path.
2. The new local tip bf69a6f387ceb30c06d2ef3b4dd6f0a0170545a0,
   committed during this worker's run after the local entry completed,
   is untested by this wave's battery; the coordinator should test it
   next wave. The read-only diff shows src/tools/toolchain/ unchanged
   between the tested tip and the new tip, but that is not battery
   coverage.

## Closing origin-tip re-check

Run-start origin tip (verbatim, via `git rev-parse origin/tnn-native-lab`
at wave start, matches coordinator expectation):
6ba3b28d2f9ca64140d296c3a612b58063c23cdc
Closing origin tip (verbatim, via read-only `git ls-remote origin
tnn-native-lab`; updated no local ref):
6ba3b28d2f9ca64140d296c3a612b58063c23cdc

The tip did NOT move during this run. The battery tested the run-start
tip 6ba3b28d2 (entries origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip, both PASS). No untested origin
tips exist for next-wave pickup.

## Scope stamp

This battery certifies toolchain and extraction stability only, not
the contents of merged commits.

## Python contact statement

Zero Python contact. No python3, no Python scripts, no Python heredocs
were used for any step by this worker or by the driver. Only the pinned
znc binary, the pure-Zag harness, and shell coreutils were used. The
driver and all scratch operations are pure bash; fixtures were written
with shell heredocs.
