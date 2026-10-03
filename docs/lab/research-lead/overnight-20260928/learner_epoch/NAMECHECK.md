# NAMECHECK: LEARNER-EPOCH

## Step 0: Toolchain guard (executed first, before any other command)

- This worker's first two exec calls ran on the default PATH and were
  read only recon (`ls`, `which python3`): no interpreter was invoked
  for research logic, and no research artifact was produced.
- From the third exec call onward, every command ran with
  `export PATH="$HOME/safebin"` inline.
- `which python3` under safebin PATH: empty. `which python`: empty.
- 49 tools in ~/safebin (coreutils, git symlink, pinned znc toolchain).
- All research logic in pure Zag, compiled with the pinned znc
  `znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev), the same binary used
  by STALE-INDEX-RECOVERY.
- Shell used only to: copy files, assemble sources, invoke znc, run
  the binary, diff/grep outputs, git add/commit with explicit
  pathspecs.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/learner_epoch/`, file prefix
`le_`. Follow-up to STALE-INDEX-RECOVERY (all 8 kill bars green):
there the world epoch (state slot 931) was bumped by stage code
(`ss(S2,931,sg(S2,931)+1)` after every world mutation in S13), while
the content checksum was the only signal the learner computed
unilaterally from the world. This experiment moves epoch stamping into
the learner's own world-mutation operations (`fact_add`,
`fact_set_obj`), so the mutation itself stamps the epoch with no
caller cooperation, and reruns the stale-index battery with zero
stage-code epoch writes.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every commit
  (shared branch tnn-native-lab; bare `git commit` forbidden).
- This prereg + namecheck committed ALONE, strictly before any
  implementation commit.
- No em/en dashes in lane files (hygiene bar LE-H1).
