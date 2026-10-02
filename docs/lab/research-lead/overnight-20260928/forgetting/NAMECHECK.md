# NAMECHECK: Forgetting Analyst

## Step 0: Toolchain guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 18 allowed tools
  (git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum
  git-receive-pack git-upload-pack), `export PATH="$HOME/safebin"`.
- Verification: `which python3 python` returned nothing (no output).
- Zero forbidden executables invoked. All work: file reads, text writes,
  git operations.

## Scope

- Analysis ONLY. Read-only. No implementation. No design document.
- Subject: frozen TNN-2, build commit `f4de7ff46`, source read at
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`.
- No sealed worlds opened. No sealed contents inspected.

## Input provenance

- Transfer analysis `475c57e23`
  (`tnn2_transfer/TRANSFER_ANALYSIS.md`), especially Q4 interference
  profile and section 7 compression notes.
- Frozen source retention functions: `alloc_node` (line 87),
  `evict_node` (254), `rec_evict` (249), `bid` (237), `is_prot` (221),
  `ref_prot` (276), `decay` (153), `promote_graph` (533),
  `ev_query` (811), `ev_observe` (831), `ev_teach` (282).
- Micah's 2026-10-01 continuous-learner message: learner freedoms
  include "forget/compress/retire structures when useful" and
  "change retention priorities"; evaluation policy distinguishes
  FROZEN RESEARCHER CODE from CONTINUOUSLY CHANGING LEARNER STATE.

## Constraints honored

- Analysis only; no source edits, no variant binaries, no new Zag code.
- Zero em dashes (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commit only.
