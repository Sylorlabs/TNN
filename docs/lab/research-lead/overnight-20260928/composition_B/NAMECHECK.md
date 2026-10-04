# NAMECHECK.md -- Composition Hypothesis B Worker

## Step 0: Toolchain Guard (MANDATORY)

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

Result: `guard-check-done` printed, `which python3 python` returned NOTHING.
Safebin active. PATH restricted to $HOME/safebin.

- Pinned compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Pure Zag for all research computation. Shell only for: invoking znc,
  running binaries, git operations, moving/copying files.
- No forbidden executable invoked. Any violation would be PROCESS-FAIL.

## Worker Identity

- Role: Composition Hypothesis B Worker (Micah TOP PRIORITY).
- Approach B: Fragment composition via persistent connection history.
- Hypothesis: co-use LINK edges (type 15, "used together") let TNN
  select fragment pairs to assemble for novel goal Z.
- Base: `knowledge_composition/kc_core.zag` lines 1-1567 (frozen TNN-2 base,
  no ev_query) + this worker's `cb_patch.zag` (extends pc_patch.zag with
  compose_try + co-use episode support).
- Frozen source: read-only. This is an UNFROZEN variant.
- Paper (`TNN_RESEARCH_PAPER_20260929.md`): untouched.
- Nothing pushed. Commits local only.

## Build

- `cb_patch.zag`: patch (this worker).
- `cb_driver.zag`: experiment driver (this worker).
- `cb_full.zag`: assembled as `head -1567 kc_core.zag` + `cb_patch.zag` + `cb_driver.zag`.
- Build: `znc cb_full.zag -o cb_bin` (via pinned toolchain).
- Runs: 3/3 byte-identical required per arm.

## Conventions Honored

- Zero em/en dashes in all docs (byte-verified).
- Explicit pathspecs for all git add/commit.
- No modes, no bridges, no task-specific handlers.
- Driver never authors A-B relations; LINK endpoints are determined by
  which MAPs actually solved the episode queries (learner-determined).
