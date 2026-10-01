# NAMECHECK: Teach-Observe Conflation Analyst

## Step 0: Toolchain Guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 16 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp,
  sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`.
- `which python3 python` returned nothing. Zero forbidden executables invoked.
- Scope: ANALYSIS ONLY. Read-only inspection of frozen source via grep/sed.
  No source edits, no builds, no binaries executed.

## Input Provenance

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
- SHA-256 verified: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
- Frozen source never modified. All line references below are to this file.
- Upstream analyses: minus-two `ede1060a5`, verification criterion `c2a48bee6`,
  theater audit `e0423538a` (T4 event log), execute-cache `7186294cd`.

## Constraints

- Analysis only. No implementation, no design of new machinery.
- Zero em dashes (byte-verified before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  not read, not modified.
- No sealed worlds opened.
- Nothing pushed. Local commit only.
- Deliverables: this file + TEACH_OBSERVE.md, committed with explicit pathspecs.
