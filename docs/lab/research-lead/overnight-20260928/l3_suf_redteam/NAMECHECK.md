# NAMECHECK: L3-SUF-1-REDTEAM

Worker: L3-SUF-1-REDTEAM (subagent, 2026-10-03).
Lane: docs/lab/research-lead/overnight-20260928/l3_suf_redteam/
Task: independent red-team per l3_suf_intermediate/PREREG.md section 12
(SUF-K10). Non-ledger task (claim minting paused).

Distinctness: this worker is a different instance from L3-SUF-INTERMEDIATE
(designer), L3-SUF-1-BUILDER, and L3-SUF-1-ADVERSARY. Verified by session:
separate subagent session id, no shared transcript.

## Step 0: toolchain guard (frozen)

- `export PATH="$HOME/safebin"` at startup for all computational work.
- `which python3` / `which python` return NOTHING under safebin PATH
  (verified 2026-10-03; system /usr/bin/python3 exists OUTSIDE the
  safebin PATH and is never invoked).
- All computational verification in pure Zag via the pinned znc
  (~/safebin/znc, 49 tools). Shell only for: invoking znc, running
  binaries, git ops, file moves/copies, text search.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL and results stay exploratory.

## Step 1: prereg freeze (this commit)

PREREG.md frozen BEFORE any red-team analysis. Freeze commit contains
ONLY PREREG.md and NAMECHECK.md, added with explicit pathspecs.

## Boundaries acknowledged

- Builder's frozen code: read-only, never modified (sha256 re-verified
  at link time against l3_suf_adversary/build/frozen_src.sha256).
- Adversary's sealed worlds: never modified; KEY.md read under seal,
  never copied into this lane, never included in REPORT.md.
- Commits local, never push, explicit pathspecs.
