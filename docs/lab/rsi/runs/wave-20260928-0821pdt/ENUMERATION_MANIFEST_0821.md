# Enumeration manifest, wave-20260928-0821pdt

Fork-battery coordinator lane. Run start: 2026-09-28 08:23 PDT.
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Task-pinned run-start commit:
3e76c0fde6b6fa9a217554aac98aa2686cca9da5
("wave-20260928-0521pdt: INCOMPLETE record (runtime failure, lock
cleared, fork-lane evidence ef418824b carried forward)").

Pinned-commit discipline: every extraction at a run-start-pinned SHA,
never at a live ref. Mid-run lane commits are inert by construction.
Read-only git throughout (rev-parse, for-each-ref, ls-remote, show,
worktree list, log, ls-tree; no checkout, no pull, no push, no fetch,
no reset). The wave lock was not touched (the parent agent owns it).

Classification rule (same as prior waves): Live = entry whose HEAD
moved since last wave, or newly enumerated this wave, or newly
testable this wave. Fixture = unchanged-SHA entries carried forward.

## Fresh enumeration versus the 0521 manifest

Fresh `git for-each-ref` at run start: 34 local branches, 6 local
remote-tracking refs. Tip-by-tip diff against ENUMERATION_MANIFEST_0521
(commit ef418824b): 33 of 34 local branch tips byte-identical. The
single moved ref is tnn-native-lab itself (f03aa6fc8 to 3e76c0fde: the
two loop-record commits). No genuinely new branches were enumerated.

Local branches (34): tnn-native-lab at 3e76c0fde (live; the only moved
ref); all 28 tnn-native-lab-wave-archive-* refs at their 0521 tips
(fixture); wave-20260927-0221pdt-exp1 at 1010a63c3c1c (fixture);
wave-20260927-0221pdt-exp2 at a2a36e6571b2 (fixture);
wave-20260927-0221pdt-sensory at c368b8e1ffec (fixture);
wave-debate-session-1-backup at 3947dca1a77c (fixture).

Local remote-tracking refs (6, no fetch this wave): origin/tnn-native-lab
bedf8b4aa, rh-main 27a4271f2, rh-pull-1-head 5802fec84,
rh-pull-2-head 4b76bb59f, rh-pull-3-head 991432226,
rh-tnn-native-lab-live-tip b257c02cc. All unchanged from 0521.

Remote heads via read-only `git ls-remote origin` at run start:
fs-gr1 23f6c0f9, main 27a4271f, r2-7 2d99d183,
reorg/phase-0-1 991432226, tnn-native-lab bedf8b4a, wg-freeze f875b341,
pull/1/head 5802fec8, pull/2/head 4b76bb59, pull/3/head 991432226.
Byte-identical to the 0521 close values. Zero remote movement.

Worktrees: 13 entries enumerated via `git worktree list`; SHAs match
the 0521 manifest except the main worktree's checked-out tip
(f03aa6fc8 to 3e76c0fde between waves, expected).

## Battery plan this wave

One live entry (local-tnn-native-lab at the task pin) tested fresh
with the frozen pure-Zag harness (see FORK_BATTERY_0821.md). The
remaining 57 named entries are fixtures at unchanged SHAs, carried
forward from ef418824b with that commit's evidence intact. Named entry
list is identical to the 0521 batch: 58 entries total, 46 unique
commits.
