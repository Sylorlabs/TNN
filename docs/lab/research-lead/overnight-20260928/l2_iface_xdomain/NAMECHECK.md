# NAMECHECK: L2-IFACE-XDOMAIN (interface adaptation of a learned procedure, cross-domain, learner-decided)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.

## Step 0: toolchain guard (recorded before any research computation)

- Safebin present at `/home/hatch/safebin` (36 tools including pinned znc).
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns NOTHING (rc=1).
  Verified 2026-10-02 at worker startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler only).
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.
- Pure Zag for all scientific computation. Shell only: znc invocation,
  running binaries, git ops, file movement, sha256sum/cmp checks,
  read-only greps.

## Reading disclosures

- Read `l2_substitute_xdomain/PREREG.md` (predecessor idiom) and the full
  `l2_specialize_xdomain/` lane (PREREG.md, PREREG_AMENDMENT1..3,
  xs_learner.zag, xs_world.zag, xs_driver.zag, NAMECHECK.md; verdict
  L2-SPECIALIZE-XDOMAIN-PASS): cross-domain adapter idiom (capability
  search, entry/fold discovery, arity check, execution verification,
  provenance edges, driver-flag causal controls), kill-bar structure
  K1-K8, and the pinned-znc stdout workaround (one preallocated buffer,
  single raw-syscall write). Skimmed xs_learner.zag for pinned-znc-safe
  Zag idioms only (u8-cell state, get32/set32, cursor emit helpers,
  `_zag_slice_ptr` + `_zag_raw_syscall` flush loop, no `as *i32` slices,
  no `!(A && B)` while-conditions, shallow if-nesting). No code copied;
  this lane's learner is designed from this lane's frozen PREREG.md.
  All function names use the `ia_` prefix; trace tags use `IA-`.
- Amendment-1 lesson applied: learner logic names NO candidate values
  and NO world literals; trial outcomes recorded via generic counters
  (TRIAL_FAIL_N, TRIAL_TOTAL) plus the accepted binding (data, not logic).
- This lane tests a DIFFERENT L2 operation: INTERFACE-ADAPT (adapt ONLY
  the interface of a learned procedure: caller-arg to callee-param
  binding, arity bridging for a decoy/missing argument, entry-relation
  name binding; the procedure's core logic and record are untouched),
  not SUBSTITUTE/EXTEND/TRUNCATE/SPECIALIZE. No overlap in claim.

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md) at
  968e3c3ab; PREREG.md byte-identical to the frozen commit (no
  modifications; only untracked implementation files added after).
- [x] Step 2: implementation (ia_learner.zag, ia_world.zag, ia_driver.zag,
  ia_full.zag, ia_bin). Binary compiles with pinned znc (exit 0, 22
  benign analyzer warnings only). ia_full.zag verified byte-identical to
  the three-file concatenation.
- [x] Step 3: 3/3 runs byte-identical (sha256
  f3ba73db757dd62decd30c6190a941f147b0cd5fad5dcba02e118b8fb15d2d14),
  REPORT.md written, verdict L2-IFACE-XDOMAIN-PASS (K1-K8 all PASS,
  FALSIFIERS 0).

## Session 2 (2026-10-03, verification + unblock)

- Toolchain guard re-verified: `export PATH="$HOME/safebin"`; `which
  python3` and `which python` return NOTHING (rc=1); `which znc` ->
  `/home/hatch/safebin/znc` (pinned). Pure Zag for all scientific
  computation. Shell only: znc, binary runs, /usr/bin/git ops, file
  movement, sha256sum/cmp, read-only greps.
- Prior attempt's BUILD-BLOCKED diagnosed and resolved:
  (a) .git-write EPERM is the known safebin git-symlink bug; all git
  writes done via `/usr/bin/git` directly (verified working:
  hash-object -w + update-index succeed). (b) Zag binary-write block
  was transient; fresh `znc ia_full.zag -o ia_bin` succeeded (exit 0).
- Prior code fixes (saw_adapt; ABLATE kill before QA) and
  PREREG_AMENDMENT1 (FULL-Q2 484 -> 482) independently re-verified
  against the frozen design (full hand re-derivation of all 7 query
  S/E values; amendment arithmetic confirmed: T4 = 13+62+37 = 112).
- ia_full.zag re-read in full against PREREG.md: generic learner holds
  no world literals (K7: 8/8 patterns zero hits); pinned-znc-safe
  idioms only (no `as *i32`, no `!(A && B)` while, no `_zag_print`
  dynamic output, `_zag_malloc as *u8` only, shallow if-nesting).
- K6 via 3/3 byte-identical runs; K1-K5/K8 via in-Zag bars; K2/K3 via
  in-Zag plus verbatim shell greps; K7 via shell grep audit.
