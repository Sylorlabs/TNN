# Fork battery results, wave-20260926-0521pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, run-start HEAD
d0076134ddd105197a9d2c3a9ac552335a406116 (a merge whose second parent
is origin/tnn-native-lab at 6c3c7b69c). Read-only git operations only:
no commits, merges, resets, rebases, fetches, or pushes by this worker.
Scratch: /tmp/tnn-forkbattery-0521pdt (not a prior wave's scratch dir).
Results file left untracked for the coordinator.

## Summary

35 enumerated entries. 33 PASS: shell battery (B1, B2 rerun, B2
recompile-identical, B3 `znc check <file>.zag --strict --no-zagd`,
NEG1, NEG2, PROBE) plus the rebuilt pure-Zag harness (VERDICT=PASS,
exit 0 on all 33). 2 FAIL: origin pull/1/head and pull/2/head, both
extraction failures, not toolchain failures: the pinned znc path and
the probe path do not exist in those trees (see Failure analysis).
On all 33 passing entries the extracted znc sha256 matched the pinned
sha byte for byte and the probe source sha was identical.
NEG1/NEG2 discriminated as required on all 33 (NEG1 fails compile and
check; NEG2 compiles and checks but its stdout differs from expected).

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
local branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the expected value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc from this working copy
(src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use, file mode 755). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to prior waves; harness build is deterministic).
The harness ran per entry with cwd = entry scratch dir and ./znc.path
naming that entry's own extracted znc copy. Harness exit 0 with
VERDICT=PASS on 33/33 tested entries.

## Enumeration (fresh, this wave)

`git branch -a` fresh at run start: 15 local branches and one
remote-tracking ref. Read-only `git ls-remote origin` (no fetch): 6
refs/heads plus 3 refs/pull/*/head refs. In addition, the 10 detached
worktrees under ~/workspace/tnn-rsi-wave3/ were enumerated via
`git worktree list` and tested, consistent with the 0221pdt wave's
coverage; their SHAs are unchanged since 0221pdt.

Local branches (15): tnn-native-lab at
d0076134ddd105197a9d2c3a9ac552335a406116 (moved aaabb0b89 ->
d0076134d since 0221pdt), 13 archive branches all at unchanged SHAs
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
2e2c65fb294e85348d4329ca1e55caf8f6c258a9), and
wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote-tracking: origin/tnn-native-lab at
6c3c7b69ce81915c3fd73159102357e47dc31278 (no longer stale; updated
since 0221pdt).

Remote heads (read-only ls-remote): tnn-native-lab at
6c3c7b69ce81915c3fd73159102357e47dc31278 (moved 1c3f9571 -> 6c3c7b69c
since 0221pdt), fs-gr1 at 23f6c0f9012887448a83edbe9060b73e13d5a7a5,
main at 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185, r2-7 at
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57, pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df. All unchanged since
0221pdt except tnn-native-lab.

Worktrees (10, SHAs verified unchanged since 0221pdt via
git -C <worktree> rev-parse HEAD): forktest/main at
293602fb1d4a2fd5d680a3376463d61b0572006b, forktest/r2-7 at
a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
forktest/reorg_phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df,
forktest/tnn-native-lab at bd30978748fa83bbea6e423a7074cf32b7304291,
forktest/tnn-native-lab-remote at
cea8db22f53ed1294aff5324aa143bd6d1df845e,
forktest/wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b, forktest/wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, and wave3 probe/senses/trades
all at bd30978748fa83bbea6e423a7074cf32b7304291.

Extraction method: local tnn-native-lab used the working-copy znc and
probe directly (working copy is at run-start HEAD; no tracked files
modified by this worker). Every other entry extracted the pinned znc
and probe via read-only `git show <commit>:src/tools/toolchain/...`
into scratch; extracted copies were chmod +x in scratch only. No
worktree was used as a live test target (SHAs were the extraction key).

## Live vs fixture split

Rule used (same as 0221pdt): Live = entry whose HEAD moved since last
wave, or newly enumerated this wave. Fixture = unchanged-SHA entries
tested for coverage.

Named entries total: 35. Live: 3. Fixture: 32.
Unique commits: 27. Unique live commits: 2.

Live: local-tnn-native-lab (aaabb0b89 -> d0076134d),
origin-tnn-native-lab-rt (58dd10ae8 -> 6c3c7b69c),
rh-tnn-native-lab (1c3f9571 -> 6c3c7b69c).

Fixture: the 13 archive branches, wave-debate-session-1-backup,
fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze, pull/1/head,
pull/2/head, pull/3/head (SHAs unchanged since 0221pdt), the 7
forktest/* worktrees, and the 3 wave3 worktrees (all unchanged SHAs).

All duplicates named explicitly with SHAs:
- origin-tnn-native-lab-rt tests the same commit as rh-tnn-native-lab:
  6c3c7b69ce81915c3fd73159102357e47dc31278.
- pull-3-head tests the same commit as rh-reorg-phase-0-1 and
  forktest-reorg_phase-0-1:
  9914322267e1358e5542a23c72ec51d1a9ae43df.
- forktest-wave-debate-session-1-backup tests the same commit as
  local wave-debate-session-1-backup:
  3947dca1a77c00818575dbc7476556c8278b8b7b.
- forktest-wg-freeze tests the same commit as rh-wg-freeze:
  f875b34179f570ba1ad555262cd401ddc4a52848.
- wave3-probe, wave3-senses, and wave3-trades each test the same
  commit as forktest-tnn-native-lab:
  bd30978748fa83bbea6e423a7074cf32b7304291.

## Verdicts (branch name, commit, PASS/FAIL, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| local tnn-native-lab (working copy) | d0076134ddd105197a9d2c3a9ac552335a406116 | PASS | run-start HEAD; live |
| tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture |
| tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | fixture |
| tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | fixture |
| tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | fixture |
| tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | fixture |
| tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | PASS | fixture |
| tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | PASS | fixture |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| origin/tnn-native-lab (remote-tracking) | 6c3c7b69ce81915c3fd73159102357e47dc31278 | PASS | live; duplicate of rh-tnn-native-lab |
| origin/fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
| origin/main | 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185 | PASS | fixture |
| origin/r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | fixture |
| origin/reorg/phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| origin/tnn-native-lab (remote head) | 6c3c7b69ce81915c3fd73159102357e47dc31278 | PASS | live; tested at 6c3c7b69c |
| origin/wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture |
| origin/pull/1/head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FAIL | extraction failure: no toolchain path in tree |
| origin/pull/2/head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FAIL | extraction failure: no toolchain path in tree |
| origin/pull/3/head | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| forktest/main | 293602fb1d4a2fd5d680a3376463d61b0572006b | PASS | fixture |
| forktest/r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | PASS | fixture |
| forktest/reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| forktest/tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture |
| forktest/tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | PASS | fixture |
| forktest/wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| forktest/wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture |
| wave3 probe | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture |
| wave3 senses | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture |
| wave3 trades | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture |

Nothing broke on any toolchain-bearing entry. The two FAILs are
extraction failures (see Failure analysis).

## Uniform battery evidence (all 33 PASS entries)

Verified identical across all 33 RESULT files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (33/33; byte-identical toolchain on every fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (33/33).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42.
- B2: rerun stdout identical; recompile byte-identical (cmp -s);
  bin sha256 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 33 (matches the 2321pdt frozen value).
- B3: `znc check forkbat_hello.zag --strict --no-zagd` exit 0
  ("znc: OK, all capability claims proven").
- NEG1: fails as required on 33/33: compile exit 1, check exit 1
  (E0002: unterminated string literal).
- NEG2: fails as required on 33/33: compile exit 0, check exit 0,
  run exit 0, stdout differs from expected at char 1, line 1.
- PROBE: fork-tree probe compiles with the fork's own znc, exit 0,
  on 33/33.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 33/33
  (reference_sha256 PASS, b1_cmp PASS, b2_bin_cmp PASS, B3 PASS,
  both negative controls failing as required).

## Failure analysis (pull/1/head, pull/2/head)

Both are extraction failures at the first step, identical to the
0221pdt wave: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails (path missing in tree). The probe path
`src/tools/toolchain/znc_probe.zag` was also verified missing in
both trees ("exists on disk, but not in '<commit>'"). Their tree
roots hold non-TNN research documents (.github, README.md, Research/,
R33_FINAL_CLOSEOUT.json); they carry no src/ directory and no
toolchain. This is a property of those forks' contents, not a
toolchain regression. They remain untestable by this battery until
their trees gain the pinned toolchain path.

## Pickup from 0221pdt: coverage changes

Newly covered this wave (previously untracked/uncovered commits,
now tested directly at their own tips):
- d0076134ddd105197a9d2c3a9ac552335a406116 (new local merge tip;
  parents aaabb0b8944a366c39f57dff3f978a004461558c and
  6c3c7b69ce81915c3fd73159102357e47dc31278).
- 6c3c7b69ce81915c3fd73159102357e47dc31278 (new remote tip; the
  origin tip moved 1c3f9571 -> 6c3c7b69c since 0221pdt; tested via
  the remote-tracking and remote-head entries).

Still uncovered: pull/1/head at 5802fec8 and pull/2/head at
4b76bb59f (extraction FAILs again; no toolchain path in tree).
Same status as 0221pdt.

Transitively covered for current-tip purposes; not directly tested
at their own tips (ancestry verified this wave with
git merge-base --is-ancestor):
- 1c3f957190a3aef9fe7b8c37c9a48047aaf403a7 (0221pdt-tested remote
  tip; verified ancestor of the directly tested 6c3c7b69c).
- aaabb0b8944a366c39f57dff3f978a004461558c (0221pdt-tested local
  tip; verified ancestor of the directly tested d0076134d).
- 58dd10ae87c7d6fca4e2ab654c5cccb78907a4fb (0221pdt stale
  remote-tracking ref; verified ancestor of d0076134d).
- bf69a6f387ceb30c06d2ef3b4dd6f0a0170545a0 and cc3b63d1a (the
  1721pdt anomaly commit and the pre-0221pdt local tip; both
  verified ancestors of d0076134d; previously covered via the
  0221pdt coverage of aaabb0b89).

Ancestry note: the archive branches at 3aa59360d3 (0923-2321pdt) and
aab82c57 (0924-0221pdt), wave-debate-session-1-backup at 3947dca1a,
and the remote heads fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze
are NOT ancestors of the current tip (verified); they are genuinely
divergent and were tested directly at their own tips. The worktree
commits 293602fb1d4a (forktest/main), a0e7f8ba2bf0 (forktest/r2-7),
and bd30978748fa (forktest-tnn-native-lab, wave3 probe/senses/trades)
are likewise NOT ancestors; forktest-tnn-native-lab-remote at
cea8db22f IS an ancestor and was tested directly at its own tip.

## Closing tip re-check

Run-start origin tip (read-only `git ls-remote origin tnn-native-lab`):
6c3c7b69ce81915c3fd73159102357e47dc31278
Closing origin tip (read-only `git ls-remote origin tnn-native-lab`):
6c3c7b69ce81915c3fd73159102357e47dc31278

The tip did NOT move during this run. The battery tested the
run-start tip 6c3c7b69c (entries origin-tnn-native-lab-rt and
rh-tnn-native-lab, both PASS). No untested origin tip exists for
next-wave pickup.

## Local HEAD

Run-start HEAD: d0076134ddd105197a9d2c3a9ac552335a406116.
HEAD at run end: d0076134ddd105197a9d2c3a9ac552335a406116.
Local HEAD did NOT move during this run.

Note: two tracked files under docs/lab/rsi/fit_authority/
(AUTHORITY_MANIFEST.md, README.md) were modified by another
concurrent worker during this run (mtimes 05:28 and 05:36 PDT).
This worker made no commits and touched no tracked files.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver and orchestration), git (read-only
rev-parse, branch, ls-remote, show, merge-base, worktree list),
sha256sum, the pinned znc binary, and the rebuilt pure-Zag harness
fork_battery. Disclosure from the prior wave: the 0221pdt worker ran
one `python3` heredoc to patch its driver text; that breach was not
repeated here. This wave's driver (run_fork.sh) was written directly
as a shell script and never edited after first use. No Python was
used for the battery, the harness build, any analysis, or any
verification step.

## Scope stamp

This battery certifies toolchain and extraction stability only, not
the contents of merged commits.
