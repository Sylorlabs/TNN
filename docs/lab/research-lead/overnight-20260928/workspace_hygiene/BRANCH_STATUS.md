# Branch Status Report: workspace hygiene sweep

Date: 2026-10-03 ~03:35 PDT (analysis of `~/workspace/tnn-rsi`)
Scope: local branches vs `tnn-native-lab` (tip `f40fbeb11`, 2026-10-03 10:30 UTC, watchdog ledger C463)
Method: for each of 182 local branches, `git merge-base --is-ancestor <branch> tnn-native-lab`
(ahead=0 for every MERGED branch; cross-checked against `git branch --merged tnn-native-lab`,
both agree). Activity inferred from `git worktree list`: a branch checked out in any
worktree (including stale worktrees) is treated as ACTIVE and is never a delete candidate.
Nothing was deleted; this is analysis only.

## Summary

| Category | Count |
|---|---|
| Total local branches | 182 |
| SAFE TO DELETE: fully merged to tnn-native-lab, not checked out anywhere | 81 |
| ACTIVE, KEEP: merged but still checked out in a worktree | 8 (incl. tnn-native-lab itself) |
| ACTIVE, KEEP: unmerged, checked out in a worktree | 62 |
| NEEDS ATTENTION: unmerged, no worktree checkout | 31 |

## 1. SAFE TO DELETE (81 branches)

All are ancestors of tnn-native-lab with zero commits ahead. No worktree checks them out,
so deletion loses no work. Verified: `git branch --merged tnn-native-lab` agrees.

### Completed worker lanes, 20261002 waves (35)
- lane-arena-20261002-0821pdt (last commit 2026-10-02)
- lane-arena-20261002-1121pdt (2026-10-02)
- lane-battery-20261002-1121pdt (2026-10-02)
- lane-comp-20261002-0821pdt (2026-10-02)
- lane-comp-20261002-1121pdt (2026-10-02)
- lane-complife-20261002 (2026-10-02)
- lane-contlearn-20261002-0821pdt (2026-10-02)
- lane-contlearn-20261002-1121pdt (2026-10-02)
- lane-ddes-20261002-0821pdt (2026-10-02)
- lane-ddes-20261002-1121pdt (2026-10-02)
- lane-devang-20261002-0821pdt (2026-10-02)
- lane-devang-20261002-1121pdt (2026-10-02)
- lane-f1rt-20261002-1121pdt (2026-10-02)
- lane-f2-20261002-0821pdt (2026-10-02)
- lane-f2-20261002-1121pdt (2026-10-03)
- lane-fork-20261002-1121pdt (2026-10-02)
- lane-hpi-20261002-0821pdt (2026-10-02)
- lane-hpi-20261002-1121pdt (2026-10-02)
- lane-hpirev2-20261002-1121pdt (2026-10-03)
- lane-index-20261002-1121pdt (2026-10-02)
- lane-index-plenfix-20261002-1421pdt (2026-10-02)
- lane-l2adapt-20261002-1121pdt (2026-10-02)
- lane-l3nir-20261002 (2026-10-03)
- lane-records-20261002-1121pdt (2026-10-02)
- lane-sensory-20261002-0821pdt (2026-10-02)
- lane-sensory-20261002-1121pdt (2026-10-03)
- lane-tnn3-20261002-1121pdt (2026-10-02)
- lane-tnn3-20261002-1421pdt (2026-10-02)
- lane-trades-20261002-0821pdt (2026-10-02)
- lane-trades-20261002-1121pdt (2026-10-02)
- lane-zncbatt-20261002-1421pdt (2026-10-02)
- lane-compinteg2-20261002 (2026-10-03)
- lane-l3b-20261002-1721pdt is ACTIVE (worktree); listed in section 2
- lane-comp-20261002-1721pdt is ACTIVE (worktree); listed in section 2

### Archived wave snapshots (45) - all merged, all stale
tnn-native-lab-wave-archive-20260924-0521pdt, -20260924-1121pdt, -20260924-1421pdt,
-20260924-1721pdt, -20260926-2021pdt, -20260927-0221pdt, -20260927-0521pdt,
-20260927-1421pdt, -20260928-2021pdt, -20260929-0221pdt, -20260929-0521pdt,
-20260929-0821pdt, -20260929-1121pdt, -20260929-1421pdt, -20260929-1721pdt,
-20260929-2321pdt, -20260930-0221pdt, -20260930-1121pdt,
tnn-native-lab-wave-archive-wave-20260924-1721pdt, -20260924-2321pdt,
-20260925-0221pdt, -20260925-0521pdt, -20260925-0821pdt, -20260925-1121pdt,
-20260925-1421pdt, -20260926-0521pdt, -20260926-0821pdt, -20260926-1121pdt,
-20260926-1421pdt, -20260926-1721pdt, -20260926-2321pdt, -20260927-0821pdt,
-20260927-1121pdt, -20260927-1721pdt, -20260927-2021pdt, -20260927-2321pdt,
-20260928-0221pdt, -20260928-0829pdt, -20260928-1721pdt, -20260928-2321pdt,
-20260930-0805pdt, -20260930-0821pdt, -20261001-0221pdt, -20261001-1421pdt,
-20261001-1721pdt, -20261001-2021pdt, -20261002-0521pdt, -20261002-1121pdt

### Other (1)
- wave-20261001-2321pdt-backup (2026-10-02) - merged; backup branch, confirm no longer needed before deleting

## 2. ACTIVE, KEEP - do not delete (70 branches)

Merged but still checked out in a worktree (8): lane-battery-e5, lane-comp-20261002-1721pdt,
lane-fork-20261002-1421pdt, lane-l3b-20261002-1721pdt, tnn-native-lab (the main line itself),
wave-20260927-0221pdt-exp1, wave-20260927-0221pdt-exp2, wave-20260927-0221pdt-sensory.
Note: three are 2026-09-27 worktrees that look abandoned but are still checked out; safe to
remove the WORKTREE first, then the branch becomes a delete candidate.

Unmerged and checked out in a worktree (62): active lanes the watchdog has not yet merged.
Includes lane-ma4b-20261003 (current hygiene worker checkout), lane-xdagfan2-20261003,
the l3niv2 w10/w11/w12 lanes, xhier family, l2 xdomain family, genpoolflood, beliefblind,
blindsweep, domainblind, jointblind, nodeblind, and wave-20261002-1721pdt. Full list in
analysis scratch at /tmp/branch_status.txt (field 1 = UNMERGED, cross-referenced with
/tmp/wt_branches.txt).

## 3. NEEDS ATTENTION - unmerged, no worktree checkout (31 branches)

These have no live worktree but are not merged to tnn-native-lab. Each is either a
completed-but-never-merged lane (watchdog should merge or explicitly reject) or an
orphaned worker branch (verify nothing of value, then drop or archive).

### 3a. Older 20261002-wave lanes, unmerged (13)
Small commit counts (1-6 ahead), last commits 2026-10-02, no worktree. Likely completed
work the watchdog never merged, or superseded lanes.
- lane-arena-c8-20261002-1421pdt (4 ahead)
- lane-arena-zeros-20261002-1421pdt (1 ahead)
- lane-contlearn-int-20261002-1421pdt (6 ahead)
- lane-devang-20261002-1421pdt-2 (6 ahead)
- lane-f1-20261002-0821pdt (4 ahead)
- lane-h5r2-skeptic2 (38 ahead)
- lane-hpirev2-20261002-1421pdt (2 ahead)
- lane-l2adapt-20261002-1421pdt-2 (3 ahead)
- lane-trades-20261002-1421pdt-2 (1 ahead)
- lane-trades-finer-20261002-1421pdt (5 ahead)
- tnn-native-lab-wave-archive-20261002-1121pdt (6 ahead)
- tnn-native-lab-wave-archive-20261002-1421pdt (7 ahead)
- tnn-native-lab-wave-archive-wave-20261002-0821pdt (5 ahead)

### 3b. Today's lanes with substantial unmerged work, no worktree (13)
Last commits 2026-10-03, large ahead counts reflect long divergence from tnn-native-lab,
not necessarily unique work. Watchdog should triage: merge, rebase-and-merge, or
explicitly reject with a reason before any deletion.
- lane-gennm10-20261003 (213 ahead)
- lane-genredim-20261003 (155 ahead)
- lane-genstatefix-20261003 (107 ahead)
- lane-genstress-20261003 (125 ahead)
- lane-gensubsumesu-20261003 (99 ahead)
- lane-l3rx-20261003 (174 ahead)
- lane-ledgerreconcile-20261003 (227 ahead)
- lane-ma4redteam-20261003 (218 ahead)
- lane-ma4rt-fix-20261003 (224 ahead)
- lane-hcontlife5-20261002 (80 ahead, last commit 2026-10-03)
- lane-l3niv2fg-20261002 (2 ahead)
- lane-l3niv2w5-20261002 (2 ahead)
- lane-xdagfan-20261002 (2 ahead)
- lane-xhier3-20261002 (43 ahead)

### 3c. Old backups / ancient archives (3)
- tnn-native-lab-wave-archive-20260923-2321pdt (64 ahead, last commit 2026-09-24)
- tnn-native-lab-wave-archive-20260924-0221pdt (10 ahead, last commit 2026-09-24)
- wave-debate-session-1-backup (1 ahead, last commit 2026-09-23)

### 3d. Caveat on section 3
"ahead" counts overstate unique work for old branches: e.g. lane-gennm10-20261003's
merge-base with tnn-native-lab is 899407c61 (2026-10-03 00:46 UTC), so the 213 commits
include history that predates its fork. Do not treat the number as a measure of unique
contribution; inspect the lane's own commits (its merge-base..tip range) before deciding.

## Recommended next actions for the parent/watchdog

1. Delete the 81 branches in section 1 (safe; all fully merged, none checked out). Suggested:
   `git branch -d <branch>` for each; `-d` refuses if the branch is not merged, giving a
   second safety check. Start with the 35 completed worker lanes and 45 archives.
2. Investigate the three abandoned-but-checked-out 2026-09-27 worktrees
   (tnn-rsi-wt-exp1, tnn-rsi-wt-exp2, tnn-rsi-wt-sensory); remove the worktree if the worker
   is gone, which makes those branches delete candidates too.
3. Triage section 3a: merge-or-reject each of the 13 old unmerged lanes, then delete.
4. Triage section 3b: the gen* and l3rx/ledgerreconcile/ma4* lanes hold today's frontier
   work with no live worktree; confirm whether the work was captured elsewhere (some may
   be superseded by sibling lanes) before any merge/drop decision.
5. Keep section 2 untouched.

No deletions were performed by this worker.
