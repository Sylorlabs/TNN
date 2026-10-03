# NAMECHECK.md -- COGOPS-COMPOSE Worker (follow-up to C408:
COGNITIVE-OPS-LEARNER MIGRATION DEMONSTRATED)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
```

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path (the safebin git
symlink has a known EPERM-on-write defect; see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the safebin `znc` symlink target; same pinned compiler as the
cognitive_ops_learner battery).

This PREREG.md + NAMECHECK.md (with this Step 0 confirmation) are committed
alone before any implementation file exists; the prereg is adopted as frozen
without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (cat), and byte verification
(cmp/sha256sum/grep).

## Scope

- Lane: `docs/lab/research-lead/overnight-20260928/cogops_compose/`
  (new). File prefix `cc_`.
- Experiment: the learner owns two specialized procedures (specialized
  RETRIEVE + specialized VERIFY, both built from experience with
  provenance) and composes them via learner-assembled plans: bindings
  discovered by trial, per-goal order derived from goal dependency
  structure, per-need versions from learned coverage, plans persisted /
  reused / re-derivable, unbindable goals declined. No
  researcher-supplied pipeline.
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
