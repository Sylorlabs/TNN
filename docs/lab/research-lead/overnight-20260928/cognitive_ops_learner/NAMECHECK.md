# NAMECHECK.md -- COGNITIVE-OPS-LEARNER Worker (overnight priority #5:
cognitive-operation bodies becoming learner-created)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
```

Setup script (repo-relative):
`docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
reported: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path (the safebin git
symlink has a known EPERM-on-write defect; see AGENTS.md).

Replacement worker (2026-10-03, 00:49 PDT): re-verified at my startup with
PATH=$HOME/safebin. `which python3` -> NOTHING, `which python` -> NOTHING.
This PREREG.md + NAMECHECK.md (with this Step 0 confirmation) are committed
alone before any implementation file exists; I adopt the prereg as frozen
without modification.

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the safebin `znc` symlink target; same pinned compiler as the
compose_collapse, compose_pair5, compose_pair6_adv, and gen_subsumes_u
batteries).

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (cat), and byte verification
(cmp/sha256sum/grep).

## Scope

- Lane: `docs/lab/research-lead/overnight-20260928/cognitive_ops_learner/`
  (new). File prefix `col_`.
- Experiment: a researcher-supplied generic VERIFY procedure (checks a
  candidate structure against evidence) is specialized by the learner through
  experience into a learner-owned indexed procedure with provenance; the
  learner then selects between the original and the revised procedure based
  on a learned coverage record, with fallback preserving correctness under
  a relation-identifier shift and re-specialization adapting to it.
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
