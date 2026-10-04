# LANE-RESTORE: P0 EVIDENCE-VISIBILITY RECOVERY

**Lane:** `lane/restores`. **Worktree:** `/Users/Shared/micah/Documents/TNN/.worktrees/restores`.
**Base:** `87a822426`. **Date:** 2026-10-04.

This lane executes the recovery items proposed by `lane/recovery` (`9b2c4db6e`,
`docs/lab/research-lead/overnight-20260928/evidence_recovery/RECOVERY_REPORT.md`).

`canonical_ledger/CLAIM_LEDGER.md` was **not modified**. No history was rewritten: no
force-push, no amend, no rebase. Every change here is a new commit that only ADDS.

## Load-bearing correction carried forward

`b3b3ee00a` deleted 160,515 paths. **None of them are lost.** All 160,515 are present in
its parent `4e7eb30b1`, which is an ancestor of all 32 local branches and is reachable
from `origin/tnn-native-lab`. The damage is **visibility**, not data: tracked paths fell
165,288 -> 5,276 and 858 of 1,108 research lanes vanished from every tip. That invisibility
is the mechanism of the earlier "CALR has no source" false negative.

## Read these

| File | What it is |
|---|---|
| `P0_UNREACHABLE_REFS.tsv` | The 33 commits re-referenced under `refs/recovered/` |
| `P0_UNREACHABLE.md` | P0 findings: reachability proof, rescue test, what it does NOT rescue |
| `REPORT.md` | Consolidated report for every item in this lane |
| `PROPOSALS.md` | Ledger proposals C650-C659. **Nothing minted.** Ledger untouched |
| `mass_delete_guard.zag` | P2 tripwire, pure Zag, refuses a >1000-path deletion |
| `cite_remap.tsv` | P1 citation remapping: unresolved sha -> what it actually resolves to |

## Method note

Every count in this lane is a `git` plumbing count (orchestration, permitted by charter
section 4) or output of a pure-Zag program compiled with `--target macos-arm64` under
`pure-zag.sh`. No forbidden interpreter was invoked; `tnn_pure_zag_report` prints
`PURE-ZAG-CLEAN`.
