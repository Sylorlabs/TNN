# NAMECHECK: L2-COMBINE-XDOMAIN (cross-domain combine with learner-chosen binding)

Worker: L2-NEWFRONTIER subagent (depth 2/2), 2026-10-02.
Parent mandate: push to a NEW L2 frontier beyond the completed
adaptive-reuse matrix (SUBSTITUTE/TRUNCATE/EXTEND/SPECIALIZE).
This wave tests L2-COMBINE-XDOMAIN: the learner combines TWO old
structures (an arithmetic aggregation MAP and a planning ROUTE
MAP) to solve a cross-domain query, choosing the source pair and
the combination binding itself via a fixed first-verifying-
combination enumeration. Parent kill bars K1-K8 govern.

## Step 0: toolchain guard (recorded before any research computation)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  (from the tnn-rsi worktree); result: SAFEBIN-READY,
  `/home/hatch/safebin` (36 tools, no python).
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns
  NOTHING (rc=1). Verified 2026-10-02 at worker startup, before
  any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler only,
  znc 2026.07.0-dev).
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.
- Pure Zag for all scientific computation. Shell only: znc invocation,
  running binaries, git ops, file movement, sha256sum/cmp/grep checks.

## Reading disclosures

- Read the sibling lane `l2_extend_xdomain/learner.zag`,
  `world.zag`, `driver.zag`, `PREREG.md`, `NAMECHECK.md`, and
  `REPORT.md` (in the tnn-rsi-l2extend worktree) for pinned-znc-safe
  Zag idioms only: u8-cell state buffer, get32/set32 helpers,
  cursor emit helpers with a single raw-syscall write, counted
  scan helpers, fold-walk with runtime relation discovery,
  flag-variable style instead of deep if-nesting, no `!(A && B)`
  while-conditions, no `as *i32` slices, no `[]u8 as *u8` casts.
  The mechanical helpers (alloc, emit, teach, exec, edge, scan,
  foldwalk) are rewritten in the same style; this lane's new
  machinery (cb_agg_seg, cb_route_seg, cb_combine, dual type-16
  provenance, partner-cap collection, (partner-source, binding)
  enumeration with BIND_TRIES accounting) is designed from this
  lane's frozen PREREG.md.
- Read `l2_extend_xdomain/REPORT.md` for the report/verdict format
  precedent (in-Zag bars + shell checks, falsifier list, F-COUNT
  hand derivation).
- This lane is a NEW L2 frontier (combine two structures), not a
  cell of the completed matrix; it does not overlap the extend
  lane's length-choice claim (the load-bearing operation here is
  the learner-chosen (partner-source, binding) pair under a
  first-verifying-combination policy, with a both-sources-
  necessary bar the matrix lanes did not need).

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md)
      at 28c5aa169, before any implementation existed.
- [x] Step 2: implementation (pure Zag learner + world + driver,
      concatenated to cb_full.zag), compiled with pinned znc
      (`znc cb_full.zag -o cb_bin`, rc=0, 43 benign analyzer
      warnings: discarded returns, unused locals; same classes
      as the sibling extend lane).
- [x] Step 3: 3/3 runs byte-identical
      (sha256 a19c97d0964b04700cfd2b96b45ecb8e1989309321a54fe773e55abcc4f6a144
      x3), K7 audit 11/11 patterns zero hits, K3 driver audit
      5/5 zero hits, REPORT.md with verdict
      L2-COMBINE-XDOMAIN-PASS (K1-K8 all PASS, 0 falsifiers,
      F-COUNT silent at A_SEARCH=254/A_EXEC=2).
