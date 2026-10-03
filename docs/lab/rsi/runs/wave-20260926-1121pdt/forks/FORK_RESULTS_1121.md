# Fork battery results, wave-20260926-1121pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2 (merge of origin/tnn-native-lab
tip 94625817c into local 4bbbca69c; the 15 new upstream commits from Micah
are treated as CLOSED, not re-litigated: content not reviewed, toolchain
stability only). Read-only git operations except one FETCH_HEAD-scoped fetch
(see Incident 1) and the final evidence commit of this file. Scratch:
/tmp/tnn-forkbattery-1121pdt (fresh this wave; /tmp is a 512M tmpfs, checked
at 512M free before starting; per-entry znc copies were deleted after each
entry's sha was recorded, so /tmp never exceeded 4M during the run).

## Verdict

38 named entries. 36 PASS, 2 extraction FAIL (origin pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and origin pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba; both trees lack the pinned
toolchain path, identical cause to the 0821pdt and 0521pdt waves; non-TNN
research-doc repos, still uncovered by this battery). 31 unique commits.
5 unique live commits (02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2,
4bbbca69cecd9c47602e125545b137380e8bab1a,
94625817c6f65e07c4ac99abde5dd533f0e810a5,
e74271015a7d1c7d3a396f67f8e14c544c225b23,
7ea4d2e61bee5e96f0c4db157a792794b7b176e4).
Live entries: 5 (local tnn-native-lab at the task-pinned run-start HEAD,
the newly enumerated archive branch
tnn-native-lab-wave-archive-wave-20260926-0821pdt, the remote-tracking ref
origin/tnn-native-lab at its run-start value 94625817c, and the two origin
tips seen during the run: e7427101 at run start and 7ea4d2e61 mid-run).
Fixture entries: 33. Every duplicate SHA named explicitly below (P1: every
enumerated entry tested; P8: duplicate SHAs named, none merged silently).
Closing tip re-check: the origin tip moved twice more during this run
(7ea4d2e61 to 006dfe027944f395a47ae8fe6d1e3329a9d7634e, then to
7c19065e7b1ce13f6479ba50b4f35e110156c734 at close); both newer tips arrived
after the testing window and are flagged for next-wave pickup, untested.
Scope stamp: this battery certifies toolchain and extraction stability only,
not the contents of the merged commits.
Incident caveats: (1) the FETCH_HEAD-scoped fetch fast-forwarded the local
remote-tracking ref origin/tnn-native-lab from 94625817c to 7ea4d2e61; no
local branch, worktree, or working-copy state was disturbed; (2) a summary
parsing bug in the first orchestrator pass marked all entries FAIL on a
mis-parsed B2 bin sha; the raw per-entry evidence files were correct and
verdicts were recomputed from them with fixed parsing (see Incident 2).

## Summary

36/36 toolchain-bearing entries PASS: frozen shell battery (B1, B2 rerun,
B2 recompile-identical, B3 `znc check <file>.zag --strict --no-zagd`, NEG1,
NEG2, fork-tree PROBE) plus the rebuilt pure-Zag harness (VERDICT=PASS,
exit 0 on all 36). On all 36 passing entries the extracted znc sha256
matched the pinned value byte for byte
(498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
36/36, single distinct value) and the probe source sha was identical
(3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919,
36/36, single distinct value). NEG1/NEG2 discriminated as required on all
36 (NEG1 fails compile and check with E0002 unterminated string literal;
NEG2 compiles and checks but its stdout differs from expected at char 1,
line 1). The B2 recompiled binary sha matched the frozen pin on all 36
(75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2,
single distinct value).

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
VERDICT=PASS on 36/36 tested entries, VERDICT=FAIL on 0.

The shell driver run_fork.sh is a faithful port of the frozen 2321pdt
driver (identical test sources, identical znc flags, identical expected
output); only the scratch BASE was relocated to this wave's /tmp scratch
dir instead of the 2321pdt in-repo scratch path.

## Enumeration (fresh, this wave)

`git branch` fresh at run start: 17 local branches. `git branch -r`: one
remote-tracking ref (origin/tnn-native-lab, at 94625817c at run start).
Read-only `git ls-remote origin` at run start: 6 refs/heads plus 3
refs/pull/*/head refs (tnn-native-lab at e7427101 then). In addition, the
10 detached worktrees under ~/workspace/tnn-rsi-wave3/ were enumerated via
`git worktree list` (SHAs re-verified per worktree, all unchanged since
0821pdt).

Local branches (17): tnn-native-lab (task-pinned run-start HEAD
02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2; the branch kept moving during
this run on coordinator commits, ending at 3eddd54a4; tested entry is the
pinned run-start HEAD), the 14 archive branches at unchanged SHAs
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
2e2c65fb294e85348d4329ca1e55caf8f6c258a9,
tnn-native-lab-wave-archive-wave-20260926-0521pdt at
4328a8350d987a65c4e86e4973dbe45c9d5f6cd5),
tnn-native-lab-wave-archive-wave-20260926-0821pdt at
4bbbca69cecd9c47602e125545b137380e8bab1a (newly enumerated this wave),
and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b.

Remote-tracking: origin/tnn-native-lab at
94625817c6f65e07c4ac99abde5dd533f0e810a5 at run start (moved 6c3c7b69c
to 94625817c since 0821pdt). See Incident 1 for the mid-run value change.

Remote heads (read-only ls-remote at run start; pull heads and the five
non-tnn-native-lab heads unchanged since 0821pdt):
tnn-native-lab at e74271015a7d1c7d3a396f67f8e14c544c225b23, fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5, main at
0ab8ed6bba02d4d59c45acb2fb22e00adbe8e185, r2-7 at
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1 at
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848, pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57, pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df.

Worktrees (10, SHAs re-verified, all unchanged since 0821pdt):
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

Extraction method: every entry (including the local entry, keyed to the
task-pinned run-start HEAD 02ee5ae59d) extracted the pinned znc and probe
via read-only `git show <commit>:src/tools/toolchain/...` into scratch;
extracted copies were chmod +x in scratch only. The mid-run origin tip
7ea4d2e61 was obtained via a FETCH_HEAD-scoped fetch (see Incident 1) and
extracted via `git show FETCH_HEAD:...`. No worktree was used as a live
test target (SHAs were the extraction key).

## Live vs fixture split

Rule used (same as 0821pdt): Live = entry whose HEAD moved since last
wave, or newly enumerated this wave. Fixture = unchanged-SHA entries
tested for coverage.

Named entries total: 38. Live: 5. Fixture: 33.
Unique commits: 31. Unique live commits: 5.

Live: local-tnn-native-lab (4328a8350d to 02ee5ae59d),
arch-wave-0926-0821 (newly enumerated this wave, at 4bbbca69c),
origin-tnn-native-lab-rt (6c3c7b69c to 94625817c at run start),
rh-tnn-native-lab-tip-start (6c3c7b69c to e7427101, run-start ls-remote
tip), rh-tnn-native-lab-tip-close (e7427101 to 7ea4d2e61, mid-run tip).

Fixture: the 14 older archive branches, wave-debate-session-1-backup,
fs-gr1, main, r2-7, reorg/phase-0-1, wg-freeze, pull/1/head, pull/2/head,
pull/3/head, the 7 forktest worktrees, and the 3 wave3 worktrees
(all unchanged SHAs).

All duplicates named explicitly with SHAs (P8):
- rh-reorg-phase-0-1, rh-pull-3-head, and wt-forktest-reorg each test the
  same commit: 9914322267e1358e5542a23c72ec51d1a9ae43df.
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
| local tnn-native-lab (task-pinned run-start HEAD) | 02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2 | PASS | live |
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
| arch tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a | PASS | live; newly enumerated |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | PASS | fixture |
| origin/tnn-native-lab (remote-tracking, run-start value) | 94625817c6f65e07c4ac99abde5dd533f0e810a5 | PASS | live |
| rh-tnn-native-lab-tip-start (run-start ls-remote tip) | e74271015a7d1c7d3a396f67f8e14c544c225b23 | PASS | live |
| rh-tnn-native-lab-tip-close (mid-run tip) | 7ea4d2e61bee5e96f0c4db157a792794b7b176e4 | PASS | live |
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

## Uniform battery evidence (all 36 PASS entries)

Verified across all 36 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (36/36; byte-identical toolchain on every fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (36/36).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (36/36).
- B2: rerun stdout identical; recompile byte-identical (cmp -s);
  bin sha256 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 36 (matches the frozen value).
- B3: `znc check forkbat_hello.zag --strict --no-zagd` exit 0
  (36/36).
- NEG1: fails as required on 36/36: compile exit 1, check exit 1
  (E0002: unterminated string literal).
- NEG2: fails as required on 36/36: compile exit 0, check exit 0,
  run exit 0, stdout differs from expected at char 1, line 1.
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  on 36/36.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 36/36
  (reference_sha256 PASS, b1_cmp PASS, b2_bin_cmp PASS, B3 PASS,
  both negative controls failing as required); VERDICT=FAIL on 0.

## Failure analysis (pull/1/head, pull/2/head)

Both are extraction failures at the first step, identical to the
0821pdt and 0521pdt waves: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails ("exists on disk, but not in '<commit>'"). The probe path
`src/tools/toolchain/znc_probe.zag` is likewise absent in both trees.
Their tree roots hold non-TNN research documents; they carry no src/
directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

## Incident 1: FETCH_HEAD-scoped fetch updated the remote-tracking ref

To test the run-start origin tip e7427101 (whose objects were not local),
this worker ran `git fetch origin refs/heads/tnn-native-lab` intending a
FETCH_HEAD-only fetch with no local ref updates. The fetch succeeded
(FETCH_HEAD recorded the then-current tip 7ea4d2e61; the origin tip had
already moved e7427101 to 7ea4d2e61 between the run-start ls-remote and
the fetch), but it also fast-forwarded the local remote-tracking ref
refs/remotes/origin/tnn-native-lab from 94625817c to 7ea4d2e61. No local
branch, worktree, or working-copy state was disturbed; the update is a
pure fast-forward to the true upstream tip, which is what any ordinary
fetch would record. This worker performed no further fetches. Lesson for
future waves: an explicit refspec on the `git fetch` command line does
not suppress the remote-tracking ref update in this git version; if the
tracking ref must stay frozen, snapshot its value first (as done here:
94625817c) and treat the live value as moved-by-worker.

## Incident 2: orchestrator summary parsing bug (evidence intact)

The first orchestrator pass (run_all.sh) had two script bugs, both in the
worker's own orchestration, neither in the frozen battery or the harness:
(a) the per-entry output redirect targeted a directory run_fork.sh had not
created yet, so all 38 entries spuriously recorded EXTRACTION_FAIL; fixed
by creating the entry dir before redirecting, then re-ran all 38 entries
from scratch. (b) After the re-run, the B2 bin sha was parsed from the
harness output with `cut -d= -f2`, but the harness prints all B2 key/value
pairs on one line, so the parse grabbed the wrong field and all 36 entries
spuriously recorded b2bin-pin-mismatch. The raw per-entry evidence files
(RESULT.txt, zag_harness.out, znc.sha256, tree_probe.zag) were correct in
both passes; verdicts were recomputed from those files with a fixed parser
(sed extraction of b2_bin_a_sha256), yielding the 36 PASS / 2 extraction
FAIL verdicts above. No entry was judged on mis-parsed data.

## Scratch space

/tmp free at run start: 512M of 512M (0 percent used). Peak /tmp usage
during the run: under 4M (per-entry 8.3M znc copies were deleted right
after each entry's sha was recorded; RESULT and harness evidence files
were kept). No /tmp-full incident this wave.

## Closing tip re-check

Run-start origin tip (read-only `git ls-remote origin tnn-native-lab`):
e74271015a7d1c7d3a396f67f8e14c544c225b23
Mid-run tip (FETCH_HEAD at fetch time): 7ea4d2e61bee5e96f0c4db157a792794b7b176e4
Closing origin tip (read-only `git ls-remote origin tnn-native-lab`):
7c19065e7b1ce13f6479ba50b4f35e110156c734

The tip moved during this run (e7427101 to 7ea4d2e61 to 006dfe02 to
7c19065e; upstream is pushing rapidly). The run-start tip e7427101 and
the mid-run tip 7ea4d2e61 were both tested by this battery (entries
rh-tnn-native-lab-tip-start and rh-tnn-native-lab-tip-close, both PASS).
The two newer tips (006dfe02, 7c19065e) arrived after the testing window;
their trees were not extracted and their toolchain pins are unverified.
Flagged for next-wave pickup. No further fetch was performed to chase
them.

## Local HEAD

Task-pinned run-start HEAD: 02ee5ae59d1296ee1ef8e1754a53f8c0f4caefb2.
HEAD at run end: 3eddd54a4e0d51b1cf9ee5d96eac5ddc8f5d93af.
Local HEAD moved during this run on the coordinator's own wave commits
(interactive TNN survey, DP-1 dossier verification, FIT evidence CONFIRM
carry-over); that delta is the coordinator's merge territory, not this
worker's. The tested local entry is the task-pinned run-start HEAD
02ee5ae59d. This worker's only commit is the evidence commit for this
file (see below); it touched no other tracked files.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summarizer scripts), git
(read-only rev-parse, branch, ls-remote, show, worktree list, cat-file,
plus one FETCH_HEAD-scoped fetch documented above), sha256sum, stat,
grep, sed, cut, cmp, the pinned znc binary, and the rebuilt pure-Zag
harness fork_battery. No Python was used for the battery, the harness
build, extraction, any analysis, or any verification step. No accidental
Python invocation occurred this wave.

## Scope stamp

This battery certifies toolchain and extraction stability only, not
the contents of merged commits.
