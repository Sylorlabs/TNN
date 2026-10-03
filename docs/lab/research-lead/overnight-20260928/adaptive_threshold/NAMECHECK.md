# NAMECHECK.md: Node2 Adaptive Threshold Worker

## Step 0: Toolchain guard (mandatory)

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

Result: `which python3 python` returned nothing. Only `guard-check-done` printed.
Safebin PATH active for all subsequent commands. Pure Zag via pinned
`znc_linux_x86_64_abed8aa1`. No Python, no other interpreters invoked.

## Step 1: Task identity

Mission: test learner-adaptive evidence requirements (Micah Priority 8).
Build on Node2-v2 `0988839a2`. Unfrozen variant only. The evidence threshold
must be WRITTEN by experience, not researcher-set. Three environments:
stable, noisy, changing. 3/3 deterministic runs per arm.

## Step 2: Scope

- Unfrozen variant of the Node2-v2 core (first 1020 lines of
  `node2_generalization/gen_base.zag`, verbatim except one documented
  call-site splice).
- Frozen source read-only. Nothing pushed. Paper untouched.
- Zero em/en dashes in documentation (byte-verified before commit).
