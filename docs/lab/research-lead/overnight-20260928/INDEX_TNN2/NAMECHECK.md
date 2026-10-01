# NAMECHECK: Documentation Indexer (INDEX_TNN2)

## Step 0: Toolchain Guard

- Safebin activated: `$HOME/safebin` created and populated with 14 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp,
  sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` applied.
- `which python3 python` returned nothing. No Python, C/C++, JavaScript, or
  Rust invoked at any point.
- Work performed: read-only directory listing (`ls`), git log queries, file
  writes of index documents. No computation, no binaries executed, no source
  modified.

## Scope

Index only. No new analysis, no new content, no claims. Every entry points at
a committed document with its commit hash verified via `git log`. Untracked
or in-progress work is marked as such rather than indexed as complete.

## Provenance

- Parent task: Documentation Indexer, spawned 2026-09-30 (PDT).
- Target tree: `docs/lab/research-lead/overnight-20260928/`
- Commit hashes verified 2026-09-30 (PDT) against branch `tnn-native-lab`.

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/INDEX_TNN2/`
- No em dashes in index documents (verified).
- Research paper `TNN_RESEARCH_PAPER_20260929.md` untouched.
- No sealed world contents inspected (index references only design/seal
  metadata documents, never world id triples or expected values).
