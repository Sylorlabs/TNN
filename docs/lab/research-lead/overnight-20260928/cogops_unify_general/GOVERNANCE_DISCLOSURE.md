# GOVERNANCE DISCLOSURE — shared-checkout branch thrash (this lane)

**Lane:** ARCHITECT-COMPRESSION · `arch/cogops-unify` · 2026-10-03

## What happened

This repository is being worked on by several lanes from **one shared
working tree and one shared `.git`**. During this lane's run the checked-out
branch was changed underneath me by another worker, so both of my commits
were recorded on top of **another lane's** history instead of mine.

Actual sequence:

1. I created `arch/cogops-unify` at `504641745` and confirmed
   `git branch --show-current` → `arch/cogops-unify`.
2. I committed the prereg. Git recorded it as `05826b235` with parent
   `92ab1903f` — a **SUF-AUDIT** commit — i.e. the branch had already been
   switched before my `git commit` ran.
3. I committed the results as `7c33dc026` with parent `8534fd128` — an
   **NS-INVARIANT** commit.
4. At the end of the run, `arch/cogops-unify` was still at `504641745`
   (unmoved) and `HEAD` was on `redteam/suf-audit`.

This is the same class of incident already disclosed by the SUF-AUDIT lane
in `9dec1bca5` ("P4 shared-checkout branch thrash orphaned prereg commit").

## Repair

Both commits were rebuilt **byte-identically** onto the correct parent using
git plumbing (`read-tree` / `git apply --cached` / `write-tree` /
`commit-tree` / `update-ref`) with a scratch index, so that **the shared
working tree and the real index were never touched** — another lane was
actively using them.

| | original (mis-parented) | rebuilt (correct) |
|---|---|---|
| prereg | `05826b235` | `3bf225125` |
| results | `7c33dc026` | `5cbab9747` |

Verification: `git diff 7c33dc026^{tree} arch/cogops-unify^{tree} --
cogops_unify_general` is **empty** — my lane's content is byte-identical.
The branch `arch/cogops-unify` now holds exactly two commits on top of
`504641745`, and `git diff --name-only 504641745 arch/cogops-unify` lists
375 files of which **0** are outside
`docs/lab/research-lead/overnight-20260928/cogops_unify_general/`.

## What I deliberately did NOT do

I did **not** reset, rebase, or otherwise move `redteam/suf-audit` or any
other branch ref. The orphaned commits `05826b235` and `7c33dc026` are still
reachable from `redteam/suf-audit`, so nothing is lost and no other lane's
ref was rewritten. Rewriting them would have been a second, larger instance
of the same thrash. The SUF-AUDIT and NS-INVARIANT workers should decide
themselves whether to strip the two foreign commits from their history.

## Claim-ID collision — disclosed, not a conflict

`1e98bde45` (SUF-AUDIT) records: *"re-mint IDs C500/C501 -> C590/C591
(collision with ns_invariant/cogops_unify_general disclosed)"*. That worker
detected the overlap and re-minted **its own** IDs. This lane's IDs are
therefore uncontested:

| id | this lane |
|---|---|
| C500 | recon of the `strat_sel` family |
| C501 | `_zag_raw_syscall` inert on this host |
| C502 | frozen prereg (bars B1–B7, predictions P1–P5) |
| C503 | UGEN, the unified mechanism |
| C504 | the ablation |
| C505 | M1/M2/M3 measurements (grid, ledger, witness) |
| C506 | verdict + report |

`368eedc95` (NS-INVARIANT) claims **C500–C509**. This lane uses
**C500–C506**. That is an **overlap of 7 ids across two lanes** and it is a
real governance defect, not a non-issue: the SUF-AUDIT lane had to re-mint
because of it. I am not re-minting unilaterally because this lane's prereg
(committed alone, `3bf225125`, before any code) already names C500–C506 in
its frozen text, and re-minting now would break the prereg-to-results
traceability that the prereg exists to provide. **Recommend a single
allocator be installed before the next wave** — SUF-AUDIT's `P5` already
proposes one and that proposal should be adopted rather than each lane
patching around it. C377–C466 were not touched.

## Recommendation

1. One git worktree (or one clone) **per lane**. `git worktree add` makes
   the branch-thrash class of incident structurally impossible.
2. A pre-commit assertion that `git branch --show-current` equals the lane's
   declared branch.
3. A claim-ID allocator, per SUF-AUDIT `P5`.
