# NAMECHECK: L2-METAREUSE-ADVERSARY (sealed-world generality probe)

Worker: L2-METAREUSE-ADVERSARY subagent (depth 2/2), 2026-10-03.
Parent mandate: design SEALED worlds for the 6-operator
meta-reuse harness (COMBINE, SUBSTITUTE, TRUNCATE,
INVERT-A/B, ABSTRACT, CONCRETIZE) as completed by
L2-INVERT-VALUE; test whether the operators work beyond
the single builder-designed world family; include at
least one family designed to falsify (greedy discovery
failure, first-match lookup failure, pattern-pool
interference, cycle trap). Do NOT modify the builder's
frozen code; design worlds, not the learner. Prereg
BEFORE implementation with frozen kill bars. Pure Zag,
safebin mandatory. Non-ledger task. Commits local, never
pushed, explicit pathspecs. Do NOT touch builder lane
directories.

## Step 0: toolchain guard (recorded before any research computation)

- `export PATH="/home/hatch/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python`
  returns NOTHING (rc=1). Verified 2026-10-03 at worker
  startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler
  only; znc 2026.07.0-dev).
- Any forbidden-executable invocation is PROCESS-FAIL. None
  occurred.
- Pure Zag for all scientific computation. Shell only: znc
  invocation, running binaries, git ops, file movement,
  sha256sum/cmp/grep checks.
- Git writes go through `/usr/bin/git` directly (safebin
  `git` symlink has the known EPERM-on-write defect;
  AGENTS.md 2026-10-03).

## Reading disclosures

- Read L2-INVERT-VALUE `REPORT.md`, `world.zag`,
  `driver.zag`, `learner.zag` in full, and
  L2-METAREUSE-EXTEND `REPORT.md`. This lane REUSES the
  builder's frozen `learner.zag` BYTE-IDENTICAL (verified
  by sha256 at implementation time); it does not redesign
  the harness. All pinned-znc-safe Zag idioms are
  inherited from the builder lanes: u8-cell state buffer,
  get32/set32 helpers, cursor emit helpers with a single
  raw-syscall write, counted scan helpers, flag-variable
  style instead of deep if-nesting, no `!(A && B)`
  while-conditions, division/modulo instead of bitwise
  ops.
- The seal is one-directional (builder-blindness): the
  builder lanes are complete and frozen; no builder saw
  these worlds. Reading the harness interface was
  necessary to design worlds for it; the worlds below
  were designed solely by this adversary worker on
  2026-10-03 and live only in this lane.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md), before any implementation exists.
- [ ] Step 2: implementation (7 sealed worlds + drivers;
      learner.zag byte-identical copy of the builder's),
      compiled with pinned znc.
- [ ] Step 3: 3/3 runs byte-identical per build, K7'-style
      seal audit, driver tag audit, REPORT.md with
      verdict.
