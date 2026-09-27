# Fork battery results, wave-20260926-2321pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
377c36fd9565ba7451a608eb0e8dd0c2362de9f1 (merge of
5ba241235482610f1c8f538d97ca0462164b4014, the executor's pre-merge
state, and 3ac39fc14a7255469b27f4b12b5d3be7491b0f0b, the
origin/tnn-native-lab tip at merge time; the merged upstream contents
are treated as CLOSED, not re-litigated: content not reviewed,
toolchain stability only). Read-only git operations throughout. A git
fetch origin was run by the coordinator before this wave; this worker
ran no fetch itself. Scratch: /tmp/fb2321 (fresh this wave; /tmp is a
512M tmpfs, 505M free at run start). The wave lock was not touched.

## Verdict

41 named battery entries. 38 PASS, 2 extraction FAIL, 1 CONFIRM under
P20 scope stamp. 34 unique commits. 4 live entries, 4 unique live
commits; 37 fixture entries.

The two extraction FAILs are the expected ones: rh-pull-1-head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and rh-pull-2-head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (both trees lack the pinned
toolchain path, identical cause six waves running; non-TNN
research-doc repos, still uncovered by this battery). The CONFIRM is
rh-main at 27a4271f208247a1e9c24cca35468c298b6cd29d: the commit
object is still absent from the local object store after the pre-wave
fetch (git cat-file -e fails), so no znc could be extracted and no
battery check ran. Per P20 this is recorded as a coverage gap, NOT a
failure, under the explicit scope stamp quoted in the verdicts table.
The previously untestable rh-tnn-native-lab-tip-start at
d9ddc556e742514eb47e7240fbd19afc49ac5685 is testable this wave: its
commit object arrived with the pre-wave fetch, and it passes the full
battery. Scope stamp: this battery certifies toolchain and extraction
stability only, not the contents of the merged commits.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
local branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the expected value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc extracted read only from the run-start
HEAD (src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to prior waves; harness build is deterministic).
The harness ran per entry with cwd = entry scratch dir and ./znc.path
naming that entry's own extracted znc copy. Harness exit 0 with
VERDICT=PASS on 38/38 tested battery entries, VERDICT=FAIL on 0.

The shell driver run_one.sh is a faithful reuse of the frozen 2321pdt
driver approach (identical test sources, identical znc flags,
identical expected output): it extracts the znc and probe read only,
records their shas, verifies both against the pins, runs the rebuilt
harness, extracts the B2 bin sha by tokenizing the harness output
first (the frozen output prints all B2 key/value pairs on one line,
so no field is ever split on '='), confirms NEG1 fails with E0002
reported by the fork's own znc stderr, confirms NEG2 stdout differs
from expected at char 1 (run stdout "WRONG OUTPUT" vs expected
"FORKBATTERY-OK 42"), compiles the tree probe with the fork's own znc
and runs it expecting R32_ZNC_PROBE_OK, then deletes the per-entry
znc copy. Correct invocations honored: znc prints its status line on
stdout (the frozen harness output captures it; the driver's
orchestrator checks never parse program output out of a compiler
status line), and strict checking uses the frozen flag order `znc
check file.zag --strict --no-zagd`.

## Enumeration (fresh, this wave)

`git branch` fresh at run start: 21 local branches (one more than
2021pdt). `git for-each-ref refs/remotes`: one remote-tracking ref,
origin/tnn-native-lab at 3ac39fc14a7255469b27f4b12b5d3be7491b0f0b
(the pre-wave fetch moved it from 75267f9df; this worker ran no
fetch). The local fetch refspec is
`+refs/heads/tnn-native-lab:refs/remotes/origin/tnn-native-lab`, so
after the pre-wave fetch there are NO rh-* or pull/* remote-tracking
refs present locally; that is the recorded state, not an assumption.
Remote heads were enumerated read-only via `git ls-remote origin` at
run start (HEAD plus 6 refs/heads plus 3 refs/pull/*/head refs), same
as prior waves. The 10 detached worktrees under
~/workspace/tnn-rsi-wave3/ were enumerated via `git worktree list`
(SHAs re-verified per worktree, all unchanged since 2021pdt, no stale
or new worktrees).

Local branches (21): tnn-native-lab (task-pinned run-start HEAD
377c36fd9565ba7451a608eb0e8dd0c2362de9f1), the 19 archive branches at
the SHAs below (all unchanged since 2021pdt except the newly
enumerated tnn-native-lab-wave-archive-20260926-2021pdt at
5ba241235482610f1c8f538d97ca0462164b4014, which is also the first
parent of the run-start merge, i.e. the executor's pre-merge state):
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
tnn-native-lab-wave-archive-20260926-2021pdt at
5ba241235482610f1c8f538d97ca0462164b4014 (newly enumerated this wave),
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
a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a,
and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote heads (read-only ls-remote at run start): fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5 (unchanged), main at
27a4271f208247a1e9c24cca35468c298b6cd29d (unchanged since 2021pdt;
commit object still absent locally), r2-7 at
2d99d183f693145c53213639990a3474ff786b69 (unchanged),
reorg/phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df
(unchanged), tnn-native-lab at
3ac39fc14a7255469b27f4b12b5d3be7491b0f0b (moved since 2021pdt, whose
tip was d9ddc556e742514eb47e7240fbd19afc49ac5685), wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848 (unchanged), pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 (unchanged), pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (unchanged), pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df (unchanged).

Worktrees (10, SHAs re-verified, all unchanged since 2021pdt):
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
extracted copies were chmod +x in scratch only. The two failed
`git show` redirects left 0-byte znc.bin files in the pull-head
evidence dirs; both were deleted before archiving, so no per-entry
znc.bin survives anywhere in the evidence tree (0 znc.bin files).

## Live vs fixture split

Rule used (same as prior waves): Live = entry whose HEAD moved since
last wave, or newly enumerated this wave, or newly testable this
wave. Fixture = unchanged-SHA entries tested for coverage.

Named entries total: 41. Live: 4. Fixture: 37.
Unique commits: 34. Unique live commits: 4.

Live: local-tnn-native-lab (fe1b5e2c0 to 377c36fd9 at run start),
arch-20260926-2021pdt (newly enumerated this wave, at
5ba241235482610f1c8f538d97ca0462164b4014; this commit is also the
first parent of the run-start merge, recorded as the executor's
pre-merge state), origin-tnn-native-lab-rt (75267f9df to 3ac39fc14 at
run start; the 3ac39fc14 state is merged into the task-pinned HEAD and
tested by this entry), rh-tnn-native-lab-tip-start (d9ddc556,
untestable in 2021pdt, newly testable this wave: the pre-wave fetch
brought its commit object into the local store; the live remote tip
has since moved to 3ac39fc14, which is tested by
origin-tnn-native-lab-rt).

Fixture: the 18 older archive branches, wave-debate-session-1-backup,
rh-main (unchanged SHA since 2021pdt; still untestable, now CONFIRM
under P20 scope stamp), rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1,
rh-wg-freeze, rh-pull-1-head, rh-pull-2-head, rh-pull-3-head, the 7
forktest worktrees, and the 3 wave3 worktrees (all unchanged SHAs).

All duplicates named explicitly with SHAs (P8):
- arch-20260926-2021pdt tests the same commit as the run-start merge's
  first parent (the executor's pre-merge state):
  5ba241235482610f1c8f538d97ca0462164b4014.
- origin-tnn-native-lab-rt tests the same commit as the run-start
  merge's second parent (the merged upstream state, CLOSED content):
  3ac39fc14a7255469b27f4b12b5d3be7491b0f0b.
- rh-reorg-phase-0-1, rh-pull-3-head, and wt-forktest-reorg each test
  the same commit: 9914322267e1358e5542a23c72ec51d1a9ae43df.
- wave-debate-session-1-backup tests the same commit as
  wt-forktest-debate-backup: 3947dca1a77c00818575dbc7476556c8278b8b7b.
- rh-wg-freeze tests the same commit as wt-forktest-wg-freeze:
  f875b34179f570ba1ad555262cd401ddc4a52848.
- wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, and
  wt-wave3-trades each test the same commit:
  bd30978748fa83bbea6e423a7074cf32b7304291.

## Verdicts (entry, commit, PASS/FAIL/CONFIRM, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| local-tnn-native-lab (task-pinned run-start HEAD) | 377c36fd9565ba7451a608eb0e8dd0c2362de9f1 | PASS | live |
| arch-20260926-2021pdt (tnn-native-lab-wave-archive-20260926-2021pdt) | 5ba241235482610f1c8f538d97ca0462164b4014 | PASS | live; newly enumerated |
| origin-tnn-native-lab-rt (remote-tracking, run-start value) | 3ac39fc14a7255469b27f4b12b5d3be7491b0f0b | PASS | live |
| rh-tnn-native-lab-tip-start (superseded remote tip, queued item) | d9ddc556e742514eb47e7240fbd19afc49ac5685 | PASS | live; newly testable after pre-wave fetch |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | CONFIRM | P20 scope stamp: enumerated-but-untestable; commit object absent locally (git cat-file -e exit 1); coverage gap, NOT a failure |
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
| arch-wave-20260926-1721pdt | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a | PASS | fixture |
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

Nothing broke on any toolchain-bearing entry. The two FAILs are
extraction failures (see Failure analysis). The one CONFIRM is the
P20 coverage gap.

## Uniform battery evidence (all 38 PASS runs)

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
  on all 38 (matches the frozen value; parsed by tokenizing the
  harness output, never by splitting a packed line on '=').
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

pull/1/head and pull/2/head: extraction failures at the first step,
identical to the 2021pdt, 1721pdt, 1421pdt, 1121pdt, 0821pdt, and 0521pdt
waves: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails ("exists on disk, but not in '<commit>'" in both cases). The probe
path `src/tools/toolchain/znc_probe.zag` is likewise absent in both
trees. Their tree roots hold non-TNN research documents; they carry no
src/ directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

rh-main (27a4271f): the commit object is absent from the local object
store (git cat-file -e fails with exit 1; git show exits 128). The
pre-wave fetch refspec covers only refs/heads/tnn-native-lab, so the
main tip's objects were not fetched, and no rh-* or pull/*
remote-tracking refs exist locally (recorded as the state after the
pre-wave fetch, not an assumption). No znc could be extracted, so no
battery check ran. Per P20 this entry is CONFIRM under the explicit
scope stamp quoted in its RESULT.txt and in the verdicts table: a
coverage gap, NOT a toolchain failure and NOT a toolchain pass.

rh-tnn-native-lab-tip-start (d9ddc556): RESOLVED this wave. The
commit object arrived with the pre-wave fetch (git cat-file -t reports
commit), the pinned znc extracted cleanly with the pin verified, and
the full battery passes (38/38 uniform evidence). The queued
improvement is done for this entry.

## P19 coverage-delta accounting vs 2021pdt

2021pdt reported 40 named entries, 36 PASS / 4 extraction FAIL, 33
unique commits, 5 live entries / 5 unique live commits, 35 fixtures.
This wave reports 41 named entries, 38 PASS / 2 extraction FAIL / 1
CONFIRM, 34 unique commits, 4 live entries / 4 unique live commits, 37
fixtures.

- Named entries 40 to 41: the cause is one newly enumerated local
  branch, tnn-native-lab-wave-archive-20260926-2021pdt, at
  5ba241235482610f1c8f538d97ca0462164b4014.
- Live entries 5 to 4: +1 for the newly enumerated archive branch
  (newly enumerated counts as live); -1 for
  arch-wave-20260926-1721pdt (a4d4ff7cd), which was live in 2021pdt as
  newly enumerated and is a fixture this wave; -1 for rh-main
  (27a4271f), whose SHA did not move since 2021pdt and is therefore a
  fixture this wave (still untestable, now CONFIRM under P20). Net
  change -1.
- Extraction FAILs 4 to 2: the two expected pull-head FAILs persist
  unchanged; rh-tnn-native-lab-tip-start (d9ddc556) is now testable and
  passes; rh-main moves from extraction FAIL to P20 CONFIRM (coverage
  gap, not a failure).
- Unique commits 33 to 34: +3 new (377c36fd9, 5ba241235, 3ac39fc14)
  minus 2 no longer tested (fe1b5e2c0, 75267f9df).

## Incidents

- Driver parser bug, caught in the single-entry dry run before the
  batch: the B3 PASS/FAIL token is not at a line start in the frozen
  harness output (it follows the b3_check_stdout bracket text), so the
  start-anchored parse read B3 empty and the dry-run verdict was FAIL
  on a passing entry. The parser was fixed to tokenize the harness
  output on whitespace before extracting KEY=VALUE tokens (no packed
  line is ever split on '='), the bogus dry-run evidence dir and run
  log were deleted (0 survive), the full 40-entry batch was rerun, and
  all 40 batch evidence dirs were verified against the entry list and
  the corrected run log (entry=, commit=, and verdict= all match). Per
  P21 this does not void the battery verdict. The rh-main CONFIRM dir
  was written separately with its explicit scope stamp.
- No fetch was performed by this worker, so no remote-tracking ref
  moved under this run. Local HEAD did not move during this run
  (377c36fd9 at start and at close). The wave lock was not touched.

## Scratch space

/tmp free at run start: 505M of 512M (2 percent used). /tmp/fb2321 at
run end: 8.4M total (8.0M pinned znc copy used for harness builds, the
rebuilt harness binary, harness source, driver, entry list, and run
log). Per-entry znc copies were deleted right after each entry's
evidence was complete (0 znc.bin files remain in the evidence tree),
so at most 8 such copies were resident at a time. No /tmp incident
this wave.

## Closing tip re-check

Run-start origin tips (read-only `git ls-remote origin`): tnn-native-lab
3ac39fc14a7255469b27f4b12b5d3be7491b0f0b, main
27a4271f208247a1e9c24cca35468c298b6cd29d.
Closing origin tips (read-only `git ls-remote origin`): identical values.

The tips did not move during this run. The run-start tip 3ac39fc14
equals the tip the executor merged (the merge's second parent); that
state was tested by this battery via the task-pinned run-start HEAD
and the origin-tnn-native-lab-rt entry. The live main tip 27a4271f is
CONFIRM under the P20 scope stamp (coverage gap). Nothing arrived
after the testing window. No fetch was performed to chase anything.

## Local HEAD

Task-pinned run-start HEAD:
377c36fd9565ba7451a608eb0e8dd0c2362de9f1.
HEAD at run end: 377c36fd9565ba7451a608eb0e8dd0c2362de9f1. Local HEAD
did not move during this run. The tested local entry is the task-pinned
run-start HEAD. This worker wrote only new files (this report plus the
41 per-entry evidence dirs); it modified no tracked files, made no
commits, and pushed nothing.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git
(read-only rev-parse, branch, for-each-ref, ls-remote, show, worktree
list, cat-file, log, config; no fetch, no checkout, no pull, no push),
sha256sum, grep, sed, awk, tr, cmp, xargs, head, the pinned znc
binary, and the rebuilt pure-Zag harness fork_battery. No Python was
used for the battery, the harness build, extraction, any analysis, or
any verification step.

## Evidence archive note (P14)

The 41 per-entry evidence dirs were moved (not copied) from
/tmp/fb2321/E into
docs/lab/rsi/runs/wave-20260926-2321pdt/forks/evidence/. Each PASS dir
holds RESULT.txt, zag_harness.out, harness.err, znc.path,
tree_probe.zag, forkbat_hello.zag, neg1.zag, neg2.zag, probe_build.log,
probe_run.out, neg1c.out, neg1c.err, neg1k.out, neg1k.err,
neg2_run.out, expected.out, bin_a, bin_b, hello_bin, neg2_bin,
probe_bin, and extract.err; the FAIL and CONFIRM dirs hold RESULT.txt
and extract.err only; no per-entry znc.bin by design. S9 note: the
frozen harness output (zag_harness.out) embeds the pinned znc binary's
own stdout status line, which uses the compiler's own punctuation;
that is captured instrument output of the frozen toolchain, not wave
documentation, and travels as a disclosed caveat unedited.
