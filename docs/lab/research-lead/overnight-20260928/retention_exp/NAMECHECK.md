# NAMECHECK: Retention Experimenter

## Step 0: Toolchain Guard (mandatory, recorded 2026-10-01)

Safebin activated:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack ln; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
```

Verification:
- `which python3 python` returns nothing (empty output, guard-check-done).
- `znc --version`: znc 2026.07.0-dev (edition 2026), pinned binary
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Safebin contains 42 tools including git, znc, ln.

## Scope

UNFROZEN VARIANT ONLY. This worker builds an experimental variant to test
whether consequence-substrate retention input makes re-learning cheaper.

- Frozen source: `rt_base.zag` is a verbatim copy of the frozen TNN-2
  cognition (SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  verified identical before and after). Frozen source is READ-ONLY.
  It is never modified, only excised-and-replaced at assembly time
  (same method as substrate_consolidation 1ed3f5a6b).
- All cognition changes live in `rt_retention.zag` (new file).
- Driver is harness-side (`rt_driver.zag`), not cognition.

## Provenance

- Base: frozen TNN-2 via substrate_consolidation/sc_base.zag (hash verified).
- Substrate machinery: adapted from sc_substrate.zag (1ed3f5a6b),
  extended with RETENTION namespace.
- Budget-pressure R5 finding: bc96dd3d8 (re-learning NOT cheaper, rec_evict
  never consulted).
- No sealed worlds opened. No paper touched. Nothing pushed.

## Constraints honored

- Pure Zag via pinned znc. Shell only for znc invocation, binary runs,
  git ops, file moves.
- Zero em/en dashes in all written files (byte-verified before commit).
- Explicit pathspecs on git add and git commit.
- No forbidden executables invoked. Any such invocation would be
  PROCESS-FAIL; none occurred.
