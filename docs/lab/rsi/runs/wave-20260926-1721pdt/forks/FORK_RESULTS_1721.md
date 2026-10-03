# Fork battery results, wave-20260926-1721pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
45d449a56b1f0d0ee921e31919a22278bf23a992 (merge of
a222f8f178049b9aeee3b053328c59e9b6fd813d, the 1421pdt wave archive
commit, and 39bf8d5d490a04b22afecdee0d1fa139d4858949, the current
origin/tnn-native-lab tip by Micah; the merged upstream contents are
treated as CLOSED, not re-litigated: content not reviewed, toolchain
stability only). Read-only git operations throughout; no fetch was
performed by this worker. Scratch: /tmp/fb1721 (fresh this wave; /tmp
is a 512M tmpfs, checked at 512M free before starting). The wave lock
was not touched.

## Verdict

39 named entries. 37 PASS, 2 extraction FAIL (origin pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba; both trees lack the pinned
toolchain path, identical cause to every recent wave; non-TNN
research-doc repos, still uncovered by this battery). 31 unique
commits. 4 live entries, 3 unique live commits
(45d449a56b1f0d0ee921e31919a22278bf23a992,
a222f8f178049b9aeee3b053328c59e9b6fd813d,
39bf8d5d490a04b22afecdee0d1fa139d4858949).
Scope stamp: this battery certifies toolchain and extraction stability
only, not the contents of the merged commits.

## SPOT_RE_RUN (agenda item 1, run first)

Re-ran three 1421pdt entries with the fixed parser (sed extraction of
b2_bin_a_sha256; never cut -d= -f2, since the harness prints all B2
key/value pairs on one line), to confirm the 1421pdt verdicts before
anyone cites them.

- (a) live entry, local tnn-native-lab at the 1421pdt task-pinned HEAD
  b6f96edaf8d3e7d422aa0f81db9abc91810671c6: harness exit 0,
  VERDICT=PASS, znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  probe sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
  b2_bin_a sha256 =
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
  b1 run sha256 =
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066,
  NEG1 E0002 hit, NEG2 stdout WRONG OUTPUT differing at char 1, probe
  build exit 0, probe run exit 0, probe stdout R32_ZNC_PROBE_OK.
  Verdict: PASS. 1421pdt PASS confirmed.
- (b) fixture entry, wt-forktest-tnn-native-lab at
  bd30978748fa83bbea6e423a7074cf32b7304291: same evidence values as
  (a), harness exit 0, VERDICT=PASS. Verdict: PASS. 1421pdt PASS
  confirmed.
- (c) extraction-FAIL entry, origin pull/1/head at
  5802fec8401f28b4036b0dd5ebb23905610cab57: znc extraction failed with
  "fatal: path 'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on
  disk, but not in '5802fec8401f28b4036b0dd5ebb23905610cab57'",
  recorded verdict EXTRACTION_FAIL. Verdict: extraction FAIL. 1421pdt
  extraction FAIL confirmed, identical cause.

All three 1421pdt verdicts are confirmed on the fixed parser. This
wave's driver parses with sed from the start. Spot evidence lives in
/tmp/fb1721/E/spot-1421-live-local, /tmp/fb1721/E/spot-1421-fixture-wt,
and /tmp/fb1721/E/spot-1421-fail-pull1, ready for the P14 archive copy.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from local
branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the expected value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc extracted read only from the run-start HEAD
(src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to prior waves; harness build is deterministic).
The harness ran per entry with cwd = entry scratch dir and ./znc.path
naming that entry's own extracted znc copy. Harness exit 0 with
VERDICT=PASS on 37/37 tested battery entries (plus 2/2 spot entries),
VERDICT=FAIL on 0.

The shell driver run_one.sh is a faithful port of the frozen 2321pdt
driver (identical test sources, identical znc flags, identical expected
output): it extracts the znc and probe read only, records their shas,
verifies both against the pins, runs the rebuilt harness, extracts the
B2 bin sha with sed, confirms NEG1 fails with E0002 reported by the
fork's own znc stderr, confirms NEG2 stdout differs from expected at
char 1 (run stdout "WRONG OUTPUT" vs "FORKBATTERY-OK 42"), compiles the
tree probe with the fork's own znc and runs it expecting
R32_ZNC_PROBE_OK, then deletes the per-entry znc copy. Correct
invocations honored: znc prints its status line on stdout (the frozen
harness output captures it; the driver's orchestrator checks never parse
program output out of a compiler status line), and strict checking uses
the flag order `znc check --strict file`.

## Enumeration (fresh, this wave)

`git branch` fresh at run start: 18 local branches. `git branch -r`:
one remote-tracking ref (origin/tnn-native-lab, value
39bf8d5d490a04b22afecdee0d1fa139d4858949 at run start; no fetch was
performed by this worker, so it was untouched by this run). Read-only
`git ls-remote origin` at run start: HEAD plus 6 refs/heads plus 3
refs/pull/*/head refs. In addition, the 10 detached worktrees under
~/workspace/tnn-rsi-wave3/ were enumerated via `git worktree list`
(SHAs re-verified per worktree, all unchanged since 1421pdt).

Local branches (18): tnn-native-lab (task-pinned run-start HEAD
45d449a56b1f0d0ee921e31919a22278bf23a992), the 17 archive branches at
the SHAs below (all unchanged since 1421pdt except the newly enumerated
tnn-native-lab-wave-archive-wave-20260926-1421pdt at a222f8f178):
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
746ff60ba16d18c36db2ccd4394cbb9db9d6266d,
tnn-native-lab-wave-archive-wave-20260926-1421pdt at
a222f8f178049b9aeee3b053328c59e9b6fd813d (newly enumerated this wave),
and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote heads (read-only ls-remote at run start; all non-tnn-native-lab
heads unchanged since 1421pdt): tnn-native-lab at
39bf8d5d490a04b22afecdee0d1fa139d4858949 (moved since 1421pdt, whose
tip was f67e989339a67b882f72378b39fad342a1aa6d9e; the move landed
before run start and was merged into the task-pinned HEAD by the run
executor), fs-gr1 at 23f6c0f9012887448a83edbe9060b73e13d5a7a5, main at
0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185, r2-7 at
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57, pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df.

Worktrees (10, SHAs re-verified, all unchanged since 1421pdt):
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
extracted copies were chmod +x in scratch only. No per-entry znc copy
survives: each was deleted right after its entry's evidence was
complete (0 znc.bin files remain in /tmp/fb1721/E).

## Live vs fixture split

Rule used (same as prior waves): Live = entry whose HEAD moved since
last wave, or newly enumerated this wave. Fixture = unchanged-SHA
entries tested for coverage.

Named entries total: 39. Live: 4. Fixture: 35.
Unique commits: 31. Unique live commits: 3.

Live: local-tnn-native-lab (b6f96edaf to 45d449a56 at run start),
arch-wave-0926-1421 (newly enumerated this wave, at a222f8f178;
this commit is also the first parent of the run-start merge,
recorded as the pre-merge archived 1421pdt state),
origin-tnn-native-lab-rt (f67e98933 to 39bf8d5d at run start),
rh-tnn-native-lab-tip-start (run-start ls-remote tip 39bf8d5d;
duplicate commit of origin-tnn-native-lab-rt).

Fixture: the 16 older archive branches, wave-debate-session-1-backup,
fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze, pull/1/head, pull/2/head,
pull/3/head, the 7 forktest worktrees, and the 3 wave3 worktrees
(all unchanged SHAs).

Note: the 1421pdt close queued pickups 006dfe027944f395a47ae8fe6d1e3329a9d7634e
and 7c19065e7b1ce13f6479ba50b4f35e110156c734 were certified by the
1421pdt battery and are now ancestors of the run-start tip; they are not
separate named entries this wave.

All duplicates named explicitly with SHAs (P8):
- origin-tnn-native-lab-rt and rh-tnn-native-lab-tip-start each test
  the same commit: 39bf8d5d490a04b22afecdee0d1fa139d4858949.
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
| local-tnn-native-lab (task-pinned run-start HEAD) | 45d449a56b1f0d0ee921e31919a22278bf23a992 | PASS | live |
| arch-wave-0926-1421 (tnn-native-lab-wave-archive-wave-20260926-1421pdt) | a222f8f178049b9aeee3b053328c59e9b6fd813d | PASS | live; newly enumerated |
| origin-tnn-native-lab-rt (remote-tracking, run-start value) | 39bf8d5d490a04b22afecdee0d1fa139d4858949 | PASS | live |
| rh-tnn-native-lab-tip-start (run-start ls-remote tip) | 39bf8d5d490a04b22afecdee0d1fa139d4858949 | PASS | live; duplicate of origin-tnn-native-lab-rt |
| arch-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture |
| arch-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | fixture |
| arch-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | fixture |
| arch-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | fixture |
| arch-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | fixture |
| arch-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | fixture |
| arch-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | fixture |
| arch-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | fixture |
| arch-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | PASS | fixture |
| arch-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | PASS | fixture |
| arch-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | PASS | fixture |
| arch-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | PASS | fixture |
| arch-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | PASS | fixture |
| arch-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | PASS | fixture |
| arch-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a | PASS | fixture |
| arch-wave-20260926-1121pdt | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d | PASS | fixture |
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
## Uniform battery evidence (all 37 PASS entries)

Verified across all 37 battery per-entry evidence files (grepped, not
sampled); the 2 spot PASS entries match the same values:

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (37/37 battery; byte-identical toolchain on every fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (37/37).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (37/37); run sha256
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066.
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 37 (matches the frozen value; parsed with sed, never cut).
- B3: `znc check forkbat_hello.zag --strict --no-zagd` exit 0
  (37/37).
- NEG1: fails as required on 37/37: compile exit 1, check exit 1, and
  the fork's own znc reports E0002 on the neg1 source on all 37.
- NEG2: fails as required on 37/37: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1, line 1.
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 37/37.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 37/37 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Failure analysis (pull/1/head, pull/2/head)

Both are extraction failures at the first step, identical to the
1421pdt, 1121pdt, 0821pdt, and 0521pdt waves: `git show
<commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1` fails ("exists on
disk, but not in '<commit>'" in both cases). The probe path
`src/tools/toolchain/znc_probe.zag` is likewise absent in both trees.
Their tree roots hold non-TNN research documents; they carry no src/
directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

## Incidents

None. No fetch was performed by this worker, so no remote-tracking ref
moved under this run. The run-start origin tip move (f67e98933 to
39bf8d5d) landed before run start and was merged into the task-pinned
HEAD by the run executor; the closing tip re-check below confirms no
mid-run move. Local HEAD did not move during this run (45d449a56 at
start and at close). The wave lock was not touched.

## Scratch space

/tmp free at run start: 512M of 512M (0 percent used). /tmp/fb1721 at
run end: 13M total (8.0M pinned znc copy used for harness builds, the
rebuilt harness binary, and per-entry evidence files for 42 entry runs:
39 battery plus 3 spot). Per-entry znc copies were deleted right after
each entry's evidence was complete (0 znc.bin files remain), so at most
one 8.0M copy was resident at a time and /tmp stayed near 13M
throughout. No /tmp incident this wave.

## Closing tip re-check

Run-start origin tip (read-only `git ls-remote origin tnn-native-lab`):
39bf8d5d490a04b22afecdee0d1fa139d4858949.
Closing origin tip (read-only `git ls-remote origin tnn-native-lab`):
39bf8d5d490a04b22afecdee0d1fa139d4858949.

The tip did not move during this run. The run-start tip itself and its
newly merged upstream commits were all tested by this battery via the
task-pinned run-start HEAD. Nothing arrived after the testing window. No
fetch was performed to chase anything.

## Local HEAD

Task-pinned run-start HEAD: 45d449a56b1f0d0ee921e31919a22278bf23a992.
HEAD at run end: 45d449a56b1f0d0ee921e31919a22278bf23a992. Local HEAD
did not move during this run. The tested local entry is the task-pinned
run-start HEAD. This worker's only repo write is this file; it touched
no other tracked files and made no commits.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git (read-only
rev-parse, branch, ls-remote, show, worktree list, cat-file, log; no
fetch, no checkout, no pull, no push), sha256sum, grep, sed, awk, tr,
cmp, the pinned znc binary, and the rebuilt pure-Zag harness
fork_battery. No Python was used for the battery, the harness build,
extraction, any analysis, or any verification step.

## Evidence archive note (P14)

The 42 per-entry evidence dirs from /tmp/fb1721/E (RESULT.txt,
zag_harness.out, znc.path, tree_probe.zag, forkbat_hello.zag, neg1.zag,
neg2.zag, probe_build.log, extract.err per entry; no per-entry znc.bin
by design) are staged for the coordinator's P14 copy into
docs/lab/rsi/runs/wave-20260926-1721pdt/forks/evidence/, including the 3
spot re-run dirs. The /tmp/fb1721 scratch is disposable after that copy.
S9 note: the frozen harness output (zag_harness.out) embeds the pinned
znc binary's own stdout status line, which uses the compiler's own
punctuation (an em dash in the original tool output); that is captured
instrument output of the frozen toolchain, not wave documentation, and
travels as a disclosed caveat unedited.
