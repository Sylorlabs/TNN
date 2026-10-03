# NAMECHECK: L2-INVERT-VALUE (value-mapping inversion for op 4 INVERT)

Worker: L2-INVERT-VALUE subagent (depth 2/2), 2026-10-03.
Parent mandate: complete the INVERT operator from
L2-METAREUSE-EXTEND (which achieved L2-METAREUSE-EXTEND-PASS
K1-K8 with the honest disclosure "INVERT here is
relation-sequence reversal (value-mapping inversion not
attempted)"). Implement value-mapping inversion: if a MAP
maps A->B (key->value), the inverse must map B->A
(value->key), by genuine reverse lookup + backward
execution, not just structural relseq reversal. New query
Q_INVVAL solvable only by the new form; the old structural
form must fail on it and the new form must fail on Q_INV.
Parent kill bars K1-K8 govern, adapted. Non-ledger task.
Commits local, never pushed, explicit pathspecs.

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

## Reading disclosures

- Read the parent lane `l2_metareuse_extend/` REPORT.md,
  PREREG.md, PREREG_AMENDMENT1.md, NAMECHECK.md,
  learner.zag, world.zag, driver.zag in full. This lane
  EXTENDS that harness; it does not redesign it. All
  pinned-znc-safe Zag idioms are inherited: u8-cell state
  buffer, get32/set32 helpers, cursor emit helpers with a
  single raw-syscall write, counted scan helpers,
  flag-variable style instead of deep if-nesting (3 or
  fewer), no `!(A && B)` while-conditions, no `&&` in
  conditions at all, no `as *i32` slices, no `[]u8 as *u8`
  casts, division/modulo instead of bitwise ops.
- New machinery in this lane (ex_find_objrel counted
  obj-match scan; mr_invert_val: reverse value lookup +
  backward chain walk; MAP dir flag at +39 with backward
  m_exec/chain_exec_bwd; mr_buildwin_inv; pipeline value
  read for inverse MAPs) is designed from this lane's
  frozen PREREG.md.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md) before any implementation existed.
- [ ] Step 2: implementation, build with pinned znc, 3/3
      byte-identical runs, K7 audit clean.
- [ ] Step 3: REPORT.md with verdict.
