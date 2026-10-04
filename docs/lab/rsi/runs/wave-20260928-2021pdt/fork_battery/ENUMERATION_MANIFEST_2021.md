# Enumeration Manifest: wave-20260928-2021pdt

Date: 2026-09-28. Battery driver: fork_battery/batch_2021.sh (frozen
driver, live entries updated; fixture SHAs unchanged from 1421pdt).

Run-start pin (task-pinned HEAD): 4340126e6c1cd3f03dbc653ee1f585a741fff806.

## Local branch enumeration (34 refs, git for-each-ref)

tnn-native-lab 4340126e6; 32 archive branches (16 plain
`tnn-native-lab-wave-archive-<date>`, 16 wave-prefixed
`tnn-native-lab-wave-archive-wave-<date>`); wave-20260927-0221pdt-exp1
1010a63c3; wave-20260927-0221pdt-exp2 a2a36e657; wave-20260927-0221pdt-sensory
c368b8e1f; wave-debate-session-1-backup 3947dca1a.

New local ref since the 1421pdt enumeration: exactly one,
`tnn-native-lab-wave-archive-wave-20260928-1721pdt` (4340126e6), created
by the 1721pdt wave as its archive pointer. It is this wave's LIVE
archive entry, pinned at the current tip.

## Remote ref enumeration (6 refs)

origin/tnn-native-lab bedf8b4a (ls-remote at wave start, unchanged);
rh-main 27a4271f2; rh-pull-1-head 5802fec84; rh-pull-2-head 4b76bb59f;
rh-pull-3-head 991432226; rh-tnn-native-lab-live-tip b257c02cc. All
pins unchanged since the 1421pdt wave.

## Battery entries: 60 named

- LIVE this wave: arch-wave-20260928-1721pdt (4340126e6, the newly
  enumerated archive) and local-tnn-native-lab (4340126e6, the
  task-pinned run-start commit). Both certify the current tip.
- Fixture: all 58 remaining entries at 1421pdt-pinned SHAs (32 local
  archives including 0829pdt, 3 experimental branches, the debate
  backup, 6 remote heads, 6 worktrees, and the fixture-side copies of
  the archive entries).

Pin divergence check: every fixture SHA resolves identically in the
current tree; the two UNTESTABLE entries from 1421pdt
(rh-pull-1-head 5802fec8, rh-pull-2-head 4b76bb59, non-TNN research-doc
trees) are expected to repeat.
