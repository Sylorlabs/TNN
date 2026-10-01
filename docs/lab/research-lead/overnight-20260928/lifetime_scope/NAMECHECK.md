# NAMECHECK: Lifetime Scoper

## Step 0: Toolchain guard

- Date: 2026-10-01.
- Safebin activated: `$HOME/safebin` created and populated with
  symlinks to system tools (git, znc, sh, bash, ls, cp, mv, rm,
  mkdir, cat, grep, sed, awk, wc, cmp, sha256sum,
  git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` set.
- `which python3 python` returned nothing (empty output,
  guard-check-done). No Python or other forbidden interpreter is
  reachable in this worker's PATH.
- Pure analysis task. No Zag compilation was required; all
  projections are arithmetic on the committed measured cost table
  from `3eeb0d78e`. Zero forbidden executables invoked.
- Scope: analysis ONLY. No source edits, no variant built, no
  implementation.

## Input provenance

- Lifetime protocol v2 (DRAFT-NOT-FROZEN):
  `docs/lab/research-lead/overnight-20260928/lifetime_protocol/LIFETIME_PROTOCOL_V2.md`,
  commit `dd745851e`. Read in full (both read calls, including the
  capped remainder covering Section 19 banked decisions D1-D5).
- Scaling analysis:
  `docs/lab/research-lead/overnight-20260928/scaling/SCALING.md`,
  committed across `02804f782` (NAMECHECK.md) and `bda26cf91`
  (SCALING.md, via shared-index collision; content verified
  byte-identical by the scaling worker).
- Cost accounting table: commit `3eeb0d78e` (COST_ACCOUNTING.md).
- Supporting: eviction corruption `986c52fdc`, white-box
  inventory (1022/1024 nodes after FW9), state dynamics
  `ee238d8d4`, forgetting `2726baf74`.

## Constraints honored

- Analysis only. The frozen protocol and frozen TNN-2 source are
  read-only; nothing modified.
- This task does NOT revise the lifetime protocol. It scopes the
  feasible envelope and proposes a minimal viable test as a
  recommendation for Micah, who owns the freeze decision (D4).
- Zero em dashes in all deliverables (verified by byte scan).
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- No sealed worlds opened.
- Nothing pushed. Commit is local only, on branch `tnn-native-lab`.
- Explicit pathspecs used on both `git add` and `git commit`
  (shared-index collision avoidance per the pattern noted in
  `bda26cf91`).

## Deliverables

- `NAMECHECK.md` (this file).
- `LIFETIME_SCOPE.md` (feasible envelope, scoped protocol,
  TNN-3 requirements).

## Verdict

LIFETIME-SCOPE-COMPLETE.
