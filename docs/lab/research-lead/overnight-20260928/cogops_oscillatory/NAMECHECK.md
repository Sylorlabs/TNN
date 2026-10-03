# NAMECHECK.md -- COGOPS-OSCILLATORY Worker (follow-up to COGOPS-CYCLES C442)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
sh ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
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
(the same pinned compiler as the cogops_cycles battery).

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

- Lane: `docs/lab/research-lead/overnight-20260928/cogops_oscillatory/`
  (new). File prefix `c6_`.
- Experiment: two oscillatory cycle goals (818 self-loop, 819 2-node)
  on a period-2 workload (world D, rel 606 2-cycle 661<->662, rel 608
  markers) run through the byte-identical C442 generalized composer;
  a convergent control (goal 816, world C) in the same binary.
  Predicted INFORMATIVE-FAIL (mechanism): the 16-pass cap fires on
  both oscillatory goals (quiescence unreachable), the emitted answers
  are deterministic phase artifacts (not fixpoints, proven by the
  stability probe), while the same composer converges (passes=9)
  where a fixpoint exists.
- Composer identity: c6_base.zag = c5_base.zag and c6_learn.zag =
  c5_learn.zag byte-identical (cmp-verified); no new composer
  functions. New code only in c6_world.zag (environment) and
  c6_main.zag (driver/oracles/probes).
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
