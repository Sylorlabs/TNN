# NAMECHECK: HOOK-PHASE1

## Step 0: Toolchain guard (executed first, before any other command)

- This worker's first exec calls were read-only recon (`ls`, `grep`,
  `sed`, `wc`, `which`): no interpreter was invoked for research
  logic, and no research artifact was produced.
- The lane directory was created with `mkdir` under the safebin PATH.
- From here on, every build/run/verify command runs with
  `export PATH="$HOME/safebin"` inline.
- `which python3` under safebin PATH: empty. `which python`: empty.
- `which znc` resolves to `/home/hatch/safebin/znc` (pinned znc
  2026.07.0-dev, the same binary used by HOOK-PHASE0 and
  EPOCH-STRONG). The compile binary used is
  `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- All research logic in pure Zag, compiled with the pinned znc.
  Shell used only to: copy files, assemble sources, invoke znc, run
  the binary, diff/grep outputs, git add/commit with explicit
  pathspecs.
- If any forbidden interpreter is invoked, this wave is PROCESS-FAIL.

## Scope

Non-ledger task (claim minting paused). Lane
`docs/lab/research-lead/overnight-20260928/hook_phase1/`, file prefix
`hq_`. Follows MUTATION-HOOK's incremental path: "Phase 1 (A2.3
inert dispatch, no governance)".

This wave implements Phase 1 only:
- A2.3: hook dispatch infrastructure (inert). Hook slot consult in
  both mutation functions (`fact_add`, `fact_set_obj`), slot default
  0 = no hook. Install/uninstall helpers and the dispatch routine.
- Built on HOOK-PHASE0 (A2.6 event counter + A2.1 allocator/registry);
  no redesign of Phase 0.

Explicitly NOT in scope: A2.2 (learner-created operation bodies,
gated on Micah's pending EXECUTE placement ruling), A2.4, A2.5, and
the strong sense of A2.3. The installed probe body is
RESEARCHER-WRITTEN; any "hook fired" observation is a dispatch
test, not invention. Per MUTATION-HOOK G3/G4, the fn-value table
must never be reported as invention progress: learner selection
among researcher-written bodies is menu selection under the L3 bar.

This is infrastructure, not invention. Nothing in this lane claims
the learner learned, invented, or stamped anything. The bars test
substrate mechanics only: the consult is inert with slot 0, dispatch
calls the right slot exactly once per mutation, payload plumbing is
exact, uninstall restores inertness, and all pre-existing outputs
are byte-identical.

## Pre-prereg toolchain finding (kept in /tmp, not a lane artifact)

The fn-value round-trip through S cells (MUTATION-HOOK T2 pattern)
was re-verified on the pinned znc before freezing the design, and a
latent ASLR hazard was found and fixed: reloading the i64 bits with
`(get32(S,off) as i64)` sign-extends bit 31, corrupting bits 32..63
of the fn address whenever the code address has bit 31 set, which
segfaulted intermittently under ASLR (unmasked form: 5/6 segfaults
on one binary, 4/10 on another). Masking the low half
(`(get32(S,off) as i64)&4294967295`) makes the round-trip exact;
the full install/fire/uninstall pattern ran 12/12 stable (exit 42).
The frozen design uses the masked reload. Probe files live in /tmp
only.

## Commit discipline

- Commits local only, never pushed. Explicit pathspecs on every
  commit (repo `tnn-rsi-gpi3`, branch `tnn-native-lab`; bare
  `git commit` forbidden).
- This prereg + namecheck committed ALONE, strictly before any
  implementation commit (prereg commit-order self-check).
- If git writes fail with EPERM through the safebin symlink, retry
  via /usr/bin/git directly (AGENTS.md lesson, XP-HIERNAV-1).
- On index.lock contention, retry with sleep backoff; never remove
  the lock while other workers are active.
- No em/en dashes in lane files (hygiene bar HQ-H1).
