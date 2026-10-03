# NAMECHECK.md - SUBSUMPTION-P0 worker

## Step 0: Toolchain Guard (mandatory, recorded first)

Executed before any work, 2026-10-03:
```
export PATH="$HOME/safebin"
which python3; which python; echo "python-check-done(empty=good)"
```
Result: `which python3` and `which python` printed nothing;
`python-check-done(empty=good)`. Safebin was exported on the very
first command of this session, before any file was read or written.
Pinned znc 2026.07.0-dev via safebin.

Commitment: all research logic in pure Zag via the pinned znc. Shell
only for safebin setup, znc invocation, binary runs, sha256sum, greps,
byte-verification, and git. No forbidden executable will be invoked;
any such invocation is PROCESS-FAIL for this wave per governance.

## Scope

Preregistered subsumption test (COMPOSITION-SYNTHESIS C436 P0): can
the frozen C424 5-op contract module (induct/check/grow/invalidate/
revise, byte-copied verbatim) reproduce COGOPS-DIAMOND's results
(goals 813/814/815/808, decline control 810), or does procedure
composition require distinct machinery? Arms B1 (bindings), B2
(version routing), V (step verification), E (generation attempt),
F (flat-memorization control). Frozen predicted outcome:
INFORMATIVE-FAIL / PARTIAL SUBSUMPTION: bindings and version
routing subsume; plan assembly, execution, and step verification
do not. Two mechanisms.

## Constraints honored

- Prereg commit-order self-check: PREREG.md + NAMECHECK.md committed
  alone before any implementation file exists in this lane.
- Commits local only, never pushed, explicit pathspecs; never
  `git reset` on the shared branch; explicit pathspec on every
  commit; /usr/bin/git absolute path if the safebin symlink EPERMs.
- Zero em/en dash bytes in lane docs (byte-verified before commit).
- Opaque integer identifiers throughout; the module never sees a
  scenario identifier; the harness contains no topo sort, no
  procedure executor, no plan records (K8/F3 audit).
- AGENTS.md toolchain workarounds apply: u8-backed state with
  get32/set32, single-buffer emit with e1str/e1i64 helpers and one
  raw syscall flush, no `as *i32` slice construction in functions,
  no `!(A && B)` in while conditions, if-nesting at most 3 with
  hoisted flags, `_zag_malloc as *u8` allocation threading, no
  `[]u8 as *u8` casts, no `_zag_print` for dynamic content.
