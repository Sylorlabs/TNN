# NAMECHECK: Genuine State Mapper

## Step 0: Toolchain guard (mandatory)

Executed at session start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Safebin active.
Zero forbidden executables invoked. Shell used only for: reading files
(sed/grep), git operations, directory creation. No compilation, no
binaries executed, no computation beyond text search.

## Scope: ANALYSIS ONLY

- Read-only white-box of frozen TNN-2 source
  (`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
  1591 lines, SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  verified before and after reading; file never modified).
- No source edits. No variant created. No binaries built or run.
- No sealed worlds opened. Research paper untouched. Nothing pushed.

## Input provenance

- Theater audit `e0423538a` (6 theater instances; genuine-state table).
- Theater ablation follow-up: all 6 classifications empirically CONFIRMED
  (T1 dead, T2 read-only, T3/T4/T5/T6 write-only).
- Forgetting analysis `2726baf74` (bid mechanics, retention decisions).
- Bid semantics `1538eeefe` (MAP bid as birth certificate).
- Teach-observe conflation `8744796fb` (5 sources, one tag).
- Execute-vs-cache `7186294cd` (MAPs as closed replays).
- Minus-two disambiguation `ede1060a5` (8 terminal paths).
- Three-stops synthesis `48cb843e5` (consequence re-entry absence).

## Deliverables

- `GENUINE_STATE.md`: component inventory, edge-type census, header
  census, interaction map, capability boundary, gaps.
- This file.

## Constraints honored

Analysis only. Zero em dashes (byte-verified before commit).
Explicit pathspecs on commit. Local commit only, nothing pushed.
