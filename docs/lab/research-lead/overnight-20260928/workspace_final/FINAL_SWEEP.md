# Workspace Final Sweep

Verification pass after BRANCH-CLEANUP (69 deleted) + BRANCH-CLEANUP-2 (11 deleted) = 80 branches deleted. Checked 2026-10-03 ~03:45 PDT. Analysis only; no deletions performed.

## Final branch count: 102

Confirmed: `git branch --list | wc -l` = 102 (182 -> 102 as expected).

## Worktree status: 69 checkouts, all healthy

- `git worktree list` reports 69 entries (main checkout + 68 linked worktrees). Every worktree path exists on disk; no missing/abandoned directories found.
- Main checkout (`~/workspace/tnn-rsi`) is on `lane-ma4b-20261003` with uncommitted changes: 1 modified (`docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`), 1 new file (`docs/lab/research-lead/overnight-20260928/hcontlife5-condrev/NAMECHECK.md`). Active worker state, not a cleanup item.
- 1 worktree in detached HEAD: `~/workspace/lane-l2-interference` at `a6127a0e3` (not tied to a branch). Flag for the owning worker to either create a branch or prune.

## Branches by checkout status

- 68 branches currently checked out in a worktree (not deletable until the worktree retires).
- 34 branches with no worktree checkout.

## Remaining cleanup candidates

### Category A: fully merged into tnn-native-lab, not checked out (4). Safe to delete at any time.

- wave-20260927-0221pdt-exp1
- wave-20260927-0221pdt-exp2
- wave-20260927-0221pdt-sensory
- wave-20261001-2321pdt-backup

### Category B: merged lane branches, but checked out in ACTIVE worktrees (4). NOT deletable yet.

- lane-battery-e5 (worktree ~/workspace/wt-e5)
- lane-comp-20261002-1721pdt (worktree ~/workspace/w1721/lane-comp)
- lane-fork-20261002-1421pdt (worktree ~/workspace/fb1002_1421pdt/lane)
- lane-l3b-20261002-1721pdt (worktree ~/workspace/w1721/lane-l3b)

### Category C: orphaned lane branches, no worktree, NOT merged (24). Cleanup candidates pending governance.

These are completed worker lanes whose worktree is gone but whose tips were never merged. They hold unique unmerged commits (verified: zero of them are merged into tnn-native-lab). Delete only after confirming their results were captured elsewhere (reports/ledger).

- lane-arena-c8-20261002-1421pdt (9ec262c7a, 2026-10-02)
- lane-arena-zeros-20261002-1421pdt (047786685, 2026-10-02)
- lane-contlearn-int-20261002-1421pdt (ee44ac546, 2026-10-02)
- lane-devang-20261002-1421pdt-2 (c5ee8f3b3, 2026-10-02)
- lane-f1-20261002-0821pdt (655c8d7d6, 2026-10-02)
- lane-gennm10-20261003 (190731d61, 2026-10-03)
- lane-genredim-20261003 (b739f81ee, 2026-10-03)
- lane-genstatefix-20261003 (983a46331, 2026-10-03)
- lane-genstress-20261003 (79396e5a4, 2026-10-03)
- lane-gensubsumesu-20261003 (96393c2a5, 2026-10-03)
- lane-h5r2-skeptic2 (709e1e82e, 2026-10-02)
- lane-hcontlife5-20261002 (be8b5fa6d, 2026-10-03)
- lane-hpirev2-20261002-1421pdt (0ef5cdd8e, 2026-10-02)
- lane-l2adapt-20261002-1421pdt-2 (c920cff65, 2026-10-02)
- lane-l3niv2fg-20261002 (5f08dc9d3, 2026-10-03) -- duplicate ref of lane-l3niv2w5-20261002
- lane-l3niv2w5-20261002 (5f08dc9d3, 2026-10-03) -- duplicate ref of lane-l3niv2fg-20261002
- lane-l3rx-20261003 (d00850b4a, 2026-10-03)
- lane-ledgerreconcile-20261003 (02f3bf13d, 2026-10-03)
- lane-ma4redteam-20261003 (012be9fb9, 2026-10-03)
- lane-ma4rt-fix-20261003 (b2c5c6817, 2026-10-03)
- lane-trades-20261002-1421pdt-2 (483211cbd, 2026-10-02)
- lane-trades-finer-20261002-1421pdt (ea0f89092, 2026-10-02)
- lane-xdagfan-20261002 (d9c0f9939, 2026-10-03)
- lane-xhier3-20261002 (17f11bf9b, 2026-10-03)

Note: lane-l3niv2fg-20261002 and lane-l3niv2w5-20261002 point at the identical commit (5f08dc9d3). One ref is redundant.

### Category D: likely-intentional retention, not recommended for deletion (6)

- tnn-native-lab-wave-archive-20260923-2321pdt
- tnn-native-lab-wave-archive-20260924-0221pdt
- tnn-native-lab-wave-archive-20261002-1121pdt
- tnn-native-lab-wave-archive-20261002-1421pdt
- tnn-native-lab-wave-archive-wave-20261002-0821pdt
- wave-debate-session-1-backup

## Summary

- 102 branches remain. 4 are safe immediate deletions (Category A).
- 24 orphaned lane branches (Category C) are the next cleanup tier but require result-capture confirmation first, since they hold unmerged commits.
- 68 checked-out branches stay until their worktrees retire.
- No broken worktree metadata found. One detached-HEAD worktree and one duplicate-ref pair flagged for follow-up.
