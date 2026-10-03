# NAMECHECK.md - CONTRACT-UNIFICATION worker (C418)

## Step 0: Toolchain Guard (mandatory, recorded first)

Executed before any work, 2026-10-03:
```
export PATH="$HOME/safebin"
which python3; which python; echo "python-check-done(empty=good)"
which znc; znc --version
```
Result: `which python3` and `which python` printed nothing;
`python-check-done(empty=good)`. znc resolves to
`/home/hatch/safebin/znc`, version `znc 2026.07.0-dev (edition 2026)`
(the pinned compiler). Safebin holds 49 allowed tools; python3/python
do not resolve. Safebin active for every subsequent command.

Commitment: all research logic in pure Zag via the pinned znc. Shell
only for safebin setup, znc invocation, binary runs, sha256sum, greps,
and git. No forbidden executable will be invoked; any such invocation
is PROCESS-FAIL for this wave per governance.

## Scope

Implement and test the COMPRESSION-AUDIT candidate-1 design
(CONTRACT-UNIFICATION): one learned-contract module with operations
induct / check / grow / invalidate / revise, tested against LCONT's
frozen drift scenario and FC's frozen grammar scenario plus an
ablation arm. Prereg frozen before implementation (this commit).

## Constraints honored

- Prereg commit-order self-check: PREREG.md + NAMECHECK.md committed
  alone before any implementation file exists.
- Commits local only, never pushed, explicit pathspecs.
- Zero em/en dash bytes in lane docs (byte-verified before commit).
- Opaque integer identifiers in the unified module; no per-scenario
  branches (F3); the scenario identifier never appears in the module.
- AGENTS.md toolchain workarounds apply: u8-backed state with
  get32/set32, single-buffer emit with e1str/e1i64 helpers and one raw
  syscall flush, no `as *i32` slice construction in functions, no
  `!(A && B)` in while conditions, if-nesting at most 3 with hoisted
  flags. `_zag_malloc as *u8` threading pattern for allocation.
