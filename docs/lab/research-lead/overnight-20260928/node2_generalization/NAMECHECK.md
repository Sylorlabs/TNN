# NAMECHECK.md - Node2-v2 Generalization Worker

## Step 0: Toolchain Guard

Date: 2026-10-01
Worker: Node2-v2 Generalization Worker (Micah Q1)

Safebin setup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned empty (no output before "guard-check-done").
No Python available in PATH. Pure Zag via pinned znc only.

## Provenance

- Base: `0988839a2` (Node2-v2 K-H3 PASS), `ab1bee9a6` (ablation)
- Frozen source: read-only reference only
- All work: unfrozen variant in `docs/lab/research-lead/overnight-20260928/node2_generalization/`
- Task: Attack researcher-owned parts per Micah Q1 (threshold=3, single policy, global replacement)

## Constraints Honored

- Unfrozen variant only
- Frozen source/prereg read-only
- Pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`)
- Zero em/en dashes in documentation (byte-verified before commit)
- Paper untouched (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`)
- Nothing pushed (local commits only)
- Explicit pathspecs on git add and git commit
