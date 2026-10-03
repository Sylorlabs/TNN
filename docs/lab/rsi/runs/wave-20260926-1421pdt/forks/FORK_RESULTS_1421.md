# Fork battery results, wave-20260926-1421pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
b6f96edaf8d3e7d422aa0f81db9abc91810671c6 (merge of origin/tnn-native-lab
tip f67e989339a67b882f72378b39fad342a1aa6d9e into local
746ff60ba16d18c36db2ccd4394cbb9db9d6266d; merged by the run executor, no
conflicts; the merged upstream commits are treated as CLOSED, not
re-litigated: content not reviewed, toolchain stability only). Read-only
git operations throughout; no fetch was needed and none was performed
(the queued pickup commits were local objects; the remote-tracking ref
was snapshotted but never touched). Scratch: /tmp/fb1421 (fresh this
wave; /tmp is a 512M tmpfs, checked at 512M free before starting).

## Verdict

40 named entries. 38 PASS, 2 extraction FAIL (origin pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba; both trees lack the pinned
toolchain path, identical cause to the 1121pdt, 0821pdt, and 0521pdt
waves; non-TNN research-doc repos, still uncovered by this battery). 32
unique commits. 6 live entries, 5 unique live commits
(b6f96edaf8d3e7d422aa0f81db9abc91810671c6,
746ff60ba16d18c36db2ccd4394cbb9db9d6266d,
f67e989339a67b882f72378b39fad342a1aa6d9e,
006dfe027944f395a47ae8fe6d1e3329a9d7634e,
7c19065e7b1ce13f6479ba50b4f35e110156c734).
Scope stamp: this battery certifies toolchain and extraction stability
only, not the contents of the merged commits.

## SPOT_RE_RUN (agenda item 1, run first)

Re-ran three 1121pdt entries with the fixed parser (sed extraction of
b2_bin_a_sha256; never cut -d= -f2, since the harness prints all B2
key/value pairs on one line), to confirm the 1121pdt verdicts before
anyone cites them.

- (a) live entry, local tnn-native-lab at the 1121pdt task-pinned HEAD
  02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2: harness exit 0,
  VERDICT=PASS, znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  probe sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
  b2_bin_a sha256 =
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
  probe build exit 0, probe run exit 0, probe stdout R32_ZNC_PROBE_OK.
  Verdict: PASS. 1121pdt PASS confirmed.
- (b) fixture entry, wt-forktest-tnn-native-lab at
  bd30978748fa83bbea6e423a7074cf32b7304291: same evidence values as
  (a), harness exit 0, VERDICT=PASS. Verdict: PASS. 1121pdt PASS
  confirmed.
- (c) extraction-FAIL entry, origin pull/1/head at
  5802fec8401f28b4036b0dd5ebb23905610cab57: znc extraction failed with
  "fatal: path 'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on
  disk, but not in '5802fec8401f28b4036b0dd5ebb23905610cab57'",
  recorded verdict EXTRACTION_FAIL. Verdict: extraction FAIL. 1121pdt
  extraction FAIL confirmed, identical cause.

All three 1121pdt verdicts are confirmed on the fixed parser. The
1121pdt incident 2 bug was confined to the orchestrator summary parser;
no entry was judged on mis-parsed data, and this wave's driver parses
with sed from the start.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from local
branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the expected value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc from this working copy
(src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to prior waves; harness build is deterministic).
The harness ran per entry with cwd = entry scratch dir and ./znc.path
naming that entry's own extracted znc copy. Harness exit 0 with
VERDICT=PASS on 38/38 tested entries, VERDICT=FAIL on 0.

The shell driver run_one.sh is a faithful port of the frozen 2321pdt
driver (identical test sources, identical znc flags, identical expected
output): it extracts the znc and probe read only, records their shas,
verifies both against the pins, runs the rebuilt harness, extracts the
B2 bin sha with sed, confirms NEG1 fails with E0002, confirms NEG2
stdout differs from expected at char 1 (run stdout "WRONG OUTPUT" vs
"FORKBATTERY-OK 42"), compiles the tree probe with the fork's own znc
and runs it expecting R32_ZNC_PROBE_OK, then deletes the per-entry znc
copy.

## Enumeration (fresh, this wave)

`git branch` fresh at run start: 18 local branches. `git branch -r`:
one remote-tracking ref (origin/tnn-native-lab, snapshotted at
f67e989339a67b882f72378b39fad342a1aa6d9e at run start; already at the
run-start tip, untouched by this worker). Read-only `git ls-remote
origin` at run start: 6 refs/heads plus 3 refs/pull/*/head refs. In
addition, the 10 detached worktrees under ~/workspace/tnn-rsi-wave3/
were enumerated via `git worktree list` (SHAs re-verified per worktree,
all unchanged since 1121pdt).

Local branches (18): tnn-native-lab (task-pinned run-start HEAD
b6f96edaf8d3e7d422aa0f81db9abc91810671c6), the 16 archive branches at
the SHAs below (all unchanged since 1121pdt except the newly enumerated
tnn-native-lab-wave-archive-wave-20260926-1121pdt at 746ff60ba):
tnn-native-lab-wave-archive-20260923-2321pdt at
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
2e2c65fb294e85348d4329ca1e55caf8f6c258a9,
tnn-native-lab-wave-archive-wave-20260926-0521pdt at
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5,
tnn-native-lab-wave-archive-wave-20260926-0821pdt at
4bbbca69cecd9c47602e125545b137380e8bab1a,
tnn-native-lab-wave-archive-wave-20260926-1121pdt at
746ff60ba16d18c36db2ccd4394cbb9db9d6266d (newly enumerated this wave),
and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote heads (read-only ls-remote at run start; all non-tnn-native-lab
heads unchanged since 1121pdt): tnn-native-lab at
f67e989339a67b882f72378b39fad342a1aa6d9e, fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5, main at
0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185, r2-7 at
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57, pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df.

Worktrees (10, SHAs re-verified, all unchanged since 1121pdt):
forktest/main at 293602fb1d4a2fd5d680a3376463d61b0572006b,
forktest/r2-7 at a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
forktest/reorg_phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df,
forktest/tnn-native-lab at bd30978748fa83bbea6e423a7074cf32b7304291,
forktest/tnn-native-lab-remote at
cea8db22f53ed1294aff5324aa143bd6d1df845e,
forktest/wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b, forktest/wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, and wave3 probe/senses/trades
all at bd30978748fa83bbea6e423a7074cf32b7304291.

Extraction method: every entry extracted the pinned znc and probe via
read-only `git show <commit>:src/tools/toolchain/...` into scratch;
extracted copies were chmod +x in scratch only. The two queued pickup
tips 006dfe027944f395a47ae8fe6d1e3329a9d7634e and
7c19065e7b1ce13f6479ba50b4f35e110156c734 were local objects
(git cat-file -t commit, both ancestors of the run-start tip
f67e98933), so they were extracted directly; no fetch was performed.

## Live vs fixture split

Rule used (same as 1121pdt and 0821pdt): Live = entry whose HEAD moved
since last wave, or newly enumerated this wave. Fixture = unchanged-SHA
entries tested for coverage.

Named entries total: 40. Live: 6. Fixture: 34.
Unique commits: 32. Unique live commits: 5.

Live: local-tnn-native-lab (02ee5ae59d to b6f96edaf),
arch-wave-0926-1121 (newly enumerated this wave, at 746ff60ba;
this commit is also the first parent of the run-start merge,
recorded as the pre-merge local tip),
origin-tnn-native-lab-rt (7ea4d2e61 to f67e98933 at run start),
rh-tnn-native-lab-tip-start (run-start ls-remote tip f67e98933;
duplicate commit of origin-tnn-native-lab-rt),
rh-tnn-native-lab-tip-006dfe02 (queued pickup from 1121pdt close,
newly tested),
rh-tnn-native-lab-tip-7c19065e (queued pickup from 1121pdt close,
newly tested).

Fixture: the 15 older archive branches, wave-debate-session-1-backup,
fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze, pull/1/head, pull/2/head,
pull/3/head, the 7 forktest worktrees, and the 3 wave3 worktrees
(all unchanged SHAs).

All duplicates named explicitly with SHAs (P8):
- origin-tnn-native-lab-rt and rh-tnn-native-lab-tip-start each test
  the same commit: f67e989339a67b882f72378b39fad342a1aa6d9e.
- rh-reorg-phase-0-1, rh-pull-3-head, and wt-forktest-reorg each test the
  same commit: 9914322267e1358e5542a23c72ec51d1a9ae43df.
- wave-debate-session-1-backup tests the same commit as
  wt-forktest-debate-backup: 3947dca1a77c00818575dbc7476556c8278b8b7b.
- rh-wg-freeze tests the same commit as wt-forktest-wg-freeze:
  f875b34179f570ba1ad555262cd401ddc4a52848.
- wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, and
  wt-wave3-trades each test the same commit:
  bd30978748fa83bbea6e423a7074cf32b7304291.

## Verdicts (entry, commit, PASS/FAIL, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| local tnn-native-lab (task-pinned run-start HEAD) | b6f96edaf8d3e7d422aa0f81db9abc91810671c6 | PASS | live |
| arch wave-0926-1121 (tnn-native-lab-wave-archive-wave-20260926-1121pdt) | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d | PASS | live; newly enumerated |
| origin/tnn-native-lab (remote-tracking, run-start value) | f67e989339a67b882f72378b39fad342a1aa6d9e | PASS | live |
| rh-tnn-native-lab-tip-start (run-start ls-remote tip) | f67e989339a67b882f72378b39fad342a1aa6d9e | PASS | live; duplicate of origin-tnn-native-lab-rt |
| rh-tnn-native-lab-tip-006dfe02 | 006dfe027944f395a47ae8fe6d1e3329a9d7634e | PASS | live; queued pickup from 1121pdt |
| rh-tnn-native-lab-tip-7c19065e | 7c19065e7b1ce13f6479ba50b4f35e110156c734 | PASS | live; queued pickup from 1121pdt |
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
| arch tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | PASS | fixture |
| arch tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a | PASS | fixture |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| rh-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
| rh-main | 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185 | PASS | fixture |
| rh-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | fixture |
| rh-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
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

## Uniform battery evidence (all 38 PASS entries)

Verified across all 38 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (38/38; byte-identical toolchain on every fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (38/38).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (38/38).
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 38 (matches the frozen value; parsed with sed, never cut).
- B3: `znc check forkbat_hello.zag --strict --no-zagd` exit 0
  (38/38).
- NEG1: fails as required on 38/38: compile exit 1, check exit 1, and
  the fork's own znc reports E0002 on the neg1 source on all 38.
- NEG2: fails as required on 38/38: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1, line 1.
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 38/38.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 38/38 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Failure analysis (pull/1/head, pull/2/head)

Both are extraction failures at the first step, identical to the
1121pdt, 0821pdt, and 0521pdt waves: `git show
<commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1` fails ("exists on
disk, but not in '<commit>'" in both cases). The probe path
`src/tools/toolchain/znc_probe.zag` is likewise absent in both trees.
Their tree roots hold non-TNN research documents; they carry no src/
directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

## Incidents

None. No fetch was performed this wave (the queued pickup commits were
local objects), so no remote-tracking ref moved under this worker. The
1121pdt incident 2 parser bug did not recur: the driver extracts
b2_bin_a_sha256 with sed from the first run onward. Local HEAD did not
move during this run (b6f96edaf at start and at close).

## Scratch space

/tmp free at run start: 512M of 512M (0 percent used). /tmp/fb1421 at
run end: 10M total (8.0M pinned znc copy used for harness builds, the
rebuilt harness binary, and per-entry evidence files). Per-entry znc
copies were deleted right after each entry's evidence was complete, so
at most one 8.0M copy was resident at a time and /tmp stayed near 10M
throughout. No /tmp incident this wave.

## Closing tip re-check

Run-start origin tip (read-only `git ls-remote origin tnn-native-lab`):
f67e989339a67b882f72378b39fad342a1aa6d9e.
Closing origin tip (read-only `git ls-remote origin tnn-native-lab`):
f67e989339a67b882f72378b39fad342a1aa6d9e.

The tip did not move during this run. Every tip enumerated during the
1121pdt run (006dfe027944f395a47ae8fe6d1e3329a9d7634e,
7c19065e7b1ce13f6479ba50b4f35e110156c734, both ancestors of
f67e98933) and the run-start tip itself were tested by this battery.
Nothing arrived after the testing window. No further fetch was performed
to chase anything.

## Local HEAD

Task-pinned run-start HEAD: b6f96edaf8d3e7d422aa0f81db9abc91810671c6.
HEAD at run end: b6f96edaf8d3e7d422aa0f81db9abc91810671c6. Local HEAD
did not move during this run. The tested local entry is the task-pinned
run-start HEAD. This worker's only write is this file; it touched no
other tracked files and made no commits.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git (read-only
rev-parse, branch, ls-remote, show, worktree list, cat-file, log,
merge-base; no fetch, no checkout), sha256sum, grep, sed, awk, the
pinned znc binary, and the rebuilt pure-Zag harness fork_battery. No
Python was used for the battery, the harness build, extraction, any
analysis, or any verification step.

## Coordinator addendum: P14 archival (judge-ordered)

The 43 per-entry evidence dirs from /tmp/fb1421/E (RESULT.txt,
zag_harness.out, znc.sha256, tree_probe.zag per entry) were copied into
docs/lab/rsi/runs/wave-20260926-1421pdt/forks/evidence/ and are committed
with this wave's evidence, closing the P14 inspectability gap. The
/tmp/fb1421 scratch is now disposable. S9 note: the frozen harness output
(zag_harness.out) embeds the pinned znc binary's own stdout status line,
which uses the compiler's own punctuation (an em dash in the original tool
output); that is captured instrument output of the frozen toolchain, not
wave documentation, and travels as a disclosed caveat unedited.
