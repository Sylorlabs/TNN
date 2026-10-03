# NAMECHECK.md: TNN-2 Construction Red Team

Date: 2026-09-30. Task: Attack TNN-2's runtime construction mechanism (Change 1).

## Step 0: Toolchain guard check

Setup command run at task start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. PATH restricted to
`$HOME/safebin`. Zero forbidden executable invocations during this task.

This is an analysis-only task: source reading, shell-driven binary
probes, and report writing. No builds, no research computation in a
forbidden language. No Python invoked at any point.

## Scope

Target (read-only, never modified):
`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
commit `f4de7ff46`, SHA-256 verified
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.

Probe binary (frozen, unmodified):
`docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin`.

Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_redteam_construction/`

Contains: NAMECHECK.md (this file), CONSTRUCTION_REDTEAM.md.

## Governance

- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff.
- No sealed FW1-FW9 assets accessed.
- Explicit git pathspecs only.
- Scope is Change 1 (runtime construction) only. Change 2 (inquiry)
  and Change 3 (revision) are covered by sibling red teams.
