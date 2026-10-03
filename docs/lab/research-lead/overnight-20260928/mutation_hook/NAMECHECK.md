# NAMECHECK: MUTATION-HOOK

## Step 0: Toolchain guard (executed first, before any other command)

- This worker's first exec calls were read only recon (`ls`, `grep`,
  `find`, `git status`, `git branch`): no interpreter was invoked for
  research logic, and no research artifact was produced.
- `export PATH="$HOME/safebin"` used for all subsequent commands.
- `which python3` under safebin PATH: empty. `which python`: empty.
  `which znc` resolves to `/home/hatch/safebin/znc` (pinned znc).
- Micro-probes of Zag language capability (function values,
  indirect calls, memory round-trip) were compiled and run with the
  pinned znc under the safebin PATH. Pure Zag in the probes; shell
  only to invoke znc and run the binaries. Probe sources lived in
  /tmp (ephemeral); nothing durable was produced from them.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/mutation_hook/`, file
prefix `mh_`. Follow-up to EPOCH-STRONG (11/11 green, null result
with teeth), which recommended: do not retry learner-created
stamping until the prerequisite machinery exists (executable-graph
construction + learner-writable mutation hooks + failure attribution
to missing mechanisms).

This task is ANALYTICAL, not an implementation wave: investigate
what it would take for the learner to install a hook on the
mutation path, decompose the six preregistered capabilities
(A2.1-A2.6) by build difficulty and protected-core implications,
and sketch an incremental path. No experiment was run, so no
prereg was required and none was written. The only compiled code in
this lane is throwaway toolchain micro-probes in /tmp.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every commit
  (shared branch tnn-native-lab; bare `git commit` forbidden).
- If git writes fail with EPERM through the safebin symlink, retry via
  /usr/bin/git directly (AGENTS.md lesson, XP-HIERNAV-1).
- On index.lock contention, retry with sleep backoff; never remove the
  lock while other workers are active.
- No em/en dashes in lane files (hygiene discipline from ES-H1).
