# Enumeration manifest, wave-20260927-1721pdt

Fork-battery worker (lane 2). Run start: 2026-09-27 ~17:21 PDT.
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Run-start HEAD (task-pinned): f55e8c27ae2df6cc0db572372f5d50a4e3fc032f
("Merge remote-tracking branch 'origin/tnn-native-lab' into tnn-native-lab").
Read-only git throughout (rev-parse, for-each-ref, ls-remote, show,
worktree list; no checkout, no pull, no push, no fetch, no reset).
The wave lock was not touched.

Enumerated fresh at run start via `git for-each-ref`,
`git worktree list`, and read-only `git ls-remote origin` (start values
captured; re-checked at close).

Classification rule (same as prior waves): Live = entry whose HEAD moved
since last wave, or newly enumerated this wave, or newly testable this
wave. Fixture = unchanged-SHA entries tested for coverage.

## Local branches (30)

| ref | tip (full sha) | class | notes |
|---|---|---|---|
| tnn-native-lab | f55e8c27ae2df6cc0db572372f5d50a4e3fc032f | live | moved b876016e6 to f55e8c27a since 1421pdt; tested as local-tnn-native-lab |
| tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | fixture | arch-20260923-2321pdt; also the dry-run entry |
| tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | fixture | arch-20260924-0221pdt |
| tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | fixture | arch-20260924-0521pdt |
| tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | fixture | arch-20260924-1121pdt |
| tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | fixture | arch-20260924-1421pdt |
| tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | fixture | arch-20260924-1721pdt |
| tnn-native-lab-wave-archive-20260926-2021pdt | 5ba241235482610f1c8f538d97ca0462164b4014 | fixture | arch-20260926-2021pdt |
| tnn-native-lab-wave-archive-20260927-0221pdt | 463b115b69e280da0d7f6da15c6ded2f3f610809 | fixture | arch-20260927-0221pdt |
| tnn-native-lab-wave-archive-20260927-0521pdt | 80c40a7afc0231493e0f1f46540a6dbe60c60c3f | fixture | arch-20260927-0521pdt |
| tnn-native-lab-wave-archive-20260927-1421pdt | 8929cdd93df7efeb8b67320d5a7d67e2d6bed467 | live | NEW this wave; tested first in the batch as arch-20260927-1421pdt |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | fixture | arch-wave-20260924-1721pdt |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | fixture | arch-wave-20260924-2321pdt |
| tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | fixture | arch-wave-20260925-0221pdt |
| tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | fixture | arch-wave-20260925-0521pdt |
| tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | fixture | arch-wave-20260925-0821pdt |
| tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | fixture | arch-wave-20260925-1121pdt |
| tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | fixture | arch-wave-20260925-1421pdt |
| tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | fixture | arch-wave-20260926-0521pdt |
| tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a | fixture | arch-wave-20260926-0821pdt |
| tnn-native-lab-wave-archive-wave-20260926-1121pdt | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d | fixture | arch-wave-20260926-1121pdt |
| tnn-native-lab-wave-archive-wave-20260926-1421pdt | a222f8f178049b9aeee3b053328c59e9b6fd813d | fixture | arch-wave-20260926-1421pdt |
| tnn-native-lab-wave-archive-wave-20260926-1721pdt | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a | fixture | arch-wave-20260926-1721pdt |
| tnn-native-lab-wave-archive-wave-20260926-2321pdt | 004616f657165191c0d0e89d91fc10a99edd2d6e | fixture | arch-wave-20260926-2321pdt |
| tnn-native-lab-wave-archive-wave-20260927-0821pdt | e9373dad1aca4a694cf39d023e7756312e125ba7 | fixture | arch-wave-20260927-0821pdt |
| tnn-native-lab-wave-archive-wave-20260927-1121pdt | 4805f5363a0dba762abf2d35e8ab8284abce6731 | fixture | arch-wave-20260927-1121pdt |
| wave-20260927-0221pdt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | fixture | exp1; pinned commit; duplicate of wt-exp1 |
| wave-20260927-0221pdt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | fixture | exp2; pinned commit; duplicate of wt-exp2 |
| wave-20260927-0221pdt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | fixture | exp-sensory; pinned commit; duplicate of wt-exp-sensory |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | fixture | duplicate of wt-forktest-debate-backup |

## Local remote-tracking refs (6, no fetch this wave)

| ref | tip | notes |
|---|---|---|
| refs/remotes/origin/tnn-native-lab | d09d5bfdeccc7a4007e996ac4757cef6af4845fe | stale vs live remote tip (see below); tested as origin-tnn-native-lab-rt |
| refs/remotes/rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | tested as rh-main |
| refs/remotes/rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | tested as rh-pull-1-head |
| refs/remotes/rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | tested as rh-pull-2-head |
| refs/remotes/rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | tested as rh-pull-3-head |
| refs/remotes/rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | pinned superseded tip; tested as fixture |

Note: the 1121pdt/1421pdt-era refs refs/remotes/rh-fs-gr1,
refs/remotes/rh-r2-7, refs/remotes/rh-reorg-phase-0-1, and
refs/remotes/rh-wg-freeze no longer exist as refs, but their commits
remain in the local object store and are tested by SHA as
rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1, rh-wg-freeze (same as the
1421pdt entries).

## Remote heads via ls-remote origin (run start, re-confirmed at close)

| head | tip | entry |
|---|---|---|
| fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | rh-fs-gr1 (fixture) |
| main | 27a4271f208247a1e9c24cca35468c298b6cd29d | rh-main (fixture; P20 gap stays closed) |
| r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | rh-r2-7 (fixture) |
| reorg/phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | rh-reorg-phase-0-1 (fixture; duplicate of rh-pull-3-head and wt-forktest-reorg) |
| tnn-native-lab | f71ff91f66bc672d01f8b0a9544cf1067e465d90 | origin-tnn-native-lab-live (live; moved 9beb0ade to f71ff91f since 1421pdt; commit object NOT in local store, no fetch authorized: UNTESTABLE, content unverifiable read-only) |
| wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | rh-wg-freeze (fixture; duplicate of wt-forktest-wg-freeze) |
| pull/1/head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | rh-pull-1-head (UNTESTABLE; toolchain path absent) |
| pull/2/head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | rh-pull-2-head (UNTESTABLE; toolchain path absent) |
| pull/3/head | 9914322267e1358e5542a23c72ec51d1a9ae43df | rh-pull-3-head (fixture; duplicate) |

Run-start remote tips (ls-remote, unchanged at close): tnn-native-lab
f71ff91f66bc672d01f8b0a9544cf1067e465d90 (moved from 9beb0ade),
main 27a4271f208247a1e9c24cca35468c298b6cd29d, fs-gr1
23f6c0f9012887448a83edbe9060b73e13d5a7a5, r2-7
2d99d183f693145c53213639990a3474ff786b69, reorg/phase-0-1
9914322267e1358e5542a23c72ec51d1a9ae43df, wg-freeze
f875b34179f570ba1ad555262cd401ddc4a52848, pull/1/head
5802fec8401f28b4036b0dd5ebb23905610cab57, pull/2/head
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba, pull/3/head
9914322267e1358e5542a23c72ec51d1a9ae43df.

Delta note: the local remote-tracking ref refs/remotes/origin/tnn-native-lab
still points at d09d5bfdeccc7a4007e996ac4757cef6af4845fe (the merge
parent), while the live origin tip via ls-remote is already
f71ff91f66bc672d01f8b0a9544cf1067e465d90. Both are enumerated and
tested/accounted this wave: origin-tnn-native-lab-rt at d09d5bfde
(UNTESTABLE, toolchain path absent) and origin-tnn-native-lab-live at
f71ff91f (UNTESTABLE, object not in local store). No coverage gap on
either value.

## Worktrees (13, SHAs re-verified at run start; all unchanged since 1421pdt)

| worktree path | commit | entry |
|---|---|---|
| ~/workspace/tnn-rsi-wave3/forktest/main | 293602fb1d4a2fd5d680a3376463d61b0572006b | wt-forktest-main (fixture) |
| ~/workspace/tnn-rsi-wave3/forktest/r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | wt-forktest-r2-7 (fixture) |
| ~/workspace/tnn-rsi-wave3/forktest/reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | wt-forktest-reorg (fixture; duplicate) |
| ~/workspace/tnn-rsi-wave3/forktest/tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | wt-forktest-tnn-native-lab (fixture; duplicate of wt-wave3-probe/senses/trades) |
| ~/workspace/tnn-rsi-wave3/forktest/tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | wt-forktest-tnn-native-lab-remote (fixture) |
| ~/workspace/tnn-rsi-wave3/forktest/wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | wt-forktest-debate-backup (fixture; duplicate) |
| ~/workspace/tnn-rsi-wave3/forktest/wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | wt-forktest-wg-freeze (fixture; duplicate) |
| ~/workspace/tnn-rsi-wave3/probe | bd30978748fa83bbea6e423a7074cf32b7304291 | wt-wave3-probe (fixture; duplicate) |
| ~/workspace/tnn-rsi-wave3/senses | bd30978748fa83bbea6e423a7074cf32b7304291 | wt-wave3-senses (fixture; duplicate) |
| ~/workspace/tnn-rsi-wave3/trades | bd30978748fa83bbea6e423a7074cf32b7304291 | wt-wave3-trades (fixture; duplicate) |
| ~/workspace/tnn-rsi-wt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | wt-exp1 (fixture; pinned; duplicate of exp1) |
| ~/workspace/tnn-rsi-wt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | wt-exp2 (fixture; pinned; duplicate of exp2) |
| ~/workspace/tnn-rsi-wt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | wt-exp-sensory (fixture; pinned; duplicate of exp-sensory) |

All worktree entries were tested at their pinned commits via read-only
git show; worktree working trees were not entered.

## Totals

Named battery entries: 54 (30 local branch entries, 11 remote entries,
13 worktree entries). Live: 4 (arch-20260927-1421pdt,
local-tnn-native-lab, origin-tnn-native-lab-rt,
origin-tnn-native-lab-live). Fixture: 50.

Manifest drift vs wave-20260927-1421pdt frozen baseline (52 entries):
- New branch: tnn-native-lab-wave-archive-20260927-1421pdt at
  8929cdd93df7efeb8b67320d5a7d67e2d6bed467.
- local-tnn-native-lab moved: b876016e6 to f55e8c27a.
- origin-tnn-native-lab moved (ls-remote): 9beb0ade to
  f71ff91f66bc672d01f8b0a9544cf1067e465d90. The local
  remote-tracking ref sits at d09d5bfdeccc7a4007e996ac4757cef6af4845fe
  (the merge parent), covered by origin-tnn-native-lab-rt.
- No missing branches: every other branch, remote-tracking ref, and
  worktree from the 1421pdt baseline is present with unchanged SHAs.
- Remote tips identical at close (fs-gr1, main, r2-7, reorg/phase-0-1,
  wg-freeze, pull/1, pull/2, pull/3 heads unchanged).
- The 4 stale rh-* refs (rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1,
  rh-wg-freeze) were already absent as refs at 1421pdt-close; their
  commits remain in the local object store and are tested by SHA.
- 13 worktrees present, SHAs re-verified, all unchanged.

See FORK_RESULTS_1721.md for the per-entry verdicts and the drift
accounting.
