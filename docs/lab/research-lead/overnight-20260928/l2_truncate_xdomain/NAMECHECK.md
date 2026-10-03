# NAMECHECK: L2-TRUNCATE-XDOMAIN (cross-domain truncate with learner-chosen cut point)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Parent mandate: L2 ADAPTIVE REUSE is top priority; the L2 operation
matrix (extend, truncate, specialize, substitute, interface-adapt)
is complete at L1/within-domain. This lane tests TRUNCATE across
domains: a learned procedure X from domain A is shortened by a
learner-chosen cut point and applied in domain B, where the full
X provably fails.

## Step 0: toolchain guard (recorded before any research computation)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  from `~/workspace/tnn-rsi`:
  `linked: 36 tools`,
  `znc: OK (.../src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns NOTHING (rc=1).
  Verified 2026-10-02 at worker startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler only).
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.
- Pure Zag for all scientific computation. Shell only: znc invocation,
  running binaries, git ops, file movement, sha256sum/cmp checks.

## Reading disclosures

- Read `l2_substitute_xdomain/PREREG.md` and `NAMECHECK.md` (sibling
  lane, cross-domain L2 operation precedent): kill-bar structure,
  five-arm driver idiom, in-Zag bar evaluation, frozen hand-derived
  cost counts with F-COUNT, K6 grep audit, driver-flag causal
  controls (ADAPT_ON precedent -> TRUNC_ON here).
- Read `l2_substitute_xdomain/learner.zag` (937 lines) for
  pinned-znc-safe Zag idioms only: u8-cell state buffer,
  get32/set32 helpers, cursor emit helpers with single raw-syscall
  write, counted scan helpers (xa_tick/xa_tickm/xa_exec),
  fold-walk with runtime relation discovery, flag-variable style
  instead of deep if-nesting, no `!(A && B)` while-conditions,
  no `as *i32` slices. No code copied; this lane's learner
  (tx_ prefix, TX- tags, own 40-byte MAP layout for 9-rel sources)
  is designed from this lane's frozen PREREG.md.
- Read `l2_substitute_xdomain/driver.zag` and `world.zag` for the
  experiment-side idioms (teaching, arms, answer provenance).
- This lane is the TRUNCATE cell of the L2 operation matrix with
  cross-domain transfer; it does not overlap the substitute lane's
  interface-adaptation claim (no arity/pair-interface machinery
  here; the load-bearing operation is the learner-chosen cut).

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md)
      at 7a58fbfd4, before any implementation existed.
- [x] Step 2: implementation (pure Zag learner + world + driver),
      compiled with pinned znc (`znc tx_full.zag -o tx_bin`,
      rc=0, 42 benign analyzer warnings: discarded returns,
      unused locals; same classes as the sibling lane).
- [x] Step 3: 3/3 runs byte-identical
      (sha256 45e010f4494d12b8742d8aeb0a2b2f9a5229bc46386440ade6ab651c8afc82ff
      x3), K6 audit 12/12 patterns zero hits, REPORT.md with
      verdict L2-TRUNCATE-XDOMAIN-PASS (K1-K8 all PASS, 0
      falsifiers).
