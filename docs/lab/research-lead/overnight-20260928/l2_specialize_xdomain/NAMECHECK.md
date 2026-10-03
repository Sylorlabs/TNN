# NAMECHECK: L2-SPECIALIZE-XDOMAIN (general procedure specialized cross-domain, learner-decided)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.

## Step 0: toolchain guard (recorded before any research computation)

- Safebin present at `/home/hatch/safebin` (36 tools including pinned znc).
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns NOTHING (rc=1).
  Verified 2026-10-02 at worker startup, before any research computation.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler only).
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.
- Pure Zag for all scientific computation. Shell only: znc invocation,
  running binaries, git ops, file movement, sha256sum/cmp checks.

## Reading disclosures

- Read `l2_substitute_xdomain/NAMECHECK.md` and `l2_substitute_xdomain/PREREG.md`
  (predecessor lane, verdict L2-SUBSTITUTE-XDOMAIN-PASS): cross-domain
  adapter idiom (capability search across domains, entry/fold discovery,
  arity pair-interface check, execution verification, type-16 provenance,
  driver-flag causal controls), kill-bar structure K1-K8, and the pinned-znc
  stdout workaround (one preallocated buffer, single raw-syscall write).
- Skimmed `l2_substitute_xdomain/xa_full.zag` for pinned-znc-safe Zag idioms
  only (u8-cell state, get32/set32, cursor emit helpers ob_app/ob_i32,
  `_zag_slice_ptr` + `_zag_raw_syscall` flush loop, no `as *i32` slices,
  no `!(A && B)` while-conditions, shallow if-nesting). No code copied;
  this lane's learner is designed from this lane's frozen PREREG.md.
  All function names use the `xs_` prefix; trace tags use `XS-`.
- This lane tests a DIFFERENT L2 operation: SPECIALIZE (narrow a general
  parametric procedure by fixing parameters, decided by the learner via
  trial-and-verification over inventory-derived candidates), not
  SUBSTITUTE. No overlap in claim.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md).
- [x] Step 2: implementation (xs_learner.zag, xs_world.zag, xs_driver.zag,
  xs_full.zag, xs_bin). Two one-line diff-class fixes only:
  adapter_trial call arity (drop ob/atp), ABLATE retire moved
  post-QB per AMENDMENT3 (matches frozen baseline). Binary compiles
  with pinned znc (exit 0).
- [x] Step 3: 3/3 runs byte-identical (sha256
  15affdeb0d6d218a34606c4980745bdcf2cea8e47150bac9c11eadfd6835fb4c),
  REPORT.md. Verdict: L2-SPECIALIZE-XDOMAIN-PASS. All 8 kill
  bars PASS, zero falsifiers.
