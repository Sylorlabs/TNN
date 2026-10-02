# NAMECHECK: Formal Error/Constraint Worker

## Step 0: Toolchain guard

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
Result: `which python3 python` returned nothing. Safebin PATH active.
Guard check recorded. No forbidden executable invoked.

## Scope

Test whether learned formal understanding constrains TNN behavior
(Constitution Sections 7 and 27). Unfrozen variant only. Frozen TNN-2
source read-only.

## Input provenance

- Base cognition: `../persistent_connections/pc_base.zag`, verified
  byte-identical copy of the frozen TNN-2 base (SHA-256 prefix
  `a29972ca8183b285`, per persistent_connections/NAMECHECK.md).
- `fe_base.zag` is a byte copy (`cmp`-verified) of that base.
- Treatment patches in `fe_patch.zag` redefine `t2_trial` (F1 relation
  filter, F2 form-ordered search) and `t2_exec` (F3 integrity check)
  via last-definition-wins concatenation. No other base function is
  altered. Driver audit helpers are read-only.

## Constraints

Pure Zag via pinned znc. Zero em/en dashes in docs. Paper untouched.
Nothing pushed. 0 modes, 0 bridges, 0 handlers, 0 semantic cases.
