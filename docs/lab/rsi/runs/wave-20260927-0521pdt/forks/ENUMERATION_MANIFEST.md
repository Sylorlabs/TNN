# Enumeration manifest, wave-20260927-0521pdt fork battery

Frozen enumeration for this wave (drafted per the queued P19 manifest task).
Enumerated fresh at run start on 2026-09-27, from working copy
~/workspace/tnn-rsi on branch tnn-native-lab at run-start HEAD
ecbe9b5b7527d6eb4a10fef19adca2b138462d1d.

Enumeration method:
- `git for-each-ref` for local branches and remote-tracking refs,
  after one task-authorized read-only `git fetch --all` at run start.
- `git ls-remote origin` at run start and at close (tips compared for P1/P8).
- `git worktree list` for worktrees (15, SHAs re-verified).
- Pull-head refs fetched read-only into refs/remotes/rh-pull-N-head
  during this run so all three are named and testable.

Classification rule (same as prior waves): Live = entry whose HEAD moved
since last wave, or newly enumerated this wave, or newly testable this
wave. Fixture = unchanged-SHA entries tested for coverage.

Run-start remote tips (ls-remote, unchanged at close): tnn-native-lab
7aad68fadb709e6c7700f03d380be9f09b965b80, main
27a4271f208247a1e9c24cca35468c298b6cd29d.

## Named entries (49)

| entry | ref | commit | class |
|---|---|---|---|
| local-tnn-native-lab | refs/heads/tnn-native-lab | ecbe9b5b7527d6eb4a10fef19adca2b138462d1d | LIVE (moved: af657c8e5 -> ecbe9b5b7; task-pinned run-start HEAD) |
| arch-20260927-0221pdt | refs/heads/tnn-native-lab-wave-archive-20260927-0221pdt | 463b115b69e280da0d7f6da15c6ded2f3f610809 | LIVE (newly enumerated; first parent of run-start merge) |
| exp1 | refs/heads/wave-20260927-0221pdt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | LIVE (moved; tested at run-start pinned commit, read-only git show, toolchain stability only) |
| exp2 | refs/heads/wave-20260927-0221pdt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | LIVE (moved; pinned at run start) |
| exp-sensory | refs/heads/wave-20260927-0221pdt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | LIVE (moved; pinned at run start) |
| wt-exp1 | worktree ~/workspace/tnn-rsi-wt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | LIVE (moved; pinned at run start) |
| wt-exp2 | worktree ~/workspace/tnn-rsi-wt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | LIVE (moved; pinned at run start) |
| wt-exp-sensory | worktree ~/workspace/tnn-rsi-wt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | LIVE (moved; pinned at run start) |
| origin-tnn-native-lab-rt | refs/remotes/origin/tnn-native-lab | 7aad68fadb709e6c7700f03d380be9f09b965b80 | LIVE (moved: c3f2261d -> 7aad68fad; second parent of run-start merge) |
| rh-tnn-native-lab-live-tip | refs/remotes/rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | FIXTURE (unchanged; superseded tip: live origin tip is now 7aad68fad, covered by origin-tnn-native-lab-rt; ref kept pinned for coverage of this commit) |
| rh-main | refs/remotes/rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | FIXTURE (unchanged; was live/newly-testable in 0221pdt, P20 gap stays closed) |
| rh-fs-gr1 | origin refs/heads/fs-gr1 | 23f6c0f9012887448a83edbe9060b73e13d5a7a5 | FIXTURE |
| rh-r2-7 | origin refs/heads/r2-7 | 2d99d183f693145c53213639990a3474ff786b69 | FIXTURE |
| rh-reorg-phase-0-1 | origin refs/heads/reorg/phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | FIXTURE |
| rh-wg-freeze | origin refs/heads/wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | FIXTURE |
| rh-pull-1-head | refs/remotes/rh-pull-1-head (origin refs/pull/1/head) | 5802fec8401f28b4036b0dd5ebb23905610cab57 | FIXTURE (expected extraction FAIL) |
| rh-pull-2-head | refs/remotes/rh-pull-2-head (origin refs/pull/2/head) | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | FIXTURE (expected extraction FAIL) |
| rh-pull-3-head | refs/remotes/rh-pull-3-head (origin refs/pull/3/head) | 9914322267e1358e5542a23c72ec51d1a9ae43df | FIXTURE |
| arch-20260923-2321pdt | refs/heads/tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | FIXTURE |
| arch-20260924-0221pdt | refs/heads/tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | FIXTURE |
| arch-20260924-0521pdt | refs/heads/tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | FIXTURE |
| arch-20260924-1121pdt | refs/heads/tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | FIXTURE |
| arch-20260924-1421pdt | refs/heads/tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | FIXTURE |
| arch-20260924-1721pdt | refs/heads/tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | FIXTURE |
| arch-20260926-2021pdt | refs/heads/tnn-native-lab-wave-archive-20260926-2021pdt | 5ba241235482610f1c8f538d97ca0462164b4014 | FIXTURE |
| arch-wave-20260924-1721pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | FIXTURE |
| arch-wave-20260924-2321pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | FIXTURE |
| arch-wave-20260925-0221pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | FIXTURE |
| arch-wave-20260925-0521pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | FIXTURE |
| arch-wave-20260925-0821pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | FIXTURE |
| arch-wave-20260925-1121pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | FIXTURE |
| arch-wave-20260925-1421pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | FIXTURE |
| arch-wave-20260926-0521pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | FIXTURE |
| arch-wave-20260926-0821pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a | FIXTURE |
| arch-wave-20260926-1121pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260926-1121pdt | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d | FIXTURE |
| arch-wave-20260926-1421pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260926-1421pdt | a222f8f178049b9aeee3b053328c59e9b6fd813d | FIXTURE |
| arch-wave-20260926-1721pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260926-1721pdt | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a | FIXTURE |
| arch-wave-20260926-2321pdt | refs/heads/tnn-native-lab-wave-archive-wave-20260926-2321pdt | 004616f657165191c0d0e89d91fc10a99edd2d6e | FIXTURE (renamed branch: 0221pdt knew it as tnn-native-lab-wave-archive-20260926-2321pdt; same commit, count-neutral) |
| wave-debate-session-1-backup | refs/heads/wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | FIXTURE |
| wt-forktest-main | worktree ~/workspace/tnn-rsi-wave3/forktest/main | 293602fb1d4a2fd5d680a3376463d61b0572006b | FIXTURE |
| wt-forktest-r2-7 | worktree ~/workspace/tnn-rsi-wave3/forktest/r2-7 | a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5 | FIXTURE |
| wt-forktest-reorg | worktree ~/workspace/tnn-rsi-wave3/forktest/reorg_phase-0-1 | 9914322267e1358e5542a23c72ec51d1a9ae43df | FIXTURE |
| wt-forktest-tnn-native-lab | worktree ~/workspace/tnn-rsi-wave3/forktest/tnn-native-lab | bd30978748fa83bbea6e423a7074cf32b7304291 | FIXTURE |
| wt-forktest-tnn-native-lab-remote | worktree ~/workspace/tnn-rsi-wave3/forktest/tnn-native-lab-remote | cea8db22f53ed1294aff5324aa143bd6d1df845e | FIXTURE |
| wt-forktest-debate-backup | worktree ~/workspace/tnn-rsi-wave3/forktest/wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | FIXTURE |
| wt-forktest-wg-freeze | worktree ~/workspace/tnn-rsi-wave3/forktest/wg-freeze | f875b34179f570ba1ad555262cd401ddc4a52848 | FIXTURE |
| wt-wave3-probe | worktree ~/workspace/tnn-rsi-wave3/probe | bd30978748fa83bbea6e423a7074cf32b7304291 | FIXTURE |
| wt-wave3-senses | worktree ~/workspace/tnn-rsi-wave3/senses | bd30978748fa83bbea6e423a7074cf32b7304291 | FIXTURE |
| wt-wave3-trades | worktree ~/workspace/tnn-rsi-wave3/trades | bd30978748fa83bbea6e423a7074cf32b7304291 | FIXTURE |

Counts: 49 named entries, 9 live, 40 fixture, 39 unique commits,
6 unique live commits.

## Duplicate commits (named explicitly, P8)

- exp1, wt-exp1: 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d
- exp2, wt-exp2: a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4
- exp-sensory, wt-exp-sensory: c368b8e1ffecec2f9061011f5d7c0e3e68675e0a
- origin-tnn-native-lab-rt: 7aad68fadb709e6c7700f03d380be9f09b965b80 = run-start merge ecbe9b5b7's second parent
- arch-20260927-0221pdt: 463b115b69e280da0d7f6da15c6ded2f3f610809 = run-start merge ecbe9b5b7's first parent
- rh-reorg-phase-0-1, rh-pull-3-head, wt-forktest-reorg: 9914322267e1358e5542a23c72ec51d1a9ae43df
- wave-debate-session-1-backup, wt-forktest-debate-backup: 3947dca1a77c00818575dbc7476556c8278b8b7b
- rh-wg-freeze, wt-forktest-wg-freeze: f875b34179f570ba1ad555262cd401ddc4a52848
- wt-forktest-tnn-native-lab, wt-wave3-probe, wt-wave3-senses, wt-wave3-trades: bd30978748fa83bbea6e423a7074cf32b7304291
