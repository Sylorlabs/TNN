# NAMECHECK: composition_verify lane, 2026-10-02

Worker: Composition Internal Verification Worker (subagent session
cdbf733b-9ea5-4e95-9534-4a1fe9b71bc5, parent label
102c9b02-9f2f-420e-ad8e-1b3daf8ddbd4).
Lane dir: docs/lab/research-lead/overnight-20260928/composition_verify/
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.

## Step 0: worker toolchain guard (2026-10-02, owner red line)

- Ran the mandated safebin setup inline (task Step 0 commands):
  created symlinks in $HOME/safebin for git znc sh bash ls cp mv rm
  mkdir cat grep sed awk wc cmp sha256sum git-receive-pack
  git-upload-pack (plus pre-existing coreutils already present).
- Every shell in this lane: `export PATH="$HOME/safebin"` first.
- `which python3 python` -> nothing (no output, before guard-check-done).
- `which znc` -> /home/hatch/safebin/znc (pinned toolchain OK,
  znc 2026.07.0-dev edition 2026).
- PURE ZAG ONLY for all research logic. No Python anywhere in this lane.
- Forbidden-executable invocation = automatic PROCESS-FAIL; none occurred.
- Dash rule: loop docs use hyphens only; verified with
  docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before each commit.
- Toolchain lessons honored (AGENTS.md): no `as *i32` + slice construction
  in functions (u8 cells with get32/set32); no `_zag_print` for dynamic
  content (single preallocated output buffer, cursor-returning emit
  helpers, one `_zag_raw_syscall` write at end); no trust in `.len` of a
  cast slice.

## Steps

- [x] Step 0: toolchain guard verified (above), 2026-10-02 ~10:10 PDT
- [x] Step 1: PREREG.md frozen ALONE (commit ca23aa436, PREREG.md only)
- [x] Step 2: implementation (pure Zag) in this lane dir only
- [x] Step 3: 3/3 byte-identical runs, sha256 recorded
      (21b6b86719162e17f7ae134291f5db680890e10a073fb1dff030866ed82b6831)
- [x] Step 4: REPORT.md (kill-bar verdicts, red-team self-review)
- [x] Step 5: commits local only, explicit pathspec, never push

## Commit log (this lane only)

- ca23aa436 prereg freeze: PREREG.md alone
- (this commit) implementation + runs + REPORT.md + this NAMECHECK.md
