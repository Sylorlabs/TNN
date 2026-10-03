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
- [x] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md) at a62b04c67, before any implementation existed.
- [x] Step 2: implementation (7 sealed worlds + drivers;
      learner.zag byte-identical copy of the builder's,
      sha256 698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731),
      compiled with pinned znc (`znc adv_*_full.zag -o
      adv_*_bin`, rc=0, only A0102 warnings, same class
      as the builder lanes). One pre-verdict amendment
      (PREREG_AMENDMENT1.md, committed at d0f04fe02):
      Z-id derivation correction for builds A/B (three
      taught MAPs -> ids 3,4,5 / 3,4); no counting-rule
      or learner-code change. One pre-verdict
      implementation fix: driver_X3 QA terminal 25->27
      (PREREG world spec authoritative; caught by xk2).
- [x] Step 3: 3/3 runs byte-identical per build (7
      sha256 recorded in REPORT.md), K7'/XK5' seal
      audit clean (learner byte-identical, 0
      operator/form trace tags in drivers/worlds,
      builder lanes untouched), REPORT.md with verdict
      L2-METAREUSE-ADVERSARY-PASS (core K1'-K5',K8'
      all PASS, 0 falsifiers; X XK1' boundary
      confirmed x4, XK2'-XK5' PASS, 0 falsifiers).
