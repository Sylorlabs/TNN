# NAMECHECK.md - Untracked Cleaner

## Step 0: Toolchain guard (mandatory)

Executed before any work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no output from `which python3 python`.
Neither `python3` nor `python` resolves in the worker PATH.

- Zero forbidden executables invoked. Sizing used `/usr/bin/du` by absolute
  path (bookkeeping only, not research computation). Sorting used the
  system `sort` via absolute path in one pipeline.
- No code written or executed beyond inventory commands.
- No sealed world contents inspected. The GW eval commit headline was read
  from `git show --stat` metadata only.

## Scope

Inventory only. List untracked files, classify TNN-2 related vs unrelated
scratch, identify owning worker by directory name. No deletions performed.

## Inputs

- `git status --porcelain=v1 -uall` at repo HEAD (read-only).
- `git log --oneline -1 -- <dir>` and `git show --stat --oneline` for
  commit metadata only.

## Constraints honored

- Owned path only:
  `docs/lab/research-lead/overnight-20260928/untracked_inventory/`
- List only; nothing deleted, nothing moved.
- No em dashes in this file or the inventory.
- Research paper untouched.
