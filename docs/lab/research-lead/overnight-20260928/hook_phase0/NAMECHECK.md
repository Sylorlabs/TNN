# NAMECHECK: HOOK-PHASE0

## Step 0: Toolchain guard (executed first, before any other command)

- This worker's first exec calls were read-only recon (`ls`, `grep`,
  `find`, `which`, `sed`, `wc`): no interpreter was invoked for
  research logic, and no research artifact was produced.
- The lane directory was created with `mkdir` under the safebin PATH.
- From here on, every build/run/verify command runs with
  `export PATH="$HOME/safebin"` inline.
- `which python3` under safebin PATH: empty. `which python`: empty.
  `which znc` resolves to `/home/hatch/safebin/znc` (pinned znc
  2026.07.0-dev, the same binary used by EPOCH-STRONG).
- All research logic in pure Zag, compiled with the pinned znc.
  Shell used only to: copy files, assemble sources, invoke znc, run
  the binary, diff/grep outputs, git add/commit with explicit
  pathspecs.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/hook_phase0/`, file prefix
`hp_`. Follows MUTATION-HOOK's recommendation: "approve Phases 0-1
(event stream, allocator, inert dispatch; preregistered, pure Zag)
as infrastructure when capacity allows; keep Phases 2+ gated."

This wave implements Phase 0 only:
- A2.6: mutation-event observability (event counter bumped by
  fact_add/fact_set_obj in lane base).
- A2.1: learner-allocated persistent state (bump allocator over a
  carved S region + learner-writable registry table).

Explicitly NOT in scope: A2.2 (learner-created operation bodies,
gated on Micah's pending EXECUTE placement ruling), A2.3-A2.5
(Phase 1+). The fn-value hook table (T1/T2) is not installed here.

This is infrastructure, not invention. Nothing in this lane claims
the learner learned, invented, or stamped anything. The bars test
substrate mechanics only: the counter advances exactly once per
mutation event, the allocator is stable across calls, the registry
round-trips, and all pre-existing outputs are byte-identical with
the new machinery present.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every commit
  (shared branch tnn-native-lab; bare `git commit` forbidden).
- This prereg + namecheck committed ALONE, strictly before any
  implementation commit (prereg commit-order self-check).
- If git writes fail with EPERM through the safebin symlink, retry via
  /usr/bin/git directly (AGENTS.md lesson, XP-HIERNAV-1).
- On index.lock contention, retry with sleep backoff; never remove the
  lock while other workers are active.
- No em/en dashes in lane files (hygiene bar HP-H1).
