# NAMECHECK: NEG-TRANSFER-1 (NT1 -- selective retention under sequential training)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary, znc
  2026.07.0-dev edition 2026; verified 2026-10-03).
- Safebin contents: coreutils, git, znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging, znc
  invocation, binary execution, hashing, cmp/diff for byte-identity
  checks, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Reference integrity

No external reference sources: `nt_full.zag` is original code for this
lane, implementing the frozen learner rules of PREREG Section 2 verbatim.
The output-helper block (z_alloc, get32, set32, o_app, o_i64, o_nl,
o_flush) is transcribed from the frozen domain_blindness template
(a_full.zag); it performs no science.

## Step 2: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/negative_transfer/`),
fresh `git init` 2026-10-03, branch `main`. Nothing is pushed to GitHub;
commits stay local, explicit pathspecs only. The prereg-alone-then-
implementation commit order is honored inside this repo: the first commit
contains ONLY PREREG.md and NAMECHECK.md (Steps 0-2). `nt_full.zag`,
build outputs, binaries, run outputs, and REPORT.md come in later
commits.

## Build record (completed 2026-10-03)

- [x] nt_full.zag written per PREREG Sections 2-5 (27 fns); audit grep for
      protect/freeze/don't-forget/task-label logic: clean
- [x] negated-conjunction while-check: clean
- [x] pinned znc build: `znc nt_full.zag -o nt_bin` (exit 0; one benign
      zagd-unavailable warning, foreground compilation)
- [x] 3/3 runs byte-identical (cmp); digests: runs
      `e89c61c7f62ff50cf5146d85df34ef3ad4bcac88a536afd648479bc33972219d`,
      nt_bin `880d7ddb43444b1be125c87be37518d64190011d50b8e6ed63c5196ec39277ad`,
      nt_full.zag `644014ee8f9f602fb5deff1eec28da793a12887b6258e58fa96208a935a3c383`
- [x] every frozen numeric prediction matched exactly (TTC 2/2/4, pc 1/3,
      retest 6/6/12/0, ML0 u=0/12 forget=12 nalias=12)
- [x] K1-K5 evaluated against frozen bars: all 1; REPORT.md with frozen
      verdict mapping: PASS
