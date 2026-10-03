# NAMECHECK.md -- INTEGRATION-B1B2 Worker (C443 follow-up: port B1/B2 into COGOPS)

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
cogops_diamond and subsumption_p0 batteries).

This PREREG.md + NAMECHECK.md (with this Step 0 confirmation) are committed
alone before any implementation file exists; the prereg is adopted as frozen
without modification.

## Forbidden executable attestation

Zero invocations of python3, python, or any other forbidden executable during
this task. All scientific computation is pure Zag (znc-compiled binaries).
Shell is used only for: safebin PATH export, znc invocation, binary execution,
git operations, file assembly (cat), and byte verification
(cmp/sha256sum/grep/diff).

Zag miscompile workarounds honored per AGENTS.md: get32/set32 only on u8
state (no `as *i32` slice construction); single-buffer emit with one raw
syscall flush (no _zag_print for dynamic content); no `!(A && B)` in while
conditions; if-nesting at most 3; allocation via _zag_malloc as *u8 threaded
through; no []u8 as *u8 casts.

## Scope

- Lane: `docs/lab/research-lead/overnight-20260928/integration_b1b2/`
  (new). File prefix `ib_`.
- Experiment: port C443's B1 (trial-learned bindings as per-tag admission
  contracts with invalidate/revise) and B2 (spec-vs-gen routing as coverage
  admission with drift revision) into the COGOPS-DIAMOND composer,
  replacing its BIND trial-count table and coverage-membership version
  routing at the binding layer. Test whether the composer gains
  revision-under-counterevidence (new stages S9A/S9B) without losing any
  of its procedure composition ability (C433's S1A-S8 frozen outcomes).
  Minimal port: 4 of the 5 u_* ops (u_grow excluded); plan assembly, topo
  order, procedure bodies, execution, and oracles are C433's logic
  unchanged.
- No other lane directories touched. Commits use explicit pathspecs on the
  current branch; nothing pushed.

## Prereg ordering

PREREG.md + this NAMECHECK.md are committed alone before any implementation
file exists. Self-check: `git log` must show the prereg commit strictly
before the implementation commit.
