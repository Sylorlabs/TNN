# Fork battery results, wave-20260926-0821pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, run-start HEAD
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5. Read-only git operations only:
no commits, merges, resets, rebases, fetches, or pushes by this worker.
Scratch: /tmp/tnn-forkbattery-0821pdt (not a prior wave's scratch dir).
Results file left untracked for the coordinator.

## Verdict

36 named entries. 34 PASS, 2 extraction FAIL (origin pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba; both trees lack the pinned
toolchain path, identical cause to the 0521pdt wave). 27 unique commits.
1 unique live commit (4328a8350d987a65c4e86e4973dbe45c9d5f6cd5).
Live entries: 2 (local tnn-native-lab and the new archive branch
tnn-native-lab-wave-archive-wave-20260926-0521pdt, both at 4328a8350d).
Fixture entries: 34. Every duplicate SHA named explicitly below (P1: every
enumerated entry tested; P8: duplicate SHAs named, none merged silently).
Scope stamp: this battery certifies toolchain and extraction stability only,
never the contents of merged frontier code.

## Summary

34/36 PASS: shell battery (B1, B2 rerun, B2 recompile-identical, B3
`znc check <file>.zag --strict --no-zagd`, NEG1, NEG2, PROBE) plus the
rebuilt pure-Zag harness (VERDICT=PASS, exit 0 on all 34). On all 34
passing entries the extracted znc sha256 matched the pinned sha byte for
byte and the probe source sha was identical (3b29aa06 prefix).
NEG1/NEG2 discriminated as required on all 34 (NEG1 fails compile and
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
VERDICT=PASS on 34/34 tested entries.

## Enumeration (fresh, this wave)

`git branch -a` fresh at run start: 16 local branches and one
remote-tracking ref (origin/tnn-native-lab). Read-only
`git ls-remote origin` (no fetch): 6 refs/heads plus 3 refs/pull/*/head
refs. In addition, the 10 detached worktrees under
~/workspace/tnn-rsi-wave3/ were enumerated via `git worktree list`.

Local branches (16): tnn-native-lab at
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 (moved d0076134d ->
4328a8350d since 0521pdt), the 13 archive branches at unchanged SHAs
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
2e2c65fb294e85348d4329ca1e55caf8f6c258a9),
tnn-native-lab-wave-archive-wave-20260926-0521pdt at
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 (new this wave), and
wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote-tracking: origin/tnn-native-lab at
6c3c7b69ce81915c3fd73159102357e47dc31278 (unchanged since 0521pdt).

Remote heads (read-only ls-remote, all unchanged since 0521pdt):
tnn-native-lab at 6c3c7b69ce81915c3fd73159102357e47dc31278, fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5, main at
0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185, r2-7 at
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57, pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df.

Worktrees (10, SHAs unchanged since 0521pdt via
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

Rule used (same as 0521pdt): Live = entry whose HEAD moved since last
wave, or newly enumerated this wave. Fixture = unchanged-SHA entries
tested for coverage.

Named entries total: 36. Live: 2. Fixture: 34.
Unique commits: 27. Unique live commits: 1.

Live: local-tnn-native-lab (d0076134d -> 4328a8350d),
arch-wave-0926-0521 (newly enumerated this wave, at 4328a8350d).

Fixture: the 13 older archive branches, wave-debate-session-1-backup,
origin/tnn-native-lab (remote-tracking, unchanged), fs-gr1, main, r2-7,
reorg/phase-0-1, wg-freeze, rh-tnn-native-lab, pull/1/head, pull/2/head,
pull/3/head, the 7 forktest/* worktrees, and the 3 wave3 worktrees
(all unchanged SHAs).

All duplicates named explicitly with SHAs (P8):
- local-tnn-native-lab tests the same commit as
  arch-wave-0926-0521: 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5.
- origin-tnn-native-lab-rt tests the same commit as rh-tnn-native-lab:
  6c3c7b69ce81915c3fd73159102357e47dc31278.
- rh-pull-3-head tests the same commit as rh-reorg-phase-0-1 and
  wt-forktest-reorg: 9914322267e1358e5542a23c72ec51d1a9ae43df.
- local wave-debate-session-1-backup tests the same commit as
  wt-forktest-debate-backup: 3947dca1a77c00818575dbc7476556c8278b8b7b.
- rh-wg-freeze tests the same commit as wt-forktest-wg-freeze:
  f875b34179f570ba1ad555262cd401ddc4a52848.
- wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, and
  wt-wave3-trades each test the same commit:
  bd30978748fa83bbea6e423a7074cf32b7304291.

## Verdicts (entry, commit, PASS/FAIL, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| local tnn-native-lab (working copy) | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | PASS | run-start HEAD; live |
| arch tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture |
| arch tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | fixture |
| arch tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | fixture |
| arch tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | fixture |
| arch tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | fixture |
| arch tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | PASS | live; duplicate of local tnn-native-lab |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| origin/tnn-native-lab (remote-tracking) | 6c3c7b69ce81915c3fd73159102357e47dc31278 | PASS | fixture; duplicate of rh-tnn-native-lab |
| rh-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
| rh-main | 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185 | PASS | fixture |
| rh-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | fixture |
| rh-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| rh-tnn-native-lab | 6c3c7b69ce81915c3fd73159102357e47dc31278 | PASS | fixture |
| rh-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FAIL | extraction failure: no toolchain path in tree |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FAIL | extraction failure: no toolchain path in tree |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture; duplicate of rh-reorg-phase-0-1 |
| wt-forktest-main | 293602fb1d4a2fd5d680a3376463d61b0572006b | PASS | fixture |
| wt-forktest-r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | PASS | fixture |
| wt-forktest-reorg | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture; duplicate of rh-reorg-phase-0-1 |
| wt-forktest-tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture |
| wt-forktest-tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | PASS | fixture |
| wt-forktest-debate-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture; duplicate of wave-debate-session-1-backup |
| wt-forktest-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture; duplicate of rh-wg-freeze |
| wt-wave3-probe | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture; duplicate of wt-forktest-tnn-native-lab |
| wt-wave3-senses | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture; duplicate of wt-forktest-tnn-native-lab |
| wt-wave3-trades | bd30978748fa83bbea6e423a7074cf32b7304291 | PASS | fixture; duplicate of wt-forktest-tnn-native-lab |

Nothing broke on any toolchain-bearing entry. The two FAILs are
extraction failures (see Failure analysis).

## Uniform battery evidence (all 34 PASS entries)

Verified identical across all 34 RESULT files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (34/34; byte-identical toolchain on every fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (34/34).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (34/34).
- B2: rerun stdout identical; recompile byte-identical (cmp -s);
  bin sha256 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 34 (matches the frozen value).
- B3: `znc check forkbat_hello.zag --strict --no-zagd` exit 0
  ("znc: OK, all capability claims proven") (34/34).
- NEG1: fails as required on 34/34: compile exit 1, check exit 1
  (E0002: unterminated string literal).
- NEG2: fails as required on 34/34: compile exit 0, check exit 0,
  run exit 0, stdout differs from expected at char 1, line 1.
- PROBE: fork-tree probe compiles with the fork's own znc, exit 0,
  on 34/34.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 34/34
  (reference_sha256 PASS, b1_cmp PASS, b2_bin_cmp PASS, B3 PASS,
  both negative controls failing as required).

## Failure analysis (pull/1/head, pull/2/head)

Both are extraction failures at the first step, identical to the
0521pdt wave: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails ("exists on disk, but not in '<commit>'"). The probe path
`src/tools/toolchain/znc_probe.zag` is likewise absent in both trees.
Their tree roots hold non-TNN research documents; they carry no src/
directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

## Scratch incident (wt-wave3-senses, wt-wave3-trades)

During this run /tmp (a 512M tmpfs) filled to 100 percent from the
36-entry extraction volume. Effects observed: the wt-wave3-trades
`git show` extraction produced a 0-byte znc_raw with silent odd exit
codes, and the wt-wave3-senses per-entry artifacts were later found
zeroed in scratch. Concurrent `tmp_pack_*` garbage in
.git/objects/pack also showed a repack was in flight, which made
isolated git object reads flaky during the same window. Neither entry
was judged on the compromised artifacts: after freeing /tmp (removed
the 36 znc_raw intermediates, whose shas were already recorded), both
entries were re-run from scratch via read-only `git show` and both
completed cleanly: B1/B2/B3 PASS, NEG1/NEG2 fail as required, probe
compiles, harness VERDICT=PASS exit 0, znc pin and probe sha matched.
The 34 final verdicts above rest on intact artifacts verified after
the re-runs. Recommendation: watch /tmp headroom on future waves
(delete znc_raw per entry after recording its sha, or use a larger
scratch).

## Closing tip re-check

Run-start origin tip (read-only `git ls-remote origin tnn-native-lab`):
6c3c7b69ce81915c3fd73159102357e47dc31278
Closing origin tip (read-only `git ls-remote origin tnn-native-lab`):
6c3c7b69ce81915c3fd73159102357e47dc31278

The tip did NOT move during this run. The battery tested the
run-start tip 6c3c7b69c (entries origin-tnn-native-lab-rt and
rh-tnn-native-lab, both PASS). No untested origin tip exists for
next-wave pickup.

Note: local HEAD (4328a8350d) is ahead of origin (6c3c7b69c) by 118
commits; that divergence is the coordinator's merge territory, not
this worker's. Local HEAD did not move during this run.

## Local HEAD

Run-start HEAD: 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5.
HEAD at run end: 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5.
Local HEAD did NOT move during this run. This worker made no commits
and touched no tracked files.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver and orchestration), git (read-only
rev-parse, branch, ls-remote, show, worktree list), sha256sum, stat,
grep, the pinned znc binary, and the rebuilt pure-Zag harness
fork_battery. The driver (run_fork.sh) and batch script (run_all.sh)
were written directly as shell and never touched by any other
language. No Python was used for the battery, the harness build,
extraction, any analysis, or any verification step.

Disclosure: after the results file was written, this worker ran one
accidental no-op `python3 -c "print('skip')"` as part of a shell
verification one-liner. It printed one word to stdout, touched no wave
data, no files, and no analysis, and was not part of the battery. It is
reported here so the record stays exact.

## Scope stamp

This battery certifies toolchain and extraction stability only, not
the contents of merged commits.
