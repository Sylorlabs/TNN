# NAMECHECK: STALE-INDEX-RECOVERY

## Step 0: Toolchain guard (executed first, before any other command)

- Worker ran with `export PATH="$HOME/safebin"` from the first command.
- `which python3` under safebin PATH: empty. `which python`: empty.
- 49 tools in ~/safebin (coreutils, git symlink, pinned znc toolchain).
- All research logic in pure Zag, compiled with the pinned znc
  `znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev), the same binary used by
  HOOK-COMPOSITION.
- Shell used only to: copy files, assemble sources, invoke znc, run the
  binary, diff/grep outputs, git add/commit with explicit pathspecs.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/stale_index/`, file prefix
`si_`. Follow-up experiment to the HOOK-COMPOSITION Amendment N1 finding:
L-state spec-procedure indexes are world-relative (fact indices into the
live world); a world restore without re-specializing made `ret_spec`
return 0 subjects, and self-trigger handled it reactively (bounded
retries, coverage retired, generic fallback, agree). This experiment asks
whether the learner can detect stale indexes BEFORE they cause
0-subject returns, which signal does it (fact count? content checksum?
world epoch?), and whether proactive recovery beats the reactive path.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every commit
  (shared branch tnn-native-lab; bare `git commit` forbidden).
- This prereg + namecheck committed ALONE, strictly before any
  implementation commit.
- No em/en dashes in lane files (hygiene bar SI-H1).
