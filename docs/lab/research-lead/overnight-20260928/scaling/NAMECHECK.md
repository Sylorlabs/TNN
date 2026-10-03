# NAMECHECK: Scaling Analyst

## Step 0: Toolchain Guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 19 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`.
- `which python3 python` returned nothing. Zero forbidden executables.
- Guard check recorded 2026-10-01.

## Scope

- Analysis ONLY. No implementation, no variant built, no binaries run.
- All cost numbers are taken from the committed cost-accounting
  deliverable (`cost_accounting/COST_ACCOUNTING.md`, commit `3eeb0d78e`).
- All structural facts verified read-only against the frozen source
  (`tnn2_build/tnn2.zag`): table constants (lines 44-47), `decay`
  (line 153), `alloc_node` (line 87), `alloc_raw` (line 105),
  `evict_node` (line 254). Frozen source never modified.
- Projections are arithmetic on measured per-operation costs under an
  explicit event-mix model. The model is stated, not hidden.

## Input provenance

- COST_ACCOUNTING.md (`3eeb0d78e`): 11-operation cost table, 8 findings.
- Frozen `tnn2.zag` (read-only): fixed-table layout, scan loops,
  allocation/eviction logic.
- Eviction-corruption analysis (zombie MAP roots): cited for the
  capability consequence of saturation, not re-derived.
- White-box inventory (1022/1024 live nodes post-FW9): cited as the
  empirical fill-rate anchor.

## Constraints honored

- Analysis only; zero source edits.
- Zero em dashes (byte-verified before commit).
- Paper untouched.
- No sealed worlds opened.
- Nothing pushed (local commit only).
- Explicit pathspecs on commit.
