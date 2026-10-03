# NAMECHECK: L2-METAREUSE-COMPOSE (operator composition probe)

Worker: L2-METAREUSE-COMPOSE subagent (depth 2/2), 2026-10-03.
Parent mandate: investigate whether the six meta-reuse
operators are composable, i.e. whether the Z-structure
produced by one operator can serve as the source for
another operator; whether the fixed-order [1..6]
enumeration needs to become a search over operator
sequences; what the termination conditions are. Build
on L2-METAREUSE-ADVERSARY (frozen 6-operator harness).
Prereg BEFORE implementation with frozen kill bars.
Pure Zag, safebin mandatory. Non-ledger task (claim
minting paused). Commits local, never pushed, explicit
pathspecs. Do NOT break the existing 6-operator
behavior: the seven sealed adversary builds must still
pass as regression.

## Step 0: toolchain guard (recorded before any research computation)

- `export PATH="/home/hatch/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python`
  returns NOTHING (rc=1). Verified 2026-10-03 at worker
  startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler
  only).
- Any forbidden-executable invocation is PROCESS-FAIL. None
  occurred.
- Pure Zag for all scientific computation. Shell only: znc
  invocation, running binaries, git ops, file movement,
  sha256sum/cmp/grep checks.
- Git writes go through `/usr/bin/git` directly (safebin
  `git` symlink has the known EPERM-on-write defect;
  AGENTS.md 2026-10-03).
- Pinned-znc-safe idioms inherited from the builder lanes:
  u8-cell state, get32/set32 helpers, cursor emit helpers
  with a single raw-syscall write, flag-variable style,
  no `!(A && B)` while-conditions, division/modulo instead
  of bitwise ops, no `as *i32` slice construction.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md) before any implementation exists.
- [ ] Step 2: implementation (extended learner with
      composition phase 2; build D composition world +
      drivers; frozen-learner control binary; 7 sealed
      regression builds against the extended learner),
      compiled with pinned znc.
- [ ] Step 3: 3/3 byte-identical runs per build, REPORT.md
      with verdict.
