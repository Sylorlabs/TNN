# Safebin Rollout: restricted PATH as the default for builder workers

Date: 2026-09-30
Status: SAFEBIN-ROLLOUT-READY

## Problem

Python Audit 2 (commit `4a97c985c`) found that only 1 of 16 workers used a
true restricted PATH where `python3` was absent. The other 15 relied on
documented non-use. Twelve Python incidents have now been recorded, all from
workers with `python3` in PATH. Zero incidents have come from safebin workers.

The pattern is not malice. `python3` is the path of least resistance for
trivial tasks: a stray `-c "pass"` prefix, arithmetic sums, em-dash byte
checks. Documented non-use does not survive contact with muscle memory. An
absent binary does.

## Technique

`$HOME/safebin` is a directory containing symlinks to exactly the allowed
toolchain and nothing else:

- 35 coreutils-style tools: awk basename cat chmod cmp cp cut date diff
  dirname echo find git grep head ls mkdir mv od printf rm sed sha256sum
  sleep sort stat tail tee timeout touch tr uname uniq wc xargs
- `znc`: symlink to the pinned compiler
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1` (absolute repo path, never
  a PATH-resolved copy)

A worker activates it with:

```sh
export PATH="$HOME/safebin"
```

After that, any `python3` or `python` invocation fails immediately with
"command not found". The failure is loud, local, and leaves no ambiguity
about whether the guard held.

Setup is idempotent and scripted:

```sh
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
```

The script links the tools, verifies `python3`/`python` do not resolve under
the safebin PATH (using the shell builtin `command -v`), and exits nonzero
on any failure. It invokes no Python itself.

Prior art: the MUL builder and the inquiry re-freeze worker both ran their
full waves under `$HOME/safebin` with zero incidents.

## Mandate

Effective immediately, all future builder workers (any worker that compiles
Zag, runs binaries, or performs build-adjacent shell work) must:

1. Run `setup_safebin.sh` (or verify an existing `$HOME/safebin`) at startup.
2. Export `PATH="$HOME/safebin"` before any build, test, or verification step.
3. Record the safebin activation in NAMECHECK.md Step 0, including the
   `command -v python3 python` empty result.

Documentation-only and analysis-only workers (ledger appends, audits,
triage) are encouraged but not required to use the safebin; their Step 0
guard record stands as before. The incident record shows the risk
concentrates in build/test/verify loops, so the mandate targets builders.

If a builder has a legitimate technical reason the safebin cannot work
(e.g. a tool outside the allowed set is genuinely required), the worker
must document the reason in NAMECHECK.md Step 0 and obtain no exception
from the guard itself: any forbidden invocation remains PROCESS-FAIL
regardless of justification. "Surgical PATH removal not possible" is no
longer accepted without a specific, verifiable technical cause, since two
workers have proven it is possible.

## Updated worker spawn template language

Replace the old toolchain guard paragraph in builder spawn messages with:

> **TOOLCHAIN GUARD (Step 0, mandatory):** This is a builder wave. At
> startup, run
> `sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
> and then `export PATH="$HOME/safebin"` before any build, test, or
> verification step. Confirm `command -v python3 python` prints nothing.
> Record the safebin activation and the empty result in NAMECHECK.md Step 0.
> All computational research must use Zag. Shell only: invoke znc, run
> binaries, git ops, move/copy files. If a forbidden executable is invoked,
> this wave is automatically PROCESS-FAIL.

For non-builder workers, keep the existing Step 0 language (run
`which python3 python`, record the result, document non-use).

## Rollout verification

The coordinator should spot-check the next three builder waves for:

- NAMECHECK.md Step 0 records safebin activation (not just `which` output).
- No `python3`/`python` in the worker's effective PATH during build steps.
- Any incident still self-disclosed per the existing disclosure norm.

If a builder wave lands without the safebin record, treat it as a process
finding in the next Python audit, not as a silent pass.

## Files

- `setup_safebin.sh` (this directory): idempotent setup + verification.
- `SAFEBIN_ROLLOUT.md` (this file): mandate and template language.
- `NAMECHECK.md` (this directory): Step 0 guard record for this wave.
