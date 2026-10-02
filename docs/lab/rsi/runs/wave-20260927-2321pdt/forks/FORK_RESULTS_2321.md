# Fork battery results, wave-20260927-2321pdt

Fork-battery worker (lane 2). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, task-pinned run-start HEAD
baf48e4744c3c075e3fc70a383f0a77efec83ad7. Read-only git operations
throughout (rev-parse, for-each-ref, ls-remote, show, worktree list,
log, ls-tree; no checkout, no pull, no push, no fetch, no reset).
Scratch: ~/workspace/fb2321 (fresh this wave). The wave lock was not
touched.

## Verdict

56 named battery entries. 54 PASS, 0 FAIL, 2 UNTESTABLE, 0 CONFIRM.
2 live entries; 54 fixture entries.

No new FAIL. The 1721pdt probe-loss FAIL stays closed: the
toolchain-dir repair (37d1d3cab) is an ancestor of the task-pinned HEAD
baf48e474; znc_probe.zag and the znc binary are present in the tree,
the probe compiles and runs with the pinned znc (expect
R32_ZNC_PROBE_OK met), and the local-tnn-native-lab entry PASSES the
full frozen battery at the new commit.

The two UNTESTABLEs are the expected pull-head entries
rh-pull-1-head and rh-pull-2-head (identical cause fourteen waves
running: non-TNN research-doc trees, pinned toolchain path absent).
No result was faked. Scope stamp: this battery certifies toolchain
and extraction stability only, not the contents of the tested
commits.

UNTESTABLE caveat: the two UNTESTABLEs are content-dependent (their
trees lack the toolchain path), not toolchain regressions; the counts
above are never headlined without this caveat.

## Harness rebuild with provenance

The pure-Zag harness fork_battery.zag was extracted read only from
local branch tnn-native-lab-wave-archive-20260923-2321pdt at
docs/lab/rsi/runs/wave-20260923-2321pdt/fork-battery/fork_battery.zag.
Extracted sha256:
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738
(matches the frozen value; no source-extraction anomaly this wave).
Rebuilt with the pinned znc extracted read only from the run-start
HEAD (src/tools/toolchain/znc_linux_x86_64_abed8aa1; sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified BEFORE use; build command: ./znc_build fork_battery.zag
--no-zagd --no-analyze --no-foreground-cache -o fork_battery). Built
binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to wave-20260927-1721pdt's rebuild; harness build is
deterministic). The harness ran per entry with cwd = entry scratch dir
and ./znc.path naming that entry's own extracted znc copy. Harness
exit 0 with VERDICT=PASS on 54/54 tested battery entries,
VERDICT=FAIL on 0.

The shell driver run_one.sh is a faithful rebuild of the frozen 2321pdt
driver approach plus the 0821pdt orchestration layer (identical test
sources, identical znc flags, identical expected output): it extracts
the znc and probe read only, records their shas, verifies both against
the pins, runs the rebuilt harness, extracts the B2 bin sha by
tokenizing the harness output on whitespace first (no packed line is
ever split on '='), confirms NEG1 fails with E0002 reported by the
fork's own znc stderr, confirms NEG2 stdout differs from expected at
char 1 (run stdout "WRONG OUTPUT" vs expected "FORKBATTERY-OK 42"),
compiles the tree probe with the fork's own znc and runs it expecting
R32_ZNC_PROBE_OK, then deletes the per-entry znc copy. Correct
invocations honored: znc prints its status line on stdout (the frozen
harness output captures it inside b3_check_stdout; the driver's
orchestrator checks never parse program output out of a compiler
status line), and strict checking uses the frozen flag order
`znc check file.zag --strict --no-zagd`.

## Enumeration (fresh, this wave)

`git for-each-ref` fresh at run start: 32 local branches, 6 local
remote-tracking refs (no fetch was run this wave; remote state came
from read-only `git ls-remote origin`). Remote heads were enumerated
read-only via `git ls-remote origin` at run start (HEAD plus 6
refs/heads plus 3 refs/pull/*/head refs): all identical to the 2021pdt
close values (fs-gr1 23f6c0f9, main 27a4271f, r2-7 2d99d183,
reorg/phase-0-1 991432226, tnn-native-lab bedf8b4a, wg-freeze f875b341,
pull/1/head 5802fec8, pull/2/head 4b76bb59, pull/3/head 991432226).
The 13 worktrees were enumerated via `git worktree list` (SHAs
re-verified per worktree; all unchanged since 2021pdt). A single-entry
dry run (arch-20260923-2321pdt) passed clean before the batch and its
RESULT body is byte-identical to the 2021pdt evidence for that entry;
its evidence dir was deleted before the batch (no bogus dirs kept,
none deleted mid-batch). The frozen enumeration manifest
ENUMERATION_MANIFEST.md in this run dir lists every named entry, its
ref, commit sha, and live/fixture classification.

Local branches (32): tnn-native-lab (task-pinned run-start HEAD
baf48e474), 10 plain archive branches, 17 wave-prefixed archive
branches (including the newly enumerated
tnn-native-lab-wave-archive-wave-20260927-2021pdt at baf48e474), the 3
experimental worker branches wave-20260927-0221pdt-exp1,
wave-20260927-0221pdt-exp2, and wave-20260927-0221pdt-sensory (tips
unchanged since 2021pdt; each tested read-only at its pinned commit
via git show, toolchain stability only), and
wave-debate-session-1-backup at 3947dca1a77c00818575dbc7476556c8278b8b7b
(unchanged). No branch known from the 2021pdt baseline is missing;
the only change is the one new archive branch.

Remote heads (read-only ls-remote at run start, identical at close):
all 9 heads unchanged since 2021pdt close. The local remote-tracking
ref origin/tnn-native-lab stayed at bedf8b4a, still agreeing with the
live tip.

Worktrees (13, SHAs re-verified): the main worktree at baf48e474
(the task-pinned run-start HEAD; see Incidents for the mid-run move);
the 10 forktest/wave3 worktrees unchanged since 2021pdt
(forktest/main at 293602fb1d4a2fd5d680a3376463d61b0572006b,
forktest/r2-7 at a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
forktest/reorg_phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df,
forktest/tnn-native-lab at bd30978748fa83bbea6e423a7074cf32b7304291,
forktest/tnn-native-lab-remote at
cea8db22f53ed1294aff5324aa143bd6d1df845e,
forktest/wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b, forktest/wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, and wave3 probe/senses/trades
all at bd30978748fa83bbea6e423a7074cf32b7304291); the 3 exp worktrees
wt-exp1, wt-exp2, wt-sensory unchanged at 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d,
a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4, and
c368b8e1ffecec2f9061011f5d7c0e3e68675e0a, each tested at its pinned
commit read-only.

Extraction method: every entry extracted the pinned znc and probe via
read-only `git show <commit>:src/tools/toolchain/...` into scratch;
extracted copies were chmod +x in scratch only. The two UNTESTABLE
`git show` redirects left 0-byte znc.bin files; both were deleted
before archiving, so no per-entry znc.bin survives anywhere in the
evidence tree (0 znc.bin files).

## Live vs fixture split

Rule used (same as prior waves): Live = entry whose HEAD moved since
last wave, or newly enumerated this wave, or newly testable this
wave. Fixture = unchanged-SHA entries tested for coverage.

Named entries total: 56. Live: 2. Fixture: 54.

Live: arch-wave-20260927-2021pdt (newly enumerated at
baf48e4744c3c075e3fc70a383f0a77efec83ad7; the new branch was included
first in the test order, before any other entry, and tested at its
pinned commit), local-tnn-native-lab (fc1a43b8c to baf48e474 at run
start; the task-pinned HEAD; PASS; toolchain-dir repair still intact).

Fixture: the 25 older archive branches (unchanged SHAs), the 3 exp
branches and their 3 worktrees (unchanged SHAs since 2021pdt; tested
at their pinned commits, toolchain stability only),
wave-debate-session-1-backup, rh-tnn-native-lab-live-tip
(superseded tip, see note), rh-main (unchanged; P20 gap stays closed),
rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1, rh-wg-freeze, rh-pull-1-head,
rh-pull-2-head, rh-pull-3-head, origin-tnn-native-lab-rt and
origin-tnn-native-lab-live (unchanged at bedf8b4a; fixture-ized this
wave), arch-wave-20260927-1721pdt (was live at 2021pdt), the 7
forktest worktrees, and the 3 wave3 worktrees.

All duplicates named explicitly with SHAs (P8):
- arch-wave-20260927-2021pdt and local-tnn-native-lab each test the
  same commit: baf48e4744c3c075e3fc70a383f0a77efec83ad7.
- exp1 and wt-exp1 each test the same commit:
  1010a63c3c1cc3f3724f6cf0ca55decc08207a2d (pinned; workers may be
  implementing in these branches concurrently, so mid-run tip movement
  cannot have affected the results; tips were also unchanged between
  run start and close).
- exp2 and wt-exp2 each test the same commit:
  a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 (same pinned-commit caveat).
- exp-sensory and wt-exp-sensory each test the same commit:
  c368b8e1ffecec2f9061011f5d7c0e3e68675e0a (same pinned-commit caveat).
- rh-reorg-phase-0-1, rh-pull-3-head, and wt-forktest-reorg each test
  the same commit: 9914322267e1358e5542a23c72ec51d1a9ae43df.
- wave-debate-session-1-backup tests the same commit as
  wt-forktest-debate-backup: 3947dca1a77c00818575dbc7476556c8278b8b7b.
- rh-wg-freeze tests the same commit as wt-forktest-wg-freeze:
  f875b34179f570ba1ad555262cd401ddc4a52848.
- wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, and
  wt-wave3-trades each test the same commit:
  bd30978748fa83bbea6e423a7074cf32b7304291.
- origin-tnn-native-lab-rt and origin-tnn-native-lab-live each test
  the same commit: bedf8b4aab0110e3c115fb1bca3903551a32577e (RT ref
  and ls-remote tip agreed at run start; both unchanged since 2021pdt).

## Verdicts (entry, commit, PASS/FAIL/UNTESTABLE, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| arch-wave-20260927-2021pdt (tnn-native-lab-wave-archive-wave-20260927-2021pdt) | baf48e4744c3c075e3fc70a383f0a77efec83ad7 | PASS | live; newly enumerated; tested first in the batch |
| local-tnn-native-lab (task-pinned run-start HEAD) | baf48e4744c3c075e3fc70a383f0a77efec83ad7 | PASS | live; toolchain-dir repair intact (znc_probe.zag plus restored files in tree); pinned znc byte-identical; duplicate of arch-wave-20260927-2021pdt |
| arch-20260923-2321pdt (tnn-native-lab-wave-archive-20260923-2321pdt) | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture; dry-run entry, RESULT body byte-identical to 2021pdt evidence |
| arch-20260924-0221pdt (tnn-native-lab-wave-archive-20260924-0221pdt) | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | fixture |
| arch-20260924-0521pdt (tnn-native-lab-wave-archive-20260924-0521pdt) | 9f681e2719ea45916da19cad15965717bffa82af | PASS | fixture |
| arch-20260924-1121pdt (tnn-native-lab-wave-archive-20260924-1121pdt) | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | fixture |
| arch-20260924-1421pdt (tnn-native-lab-wave-archive-20260924-1421pdt) | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | fixture |
| arch-20260924-1721pdt (tnn-native-lab-wave-archive-20260924-1721pdt) | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | fixture |
| arch-20260926-2021pdt (tnn-native-lab-wave-archive-20260926-2021pdt) | 5ba241235482610f1c8f538d97ca0462164b4014 | PASS | fixture |
| arch-20260927-0221pdt (tnn-native-lab-wave-archive-20260927-0221pdt) | 463b115b69e280da0d7f6da15c6ded2f3f610809 | PASS | fixture |
| arch-20260927-0521pdt (tnn-native-lab-wave-archive-20260927-0521pdt) | 80c40a7afc0231493e0f1f46540a6dbe60c60c3f | PASS | fixture |
| arch-20260927-1421pdt (tnn-native-lab-wave-archive-20260927-1421pdt) | 8929cdd93df7efeb8b67320d5a7d67e2d6bed467 | PASS | fixture |
| arch-wave-20260924-1721pdt (tnn-native-lab-wave-archive-wave-20260924-1721pdt) | d24bb4b502022efc675dda80e0e97436acc09278 | PASS | fixture |
| arch-wave-20260924-2321pdt (tnn-native-lab-wave-archive-wave-20260924-2321pdt) | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | PASS | fixture |
| arch-wave-20260925-0221pdt (tnn-native-lab-wave-archive-wave-20260925-0221pdt) | 058ee02a8a31efc66fb8e92293d399752ce33a6f | PASS | fixture |
| arch-wave-20260925-0521pdt (tnn-native-lab-wave-archive-wave-20260925-0521pdt) | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | PASS | fixture |
| arch-wave-20260925-0821pdt (tnn-native-lab-wave-archive-wave-20260925-0821pdt) | 393007563d27b931c8af59ad9d9fedc336fbed1d | PASS | fixture |
| arch-wave-20260925-1121pdt (tnn-native-lab-wave-archive-wave-20260925-1121pdt) | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | PASS | fixture |
| arch-wave-20260925-1421pdt (tnn-native-lab-wave-archive-wave-20260925-1421pdt) | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | PASS | fixture |
| arch-wave-20260926-0521pdt (tnn-native-lab-wave-archive-wave-20260926-0521pdt) | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | PASS | fixture |
| arch-wave-20260926-0821pdt (tnn-native-lab-wave-archive-wave-20260926-0821pdt) | 4bbbca69cecd9c47602e125545b137380e8bab1a | PASS | fixture |
| arch-wave-20260926-1121pdt (tnn-native-lab-wave-archive-wave-20260926-1121pdt) | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d | PASS | fixture |
| arch-wave-20260926-1421pdt (tnn-native-lab-wave-archive-wave-20260926-1421pdt) | a222f8f178049b9aeee3b053328c59e9b6fd813d | PASS | fixture |
| arch-wave-20260926-1721pdt (tnn-native-lab-wave-archive-wave-20260926-1721pdt) | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a | PASS | fixture |
| arch-wave-20260926-2321pdt (tnn-native-lab-wave-archive-wave-20260926-2321pdt) | 004616f657165191c0d0e89d91fc10a99edd2d6e | PASS | fixture |
| arch-wave-20260927-0821pdt (tnn-native-lab-wave-archive-wave-20260927-0821pdt) | e9373dad1aca4a694cf39d023e7756312e125ba7 | PASS | fixture |
| arch-wave-20260927-1121pdt (tnn-native-lab-wave-archive-wave-20260927-1121pdt) | 4805f5363a0dba762abf2d35e8ab8284abce6731 | PASS | fixture |
| arch-wave-20260927-1721pdt (tnn-native-lab-wave-archive-wave-20260927-1721pdt) | 4042f15bf40b1c73a516ba5eda2a412033db9f6d | PASS | fixture; was live at 2021pdt |
| exp1 (wave-20260927-0221pdt-exp1, pinned) | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | PASS | fixture; duplicate of wt-exp1 |
| exp2 (wave-20260927-0221pdt-exp2, pinned) | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | PASS | fixture; duplicate of wt-exp2 |
| exp-sensory (wave-20260927-0221pdt-sensory, pinned) | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | PASS | fixture; duplicate of wt-exp-sensory |
| wt-exp1 (pinned) | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | PASS | fixture; duplicate of exp1 |
| wt-exp2 (pinned) | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | PASS | fixture; duplicate of exp2 |
| wt-exp-sensory (pinned) | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | PASS | fixture; duplicate of exp-sensory |
| rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | PASS | fixture; superseded tip, ref kept pinned |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | PASS | fixture; P20 gap stays closed |
| rh-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
| rh-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | fixture |
| rh-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| rh-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | UNTESTABLE | pinned toolchain path absent in tree (git show exit 128) |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | UNTESTABLE | pinned toolchain path absent in tree (git show exit 128) |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture; duplicate of rh-reorg-phase-0-1 |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| origin-tnn-native-lab-rt (local RT ref tip at run start) | bedf8b4aab0110e3c115fb1bca3903551a32577e | PASS | fixture; unchanged since 2021pdt |
| origin-tnn-native-lab-live (origin tip via ls-remote at run start) | bedf8b4aab0110e3c115fb1bca3903551a32577e | PASS | fixture; unchanged since 2021pdt; duplicate of the RT entry this wave |
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

No FAIL. No CONFIRM. The two UNTESTABLEs are extraction failures
with content-dependent causes (no result faked).

## Uniform battery evidence (all 54 PASS runs)

Verified across all 54 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (54/54; byte-identical toolchain on every tested fork, no
  divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (54/54).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (54/54); run sha256
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066.
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 54 (matches the frozen value; parsed by tokenizing the
  harness output on whitespace first, never by splitting a packed
  line on '=').
- B3: strict check exit 0 (54/54).
- NEG1: fails as required on 54/54: driver compile exit 1, check exit
  1, and the fork's own znc reports E0002 on the neg1 source on all
  54.
- NEG2: fails as required on 54/54: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1 ("F" vs "W").
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 54/54.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 54/54 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Tree repair verification (local-tnn-native-lab)

At the task-pinned HEAD baf48e4744c3c075e3fc70a383f0a77efec83ad7,
`git ls-tree -r` shows src/tools/toolchain/ holding znc_probe.zag,
znc_linux_x86_64_abed8aa1 (pin verified byte-identical), the two macOS
znc binaries, the R32_E45_ARM64_7CAC_AGGREGATE_ABI bundle files, and
R32_ZNC_PROVENANCE_2026-08-23.json: the 12 files dropped by the
1721pdt merge stay restored (the repair at 37d1d3cab is an ancestor of
the pinned HEAD; `git merge-base --is-ancestor 37d1d3cab baf48e474`
confirmed). The battery's tree-probe step on the local entry
compiled znc_probe.zag with the fork's own znc (exit 0) and the run
emitted R32_ZNC_PROBE_OK, exactly as the frozen battery expects.

## UNTESTABLE analysis

pull/1/head and pull/2/head: extraction failures at the first step,
identical to the prior thirteen waves: `git show
<commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1` fails
("exists on disk, but not in '<commit>'" in both cases). The probe
path `src/tools/toolchain/znc_probe.zag` is likewise absent in both
trees. Their tree roots hold non-TNN research documents; they carry
no src/ directory and no toolchain. This is a property of those
forks' contents, not a toolchain regression. Per the standing rule
they are recorded as UNTESTABLE with that reason (no result faked);
they remain untestable by this battery until their trees gain the
pinned toolchain path.

rh-main (27a4271f): P20 coverage gap stays closed. Its commit object is
in the local store; the pinned znc extracted cleanly with the pin
verified, and the full battery passes (uniform 54/54 evidence).

## Manifest-drift report (P1/P8, vs 2021pdt frozen baseline)

- One new branch: tnn-native-lab-wave-archive-wave-20260927-2021pdt at
  baf48e4744c3c075e3fc70a383f0a77efec83ad7 (the wave-2021pdt LOOP_STATE
  archive commit, enumerated this wave as arch-wave-20260927-2021pdt,
  tested first in the batch at its pinned commit). PASS.
- local-tnn-native-lab moved: fc1a43b8c to baf48e474 (the task-pinned
  run-start HEAD; live, tested at the pin; PASS, toolchain repair
  still intact).
- Both origin entries unchanged at bedf8b4a since 2021pdt close;
  fixture-ized this wave; both still PASS.
- arch-wave-20260927-1721pdt fixture-ized (was live at 2021pdt).
- No missing branches: every other branch, remote-tracking ref, and
  worktree from the 2021pdt baseline is present with unchanged SHAs.
- Remote tips identical at run start and close (fs-gr1, main, r2-7,
  reorg/phase-0-1, wg-freeze, tnn-native-lab, pull/1, pull/2, pull/3
  heads unchanged).
- The 3 pull-head refs carried over from 2021pdt (tips identical to
  ls-remote; no refetch needed).
- All 13 worktrees present, SHAs re-verified, all unchanged except the
  main worktree's checked-out tip (fc1a43b8c at 2021pdt close to
  baf48e474 at this wave's run start; the main worktree is not a
  battery entry itself).
- Coverage-delta accounting, recomputed from this wave's own verdict
  table (standing hygiene rule; 44 unique commits across 56 entries):
  named entries 55 to 56 (+1 new archive entry; the new live archive
  and local-tnn-native-lab coincide on baf48e474 this wave but remain
  two named entries). Live entries 4 to 2 (set changed: the 2021pdt
  live set fixture-ized; new live set is the new archive branch and
  the moved local tip). Unique commits 44 to 44 (+baf48e474, minus the
  superseded fc1a43b8c which no longer appears in any entry). PASS 53
  to 54; FAIL 0 to 0; UNTESTABLE 2 to 2 (the two pull-head entries keep
  the identical cause, fourteen waves running).

## Incidents

- The single-entry dry run passed clean before the batch; its RESULT
  body is byte-identical to the 2021pdt evidence for that entry and
  its evidence dir was deleted before the batch (no bogus evidence
  dirs were created and none were deleted mid-batch).
- Local HEAD moved during this run: baf48e474 at run start to
  9c6646c047abb6cc0ec4869ad438df94229b2715 at close (another lane's
  commit: "wave-20260927-2321pdt: interactive re-survey
  fc1a43b8c..baf48e474, verdict NONE (no new chat/REPL/stdin entry
  points)"). The tested local entry is the task-pinned run-start HEAD
  baf48e474; pinning by commit made the results inert to the move. The
  new commit 9c6646c04 landed after the run-start enumeration; it is
  not a battery entry this wave and will be enumerated by the next
  wave.
- Origin tnn-native-lab tip did not move during this run (bedf8b4a at
  run start and at close).
- No new refs were created by this run. No fetch was run; remote tips
  came from read-only `git ls-remote origin`. The wave lock was not
  touched.
- The three experimental worker branches (exp1, exp2, exp-sensory) are
  under concurrent implementation by other workers; this battery tested
  only the pinned commits (1010a63c3, a2a36e657, c368b8e1f) via
  read-only git show, so mid-write branch state cannot have affected
  the results. Each RESULT.txt pins the tested commit.

## Scratch space

~/workspace/fb2321 at run end holds the extracted harness source
(fork_battery.zag), the rebuilt harness binary (fork_battery), the
driver script (run_one.sh), the batch driver (batch.sh), the
ls-remote start/close captures, harness_build.err, and batch.log. The
56 per-entry evidence dirs were moved into
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/evidence/; build-record
copies (batch.sh, run_one.sh, fork_battery.zag, harness_build.err,
batch.log, lsremote_start.txt, lsremote_close.txt) sit alongside
ENUMERATION_MANIFEST.md in forks/. Per-entry znc copies were deleted
right after each entry's evidence was complete (0 znc.bin files remain
in the evidence tree). The pinned build znc copy (znc_build) was
deleted from scratch before handoff.

## Closing tip re-check

Run-start origin tips (read-only `git ls-remote origin`):
tnn-native-lab bedf8b4aab0110e3c115fb1bca3903551a32577e, main
27a4271f208247a1e9c24cca35468c298b6cd29d.
Closing origin tips (read-only `git ls-remote origin`): tnn-native-lab
bedf8b4aab0110e3c115fb1bca3903551a32577e, main
27a4271f208247a1e9c24cca35468c298b6cd29d.

The tnn-native-lab tip did not move during this run. The main tip
27a4271f was tested via the rh-main entry. Nothing arrived after the
testing window.

## Local HEAD

Task-pinned run-start HEAD:
baf48e4744c3c075e3fc70a383f0a77efec83ad7.
HEAD at close: 9c6646c047abb6cc0ec4869ad438df94229b2715 (moved by
another lane during the run; this worker's extraction was pinned to
the run-start commit and is unaffected).
This worker wrote only new files (this report, the enumeration
manifest, the build-record files, plus the 56 per-entry evidence
dirs); it modified no tracked files and pushed nothing.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git
(read-only rev-parse, branch, for-each-ref, ls-remote, show, worktree
list, log, ls-tree; no checkout, no pull, no push, no fetch, no
reset), sha256sum, grep, cut, tr, head, cmp, diff, mv, the pinned znc
binary, and the rebuilt pure-Zag harness fork_battery. No Python was
used for the battery, the harness build, extraction, any analysis, or
any verification step.

## Evidence archive note (P14)

The 56 per-entry evidence dirs were moved (not copied) from
~/workspace/fb2321/E into
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/evidence/. Each PASS dir
holds RESULT.txt, zag_harness.out, harness.err, znc.path,
tree_probe.zag, forkbat_hello.zag, neg1.zag, neg2.zag, probe_build.log,
probe_run.out, neg1c.out, neg1c.err, neg1k.out, neg1k.err,
neg2_run.out, expected.out, bin_a, bin_b, hello_bin, neg2_bin,
probe_bin, and extract.err; the UNTESTABLE dirs hold RESULT.txt and
extract.err only; no per-entry znc.bin by design. S9 note: the frozen
harness output (zag_harness.out) embeds the pinned znc binary's own
stdout status line, which uses the compiler's own punctuation; that is
captured instrument output of the frozen toolchain, not wave
documentation, and travels as a disclosed caveat unedited.

## tnn_chat FIT note

Fresh FIT behavioral battery was NOT run this wave (queued separately
by the parent). FIT staleness: 4 of 8 as of 2021pdt, so 5 of 8 after
this wave. The harness behavior was re-verified on the main line via
the single-entry dry run (arch-20260923-2321pdt, RESULT body
byte-identical to the 2021pdt evidence).

## UNTOUCHED lines

- The six governance rulings are untouched: S7 strike vs debate
  narrowing, MD-SSD-1 keep-with-UNVERIFIABLE vs re-freeze and re-run,
  S11 pull, S11-AUD pull, C12 judge queue, Python-mirror logic
  adoption.
- Sealed blind pairs untouched: R9, C1, C2v3, S11-IMG, C12, S11-AUD,
  S13, S14, whirlpool-planform. None were opened, re-certified, or
  moved.

## Proposed verdict line

CONFIRM fork battery [clean]: 56 named, 54 PASS, 0 FAIL, 2 UNTESTABLE
(toolchain stability only; no new FAIL; the new archive branch and the
moved local tip both PASS at baf48e474 with the toolchain repair
intact; the pull-head UNTESTABLEs are the expected non-TNN
research-doc trees, unchanged cause fourteen waves running).
