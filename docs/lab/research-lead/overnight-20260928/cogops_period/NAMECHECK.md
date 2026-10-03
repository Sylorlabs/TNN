# NAMECHECK.md -- COGOPS-PERIOD Worker (follow-up to COGOPS-OSCILLATORY C451)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
```

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc
- setup_safebin.sh reports: SAFEBIN-READY (36 tools, no python)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path (the safebin git
symlink has a known EPERM-on-write defect; see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned compiler as the cogops_oscillatory battery).

This PREREG.md + NAMECHECK.md (with this Step 0 confirmation) are committed
alone before any implementation file exists; the prereg is adopted as frozen
without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (cat/cp/cmp), and byte verification
(cmp/sha256sum/grep).

## Scope

- Lane: `docs/lab/research-lead/overnight-20260928/cogops_period/`
  (new). File prefix `c7_`.
- Experiment: period-detection halting vocabulary in learner-owned
  state, additive on the C442/C451 composer. Two period-2 goals
  (818 self-loop, 819 2-node, world D) plus a new period-3 goal
  (820 self-loop, world E: rel 612 3-cycle, rel 613 markers),
  run through the period-aware composer (compose_iter_pd);
  a convergent control (goal 816, world C) in the same binary.
  Predicted BUILD-PASS (mechanism): period-2 detected and
  reported with full orbit at passes 3 and 4 (not the 16-pass
  cap), period-3 detected at pass 4, convergent control
  reproduces C451 byte-exactly (passes=9, halt=conv).
- Composer additivity: c7_base.zag = c6_base.zag byte-identical
  (cp + cmp); c7_learn.zag = c6_learn.zag bytes + purely additive
  period-detection section (prefix-verified by head -c + cmp);
  no existing composer function modified. New code only in the
  additive learn section (generic machinery + learner-state
  history/outcome), c7_world.zag (environment: world E,
  patterns, goal 820), and c7_main.zag (driver/oracles/probes).
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
