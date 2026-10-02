# NAMECHECK: Composition Collapse Builder

## Step 0: Toolchain Guard

Executed at worker startup (2026-10-02):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result:
- `which python3 python` returned NOTHING (empty output before "guard-check-done")
- PATH=/home/hatch/safebin
- Pure Zag for all research computation. Shell used only for: invoking
  znc, running binaries, git ops, moving/copying files.

**Zero forbidden executables invoked during this wave.**

## Worker Identity

- Mission: Priority D composition collapse. Build ONE mechanism replacing
  A/B/C (per comparative battery commit 3dceac9cc and ledger C208).
- Task: C's DFS + A's plen-contracts + B's co-use history as pluggable
  applicability predicates; remove 3-segment cap; retire A/B pair-search.
- Branch: tnn-native-lab (local only, nothing pushed).
- Prereg: PREREG.md committed ALONE as 06ea103bd, strictly before any
  implementation commit (commit-order self-check).
- Note: untracked design scratch from a prior incomplete attempt existed
  in this directory (never committed); this session wrote PREREG.md fresh,
  then wrote un_patch.zag and un_driver.zag itself after the prereg commit.
  The prior attempt's stale build artifacts were removed and rebuilt.

## Build Records

- Base: composition_C/cc_base.zag (1677 lines, frozen, read only)
- Patch: composition_unified/un_patch.zag (420 lines, this worker)
- Driver: composition_unified/un_driver.zag (289 lines, this worker)
- Build: cat cc_base.zag un_patch.zag un_driver.zag > un_full.zag
  (2386 lines)
- Binary: un_bin (pinned znc_linux_x86_64_abed8aa1), 289243 bytes
- Compile log: un_compile.txt (exit 0; benign A0102 warnings only, same
  class as the comparative battery builds)
- Runs: un_run1/2/3.txt
- SHA-256: 96ffabf454070de47590e60f1d57e288b9ec47f6107967e8a95d8406842032d8
  (all three runs byte-identical)
- Determinism: 3/3 byte-identical

## Line Count Audit (kill bar K5)

- A cx_patch.zag: 183
- B cb_patch.zag: 298
- C cc_patch.zag: 308
- Sum A+B+C: 789
- Unified un_patch.zag: 420
- Delta: 369 fewer lines (47% reduction)

## Bridge Audit (kill bar K7)

- `fn compose_try`: exactly 1 definition (un_patch.zag line 1961 of
  un_full.zag), exactly 1 call site (ev_query).
- `compose_on`: the same one-line config toggle A/B/C each had.
- COMPOSE_MODE: 0 occurrences anywhere in the build.
- MODE identifiers: none (case-insensitive grep over un_full.zag).
- Task-specific relation numbers in un_patch.zag: none.
- Modes / bridges / handlers / new semantic cases: 0.

## Constraints Observed

- Unfrozen only. Frozen source read only (cc_base.zag used as assembly
  base, never modified).
- Pure Zag for all research logic.
- Zero em/en dashes in PREREG.md, NAMECHECK.md, REPORT.md (byte-verified
  before commit).
- Paper untouched: docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
  never modified.
- Nothing pushed to GitHub.
- Explicit pathspecs for all git add/commit operations.
