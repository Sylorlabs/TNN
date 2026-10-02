# Fork battery results, wave-20260927-0221pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
af657c8e5da5e6105b4d8e106d20d83d57b6d508 (merge of
004616f657165191c0d0e89d91fc10a99edd2d6e, the new archive commit, and
c3f2261d6397c8498f273c73cd9c4261ac2c4a0c, the origin/tnn-native-lab
state at merge time; add/add conflicts in docs/lab/invention/survival
resolved keeping both sides. The merged upstream contents are treated
as CLOSED, not re-litigated: content not reviewed, toolchain
stability only). Read-only git operations throughout except the two
authorized read-only fetches named below. Scratch: /tmp/fb0221 (fresh
this wave). The wave lock was not touched.

## Verdict

48 named battery entries. 46 PASS, 2 extraction FAIL, 0 CONFIRM. 35
unique commits. 10 live entries, 5 unique live commits; 38 fixture
entries.

The two extraction FAILs are the expected ones: rh-pull-1-head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and rh-pull-2-head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (both trees lack the pinned
toolchain path, identical cause seven waves running; non-TNN
research-doc repos, still uncovered by this battery). The P20 coverage
gap from last wave is CLOSED: rh-main at
27a4271f208247a1e9c24cca35468c298b6cd29d was fetched read-only into
refs/remotes/rh-main during this run, its commit object is now
present locally, the pinned znc extracted cleanly with pins verified,
and the full battery passes. No CONFIRM entries this wave. Scope
stamp: this battery certifies toolchain and extraction stability
only, not the contents of the merged commits.

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
VERDICT=PASS on 46/46 tested battery entries, VERDICT=FAIL on 0.

The shell driver run_one.sh is a faithful reuse of the frozen 2321pdt
driver approach (identical test sources, identical znc flags,
identical expected output): it extracts the znc and probe read only,
records their shas, verifies both against the pins, runs the rebuilt
harness, extracts the B2 bin sha by tokenizing the harness output on
whitespace first (no packed line is ever split on '='), confirms NEG1
fails with E0002 reported by the fork's own znc stderr, confirms NEG2
stdout differs from expected at char 1 (run stdout "WRONG OUTPUT" vs
expected "FORKBATTERY-OK 42"), compiles the tree probe with the fork's
own znc and runs it expecting R32_ZNC_PROBE_OK, then deletes the
per-entry znc copy. Correct invocations honored: znc prints its status
line on stdout (the frozen harness output captures it inside
b3_check_stdout; the driver's orchestrator checks never parse program
output out of a compiler status line), and strict checking uses the
frozen flag order `znc check file.zag --strict --no-zagd`.

## Enumeration (fresh, this wave)

`git branch` fresh at run start: 25 local branches (4 more than
2321pdt). `git for-each-ref refs/remotes` at run start: one
remote-tracking ref, origin/tnn-native-lab at
c3f2261d6397c8498f273c73cd9c4261ac2c4a0c. Remote heads were enumerated
read-only via `git ls-remote origin` at run start (HEAD plus 6
refs/heads plus 3 refs/pull/*/head refs), same ref set as prior
waves. The 13 worktrees were enumerated via `git worktree list` (SHAs
re-verified per worktree; the 10 prior worktrees unchanged since
2321pdt, plus 3 new exp worktrees). A single-entry dry run
(arch-20260923-2321pdt) passed clean before the batch; its evidence
dir was kept as that entry's archive.

Local branches (25): tnn-native-lab (task-pinned run-start HEAD
af657c8e5da5e6105b4d8e106d20d83d57b6d508), the 20 archive branches at
the SHAs below (19 unchanged since 2321pdt; the newly enumerated
tnn-native-lab-wave-archive-20260926-2321pdt at
004616f657165191c0d0e89d91fc10a99edd2d6e is the first parent of the
run-start merge), the 3 new experimental worker branches
wave-20260927-0221pdt-exp1, wave-20260927-0221pdt-exp2, and
wave-20260927-0221pdt-sensory (all pinned at af657c8e5da5e6105b4d8e106d20d83d57b6d508
at run start; experiment workers are implementing in them
concurrently, so each was tested read-only at its pinned commit via
git show, toolchain stability only), and
wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b (unchanged):
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
5ba241235482610f1c8f538d97ca0462164b4014,
tnn-native-lab-wave-archive-20260926-2321pdt at
004616f657165191c0d0e89d91fc10a99edd2d6e (newly enumerated),
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
a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a.

Remote heads (read-only ls-remote at run start): fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5 (unchanged), main at
27a4271f208247a1e9c24cca35468c298b6cd29d (unchanged since 2321pdt;
commit object fetched into the local store during this run), r2-7 at
2d99d183f693145c53213639990a3474ff786b69 (unchanged),
reorg/phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df
(unchanged), tnn-native-lab at
b257c02cc68b7a1f079dee28611cccd93b6efc9d (moved since 2321pdt; see
the origin-tip note below), wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848 (unchanged), pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 (unchanged), pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (unchanged), pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df (unchanged).

Worktrees (13, SHAs re-verified; the 10 prior ones unchanged since
2321pdt): forktest/main at 293602fb1d4a2fd5d680a3376463d61b0572006b,
forktest/r2-7 at a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
forktest/reorg_phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df,
forktest/tnn-native-lab at bd30978748fa83bbea6e423a7074cf32b7304291,
forktest/tnn-native-lab-remote at
cea8db22f53ed1294aff5324aa143bd6d1df845e,
forktest/wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b, forktest/wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, and wave3 probe/senses/trades
all at bd30978748fa83bbea6e423a7074cf32b7304291; plus the 3 new exp
worktrees wt-exp1, wt-exp2, wt-sensory (one locked), each pinned at
af657c8e5da5e6105b4d8e106d20d83d57b6d508 at run start and tested at
that pinned commit read-only.

Origin-tip note: at run start the local remote-tracking ref
origin/tnn-native-lab read c3f2261d6397c8498f273c73cd9c4261ac2c4a0c
(the state the executor merged as the run-start merge's second
parent), while live origin/tnn-native-lab had already advanced to
b257c02cc68b7a1f079dee28611cccd93b6efc9d (origin moved after the
pre-wave fetch). The live tip was fetched read-only into the new local
ref refs/remotes/rh-tnn-native-lab-live-tip during this run and tested
as its own entry (PASS). No coverage gap remains on either value.

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

Named entries total: 48. Live: 10. Fixture: 38.
Unique commits: 35. Unique live commits: 5.

Live: local-tnn-native-lab (377c36fd9 to af657c8e5 at run start),
arch-20260926-2321pdt (newly enumerated, at
004616f657165191c0d0e89d91fc10a99edd2d6e; also the first parent of the
run-start merge), exp1, exp2, exp-sensory (newly enumerated, each
pinned at af657c8e5da5e6105b4d8e106d20d83d57b6d508), wt-exp1,
wt-exp2, wt-exp-sensory (newly enumerated, each pinned at the same
commit), origin-tnn-native-lab-rt (3ac39fc14 to c3f2261d at run
start; the c3f2261d state is merged into the task-pinned HEAD and
tested by this entry), rh-main (27a4271f, unchanged SHA but newly
testable this wave: the authorized fetch brought its commit object
into the local store; the P20 coverage gap is closed), and
rh-tnn-native-lab-live-tip (newly enumerated live origin tip at
b257c02cc68b7a1f079dee28611cccd93b6efc9d, fetched read-only into
refs/remotes/rh-tnn-native-lab-live-tip during this run).

Fixture: the 19 older archive branches, wave-debate-session-1-backup,
rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1, rh-wg-freeze, rh-pull-1-head,
rh-pull-2-head, rh-pull-3-head, the 7 forktest worktrees, and the 3
wave3 worktrees (all unchanged SHAs). The queued 2321pdt entry
rh-tnn-native-lab-tip-start (d9ddc556) is dropped: its superseded-tip
role is now covered by origin-tnn-native-lab-rt at c3f2261d.

All duplicates named explicitly with SHAs (P8):
- local-tnn-native-lab, exp1, exp2, exp-sensory, wt-exp1, wt-exp2, and
  wt-exp-sensory each test the same commit:
  af657c8e5da5e6105b4d8e106d20d83d57b6d508 (the task-pinned run-start
  HEAD; the exp entries test it at the run-start pinned commit,
  toolchain stability only).
- arch-20260926-2321pdt tests the same commit as the run-start merge's
  first parent: 004616f657165191c0d0e89d91fc10a99edd2d6e.
- origin-tnn-native-lab-rt tests the same commit as the run-start
  merge's second parent (the merged upstream state, CLOSED content):
  c3f2261d6397c8498f273c73cd9c4261ac2c4a0c.
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
| local-tnn-native-lab (task-pinned run-start HEAD) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live |
| arch-20260926-2321pdt (tnn-native-lab-wave-archive-20260926-2321pdt) | 004616f657165191c0d0e89d91fc10a99edd2d6e | PASS | live; newly enumerated; first parent of run-start merge |
| exp1 (wave-20260927-0221pdt-exp1, pinned) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live; newly enumerated; duplicate of run-start HEAD |
| exp2 (wave-20260927-0221pdt-exp2, pinned) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live; newly enumerated; duplicate of run-start HEAD |
| exp-sensory (wave-20260927-0221pdt-sensory, pinned) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live; newly enumerated; duplicate of run-start HEAD |
| wt-exp1 (pinned) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live; newly enumerated; duplicate of run-start HEAD |
| wt-exp2 (pinned) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live; newly enumerated; duplicate of run-start HEAD |
| wt-exp-sensory (pinned) | af657c8e5da5e6105b4d8e106d20d83d57b6d508 | PASS | live; newly enumerated; duplicate of run-start HEAD |
| origin-tnn-native-lab-rt (remote-tracking, run-start value) | c3f2261d6397c8498f273c73cd9c4261ac2c4a0c | PASS | live; second parent of run-start merge |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | PASS | live; newly testable; P20 coverage gap CLOSED by authorized fetch |
| rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | PASS | live; newly enumerated live origin tip; fetched read-only during this run |
| rh-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
| rh-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | fixture |
| rh-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| rh-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FAIL | extraction failure: no toolchain path in tree |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FAIL | extraction failure: no toolchain path in tree |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture; duplicate of rh-reorg-phase-0-1 |
| arch-20260926-2021pdt | 5ba241235482610f1c8f538d97ca0462164b4014 | PASS | fixture |
| arch-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture; dry-run entry, kept |
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
extraction failures (see Failure analysis). No CONFIRM entries.

## Uniform battery evidence (all 46 PASS runs)

Verified across all 46 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (46/46; byte-identical toolchain on every tested fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (46/46).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (46/46); run sha256
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066.
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 46 (matches the frozen value; parsed by tokenizing the
  harness output on whitespace first, never by splitting a packed
  line on '=').
- B3: strict check exit 0 (46/46).
- NEG1: fails as required on 46/46: driver compile exit 1, check exit 1,
  and the fork's own znc reports E0002 on the neg1 source on all 46.
- NEG2: fails as required on 46/46: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1 ("F" vs "W").
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 46/46.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 46/46 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Failure analysis

pull/1/head and pull/2/head: extraction failures at the first step,
identical to the 2321pdt, 2021pdt, 1721pdt, 1421pdt, 1121pdt, 0821pdt,
and 0521pdt waves: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails ("exists on disk, but not in '<commit>'" in both cases). The probe
path `src/tools/toolchain/znc_probe.zag` is likewise absent in both
trees. Their tree roots hold non-TNN research documents; they carry no
src/ directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

rh-main (27a4271f): RESOLVED this wave. The authorized read-only fetch
`git fetch origin main:refs/remotes/rh-main` brought the commit
object into the local store (git cat-file -e now succeeds), the pinned
znc extracted cleanly with the pin verified, and the full battery
passes (46/46 uniform evidence). The P20 coverage gap is closed; no
CONFIRM entries remain.

## P19 coverage-delta accounting vs 2321pdt

2321pdt reported 41 named entries, 38 PASS / 2 extraction FAIL / 1
CONFIRM, 34 unique commits, 4 live entries / 4 unique live commits, 37
fixtures. This wave reports 48 named entries, 46 PASS / 2 extraction
FAIL / 0 CONFIRM, 35 unique commits, 10 live entries / 5 unique live
commits, 38 fixtures.

- Named entries 41 to 48: +1 newly enumerated archive branch
  (tnn-native-lab-wave-archive-20260926-2321pdt at 004616f65), +3 new
  experimental worker branches (exp1, exp2, exp-sensory), +3 new exp
  worktrees (wt-exp1, wt-exp2, wt-exp-sensory), +1 newly enumerated
  live origin tip entry (rh-tnn-native-lab-live-tip), -1 dropped queued
  entry (rh-tnn-native-lab-tip-start at d9ddc556; its superseded-tip
  role is now covered by origin-tnn-native-lab-rt at c3f2261d).
- Live entries 4 to 10: the 2 continuing live entries
  (local-tnn-native-lab, origin-tnn-native-lab-rt, both moved), plus 8
  new live entries: arch-20260926-2321pdt (newly enumerated), exp1,
  exp2, exp-sensory, wt-exp1, wt-exp2, wt-exp-sensory (newly
  enumerated), rh-main (newly testable; was fixture-CONFIRM in 2321pdt),
  rh-tnn-native-lab-live-tip (newly enumerated). The 2321pdt live
  entries arch-20260926-2021pdt (fixture now) and
  rh-tnn-native-lab-tip-start (dropped entry) are no longer live.
- Extraction FAILs stay at 2: the same expected pull-head FAILs,
  unchanged cause.
- CONFIRM 1 to 0: rh-main moves from P20 CONFIRM (coverage gap) to
  PASS after the authorized fetch.
- Unique commits 34 to 35: +4 new (af657c8e5, 004616f65, c3f2261d,
  b257c02c) minus 3 no longer tested (377c36fd9, 3ac39fc14, d9ddc556).

## Incidents

- None this wave. The single-entry dry run passed clean before the
  batch (no parser incident), so its evidence dir was kept as the
  arch-20260923-2321pdt archive entry; no bogus evidence dirs were
  created and none were deleted.
- The two authorized read-only fetches created two new local refs:
  refs/remotes/rh-main (at 27a4271f208247a1e9c24cca35468c298b6cd29d)
  and refs/remotes/rh-tnn-native-lab-live-tip (at
  b257c02cc68b7a1f079dee28611cccd93b6efc9d). No existing ref moved
  under this run: the remote-tracking ref origin/tnn-native-lab stayed
  at c3f2261d, and local HEAD did not move during this run
  (af657c8e5 at start and at close). The wave lock was not touched.
- The three experimental worker branches (exp1, exp2, exp-sensory) are
  under concurrent implementation by other workers; this battery tested
  only the run-start pinned commit af657c8e5 via read-only git show,
  so mid-write worktree state cannot have affected the results. Branch
  tips may have moved since enumeration; each RESULT.txt pins the
  tested commit.

## Scratch space

/tmp/fb0221 at run end holds the pinned znc copy, the extracted
harness source, the rebuilt harness binary, the probe source, the
driver script, the entry list, and the run log (about 9M total).
Per-entry znc copies were deleted right after each entry's evidence
was complete (0 znc.bin files remain in the evidence tree).

## Closing tip re-check

Run-start origin tips (read-only `git ls-remote origin`):
tnn-native-lab b257c02cc68b7a1f079dee28611cccd93b6efc9d, main
27a4271f208247a1e9c24cca35468c298b6cd29d.
Closing origin tips (read-only `git ls-remote origin`): identical
values.

The tips did not move during this run. The live tnn-native-lab tip
b257c02c was tested by this battery via the rh-tnn-native-lab-live-tip
entry. The merged state c3f2261d was tested via the task-pinned
run-start HEAD and the origin-tnn-native-lab-rt entry. The main tip
27a4271f was tested via the rh-main entry. Nothing arrived after the
testing window.

## Local HEAD

Task-pinned run-start HEAD:
af657c8e5da5e6105b4d8e106d20d83d57b6d508.
HEAD at run end: af657c8e5da5e6105b4d8e106d20d83d57b6d508. Local HEAD
did not move during this run. The tested local entry is the task-pinned
run-start HEAD. This worker wrote only new files (this report plus the
48 per-entry evidence dirs); it modified no tracked files, made no
commits, and pushed nothing.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git
(read-only rev-parse, branch, for-each-ref, ls-remote, show, worktree
list, cat-file, log; plus the two task-authorized read-only fetches
for rh-main and the live tnn-native-lab tip; no checkout, no pull, no
push), sha256sum, grep, awk, cut, sed, cmp, head, xargs, the pinned
znc binary, and the rebuilt pure-Zag harness fork_battery. No Python
was used for the battery, the harness build, extraction, any
analysis, or any verification step.

## Evidence archive note (P14)

The 48 per-entry evidence dirs were moved (not copied) from
/tmp/fb0221/E into
docs/lab/rsi/runs/wave-20260927-0221pdt/forks/evidence/. Each PASS dir
holds RESULT.txt, zag_harness.out, harness.err, znc.path,
tree_probe.zag, forkbat_hello.zag, neg1.zag, neg2.zag, probe_build.log,
probe_run.out, neg1c.out, neg1c.err, neg1k.out, neg1k.err,
neg2_run.out, expected.out, bin_a, bin_b, hello_bin, neg2_bin,
probe_bin, and extract.err; the FAIL dirs hold RESULT.txt and
extract.err only; no per-entry znc.bin by design. S9 note: the
frozen harness output (zag_harness.out) embeds the pinned znc binary's
own stdout status line, which uses the compiler's own punctuation;
that is captured instrument output of the frozen toolchain, not wave
documentation, and travels as a disclosed caveat unedited.
