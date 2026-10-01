# NAMECHECK: Three Stops Synthesizer

## Step 0: Toolchain guard

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
Result: `guard-check-done`. `which python3 python` returned nothing.
Zero forbidden executables invoked. Safebin active for all shell work.

## Scope

SYNTHESIS ONLY. No implementation, no source modifications, no new Zag code.
This worker reads the four completed analyses and the frozen H3-lite prereg
and produces a unified architecture synthesis. No design proposals beyond
what the source analyses already state; the synthesis unifies, ranks, and
relates.

## Input provenance

- Decline signal: `docs/lab/research-lead/overnight-20260928/decline_signal/DECLINE_SIGNAL.md` (commit `9e0ae81d1`)
- Abandonment: `docs/lab/research-lead/overnight-20260928/abandonment/ABANDONMENT.md` (commit `ae76a60a7`)
- Forgetting: `docs/lab/research-lead/overnight-20260928/forgetting/FORGETTING_ANALYSIS.md` (commit `2726baf74`)
- Failure retention: `docs/lab/research-lead/overnight-20260928/failure_retention/FAILURE_RETENTION.md` (commit `d3e896c8c`)
- H3-lite prereg: `docs/lab/research-lead/overnight-20260928/h3lite_prereg/H3LITE_PREREG_FROZEN.md` (commit `9084a7760`)

All read-only. Frozen TNN-2 source never touched.

## Constraints

- Synthesis only; no implementation.
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not modified.
- No sealed worlds opened.
- Nothing pushed. Local commits only.
- Explicit git pathspecs for the commit.
