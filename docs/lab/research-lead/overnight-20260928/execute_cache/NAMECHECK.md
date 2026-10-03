# NAMECHECK: Execute-vs-Cache Analyst

## Step 0: Toolchain guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 19 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp,
  sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` set for all commands.
- `which python3 python` returns nothing. Zero forbidden executables invoked.
- All source reading via `sed`/`grep` (safebin). No computation performed
  beyond file reads. Analysis only.

## Scope

ANALYSIS ONLY. Read-only. No implementation, no source edits, no binaries
built, no evaluators run.

## Input provenance

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  1591 lines). Read-only. Unmodified.
- Duality analysis: `duality_analysis/DUALITY_ANALYSIS.md` (commit `6fa7dd2ec`).
  Semantic decision 1 of 4: execute-vs-cache policy.
- Reuse experiment: `reuse_experiment/REUSE_EXPERIMENT.md` (commit `ea8fc0ac1`).
  MAP-first lookup on unfrozen variant.
- Revision substrate: `revision_substrate/REVISION_SUBSTRATE.md`
  (commit `880c87c4c`). Copy-and-commit + MAP retargeting.
- White-box inventory: `whitebox_inventory/WHITEBOX_INVENTORY.md`
  (commit `b17fee225`). MAP eviction corruption finding.
- Transfer analysis: `xfer_experiment/` (commit `cbd7bc803`). Barrier 4
  (literals baked in, no rebinding).
- H2 void: `h2_eval/H2_EVAL_REPORT.md` (commit `72173fe11`). Direct facts
  short-circuit the trial.

## Constraints honored

- No sealed worlds opened. No sealed contents inspected.
- Frozen TNN-2 source and binary untouched.
- Zero em dashes (byte-verified before commit).
- Research paper `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  untouched.
- Nothing pushed. Local commit only.
