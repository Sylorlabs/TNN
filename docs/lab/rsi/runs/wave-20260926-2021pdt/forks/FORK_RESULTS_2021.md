# Fork battery results, wave-20260926-2021pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91 (merge of
a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a, the executor's pre-merge
state, and 75267f9df70702fcd473619c70a454b191d21a9c, the
origin/tnn-native-lab tip at merge time; the merged upstream contents
are treated as CLOSED, not re-litigated: content not reviewed,
toolchain stability only). Read-only git operations throughout; no
fetch was performed by this worker. Scratch: /tmp/fb2021 (fresh this
wave; /tmp is a 512M tmpfs, 512M free at run start). The wave lock was
not touched.

## Verdict

40 named battery entries. 36 PASS, 4 extraction FAIL. 33 unique
commits. 5 live entries, 5 unique live commits; 35 fixture entries.
Two extraction FAILs are the expected ones: origin pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (both trees lack the pinned
toolchain path, identical cause five waves running; non-TNN
research-doc repos, still uncovered by this battery). Two extraction
FAILs are new live remote tips whose commits are absent from the local
object store: rh-tnn-native-lab-tip-start at
d9ddc556e742514eb47e7240fbd19afc49ac5685 and rh-main at
27a4271f208247a1e9c24cca35468c298b6cd29d. Cause: the origin tips moved
after the executor's merge snapshot and no fetch is performed by this
worker, so those commit objects are not available locally to test
(git cat-file: could not get object info). This is a coverage gap, not
a toolchain regression. Scope stamp: this battery certifies toolchain
and extraction stability only, not the contents of the merged commits.

## SPOT_RE_RUN (agenda item 1, run first)

Re-ran three 1721pdt entries with this wave's parser (sed extraction of
b2_bin_a_sha256; never cut -d= -f2, since the harness prints all B2
key/value pairs on one line), to confirm the 1721pdt verdicts before
anyone cites them.

- (a) live entry, local tnn-native-lab at the 2021pdt task-pinned HEAD
  fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91: harness exit 0,
  VERDICT=PASS, znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  probe sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
  b2_bin_a sha256 =
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
  b1 run sha256 =
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066,
  NEG1 E0002 hit (driver compile exit 1, check exit 1), NEG2 stdout
  "WRONG OUTPUT" differing from expected at char 1 ("F" vs "W"), probe
  build exit 0, probe run exit 0, probe stdout R32_ZNC_PROBE_OK.
  Verdict: PASS. 1721pdt PASS confirmed.
- (b) fixture entry, wt-forktest-tnn-native-lab at
  bd30978748fa83bbea6e423a7074cf32b7304291: same evidence values as
  (a), harness exit 0, VERDICT=PASS. Verdict: PASS. 1721pdt PASS
  confirmed.
- (c) extraction-FAIL entry, origin pull/1/head at
  5802fec8401f28b4036b0dd5ebb23905610cab57: znc extraction failed with
  "fatal: path 'src/tools/toolchain/znc_linux_x86_64_abed8aa1' exists on
  disk, but not in '5802fec8401f28b4036b0dd5ebb23905610cab57'",
  recorded verdict EXTRACTION_FAIL. Verdict: extraction FAIL. 1721pdt
  extraction FAIL confirmed, identical cause.

All three 1721pdt verdicts are confirmed. This wave's driver parses with
sed from the start. Spot evidence lives in the P14 archive as
spot-2021-live-local, spot-2021-fixture-wt, and spot-2021-fail-pull1.

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
VERDICT=PASS on 36/36 tested battery entries (plus 2/2 spot entries),
VERDICT=FAIL on 0.

The shell driver run_one.sh is a faithful port of the frozen 2321pdt
driver (identical test sources, identical znc flags, identical expected
output): it extracts the znc and probe read only, records their shas,
verifies both against the pins, runs the rebuilt harness, extracts the
B2 bin sha with sed, confirms NEG1 fails with E0002 reported by the
fork's own znc stderr, confirms NEG2 stdout differs from expected at
char 1 (run stdout "WRONG OUTPUT" vs expected "FORKBATTERY-OK 42"),
compiles the tree probe with the fork's own znc and runs it expecting
R32_ZNC_PROBE_OK, then deletes the per-entry znc copy. Correct
invocations honored: znc prints its status line on stdout (the frozen
harness output captures it; the driver's orchestrator checks never parse
program output out of a compiler status line), and strict checking uses
the frozen flag order `znc check file.zag --strict --no-zagd` (the
harness is the frozen byte-identical artifact; the task's alternate
order note is recorded here but the frozen order is what ran).

## Enumeration (fresh, this wave)

`git branch` fresh at run start: 20 local branches. `git branch -r`:
one remote-tracking ref (origin/tnn-native-lab, value
75267f9df70702fcd473619c70a454b191d21a9c at run start; no fetch was
performed by this worker, so it was untouched by this run). Read-only
`git ls-remote origin` at run start: HEAD plus 6 refs/heads plus 3
refs/pull/*/head refs. In addition, the 10 detached worktrees under
~/workspace/tnn-rsi-wave3/ were enumerated via `git worktree list`
(SHAs re-verified per worktree, all unchanged since 1721pdt).

Local branches (20): tnn-native-lab (task-pinned run-start HEAD
fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91), the 18 archive branches at
the SHAs below (all unchanged since 1721pdt except the newly enumerated
tnn-native-lab-wave-archive-wave-20260926-1721pdt at
a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a):
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
a222f8f178049b9aeee3b053328c59e9b6fd813d,
tnn-native-lab-wave-archive-wave-20260926-1721pdt at
a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a (newly enumerated this wave),
and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote heads (read-only ls-remote at run start): fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5 (unchanged), main at
27a4271f208247a1e9c24cca35468c298b6cd29d (moved since 1721pdt, whose
tip was 0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185), r2-7 at
2d99d183f693145c53213639990a3474ff786b69 (unchanged),
reorg/phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df
(unchanged), tnn-native-lab at
d9ddc556e742514eb47e7240fbd19afc49ac5685 (moved; the executor's merge
snapshot pinned 75267f9df70702fcd473619c70a454b191d21a9c, which is the
local remote-tracking value this wave), wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848 (unchanged), pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 (unchanged), pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (unchanged), pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df (unchanged).

Worktrees (10, SHAs re-verified, all unchanged since 1721pdt):
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
complete (0 znc.bin files remain in the evidence tree).

## Live vs fixture split

Rule used (same as prior waves): Live = entry whose HEAD moved since
last wave, or newly enumerated this wave. Fixture = unchanged-SHA
entries tested for coverage.

Named entries total: 40. Live: 5. Fixture: 35.
Unique commits: 33. Unique live commits: 5.

Live: local-tnn-native-lab (45d449a56 to fe1b5e2c0 at run start),
arch-wave-20260926-1721pdt (newly enumerated this wave, at
a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a; this commit is also the first
parent of the run-start merge, recorded as the executor's pre-merge
state), origin-tnn-native-lab-rt (39bf8d5d to 75267f9df at run start;
the 75267f9df state is merged into the task-pinned HEAD and tested by
this entry), rh-main (0ab8ed6b to 27a4271f at run start; the new commit
is absent locally, entry untestable this wave, extraction FAIL),
rh-tnn-native-lab-tip-start (run-start ls-remote tip d9ddc556, a
distinct commit from the remote-tracking 75267f9df; the new commit is
absent locally, entry untestable this wave, extraction FAIL).

Fixture: the 17 older archive branches, wave-debate-session-1-backup,
fs-gr1, r2-7, reorg/phase-0-1, wg-freeze, pull/1/head, pull/2/head,
pull/3/head, the 7 forktest worktrees, and the 3 wave3 worktrees
(all unchanged SHAs).

All duplicates named explicitly with SHAs (P8):
- origin-tnn-native-lab-rt tests the same commit merged into the
  task-pinned HEAD's second parent:
  75267f9df70702fcd473619c70a454b191d21a9c.
- rh-reorg-phase-0-1, rh-pull-3-head, and wt-forktest-reorg each test
  the same commit: 9914322267e1358e5542a23c72ec51d1a9ae43df.
- wave-debate-session-1-backup tests the same commit as
  wt-forktest-debate-backup: 3947dca1a77c00818575dbc7476556c8278b8b7b.
- rh-wg-freeze tests the same commit as wt-forktest-wg-freeze:
  f875b34179f570ba1ad555262cd401ddc4a52848.
- wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, and
  wt-wave3-trades each test the same commit:
  bd30978748fa83bbea6e423a7074cf32b7304291.
- Spot entries duplicate battery entries: spot-2021-live-local
  duplicates local-tnn-native-lab (fe1b5e2c0),
  spot-2021-fixture-wt duplicates wt-forktest-tnn-native-lab
  (bd3097874), spot-2021-fail-pull1 duplicates rh-pull-1-head
  (5802fec8).

## Verdicts (entry, commit, PASS/FAIL, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| local-tnn-native-lab (task-pinned run-start HEAD) | fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91 | PASS | live |
| arch-20260926-1721pdt (tnn-native-lab-wave-archive-wave-20260926-1721pdt) | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a | PASS | live; newly enumerated |
| origin-tnn-native-lab-rt (remote-tracking, run-start value) | 75267f9df70702fcd473619c70a454b191d21a9c | PASS | live |
| rh-tnn-native-lab-tip-start (run-start ls-remote tip) | d9ddc556e742514eb47e7240fbd19afc49ac5685 | FAIL | live; extraction failure: commit absent locally, no fetch performed |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | FAIL | live; extraction failure: commit absent locally, no fetch performed |
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
| arch-wave-20260926-1421pdt | a222f8f178049b9aeee3b053328c59e9b6fd813d | PASS | fixture |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| rh-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
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

Nothing broke on any toolchain-bearing entry. The four FAILs are
extraction failures (see Failure analysis).

## Uniform battery evidence (all 38 PASS runs: 36 battery plus 2 spot)

Verified across all 38 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (38/38; byte-identical toolchain on every tested fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (38/38).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (38/38); run sha256
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066.
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 38 (matches the frozen value; parsed with sed, never cut).
- B3: strict check exit 0 (38/38).
- NEG1: fails as required on 38/38: driver compile exit 1, check exit 1,
  and the fork's own znc reports E0002 on the neg1 source on all 38.
- NEG2: fails as required on 38/38: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1 ("F" vs "W").
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 38/38.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 38/38 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Failure analysis

Two kinds of extraction failure this wave.

pull/1/head and pull/2/head: extraction failures at the first step,
identical to the 1721pdt, 1421pdt, 1121pdt, 0821pdt, and 0521pdt waves:
`git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1` fails
("exists on disk, but not in '<commit>'" in both cases). The probe path
`src/tools/toolchain/znc_probe.zag` is likewise absent in both trees.
Their tree roots hold non-TNN research documents; they carry no src/
directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

rh-tnn-native-lab-tip-start (d9ddc556) and rh-main (27a4271f): the
commit objects are absent from the local object store (git cat-file
reports "could not get object info" for both). The origin tips moved
after the executor's merge snapshot (75267f9df was the
origin/tnn-native-lab tip when the task-pinned merge was built, and
that state was tested: it is merged into fe1b5e2c0 and tested by both
the local-tnn-native-lab entry and the origin-tnn-native-lab-rt entry).
No fetch is performed by this worker under the frozen procedure, so the
new tips could not be extracted and could not be tested. This is a
coverage gap, not a toolchain regression. Recommendation: the next
wave should fetch before enumeration, or the coordinator should make
the new tip commits available locally; until then these two entries
are untestable, not failing.

## P19 coverage-delta accounting vs 1721pdt

1721pdt reported 39 named entries, 37 PASS / 2 extraction FAIL, 31
unique commits, 4 live entries / 3 unique live commits.
This wave reports 40 named entries, 36 PASS / 4 extraction FAIL, 33
unique commits, 5 live entries / 5 unique live commits.

- Named entries 39 to 40: the cause is one newly enumerated local
  branch, tnn-native-lab-wave-archive-wave-20260926-1721pdt, at
  a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a. The origin tip split (the
  remote-tracking origin/tnn-native-lab at 75267f9df versus the live
  run-start tip at d9ddc556) changed which commits the two existing
  entry names test, but it did not change the named entry count.
- Live entries 4 to 5: +1 for the newly enumerated archive branch
  (newly enumerated counts as live); +1 for rh-main, whose commit moved
  from 0ab8ed6b to 27a4271f since 1721pdt (moved counts as live, even
  though its commit is untestable this wave); -1 for
  arch-wave-20260926-1421pdt (a222f8f178), which was live in 1721pdt as
  newly enumerated and is a fixture this wave. Net change +1.
- Extraction FAILs 2 to 4: the two expected pull-head FAILs persist
  unchanged; the two new ones are rh-main and
  rh-tnn-native-lab-tip-start, whose commits are absent locally (no
  fetch), not toolchain failures.
- Unique commits 31 to 33: +5 new (fe1b5e2c0, a4d4ff7c, 75267f9df,
  27a4271f, d9ddc556) minus 3 no longer tested (45d449a56, 39bf8d5d,
  0ab8ed6b).

## Incidents

- Driver invocation bug, caught before any result was cited: the first
  parallel batch call passed name and ref as one whitespace-split token
  stream, so jobs ran with the ref empty and git would have resolved
  the extraction against the working tree instead of the entry's commit.
  Every bogus evidence dir was deleted (0 survive), the batch was
  re-run with correct name/ref pairs, and all 43 surviving evidence
  dirs were verified against the corrected run log. No bogus data is
  cited anywhere in this report.
- No fetch was performed by this worker, so no remote-tracking ref
  moved under this run. Local HEAD did not move during this run
  (fe1b5e2c0 at start and at close). The wave lock was not touched.

## Scratch space

/tmp free at run start: 512M of 512M (0 percent used). /tmp/fb2021 at
run end: 13M total (8.0M pinned znc copy used for harness builds, the
rebuilt harness binary, and per-entry evidence staging for 43 entry
runs: 40 battery plus 3 spot). Per-entry znc copies were deleted right
after each entry's evidence was complete (0 znc.bin files remain), so at
most 8 such copies were resident at a time and /tmp stayed near 13M
throughout. No /tmp incident this wave.

## Closing tip re-check

Run-start origin tips (read-only `git ls-remote origin`): tnn-native-lab
d9ddc556e742514eb47e7240fbd19afc49ac5685, main
27a4271f208247a1e9c24cca35468c298b6cd29d.
Closing origin tips (read-only `git ls-remote origin`): identical values.

The tips did not move during this run. Note: the run-start tip
d9ddc556 differs from the tip the executor merged (75267f9df); the
merged 75267f9df state was tested by this battery via the task-pinned
run-start HEAD and the origin-tnn-native-lab-rt entry. The live d9ddc556
tip and the live main tip 27a4271f were not tested this wave because
their commits are absent locally. Nothing arrived after the testing
window. No fetch was performed to chase anything.

## Local HEAD

Task-pinned run-start HEAD:
fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91.
HEAD at run end: fe1b5e2c09c4450fc9fdff12e3527d8cd05f3c91. Local HEAD
did not move during this run. The tested local entry is the task-pinned
run-start HEAD. This worker's only repo write is this file; it touched
no other tracked files and made no commits.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git (read-only
rev-parse, branch, ls-remote, show, worktree list, cat-file, log; no
fetch, no checkout, no pull, no push), sha256sum, grep, sed, awk, tr,
cmp, xargs, head, the pinned znc binary, and the rebuilt pure-Zag
harness fork_battery. No Python was used for the battery, the harness
build, extraction, any analysis, or any verification step.

## Evidence archive note (P14)

The 43 per-entry evidence dirs (40 battery plus 3 spot) were moved (not
copied) from /tmp/fb2021/E into
docs/lab/rsi/runs/wave-20260926-2021pdt/forks/evidence/. Each dir holds
RESULT.txt, zag_harness.out, znc.path, tree_probe.zag, forkbat_hello.zag,
neg1.zag, neg2.zag, probe_build.log, probe_run.out, neg1c/neg1k logs,
neg2_run.out, expected.out, bin_a, bin_b, hello_bin, neg2_bin, probe_bin,
extract.err, and harness.err as applicable; no per-entry znc.bin by
design. S9 note: the frozen harness output (zag_harness.out) embeds the
pinned znc binary's own stdout status line, which uses the compiler's
own punctuation; that is captured instrument output of the frozen
toolchain, not wave documentation, and travels as a disclosed caveat
unedited.
