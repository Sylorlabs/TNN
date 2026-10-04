# P0 - 33 UNREACHABLE COMMITS RE-REFERENCED

**Status: DONE. All 33 confirmed unreachable, then all 33 re-referenced. Zero lost.**

## 1. Why this was urgent

These 33 commits are reachable from **no ref whatsoever**. `git gc --prune` would
unlink them. They carry R32 / E51-E56 work, including `ee7e4dea1` at 37,754 touched
paths and `01cecb5fc` at 39,259. This lane re-referenced them before doing anything
else, because it is the only item on the list whose loss is irreversible.

## 2. Reachability proof (before the fix)

```
$ git fsck --unreachable --no-reflogs | grep -c 'unreachable commit'
33
$ git for-each-ref --contains <sha>          # for each of the 33
(empty for all 33)
```

`--no-reflogs` is required to see all 33. With reflogs enabled git reports 31; the
remaining 2 are held only by reflog entries, which expire on the default 90-day
schedule. Nothing was keeping any of the 33 alive except, for 2 of them, a reflog.

Date span 2026-08-29 to 2026-09-18. Content: E51A-E51D, E52B, E53/E53A, E54, E55A,
E55B, E56A/E56B native R32 work, plus `ee7e4dea1` "checkpoint before masterplan
execution" and `01cecb5fc` "Ignore reproducible local artifacts".

## 3. The fix

One `git update-ref` per commit, into a non-collected namespace:

```
refs/recovered/unreachable-<9-char-abbrev>   ->   <full sha>
```

`refs/recovered/*` is not matched by any `refs/heads/*` or `refs/tags/*` pattern, so
these refs do not perturb branch listings, `git log --all` lane walks, or the ledger
audit's ref enumeration. They exist purely to keep the objects alive.

```
created=33
$ git fsck --unreachable --no-reflogs | grep -c 'unreachable commit'
0
$ git for-each-ref 'refs/recovered/*' | wc -l
33
```

Verified after the fact: unreachable commit count is **0**. Full listing with dates,
subjects, and ref names in `P0_UNREACHABLE_REFS.tsv`.

## 4. What these 33 do NOT rescue - independently re-derived

The audit reported that none of the 252 unresolvable ledger citations matches any of
these 33. Re-derived from scratch, not copied:

```
absent shas (sha_res.tsv, ABSENT)         252
8-char prefixes of those                  252 distinct
matched against the 33 unreachable shas   0
```

**Zero of 252.** Re-referencing these commits makes zero difference to the citation
audit. They are orphaned *work*, not orphaned *evidence*. Do not read this P0 as
repairing any claim.

## 5. Boundary

- This is a **liveness** fix, not a **content** fix. It does not restore any deleted
  path and does not make any ledger claim citable.
- `refs/recovered/*` were pushed to `origin` so the objects are safe off-host too.
- History was not rewritten. The 33 commits keep their original shas, authors, dates
  and messages.
- Two further classes of object are unreferenced and were deliberately NOT handled
  here: 255 blobs and 252 trees, per the audit. None is a commit, so none is at risk
  from `--prune=now` differently from the commits, and no ledger citation names one.
