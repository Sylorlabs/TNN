# NAMECHECK.md -- Knowledge Composition Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed. `which python3 python` returned NOTHING.
PATH=/home/hatch/safebin. Safebin active for all subsequent work.

No forbidden executable invoked. Pure Zag via pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1).

## Step 1: Task identity

Knowledge Composition Worker. Test novel composition X+Y->Z per
Constitution Sections 8 and 26. Unfrozen variant only.

## Step 2: Constraints honored

- Unfrozen only. Frozen source read-only (never modified).
- Pure Zag. Shell only for znc invocation, binary runs, git, file moves.
- Zero em/en dashes in documentation (byte-verified before commit).
- Paper untouched: docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
- Nothing pushed. Commits local only on tnn-native-lab.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
