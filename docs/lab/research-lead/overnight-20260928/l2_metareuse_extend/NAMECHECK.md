# NAMECHECK: L2-METAREUSE-EXTEND (INVERT / ABSTRACT / CONCRETIZE)

Worker: L2-METAREUSE-EXTEND subagent (depth 2/2), 2026-10-03.
Parent mandate: extend the L2-METAREUSE meta-reuse harness
(which achieved L2-METAREUSE-PASS K1-K8 with operators
1=COMBINE, 2=SUBSTITUTE, 3=TRUNCATE) with three new reuse
operators: 4=INVERT (reverse a structure), 5=ABSTRACT
(extract a pattern from examples), 6=CONCRETIZE (instantiate
a pattern with specific values). New op ids + mask bits,
new queries each solvable by exactly one of the new
operators, learner selects by trial verification under the
same fixed order. Parent kill bars K1-K8 govern (adapted to
six operators). Non-ledger task. Commits local, never
pushed, explicit pathspecs.

## Step 0: toolchain guard (recorded before any research computation)

- `export PATH="/home/hatch/safebin"` active for all work below.
- `/home/hatch/safebin` holds 49 tools (setup script path
  from prior waves:
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`).
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

## Reading disclosures

- Read the parent lane `l2_adaptive_reuse/` REPORT.md,
  PREREG.md, PREREG_AMENDMENT1.md, NAMECHECK.md,
  learner.zag, world.zag, driver.zag in full. This lane
  EXTENDS that harness; it does not redesign it. All
  pinned-znc-safe Zag idioms are inherited: u8-cell state
  buffer, get32/set32 helpers, cursor emit helpers with a
  single raw-syscall write, counted scan helpers, fold-walk
  with runtime relation discovery, flag-variable style
  instead of deep if-nesting (3 or fewer), no `!(A && B)`
  while-conditions, no `&&` in conditions at all, no
  `as *i32` slices, no `[]u8 as *u8` casts, division/modulo
  instead of bitwise ops.
- The parent PREREG.md file on disk is physically truncated
  mid-sentence (ends "...MR_OP_TRIES++,\\n...[truncated
  12582 chars]" at the mr_adapt description; the committed
  version at 4f043b49f is identically truncated). The
  complete frozen semantics were recovered from the parent
  REPORT.md, PREREG_AMENDMENT1.md, and the committed
  learner.zag/driver.zag sources, which are the
  authoritative frozen record. This lane's PREREG.md is
  written complete and verified byte-whole before freezing.
- New machinery in this lane (mr_invert: stored-relseq
  reversal + strict forward walk; mr_abstract: pattern
  extraction with interface-match entry filter + runtime
  fold discovery; mr_concretize: pattern-MAP source search
  + any-entry candidates + runtime fold discovery with
  novel-folds check; mr_adapt ops 4/5/6 under mask bits
  8/16/32; 44-fact capacity layout shift) is designed from
  this lane's frozen PREREG.md.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md) before any implementation exists.
- [ ] Step 2: implementation (extend learner.zag +
      world.zag + driver.zag, concatenated to mx_full.zag),
      compiled with pinned znc.
- [ ] Step 3: 3/3 runs byte-identical, K7 audit, driver
      audit, REPORT.md with verdict.
