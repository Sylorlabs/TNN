# Fork battery results, wave-20260926-0221pdt

Worker 2 (fork battery). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, tested at run-start HEAD
aaabb0b8944a366c39f57dff3f978a004461558c (a merge: parents
02d1dcb31d5f27aa69d7d22d0733a857b2b7d713 local tip and
58dd10ae87c7d6fca4e2ab654c5cccb78907a4fb origin/tnn-native-lab).
This worker commits its results file locally per the wave task; no
merges, resets, rebases, or pushes were made.

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
stdout differs from expected). No Python was used for any battery,
harness, analysis, or verification step (one python3 heredoc was used
once, only to patch this wave's driver text; see Python contact
statement).

GOOD NEWS: local HEAD did NOT move during this worker's run. Run-start
HEAD aaabb0b8944a366c39f57dff3f978a004461558c was captured at
2026-09-26T09:36:26Z and is still HEAD at run end. No untested local
commits exist for next-wave pickup. The 1721pdt anomaly commit
bf69a6f387ceb30c06d2ef3b4dd6f0a0170545a0 (untested at that wave) is
now an ancestor of the tested merge (verified with
git merge-base --is-ancestor), as is cc3b63d1a; both are covered by
this wave's coverage of aaabb0b89.

GOOD NEWS: the origin/tnn-native-lab tip did NOT move during this
run. The live tip at enumeration was
1c3f957190a3aef9fe7b8c37c9a48047aaf403a7 (moved 6ba3b28d2 ->
1c3f9571 since last wave; the local remote-tracking ref is stale at
58dd10ae8, which is the tested merge's second parent, so it is
covered as part of the merge). This wave tested the live tip
1c3f9571 directly (entries origin-tnn-native-lab and
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

Ran `git branch`, `git branch -a`, and `git worktree list` fresh; no
stale lists used.

Local branches found (15, same count as last wave): tnn-native-lab
at aaabb0b8944a366c39f57dff3f978a004461558c (moved cc3b63d1a ->
aaabb0b89 since last wave), 13 archive branches, all at unchanged
SHAs (tnn-native-lab-wave-archive-20260923-2321pdt at
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
2e2c65fb294e85348d4329ca1e55caf8f6c258a9), and
wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b. No brief-listed local
branch was absent, and no unlisted local branch was present.

Remote-tracking refs in this clone: only origin/tnn-native-lab,
stale at 58dd10ae87c7d6fca4e2ab654c5cccb78907a4fb (the merge's
second parent). Read-only `git ls-remote origin` showed the live
origin heads: tnn-native-lab at
1c3f957190a3aef9fe7b8c37c9a48047aaf403a7 (moved 6ba3b28d2 ->
1c3f9571 since last wave), fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5, main at
0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185, r2-7 at
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, and the three pull heads
at the same SHAs as last wave (pull/1 5802fec84, pull/2 4b76bb59f,
pull/3 991432226). All nine remote heads were fetched read only
into FETCH_HEAD one at a time (no local ref created or updated, no
merge, no reset, no push) and extracted read only via
`git show FETCH_HEAD:<path>`. Nothing was checked out and nothing
was written to any origin/* ref. No fetch failed this wave.

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

Entries total: 35. Live: 3. Fixture: 32. Unique commits tested: 27.
Unique live commits: 2.

Live: local-tnn-native-lab (moved cc3b63d1a -> aaabb0b89),
origin-tnn-native-lab (moved 6ba3b28d2 -> 1c3f9571),
origin-tnn-native-lab-runstart-tip (explicit duplicate: tests the same
commit 1c3f9571 as origin-tnn-native-lab).

Fixture: the 13 unchanged archive branches, wave-debate-session-1-backup,
origin-fs-gr1, origin-main, origin-r2-7, origin-reorg-phase-0-1,
origin-wg-freeze, origin-pull-1-head, origin-pull-2-head,
origin-pull-3-head (SHAs unchanged since last wave), the 7 forktest/*
worktrees (unchanged SHAs), and the 3 wave3 worktrees (unchanged at
bd3097874).

All duplicates named explicitly:
- origin-tnn-native-lab-runstart-tip tests the same commit as
  origin-tnn-native-lab (1c3f957190a3aef9fe7b8c37c9a48047aaf403a7).
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
compilation, identical to last wave: `git show
FETCH_HEAD:src/tools/toolchain/znc_linux_x86_64_abed8aa1` and
`git show FETCH_HEAD:src/tools/toolchain/znc_probe.zag` fail with
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
wave-debate-session-1-backup, and all live remote heads (tnn-native-lab
1c3f9571, fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze, pull/3/head).
The pull-1-head and pull-2-head trees carry no toolchain path (mode
field empty). Mode drift is metadata only: every extracted znc copy
that exists sha256-matches the pinned sha.

## Verdicts

znc sha256 matched the pinned sha on all 33 toolchain-bearing forks:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
znc_probe.zag sha256 was identical on all 33:
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919.
(The two pull-head failures extracted empty files; see above.)

| ref | label | commit | shell battery | harness |
|---|---|---|---|---|
| working copy, branch tnn-native-lab | local-tnn-native-lab | aaabb0b8944a366c39f57dff3f978a004461558c (run-start HEAD, merge; HEAD did not move during this run) | PASS | VERDICT=PASS |
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
| tnn-native-lab-wave-archive-wave-20260925-1421pdt | local-archive-wave-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | PASS | VERDICT=PASS |
| wave-debate-session-1-backup | local-wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | VERDICT=PASS |
| origin/tnn-native-lab live tip (via FETCH_HEAD) | origin-tnn-native-lab | 1c3f957190a3aef9fe7b8c37c9a48047aaf403a7 (moved 6ba3b28d2 -> 1c3f9571 since last wave) | PASS | VERDICT=PASS |
| origin run-start tip (explicit entry) | origin-tnn-native-lab-runstart-tip | 1c3f957190a3aef9fe7b8c37c9a48047aaf403a7 (same commit as origin-tnn-native-lab) | PASS | VERDICT=PASS |
| origin/fs-gr1 (via FETCH_HEAD) | origin-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | VERDICT=PASS |
| origin/main (via FETCH_HEAD) | origin-main | 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185 | PASS | VERDICT=PASS |
| origin/r2-7 (via FETCH_HEAD) | origin-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | VERDICT=PASS |
| origin/reorg/phase-0-1 (via FETCH_HEAD) | origin-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df (same commit as forktest-reorg_phase-0-1 and origin-pull-3-head) | PASS | VERDICT=PASS |
| origin/wg-freeze (via FETCH_HEAD) | origin-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 (same commit as forktest-wg-freeze) | PASS | VERDICT=PASS |
| origin/pull/1/head (via FETCH_HEAD) | origin-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FAIL (no toolchain path in tree; extraction failed) | VERDICT=FAIL (exit 1) |
| origin/pull/2/head (via FETCH_HEAD) | origin-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FAIL (no toolchain path in tree; extraction failed) | VERDICT=FAIL (exit 1) |
| origin/pull/3/head (via FETCH_HEAD) | origin-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df (same commit as origin-reorg-phase-0-1) | PASS | VERDICT=PASS |
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

Shell driver adapted from the frozen wave-20260925-1721pdt driver at
~/workspace/tnn-forkbattery-wave-20260925-1721pdt/driver.sh; this wave's
driver is ~/workspace/tnn-forkbattery-wave-20260926-0221pdt/driver.sh.
Deltas: scratch path, wave id, no new archive branch (branch set
unchanged at 15); local HEAD is now the merge aaabb0b89; the
run-start-tip entries now test the live origin tip
1c3f957190a3aef9fe7b8c37c9a48047aaf403a7 (origin tip moved 6ba3b28d2
-> 1c3f9571 since last wave), and the remote head loop now includes
tnn-native-lab itself fetched read only into FETCH_HEAD (fetch
fallback from refs/heads/<r> to refs/<r> covers the pull refs; no
local ref created). wave_head.txt records run-start local HEAD
aaabb0b8944a366c39f57dff3f978a004461558c at 2026-09-26T09:39:02Z
(first capture at 2026-09-26T09:36:26Z, same sha). Each fork scratch
dir (under ~/workspace/tnn-forkbattery-wave-20260926-0221pdt/)
contains znc (chmod +x copy), znc_probe.zag, the fixture sources,
built binaries, znc.path, and RESULT.txt/full.log/harness.log. No
merges, resets, rebases, or pushes were made by this worker; the
fetch loop used explicit refspecs into FETCH_HEAD only, leaving all
local branches and remote-tracking refs untouched (branch count 15
before and after; origin/tnn-native-lab still 58dd10ae8).

## CANNOT-CONFIRM items

1. origin-pull-1-head (5802fec84) and origin-pull-2-head (4b76bb59f)
   carry no toolchain in their trees, so the battery could not run on
   them; their FAIL verdicts certify the extraction failure, not a
   toolchain regression. They remain untestable by this battery until
   their trees gain the pinned toolchain path.
2. The local remote-tracking ref origin/tnn-native-lab is stale at
   58dd10ae8; this wave tested the live origin tip 1c3f9571 directly
   via FETCH_HEAD, and 58dd10ae8 is covered as the tested merge's
   second parent. No untested origin tip exists.

## Closing origin-tip re-check

Run-start origin tip (verbatim, via read-only `git ls-remote origin`
at wave start, and re-confirmed by the driver's FETCH_HEAD fetch):
1c3f957190a3aef9fe7b8c37c9a48047aaf403a7
Closing origin tip (verbatim, via read-only `git ls-remote origin
tnn-native-lab`; updated no local ref):
1c3f957190a3aef9fe7b8c37c9a48047aaf403a7

The tip did NOT move during this run. The battery tested the run-start
tip 1c3f9571 (entries origin-tnn-native-lab and
origin-tnn-native-lab-runstart-tip, both PASS). No untested origin
tips exist for next-wave pickup.

## Scope stamp

This battery certifies toolchain and extraction stability only, not
the contents of merged commits.

## Python contact statement

One python3 heredoc was used exactly once, to apply a multi-line
text patch to this wave's driver.sh. No Python was used for the
battery, the harness, any analysis, or any verification step. Apart
from that single text edit, zero Python contact: only the pinned
znc binary, the pure-Zag harness, and shell coreutils were used.
The driver and all scratch operations are pure bash; fixtures were
written with shell heredocs.
