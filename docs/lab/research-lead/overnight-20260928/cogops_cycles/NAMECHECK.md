# NAMECHECK.md -- COGOPS-CYCLES Worker (follow-up to COGOPS-DIAMOND C433)

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
- setup_safebin.sh reports: SAFEBIN-READY (no python)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path (the safebin git
symlink has a known EPERM-on-write defect; see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned compiler as the cogops_diamond battery).

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

- Lane: `docs/lab/research-lead/overnight-20260928/cogops_cycles/`
  (new). File prefix `c5_`.
- Experiment: two phases on cycle goals for learner-owned procedures.
  Phase 1 (frozen C433 machinery, predicted INFORMATIVE-FAIL): the
  self-loop goal 816 and the 2-node VERIFY->RETRIEVE cycle goal 817
  cannot be composed by single-pass topo execution (self-link reads
  zeros; Kahn emits the corrupt order [0,0,2,1] on the 2-cycle).
  Phase 2 (preregistered additive generalization, predicted PASS):
  topo_g (stall-aware topo with deterministic fallback),
  apply_kind1_g (uniform non-empty-source link rule),
  execute_plan_iter (change-driven iterated execution to
  quiescence with a frozen pass cap of 16), compose_iter.
  Both cycle goals iterate learner-owned RETRIEVE/VERIFY to the
  taught fixpoint at lower check cost than all-generic oracles;
  the C433 diamond/chain/decline battery reproduces exactly.
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
