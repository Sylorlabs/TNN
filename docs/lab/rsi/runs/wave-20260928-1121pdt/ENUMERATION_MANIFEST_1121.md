# Enumeration manifest, wave-20260928-1121pdt

Fork-battery lane. Working copy: ~/workspace/tnn-rsi, branch
tnn-native-lab, run-start HEAD 81f0cfe12c614fef83faab91bef676441e679833
("wave-20260928-0829pdt: LOOP_STATE verdicts (battery CONFIRM 56/58 at
pin; design NULLs; EXP1c stand-down; survey NONE; commit-order VALID
VACUOUS; FIT staleness 2/8)"). Enumeration run start: 2026-09-28 11:24 PDT.

Pinned-commit discipline (mandatory this wave): every entry extracted
read only at its run-start-pinned SHA, never at a live ref. Mid-run
lane commits are inert by construction. Read-only git throughout
(rev-parse, for-each-ref, ls-remote, show, worktree list, log,
ls-tree; fetch origin ran once before enumeration; no checkout, no
pull, no push, no reset). The wave lock was not touched.

Classification rule (same as prior waves): Live = entry whose HEAD
moved since the last executed battery, or newly enumerated this wave,
or newly testable this wave. Fixture = unchanged-SHA entries tested
for coverage.

## Local branches (34)

tnn-native-lab at 81f0cfe12c614fef83faab91bef676441e679833: LIVE.
Run-start pin; tip moved 9f3827356 to 81f0cfe12 since the last
executed battery (wave-20260928-0829pdt, pin 9f3827356). The three
loop record commits between pins (a14285aef, 476ce15da, 81f0cfe12)
are loop documentation only; a14285aef and 476ce15da are ancestors
of the pin and are covered by the tip test per the scope stamp.

tnn-native-lab-wave-archive-wave-20260928-0829pdt at
81f0cfe12c614fef83faab91bef676441e679833: LIVE (newly enumerated
this wave; post-0829pdt parent archive tag). Honest-treatment note:
its tip is byte-identical to the live run-start pin, so its battery
entry shares the live commit. It is tested as its own named entry
per the duplicate naming rule; it adds no new commit coverage.

All 32 remaining local branches: fixture, unchanged SHAs vs the
0829pdt manifest (listed below; every SHA re-verified byte-equal to
the 0829pdt pins).

| entry | branch | tip |
|---|---|---|
| arch-20260923-2321pdt | tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 |
| arch-20260924-0221pdt | tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 |
| arch-20260924-0521pdt | tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af |
| arch-20260924-1121pdt | tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 |
| arch-20260924-1421pdt | tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f |
| arch-20260924-1721pdt | tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 |
| arch-20260926-2021pdt | tnn-native-lab-wave-archive-20260926-2021pdt | 5ba241235482610f1c8f538d97ca0462164b4014 |
| arch-20260927-0221pdt | tnn-native-lab-wave-archive-20260927-0221pdt | 463b115b69e280da0d7f6da15c6ded2f3f610809 |
| arch-20260927-0521pdt | tnn-native-lab-wave-archive-20260927-0521pdt | 80c40a7afc0231493e0f1f46540a6dbe60c60c3f |
| arch-20260927-1421pdt | tnn-native-lab-wave-archive-20260927-1421pdt | 8929cdd93df7efeb8b67320d5a7d67e2d6bed467 |
| arch-wave-20260924-1721pdt | tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 |
| arch-wave-20260924-2321pdt | tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 |
| arch-wave-20260925-0221pdt | tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f |
| arch-wave-20260925-0521pdt | tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a |
| arch-wave-20260925-0821pdt | tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d |
| arch-wave-20260925-1121pdt | tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba |
| arch-wave-20260925-1421pdt | tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 |
| arch-wave-20260926-0521pdt | tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 |
| arch-wave-20260926-0821pdt | tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a |
| arch-wave-20260926-1121pdt | tnn-native-lab-wave-archive-wave-20260926-1121pdt | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d |
| arch-wave-20260926-1421pdt | tnn-native-lab-wave-archive-wave-20260926-1421pdt | a222f8f178049b9aeee3b053328c59e9b6fd813d |
| arch-wave-20260926-1721pdt | tnn-native-lab-wave-archive-wave-20260926-1721pdt | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a |
| arch-wave-20260926-2321pdt | tnn-native-lab-wave-archive-wave-20260926-2321pdt | 004616f657165191c0d0e89d91fc10a99edd2d6e |
| arch-wave-20260927-0821pdt | tnn-native-lab-wave-archive-wave-20260927-0821pdt | e9373dad1aca4a694cf39d023e7756312e125ba7 |
| arch-wave-20260927-1121pdt | tnn-native-lab-wave-archive-wave-20260927-1121pdt | 4805f5363a0dba762abf2d35e8ab8284abce6731 |
| arch-wave-20260927-1721pdt | tnn-native-lab-wave-archive-wave-20260927-1721pdt | 4042f15bf40b1c73a516ba5eda2a412033db9f6d |
| arch-wave-20260927-2021pdt | tnn-native-lab-wave-archive-wave-20260927-2021pdt | baf48e4744c3c075e3fc70a383f0a77efec83ad7 |
| arch-wave-20260927-2321pdt | tnn-native-lab-wave-archive-wave-20260927-2321pdt | 43f339e60dad44bf5ceccef83962248b7a434256 |
| arch-wave-20260928-0221pdt | tnn-native-lab-wave-archive-wave-20260928-0221pdt | f03aa6fc81b7ed5dd141e393703425c16f65b794 |
| exp1 | wave-20260927-0221pdt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d |
| exp2 | wave-20260927-0221pdt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 |
| exp-sensory | wave-20260927-0221pdt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a |
| wave-debate-session-1-backup | wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b |

arch-wave-20260928-0829pdt is the only new branch since 0829pdt
(a post-wave parent archive tag of the 0829pdt pin). No branch
moved, no branch deleted, no branch renamed.

## Local remote-tracking refs (6)

refs/remotes/origin/tnn-native-lab at bedf8b4aab0110e3c115fb1bca3903551a32577e
(fixture; unchanged since 2021pdt; tested as origin-tnn-native-lab-rt).
refs/remotes/rh-main at 27a4271f208247a1e9c24cca35468c298b6cd29d.
refs/remotes/rh-pull-1-head at 5802fec8401f28b4036b0dd5ebb23905610cab57.
refs/remotes/rh-pull-2-head at 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba.
refs/remotes/rh-pull-3-head at 9914322267e1358e5542a23c72ec51d1a9ae43df.
refs/remotes/rh-tnn-native-lab-live-tip at b257c02cc68b7a1f079dee28611cccd93b6efc9d.

The 4 stale rh-* refs (rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1,
rh-wg-freeze) remain absent as refs; their commits are tested by SHA
as rh-fs-gr1, rh-r2-7, rh-reorg-phase-0-1, rh-wg-freeze (same as 0829pdt).

## Remote heads via ls-remote origin (run start)

fs-gr1 23f6c0f9012887448a83edbe9060b73e13d5a7a5,
main 27a4271f208247a1e9c24cca35468c298b6cd29d,
r2-7 2d99d183f693145c53213639990a3474ff786b69,
reorg/phase-0-1 9914322267e1358e5542a23c72ec51d1a9ae43df,
wg-freeze f875b34179f570ba1ad555262cd401ddc4a52848,
tnn-native-lab bedf8b4aab0110e3c115fb1bca3903551a32577e,
pull/1/head 5802fec8401f28b4036b0dd5ebb23905610cab57,
pull/2/head 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba,
pull/3/head 9914322267e1358e5542a23c72ec51d1a9ae43df.

All remote tips byte-identical to the 0829pdt run-start pins (zero
remote drift; git fetch origin succeeded with no new objects).
Local remote-tracking ref and live ls-remote tip agree at bedf8b4a
(unchanged since 2021pdt). Closing ls-remote re-check at batch close:
see FORK_BATTERY_1121.md.

## Worktrees (13)

Same 13 worktrees as 0829pdt, full SHAs re-verified at run start
(all byte-equal to the 0829pdt pins):
main 293602fb1d4a2fd5d680a3376463d61b0572006b,
r2-7 a0e7f8ba2bf0e32ec5b989cae0838fdcd14d33a5,
reorg_phase-0-1 9914322267e1358e5542a23c72ec51d1a9ae43df,
tnn-native-lab bd30978748fa83bbea6e423a7074cf32b7304291,
tnn-native-lab-remote cea8db22f53ed1294aff5324aa143bd6d1df845e,
wave-debate-session-1-backup 3947dca1a77c00818575dbc7476556c8278b8b7b,
wg-freeze f875b34179f570ba1ad555262cd401ddc4a52848,
probe/senses/trades bd30978748fa83bbea6e423a7074cf32b7304291,
wt-exp1 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d,
wt-exp2 a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4,
wt-exp-sensory c368b8e1ffecec2f9061011f5d7c0e3e68675e0a.
The main worktree is not itself a battery entry; the local entry is
tested at the task-pinned commit 81f0cfe12.

## Totals

Named battery entries: 59. Live: 2 (local-tnn-native-lab at
81f0cfe12, arch-wave-20260928-0829pdt at 81f0cfe12 as newly
enumerated). Fixture: 57.

Drift vs the 0829pdt executed battery: exactly two changes,
local-tnn-native-lab 9f3827356 to 81f0cfe12 (three loop record
commits landed between waves), and the newly enumerated post-0829pdt
archive branch arch-wave-20260928-0829pdt whose tip is byte-identical
to the live pin. No missing, moved, or renamed branches, refs,
worktrees, or remote heads. No remote drift.
