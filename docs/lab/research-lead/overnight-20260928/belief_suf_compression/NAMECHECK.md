# NAMECHECK: BELIEF-SUF-COMPRESSION

Worker: BELIEF-SUF-COMPRESSION subagent, 2026-10-03.
Lane: docs/lab/research-lead/overnight-20260928/belief_suf_compression/
Task: architecture compression analysis of the belief layer
(BELIEF-PROVENANCE through BP-8) vs L3-SUF-1 resolution records.
Non-ledger task (claim minting paused); nothing minted.
Analysis only; no mechanism code is modified by this lane.

## Step 0: toolchain guard

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (from the tnn-rsi checkout; the script is absent from tnn-rsi-gpi3).
  Result: SAFEBIN-READY, /home/hatch/safebin, 36 tools, no python.
- Verified with PATH="$HOME/safebin": `which python3` empty,
  `which python` empty, `which znc` -> /home/hatch/safebin/znc,
  znc 2026.07.0-dev (edition 2026).
- All scientific computation in this lane (the decision-logic toy
  model) is pure Zag, built and run under the safebin PATH.
- No python3/python/C/JS/Rust invoked at any point in this lane.
- Git note: $HOME/safebin/git is a symlink to /usr/bin/git and has a
  known EPERM-on-write failure mode on this shared worktree; all git
  writes in this lane use /usr/bin/git directly.

## Step 1: identity

- Lane name matches the assigned lane exactly.
- No prior lane with this name exists in tnn-rsi-gpi3.

## Step 2: scope

- Read-only on belief_provenance*/ and l3_suf_intermediate/.
- Writes only inside belief_suf_compression/ (PREREG.md, this file,
  model/, ANALYSIS.md).
- Commits local on tnn-native-lab with explicit pathspecs, never pushed.

## Step 3: commit order

- PREREG.md is committed alone strictly before any analysis artifact
  (model code, model outputs, ANALYSIS.md). The analysis commit follows
  the prereg commit. Self-check recorded in PREREG.md section 6.
