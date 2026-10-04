# Fork battery results, wave-20260927-0521pdt

Fork-battery worker. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, task-pinned run-start HEAD
ecbe9b5b7527d6eb4a10fef19adca2b138462d1d ("Merge remote-tracking
branch 'origin/tnn-native-lab' into tnn-native-lab"; the parent merged
origin/tnn-native-lab this morning, 9 new commits integrated cleanly.
The merged upstream contents are treated as CLOSED, not re-litigated:
content not reviewed, toolchain stability only). Read-only git
operations throughout except the two authorized read-only fetches named
below. Scratch: /tmp/fb0521 (fresh this wave). The wave lock was not
touched.

## Verdict

49 named battery entries. 47 PASS, 2 extraction FAIL, 0 CONFIRM. 39
unique commits. 9 live entries, 6 unique live commits; 40 fixture
entries.

The two extraction FAILs are the expected ones: rh-pull-1-head at
5802fec8401f28b4036b0dd5ebb23905610cab57 and rh-pull-2-head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (both trees lack the pinned
toolchain path, identical cause eight waves running; non-TNN
research-doc repos, still uncovered by this battery). No CONFIRM entries
this wave. Scope stamp: this battery certifies toolchain and extraction
stability only, not the contents of the merged commits.

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
verified BEFORE use). Built binary sha256:
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to prior waves; harness build is deterministic).
The harness ran per entry with cwd = entry scratch dir and ./znc.path
naming that entry's own extracted znc copy. Harness exit 0 with
VERDICT=PASS on 47/47 tested battery entries, VERDICT=FAIL on 0.

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

`git for-each-ref` fresh at run start after the task-authorized
`git fetch --all`: 26 local branches, 3 remote-tracking refs at run
start (origin/tnn-native-lab, rh-main, rh-tnn-native-lab-live-tip),
plus 3 pull-head refs fetched read-only into refs/remotes/rh-pull-N-head
during this run. Remote heads were enumerated read-only via
`git ls-remote origin` at run start (HEAD plus 6 refs/heads plus 3
refs/pull/*/head refs), same ref set as prior waves except
tnn-native-lab moved to 7aad68fadb709e6c7700f03d380be9f09b965b80.
The 15 worktrees were enumerated via `git worktree list` (SHAs
re-verified per worktree; the 10 prior non-exp worktrees unchanged
since 0221pdt; the 3 exp worktrees moved to new implementation
commits). A single-entry dry run (arch-20260923-2321pdt) passed clean
before the batch and its RESULT.txt is byte-identical to the 0221pdt
evidence for that entry; its evidence dir was kept as that entry's
archive. The frozen enumeration manifest ENUMERATION_MANIFEST.md in
this run dir lists every named entry, its ref, commit sha, and
live/fixture classification.

Local branches (26): tnn-native-lab (task-pinned run-start HEAD
ecbe9b5b7527d6eb4a10fef19adca2b138462d1d), 8 plain archive branches,
13 wave-prefixed archive branches, the 3 experimental worker branches
wave-20260927-0221pdt-exp1, wave-20260927-0221pdt-exp2, and
wave-20260927-0221pdt-sensory (each pinned at its run-start commit for
testing; experiment workers are implementing in them concurrently, so
each was tested read-only at its pinned commit via git show,
toolchain stability only), and wave-debate-session-1-backup at
3947dca1a77c00818575dbc7476556c8278b8b7b (unchanged). The newly
enumerated archive branch is tnn-native-lab-wave-archive-20260927-0221pdt
at 463b115b69e280da0d7f6da15c6ded2f3f610809 (first parent of the
run-start merge). The plain-named branch
tnn-native-lab-wave-archive-20260926-2321pdt known from 0221pdt no
longer exists; the same commit 004616f657165191c0d0e89d91fc10a99edd2d6e
is now tipped by tnn-native-lab-wave-archive-wave-20260926-2321pdt
(branch renamed between waves; entry renamed
arch-20260926-2321pdt to arch-wave-20260926-2321pdt; coverage is
continuous and the count is unchanged).

Remote heads (read-only ls-remote at run start): fs-gr1 at
23f6c0f9012887448a83edbe9060b73e13d5a7a5 (unchanged), main at
27a4271f208247a1e9c24cca35468c298b6cd29d (unchanged), r2-7 at
2d99d183f693145c53213639990a3474ff786b69 (unchanged),
reorg/phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df
(unchanged), tnn-native-lab at
7aad68fadb709e6c7700f03d380be9f09b965b80 (moved since 0221pdt; merged
by the parent into the run-start HEAD before this wave), wg-freeze at
f875b34179f570ba1ad555262cd401ddc4a52848 (unchanged), pull/1/head at
5802fec8401f28b4036b0dd5ebb23905610cab57 (unchanged), pull/2/head at
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba (unchanged), pull/3/head at
9914322267e1358e5542a23c72ec51d1a9ae43df (unchanged).

Worktrees (15, SHAs re-verified): the 10 forktest/wave3 worktrees
unchanged since 0221pdt (forktest/main at 293602fb1d4a2fd5d680a3376463d61b0572006b,
forktest/r2-7 at a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
forktest/reorg_phase-0-1 at 9914322267e1358e5542a23c72ec51d1a9ae43df,
forktest/tnn-native-lab at bd30978748fa83bbea6e423a7074cf32b7304291,
forktest/tnn-native-lab-remote at cea8db22f53ed1294aff5324aa143bd6d1df845e,
forktest/wave-debate-session-1-backup at 3947dca1a77c00818575dbc7476556c8278b8b7b,
forktest/wg-freeze at f875b34179f570ba1ad555262cd401ddc4a52848, and
wave3 probe/senses/trades all at bd30978748fa83bbea6e423a7074cf32b7304291);
the 3 exp worktrees wt-exp1, wt-exp2, wt-sensory moved since 0221pdt to
1010a63c3c1cc3f3724f6cf0ca55decc08207a2d,
a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4, and
c368b8e1ffecec2f9061011f5d7c0e3e68675e0a respectively, each tested at
its run-start pinned commit read-only.

Origin-tip note: at run start the local remote-tracking ref
origin/tnn-native-lab was already at 7aad68fad (the state the parent
merged as the run-start merge's second parent). The live tip was
tested by this battery via the origin-tnn-native-lab-rt entry (PASS).
The local ref refs/remotes/rh-tnn-native-lab-live-tip stays pinned at
b257c02cc68b7a1f079dee28611cccd93b6efc9d as a superseded-tip fixture;
the b257c02c value is no longer the live origin tip, and the live tip
7aad68fad is covered by origin-tnn-native-lab-rt. No coverage gap
remains on either value.

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

Named entries total: 49. Live: 9. Fixture: 40.
Unique commits: 39. Unique live commits: 6.

Live: local-tnn-native-lab (af657c8e5 to ecbe9b5b7 at run start),
arch-20260927-0221pdt (newly enumerated, at
463b115b69e280da0d7f6da15c6ded2f3f610809; also the first parent of the
run-start merge), exp1, exp2, exp-sensory (moved since 0221pdt; each
pinned at its run-start commit, tested read-only at that commit,
toolchain stability only), wt-exp1, wt-exp2, wt-exp-sensory (moved
since 0221pdt; pinned likewise), origin-tnn-native-lab-rt (c3f2261d to
7aad68fad at run start; the 7aad68fad state is merged into the
task-pinned HEAD as its second parent and tested by this entry).

Fixture: the 20 older archive branches, arch-wave-20260926-2321pdt
(renamed branch, same commit 004616f65 as 0221pdt's
arch-20260926-2321pdt entry), wave-debate-session-1-backup,
rh-tnn-native-lab-live-tip (superseded tip, see note), rh-main
(unchanged; P20 gap stays closed), rh-fs-gr1, rh-r2-7,
rh-reorg-phase-0-1, rh-wg-freeze, rh-pull-1-head, rh-pull-2-head,
rh-pull-3-head, the 7 forktest worktrees, and the 3 wave3 worktrees
(all unchanged SHAs).

All duplicates named explicitly with SHAs (P8):
- exp1 and wt-exp1 each test the same commit:
  1010a63c3c1cc3f3724f6cf0ca55decc08207a2d (run-start pinned; workers
  are implementing in these branches concurrently, so mid-run tip
  movement cannot have affected the results).
- exp2 and wt-exp2 each test the same commit:
  a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 (same pinned-commit caveat).
- exp-sensory and wt-exp-sensory each test the same commit:
  c368b8e1ffecec2f9061011f5d7c0e3e68675e0a (same pinned-commit caveat).
- origin-tnn-native-lab-rt tests the same commit as the run-start
  merge's second parent (the merged upstream state, CLOSED content):
  7aad68fadb709e6c7700f03d380be9f09b965b80.
- arch-20260927-0221pdt tests the same commit as the run-start merge's
  first parent: 463b115b69e280da0d7f6da15c6ded2f3f610809.
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
| local-tnn-native-lab (task-pinned run-start HEAD) | ecbe9b5b7527d6eb4a10fef19adca2b138462d1d | PASS | live |
| arch-20260927-0221pdt (tnn-native-lab-wave-archive-20260927-0221pdt) | 463b115b69e280da0d7f6da15c6ded2f3f610809 | PASS | live; newly enumerated; first parent of run-start merge |
| exp1 (wave-20260927-0221pdt-exp1, pinned) | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | PASS | live; moved; duplicate of wt-exp1; pinned at run start |
| exp2 (wave-20260927-0221pdt-exp2, pinned) | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | PASS | live; moved; duplicate of wt-exp2; pinned at run start |
| exp-sensory (wave-20260927-0221pdt-sensory, pinned) | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | PASS | live; moved; duplicate of wt-exp-sensory; pinned at run start |
| wt-exp1 (pinned) | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | PASS | live; moved; duplicate of exp1; pinned at run start |
| wt-exp2 (pinned) | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | PASS | live; moved; duplicate of exp2; pinned at run start |
| wt-exp-sensory (pinned) | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | PASS | live; moved; duplicate of exp-sensory; pinned at run start |
| origin-tnn-native-lab-rt (remote-tracking, run-start value) | 7aad68fadb709e6c7700f03d380be9f09b965b80 | PASS | live; second parent of run-start merge |
| rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | PASS | fixture; superseded tip, ref kept pinned |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | PASS | fixture; P20 gap stays closed |
| rh-fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | PASS | fixture |
| rh-r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | PASS | fixture |
| rh-reorg-phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture |
| rh-wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | PASS | fixture |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FAIL | extraction failure: no toolchain path in tree |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FAIL | extraction failure: no toolchain path in tree |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | PASS | fixture; duplicate of rh-reorg-phase-0-1 |
| arch-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | PASS | fixture; dry-run entry, RESULT byte-identical to 0221pdt evidence, kept |
| arch-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | PASS | fixture |
| arch-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | PASS | fixture |
| arch-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | PASS | fixture |
| arch-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | PASS | fixture |
| arch-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | PASS | fixture |
| arch-20260926-2021pdt | 5ba241235482610f1c8f538d97ca0462164b4014 | PASS | fixture |
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
| arch-wave-20260926-2321pdt | 004616f657165191c0d0e89d91fc10a99edd2d6e | PASS | fixture; renamed branch (was arch-20260926-2321pdt in 0221pdt), same commit |
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

## Uniform battery evidence (all 47 PASS runs)

Verified across all 47 per-entry evidence files (grepped, not sampled):

- znc pin: every extracted znc sha256 =
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (47/47; byte-identical toolchain on every tested fork, no divergence).
- probe source sha: every extracted znc_probe.zag sha256 =
  3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
  (47/47).
- B1: compile exit 0, run exit 0, stdout byte-identical to
  FORKBATTERY-OK 42 (47/47); run sha256
  5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066.
- B2: rerun stdout identical; recompile byte-identical; bin sha256
  75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
  on all 47 (matches the frozen value; parsed by tokenizing the
  harness output on whitespace first, never by splitting a packed
  line on '=').
- B3: strict check exit 0 (47/47).
- NEG1: fails as required on 47/47: driver compile exit 1, check exit 1,
  and the fork's own znc reports E0002 on the neg1 source on all 47.
- NEG2: fails as required on 47/47: compile exit 0, check exit 0,
  run exit 0, stdout "WRONG OUTPUT" which differs from expected at
  char 1 ("F" vs "W").
- Fork-tree test: tree probe compiles with the fork's own znc, exit 0,
  run exit 0, stdout R32_ZNC_PROBE_OK, on 47/47.
- Pure-Zag harness: VERDICT=PASS, exit 0, on 47/47 (B1 PASS, B2 PASS,
  B3 PASS, both negative controls failing as required); VERDICT=FAIL
  on 0.

## Failure analysis

pull/1/head and pull/2/head: extraction failures at the first step,
identical to the 2321pdt, 2021pdt, 1721pdt, 1421pdt, 1121pdt, 0821pdt,
0521pdt, and 0221pdt waves: `git show <commit>:src/tools/toolchain/znc_linux_x86_64_abed8aa1`
fails ("exists on disk, but not in '<commit>'" in both cases). The probe
path `src/tools/toolchain/znc_probe.zag` is likewise absent in both
trees. Their tree roots hold non-TNN research documents; they carry no
src/ directory and no toolchain. This is a property of those forks'
contents, not a toolchain regression. They remain untestable by this
battery until their trees gain the pinned toolchain path.

rh-main (27a4271f): P20 coverage gap stays closed. Its commit object is
in the local store from the 0221pdt fetch; the pinned znc extracted
cleanly with the pin verified, and the full battery passes (47/47
uniform evidence).

## P19 coverage-delta accounting vs 0221pdt

0221pdt reported 48 named entries, 46 PASS / 2 extraction FAIL / 0
CONFIRM, 35 unique commits, 10 live entries / 5 unique live commits, 38
fixtures. This wave reports 49 named entries, 47 PASS / 2 extraction
FAIL / 0 CONFIRM, 39 unique commits, 9 live entries / 6 unique live
commits, 40 fixtures.

- Named entries 48 to 49: +1 newly enumerated archive branch
  (tnn-native-lab-wave-archive-20260927-0221pdt at 463b115b6, the first
  parent of the run-start merge). The plain-named archive branch
  tnn-native-lab-wave-archive-20260926-2321pdt known from 0221pdt no
  longer exists; the same commit 004616f65 is now tipped by
  tnn-native-lab-wave-archive-wave-20260926-2321pdt, so the entry was
  renamed arch-20260926-2321pdt to arch-wave-20260926-2321pdt: same
  commit, continuous coverage, count-neutral.
- Live entries 10 to 9: the continuing live entries local-tnn-native-lab
  (moved af657c8e5 to ecbe9b5b7), origin-tnn-native-lab-rt (moved c3f2261d
  to 7aad68fad), exp1, exp2, exp-sensory, wt-exp1, wt-exp2, wt-exp-sensory
  (all moved since 0221pdt, tested at run-start pinned commits), plus the
  newly enumerated arch-20260927-0221pdt. No longer live: rh-main and
  rh-tnn-native-lab-live-tip (both unchanged SHAs, now fixtures; the
  live origin tip is 7aad68fad, covered by origin-tnn-native-lab-rt).
- Extraction FAILs stay at 2: the same expected pull-head FAILs,
  unchanged cause.
- CONFIRM stays at 0: no new coverage gaps.
- Unique commits 35 to 39: +6 new (ecbe9b5b7, 463b115b6, 1010a63c3,
  a2a36e657, c368b8e1f, 7aad68fad) minus 2 no longer tested (af657c8e5,
  c3f2261d).

## Incidents

- None this wave. The single-entry dry run passed clean before the
  batch (no parser incident); its RESULT.txt is byte-identical to the
  0221pdt evidence for that entry, so its evidence dir was kept as the
  arch-20260923-2321pdt archive entry; no bogus evidence dirs were
  created and none were deleted.
- The authorized read-only fetches created three new local refs:
  refs/remotes/rh-pull-1-head (at
  5802fec8401f28b4036b0dd5ebb23905610cab57), refs/remotes/rh-pull-2-head
  (at 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba), and
  refs/remotes/rh-pull-3-head (at
  9914322267e1358e5542a23c72ec51d1a9ae43df). No existing ref moved
  under this run: the remote-tracking ref origin/tnn-native-lab was
  already at 7aad68fad after the task-authorized fetch at run start,
  and local HEAD did not move during this run (ecbe9b5b7 at start and
  at close). The wave lock was not touched.
- The three experimental worker branches (exp1, exp2, exp-sensory) are
  under concurrent implementation by other workers; this battery tested
  only the run-start pinned commits (1010a63c3, a2a36e657, c368b8e1f)
  via read-only git show, so mid-write branch state cannot have
  affected the results. Each RESULT.txt pins the tested commit.

## Scratch space

/tmp/fb0521 at run end holds the pinned znc copy (znc_build, deleted
before handoff), the extracted harness source, the rebuilt harness
binary, the run log, the entries list, the ls-remote start/end
captures, and the driver script (about 9M total). Per-entry znc copies
were deleted right after each entry's evidence was complete (0 znc.bin
files remain in the evidence tree).

## Closing tip re-check

Run-start origin tips (read-only `git ls-remote origin`):
tnn-native-lab 7aad68fadb709e6c7700f03d380be9f09b965b80, main
27a4271f208247a1e9c24cca35468c298b6cd29d.
Closing origin tips (read-only `git ls-remote origin`): identical
values.

The tips did not move during this run. The live tnn-native-lab tip
7aad68fad was tested by this battery via the origin-tnn-native-lab-rt
entry and is merged into the task-pinned run-start HEAD (second
parent). The merged first parent 463b115b6 was tested via the
arch-20260927-0221pdt entry. The main tip 27a4271f was tested via the
rh-main entry. Nothing arrived after the testing window.

## Local HEAD

Task-pinned run-start HEAD:
ecbe9b5b7527d6eb4a10fef19adca2b138462d1d.
HEAD at run end: ecbe9b5b7527d6eb4a10fef19adca2b138462d1d. Local HEAD
did not move during this run. The tested local entry is the task-pinned
run-start HEAD. This worker wrote only new files (this report, the
enumeration manifest, plus the 49 per-entry evidence dirs); it modified
no tracked files, made no commits, and pushed nothing.

## Zero-Python attestation

Zero Python ran in this worker's work. Everything was done with:
POSIX shell (battery driver, orchestration, and summary), git
(read-only rev-parse, branch, for-each-ref, ls-remote, show, worktree
list, cat-file, log; plus the task-authorized read-only fetches for
the pull-head refs; no checkout, no pull, no push), sha256sum, grep,
awk, cut, sed, cmp, head, tr, the pinned znc binary, and the rebuilt
pure-Zag harness fork_battery. No Python was used for the battery, the
harness build, extraction, any analysis, or any verification step.

## Evidence archive note (P14)

The 49 per-entry evidence dirs were moved (not copied) from
/tmp/fb0521/E into
docs/lab/rsi/runs/wave-20260927-0521pdt/forks/evidence/. Each PASS dir
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

## Proposed verdict line

CONFIRM fork battery [RE-CERT]: 49 named, 47 PASS, 2 extraction FAIL,
0 CONFIRM (toolchain stability only; pull-head FAILs are the expected
non-TNN research-doc trees, unchanged cause eight waves running).
