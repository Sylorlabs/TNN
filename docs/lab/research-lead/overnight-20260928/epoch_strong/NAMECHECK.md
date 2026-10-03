# NAMECHECK: EPOCH-STRONG

## Step 0: Toolchain guard (executed first, before any other command)

- This worker's first exec calls ran on the default PATH and were
  read only recon (`ls`, `grep`, `which`): no interpreter was invoked
  for research logic, and no research artifact was produced.
- The lane directory was created with `mkdir` under the safebin PATH.
- From here on, every build/run/verify command runs with
  `export PATH="$HOME/safebin"` inline.
- `which python3` under safebin PATH: empty. `which python`: empty.
- 38 tools in ~/safebin (coreutils, git symlink, pinned znc toolchain).
- All research logic in pure Zag, compiled with the pinned znc
  `znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev), the same binary used
  by STALE-INDEX-RECOVERY and LEARNER-EPOCH.
- Shell used only to: copy files, assemble sources, invoke znc, run
  the binary, diff/grep outputs, git add/commit with explicit
  pathspecs.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/epoch_strong/`, file prefix
`es_`. Follow-up to LEARNER-EPOCH (all 9 kill bars green), which left
open: "learner-created stamping (strong sense of priority 5): the
learner installs or revises the stamping operation itself from
experience of a missed-bump failure, rather than receiving it by
placement."

This experiment is a preregistered capability-gap probe: the
researcher-designed stamping is REMOVED (no versioning installed),
the learner is given the exact staleness-failure experience that
should motivate invention, and frozen kill bars discriminate
presence vs absence of every invention signature. Predicted outcome
is absence, with the missing capabilities named. A null result with
teeth, not a theater of invention: writing the invention in Zag
source would be the weak sense one level removed.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every commit
  (shared branch tnn-native-lab; bare `git commit` forbidden).
- This prereg + namecheck committed ALONE, strictly before any
  implementation commit.
- If git writes fail with EPERM through the safebin symlink, retry via
  /usr/bin/git directly (AGENTS.md lesson, XP-HIERNAV-1).
- On index.lock contention, retry with sleep backoff; never remove the
  lock while other workers are active.
- No em/en dashes in lane files (hygiene bar ES-H1).
