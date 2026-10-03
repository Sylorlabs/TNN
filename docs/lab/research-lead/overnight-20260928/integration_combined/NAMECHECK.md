# NAMECHECK.md -- INTEGRATION-COMBINED Worker (self-trigger + plan-invalidation hook + B1/B2)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
```

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)

The safebin itself is present at $HOME/safebin (36 tools, no
python) and is used directly. PATH is restricted to
$HOME/safebin for every command in this task.

Result: PASS. No python3/python reachable in PATH. All
subsequent commands in this task run with PATH=$HOME/safebin
(exported in every shell invocation). Git write operations
use /usr/bin/git by absolute path (the safebin git symlink
has a known EPERM-on-write defect; see AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the safebin `znc` symlink target; same pinned compiler as
the integration_selftrig and integration_stress batteries).

This PREREG.md + NAMECHECK.md (with this Step 0 confirmation)
are committed alone before any implementation file exists;
the prereg is adopted as frozen without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden
executable during this task. All scientific computation is
pure Zag (znc-compiled binaries). Shell is used only for:
safebin PATH export, znc invocation, binary execution, git
operations, file assembly (cat), and byte verification
(cmp/sha256sum/grep/diff).

Zag miscompile workarounds honored per AGENTS.md:
get32/set32 only on u8 state (no `as *i32` slice
construction); single-buffer emit with one raw syscall flush
(no _zag_print for dynamic content); no `!(A && B)` in while
conditions; if-nesting at most 3; allocation via _zag_malloc
as *u8 threaded through; no []u8 as *u8 casts.

## Scope

- Lane:
  `docs/lab/research-lead/overnight-20260928/integration_combined/`
  (new). File prefix `cb_`.
- Experiment: combine the three mechanisms (self-triggered
  revision from INTEGRATION-SELFTRIG, the plan-invalidation
  hook motivated by INTEGRATION-STRESS IS-D, the integrated
  B1/B2 contracts from C455) in one binary and test for
  interference: Act 1 reruns S1A-S10F byte-identical (hook
  dormant); Act 2 stages a B1 tag-shape collision (IS-D
  apparatus) and verifies the hook rebuilds the stale plan
  in the live query path with no clear_plans.
- Build on C455/C461 foundations; the u_* module bodies are
  untouched (byte-copy). The hook is additive in compose's
  hit path only.
- No other lane directories touched. Commits use explicit
  pathspecs on the current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any
implementation file exists. Self-check: `git log` must show
the prereg commit strictly before the implementation commit.
