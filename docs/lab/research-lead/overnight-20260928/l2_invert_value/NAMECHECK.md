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
- [x] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md) at ee8dca0ca, before any implementation existed.
- [x] Step 2: implementation (extended learner.zag +
      world.zag + driver.zag, concatenated to iv_full.zag,
      2797 lines), compiled with pinned znc (`znc
      iv_full.zag -o iv_bin`, rc=0, only A0102
      ignored-return-value warnings, same class as the
      parent lane).
- [x] Step 3: 3/3 runs byte-identical (sha256
      649609a2e92041a8ffb299a48bec6294b417a685b7ce04b3d64aea9f221b8e9c
      x3), K7 audit clean (frozen token allowlist +
      new-id spot check), driver tag audit 0 hits,
      REPORT.md with verdict L2-INVERT-VALUE-PASS
      (K1-K8 all PASS, 0 falsifiers, F-COUNT silent at
      333/335/324/1237/1286/1146/393). One pre-verdict
      transparent amendment (PREREG_AMENDMENT1.md):
      QV-AS 1186->1237 (prereg used pre-amendment
      parent base 1142 instead of amended 1193),
      removal of a stale duplicate F-ABLATET-T16 line,
      and corrections to two informational
      ablation-arm counts (ABLATE-TRUNC 585->497,
      ABLATE-INV QINV 1132->1183) whose parent bases
      contained errors; no counting-rule or
      learner-code change.
