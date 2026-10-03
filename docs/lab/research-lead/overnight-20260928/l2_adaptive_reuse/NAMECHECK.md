# NAMECHECK: L2-METAREUSE (learner-selected reuse operator)

Worker: L2-ADAPTIVE-REUSE subagent (depth 2/2), 2026-10-03.
Parent mandate: push L2 adaptive reuse to a NEW frontier beyond
the completed matrix (SUBSTITUTE/TRUNCATE/EXTEND/SPECIALIZE,
all PASS) and the L2-COMBINE-XDOMAIN wave (PASS, 2026-10-02).
This wave tests L2-METAREUSE: the learner holds THREE reuse
operators (COMBINE, SUBSTITUTE, TRUNCATE) and, per query,
selects WHICH operator to apply by trial verification in a
fixed generic order. The driver never assigns an operator to a
query. Parent kill bars K1-K8 govern.

## Step 0: toolchain guard (recorded before any research computation)

- `export PATH="/home/hatch/safebin"` active for all work below.
- `/home/hatch/safebin` holds 49 tools (safebin; setup script
  path from prior waves:
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`).
- `which python3` returns NOTHING (rc=1). `which python`
  returns NOTHING (rc=1). Verified 2026-10-03 at worker
  startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler
  only, znc 2026.07.0-dev).
- Any forbidden-executable invocation is PROCESS-FAIL. None
  occurred.
- Pure Zag for all scientific computation. Shell only: znc
  invocation, running binaries, git ops, file movement,
  sha256sum/cmp/grep checks.

## Reading disclosures

- Read the sibling lane `l2_newfrontier/learner.zag`,
  `world.zag`, `driver.zag`, `PREREG.md`, `NAMECHECK.md`, and
  `REPORT.md` for pinned-znc-safe Zag idioms only: u8-cell
  state buffer, get32/set32 helpers, cursor emit helpers with
  a single raw-syscall write, counted scan helpers,
  fold-walk with runtime relation discovery, flag-variable
  style instead of deep if-nesting (3 or fewer), no `!(A && B)`
  while-conditions, no `&&` in conditions at all, no `as *i32`
  slices, no `[]u8 as *u8` casts, division/modulo instead of
  bitwise ops. The mechanical helpers (alloc, emit, teach,
  exec, edge, scan, foldwalk, agg_seg, route_seg, buildwin)
  are rewritten in the same style; this lane's new machinery
  (mr_substitute with entry-candidate collection, mr_truncate
  with nf-descending prefix trials, mr_adapt fixed-order op
  enumeration under OP_MASK, MR_OP/MR_OP_TRIES/MR_OP_DECIDED
  state) is designed from this lane's frozen PREREG.md.
- Read `l2_newfrontier/REPORT.md` for the report/verdict
  format precedent (in-Zag bars + shell checks, falsifier
  list, F-COUNT hand derivation).
- Read `l2_substitute_xdomain/REPORT.md` (partial) to keep
  the SUBSTITUTE operator's meaning consistent with the
  completed matrix (interface adaptation of one learned
  structure; here in the narrow form of entry-relation
  substitution, disclosed in the prereg).
- This lane is a NEW L2 frontier (learner-selected reuse
  operator), not a cell of the completed matrix and not a
  repeat of the combine lane; the load-bearing claim is the
  per-query OPERATOR CHOICE (same fixed order and same mask
  yield different operators on different queries), which no
  prior wave tested.

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (this file +
      PREREG.md) at 4f043b49f, before any implementation existed.
- [x] Step 2: implementation (pure Zag learner + world +
      driver, concatenated to mr_full.zag, 1585 lines),
      compiled with pinned znc (`znc mr_full.zag -o mr_bin`,
      rc=0, 59 benign analyzer warnings: A0102
      ignored-return-value class + two E0101/E0102
      constant-fold notes in driver arithmetic, same
      classes as the sibling lanes).
- [x] Step 3: 3/3 runs byte-identical
      (sha256 5fb7423cce26c3a34ceb52f201591e2349ea7c62ae56f0865dc8c0e3f0bbe6d8
      x3), K7 audit 12/12 patterns zero hits, driver
      audit 5/5 zero hits, REPORT.md with verdict
      L2-METAREUSE-PASS (K1-K8 all PASS, 0 falsifiers,
      F-COUNT silent at QC 260/2, QS 214/2, QT 203/2).
      One pre-verdict transparent amendment
      (PREREG_AMENDMENT1.md, commit d57f14216): QC-AS
      280->260 pure hand-derivation arithmetic
      correction (b=1 tail attempted only when the
      AGG-head succeeds); no counting-rule or code
      change.
