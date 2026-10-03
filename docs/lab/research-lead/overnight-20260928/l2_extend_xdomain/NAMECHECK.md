# NAMECHECK: L2-EXTEND-XDOMAIN (cross-domain extend with learner-chosen length)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Parent mandate: test L2 EXTEND with cross-domain transfer: a
learned procedure X from domain A is lengthened by a
learner-chosen extension and applied in domain B, where the
unextended X provably fails. Parent kill bars K1-K8 govern.

## Step 0: toolchain guard (recorded before any research computation)

- `export PATH="$HOME/safebin"` active for all work below.
- `$HOME/safebin` contains 36 allowed tools including the pinned
  `znc` (znc 2026.07.0-dev); `python3`/`python` do not resolve.
- `which python3` returns NOTHING (rc=1). `which python` returns
  NOTHING (rc=1). Verified 2026-10-02 at worker startup, before
  any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler only).
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.
- Pure Zag for all scientific computation. Shell only: znc invocation,
  running binaries, git ops, file movement, sha256sum/cmp/grep checks.

## Reading disclosures

- Read the sibling lane `l2_truncate_xdomain/PREREG.md`,
  `NAMECHECK.md`, and `tx_full.zag` (learner + world + driver,
  concatenated) for pinned-znc-safe Zag idioms only: u8-cell state
  buffer, get32/set32 helpers, cursor emit helpers with a single
  raw-syscall write, counted scan helpers, fold-walk with runtime
  relation discovery, flag-variable style instead of deep
  if-nesting, no `!(A && B)` while-conditions, no `as *i32`
  slices. No code copied verbatim; this lane's learner (ex_
  prefix, EX- tags, own enumeration direction and EXT_TRIES
  counter) is designed from this lane's frozen PREREG.md.
- Read `l2_substitute_xdomain/PREREG.md` for the five-arm driver
  idiom and in-Zag bar evaluation precedent (four arms used here:
  FULL / NOEXTEND / ABLATE-X / FRESH; the reuse check is a
  falsifier-guarded second query inside FULL, as in the sibling).
- This lane is the EXTEND cell of the L2 operation matrix with
  cross-domain transfer; it does not overlap the truncate lane's
  cut-point claim (the load-bearing operation here is the
  learner-chosen extension length under a shortest-first
  verifying policy, with a minimality bar the truncate lane did
  not need).

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md)
      at b6652e3d6, before any implementation existed.
- [x] Step 2: implementation (pure Zag learner + world + driver,
      concatenated to ex_full.zag), compiled with pinned znc
      (`znc ex_full.zag -o ex_bin`, rc=0, 43 benign analyzer
      warnings: discarded returns, unused locals; same classes
      as the sibling lane).
- [x] Step 3: 3/3 runs byte-identical
      (sha256 d8dac499d75487d64c514216314523180117b52fe31bc58440f9d71eec80981d
      x3), K7 audit 12/12 patterns zero hits, REPORT.md with
      verdict L2-EXTEND-XDOMAIN-PASS (K1-K8 all PASS, 0
      falsifiers, F-COUNT silent at A_SEARCH=272/A_EXEC=2).
