# NAMECHECK.md -- DISAGREEMENT-ATTRIBUTION Worker (learner-owned probe for F4)

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
(the same pinned compiler as the integration_combined battery).

This PREREG.md + NAMECHECK.md (with this Step 0 confirmation)
are committed alone before any implementation file exists;
the prereg is adopted as frozen without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden
executable during this task. All scientific computation is
pure Zag (znc-compiled binaries). Shell is used only for:
safebin PATH export, znc invocation, binary execution, git
operations, file assembly (cat/sed), and byte verification
(cmp/sha256sum/grep).

Zag miscompile workarounds honored per AGENTS.md:
get32/set32 only on u8 state (no `as *i32` slice
construction); single-buffer emit with one raw syscall flush
(no _zag_print for dynamic content); no `!(A && B)` in while
conditions; if-nesting at most 3; allocation via _zag_malloc
as *u8 threaded through; no []u8 as *u8 casts. The probe's
per-family coverage checks are factored into small helper
functions to keep if-nesting shallow.

## Scope

- Lane:
  `docs/lab/research-lead/overnight-20260928/disagreement_attribution/`
  (new). File prefix `da_`.
- Experiment: build the learner-owned disagreement-attribution
  probe (attr_probe) into INTEGRATION-COMBINED's do_query retry
  loop (additive; trigger B, the M3 hook, and contracts untouched),
  stage 16 purpose-built collision trials (8 BIND tag-shape
  collisions, 8 COV drift-stale-coverage) plus 4 CLEAN trials, and
  test whether the probe attributes the disagreement source with
  evidence that discriminates attribution from guessing (null
  always-BINDING probe control).
- Build on INTEGRATION-COMBINED: da_base.zag and da_module.zag are
  byte-copies (cmp-verified); da_world.zag extends cb_world.zag
  (world A3 deletion drift + trial tables/goal builders);
  da_learn.zag extends cb_learn.zag (attr_probe + helpers);
  da_main.zag is new (trial battery, oracle_1cnt, scoring).
- No other lane directories touched. Commits use explicit
  pathspecs on branch tnn-native-lab; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any
implementation file exists. Self-check: `git log` must show
the prereg commit strictly before the implementation commit.
