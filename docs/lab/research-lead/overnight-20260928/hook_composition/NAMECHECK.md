# NAMECHECK: HOOK-COMPOSITION

## Step 0: Toolchain guard (executed first, before any other command)

- Worker ran with `export PATH="$HOME/safebin"` from the first command.
- `which python3` under safebin PATH: empty. `which python`: empty.
- 49 tools in ~/safebin (coreutils, git symlink, pinned znc toolchain).
- All research logic in pure Zag, compiled with the pinned znc
  `znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev), same binary used by
  INTEGRATION-COMBINED and INTEGRATION-HOOK-GENERALIZE.
- Shell used only to: copy files, assemble sources, invoke znc, run the
  binary, diff/grep outputs, git add/commit with explicit pathspecs.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/hook_composition/`, file
prefix `hc_`. Merge the generalized hook battery (multi-need, lazy,
coverage-aware, retirement) from INTEGRATION-HOOK-GENERALIZE into the
INTEGRATION-COMBINED binary (self-trigger + hook + B1/B2). Additive
only: no redesign of either predecessor.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every commit
  (shared branch tnn-native-lab; bare `git commit` forbidden).
- This prereg + namecheck committed ALONE, strictly before any
  implementation commit.
- No em/en dashes in lane files (hygiene bar HK-G8).
