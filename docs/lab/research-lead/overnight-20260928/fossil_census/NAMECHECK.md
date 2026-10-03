# NAMECHECK: Fossil Census Worker

## Step 0: Toolchain Guard (mandatory)

**Date:** 2026-10-01 UTC
**Worker:** Fossil Census Worker (subagent)

### Safebin activation

```sh
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `which python3 python` returned nothing. `guard-check-done` printed.
Zero forbidden executables invoked. All computation in Zag via pinned
`znc_linux_x86_64_abed8aa1` (resolved from safebin).

### UNFROZEN VARIANT DECLARATION

This work is on an **UNFROZEN VARIANT ONLY**.

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
- `fossil_base.zag`: verbatim copy (SHA-256 identical, verified before/after).
- `fossil_full.zag`: verbatim copy + 3 read-only-behavior instrumentation hooks.
- Frozen source, frozen binary, build `f4de7ff46`: **UNTOUCHED**.
- Original test `main` removed from both build files; driver appended.

Per Micah: "try stuff unfrozen as you go on." This is a measurement
experiment, not TNN-3 implementation.

## Instrumentation (fossil_full.zag only, behavior-preserving)

Field 12 and field 16 of tag-20 MAP nodes are written at promotion
(`ns(W,m,12,-1); ns(W,m,16,-1)`) and never read by any production code
(verified by exhaustive grep: the only `ng(...,12)` / `ng(...,16)` reads
are on tag-101/102/103/104 graph cells inside `execute` and `t2_sig`).

1. `promote_graph`: field 12 init `-1` -> `0` (reference counter);
   field 16 init `-1` -> `hg(W,0)` (birth clock tick).
2. `t2_revise_graph` entry: `ns(W,m,12,ng(W,m,12)+1)` (revision references MAP).
3. New `mark_root_exec(W,root)` called from `t2_exec`: scans live tag-20
   nodes for `ng(W,m,20)==root` and bumps the reference counter
   (attributes post-promotion graph execution to the owning MAP;
   trial-time roots are unpromoted so no false attribution).

Behavioral equivalence verified: `fossil_base_bin` (no hooks) and
`fossil_full_bin` (hooks) produce byte-identical `BAT` battery output.

## Classification

For each live tag-20 MAP at census time:
- ZOMBIE: graph root invalid (out of range, dead slot, or non-graph tag).
- DEGRADED: root valid but graph walk (t2_sig order) hits a dead/invalid cell.
- LIVE: root and graph intact, reference counter > 0.
- FOSSIL: root and graph intact, reference counter == 0.

## Input provenance

- Bid semantics `1538eeefe` (MAP bid is a birth certificate; fossil mechanism).
- Eviction corruption `986c52fdc` (zombie mechanism; design flaw).
- Barrier implementation `d7a62ea34` (counter pattern precedent).

## Constraints

- UNFROZEN ONLY. Frozen source/binary untouched (SHA-256 re-verified at end).
- Pure Zag. Zero em dashes in documentation (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commits only.
- 3/3 byte-identical runs required.
