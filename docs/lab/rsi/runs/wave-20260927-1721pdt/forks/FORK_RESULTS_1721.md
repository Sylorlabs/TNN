# Fork battery results, wave-20260927-1721pdt

Fork-battery worker (lane 2). Working copy: ~/workspace/tnn-rsi,
branch tnn-native-lab, task-pinned run-start HEAD
f55e8c27ae2df6cc0db572372f5d50a4e3fc032f. Read-only git operations
throughout (rev-parse, for-each-ref, ls-remote, show, worktree list;
no checkout, no pull, no push, no fetch, no reset). Scratch:
~/workspace/fb1721 (fresh this wave). The wave lock was not touched.

## Verdict

54 named battery entries. 49 PASS, 1 FAIL, 4 UNTESTABLE, 0 CONFIRM.
4 live entries; 50 fixture entries.

The FAIL is local-tnn-native-lab at the pinned run-start HEAD
f55e8c27a: the merge kept the pinned znc binary byte-identical (pin
verified) but dropped src/tools/toolchain/znc_probe.zag from the
tree, so the frozen battery's probe step cannot run on this entry.
This is a content loss in the merge resolution, not a toolchain
regression. See Failure analysis.

The four UNTESTABLEs are all content-dependent, never headlined as
failures: origin-tnn-native-lab-rt at
d09d5bfdeccc7a4007e996ac4757cef6af4845fe (origin's merged tip; tree
lacks the pinned toolchain path), origin-tnn-native-lab-live at
f71ff91f66bc672d01f8b0a9544cf1067e465d90 (run-start live origin tip;
commit object not in the local store, no fetch authorized, content
unverifiable read-only), rh-pull-1-head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and rh-pull-2-head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (both trees lack the pinned
toolchain path, identical cause twelve waves running; non-TNN
research-doc repos, still uncovered by this battery). No result was
faked. Scope stamp: this battery certifies toolchain and extraction
stability only, not the contents of the tested commits.

UNTESTABLE caveat: all four UNTESTABLEs are content-dependent (their
trees lack the toolchain path, or their commits are not in the local
store), not toolchain regressions; the counts above are never
headlined without this caveat.

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
verified BEFORE use; tree mode 100755). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to wave-20260927-1121pdt's rebuild; harness build is
deterministic). The harness ran per entry with cwd = entry scratch dir
and ./znc.path naming that entry's own extracted znc copy. Harness
exit 0 with VERDICT=PASS on 49/49 tested battery entries,
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

`git for-each-ref` fresh at run start: 30 local branches, 6 local
remote-tracking refs (no fetch was run this wave; remote state came
from read-only `git ls-remote origin`). Remote heads were enumerated
read-only via `git ls-remote origin` at run start (HEAD plus 6
refs/heads plus 3 refs/pull/*/head refs): fs-gr1 23f6c0f9, main
27a4271f, r2-7 2d99d183, reorg/phase-0-1 991432226, tnn-native-lab
f71ff91f (moved from 9beb0ade), wg-freeze f875b341, pull/1/head
5802fec8, pull/2/head 4b76bb59, pull/3/head 991432226. The 13
worktrees were enumerated via `git worktree list` (SHAs re-verified
per worktree; all unchanged since 1421pdt). A single-entry dry run
(arch-20260923-2321pdt) passed clean before the batch and its
RESULT.txt is byte-identical to the 1421pdt evidence for that entry;
its evidence dir was archived with the batch as that entry's PASS
evidence. The frozen enumeration manifest ENUMERATION_MANIFEST.md in
this run dir lists every named entry, its ref, commit sha, and
live/fixture classification.

Local branches (30): tnn-native-lab (task-pinned run-start HEAD
f55e8c27a), 10 plain archive branches (including the newly enumerated
tnn-native-lab-wave-archive-20260927-1421pdt at 8929cdd93), 15
wave-prefixed archive branches, the 3 experimental worker branches
wave-20260927-0221pdt-exp1, wave-20260927-0221pdt-exp2, and
wave-20260927-0221pdt-sensory (tips unchanged since 1421pdt; each
tested read-only at its pinned commit via git show, toolchain
stability only), and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b (unchanged). No branch known
from the 1421pdt baseline is missing; the only change is the one new
archive branch.

Remote heads (read-only ls-remote at run start): fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5 (unchanged), main at
27a4271f208247a1e9c24cca35468c298b6cd29d (unchanged), r2-7 at
2d99d183f693145c53213639990a3474ff786b69 (unchanged),
reorg/phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df
(unchanged), tnn-native-lab at
f71ff91f66bc672d01f8b0a9544cf1067e465d90 (moved from 9beb0ade;
origin's tnn-native-lab advanced again; moved again mid-run to
a5bba138f513c5f7c818dbf28378db7a6aef08b9 after the testing window,
see Incidents), wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848 (unchanged), pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 (unchanged), pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (unchanged), pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df (unchanged).

Worktrees (13, SHAs re-verified): the 10 forktest/wave3 worktrees
unchanged since 1421pdt (forktest/main at
293602fb1d4a2fd5d680a3376463d61b0572006b, forktest/r2-7 at
a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5, forktest/reorg_phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, forktest/tnn-native-lab at
bd30978748fa83bbea6e423a7074cf32b7304291, forktest/tnn-native-lab-remote
at cea8db22f53ed1294aff5324aa143bd6d1df845e,
forktest/wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b, forktest/wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, and wave3 probe/senses/trades
all at bd30978748fa83bbea6e423a7074cf32b7304291); the 3 exp worktrees
wt-exp1, wt-exp2, wt-sensory unchanged at 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d,
a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4, and
c368b8e1ffecec2f9061011f5d7c0e3e68675e0a, each tested at its pinned
commit read-only.

Origin-tip note: at run start the origin tnn-native-lab tip was
f71ff91f (moved from 9beb0ade since 1421pdt). It was accounted for by
this battery via the origin-tnn-native-lab-live entry (UNTESTABLE:
commit object not in the local store, no fetch authorized). The local
ref refs/remotes/rh-tnn-native-lab-live-tip stays pinned at
b257c02cc68b7a1f079dee28611cccd93b6efc9d as a superseded-tip
fixture. The local remote-tracking ref
refs/remotes/origin/tnn-native-lab sits at
d09d5bfdeccc7a4007e996ac4757cef6af4845fe (the merge parent; stale vs
the live remote tip), covered by origin-tnn-native-lab-rt
(UNTESTABLE: tree lacks the toolchain path). The live tip moved again
mid-run to a5bba138 (object not in local store); it arrived after the
testing window and is noted, not tested. No coverage gap remains on
any value this battery could test.

Extraction method: every entry extracted the pinned znc and probe via
read-only `git show <commit>:src/tools/toolchain/...` into scratch;
extracted copies were chmod +x in scratch only. The four UNTESTABLE
`git show` redirects left 0-byte znc.bin files; all were deleted
before archiving, so no per-entry znc.bin survives anywhere in the
evidence tree (0 znc.bin files).

## Live vs fixture split

Rule used (same as prior waves): Live = entry whose HEAD moved since
last wave, or newly enumerated this wave, or newly testable this
wave. Fixture = unchanged-SHA entries tested for coverage.

Named entries total: 54. Live: 4. Fixture: 50.

Live: arch-20260927-1421pdt (newly enumerated at
8929cdd93df7efeb8b67320d5a7d67e2d6bed467; the new branch was
included first in the test order, before any other entry, and tested
at its pinned commit), local-tnn-native-lab (b876016e6 to f55e8c27a
at run start; the task-pinned HEAD; FAIL, probe loss in the merge),
origin-tnn-native-lab-rt (moved 9beb0ade to d09d5bfde; UNTESTABLE),
origin-tnn-native-lab-live (moved 9beb0ade to f71ff91f at run start;
UNTESTABLE; superseded mid-run by a5bba138).

Fixture: the 24 older archive branches (unchanged SHAs), the 3 exp
branches and their 3 worktrees (unchanged SHAs since 1421pdt, no
longer live; tested at their pinned commits, toolchain stability
only), wave-debate-session-1-backup, rh-tnn-native-lab-live-tip
(superseded tip, see note), rh-main (unchanged; P20 gap stays closed),
rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1, rh-wg-freeze, rh-pull-1-head,
rh-pull-2-head, rh-pull-3-head, the 7 forktest worktrees, and the 3
wave3 worktrees.

All duplicates named explicitly with SHAs (P8):
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

## Verdicts (entry, commit, PASS/FAIL/UNTESTABLE, what broke)

| entry | commit | verdict | notes |
|---|---|---|---|
| arch-20260927-1421pdt (tnn-native-lab-wave-archive-20260927-1421pdt) | 8929cdd93df7efeb8b67320d5a7d67e2d6bed467 | PASS | live; newly enumerated; tested first in the batch |
| local-tnn-native-lab (task-pinned run-start HEAD) | f55e8c27ae2df6cc0db572372f5d50a4e3fc032f | FAIL | live; merge dropped src/tools/toolchain/znc_probe.zag (plus 11 other toolchain-dir files); frozen probe step cannot run; znc binary itself byte-identical (pin verified) |
| origin-tnn-native-lab-rt (local RT ref tip at run start) | d09d5bfdeccc7a4007e996ac4757cef6af4845fe | UNTESTABLE | live; moved 9beb0ade to d09d5bfde; pinned toolchain path absent in tree (git show exit 128) |
| origin-tnn-native-lab-live (origin tip via ls-remote at run start) | f71ff91f66bc672d01f8b0a9544cf1067e465d90 | UNTESTABLE | live; moved 9beb0ade to f71ff91f; commit object not in local store, no fetch authorized |
| arch-20260923-2321pdt (tnn-native-lab-wave-archive-20260923-2321pdt) | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture; dry-run entry, RESULT byte-identical to 1421pdt evidence |
| arch-20260924-0221pdt (tnn-native-lab-wave-archive-20260924-0221pdt) | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | fixture |
| arch-20260924-0521pdt (tnn-native-lab-wave-archive-20260924-0521pdt) | 9f681e2719ea45916da19cad15965717bffa82af | PASS | fixture |
| arch-20260924-1121pdt (tnn-native-lab-wave-archive-20260924-1121pdt) | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | fixture |
| arch-20260924-1421pdt (tnn-native-lab-wave-archive-20260924-1421pdt) | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | fixture |
| arch-20260924-1721pdt (tnn-native-lab-wave-archive-20260924-1721pdt) | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | fixture |
| arch-20260926-2021pdt (tnn-native-lab-wave-archive-20260926-2021pdt) | 5ba241235482610f1c8f538d97ca0462164b4014 | PASS | fixture |
| arch-20260927-0221pdt (tnn-native-lab-wave-archive-20260927-0221pdt) | 463b115b69e280da0d7f6da15c6ded2f3f610809 | PASS | fixture |
| arch-20260927-0521pdt (tnn-native-lab-wave-archive-20260927-0521pdt) | 80c40a7afc0231493e0f1f46540a6dbe60c60c3f | PASS | fixture |
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

The FAIL is an extraction failure at the frozen battery's probe step
(see Failure analysis). The four UNTESTABLEs are extraction failures
with content-dependent causes (no result faked). No CONFIRM.

## Uniform battery evidence (all 49 PASS runs)

Verified across all 49 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (49/49; byte-identical toolchain on every tested fork, no divergence;
  the FAIL entry's znc also extracted with this exact sha before the
  probe step failed).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (49/49).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (49/49); run sha256
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066.
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 49 (matches the frozen value; parsed by tokenizing the
  harness output on whitespace first, never by splitting a packed
  line on '=').
- B3: strict check exit 0 (49/49).
- NEG1: fails as required on 49/49: driver compile exit 1, check exit 1,
  and the fork's own znc reports E0002 on the neg1 source on all 49.
- NEG2: fails as required on 49/49: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1 ("F" vs "W").
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 49/49.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 49/49 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Failure analysis

local-tnn-native-lab (f55e8c27a): the znc extraction succeeded and the
pin verified byte-identical, then the probe extraction failed:
`git show f55e8c27a:src/tools/toolchain/znc_probe.zag` reports
"path ... does not exist in 'f55e8c27a'". Tree inspection shows the
merge f55e8c27a (parents 8929cdd93 and d09d5bfde) kept exactly one
file under src/tools/toolchain/: znc_linux_x86_64_abed8aa1 (blob
611b7f0c215385b7d3073bbebbf6078224c70b4c, byte-identical to the base).
The merge dropped the other 12 files present in the first parent's
toolchain dir (znc_probe.zag, the two macOS znc binaries, the
R32_E45_ARM64_7CAC_AGGREGATE_ABI_* bundle, and
R32_ZNC_PROVENANCE_2026-08-23.json; 423 deletions). The second parent
d09d5bfde had deleted the whole dir in 13c557cd3, so the merge
resolution sided with origin's deletion for everything except the one
Linux binary. The driver's frozen rule maps probe-extraction failure
to FAIL, so the verdict stands as FAIL. This is tree-content loss in
the merge, not a toolchain regression: the pinned znc binary on this
entry is byte-identical to the pin. Until znc_probe.zag is restored on
the line, the frozen battery cannot complete its tree-probe step on
local-tnn-native-lab. This worker did not restore it (a content
change to the branch is outside this lane's mandate); it is flagged
for the parent.

origin-tnn-native-lab-rt (d09d5bfde): `git show
<commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1` fails
("exists on disk, but not in '<commit>'"). The tree has no toolchain
dir at all (origin deleted it in 13c557cd3). Content-dependent
UNTESTABLE, as anticipated in the wave delta.

origin-tnn-native-lab-live (f71ff91f): commit object not in the local
store (git cat-file fails; a control `git show` against a known-bogus
sha produces the identical stderr, confirming the message means the
rev is unresolvable). No fetch is authorized, so the tree content is
unverifiable read-only. Content-dependent UNTESTABLE.

pull/1/head and pull/2/head: extraction failures at the first step,
identical to the prior eleven waves: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails ("exists on disk, but not in '<commit>'" in both cases). The probe
path `src/tools/toolchain/znc_probe.zag` is likewise absent in both
trees. Their tree roots hold non-TNN research documents; they carry no
src/ directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. Per the standing rule they are
recorded as UNTESTABLE with that reason (no result faked); they remain
untestable by this battery until their trees gain the pinned toolchain
path.

rh-main (27a4271f): P20 coverage gap stays closed. Its commit object is
in the local store; the pinned znc extracted cleanly with the pin
verified, and the full battery passes (uniform 49/49 evidence).

## Manifest-drift report (P1/P8, vs 1421pdt frozen baseline)

- One new branch: tnn-native-lab-wave-archive-20260927-1421pdt at
  8929cdd93df7efeb8b67320d5a7d67e2d6bed467 (the wave-1421pdt archive
  commit, enumerated this wave as arch-20260927-1421pdt, tested
  first in the batch at its pinned commit). PASS.
- local-tnn-native-lab moved: b876016e6 to f55e8c27a (the task-pinned
  run-start HEAD; live, tested at the pin). FAIL (probe loss in merge,
  see Failure analysis).
- origin-tnn-native-lab moved (ls-remote): 9beb0ade to f71ff91f at
  run start (live, accounted via origin-tnn-native-lab-live at its
  pinned commit; UNTESTABLE, object absent locally). The live tip moved
  again mid-run to a5bba138f513c5f7c818dbf28378db7a6aef08b9 after the
  testing window (object not in local store; noted, not tested).
- The local remote-tracking ref refs/remotes/origin/tnn-native-lab
  sits at d09d5bfdeccc7a4007e996ac4757cef6af4845fe (the merge parent;
  stale vs the live remote tip), covered by origin-tnn-native-lab-rt
  (UNTESTABLE, toolchain path absent in tree).
- No missing branches: every branch, remote-tracking ref, and worktree
  from the 1421pdt baseline is still present with the same SHAs,
  except the moved entries above.
- Remote tips unchanged at close except tnn-native-lab (all other
  ls-remote values identical at run start and close).
- The 3 pull-head refs carried over from 1421pdt (tips identical to
  ls-remote; no refetch needed).
- All 13 worktrees present, SHAs re-verified, all unchanged.
- Coverage-delta accounting, recomputed from this wave's own verdict
  table (standing hygiene rule; 44 unique commits across 54 entries):
  named entries 52 to 54 (+1 new archive entry, +1 origin-live
  entry; the origin-rt entry changed member 9beb0ade to d09d5bfde).
  Live entries 3 to 4. Unique commits 42 to 44 (+f55e8c27a,
  +8929cdd93, +d09d5bfde, +f71ff91f, minus the superseded b876016e6
  and 9beb0ade which no longer appear in any entry). PASS 50 to 49;
  FAIL 0 to 1 (local-tnn-native-lab probe loss); UNTESTABLE 2 to 4
  (the two pull-head entries keep the identical cause, twelve waves
  running, plus the two origin entries).

## Incidents

- The single-entry dry run passed clean before the batch (no parser
  incident); its RESULT.txt is byte-identical to the 1421pdt evidence
  for that entry and its evidence dir was archived with the batch as
  that entry's PASS evidence; no bogus evidence dirs were created and
  none were deleted.
- Local HEAD moved during this run: f55e8c27a at run start to
  763983e3a62b119edf5eb16a5e67307e0ef86798 at close (another lane's
  commit). The tested local entry is the task-pinned run-start HEAD
  f55e8c27a; pinning by commit made the results inert to the move.
- Origin tnn-native-lab tip moved mid-run: f71ff91f at run start to
  a5bba138 at close (after the testing window; object not in the local
  store; noted, not tested).
- The merge f55e8c27a's first parent is 8929cdd93 (the 1421pdt wave
  archive commit), second parent d09d5bfde (origin tip). The merge
  resolution dropped 12 of 13 toolchain-dir files (see Failure
  analysis); this worker made no content change in response.
- No new refs were created by this run. No fetch was run; remote tips
  came from read-only `git ls-remote origin`. The wave lock was not
  touched.
- The three experimental worker branches (exp1, exp2, exp-sensory) are
  under concurrent implementation by other workers; this battery tested
  only the pinned commits (1010a63c3, a2a36e657, c368b8e1f) via
  read-only git show, so mid-write branch state cannot have affected
  the results. Each RESULT.txt pins the tested commit.

## Scratch space

~/workspace/fb1721 at run end holds the extracted harness source
(fork_battery.zag), the rebuilt harness binary (fork_battery), the
driver script (run_one.sh), the batch driver (batch.sh), the
ls-remote start/close captures, harness_build.err, znc_extract.err,
batch.log, and the dry-run state. The 54 per-entry evidence dirs were
moved into
docs/lab/rsi/runs/wave-20260927-1721pdt/forks/evidence/ (see P14
note). Per-entry znc copies were deleted right after each entry's
evidence was complete (0 znc.bin files remain in the evidence tree).
The pinned build znc copy (znc_build) was deleted from scratch before
handoff.

## Closing tip re-check

Run-start origin tips (read-only `git ls-remote origin`):
tnn-native-lab f71ff91f66bc672d01f8b0a9544cf1067e465d90, main
27a4271f208247a1e9c24cca35468c298b6cd29d.
Closing origin tips (read-only `git ls-remote origin`): tnn-native-lab
a5bba138f513c5f7c818dbf28378db7a6aef08b9, main
27a4271f208247a1e9c24cca35468c298b6cd29d.

The tnn-native-lab tip moved during this run (after the testing
window); the run-start tip f71ff91f was accounted for by this battery
via the origin-tnn-native-lab-live entry. The main tip 27a4271f was
tested via the rh-main entry. Nothing else arrived after the testing
window.

## Local HEAD

Task-pinned run-start HEAD:
f55e8c27ae2df6cc0db572372f5d50a4e3fc032f.
HEAD at close: 763983e3a62b119edf5eb16a5e67307e0ef86798 (moved by
another lane during the run; this worker's extraction was pinned to
the run-start commit and is unaffected).
This worker wrote only new files (this report, the enumeration
manifest, plus the 54 per-entry evidence dirs); it modified no tracked
files and pushed nothing.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git
(read-only rev-parse, branch, for-each-ref, ls-remote, show, worktree
list, log, diff, ls-tree; no checkout, no pull, no push, no fetch, no
reset), sha256sum, grep, cut, tr, head, cmp, diff, mv, the pinned znc
binary, and the rebuilt pure-Zag harness fork_battery. No Python was
used for the battery, the harness build, extraction, any analysis, or
any verification step.

## Evidence archive note (P14)

The 54 per-entry evidence dirs were moved (not copied) from
~/workspace/fb1721/E into
docs/lab/rsi/runs/wave-20260927-1721pdt/forks/evidence/. Each PASS dir
holds RESULT.txt, zag_harness.out, harness.err, znc.path,
tree_probe.zag, forkbat_hello.zag, neg1.zag, neg2.zag, probe_build.log,
probe_run.out, neg1c.out, neg1c.err, neg1k.out, neg1k.err,
neg2_run.out, expected.out, bin_a, bin_b, hello_bin, neg2_bin,
probe_bin, and extract.err; the FAIL dir holds RESULT.txt, extract.err,
and the znc pin line (no harness artifacts, the driver stopped at the
probe step); the UNTESTABLE dirs hold RESULT.txt and extract.err only;
no per-entry znc.bin by design. S9 note: the frozen harness output
(zag_harness.out) embeds the pinned znc binary's own stdout status
line, which uses the compiler's own punctuation; that is captured
instrument output of the frozen toolchain, not wave documentation,
and travels as a disclosed caveat unedited.

## tnn_chat FIT note

Fresh FIT behavioral battery was NOT run this wave (queued separately
by the parent). FIT staleness: 2 of 8 as of 1421pdt, so 3 of 8 after
this wave. The harness behavior was re-verified on the main line via
the single-entry dry run (arch-20260923-2321pdt, RESULT.txt
byte-identical to the 1421pdt evidence).

## UNTOUCHED lines

- The six governance rulings are untouched: S7 strike vs debate
  narrowing, MD-SSD-1 keep-with-UNVERIFIABLE vs re-freeze and re-run,
  S11 pull, S11-AUD pull, C12 judge queue, Python-mirror logic
  adoption.
- Sealed blind pairs untouched: R9, C1, C2v3, S11-IMG, C12, S11-AUD,
  S13, S14, whirlpool-planform. None were opened, re-certified, or
  moved.

## Proposed verdict line

CONFIRM fork battery [RE-CERT with one FAIL]: 54 named, 49 PASS, 1
FAIL, 4 UNTESTABLE, 0 CONFIRM (toolchain stability only; the FAIL is
the merge dropping znc_probe.zag from the local tree while the pinned
znc binary stays byte-identical; pull-head UNTESTABLEs are the
expected non-TNN research-doc trees, unchanged cause twelve waves
running; both origin entries UNTESTABLE with content-dependent
causes).
