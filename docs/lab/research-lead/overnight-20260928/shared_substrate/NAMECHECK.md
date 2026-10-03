# NAMECHECK: Shared Substrate Specifier

**Worker:** Shared Substrate Specifier
**Date:** 2026-10-01
**Scope:** SPECIFICATION ONLY. No implementation, no variant, no TNN-3 design.

## Step 0: Toolchain guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 17 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack), `export PATH="$HOME/safebin"`
- `which python3 python` returned nothing (empty output, guard-check-done)
- Zero forbidden executables invoked. Analysis and specification used
  only file reads (muse.read) and text search (grep via safebin).
- Pure specification work; no Zag compilation was needed or performed.

## Input provenance

- Learning machinery `3416ed218`
  (learning_machinery/LEARNING_MACHINERY.md): C2 shared retention
  substrate requirement, minimal viable set, C6 source tags, C7 utility.
- Consequence re-entry `7eab34ff2`
  (consequence_reentry/CONSEQUENCE_REENTRY.md): M1-M4 anatomy, "one
  shared retention substrate should feed decline, abandonment,
  retention/eviction."
- Three stops `48cb843e5` (three_stops/THREE_STOPS.md): dependency
  graph, section 2.3 state maintained, R0-R4 implementation order,
  H3-lite composition result.
- H3-lite Node 1 `45c55ed83`
  (h3lite_node1/H3LITE_NODE1.md): narrow counter pattern (tag 40,
  subtype 1, fields 8/12/16/20/24/28 order, field 32 rejection count).

## Constraints honored

- Specification only; frozen source and frozen preregs read-only, never
  modified.
- Zero em dashes in deliverables (byte-verified before commit).
- Paper
  (`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`)
  untouched.
- No sealed worlds opened.
- Nothing pushed; commit is local on branch `tnn-native-lab`.
- Commit uses explicit pathspecs on BOTH `git add` and `git commit`
  (shared-index collision lesson from `bda26cf91`).

## Deliverables

- `SHARED_SUBSTRATE.md`: full specification (record format, key
  namespaces, write paths, read paths, H3-lite convergence,
  boundedness, source tagging, non-specifications, evaluation).
- This file.

**Verdict:** SHARED-SUBSTRATE-COMPLETE.
