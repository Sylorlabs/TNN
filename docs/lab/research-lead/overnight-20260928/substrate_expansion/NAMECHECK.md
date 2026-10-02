# NAMECHECK: Shared Substrate Expansion Worker

## Step 0: Toolchain guard

Executed at worker startup, before any research computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed, `which python3 python` returned
nothing. Safebin active with 42 tools. PATH restricted for the whole
session.

Mission: drive 5 behaviors (policy, withholding, abandonment,
retention, search-order) from ONE shared consequence substrate, with
per-behavior ablations. Build on commit fa8405a90.

Base: frozen sc_base.zag SHA-256 a29972ca8183b285... (verified).
Unfrozen variant only. Frozen source read-only.

Constraints: pure Zag via pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1). Zero em/en dashes
in docs (byte-verified before commit). Paper untouched. Nothing
pushed. 0 modes, 0 bridges, 0 handlers, 0 semantic cases.
