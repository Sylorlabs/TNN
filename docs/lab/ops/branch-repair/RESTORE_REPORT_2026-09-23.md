# Branch repair report — 2026-09-23

## What happened
Commit `308bf3655575` ("Fork H3: H3ADV video fixtures") was created via the
GitHub API with **main's full tree** as the commit tree, instead of layering
the H3 files onto `tnn-native-lab`'s tree. The follow-up `4e1fc55f` did the
same. Net effect on `tnn-native-lab`:

- **26,447 files deleted** (everything on the lab branch that was not on main)
- **53 files clobbered** (`.github/scripts/*`, `.github/workflows/*` replaced with main's versions)
- 23 files leaked in from main's tree (dedup + ingest_10gb/clean work products)

This was an operator error during the move of the H3 crew's mis-committed
work off `main`, not a crew bug. The r10 crew caught it and restored their
own files; this commit restores the rest.

## What this commit does
Restores byte-identical blobs from the pre-damage tree `506dd39c`:

- 26,146 deleted files still absent at the head
- 53 clobbered CI scripts/workflows back to their lab versions

Deliberately kept as-is:

- 301 files crews had already re-committed (their versions stand)
- The H3 fixtures + verdict — the actual intent of the two bad commits
- The 23 leaked files — genuine work products of lab tracks (dedup,
  ingest_10gb/clean); deleting them would destroy work
- Files later commits legitimately changed after the damage

## Verification
- Restored blob SHAs match the pre-damage tree exactly (content-addressed).
- Spot-checks: H3ADV fixtures present, r10 files present, dialogue repair
  files present, `.github` scripts match lab versions.
- New tree = previous head + restorations; no present file was modified or
  removed by this commit.

## Lesson
Never create a branch commit via the API with another branch's tree.
Layer additions onto the branch's own tree (base_tree), or cherry-pick the
file delta. A tree-replace is a silent mass delete.
