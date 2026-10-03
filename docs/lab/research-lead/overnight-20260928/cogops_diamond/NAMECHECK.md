# NAMECHECK.md -- COGOPS-DIAMOND Worker (follow-up to COGOPS-3WAY C422)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
sh ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
```

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)
- setup_safebin.sh reports: SAFEBIN-READY (36 tools, no python)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path (the safebin git
symlink has a known EPERM-on-write defect; see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the safebin `znc` symlink target; same pinned compiler as the
cogops_3way battery).

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

- Lane: `docs/lab/research-lead/overnight-20260928/cogops_diamond/`
  (new). File prefix `c4_`.
- Experiment: the learner owns three specialized procedures
  (specialized RETRIEVE id 2 + specialized VERIFY id 3 +
  specialized COUNT id 5, all built from experience with
  provenance) and composes them via learner-assembled plans over
  DIAMOND goals (fan-out then fan-in): bindings discovered by
  trial over three families, topo assembly over goal links
  (including multi-source fan-in), per-need versions from
  learned coverage, plans persisted / reused / re-derivable,
  unbindable goals declined. One preregistered generic
  generalization of the fan-in link semantics
  (multi-source apply_kind3; chain behavior unchanged); no
  diamond handler.
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
