# NAMECHECK: Node2-v2 Builder

## Step 0: Toolchain Guard
- Safebin activated: `mkdir -p $HOME/safebin`, symlinked allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`
- `which python3 python` returned nothing. Guard check done.
- Zero forbidden executables invoked.

## Scope
BUILD AND TEST. Prereg frozen before implementation. Unfrozen variant only.

## Input Provenance
- Node2-v2 design: `docs/lab/research-lead/overnight-20260928/node2v2_prereg/NODE2V2_PREREG.md` (DRAFT, commit `21115becf`). Read fully.
- Frozen H3-lite prereg: `9084a7760`. Preserved as negative finding. NOT modified.
- Node 2 unreachability: `b0ad6c5d3`. Read-only.
- Base source: `node2_reachability/tnn2_base.zag` (verbatim frozen, 1591 lines). Read-only.
- Node 2 implementation: `node2_reachability/tnn2_node2.zag` (1701 lines). Reference for policy node pattern. Read-only.

## Build Plan
1. Freeze prereg (FROZEN_PREREG.md with timestamp, commit before implementation).
2. Unfrozen variant: copy base, add policy node (tag 40, subtype 2), modify miss_inquire to read field 20, add ev_observe with a_w parameter, implement resolve_uncertainty_v2 recording world-revealed actions.
3. Sealed test worlds: 3 phases (baseline, shift, confirmation).
4. Run 3/3 deterministic, measure against kill bars.
5. Verdict: K-H3 PASS/FAIL.

## Constraints
- Prereg frozen BEFORE implementation (commit-order rule).
- Unfrozen variant only. Frozen source/prereg read-only.
- Pure Zag via pinned znc. Zero em/en dashes.
- Paper untouched. Nothing pushed.
