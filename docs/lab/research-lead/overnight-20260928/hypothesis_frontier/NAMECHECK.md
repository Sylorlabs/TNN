# NAMECHECK.md: Hypothesis Generator Worker

## Step 0: Toolchain guard (2026-10-02, frontier_gen_20261002 session)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinks for git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack, `export PATH="$HOME/safebin"`.
- `which python3 python 2>/dev/null` returned nothing (guard-check-done, no python entries).
- Task is analysis and writing only. No Zag code. No computation beyond shell/git/file reads.
- Zero forbidden executables invoked.

## Step 0: Toolchain guard (prior session, 2026-10-01)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinks for git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack, `export PATH="$HOME/safebin"`.
- `which python3 python 2>/dev/null` returned nothing (guard-check-done, no python entries).
- Task is analysis and writing only. No Zag code. No computation beyond shell/git.
- Zero forbidden executables invoked.

## Task scope

Hypothesis generation only. No implementation, no experiments, no binaries.
Deliverable: HYPOTHESES.md with 15+ hypotheses, each with question, information gain rationale, experiment design, falsifier, and priority.

## Constraints honored

- Zero em/en dashes in documentation (byte-verified before commit).
- TNN_RESEARCH_PAPER_20260929.md untouched.
- Explicit pathspecs for git add and git commit.
- Nothing pushed. Commits local only.
