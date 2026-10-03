# NAMECHECK.md: Provenance Experiment Builder

## Step 0: Toolchain Guard (2026-10-01)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 36 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing (verified empty).
- Zero forbidden executables invoked.

## Scope

UNFROZEN VARIANT ONLY. Frozen TNN-2 source is read-only reference.
This worker builds a provenance-tagged variant, runs treatment vs
control batteries, and reports PROVENANCE-COMPLETE.

## Input provenance

- Discount pilot implementation: `0daaa2ed4`
  (`docs/lab/research-lead/overnight-20260928/discount_impl/`)
- Discount adversary design: `b0cd36859`
  (`docs/lab/research-lead/overnight-20260928/discount_adversary/`)
- Discount specification: `62fa77192`
  (`docs/lab/research-lead/overnight-20260928/discount/`)

## Constraints honored

- Pure Zag via pinned znc
  (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell only: invoke znc, run binaries, git ops, move/copy files.
- Zero em/en dashes in all outputs (byte-verified before commit).
- Paper
  (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`)
  untouched.
- No sealed worlds. Nothing pushed. Commits local only.
- Explicit pathspecs on both `git add` and `git commit`.
